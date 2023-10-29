""" Generate preview and sale versions of albums for itchio et al """
# pylint:disable=too-many-arguments,import-outside-toplevel

import argparse
import base64
import collections
import concurrent.futures
import copy
import functools
import itertools
import json
import logging
import os
import os.path
import shutil
import subprocess
import typing

from . import images, util

try:
    from .__version__ import __version__
except ImportError:
    __version__ = '(unknown)'

LOGGER = logging.getLogger(__name__)


def wait_futures(futures):
    """ Waits for some futures to complete. If any exceptions happen, they propagate up. """
    for task in concurrent.futures.as_completed(futures):
        task.result()


def generate_id3_apic(album, track, size):
    """ Generate the APIC tags for an mp3 track
    :param dict album: The album's data
    :param dict track: The track's data
    :param int size: Maximum rendition size
    """
    from mutagen import id3

    art_tags = []
    for container, picture_type, desc in (
        (album, id3.PictureType.COVER_FRONT, 'Front Cover'),
        (track, id3.PictureType.OTHER, 'Song Cover')
    ):
        if 'artwork_path' in container:
            try:
                img_data = images.generate_blob(container['artwork_path'],
                                                size=size, ext='jpeg')
                art_tags.append(id3.APIC(id3.Encoding.UTF8,
                                         'image/jpeg',
                                         picture_type,
                                         desc,
                                         img_data))
            except Exception:  # pylint:disable=broad-exception-caught
                LOGGER.exception(
                    "Got an error converting image %s", container['artwork_path'])
    return art_tags


def run_encoder(infile, outfile, args):
    """ Run an encoder; if the encode process fails, delete the file

    :param str outfile: The output file path
    :param list args: The entire arglist (including output file path)
    """

    if not os.path.isfile(infile):
        raise FileNotFoundError(f"Can't encode {outfile}: {infile} not found")

    if util.is_newer(infile, outfile):
        try:
            subprocess.run([util.ffmpeg_path(),
                            '-hide_banner', '-loglevel', 'error',
                            '-i', infile,
                            *args,
                            '-y', outfile], check=True,
                           capture_output=True,
                           creationflags=getattr(
                               subprocess, 'CREATE_NO_WINDOW', 0),
                           )
        except subprocess.CalledProcessError as err:
            os.remove(outfile)
            raise RuntimeError(
                f'Error {err.returncode} encoding {outfile}: {err.output}') from err
        except KeyboardInterrupt as err:
            os.remove(outfile)
            raise RuntimeError(
                f'User aborted while encoding {outfile}') from err


def encode_mp3(in_path, out_path, idx, album, track, encode_args, cover_art=None):
    """ Encode a track as mp3

    :param str in_path: Input file path
    :param str out_path: Output file path
    :param str idx: Track number
    :param dict album: Album metadata
    :param dict track: Track metadata
    :param str encode_args: Arguments to pass along to LAME
    :param str cover_art: Artwork rendition size
    """
    from mutagen import id3

    run_encoder(in_path, out_path, encode_args)

    try:
        tags = id3.ID3(out_path)
    except id3.ID3NoHeaderError:
        tags = id3.ID3()

    frames = {
        id3.TYER: str(album['year']) if 'year' in album else None,
        id3.TALB: album.get('title'),

        id3.TPE1: track.get('artist', album.get('artist')),
        id3.TPE2: album.get('artist'),
        id3.TOPE: track.get('cover_of', album.get('cover_of')),

        id3.TRCK: str(idx),
        id3.TIT1: track.get('group'),
        id3.TIT2: track.get('title'),

        id3.TCON: track.get('genre', album.get('genre')),
        id3.TCOM: track.get('composer', album.get('composer')),
        id3.USLT: '\n'.join(track['lyrics']) if 'lyrics' in track else None,

        id3.COMM: track.get('comment'),
    }

    for frame, val in frames.items():
        if val:
            LOGGER.debug("%s: Setting %s to %s", out_path, frame.__name__, val)
            tags.setall(frame.__name__, [frame(text=val)])

    if cover_art:
        art_tags = generate_id3_apic(album, track, cover_art)
        if art_tags:
            LOGGER.debug("%s: Adding %d artworks", out_path, len(art_tags))
            tags.setall('APIC', art_tags)

    tags.save(out_path, v2_version=3)
    LOGGER.info("Finished writing %s", out_path)


def track_tag_title(track):
    """ Get the tag title for a track """
    title = track.get('title', 'Unknown Track')
    if track.get('explicit'):
        title += ' [explicit]'


