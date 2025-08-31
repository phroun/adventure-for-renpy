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

### 0.1.0
- Initial release
- Supports multiple labeled Polygons per Room
