from mutagen import File

UNKNOWN_ARTIST = "Unknown"


def get_artist(file_path):
    if not isinstance(file_path, str) or not file_path:
        return UNKNOWN_ARTIST

    try:
        audio = File(file_path)

        if audio is None:
            return UNKNOWN_ARTIST

        # Common artist/author metadata keys used by supported containers.
        artist_keys = (
            "artist",
            "TPE1",  # MP3 - Lead performer
            "\xa9ART",  # M4A/MP4 - Artist
            "Author",  # Some formats
            "WM/AlbumArtist",
        )

        for key in artist_keys:
            if key not in audio:
                continue

            value = audio[key]

            if isinstance(value, (list, tuple)):
                values = value
            else:
                values = (value,)

            for candidate in values:
                artist = str(candidate).strip()
                if artist:
                    return artist

        return UNKNOWN_ARTIST

    except Exception:
        return UNKNOWN_ARTIST
