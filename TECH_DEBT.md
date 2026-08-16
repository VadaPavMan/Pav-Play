# Technical Debt

This document tracks known technical debt, architectural improvements, cleanup work, and future refactoring tasks in **Pav Play**.

The current priority is to get the application to a stable and functional first release before performing a major refactor.

> **Important:** Do not treat every item in this document as an immediate task.
> During the current development phase, functionality and stability take priority over architectural perfection.

---

# 1. Current Development Philosophy

Pav Play is currently being developed feature-first.

The current priority order is:

1. Build the required functionality.
2. Test the functionality.
3. Fix bugs and stability issues.
4. Reach a stable first release.
5. Perform a dedicated refactoring pass.
6. Improve contributor experience.
7. Continue adding features on top of the cleaner architecture.

During the current pre-release stage, some code duplication, tightly coupled UI logic, temporary implementations, and inconsistent naming are acceptable.

The goal is to avoid premature refactoring while still documenting problems so they are not forgotten.

---

# 2. High-Priority Technical Debt

## 2.1 Refactor `MainUi`

### Current situation

`MainUi` currently handles a large number of responsibilities:

* Main window setup
* Main layout creation
* Navigation bar construction
* Media section construction
* Player page construction
* Placeholder page construction
* Control bar construction
* Button creation
* Slider styling
* Playback-state UI updates
* Position updates
* Duration updates
* Seeking
* File selection handling
* Player page switching

This makes `ui.py` increasingly large and difficult to navigate.

### Planned improvement

Split the UI into smaller components.

Potential structure:

```text
ui/
├── main_window.py
├── navigation_bar.py
├── player_view.py
├── controls_bar.py
└── playlist_panel.py
```

Possible responsibilities:

```text
MainWindow
    └── Coordinates major UI sections

NavigationBar
    └── Open File
    └── Open Folder
    └── Theme
    └── Settings

PlayerView
    └── Placeholder
    └── Video page
    └── Audio page

ControlsBar
    └── Play/Pause
    └── Previous
    └── Next
    └── Seek
    └── Volume
    └── Status

PlaylistPanel
    └── Playlist display
    └── Selection
    └── Queue controls
```

---

# 3. Separate UI Logic From Application Logic

## Current situation

Some application-level behavior is still handled directly inside `MainUi`.

For example:

```python
def onFileSelected(self, filePath):
    page = self.controller.loadMedia(filePath)

    if page == "video":
        self.playerStack.setCurrentWidget(self.videoPage)
    elif page == "audio":
        self.playerStack.setCurrentWidget(self.musicPage)
```

This works, but the main UI is responsible for deciding application behavior.

### Planned improvement

Introduce a higher-level application/controller layer.

Possible future architecture:

```text
UI
 ↓
Application Controller
 ↓
Player Controller
 ↓
QMediaPlayer
```

The UI should primarily:

* display information
* emit user actions
* receive state updates

The application/controller layer should handle:

* media selection
* queue management
* page/state decisions
* playback workflow

---

# 4. Improve `PlayerController`

## Current situation

`PlayerController` already exists, which is good.

It currently provides an important separation between the UI and `QMediaPlayer`.

However, as more functionality is added, it will likely become responsible for:

* Loading media
* Playing
* Pausing
* Seeking
* Volume
* Mute
* Playback state
* Media errors
* Media status
* End-of-media handling
* Playlist navigation
* Repeat
* Shuffle

### Planned improvement

Keep `PlayerController` focused on **media playback**.

Do not allow it to become a giant "everything controller."

Potential future separation:

```text
controllers/
├── player_controller.py
├── playlist_controller.py
└── settings_controller.py
```

---

# 5. Create a Dedicated Playlist Model

## Current situation

The playlist panel exists visually, but playlist functionality is not implemented yet.

The current architecture should not rely on the UI widget itself being the source of truth for playlist data.

### Planned improvement

Create a dedicated playlist/data model.

Possible structure:

```text
playlist/
├── playlist_model.py
└── playlist_item.py
```

The model should manage:

