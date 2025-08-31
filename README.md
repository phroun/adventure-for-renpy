# @phroun/adventure-for-renpy

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A module to add point-and-click adventure game support to RenPy.

## Requirements

- **RenPy 8.4.1 or newer**: A python-infused framework for Visual Novels.

## Features

- **Clickable Zones**: Define multiple clickable zones per room.

## Quick Start

```rpy
label lounge:
    scene bg lounge

    $ adventure.roomName = "lounge"
    call adventure_input

    "You got [adventure.result]"

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

### 0.1.1
- Added To-Do List to README.md

### 0.1.0
- Initial release
- Supports multiple labeled Polygons per Room

## To-Do

### Requirements to achieve 1.0:

- Move editing mode features into a separate .rpy file (to exclude from game distributions)
- Add Verb Options for Polygons
  - Movement Mode Verbs: Go [-/Through/In/Out/Across/Under]
  - Examine Mode Verbs: Look/Read/Taste
  - Operate Mode Verbs: Use/Open/Close/Touch
  - Speak Mode Verbs: Talk To/Speak/Ask
  - Auto-Operate Mode Verbs: Move Mode + Operate Mode + Examine Mode
- Allow placement of Verb Overlay Icons in addition to Polygons
  - Operate Mode Verbs: Move/Speak/Talk/Hit/Wait/Eat/Taste/Hit/Take
  - Examine Mode Verbs: Taste/Look/Look(Hint)/Read(Hint)
  - Allow Active Scenes to Overload a Room+Verb+Label with a Scene Trigger
    - Generate an Error in Advance if Specified Room+Verb+Label is Undefined
- Allow Game Designer to Specify Global or Per-Scene Screens to "Use"
  - And to Specify to Load either Before or After the Adventure UI
- Add support for a Game Toolbar for Mode Selection
  - Toolbar Radio Buttons
  - Toolbar Checkboxes
  - Toolbar Action Buttons
- Allow Saving and Loading Room Data to/from .json or .rpy file
- Add Cascading Flags System (Persistent, Scenes & Rooms)
- Add Flag Conditionals for Polygons & Overlay Icons

### Feature Requests:

- Hide Polygons & Editor UI when not in Editor Mode
- Fading Overlay Icons
- Room List
- Label List
- Draw/Play Icon
- Click Existing Polygon to Switch Polygons
- New Icon to Add New Polygon
- Points Icon to Edit Existing Points
- Checkmark Button to Finish Editing Points
- Visible Polygon Labels