def tag_vorbis(tags, idx, album, track):
    """ Add a vorbis comment section to an ogg/flac file """
    frames = {
        'ARTIST': track.get('artist', album.get('artist')),
        'ALBUM': album.get('title'),
        'TITLE': track.get('title'),
        'TRACKNUMBER': str(idx),
        'GENRE': track.get('genre', album.get('genre')),
        'LYRICS': '\n'.join(track['lyrics']) if 'lyrics' in track else None,
        'DESCRIPTION': track.get('comment'),
    }
    if track.get('cover_of', album.get('cover_of')):
        # Covers are handled weirdly in Vorbiscomment; see https://dogphilosophy.net/?page_id=66
        frames.update({
            'ARTIST': track.get('cover_of', album.get('cover_of')),
            'PERFORMER': track.get('artist', album.get('artist'))
        })

    for frame, val in frames.items():
        if val:
            tags[frame] = val


def get_flac_picture(artwork_path, size):
    """ Generate a FLAC picture frame """
    from mutagen import flac, id3
    img = images.generate_image(artwork_path, size)

    pic = flac.Picture()
    pic.type = id3.PictureType.COVER_FRONT
    pic.width = img.width
    pic.height = img.height
    pic.mime = "image/jpeg"
    pic.data = images.generate_blob(artwork_path, size, ext='jpeg')

    return pic


def encode_ogg(in_path, out_path, idx, album, track, encode_args, cover_art):
    """ Encode a track as ogg vorbis """
    from mutagen import oggvorbis

    run_encoder(in_path, out_path, encode_args)

    tags = oggvorbis.OggVorbis(out_path)
    tag_vorbis(tags, idx, album, track)

    if cover_art and 'artwork_path' in track:
        picture_data = get_flac_picture(
            track['artwork_path'], cover_art).write()
        tags['metadata_block_picture'] = [
            base64.b64encode(picture_data).decode("ascii")]

    tags.save(out_path)
    LOGGER.info("Finished writing %s", out_path)


def encode_flac(in_path, out_path, idx, album, track, encode_args, cover_art):
    """ Encode a track as ogg vorbis """
    from mutagen import flac

    run_encoder(in_path, out_path, encode_args)

    tags = flac.FLAC(out_path)
    tag_vorbis(tags.tags, idx, album, track)

    if cover_art and 'artwork_path' in track:
        tags.add_picture(get_flac_picture(track['artwork_path'], cover_art))

    tags.save(out_path)
    LOGGER.info("Finished writing %s", out_path)


def make_web_preview(input_dir, output_dir, album, protections, futures):
    """ Generate the embedded preview player """
    LOGGER.info("Preview: Waiting for %s (%d tasks)", output_dir, len(futures))
    wait_futures(futures)
    LOGGER.info("Preview: Building player in %s", output_dir)

    from .players import blamscamp
    player = blamscamp.Player()

    @functools.lru_cache()
    def gen_art_preview(in_path: str) -> typing.Dict[str, str]:
        """ Generate web preview art for the given file

        :param str in_path: Input path of the source file
        :param str out_dir: Output directory

        :returns: tuple of the 1x and 2x renditions of the artwork
        """
        LOGGER.debug("generating preview art for %s", in_path)
        return {spec: images.generate_rendition(in_path, output_dir, size)
                for spec, size in player.art_rendition_sizes.items()}

    if 'artwork' in album:
        LOGGER.debug("album art")
        album['artwork_preview'] = gen_art_preview(
            os.path.join(input_dir, album['artwork']))
        protections |= set(album['artwork_preview'].values())
        LOGGER.debug("added preview protections %s", album['artwork_preview'])

    for track in album['tracks']:
        if 'artwork' in track:
            track['artwork_preview'] = gen_art_preview(
                os.path.join(input_dir, track['artwork']))
            protections.add(track['artwork_preview'].values())
            LOGGER.debug("added preview protections %s",
                         track['artwork_preview'])

    player.convert(album, output_dir, protections, version=__version__)

    LOGGER.info("Preview: Finished generating web preview at %s; protections=%s",
                output_dir, protections)


def clean_subdir(path: str, allowed: typing.Set[str], futures):
    """ Clean up a subdirectory of extraneous files """
    LOGGER.info("Cleanup: Waiting for %s (%d tasks)", path, len(futures))
    wait_futures(futures)
    LOGGER.info("Cleaning up directory %s", path)

    LOGGER.info("Allowed in %s: %s", path, allowed)
    for file in os.scandir(path):
        if file.name not in allowed:
            LOGGER.info("Removing extraneous file %s", file.path)
            if file.is_dir():
                shutil.rmtree(file)
            else:
                os.remove(file)