* Media entries
* Current index
* Adding files
* Removing files
* Clearing playlist
* Next item
* Previous item
* Current item
* Queue order
* Shuffle order

The UI should only display the model.

---

# 6. Implement Next / Previous Through Playlist State

## Current situation

The Previous and Next buttons exist visually, but their functionality depends on a proper playlist system.

### Planned improvement

Do not implement Previous/Next by directly manipulating UI elements.

Instead:

```text
Next Button
    ↓
Playlist Controller
    ↓
Next Media Item
    ↓
Player Controller
    ↓
QMediaPlayer
```

The same architecture should be used for Previous.

---

# 7. Implement Automatic Next-Track Playback

## Current situation

When the current media reaches the end, the application does not yet have a complete queue-management workflow.

### Planned improvement

Connect the media player's end-of-media state to playlist management.

Expected flow:

```text
Media Ends
    ↓
Player Controller
    ↓
Playlist Controller
    ↓
Is another item available?
    ↓
Yes
    ↓
Load next item
```

Eventually support:

* Normal playback
* Repeat current
* Repeat playlist
* Stop after current
* Shuffle

---

# 8. Extract Control Bar Into Its Own Widget

## Current situation

The entire control bar is created inside `MainUi.setupControlsBar()`.

It currently contains:

* Progress layout
* Current-time label
* Position slider
* Total-time label
* Transport controls
* Volume controls
* Status label

The current implementation works, but this method will continue growing.

### Planned improvement

Create:

```text
widgets/
└── controls_bar.py
```

Potential class:

```python
class ControlsBar(QFrame):
    ...
```

The widget should expose signals such as:

```text
playRequested
pauseRequested
nextRequested
previousRequested
seekRequested
volumeChanged
muteRequested
```

This would allow the main window to connect the controls without knowing their internal layout.

---

# 9. Extract Navigation Bar

## Current situation

`setupNavigationBar()` creates the navigation UI directly inside `MainUi`.

The current implementation includes:

* Application icon
* Open File
* Open Folder
* Theme toggle
* Settings

The buttons are currently generated through a helper method.

### Planned improvement

Create:

```text
widgets/
└── navigation_bar.py
```

Potential class:

```python
class NavigationBar(QFrame):
    ...
```

Expose signals instead of directly implementing application behavior.

Example:

```text
openFileRequested
openFolderRequested
themeToggleRequested
settingsRequested
```

---

# 10. Remove Unused Imports

The current `ui.py` contains many imports that are not currently required.

Examples include:

```python
random
QTime
QPropertyAnimation
QEasingCurve
Property
QCoreApplication
QMetaObject
QRect
QAction
QFont
QKeyEvent
QDragEnterEvent
QDropEvent
QColor
QPalette
QListWidget
QListWidgetItem
QSplitter
QFileDialog
QStatusBar
QToolBar
QSizePolicy
QMenu
QMenuBar
QToolTip
QSpacerItem
QToolButton
QAudioOutput
```

Some may be required later, but unused imports should eventually be removed.

### Planned improvement

Perform an import cleanup after the first stable version.

Use an import sorter/linter if appropriate.

---

# 11. Remove Temporary `sys.path` Manipulation

## Current situation

`ui.py` currently contains:

```python
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
```

This is currently being used to make project imports work.

### Planned improvement

Convert the project into a proper Python package and use package-relative/importable module structure.

For example:

```text
pavplay/
├── __init__.py
├── main.py
├── ui/
├── controllers/
└── widgets/
```

Then use proper imports rather than modifying `sys.path`.

---

# 12. Standardize Naming Conventions

## Current situation

There are some inconsistent naming patterns.

For example:

```python
Button
```

is used as a local variable even though Python convention generally reserves capitalized names for classes.

### Planned improvement

Use:

```python
button
```

instead of:

```python
Button
```

Likewise, eventually standardize names such as:

```python
heroPixmap
```

or preferably:

```python
hero_pixmap
```

and:

```python
filePath
```

or preferably:

```python
file_path
```

The project should consistently follow PEP 8 naming conventions.

---

# 13. Standardize Method Naming

Current methods include names such as:

