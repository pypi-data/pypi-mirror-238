import os
from pathlib import Path
import re
import readline  # this is imported to fix input usage
import sys

import requests

import trulogger


import mutagen
from mutagen.id3 import APIC, TIT2, TALB, TPE1, TPE2, TRCK, TDRC, TPOS, TCON
from mutagen.mp4 import MP4Cover

from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic, setup_oauth


# pylint: disable=too-many-instance-attributes
class TruMusic:
    supported_file_extensions = ['mp3', 'm4a']

    field_maps = {
        'MP4': {
            "artist": "\xa9ART",
            "album_artist": "aART",
            "album": "\xa9alb",
            "title": "\xa9nam",
            "year": "\xa9day",
            "track": "trkn",
            "disk": "disk",
            "cover": "covr",
        },
        "MP3": {
            "artist": TPE1,
            "album_artist": TPE2,
            "album": TALB,
            "title": TIT2,
            "year": TDRC,
            "track": TRCK,
            "disk": TPOS,
            "cover": APIC,
            # "genre": TCON,
        }
    }

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            ext: str = '.mp3',
            dry_run: bool = False,
            quiet: bool = False,
            verbose: bool = False,
    ):
        self.home = str(Path.home())
        self._base_dest_dir = None
        self._oauth_file = None
        self._yt_music = None
        self._dest_dir = None

        self.current_filename = None

        self.ext = ext
        self.dry_run = dry_run
        self.logger = trulogger.TruLogger({'verbose': verbose})
        self.quiet = quiet

        self._image_file: str = None

        self.album_info: dict = {}

        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.ext,
            }],
            "progress_hooks": [self.yt_dlp_monitor]
        }

    @property
    def base_dest_dir(self):
        if self._base_dest_dir is None:
            self._base_dest_dir = f"{self.home}/Music/TruMusic"

        if not os.path.isdir(self._base_dest_dir):
            os.makedirs(self._base_dest_dir)

        return self._base_dest_dir

    @base_dest_dir.setter
    def base_dest_dir(self, value):
        self._base_dest_dir = value

    @property
    def oauth_file(self):
        if self._oauth_file is None:
            self._oauth_file = f"{self.home}/.config/ytmusicapi/oauth.json"

        if not os.path.isfile(self._oauth_file):
            # create the oauth file directory if it doesn't exist
            if not os.path.isdir(os.path.dirname(self._oauth_file)):
                os.makedirs(os.path.dirname(self._oauth_file))
            # open the browser to authenticate the user
            setup_oauth(filepath=self._oauth_file, open_browser=True)

        return self._oauth_file

    @oauth_file.setter
    def oauth_file(self, value):
        self._oauth_file = value

    @property
    def dest_dir(self):
        return self._dest_dir

    @dest_dir.setter
    def dest_dir(self, value):
        self._dest_dir = f"{self.base_dest_dir}/{value}"
        if not os.path.exists(self._dest_dir):
            if not self.dry_run:
                os.makedirs(self._dest_dir)

    @property
    def image_file(self):
        return self._image_file

    @image_file.setter
    def image_file(self, thumbnails):
        _thumbnails = {thumbnail.get("width"): thumbnail.get("url") for thumbnail in thumbnails}
        cover_url = _thumbnails.get(max(_thumbnails))
        img_data = requests.get(cover_url, timeout=30).content
        self._image_file = f"{self.dest_dir}/cover.jpg"
        if not self.dry_run:
            with open(self._image_file, 'wb') as handler:
                handler.write(img_data)

    @property
    def yt_music(self):
        if self._yt_music is None:
            self._yt_music = YTMusic(self.oauth_file)
        return self._yt_music

    def yt_dlp_monitor(self, data):
        if data['status'] == 'finished':
            info_dict = data.get('info_dict')
            self.current_filename = info_dict.get('filename').replace(f".{info_dict.get('ext')}", f".{self.ext}")

    @staticmethod
    def _clean_string(title):
        return re.sub(' +', ' ', re.sub('[/|⧸]', '', title))

    @staticmethod
    def _clean_search_string(title):
        return title.replace('⧸', '/')

    def _set_log_prefix(self, prefix=None):
        _prefix = ""
        if self.dry_run:
            _prefix += "[ DRY RUN ] "
        if prefix is not None:
            if isinstance(prefix, list):
                for item in prefix:
                    _prefix += f"[ {item} ] "
            elif isinstance(prefix, str):
                _prefix += f"[ {prefix} ] "
        self.logger.set_prefix(_prefix)

    def _cleanup(self):
        if self.image_file is not None and os.path.exists(self.image_file):
            os.remove(self.image_file)
            self._image_file = None
            self.album_info = {}

    # pylint: disable=too-many-branches
    def tag_file(self, track_info: dict):
        """
        Tag audio files based on directory structure
        :param track_info: dict of track info
        :return:
        """
        artist = track_info.get("artist")
        album = track_info.get("album")

        track_tags = {
            "artist": artist,
            "album": album,
            "album_artist": artist,
            "year": track_info.get('year'),
            "cover": track_info.get('cover'),
            "title": track_info.get('title'),
            "track": (track_info.get('track_num'), track_info.get("track_count")),
            "disk": (1, 1),
        }

        track_file = track_info.get('filename')

        self.logger.success(f"TAGGING: {track_file}")

        audiofile = mutagen.File(track_file)

        if hasattr(audiofile, "tags"):
            del audiofile.tags
        audiofile.add_tags()

        file_type = audiofile.__class__.__name__
        if file_type not in self.field_maps:
            self.logger.error(f"Unsupported file type: {file_type}")
            return False

        field_map = self.field_maps[file_type]
        for field in field_map:
            if field in track_tags:
                _field = field_map[field]
                if field == "cover":
                    if os.path.exists(track_tags[field]):
                        with open(track_tags[field], "rb") as file_handle:
                            if file_type == "MP4":
                                audiofile.tags[_field] = [
                                    MP4Cover(file_handle.read(), imageformat=MP4Cover.FORMAT_JPEG)
                                ]
                            elif file_type == "MP3":
                                audiofile.tags.add(
                                    APIC(
                                        mime='image/jpeg',
                                        type=3,
                                        desc='Cover',
                                        data=file_handle.read()
                                    )
                                )
                            else:
                                self.logger.warning(f"Unsupported file type (cover art): {file_type}")
                    else:
                        self.logger.warning(f"Album art is missing: {track_tags[field]}")
                else:
                    if file_type == "MP3":
                        if field in ["track", "disk"]:
                            track_tags[field] = f"{track_tags[field][0]}/{track_tags[field][1]}"
                        audiofile.tags[_field] = field_map[field](encoding=3, text=track_tags[field])
                    elif file_type == "MP4":
                        audiofile.tags[_field] = [track_tags[field]]
            else:
                self.logger.warning(f"Field not found in data: {field}")

        if not self.dry_run:
            audiofile.save()

        return True

    # pylint: disable=too-many-branches
    def clean_tags(self, _file_path):
        """
        Tag audio files based on directory structure
        :param _file_path:
        :return:
        """

        self.logger.info(f"CLEANING TAGS: {_file_path}")

        audiofile = mutagen.File(_file_path)

        file_type = audiofile.__class__.__name__
        if file_type not in self.field_maps:
            self.logger.error(f"Unsupported file type: {file_type}")
            return False

        field_map = self.field_maps[file_type]
        # pylint: disable=too-many-nested-blocks
        if hasattr(audiofile, "tags"):
            tags = {}
            for field, _field in field_map.items():
                if _field in audiofile.tags:
                    field_data = audiofile.tags[_field]
                    if field == "cover":
                        if file_type == "MP4":
                            audiofile.tags[_field] = [
                                MP4Cover(field_data, imageformat=MP4Cover.FORMAT_JPEG)
                            ]
                        elif file_type == "MP3":
                            tags[_field] = field_data
                            #audiofile.tags.add(
                            #    APIC(mime='image/jpeg', type=3, desc=u'Cover', data=field_data))
                        else:
                            self.logger.warning(f"Unsupported file type (cover art): {file_type}")
                    else:
                        if file_type == "MP3":
                            module = getattr(sys.modules[__name__], field_map[field])
                            if field in ["track", "disk"]:
                                if str(field_data).endswith("/0") or str(field_data).startswith("0/"):
                                    field_data = "1/1"
                            tags[_field] = module(encoding=3, text=str(field_data))
                        elif file_type == "MP4":
                            tags[_field] = [field_data]
                else:
                    self.logger.warning(f"Field not found in data: {field}/{_field}")
                    if field == "disk":
                        self.logger.info(f"Populating field with default value: {field}/{_field} :: 1/1")
                        if file_type == "MP3":
                            module = getattr(sys.modules[__name__], field_map[field])
                            tags[_field] = module(encoding=3, text="1/1")
                        elif file_type == "MP4":
                            tags[_field] = ["1/1"]
            del audiofile.tags
            audiofile.add_tags()
            for tag in tags.values():
                audiofile.tags.add(tag)
            if not self.dry_run:
                audiofile.save()
        return True

    # pylint: disable=too-many-branches,too-many-nested-blocks
    def download_artist_album(self, artist_name, album_name, clean=False):
        search_results = self.yt_music.search(artist_name, filter='albums')
        for item in search_results:
            if item['title'].lower() == album_name.lower():
                _artist_name = item.get('artists')[0]['name']
                thumbnails = item.get("thumbnails")
                album = self.yt_music.get_album(item['browseId'])
                if clean:
                    is_clean = not item['isExplicit']
                    if not is_clean:
                        for other_version in album['other_versions']:
                            is_clean = not other_version['isExplicit']
                            if is_clean:
                                thumbnails = other_version.get("thumbnails")
                                album = self.yt_music.get_album(other_version.get('browseId'))
                                break

                    if is_clean:
                        self.logger.warning("Getting clean version")

                self.dest_dir = f"{_artist_name}/{album.get('title')}"
                self.image_file = thumbnails

                self.logger.info(
                    f'{_artist_name} :: {album.get("title")} ({album.get("year")}) [ {album.get("trackCount")} tracks ]'
                )
                self._set_log_prefix([_artist_name, album.get('title')])
                for index, track in enumerate(album.get("tracks"), 1):
                    track_num = str(index).zfill(2)
                    self.logger.info(
                        f"DOWNLOADING: {track_num} - {track['title']}{' [E]' if track['isExplicit'] else ''}"
                        f" ({track['duration']})"
                    )
                    if not self.dry_run:
                        self.ydl_opts['outtmpl'] = f"{self.dest_dir}/{track_num} - {track.get('title')}.%(ext)s"
                        with YoutubeDL(self.ydl_opts) as ydl:
                            ydl.download([f"https://music.youtube.com/watch?v={track.get('videoId')}"])
                            self.tag_file({
                                "title": track.get('title'),
                                "artist": _artist_name,
                                "album": album.get('title'),
                                "album_artist": _artist_name,
                                "year": album.get('year'),
                                "cover": self.image_file,
                                "track_num": index,
                                "track_count": album.get('trackCount'),
                                "filename": self.current_filename,
                            })
        self._cleanup()
