"""Default values for Pav Play settings.

The first stable build only establishes the settings framework.  These values
are kept here so actual setting controls can be added without scattering
hard-coded defaults throughout the UI.
"""

DEFAULT_SETTINGS = {
    "audio/auto_play": True,
    "audio/resume_playback": False,
    "audio/remember_position": False,
    "audio/default_volume": 100,
    "audio/remember_volume": False,
    "audio/default_loop_mode": 0,
    "audio/default_shuffle": False,
    "video/auto_play": True,
    "video/resume_playback": False,
    "core/remember_last_media": False,
    "core/remember_last_playlist": False,
    "core/confirm_before_exit": False,
    "core/add_opened_files_to_playlist": True,
}
