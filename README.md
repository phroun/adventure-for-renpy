# @phroun/adventure-for-renpy

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/F2F61JR2B4)

A module to add point-and-click adventure game support to RenPy.
If you use this, please support me on ko-fi:  https://ko-fi.com/jeffday

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
init python:
    adventure_declare_flags([
      ("Day", "Present when it is daytime"),
      ("Night", "Present when it is nighttime"),
    ])

label lounge:
    scene bg lounge
    
    # the following will only persist until the next set_scene
    adventure_set_scene("int, day")

    call adventure_input("lounge")
    if player_chooses_to("examine desk"):
        if adventure_check_condition("night"):
           "A card next to a bell says, \"ring for service\""
        else:
           "The hotel clerk stands behind the desk."
    if player_chooses_to("use bell"):
       "You ring the bell and wait a moment.  No one arrives."
    
    if player_chooses_to("enter the lift"):
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

### 0.2.1
- Added tooltip hint for actions (configurable via adventure.action_tip) 
- Began improving choice/menu layout.

### 0.2.0
- Added Cascading Flags System (Persistent & Scene-Based)
- Implemented Flag Conditionals for Polygons & Overlay Icons
  - Supports & AND, | OR, ! NOT, and () parenthesis in evaluation

### 0.1.11
- Added basic Toolbar Support for Mode Selection

### 0.1.10
- Improved handling of icon verbs
  - We now store the icon name instead of hard-coding the verbs
- Source code cleanup (named constants instead of magic numbers)
- Changed layer tool-icons to a more investigative order (examine, speak, operate, go)

### 0.1.9
- Allow selecting icons or polygons with the arrow tool
- Added verb icon palette
- Clicking an icon now generates a command for the parser

### 0.1.8
- History log now records actions with either first or third person

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

- Enhance Toolbar Display
- Room-Persistent Flags (Useful for Inventory-Related Tasks)
- Debug Mode to Force-Override Flag Values
- Allow Active Scenes to Overload a Room+Verb+Label with a Scene Trigger
  - Generate an Error in Advance if Specified Room+Verb+Label is Undefined

### Upcoming Planned Features:

- Dialogue and Choices Style
- Task & Notes Journal

### Feature Requests:

- Fading Overlay Icons
- Visible Polygon Labels
- Add support for custom toolbar element:
  - Toolbar Radio Buttons
  - Toolbar Checkboxes
  - Toolbar Action Buttons