```python
SliderStyle()
controlButtons()
navButtons()
```

These should eventually use snake_case:

```python
slider_style()
create_control_button()
create_nav_button()
```

Similarly:

```python
onFileSelected()
updatePlayPauseIcon()
updatePosition()
updateDuration()
seekPosition()
```

should eventually become:

```python
on_file_selected()
update_play_pause_icon()
update_position()
update_duration()
seek_position()
```

This is not urgent because changing names during active development creates unnecessary churn.

---

# 14. Centralize Asset Paths

## Current situation

Asset paths are repeated throughout the UI.

Examples:

```python
"assets\\controls\\play.png"
"assets\\controls\\pause.png"
"assets\\controls\\previous.png"
"assets\\controls\\next.png"
"assets\\controls\\speaker.png"
```

### Planned improvement

Create a centralized asset/path module.

Example:

```text
config/
└── paths.py
```

or:

```text
core/
└── assets.py
```

Then:

```python
PLAY_ICON = ...
PAUSE_ICON = ...
NEXT_ICON = ...
PREVIOUS_ICON = ...
```

Benefits:

* Easier asset management
* Fewer path mistakes
* Easier future packaging
* Easier resource-system migration

---

# 15. Use Cross-Platform Paths

## Current situation

Many paths currently use Windows-style backslashes:

```python
"assets\\controls\\play.png"
```

### Planned improvement

Use `pathlib.Path`.

Example:

```python
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
PLAY_ICON = PROJECT_ROOT / "assets" / "controls" / "play.png"
```

This will make the application easier to run on:

* Windows
* Linux
* macOS

---

# 16. Centralize UI Styling

## Current situation

Stylesheets are currently defined directly inside UI methods.

Examples include:

```python
self.controlsFrame.setStyleSheet(...)
self.playPauseButton.setStyleSheet(...)
self.volumeSlider.setStyleSheet(...)
```

This works during development but will become difficult to maintain as the application grows.

### Planned improvement

Move styles into dedicated QSS files.

Possible structure:

```text
styles/
├── dark.qss
└── light.qss
```

Then load the stylesheet at application startup.

This will also make theme switching much easier.

---

# 17. Create a Theme Manager

## Current situation

A Theme Toggle button exists, but theme functionality is not yet fully implemented.

### Planned improvement

Create a dedicated theme system.

Possible structure:

```text
themes/
├── dark.qss
├── light.qss
└── theme_manager.py
```

Responsibilities:

* Load dark theme
* Load light theme
* Switch theme
* Remember selected theme
* Apply theme globally

---

# 18. Remove `print()` Debugging

## Current situation

`onFileSelected()` currently contains:

```python
print("Selected:", filePath)
```

This is useful while developing.

### Planned improvement

Replace debugging prints with Python's `logging` module.

Potential levels:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

This becomes especially useful when debugging issues reported by contributors.

---

# 19. Add Centralized Logging

Eventually create:

```text
core/
└── logger.py
```

The logger should provide consistent output for:

* Media loading
* Playback errors
* Unsupported formats
* Playlist operations
* File system errors
* Application startup
* Settings changes

---

# 20. Improve Error Handling

## Current situation

Unsupported media formats currently produce a `QMessageBox`.

That is a good starting point.

However, media playback itself can fail for reasons other than file extension.

### Planned improvement

Handle:

* Invalid media
* Missing files
* Permission errors
* Corrupted files
* Unsupported codecs
* Audio output errors
* Video output errors
* Failed media loading
* Network errors if network playback is added later

Use `QMediaPlayer.errorOccurred` and related signals where appropriate.

---

# 21. Validate Files Before Adding Them

Currently file extensions are used to determine whether a file is considered audio or video.

### Planned improvement

Eventually separate:

```text
File extension validation
```

from:

```text
Actual media capability validation
```

A file named:

```text
movie.mp4
```

does not necessarily mean it is a valid playable MP4.

The media backend should ultimately be treated as the source of truth for playback validity.

---

# 22. Centralize Supported Formats

## Current situation

Supported formats are currently displayed inside `DropArea`.

The same format lists will likely eventually be needed by:

