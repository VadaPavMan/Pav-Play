# Technical Debt

This document tracks **post-v1 technical debt** and architectural work for Pav Play.

The v1 feature set is considered stabilized. Technical debt listed here is intentionally separated from normal feature development so that working behavior is not unnecessarily disturbed.

> **Rule:** Do not change existing behavior during refactoring unless the change is intentional, documented, and tested.

---

## 1. Current State

Pav Play has completed the following development phases:

```text
Phase 1  → Playlist behavior
Phase 2  → Media opening / folders / drag & drop / core integration
Phase 3  → Audio / video polish / media switching
Phase 4  → Error handling / keyboard shortcuts / edge-case testing
Phase 5  → v1 stabilization
```

The next major phase is:

```text
Phase 6 → Architecture refactor
```

The purpose of Phase 6 is to improve maintainability without turning the v1 stabilization work into an uncontrolled rewrite.

---

## 2. Architecture Debt

### 2.1 `MainUi` is too large

`src/ui.py` currently owns many responsibilities, including:

- Main window construction
- Navigation
- Player pages
- Controls
- Playlist UI
- Theme application
- File selection
- Media classification
- Playback workflow
- Settings integration
- Persistence
- Keyboard shortcuts

### Planned direction

Split the UI into focused components.

Possible structure:

```text
src/
├── ui/
│   ├── main_window.py
│   ├── navigation_bar.py
│   ├── player_view.py
│   ├── controls_bar.py
│   └── playlist_panel.py
```

The refactor should be incremental. Each extraction should preserve existing behavior before moving to the next component.

---

### 2.2 Separate application logic from UI logic

Some application workflow still lives directly inside `MainUi`.

Future architecture:

```text
UI
 ↓
Application / Playback Workflow
 ↓
Controllers
 ↓
Qt Multimedia
```

The UI should primarily display state and emit user actions.

---

### 2.3 Keep `PlayerController` focused

`PlayerController` should remain responsible for media playback rather than gradually becoming responsible for playlists, application state, settings, and every UI decision.

Potential future controller split:

```text
controllers/
├── player_controller.py
├── playlist_controller.py
└── settings_controller.py
```

---

## 3. Playlist / Data Architecture

The playlist currently relies heavily on the UI widget.

Future architecture should introduce a dedicated model containing:

- Media entries
- Current item
- Current index
- Add / remove / clear operations
- Next / previous semantics
- Shuffle order
- Playlist persistence data

Desired relationship:

```text
Playlist Model
      ↓
Playlist UI
```

rather than:

```text
QListWidget
      ↓
Application state
```

---

## 4. Media Model

Playlist entries are currently based largely on file paths.

A future `MediaItem` model could contain:

```text
path
title
display_name
duration
media_type
artist
album
thumbnail
```

Media metadata extraction should remain outside the UI layer.

---

## 5. Resource and Path Management

The project currently uses centralized icon constants, which is useful, but many resource references still use Windows-style relative paths.

Future work:

- Use `pathlib`
- Centralize project/resource paths
- Make resource handling explicit
- Prepare resources for packaged builds
- Avoid depending on the current working directory

Potential future module:

```text
core/
└── paths.py
```

---

## 6. Styling / Theme Architecture

Theme switching currently works in the v1 implementation.

Future cleanup can:

- Move large QSS blocks out of Python
- Separate theme definitions from widget logic
- Introduce a dedicated theme manager only if the resulting architecture is simpler
- Preserve the current theme appearance and transition behavior

Possible future structure:

```text
styles/
├── dark.qss
└── light.qss
```

Do not refactor the working theme transition merely for cosmetic reasons.

---

## 7. Naming and Code Quality

The codebase still contains mixed naming conventions.

Examples that can be standardized during Phase 6:

```text
filePath       → file_path
heroPixmap     → hero_pixmap
updatePosition → update_position
seekPosition   → seek_position
```

Helper names such as `SliderStyle()`, `controlButtons()`, and `navButtons()` can also be converted to consistent snake_case naming.

Do this only during the dedicated refactor to avoid breaking active v1 work.

---

## 8. Imports and Debug Output

Future cleanup should:

- Remove unused imports
- Replace remaining development `print()` calls with logging where appropriate
- Keep comments focused on non-obvious behavior and Qt-specific workarounds

