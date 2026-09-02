from mutagen import File


def get_artist(file_path):
    try:
        audio = File(file_path)

        if audio is None:
            return "Unknown"

        # Common artist/author metadata keys
        artist_keys = [
            "artist",
            "TPE1",  # MP3 - Lead performer
            "\xa9ART",  # M4A/MP4 - Artist
            "Author",  # Some formats
            "WM/AlbumArtist",
        ]

        for key in artist_keys:

            if key not in audio:
                continue

            value = audio[key]

            if isinstance(value, list):

                if len(value) > 0:
                    artist = str(value[0]).strip()

                    if artist:
                        return artist

            else:
                artist = str(value).strip()

                if artist:
                    return artist

        return "Unknown"

    except Exception as e:
        print(f"Error reading artist metadata: {e}")
        return "Unknown"