* File dialogs
* File validation
* Playlist filtering
* Drag & drop
* Media classification

### Planned improvement

Create a centralized format definition.

Example:

```python
VIDEO_FORMATS = {
    ".mp4",
    ".mkv",
    ".mov",
    ".webm",
    ".avi",
    ".wmv",
}

AUDIO_FORMATS = {
    ".mp3",
    ".m4a",
    ".aac",
    ".wav",
    ".flac",
    ".ogg",
    ".wma",
}
```

Then use the same source everywhere.

This prevents the UI saying one thing while the player accepts something different.

---

# 23. Improve `DropArea`

## Current situation

`DropArea` is already a separate custom widget, which is good.

Future improvements may include:

* Better drag-enter visual feedback
* Drag-leave handling
* Highlighting when a valid file is dragged over it
* Rejecting unsupported files
* Multiple-file drops
* Folder drops
* Better user feedback
* Keyboard accessibility
* Click handling isolated to the intended drop zone

---

# 24. Support Multiple Files in Drag & Drop

The current drag-and-drop implementation primarily deals with selecting media files.

### Planned improvement

Allow:

```text
Drag 1 file
```

and:

```text
Drag 20 files
```

The application should be able to:

1. Inspect all dropped URLs.
2. Filter supported media.
3. Add valid files to the playlist.
4. Ignore or report unsupported files.

---

# 25. Separate Media Classification

## Current situation

`onFileSelected()` currently receives a path and asks the controller to load it.

### Planned improvement

Create a dedicated media classification utility:

```text
MediaFile
    ├── AUDIO
    ├── VIDEO
    └── UNKNOWN
```

This avoids repeating extension checks throughout the application.

---

# 26. Introduce a Media Item Model

Eventually, a playlist item should not just be a raw string path.

Create something conceptually similar to:

```python
MediaItem(
    path=...,
    title=...,
    duration=...,
    media_type=...,
)
```

Potential future metadata:

* File path
* Filename
* Display title
* Duration
* Media type
* Thumbnail
* Artist
* Album
* Track number

---

# 27. Separate Display Name From File Name

A media player should not necessarily display:

```text
C:\Users\Harsh\Downloads\My Song - Final Version.mp3
```

as the playlist item.

Eventually display:

```text
My Song - Final Version
```

while retaining the complete file path internally.

---

# 28. Playlist UI Should Not Own Playlist Data

The future `QListWidget`/playlist UI should be treated as a **view**.

It should display data from the playlist model.

Avoid making the widget itself the application's source of truth.

---

# 29. Add Media Metadata Support

Future versions may extract:

* Song title
* Artist
* Album
* Album artwork
* Duration
* Video resolution
* Video codec
* Audio codec

This should be implemented outside the UI layer.

Potential future module:

```text
media/
└── metadata.py
```

---

# 30. Improve Audio Player Page

## Current situation

The audio page is currently a placeholder:

```text
Audio Player
```

The video player already has a `QVideoWidget`.

### Planned improvement

Create a dedicated audio visualization/player UI.

Potential features:

* Album artwork
* Song title
* Artist
* Album
* Audio visualization
* Playback information
* Background artwork
* Metadata

---

# 31. Improve Video Player Page

Future improvements:

* Video scaling modes
* Fullscreen
* Aspect-ratio control
* Double-click fullscreen
* Video information
* Subtitle support
* Audio track selection
* Playback speed

---

# 32. Keyboard Shortcuts

Eventually add global media shortcuts.

Potential shortcuts:

```text
Space
    Play/Pause

Left Arrow
    Seek backward

Right Arrow
    Seek forward

Up Arrow
    Increase volume

Down Arrow
    Decrease volume

M
    Mute

F
    Fullscreen
```

Keyboard handling should eventually be separated from the main UI class.

---

# 33. Accessibility

Before the first major public release, review:

* Keyboard navigation
* Button tooltips
* Accessible names
* Focus behavior
* Slider accessibility
* Contrast
* Font scaling
* Screen-reader compatibility where possible

---

# 34. Window Resizing Behavior

