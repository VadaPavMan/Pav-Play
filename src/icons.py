from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def _asset(*parts):
    return str(ASSETS_DIR.joinpath(*parts))


class Icons:

    # Nav Bar Icons
    APPICON = _asset("nav", "appicon.png")
    FILES = _asset("nav", "files.png")
    FOLDER = _asset("nav", "folder.png")
    SETTINGS = _asset("nav", "settings.png")
    THEME = _asset("nav", "theme.png")
    BACK = _asset("nav", "back.png")

    # Credits
    EUCALYP = _asset("credits", "eucalyp.jpg")
    MITIABULAITI = _asset("credits", "mitiabulaiti.png")
    MUHAMMADALI = _asset("credits", "muhammad-ali.jpg")
    STORYSET = _asset("credits", "storyset.png")
    XNIMRODX = _asset("credits", "xnimrodx.jpg")
    VADAPAVMAN = _asset("credits", "vadapavman.png")
    GITHUB = _asset("credits", "github.png")
    EMAIL = _asset("credits", "email.png")

    # Hero
    MULTIMEDIA = _asset("hero", "multimedia.png")
    MUSICHERO = _asset("hero", "musicHero.png")
    MUSICHERO_G = _asset("hero", "musicHeroG.png")

    # Controls Icons
    PLAY = _asset("controls", "play.png")
    PAUSE = _asset("controls", "pause.png")
    PREVIOUS = _asset("controls", "previous.png")
    NEXT = _asset("controls", "next.png")
    SPEAKER = _asset("controls", "speaker.png")
    MUTE = _asset("controls", "mute.png")
    SHUFFLE = _asset("controls", "shuffle.png")
    LOOP = _asset("controls", "loop.png")
    LOOP_ONE = _asset("controls", "loop_one.png")
    LOOP_OFF = _asset("controls", "loop_off.png")

    # Playlist Icons
    MUSIC = _asset("playlist", "music.png")
    VIDEO = _asset("playlist", "video.png")
