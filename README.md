+--------------------------------------------------------+
|                     Menu Bar                           |
+--------------------------------------------------------+
|                                                        |
|   Album Art        Song Name                           |
|                    Artist                              |
|                                                        |
|--------------------------------------------------------|
|                                                        |
|               Playlist (QListWidget)                   |
|                                                        |
|                                                        |
|                                                        |
|--------------------------------------------------------|
| <<   ▶   >>     -----------Slider----------- 03:20     |
|                                                        |
| Volume 🔊 --------Slider-------------------            |
+--------------------------------------------------------+

# Refactoring job

PavPlay/
│
├── pavplay/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── controls_bar.py
│   │   └── navigation_bar.py
│   │
│   ├── controllers/
│   │   ├── player_controller.py
│   │   └── playlist_controller.py
│   │
│   ├── widgets/
│   │   └── drop_area.py
│   │
│   ├── models/
│   │   └── media_item.py
│   │
│   └── core/
│       ├── icons.py
│       ├── formats.py
│       └── settings.py
│
├── assets/
├── tests/
├── README.md
├── CONTRIBUTING.md
├── TECH_DEBT.md
└── requirements.txt