The UI currently uses layout stretch factors such as:

```python
self.mediaLayout.addWidget(self.playerFrame, 4)
self.mediaLayout.addWidget(self.playlistFrame, 1)
```

This is a good starting point.

However, resizing should eventually be tested at:

* 1280×720
* 1366×768
* 1920×1080
* 2560×1440
* Small laptop displays
* Very wide displays

Make sure:

* Controls do not overlap.
* Playlist remains usable.
* Buttons remain visible.
* Labels do not get clipped.
* Video maintains appropriate proportions.

---

# 35. Fullscreen Mode

Eventually implement:

```text
Normal Window
        ↓
Fullscreen
        ↓
Video-focused UI
```

Potential behavior:

* Hide navigation bar
* Hide playlist
* Expand video
* Keep essential controls visible
* Escape to exit fullscreen

---

# 36. Settings System

The Settings button exists but settings functionality is not implemented yet.

Eventually create:

```text
settings/
├── settings_manager.py
└── settings_dialog.py
```

Potential settings:

* Theme
* Default volume
* Playback behavior
* Repeat mode
* Shuffle
* Remember last media
* Remember window size
* Hardware acceleration if configurable
* Subtitle preferences

---

# 37. Persistent Settings

Use an appropriate persistent settings mechanism, such as Qt's settings system.

Persist things like:

```text
Theme
Window size
Window position
Volume
Mute state
Playback preferences
```

Avoid storing application configuration directly inside UI code.

---

# 38. Configuration Constants

Current values such as:

```python
WIDTH = 1280
HEIGHT = 720
```

are defined directly in `ui.py`.

Eventually move configuration/constants into a dedicated module.

Potential structure:

```text
core/
└── constants.py
```

---

# 39. Add Type Hints

Current code mostly relies on implicit types.

Eventually add type hints to public methods.

Example:

```python
def format_time(milliseconds: int) -> str:
    ...
```

and:

```python
def on_file_selected(file_path: str) -> None:
    ...
```

This will improve:

* IDE support
* Static analysis
* Contributor understanding
* Refactoring safety

---

# 40. Add Docstrings

Public classes and important methods should eventually have concise docstrings.

Example:

```python
class PlayerController:
    """Controls media playback and audio output."""
```

For complex methods, explain:

* What it does
* Parameters
* Return value
* Important side effects

Do not over-document trivial UI construction.

---

# 41. Improve Comments

Current code contains comments such as:

```text
# Media Setup Controller (Default Video Player)
```

Comments are useful, but after refactoring, many comments explaining obvious code should be removed.

Prefer code that explains itself.

Use comments primarily for:

* Why something is done
* Non-obvious Qt behavior
* Workarounds
* Important architectural decisions

---

# 42. Add Automated Formatting/Linting

Eventually configure development tools such as:

```text
Ruff
Black
isort
mypy
```

or another consistent toolchain.

The project should have one agreed-upon formatting style.

Contributors should not have to guess how code should be formatted.

---

# 43. Add Pre-Commit Checks

Before accepting contributions, eventually check:

* Formatting
* Imports
* Linting
* Type checking
* Tests

This prevents unnecessary style-related review comments.

---

# 44. Add Automated Tests

Currently the project is primarily being tested manually.

That is acceptable during early development.

Eventually add tests for:

### Player Controller

* Loading valid media
* Rejecting unsupported formats
* Play
* Pause
* Seek
* Volume

### Playlist

* Add
* Remove
* Clear
* Next
* Previous
* Shuffle

### Utilities

* Time formatting
* File classification
* Path handling

---

# 45. Add Integration Tests

Eventually test complete workflows:

```text
Open File
    ↓
Load Media
    ↓
Switch Player Page
    ↓
Play
    ↓
Seek
    ↓
Pause
```

And:

```text
Drag File
    ↓
DropArea
    ↓
Playlist
    ↓
Player
```

---

# 46. Avoid Testing UI Layout Pixel-by-Pixel

Do not create fragile tests that depend heavily on exact pixel positions.

Prefer testing behavior:

```text
Clicking Play changes player state.
```

rather than:

```text
Play button must be exactly at x=640.
```

---

# 47. Package Resource Handling

Current asset references use relative paths such as:

```python
"assets\\hero\\multimedia.png"
```

This may work during development but can break when packaged.

Eventually establish a proper resource strategy for:

* PyInstaller
* Windows builds
* Linux builds
* Potential future macOS builds

---

# 48. Application Packaging

Eventually test packaged builds rather than only running Python directly.

Potential targets:

```text
Windows
Linux
```

Future possibility:

```text
macOS
```

Packaging should correctly include:

* Icons
* QSS files
* Images
* Fonts
* Other resources

---

# 49. Cross-Platform Testing

Before calling the project stable, test on supported platforms.

At minimum:

```text
Windows
Linux
```

Check:

* File paths
* File dialogs
* Drag & drop
* Audio output
* Video playback
* Icons
* Fonts
* Theme
* Packaging

---

# 50. Dependency Management

Document the required Python/PySide6 version and dependencies.

Eventually add an appropriate dependency file such as:

```text
requirements.txt
```

or a modern Python packaging configuration.

Avoid relying on packages being installed manually without documentation.

---

# 51. Python Version Compatibility

Document the supported Python versions.

For example:

```text
Supported Python:
3.x
```

The exact supported versions should be decided before the first stable release.

---

# 52. PySide6 Version Compatibility

Document the PySide6 version range tested by the project.

Qt Multimedia behavior can vary between Qt/PySide6 versions, so the supported version should eventually be explicit.

---

# 53. Handle Media Backend Differences

Playback behavior can depend on the underlying multimedia backend and operating system.

Do not assume that a format working on one operating system will behave identically everywhere.

Before promising format support, test the format on each supported platform.

---

# 54. Better Status Reporting

The current status label starts with:

```text
Ready
```

Eventually it should communicate useful application state:

```text
Ready
Loading...
Playing
Paused
Stopped
Buffering...
Unsupported format
Playback error
```

Avoid exposing raw technical errors directly to users.

---

# 55. Better Media Error Reporting

Instead of only displaying:

```text
Unsupported media format
```

eventually provide useful messages such as:

```text
Unable to play this file.

The media format may be unsupported or the file may be corrupted.
```

Technical details can go to the log.

---

# 56. Handle Missing/Deleted Playlist Files

If a file in the playlist is deleted or moved externally:

```text
Playlist item
    ↓
File no longer exists
```

The application should detect this and provide appropriate feedback rather than crashing.

---

# 57. Prevent Duplicate Playlist Entries

Decide whether the playlist should allow:

```text
song.mp3
song.mp3
song.mp3
```

multiple times.

If duplicates are not allowed, define a consistent rule based on canonical file paths.

---

# 58. Define Playlist Semantics

Before implementing advanced playlist behavior, document:

* What Next means
* What Previous means
* What happens at the end
* What happens at the beginning
* Shuffle behavior
* Repeat behavior
* Removing current media
* Clearing the playlist while playing

This prevents inconsistent behavior later.

---

# 59. Add Application State Management

As the project grows, several states will interact:

```text
Current media
Current playlist index
Playback state
Volume
Mute state
Position
Duration
Repeat mode
Shuffle mode
Current page
Theme
```

Eventually consider a centralized application/player state model rather than storing state across many UI widgets.

---

# 60. Avoid UI Widgets Becoming the Source of Truth

For example, eventually:

```python
volumeSlider.value()
```

should not necessarily be treated as the application's actual volume state.

The player/controller should own the state.

The slider should reflect it.

Desired relationship:

```text
Controller State
      ↓
      UI

User Action
      ↓
      Controller
      ↓
Updated State
      ↓
      UI
```

---

# 61. Improve Signal Naming

As custom signals are added, use descriptive names.

Examples:

```text
fileSelected
mediaLoaded
playRequested
pauseRequested
seekRequested
volumeChanged
playlistChanged
currentMediaChanged
```

Signals should describe **what happened**, rather than how the UI should implement it.

---

# 62. Avoid Excessive Coupling Between Widgets

A widget should not directly manipulate unrelated widgets.