def submit_butler(config, target, futures):
    """ Submit the directory to itch.io via butler """
    channel = f'{config.butler_target}:{config.butler_prefix}{target}'
    output_dir = os.path.join(config.output_dir, target)

    LOGGER.info("Butler: Waiting for %s (%d tasks)", output_dir, len(futures))
    wait_futures(futures)

    LOGGER.info("Butler: pushing '%s' to channel '%s'", output_dir, channel)
    try:
        subprocess.run([config.butler_path, 'push', *config.butler_args,
                       output_dir, channel],
                       stdin=subprocess.DEVNULL,
                       capture_output=True,
                       check=True,
                       creationflags=getattr(
                           subprocess, 'CREATE_NO_WINDOW', 0),
                       )
    except subprocess.CalledProcessError as err:
        if 'Please set BUTLER_API_KEY' in err.output.decode():
            raise RuntimeError("Butler login needed") from err
        raise RuntimeError(f'Butler error: {err.output}') from err


def seconds_to_timestamp(duration):
    """ Convert a duration (in seconds) to a timestamp like h:mm:ss """
    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)

    if hours:
        return f'{hours:.0f}:{minutes:02.0f}:{seconds:02.0f}'
    return f'{minutes:.0f}:{seconds:02.0f}'


def seconds_to_datetime(duration):
    """ Convert a duration (in seconds) to an HTML5 datetime like 3h 5m 10s """
    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)

    if hours:
        return f'{hours:.0f}h {minutes:.0f}m {seconds:.0f}s'
    return f'{minutes:.0f}m {seconds:.0f}s'


def encode_tracks(config, album, protections, pool, futures):
    """ run the track encode process """

    for idx, track in enumerate(album['tracks'], start=1):
        title = track.get('title', f'track {idx}')
        track['title'] = title

        base_filename = f'{idx:02d} '
        if 'artist' in track:
            base_filename += f"{track['artist']} - "
        base_filename += title
        base_filename = util.slugify_filename(base_filename)

        def out_path(fmt, ext=None):
            # pylint:disable=cell-var-from-loop
            protections[fmt].add(f'{base_filename}.{ext or fmt}')
            return os.path.join(config.output_dir, fmt, f'{base_filename}.{ext or fmt}')

        input_filename = os.path.join(config.input_dir, track['filename'])

        if 'artwork' in track:
            track['artwork_path'] = os.path.join(
                config.input_dir, track['artwork'])

        if 'lyrics' in track and isinstance(track['lyrics'], str):
            lyricfile = os.path.join(config.input_dir, track['lyrics'])
            if os.path.isfile(lyricfile):
                track['lyrics'] = util.read_lines(lyricfile)

        duration = util.get_audio_duration(input_filename)
        track['duration'] = seconds_to_timestamp(duration)
        track['duration_datetime'] = seconds_to_datetime(duration)

        # generate preview track, if desired
        if config.do_preview and not track.get('hidden') and track.get('preview', True):
            track['preview_mp3'] = f'{base_filename}.mp3'
            futures['encode-preview'].append(pool.submit(
                encode_mp3,
                input_filename,
                out_path('preview', 'mp3'),
                idx, album, track, config.preview_encoder_args,
                cover_art=300))

        if config.do_mp3:
            futures['encode-mp3'].append(pool.submit(
                encode_mp3,
                input_filename,
                out_path('mp3'),
                idx, album, track, config.mp3_encoder_args, cover_art=1500))

        if config.do_ogg:
            futures['encode-ogg'].append(pool.submit(
                encode_ogg,
                input_filename,
                out_path('ogg'),
                idx, album, track, config.ogg_encoder_args, cover_art=1500))

        if config.do_flac:
            futures['encode-flac'].append(pool.submit(
                encode_flac,
                input_filename,
                out_path('flac'),
                idx, album, track, config.flac_encoder_args, cover_art=1500))


def make_zipfile(input_dir, output_file, futures):
    """ Make a .zip archive for manual uploading """
    LOGGER.info("Zipfile: Waiting for %s (%d tasks)",
                input_dir, len(futures))
    wait_futures(futures)

    LOGGER.info("Building %s.zip from directory %s", output_file, input_dir)
    shutil.make_archive(output_file, 'zip', input_dir)