A small centralized logging facility may be introduced when the application has enough diagnostic output to justify it.

---

## 9. Type Hints and Documentation

Future quality improvements:

- Add type hints to public methods
- Add concise docstrings to important classes and methods
- Document non-obvious playback/resume behavior
- Keep comments focused on **why**, not simply **what**

Avoid over-documenting trivial widget construction.

---

## 10. Testing

The project now has targeted stabilization tests, but broader automated coverage is still a future task.

Important future test areas:

### Utilities

- Time formatting
- Format classification
- Path handling
- Metadata extraction

### Playlist

- Add
- Remove
- Clear
- Current item
- Next / previous
- Shuffle
- Loop behavior
- Missing files
- Duplicate entries

### Player

- Media loading
- Invalid media
- Play / pause
- Seek
- End-of-media behavior
- Volume
- Mute

### Integration

```text
Open File
   ↓
Load Media
   ↓
Select Player Page
   ↓
Play
   ↓
Seek
   ↓
Pause
```

and:

```text
Drag / Drop
   ↓
DropArea
   ↓
Playlist
   ↓
Player
```

Prefer behavior-based tests over pixel-perfect UI tests.

---

## 11. Cross-Platform and Packaging

Before treating Pav Play as a broadly distributed desktop application, validate:

- Windows
- Linux
- macOS where supported

Test:

- File paths
- File dialogs
- Drag & drop
- Audio output
- Video playback
- Icons
- Fonts
- Themes
- Qt Multimedia behavior
- Packaged resources

Packaging should eventually be tested with the real resource tree rather than only `python src/main.py`.

---

## 12. Dependency Management

The runtime dependency list currently contains only the libraries used by the application:

```text
PySide6
mutagen==1.48.1
```

`PyQt6` is intentionally not included because Pav Play uses PySide6.

Future release work should document:

- Supported Python versions
- Tested PySide6 versions
- Platform/version combinations tested
- Packaging requirements

PySide6 should be pinned once a release-tested compatibility matrix exists rather than guessing a version now.

---

## 13. Accessibility and UX

Before a broader public release, review:

- Keyboard navigation
- Focus behavior
- Accessible names
- Slider accessibility
- Contrast
- Text scaling
- Error-message clarity

The existing v1 controls and shortcuts should remain functional while this work is introduced.

---

## 14. Completed During v1 Stabilization

The following areas were addressed during Phase 5 and should not be treated as open v1 blockers:

- Media/path validation
- Invalid-media handling
- Resume-state safeguards
- Application shutdown persistence
- Settings loading safeguards
- Settings value validation
- Format consistency
- Metadata failure safety
- Drag/drop validation
- Duplicate dropped-file filtering
- Keyboard shortcut integration
- Project dependency cleanup
- Project documentation alignment

---

## 15. Refactoring Order

When Phase 6 begins, use this order:

### Step 1 — Audit

- Identify coupling
- Identify duplicated logic
- Identify oversized methods/classes
- Identify remaining dead code

### Step 2 — Extract UI Components

- Navigation bar
- Controls bar
- Player view
- Playlist panel

### Step 3 — Separate Application Logic

- Playback workflow
- Playlist controller
- Application state

### Step 4 — Introduce Models

- `MediaItem`
- Playlist model/state

### Step 5 — Resources

- `pathlib`
- Resource paths
- QSS

### Step 6 — Quality

- Naming
- Imports
- Type hints
- Docstrings
- Logging

### Step 7 — Testing

- Unit tests
- Integration tests
- Regression testing
- Packaging tests

---

## 16. Refactoring Rule

The main refactoring invariant is:

```text
Before refactor:
Feature works
Code is difficult to maintain

After refactor:
Feature still works
Code is easier to maintain
```

A cleaner architecture is not considered successful if it silently changes existing v1 behavior.

---

## 17. Current Priority

```text
Phase 5: v1 stabilization        ✅ Complete

Phase 6:
    Architecture refactor        → Next
    Resource/path cleanup
    UI component extraction
    Controller boundaries
    Playlist model
    Testing expansion
    Packaging preparation
```

New product features should be added carefully during the refactor. Major architectural changes should remain isolated from unrelated feature work.

---

*Last updated: September 2026*