Avoid patterns such as:

```python
dropArea.playButton.setIcon(...)
```

Prefer:

```text
DropArea
    ↓ signal
Main/Application Controller
    ↓
Player
    ↓ signal
ControlsBar
```

---

# 63. Extract Reusable UI Helpers

Current helper methods:

```python
controlButtons()
navButtons()
SliderStyle()
```

are useful.

Eventually move reusable helpers into a dedicated module if multiple widgets require them.

---

# 64. Avoid Over-Abstraction

Do not create a class/module simply because it is possible.

Refactoring should be driven by:

* Repetition
* Complexity
* Coupling
* Maintainability
* Reuse

Avoid turning every five lines of UI code into a separate class.

---

# 65. Document Architecture

Once the refactor is complete, create:

```text
ARCHITECTURE.md
```

It should explain:

* Application structure
* UI layer
* Controller layer
* Models
* Widgets
* Signals
* Media flow
* Playlist flow
* Settings flow

This will be particularly useful for contributors.

---

# 66. Add Contribution Documentation

Before inviting contributors, create:

```text
CONTRIBUTING.md
```

Document:

* How to clone the project
* How to install dependencies
* How to run it
* Code style
* Branch naming
* Commit conventions
* Pull request process
* Testing requirements
* Bug reporting

---

# 67. Add Development Setup Documentation

The README should eventually contain a simple setup flow:

```text
Clone repository
    ↓
Create virtual environment
    ↓
Install dependencies
    ↓
Run application
```

A contributor should be able to get the application running without asking the maintainer for help.

---

# 68. Improve Git Hygiene

Before the public release, verify:

```text
.gitignore
```

contains:

* Virtual environments
* Python cache
* IDE files
* Build artifacts
* Distribution files
* Logs
* Temporary files
* Local settings

Never commit user-specific paths or generated artifacts.

---

# 69. Add Versioning

Define a project version.

Example:

```text
0.1.0
```

for the first development release.

Then follow a consistent versioning strategy.

---

# 70. Create Release Checklist

Before the first stable release:

* [ ] Application starts cleanly
* [ ] No unexpected console errors
* [ ] Open File works
* [ ] Open Folder works
* [ ] Drag & Drop works
* [ ] Audio playback works
* [ ] Video playback works
* [ ] Play/Pause works
* [ ] Seeking works
* [ ] Volume works
* [ ] Mute works
* [ ] Playlist works
* [ ] Next/Previous work
* [ ] End-of-media behavior works
* [ ] Theme switching works
* [ ] Settings work
* [ ] Invalid files are handled
* [ ] Missing files are handled
* [ ] Application can be packaged
* [ ] Packaged application tested
* [ ] README updated
* [ ] CONTRIBUTING.md added
* [ ] ARCHITECTURE.md added
* [ ] License added
* [ ] Version tagged

---

# 71. Suggested Refactoring Order

When the first stable version is complete, do **not** attempt to fix everything randomly.

Use this order.

## Phase 1 — Cleanup

* [ ] Remove unused imports
* [ ] Rename inconsistent variables
* [ ] Rename methods to consistent conventions
* [ ] Remove debug prints
* [ ] Format code
* [ ] Add type hints where useful

## Phase 2 — Resources

* [ ] Centralize asset paths
* [ ] Use `pathlib`
* [ ] Centralize supported formats
* [ ] Move stylesheets to QSS

## Phase 3 — UI Components

* [ ] Extract NavigationBar
* [ ] Extract ControlsBar
* [ ] Extract PlayerView
* [ ] Extract PlaylistPanel

## Phase 4 — Application Logic

* [ ] Improve PlayerController
* [ ] Create PlaylistController
* [ ] Create MediaFile/MediaItem model
* [ ] Separate application state

## Phase 5 — Infrastructure

* [ ] Logging
* [ ] Settings manager
* [ ] Resource management
* [ ] Packaging
* [ ] Error handling

## Phase 6 — Developer Experience

* [ ] Tests
* [ ] Linting
* [ ] Formatting
* [ ] Type checking
* [ ] CONTRIBUTING.md
* [ ] ARCHITECTURE.md