def process(config, album, pool, futures):
    """
    Process the album given the parsed config and the loaded album data

    :param options.Options config: Encoder configuration
    :param dict album: :doc:`Album metadata <metadata>`
    :param concurrent.Futures.Executor pool: The threadpool to submit tasks to
    :param dict futures: Pending tasks for a particular build phase; should be
        a :py:class:`collections.defaultdict(list)` or similar

    Each format has the following phases, each one depending on the previous:

    1. ``encode``: Encodes and tags the output files
    2. ``build``: Builds any extra files (e.g. the web player)
    3. ``clean``: Directory cleanup tasks

    And then these two phases are shared across formats but depend on ``clean``
    (and may run in parallel):

    1. ``butler``: Pushes the build to itch.io via the butler tool
    2. ``zip``: Builds the local .zip file for manual uploading

    When this function exits, the futures dict will be fully-populated with a
    mapping from each phase to a list of :py:class:`concurrent.futures.Future` for
    that phase.

    You can wait on each phase's list separately, or you can collapse it with e.g.:

    .. code-block:: python

        all_futures = list(itertools.chain(*futures.values()))
        concurrent.futures.wait(all_futures)

    """
    # pylint:disable=too-many-branches

    # Make a copy of the dict, since some pipeline steps mutate it and we want
    # to be nice to the caller
    album = copy.deepcopy(album)

    # Coerce album configuration to app configuration if it hasn't been specified
    for attrname, default in (
        ('do_preview', True),
        ('do_mp3', True),
        ('do_ogg', True),
        ('do_flac', True),
        ('do_zip', True),
        ('do_butler', bool(album.get('butler_target'))),
        ('butler_target', ''),
        ('butler_prefix', '')
    ):
        LOGGER.debug("config.%s = %s", attrname, getattr(config, attrname))
        if getattr(config, attrname) is None:
            setattr(config, attrname, album.get(attrname, default))
            LOGGER.debug("config.%s unset, using album value %s",
                         attrname, getattr(config, attrname))

    LOGGER.info("Starting encode with configuration: %s", config)

    formats = set()
    for target in ('preview', 'mp3', 'ogg', 'flac'):
        attrname = f'do_{target}'
        if getattr(config, attrname) is None:
            LOGGER.debug(
                "config.%s is None, falling back to album spec", attrname)
            setattr(config, attrname, album.get(attrname, True))

        if getattr(config, attrname):
            LOGGER.info("Building %s", target)
            formats.add(target)
            os.makedirs(os.path.join(
                config.output_dir, target), exist_ok=True)

    if config.do_butler and not (config.butler_path and shutil.which(config.butler_path)):
        LOGGER.warning("Couldn't find tool 'butler'; disabling upload")
        config.do_butler = False

    if not formats:
        raise RuntimeError("No targets specified and nothing to do")

    protections: typing.Dict[str, typing.Set[str]
                             ] = collections.defaultdict(set)

    if 'artwork' in album:
        album['artwork_path'] = os.path.join(
            config.input_dir, album['artwork'])

    # this populates encode-XXX futures
    encode_tracks(config, album, protections, pool, futures)

    # make build block on encode for all targets
    for target in formats:
        futures[f'build-{format}'].append(pool.submit(wait_futures,
                                                      futures[f'encode-{format}']))

    if config.do_preview:
        futures['build-preview'].append(pool.submit(make_web_preview,
                                                    config.input_dir,
                                                    os.path.join(config.output_dir,
                                                                 'preview'),
                                                    album, protections['preview'],
                                                    futures['encode-preview']))

    # make clean block on build for all targets
    for target in formats:
        if config.do_cleanup:
            futures[f'clean-{target}'].append(pool.submit(
                clean_subdir, os.path.join(config.output_dir, target),
                protections[target], futures[f'build-{target}']))
        else:
            futures[f'clean-{target}'].append(pool.submit(
                wait_futures, futures[f'build-{target}']))

    if config.do_butler and config.butler_target:
        for target in formats:
            futures['butler'].append(pool.submit(
                submit_butler,
                config,
                target,
                futures[f'clean-{target}']))

    if config.do_zip:
        filename_parts = [album.get(field)
                          for field in ('artist', 'title')
                          if album.get(field)]
        for target in formats:
            fname = os.path.join(config.output_dir,
                                 util.slugify_filename(
                                     ' - '.join([*filename_parts, target])))
            futures['zip'].append(pool.submit(
                make_zipfile,
                os.path.join(config.output_dir, target),
                fname,
                futures[f'clean-{target}'])
            )
