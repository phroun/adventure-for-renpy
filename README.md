# @phroun/adventure-for-renpy

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A module to add point-and-click adventure game support to RenPy.

## Requirements

- **RenPy 7.5 or newer (8.4.1 recommended)**: A python-infused framework for Visual Novels.

## Features

- **Clickable Zones**: Define multiple clickable zones per room.
- **Editor UI**: Presence of adventure-editor.rpy (not shipped in build) enables editor UI.
- **Tool Groups for Verbs**:
  - Movement Mode Verbs: Go [-/Through/In/Out/Across]
  - Examine Mode Verbs: Look/Read/Taste/Listen/Smell
  - Operate Mode Verbs: Use/Open/Close/Touch
  - Speak Mode Verbs: Talk To/Speak/Ask
  - Auto-Operate Mode Verbs: Move Mode Verbs + Operate Mode Verbs + (Non-Icon) Examine Mode Verbs

## Quick Start

```rpy
label lounge:
    scene bg lounge
    call adventure_input("lounge")
    if player_chooses_to("enter the elevator"):
        "The elevator door is jammed."
    jump lounge
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes
4. Test changes
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Changelog

### 0.1.7
- Added basic parser function:  player_chooses_to()
- Ability to edit Condition on any Interactable

### 0.1.6
- Added Create New Polygon
- Added Create New Icon
- Added Delete option in Point Editor
- Added Verb Editor for Polygons
  - (Prefix with * to invoke an entire verb group)

### 0.1.5
- Added adventure_overlay and adventure_underlay screens
  - (to be redefined by game authors who need advanced customization)
  
### 0.1.4
- Added "Play" Icon to Hide Editor Polygons
- Added Point Editor Mode to Edit Existing Points
- Added Tool UI Icon to Add a New Polygon

### 0.1.3
- Allow room parameter to be passed directly to adventure_input() call

### 0.1.2
- Moved editing mode features into a separate .rpy file (to exclude from game distributions)
- Allow Saving and Loading Room Data to/from .rpy file

### 0.1.1
- Added To-Do List to README.md

### 0.1.0
- Initial release
- Supports multiple tagged Polygons per Room

## To-Do

### Requirements to achieve 1.0:

- Allow placement of Verb Overlay Icons in addition to Polygons
  - Operate Mode Verbs: Move/Speak/Talk/Hit/Wait/Eat/Taste/Take
  - Examine Mode Verbs: Taste/Look/Look(Hint)/Read(Hint)
  - Allow Active Scenes to Overload a Room+Verb+Label with a Scene Trigger
    - Generate an Error in Advance if Specified Room+Verb+Label is Undefined
- Add support for a Game Toolbar for Mode Selection
  - Toolbar Radio Buttons
  - Toolbar Checkboxes
  - Toolbar Action Buttons
- Add Cascading Flags System (Persistent, Scenes & Rooms)
- Add Flag Conditionals for Polygons & Overlay Icons
  - Into Editor
  - Into Click Processing
- Debug Mode to Force-Override Flag Values

### Feature Requests:

- Fading Overlay Icons
- Visible Polygon Labels