---

# 72. Definition of "Refactored"

The refactoring phase should be considered successful when:

* `MainUi` is no longer responsible for the entire application.
* UI components have clear responsibilities.
* Controllers contain application behavior.
* Models contain application data.
* Widgets communicate primarily through signals.
* Styles are centralized.
* Assets are centralized.
* Paths are cross-platform.
* Supported formats have one source of truth.
* Debug prints have been replaced with logging.
* Tests cover important application logic.
* A new contributor can understand the project structure without reading every file.

---

# 73. Current Priority

At the current development stage:

> **DO NOT stop feature development just to eliminate the technical debt listed above.**

Continue building the first working version.

Recommended immediate priorities:

1. Playlist system
2. Next / Previous
3. Open Folder
4. Automatic next-media playback
5. Volume control
6. Mute
7. Repeat / Shuffle
8. Audio player UI
9. Settings
10. Theme switching
11. Error handling
12. Stability testing

After the feature set is sufficiently complete:

> **Freeze major feature development and perform a dedicated refactoring sprint.**

---

# 74. Refactoring Sprint

When the first stable version is reached, dedicate a focused period exclusively to technical debt.

Recommended approach:

### Day 1 — Codebase Audit

* [ ] Identify duplicated code
* [ ] Identify oversized classes
* [ ] Identify tightly coupled components
* [ ] Identify unused code
* [ ] Identify inconsistent naming
* [ ] Identify hardcoded paths
* [ ] Identify hardcoded styles
* [ ] Identify missing error handling

### Day 2 — Architecture

* [ ] Extract UI components
* [ ] Improve controller boundaries
* [ ] Introduce models
* [ ] Establish clear dependencies

### Day 3 — Code Quality

* [ ] Naming
* [ ] Formatting
* [ ] Type hints
* [ ] Docstrings
* [ ] Logging
* [ ] Imports

### Day 4 — Resources and Configuration

* [ ] Asset management
* [ ] QSS
* [ ] Settings
* [ ] Constants
* [ ] Cross-platform paths

### Day 5 — Testing

* [ ] Unit tests
* [ ] Integration tests
* [ ] Manual regression testing
* [ ] Packaging tests

The exact schedule can change depending on project size.

---

# 75. Important Refactoring Rule

**Do not change behavior while refactoring unless necessary.**

During the refactoring sprint:

```text
Before:

Feature works
Code is messy

After:

Feature works
Code is cleaner
```

Avoid:

```text
Before:

Feature works
Code is messy

After:

Code is cleaner
Feature behaves differently
```

Refactoring should preserve existing behavior wherever possible.

---

# 76. Technical Debt Status

| Area                             | Status      | Priority |
| -------------------------------- | ----------- | -------- |
| MainUi size                      | Open        | High     |
| NavigationBar extraction         | Open        | Medium   |
| ControlsBar extraction           | Open        | High     |
| PlayerView extraction            | Open        | Medium   |
| Playlist architecture            | Open        | High     |
| PlayerController separation      | In progress | High     |
| Supported formats centralization | Open        | Medium   |
| Asset paths                      | Open        | Medium   |
| QSS extraction                   | Open        | Medium   |
| Naming consistency               | Open        | Medium   |
| Type hints                       | Open        | Low      |
| Logging                          | Open        | Medium   |
| Error handling                   | Open        | High     |
| Settings architecture            | Open        | Medium   |
| Testing                          | Open        | High     |
| Packaging                        | Open        | High     |
| Documentation                    | Open        | High     |
| Contributor setup                | Open        | High     |

---

# 77. Guiding Principle

Pav Play is currently being built by prioritizing **working software first**.

Technical debt is being tracked intentionally rather than ignored.

The objective is not to produce perfectly structured code before the application exists.

The objective is:

```text
Build
    ↓
Test
    ↓
Stabilize
    ↓
Refactor
    ↓
Document
    ↓
Open Source
```

The first version does not need to be perfect.

It needs to be **functional, stable, understandable, and worth improving**.

---

*Last updated: August 2026*
