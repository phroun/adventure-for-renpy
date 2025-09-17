init python:
     """
**************************************************************************
**
**   adventure.rpy - Adventure Module (for Ren'Py)
**
**   Version 0.2 revision 12
**
**************************************************************************
This module is released under the MIT License:
==========================================================================

Copyright 2025 Jeffrey R. Day

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the “Software”),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

**************************************************************************
"""

define ADVENTURE_VERSION_MAJOR = 0
define ADVENTURE_VERSION_MINOR = 2
define ADVENTURE_VERSION_REVISION = 12

define ADVENTURE_UNSET = "unset"

# <init>
init -10 python:

    import time
    import math
    import pygame
    import renpy.display.render as render
    from renpy.display.core import Displayable
    import math
    import re

    # <class>
    class AdventureStore(object):
        # <def>
        def __init__(self):
            self.initialized = False
        # </def>
    # </class>

    ADVENTURE_LOG = Character(">>>", who_color="#999999", what_color="#999999")
    adventure = AdventureStore()

    # Automatic conversion and installation of App/.exe and Window icon will only
    # function when both adventure-editor.rpy and and adventure-utils.rpy are present.

    adventure.generate_icons = True
    adventure.game_icon = "adventure/images/editor-icons/about.png"

    # The following settings can also be overriden in your script's init
    # python section:

    #### DO NOT MODIFY THIS FILE ####

    adventure.guiscale = 2  # For the Editor GUI
    
    #### DO NOT MODIFY THIS FILE ####

    adventure.do_logging = True
    adventure.first_person = False  # False = You, True = I, None = Disabled
    adventure.narratorName = ""

    #### DO NOT MODIFY THIS FILE ####

    adventure.tooltip_xpos = 0.5
    adventure.tooltip_ypos = 20
    adventure.tooltip_size = 18
    adventure.tooltip_bg_opacity = 0.5
    adventure.action_tip = True

    #### DO NOT MODIFY THIS FILE ####

    adventure.images_base = "images"
    adventure.iconset = "free-icons"
    adventure.iconzoom = 0.1
    adventure.icon_padding = 5
    adventure.icon_grace_radius = 60

    #### DO NOT MODIFY THIS FILE ####

    adventure.toolbar_position = "bottom"
    adventure.toolbar_icons_base = "images"
    adventure.toolbar_iconset = "free-icons"
    adventure.toolbar_iconzoom = 0.1
    adventure.toolbar_anchor = 0.5
    adventure.toolbar_margin_edge = 40
    adventure.toolbar_margin_start = 20
    adventure.toolbar_margin_end = 20
    adventure.toolbar_bg_opacity = 0.5
    adventure.toolbar_icons = ["auto", "ex", "inventory"]
    adventure.toolbar_menu = "touch_only"
    adventure.toolbar_inventory_expand = True # one button per item? False = bag icon
    
    #### DO NOT MODIFY THIS FILE ####

    adventure.choice_position = "right"
    adventure.choice_frame = "adventure/images/choice-frame.png"
    adventure.choice_frame_hover = "adventure/images/choice-frame-hover.png"
    adventure.choice_frame_selected = None
    adventure.choice_textcolor = "#000000"
    adventure.choice_textcolor_hover = "#ffff00"
    adventure.choice_textcolor_selected = "#003333"
    
    #### DO NOT MODIFY THIS FILE ####
    
    adventure.confirm_frame = "adventure/images/confirm-frame.png"
    
    #### DO NOT MODIFY THIS FILE ####

    adventure.slice_metrics = {
       "adventure/images/choice-frame.png": {
           "left": 400, "top": 36, "right": 36, "bottom": 36,
           "source_render_width": 640,
       },
       "adventure/images/choice-frame-hover.png": {
           "left": 400, "top": 36, "right": 36, "bottom": 36,
           "source_render_width": 640,
       },
       "adventure/images/confirm-frame.png": {
           "left": 212, "top": 212, "right": 212, "bottom": 212,
           "source_render_width": 189,
           "render_before": "adventure/images/confirm-frame-shadow.png",
           # "render_before_zoom": 1.0,
       },
       "button": {
           "source": "adventure/images/confirm-frame.png",
           "left": 212, "top": 212, "right": 212, "bottom": 212,
           "source_render_width": 189,
           "render_before": "adventure/images/confirm-frame-shadow.png",
           # "render_before_zoom": 1.0,
       },
       "button-hover": {
           "source": "adventure/images/confirm-frame.png",
           "left": 212, "top": 212, "right": 212, "bottom": 212,
           "source_render_width": 189,
           "render_before": "adventure/images/confirm-frame-shadow.png",
           # "render_before_zoom": 1.0,
       },
       "button-selected": {
           "source": "adventure/images/confirm-frame.png",
           "left": 212, "top": 212, "right": 212, "bottom": 212,
           "source_render_width": 189,
           "render_before": "adventure/images/confirm-frame-shadow.png",
           # "render_before_zoom": 1.0,
       },
       "adventure/images/confirm-frame-shadow.png": {
           "left": 212, "top": 212, "right": 212, "bottom": 212,
           "extend-left": 159, "extend-top": 146, "extend-right": 259, "extend-bottom": 272,
           "x-offset": 0, "y-offset": 0,
           "source_render_width": 189,
           # "zoom": 0.31
       },
    }

    #### DO NOT MODIFY THIS FILE ####

    adventure.toolbar_hints = {

        # These are the tooltips for the toolbar icons:

        "go": "Go (Walk, Travel, Turn)",
        "ex": "Examine (Look, Listen, etc.)",
        "op": "Use",
        "say": "Talk",
        "auto": "Action",
    }

    #### DO NOT MODIFY THIS FILE ####

    adventure.tool_icons = {

        # These are the image filename associated with each verb mode tool:

        "go": "mode-go.png",
        "ex": "mode-examine.png",
        "op": "mode-operate.png",
        "say": "mode-talk.png",
        "auto": "mode-auto.png",
    }

    #### DO NOT MODIFY THIS FILE ####

    adventure.verb_icons = {  # organized by tool mode

        # These are the image filenames and verb(s) associated with
        # each overlay icon:

        "go": {
            "go": ("verb-go.png", "*go"),
            "go back": ("verb-go-back.png", "go back;retreat"),
            "turn left": ("verb-turn-left.png", "turn left;turn to the left;look left;look to the left;left face;face left"),
            "turn right": ("verb-turn-right.png", "turn right;turn to the right;look right;look to the right;right face;face right"),
            "turn around": ("verb-turn-around.png", "turn around;look back;about face"),
        },
        "ex": {
            "ex": ("verb-hint.png", "*ex"),
            "taste": ("verb-taste.png", "taste;lick"),
            "look": ("verb-look.png", "look"),
            "read": ("verb-read.png", "read"),
        },
        "op": {
            "op": ("verb-hint.png", "*op"),
            "hit": ("verb-hit.png", "hit;kick;fight;punch"),
            "eat": ("verb-eat.png", "eat"),
            "wait": ("verb-wait.png", "wait"),
            "taste": ("verb-taste.png", "taste;lick"),
            "read": ("verb-read.png", "read"),
        },
        "say": {
            "speak": ("verb-speak.png", "*say"),
        }
    }

    #### DO NOT MODIFY THIS FILE ####

    adventure.verb_aliases = {

        # The parser will extract the fullest possible tag from the right
        # end of the command string first, then will replace these words
        # (left side of list below) in the remaining verb part to the
        # canonical form (right side) before performing verb matching:
        
        "op": "operate",
        "ex": "examine"
    }

    #### DO NOT MODIFY THIS FILE ####

    adventure.tag_aliases = {

        # Interactables can also match more than one tag.  The tag field can
        # be a semicolon separated list.
        # The following aliases are also applied, the "*" section globally,
        # and other sections can be added here by room name.
        # If the tag exactly matches either side, the term in the other side
        # of the list is implicitly added to the interactable.
        # If the item begins with tilde (~) then it will also be considered
        # a match if it is contained (as whole words) within a larger tag
        # name.  If the other side contains a tilde as well, then the matching
        # portion will be swapped out for the other side, but if the other
        # side does not contain a tilde, then it will be added alone into the
        # tag list.
        
        "*": {
          "~armor": "~armour",
          "~color": "~colour",
        }

    }

    #### DO NOT MODIFY THIS FILE ####

    adventure.tool_verbs = {

        # A click with each of these tools will register as
        # any or all of the verbs listed here:

        "go": [
             "go", "go through",
             "enter", "go in", "go into",
             "exit", "go out", "go out of",
             "go across",
             # "walk",
             # "climb", "climb up", "climb down", "climb across", "climb over",
             # "crawl", "crawl under", "crawl underneath", "crawl across", "crawl through",
         ],
         "ex": [
             "examine", "look", "read", "taste", "listen", "smell"
         ],
         "op": [
             "operate", "use", "touch",
             "press", "push", "pull",
             "open", "close",
             "turn", "turn on", "activate",
             "turn off", "deactivate"
         ],
         "say": [
             "talk", "talk to", "speak", "speak to", "say", "ask"
         ],
         "auto": [
             "*go", "*op", "*say", ".*ex"
         ]
    }

    #### DO NOT MODIFY THIS FILE ####

    adventure.choice_positions = {
        "center": {
            "xpos": 0.5,
            "ypos": 0.5,
            "xanchor": 0.5,
            "yanchor": 0.5,
            "yalign": 0.5,
            "width": 0.5,
            "height": None
        },
        "top": {
            "xpos": 0.5,
            "ypos": 0,
            "xanchor": 0.5,
            "yanchor": 0,
            "yalign": 0,
            "width": 0.5,
            "height": None
        },
        "bottom": {
            "xpos": 0.5,
            "ypos": 1.0,
            "xanchor": 0.5,
            "yanchor": 1.0,
            "yalign": 1.0,
            "width": 0.5,
            "height": None
        },
        "left": {
            "xpos": 0,
            "ypos": 0,
            "xanchor": 0,
            "yanchor": 0,
            "yalign": 0,
            "width": 0.33,
            "height": 1
        },
        "right": {
            "xpos": 1 - 0.33,
            "ypos": 0,
            "xanchor": 1,
            "yanchor": 0,
            "yalign": 0,
            "width": 0.33,
            "height": 1
        }
    }
    
    #### DO NOT MODIFY THIS FILE ####

    # The following are used internally to track state and configuration:

    roomData = {}
    adventure.all_known_flags = set()
    adventure.flag_descriptions = {}
    adventure.persistent_flags = set()
    adventure.scene_flags = set()
    adventure.scene_flags_removed = set()
    adventure.boiled_flags = set()
    adventure.room = []
    adventure.roomName = "demo_room"
    adventure.matched_action = False
    adventure.action_collector = False
    adventure.editing = False
    adventure.modalFreeze = 0
    adventure.mousex = -1
    adventure.mousey = -1
    adventure.visibleMode = "default"
    adventure.interactableId = 0
    adventure.hover_icon = None
    adventure.last_hover_icon = None
    adventure.editorPos = 0
    adventure.result = ""
    adventure.lastRoom = "nowhere"
    adventure.screen_should_exit = False
    adventure.prompt_icons = False
    adventure.targets = []
    adventure.considered_targets = []
    adventure.target_x = -1
    adventure.target_y = -1
    adventure._temp_return = ""
    adventure.plugin_metrics = {}
    adventure.iconSizes = {}
    adventure.screen_icons = []
    adventure.debug_show_inactive = False
    adventure.active_tool = "auto"
    adventure.last_target_stamp = 0
    adventure.last_targets = []
    adventure.last_hint = None
    adventure.gathering_hints = False
    adventure.actions = []
    adventure.multiToolCache = {}
    adventure.rexCache = {}
    adventure.darkThemeCache = None

    build.classify('game/adventure/adventure-editor.rpy', None)
    build.classify('game/adventure/adventure-editor.rpyc', None)
    build.classify('game/adventure/images/editor-icons/**', None)

    # <def>    
    def adventure_cached_exists(filename):
        # <if>
        if not filename in adventure.rexCache:
            adventure.rexCache[filename] = renpy.loadable(filename)
        # </if>
        return adventure.rexCache[filename]
    # </def>
    
    # <def>
    def adventure_is_dark_theme():
        # <if>
        if adventure.darkThemeCache is None:
            bg_color = gui.main_menu_background
            # <if>
            if isinstance(bg_color, str):
                # Fall back to interface text color - light text usually means dark theme
                text_color = Color(gui.text_color)
                r, g, b, a = text_color.rgba
                # If text is light (high values), theme is probably dark
                return (r + g + b) / 3 > 0.5
            # </if>
            # <if>
            if hasattr(bg_color, 'rgba'):
                color = bg_color
            else:
                color = Color(bg_color)
            # </if>
            r, g, b, a = color.rgba
            luminance = 0.299 * r + 0.587 * g + 0.114 * b
            adventure.darkThemeCache = luminance < 0.5  # Dark if luminance is low
        # </if>
        return adventure.darkThemeCache
    # </def adventure_is_dark_theme>
    
    # <def>
    def adventure_dark_inversion():
        return 1 if adventure_is_dark_theme() else 0
    # </def>
    
    # <def>
    def AdventureDarkColorizeMatrix(color):
        """
        Creates a matrix that transforms black pixels to the specified color,
        leaves white pixels white, and preserves transparency.
        """
        r, g, b = color[:3]  # Extract RGB values (0.0 to 1.0)
        
        return Matrix([
            r, 0, 0, 0,     # Red channel: black becomes r, white stays 1.0
            0, g, 0, 0,     # Green channel: black becomes g, white stays 1.0  
            0, 0, b, 0,     # Blue channel: black becomes b, white stays 1.0
            0, 0, 0, 1.0    # Alpha channel: preserved as-is
        ])
    # </def AdventureDarkColorizeMatrix>
    
    def adventure_invert_color(html_color):
        color = Color(html_color)
        r, g, b = color.rgb
        
        # Convert back to 0-255 range and format as hex
        r_int = int((1.0 - r) * 255)
        g_int = int((1.0 - g) * 255)
        b_int = int((1.0 - b) * 255)
        
        return "#{:02x}{:02x}{:02x}".format(r_int, g_int, b_int)   

    def adventure_rgb_to_hsv(r, g, b):
        """Convert RGB (0-1) to HSV (0-1)"""
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        diff = max_val - min_val
        
        # Value
        v = max_val
        
        # Saturation
        s = 0 if max_val == 0 else diff / max_val
        
        # Hue
        if diff == 0:
            h = 0
        elif max_val == r:
            h = (60 * ((g - b) / diff) + 360) % 360
        elif max_val == g:
            h = (60 * ((b - r) / diff) + 120) % 360
        else:
            h = (60 * ((r - g) / diff) + 240) % 360
        
        return h / 360.0, s, v

    def adventure_hsv_to_rgb(h, s, v):
        """Convert HSV (0-1) to RGB (0-1)"""
        h *= 360
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return r + m, g + m, b + m

    def adventure_rotate_hue(html_color, degrees):
        """Rotate hue by specified degrees, preserving saturation and brightness"""
        # Convert hex to RGB
        html_color = html_color.lstrip('#')
        r = int(html_color[0:2], 16) / 255.0
        g = int(html_color[2:4], 16) / 255.0
        b = int(html_color[4:6], 16) / 255.0
        
        # Convert to HSV
        h, s, v = adventure_rgb_to_hsv(r, g, b)
        
        # Rotate hue
        h = (h + degrees / 360.0) % 1.0
        
        # Convert back to RGB
        r, g, b = adventure_hsv_to_rgb(h, s, v)
        
        # Convert to hex
        r_int = int(r * 255)
        g_int = int(g * 255)
        b_int = int(b * 255)
        
        return "#{:02x}{:02x}{:02x}".format(r_int, g_int, b_int)
    
    # <def ThemeColorizeMatrix>
    def AdventureThemeColorizeMatrix(color):
        dark = adventure_is_dark_theme()
        return ColorizeMatrix("#000000", color) * InvertMatrix(1.0) if dark else (ColorizeMatrix("#FFFFFF", color) *
        InvertMatrix(1.0))
    # </def>

    # <def>
    def adventure_icon(name):
        iconset_mid = "/" + adventure.iconset + "/"
        # <if>
        if adventure_cached_exists(adventure.images_base + iconset_mid + name):
            return adventure.images_base + iconset_mid + name
        elif adventure_cached_exists("adventure/images" + iconset_mid + name):
            return "adventure/images" + iconset_mid + name
        else:
            return "adventure/images/free-icons/" + name
        # </if>
    # </def>

    # <def>
    def adventure_toolbar_icon(name):
        iconset_mid = "/" + adventure.toolbar_iconset + "/"
        # <if>
        if adventure_cached_exists(adventure.toolbar_icons_base + iconset_mid + name):
            return adventure.toolbar_icons_base + iconset_mid + name
        elif adventure_cached_exists("adventure/images" + iconset_mid + name):
            return "adventure/images" + iconset_mid + name
        else:
            return "adventure/images/free-icons/" + name
        # </if>
    # </def>

    # <def>
    def adventure_plugin_path(filename):
        relpath = os.path.dirname(filename)
        if relpath.startswith("//game/"):
            relpath = relpath[7:]
        if relpath.startswith("game/"):
            relpath = relpath[5:]
        return relpath
    # </def>

    # <def>
    def adventure_get_relative_path(icon_file, base_path=None):
        base_path = base_path or renpy.config.gamedir
        relative_path = os.path.relpath(icon_file, base_path)
        return relative_path.replace(os.sep, '/')
    # </def>

    # <def>
    def adventure_custom_link(target):
        webbrowser.open(target)
    # </def>

    # <def>
    def adventure_capitalize_first_letter(input_string):
        # <if>
        if not input_string:
            return input_string
        # </if>
        return input_string[0].upper() + input_string[1:]
    # </def>

    # <def>
    def adventure_known_flag(flag):
        return flag.lower() in adventure.all_known_flags
    # </def>

    # <def>
    def adventure_declare_flag(flag, description=None):
        if adventure_known_flag(flag):
            new_flag = (flag, description)
            existing_flag = adventure.flag_descriptions[flag.lower()]
            raise ValueError(f"Flag already declared while trying to declare {new_flag}.  Conflicting flag: {existing_flag}")
        else:
            adventure.all_known_flags.add(flag.lower())
            adventure.flag_descriptions[flag.lower()] = (flag, description)
        # </if>
    # </def adventure_declare_flag>

    # <def>
    def adventure_declare_flags(flag_list):
        # <if>
        if len(flag_list) == 1 and isinstance(flag_list[0], (list, tuple, set)):
            data = flag_list[0]
        else:
            data = flag_list
        # </if>
        # <for>
        for item in data:
            # <if>
            if isinstance(item, str):
                adventure_declare_flag(item, None)
            elif isinstance(item, tuple):
                # <if>
                if len(item) == 1:
                    # Single-element tuple - use as flag name, description is None
                    adventure_declare_flag(item[0], None)
                else:
                    flag, description = item
                    adventure_declare_flag(flag, description)
                # </if>
            else:
                raise ValueError(f"Item must be a string or tuple, got: {type(item).__name__}")
            # </if>
        # </for>
    # </def adventure_declare_flags>

    # <def>
    def adventure_flags(flag_string):
        # <if>
        if not flag_string.strip():
            return set()
        # </if>
        # Split on both comma and semicolon, then clean up whitespace
        raw_flags = []
        # <for>
        for part in flag_string.replace(';', ',').split(','):
            cleaned = part.strip()
            # <if>
            if cleaned:
                raw_flags.append(cleaned)
            # </if>
        # </for>
        result_set = set()
        unknown_flags = set()
        # <for>
        for flag in raw_flags:
            normalized_flag = flag.lower()
            # <if>
            if adventure_known_flag(normalized_flag):
                result_set.add(normalized_flag)
            else:
                unknown_flags.add(flag)  # Keep original case for error message
            # </if>
        # </for>
        # <if>
        if unknown_flags:
            raise ValueError(f"Unknown flags: {unknown_flags}")
        # </if>
        return result_set
    # </def adventure_flags>
    
    # <def>
    def adventure_set_set(target_set, flags):
        """
        Add flags to a target set, handling various input formats.
        
        Args:
            target_set: Set to add flags to (modified in place)
            flags: Can be:
                   - A set of flag names
                   - A list of flag names  
                   - A single string (either a flag name or comma/semicolon-separated list)
        
        Raises:
            ValueError: If any flags are unknown (from adventure_flags validation)
        """
        # <if>
        if isinstance(flags, set):
            # It's already a set - validate each flag and add to target
            unknown_flags = set()
            # <for>
            for flag in flags:
                normalized_flag = flag.lower()
                # <if>
                if adventure_known_flag(normalized_flag):
                    target_set.add(normalized_flag)
                else:
                    unknown_flags.add(flag)
                # </if>
            # </for>
            
            # <if>
            if unknown_flags:
                raise ValueError(f"Unknown flags: {unknown_flags}")
            # </if>
        elif isinstance(flags, list):
            # It's a list - treat each item as a separate flag
            unknown_flags = set()
            # <for>
            for flag in flags:
                # <if>
                if not isinstance(flag, str):
                    raise ValueError(f"List items must be strings, got: {type(flag).__name__}")
                # </if>
                
                normalized_flag = flag.lower()
                # <if>
                if adventure_known_flag(normalized_flag):
                    target_set.add(normalized_flag)
                else:
                    unknown_flags.add(flag)
                # </if>
            # </for>
            # <if>
            if unknown_flags:
                raise ValueError(f"Unknown flags: {unknown_flags}")
            # </if>
        elif isinstance(flags, str):
            parsed_flags = adventure_flags(flags)
            target_set.update(parsed_flags)
        else:
            raise ValueError(f"Flags parameter must be a set, list, or string, got: {type(flags).__name__}")
        # </if>
    # </def adventure_set_set>

    # <def>
    def adventure_unset_set(target_set, flags):
        """
        Remove flags from a target set, handling various input formats.
        
        Args:
            target_set: Set to remove flags from (modified in place)
            flags: Can be:
                   - A set of flag names
                   - A list of flag names  
                   - A single string (either a flag name or comma/semicolon-separated list)
        
        Raises:
            ValueError: If any flags are unknown (from adventure_flags validation)
        """
        # <if>
        if isinstance(flags, set):
            # It's already a set - validate each flag and add to target
            unknown_flags = set()
            # <for>
            for flag in flags:
                normalized_flag = flag.lower()
                # <if>
                if adventure_known_flag(normalized_flag):
                    target_set.discard(normalized_flag)
                else:
                    unknown_flags.add(flag)
                # </if>
            # </for>
            
            # <if>
            if unknown_flags:
                raise ValueError(f"Unknown flags: {unknown_flags}")
            # </if>
        elif isinstance(flags, list):
            # It's a list - treat each item as a separate flag
            unknown_flags = set()
            # <for>
            for flag in flags:
                # <if>
                if not isinstance(flag, str):
                    raise ValueError(f"List items must be strings, got: {type(flag).__name__}")
                # </if>
                
                normalized_flag = flag.lower()
                # <if>
                if adventure_known_flag(normalized_flag):
                    target_set.discard(normalized_flag)
                else:
                    unknown_flags.add(flag)
                # </if>
            # </for>
            # <if>
            if unknown_flags:
                raise ValueError(f"Unknown flags: {unknown_flags}")
            # </if>
        elif isinstance(flags, str):
            # It's a string - use adventure_flags to handle it
            parsed_flags = adventure_flags(flags)
            # <for>
            for flag in parsed_flags:
                target_set.discard(flag)
            # </for>
        else:
            raise ValueError(f"Flags parameter must be a set, list, or string, got: {type(flags).__name__}")
        # </if>
    # </def adventure_unset_set>
    
    # <def>
    def adventure_set(flags):
       adventure_set_set(adventure.persistent_flags, flags)
       adventure_boil_flags()
    # </def adventure_set>

    # <def>
    def adventure_unset(flags):
       adventure_unset_set(adventure.persistent_flags, flags)
       adventure_boil_flags()
    # </def adventure_unset>
    
    # <def>
    def adventure_set_scene(flags, special="unset", unset_flags=None):
       adventure.scene_flags.clear()
       adventure.scene_flags_removed.clear()
       adventure_set_set(adventure.scene_flags, flags)
       # <if>
       if special=="unset" and unset_flags != None:
           adventure_set_set(adventure.scene_flags_removed, unset_flags)
       # </if>
       adventure_boil_flags()
    # </def>
    
    # <def>
    def adventure_boil_flags():
       adventure.boiled_flags = (adventure.persistent_flags | adventure.scene_flags) - adventure.scene_flags_removed
    # </def>

    def adventure_validate_condition(condition, all_known_flags=None):
        """
        Validate a flag condition's syntax and check for unknown flags.
        
        Args:
            condition: String condition to validate
            all_known_flags: Set of known flag names (case-insensitive), or None to skip flag checking
        
        Returns:
            Tuple of (valid, unknown_flags)
            - valid: True if syntax is correct
            - unknown_flags: Set of flag names that aren't in all_known_flags
        """
        # <if>
        if not condition.strip():
            return True, set()
        # </if>
        
        # First, extract all potential flag names regardless of syntax
        unknown_flags = set()
        # <if>
        if all_known_flags is not None:
            # <try>
            try:
                tokens = adventure_condition_tokenize(condition)
                known_lower = {flag.lower() for flag in all_known_flags}
                
                # Find all FLAG tokens and check if they're unknown
                # <for>
                for token_type, token_value in tokens:
                    # <if>
                    if token_type == 'FLAG' and token_value.lower() not in known_lower:
                        unknown_flags.add(token_value)
                    # </if>
                # </for>
            except ValueError:
                # Even if tokenization fails, we still want to try to extract flag-like strings
                unknown_flags = adventure_extract_flag_like_strings(condition, all_known_flags)
            # </try>
        
        # Now validate syntax
        # <try>
        try:
            tokens = adventure_condition_tokenize(condition)
            validator = AdventureConditionValidator(tokens, all_known_flags)
            validator.process()
            return True, unknown_flags
        except ValueError:
            return False, unknown_flags
        # </try>
    # </def adventure_validate_condition>

    # <def>
    def adventure_extract_flag_like_strings(condition, all_known_flags):
        """Extract potential flag names from malformed expressions"""
        unknown_flags = set()
        known_lower = {flag.lower() for flag in all_known_flags}
        
        # Simple character-by-character extraction of identifier-like strings
        i = 0
        # <while>
        while i < len(condition):
            char = condition[i]
            
            # If we find the start of an identifier
            # <if>
            if char.isalpha() or char == '_':
                start = i
                # Continue while we have valid identifier characters
                # <while>
                while i < len(condition) and (condition[i].isalnum() or condition[i] in '_.'):
                    i += 1
                # </while>
                
                potential_flag = condition[start:i]
                # <if>
                if potential_flag.lower() not in known_lower:
                    unknown_flags.add(potential_flag)
                # </if>
            else:
                i += 1
            # </if>
        # </while>
        
        return unknown_flags
    # </def adventure_extract_flag_like_strings>

    # <def>
    def adventure_check_condition(condition, flag_set=None):
        """
        Check if a flag condition is satisfied by the given flag set.
        
        Args:
            flag_set: Set/iterable of flag names
            condition: String like "night & (friday | saturday) | !monday"
        
        Returns:
            Boolean result
        """
        # <if>
        if flag_set is None:
            flag_set = adventure.boiled_flags
        # </if>
        # <if>
        if not condition.strip():
            return True
        # </if>
        
        normalized_flags = {flag.lower() for flag in flag_set}
        tokens = adventure_condition_tokenize(condition)
        evaluator = AdventureConditionEvaluator(tokens, normalized_flags)
        return evaluator.process()
    # </def adventure_check_condition>

    # <def>
    def adventure_condition_tokenize(condition):
        tokens = []
        i = 0
        # <while>
        while i < len(condition):
            char = condition[i]
            # <if>
            if char.isspace():
                i += 1
                continue
            # </if>
            # <if>
            if char in '&|!()':
                # <if>
                if char == '&':
                    tokens.append(('AND', char))
                elif char == '|':
                    tokens.append(('OR', char))
                elif char == '!':
                    tokens.append(('NOT', char))
                elif char == '(':
                    tokens.append(('LPAREN', char))
                elif char == ')':
                    tokens.append(('RPAREN', char))
                # </if>
                i += 1
            # Handle flag names (start with letter or underscore)
            elif char.isalpha() or char == '_':
                start = i
                # Continue while we have valid flag name characters
                # <while>
                while i < len(condition) and (condition[i].isalnum() or condition[i] in '_.'):
                    i += 1
                # </while>
                flag_name = condition[start:i]
                tokens.append(('FLAG', flag_name))
            else:
                raise ValueError(f"Invalid character: '{char}' at position {i}")
            # </if>
        
        return tokens
    # </def adventure_condition_tokenize>

    # <class>
    class AdventureBaseConditionProcessor:
        # <def>
        def __init__(self, tokens):
            self.tokens = tokens
            self.pos = 0
        # </def>
        # <def>
        def current_token(self):
            # <if>
            if self.pos < len(self.tokens):
                return self.tokens[self.pos]
            # </if>
            return None
        # </def>
        # <def>
        def consume(self, expected_type=None):
            token = self.current_token()
            # <if>
            if token and (expected_type is None or token[0] == expected_type):
                self.pos += 1
                return token
            # </if>
            return None
        # </def>
        # <def>
        def process(self):
            """Main entry point - subclasses should call this"""
            result = self.process_or()
            # <if>
            if self.current_token() is not None:
                raise ValueError(f"Unexpected token: {self.current_token()}")
            # </if>
            return result
        # </def>
        # <def>
        def process_or(self):
            """Process OR expressions (lowest precedence)"""
            left = self.process_and()
            # <while>
            while self.current_token() and self.current_token()[0] == 'OR':
                self.consume('OR')
                right = self.process_and()
                left = self.combine_or(left, right)
            # </while>
            
            return left
        # </def>
        # <def>
        def process_and(self):
            """Process AND expressions (higher precedence than OR)"""
            left = self.process_not()
            # <while>
            while self.current_token() and self.current_token()[0] == 'AND':
                self.consume('AND')
                right = self.process_not()
                left = self.combine_and(left, right)
            # </while>
            return left
        # </def>
        # <def>
        def process_not(self):
            """Process NOT expressions (highest precedence except parentheses)"""
            # <if>
            if self.current_token() and self.current_token()[0] == 'NOT':
                self.consume('NOT')
                operand = self.process_primary()
                return self.combine_not(operand)
            else:
                return self.process_primary()
            # </if>
        # </def>
        # <def>
        def process_primary(self):
            """Process primary expressions (flags and parentheses)"""
            token = self.current_token()
            # <if>
            if not token:
                raise ValueError("Unexpected end of expression")
            # </if>
            # <if>
            if token[0] == 'FLAG':
                flag_name = self.consume('FLAG')[1]
                return self.handle_flag(flag_name)
            elif token[0] == 'LPAREN':
                self.consume('LPAREN')
                result = self.process_or()  # Start fresh with OR precedence
                # <if>
                if not self.consume('RPAREN'):
                    raise ValueError("Missing closing parenthesis")
                # </if>
                return result
            else:
                raise ValueError(f"Unexpected token: {token}")
            # </if>
        # </def>
        
        # Abstract methods that subclasses must implement
        # <def>
        def combine_or(self, left, right):
            raise NotImplementedError
        # </def>
        # <def>
        def combine_and(self, left, right):
            raise NotImplementedError
        # </def>
        # <def>
        def combine_not(self, operand):
            raise NotImplementedError
        # </def>
        # <def>
        def handle_flag(self, flag_name):
            raise NotImplementedError
        # </def>
    # </class AdventureBaseConditionProcessor>

    # <class>
    class AdventureConditionValidator(AdventureBaseConditionProcessor):
        """Validates syntax only - unknown flags are handled separately"""
        # <def>
        def __init__(self, tokens, known_flags):
            super().__init__(tokens)
        # </def>
        
        # <def>
        def combine_or(self, left, right):
            return None
        # </def>
        
        # <def>
        def combine_and(self, left, right):
            return None
        # </def>
        
        # <def>
        def combine_not(self, operand):
            return None
        # </def>
        
        # <def>
        def handle_flag(self, flag_name):
            return None
        # </def>
        
        # <def>
        def process(self):
            """Override to return nothing - we just want to validate syntax"""
            super().process()
            return None
        # </def>
    # </class AdventureConditionValidator>

    # <class>
    class AdventureConditionEvaluator(AdventureBaseConditionProcessor):
        """Evaluates conditions against a flag set"""
        # <def>
        def __init__(self, tokens, flag_set):
            super().__init__(tokens)
            self.flag_set = flag_set
        # </def>
        
        # <def>
        def combine_or(self, left, right):
            return left or right
        # </def>
        
        # <def>
        def combine_and(self, left, right):
            return left and right
        # </def>
        
        # <def>
        def combine_not(self, operand):
            return not operand
        # </def>
        
        # <def>
        def handle_flag(self, flag_name):
            return flag_name.lower() in self.flag_set
        # </def>
    # </class AdventureConditionEvaluator>

    # <class>
    class AdventureNineSliceFrame(renpy.Displayable):
        """
        A nine-slice frame displayable with support for render_before base frames.
        """
        
        def __init__(self, image_file, child=None, bgzoom=1.0, matrixcolor=None, style='default', **properties):
            super(AdventureNineSliceFrame, self).__init__(**properties)

            self.child = renpy.displayable(child) if child else None
            self.image_file = image_file
            self.matrixcolor = matrixcolor if matrixcolor is not None else InvertMatrix(0.0)

            # Get margins from registry or use default
            # <if>
            if image_file in adventure.slice_metrics:
                margins = adventure.slice_metrics[image_file]
            else:
                margins = {"top": 16, "left": 16, "right": 16, "bottom": 16 }
            # </if>
            
            # Determine actual image file to load
            # If 'source' is specified in metrics, use that as the actual filename
            # Otherwise, use the image_file parameter as both key and filename
            self.actual_image_file = margins.get("source", image_file)
            self.margin_top = margins["top"]
            self.margin_left = margins["left"]
            self.margin_right = margins["right"]
            self.margin_bottom = margins["bottom"]

            self.extend_top = margins.get("extend-top", 0)
            self.extend_left = margins.get("extend-left", 0)
            self.extend_right = margins.get("extend-right", 0)
            self.extend_bottom = margins.get("extend-bottom", 0)
            self.x_offset = margins.get("x-offset", 0) - self.extend_left
            self.y_offset = margins.get("y-offset", 0) - self.extend_top

            # Handle render_before recursively
            self.render_before_file = margins.get("render_before", None)
            self.render_before_zoom = margins.get("render_before_zoom", 1.0)
            self.render_before_frame = None
            if self.render_before_file:
                # Create the render_before nine-slice frame (no child, as it's just a base)
                self.render_before_frame = AdventureNineSliceFrame(
                    self.render_before_file, 
                    child=None, 
                    bgzoom=bgzoom*self.render_before_zoom, 
                    style=style, 
                    **properties
                )

            # Handle render_after recursively
            self.render_after_file = margins.get("render_after", None)
            self.render_after_zoom = margins.get("render_after_zoom", 1.0)
            self.render_after_frame = None
            if self.render_after_file:
                # Create the render_after nine-slice frame (no child, as it's just an overlay)
                self.render_after_frame = AdventureNineSliceFrame(
                    self.render_after_file, 
                    child=None, 
                    bgzoom=bgzoom*self.render_after_zoom,
                    style=style,
                    **properties
                )

            # Load base image and get original size
            self.base_image = Image(self.actual_image_file)
            self.orig_width, self.orig_height = self.base_image.load().get_size()

            rwidth = margins.get("source_render_width", None)
            rheight = margins.get("source_render_height", None)
            rzoom = margins.get("zoom", 1.0)

            if rwidth is not None:
                # Calculate the nine-slice area width (excluding extension areas)
                nineslice_orig_width = self.orig_width - self.extend_left - self.extend_right
                self.bgzoom = (rwidth / nineslice_orig_width) * bgzoom
            elif rheight is not None:
                # Calculate the nine-slice area height (excluding extension areas)
                nineslice_orig_height = self.orig_height - self.extend_top - self.extend_bottom
                self.bgzoom = (rheight / nineslice_orig_height) * bgzoom
            else:
                self.bgzoom = bgzoom * rzoom

            # Create cropped and bgzoomed pieces
            self.pieces = self._create_pieces()

        def _create_pieces(self):
            """Create the 9 cropped pieces from the main image"""
            pieces = {}

            # Apply bgzoom to the base image first, then crop
            if self.bgzoom != 1.0:
                zoomed_image = Transform(self.base_image, zoom=self.bgzoom)
            else:
                zoomed_image = self.base_image

            # Use original margins for cropping (before any zoom scaling)
            left = self.extend_left
            right = self.extend_right
            top = self.extend_top
            bottom = self.extend_bottom
            mleft = self.margin_left
            mright = self.margin_right
            mtop = self.margin_top
            mbottom = self.margin_bottom

            # Calculate zoomed dimensions for cropping
            zoomed_left = int(left * self.bgzoom) + int(mleft * self.bgzoom)
            zoomed_right = int(right * self.bgzoom) + int(mright * self.bgzoom)
            zoomed_top = int(top * self.bgzoom) + int(mtop * self.bgzoom)
            zoomed_bottom = int(bottom * self.bgzoom) + int(mbottom * self.bgzoom)
            zoomed_width = int(self.orig_width * self.bgzoom)
            zoomed_height = int(self.orig_height * self.bgzoom)

            center_width = zoomed_width - zoomed_left - zoomed_right
            center_height = zoomed_height - zoomed_top - zoomed_bottom

            # Create pieces by cropping the zoomed image
            # Top row
            pieces['tl'] = Transform(zoomed_image, crop=(0, 0, zoomed_left, zoomed_top), matrixcolor=self.matrixcolor)
            pieces['top'] = Transform(zoomed_image, crop=(zoomed_left, 0, center_width, zoomed_top), matrixcolor=self.matrixcolor)
            pieces['tr'] = Transform(zoomed_image, crop=(zoomed_left + center_width, 0, zoomed_right, zoomed_top), matrixcolor=self.matrixcolor)

            # Middle row
            pieces['left'] = Transform(zoomed_image, crop=(0, zoomed_top, zoomed_left, center_height), matrixcolor=self.matrixcolor)
            pieces['middle'] = Transform(zoomed_image, crop=(zoomed_left, zoomed_top, center_width, center_height), matrixcolor=self.matrixcolor)
            pieces['right'] = Transform(zoomed_image, crop=(zoomed_left + center_width, zoomed_top, zoomed_right, center_height), matrixcolor=self.matrixcolor)

            # Bottom row
            pieces['bl'] = Transform(zoomed_image, crop=(0, zoomed_top + center_height, zoomed_left, zoomed_bottom), matrixcolor=self.matrixcolor)
            pieces['bottom'] = Transform(zoomed_image, crop=(zoomed_left, zoomed_top + center_height, center_width, zoomed_bottom), matrixcolor=self.matrixcolor)
            pieces['br'] = Transform(zoomed_image, crop=(zoomed_left + center_width, zoomed_top + center_height, zoomed_right, zoomed_bottom), matrixcolor=self.matrixcolor)

            return pieces

        def _calculate_main_frame_dimensions(self, width, height):
            """Calculate the main frame dimensions based on child content, using bgzoom from source_render_width"""
            # Get child size if we have one
            child_width = child_height = 0
            if self.child:
                child_render = renpy.render(self.child, width, height, 0, 0)
                child_width, child_height = child_render.get_size()

            # Calculate the actual sizes of the bgzoomed pieces (margins are scaled by bgzoom)
            actual_left_width = int(self.extend_left * 0 * self.bgzoom) + int(self.margin_left * self.bgzoom)
            actual_right_width = int(self.extend_right * 0 * self.bgzoom) + int(self.margin_right * self.bgzoom)
            actual_top_height = int(self.extend_top * 0 * self.bgzoom) + int(self.margin_top * self.bgzoom)
            actual_bottom_height = int(self.extend_bottom * 0 * self.bgzoom) + int(self.margin_bottom * self.bgzoom)

            # Calculate minimum frame size needed based on content and scaled margins
            min_width = actual_left_width + actual_right_width + child_width
            min_height = actual_top_height + actual_bottom_height + child_height
            
            # Determine main frame size based on content requirements
            main_frame_width = max(min_width, width if width < 999999 else min_width)
            main_frame_height = max(min_height, height if height < 999999 else min_height)

            return main_frame_width, main_frame_height, child_width, child_height

        def _render_nine_slice(self, render, frame_width, frame_height, offset_x, offset_y, st, at):
            """Render the nine-slice pieces to the given render object"""
            # Calculate the actual sizes of the bgzoomed pieces
            actual_frame_width = frame_width + int(self.extend_left*self.bgzoom) + int(self.extend_right * self.bgzoom)
            actual_frame_height = frame_height + int(self.extend_top*self.bgzoom) + int(self.extend_bottom * self.bgzoom)

            actual_left_width = int(self.extend_left*self.bgzoom) + int(self.margin_left*self.bgzoom)
            actual_right_width = int(self.extend_right*self.bgzoom) + int(self.margin_right*self.bgzoom)
            actual_top_height = int(self.extend_top*self.bgzoom) + int(self.margin_top*self.bgzoom)
            actual_bottom_height = int(self.extend_bottom*self.bgzoom) + int(self.margin_bottom* self.bgzoom)
            actual_mleft_width = int(self.margin_left * self.bgzoom)
            actual_mright_width = int(self.margin_right * self.bgzoom)
            actual_mtop_height = int(self.margin_top * self.bgzoom)
            actual_mbottom_height = int(self.margin_bottom * self.bgzoom)

            # Calculate stretching dimensions
            stretch_width = int(frame_width - actual_mleft_width - actual_mright_width)
            stretch_height = int(frame_height - actual_mtop_height - actual_mbottom_height)

            # RENDER MIDDLE FIRST (as background layer)
            if stretch_width > 0 and stretch_height > 0:
                middle_piece = Transform(self.pieces['middle'],
                                       xsize=stretch_width,
                                       ysize=stretch_height,
                                       fit="stretch")
                middle_render = renpy.render(middle_piece, stretch_width, stretch_height, st, at)
                render.blit(middle_render, (actual_left_width + offset_x, actual_top_height + offset_y))

            # RENDER EDGES ON TOP OF MIDDLE
            if stretch_width > 0:
                if actual_top_height > 0:
                    # Top edge: stretch horizontally, keep natural height
                    top_piece = Transform(self.pieces['top'],
                                        xsize=stretch_width,
                                        ysize=actual_top_height,
                                        fit="stretch")
                    top_render = renpy.render(top_piece, stretch_width, actual_top_height, st, at)
                    render.blit(top_render, (actual_left_width + offset_x, 0 + offset_y))

                if actual_bottom_height > 0:
                    # Bottom edge: stretch horizontally, keep natural height
                    bottom_piece = Transform(self.pieces['bottom'],
                                           xsize=stretch_width,
                                           ysize=actual_bottom_height,
                                           fit="stretch")
                    bottom_render = renpy.render(bottom_piece, stretch_width, actual_bottom_height, st, at)
                    render.blit(bottom_render, (actual_left_width + offset_x, actual_top_height + stretch_height + offset_y))

            if stretch_height > 0:
                if actual_left_width > 0:
                    # Left edge: keep natural width, stretch vertically
                    left_piece = Transform(self.pieces['left'],
                                         xsize=actual_left_width,
                                         ysize=stretch_height,
                                         fit="stretch")
                    left_render = renpy.render(left_piece, actual_left_width, stretch_height, st, at)
                    render.blit(left_render, (0 + offset_x, actual_top_height + offset_y))

                if actual_right_width > 0:
                    # Right edge: keep natural width, stretch vertically
                    right_piece = Transform(self.pieces['right'],
                                          xsize=actual_right_width,
                                          ysize=stretch_height,
                                          fit="stretch")
                    right_render = renpy.render(right_piece, actual_right_width, stretch_height, st, at)
                    render.blit(right_render, (actual_left_width + stretch_width + offset_x, actual_top_height + offset_y))

            # RENDER CORNERS LAST (on top of everything)
            if actual_left_width > 0 and actual_top_height > 0:
                tl_render = renpy.render(self.pieces['tl'], actual_left_width, actual_top_height, st, at)
                render.blit(tl_render, (0 + offset_x, 0 + offset_y))

            if actual_right_width > 0 and actual_top_height > 0:
                tr_render = renpy.render(self.pieces['tr'], actual_right_width, actual_top_height, st, at)
                render.blit(tr_render, (actual_left_width + stretch_width + offset_x, 0 + offset_y))

            if actual_left_width > 0 and actual_bottom_height > 0:
                bl_render = renpy.render(self.pieces['bl'], actual_left_width, actual_bottom_height, st, at)
                render.blit(bl_render, (0 + offset_x, actual_top_height + stretch_height + offset_y))

            if actual_right_width > 0 and actual_bottom_height > 0:
                br_render = renpy.render(self.pieces['br'], actual_right_width, actual_bottom_height, st, at)
                render.blit(br_render, (actual_left_width + stretch_width + offset_x, actual_top_height + stretch_height + offset_y))

        def render(self, width, height, st, at):
            # Calculate main frame dimensions based on child content
            main_frame_width, main_frame_height, child_width, child_height = self._calculate_main_frame_dimensions(width, height)
            
            # Determine total render size considering extensions (scaled from native pixels)
            scaled_extend_width = int(self.extend_left*self.bgzoom) + int(self.extend_right * self.bgzoom)
            scaled_extend_height = int(self.extend_top*self.bgzoom) + int(self.extend_bottom * self.bgzoom)
            total_render_width = main_frame_width + scaled_extend_width
            total_render_height = main_frame_height + scaled_extend_height
            
            # If we have render_before or render_after frames, we need to account for their extensions too
            render_before_extensions_x = 0
            render_before_extensions_y = 0
            render_before_render = None
            render_after_extensions_x = 0
            render_after_extensions_y = 0
            render_after_render = None
            
            if self.render_before_frame:
                # Render the render_before frame with the same main frame size
                # This ensures it uses the same base dimensions but may extend beyond
                render_before_render = self.render_before_frame.render(main_frame_width, main_frame_height, st, at)
                render_before_width, render_before_height = render_before_render.get_size()
                
                # Update total render size to accommodate render_before extensions
                total_render_width = max(total_render_width, render_before_width)
                total_render_height = max(total_render_height, render_before_height)

            if self.render_after_frame:
                # Render the render_after frame with the same main frame size
                # This ensures it uses the same base dimensions but may extend beyond
                render_after_render = self.render_after_frame.render(main_frame_width, main_frame_height, st, at)
                render_after_width, render_after_height = render_after_render.get_size()
                
                # Update total render size to accommodate render_after extensions
                total_render_width = max(total_render_width, render_after_width)
                total_render_height = max(total_render_height, render_after_height)

            # Create the final render with the calculated total size
            render = renpy.Render(total_render_width, total_render_height)

            # Render the render_before frame first (as base layer)
            if render_before_render:
                # Position the render_before frame, accounting for its own offsets
                render_before_x = 0
                render_before_y = 0
                render.blit(render_before_render, (render_before_x, render_before_y))

            # Render our main nine-slice frame on top
            # Position it using scaled offsets (offsets are in native pixels)
            main_frame_offset_x = int(self.x_offset * self.bgzoom)
            main_frame_offset_y = int(self.y_offset * self.bgzoom)
            
            self._render_nine_slice(render, main_frame_width, main_frame_height, 
                                   main_frame_offset_x, main_frame_offset_y, st, at)

            # Render child content if present - positioned relative to MAIN frame only
            if self.child:
                child_render = renpy.render(self.child, width, height, st, at)
                
                # Use content margins to position child in correct area (ignoring extensions/offsets)
                actual_content_left = 0 # int(self.content_margin_left * self.bgzoom)
                actual_content_right = 0 # int(self.content_margin_right * self.bgzoom)
                actual_content_top = 0 # int(self.content_margin_top * self.bgzoom)
                actual_content_bottom = 0 # int(self.content_margin_bottom * self.bgzoom)

                # Center the child in the main frame content area (excluding shaded areas)
                available_width = main_frame_width - actual_content_left - actual_content_right
                available_height = main_frame_height - actual_content_top - actual_content_bottom
                child_x = actual_content_left + (available_width - child_width) // 2
                child_y = actual_content_top + (available_height - child_height) // 2

                # Apply main frame offset to child positioning
                child_x += main_frame_offset_x
                child_y += main_frame_offset_y

                render.blit(child_render, (child_x, child_y))

            # Render the render_after frame last (as top overlay layer)
            if render_after_render:
                # Position the render_after frame, accounting for its own offsets
                render_after_x = 0
                render_after_y = 0
                render.blit(render_after_render, (render_after_x, render_after_y))

            return render
    # </class>

    class AdventureExpandedDisplayable(renpy.Displayable):
        # <def>
        def __init__(self, child, expand_left=0, expand_right=0, expand_top=0, expand_bottom=0, **kwargs):
            super(AdventureExpandedDisplayable, self).__init__(**kwargs)
            
            self.child = renpy.displayable(child)
            self.expand_left = expand_left
            self.expand_right = expand_right  
            self.expand_top = expand_top
            self.expand_bottom = expand_bottom
        # </def __init__>
            
        # <def>
        def render(self, width, height, st, at):
            # Render the child displayable
            child_render = renpy.render(self.child, width, height, st, at)
            child_width, child_height = child_render.get_size()
            
            # Calculate expanded dimensions
            expanded_width = child_width + self.expand_left + self.expand_right
            expanded_height = child_height + self.expand_top + self.expand_bottom
            
            # Create the expanded render
            render = renpy.Render(expanded_width, expanded_height)
            
            # Position the child in the center of the expanded area
            render.blit(child_render, (self.expand_left, self.expand_top))
            
            return render
        # </def render>
            
        def visit(self):
            return [self.child]
        # </def>
    # </class>

    # <def>
    def AdventureExpandedBackground(displayable, left=0, right=0, top=0, bottom=0):
        return AdventureExpandedDisplayable(displayable, left, right, top, bottom)
    # </def>
    
    # <def>
    def adventure_tool_applies(tool, layers):
        # <if>
        if tool in layers:
            return True
        else:
            # <for>
            for verb in adventure.tool_verbs[tool]:
                included_tool = None
                # <if>
                if verb.startswith('*'):
                    included_tool = verb[1:]
                elif verb.startswith('.*'):
                    included_tool = verb[2:]
                # </if>
                # <if>
                if included_tool is not None:
                    # <if>
                    if included_tool in layers:
                        return True
                    # </if>
                # </if>
            # </for>
        # </if>
    # </def>

    # <class>
    class AdventureGetMousePosition(renpy.Displayable):

        # <def>
        def __init__(self):
            renpy.Displayable.__init__(self)
        # </def __init__>

        # <def>
        def event(self, ev, x, y, st):
            import pygame
            # <try>
            try:
                adventure_editor_event(ev, x, y, st)
            except:
                pass
            # </try>
            need_res = False
            # <if>
            this_stamp = time.time()
            waited = abs(this_stamp - adventure.last_target_stamp) > 0.1
            if (ev.type == pygame.MOUSEMOTION and waited) or ev.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                adventure.hover_icon = None
                adventure_fix_message()
                adventure.last_target_stamp = this_stamp
                adventure.last_targets = adventure.targets
                clicking = ev.type == pygame.MOUSEBUTTONDOWN
                clicked = ev.type == pygame.MOUSEBUTTONUP
                adventure.mousex = x
                adventure.mousey = y
                current_x = adventure.mousex
                current_y = adventure.mousey
                # <try>
                try:
                    # <if>
                    if clicked and ev.button == 1:
                        current_handled = adventure_editor_mouse(adventure.mousex, adventure.mousey)
                    else:
                        current_handled = False
                    # </if>
                except:
                    current_handled = False
                    adventure.editing = False
                # </try>
                # <if>
                if not current_handled and current_x > 0 and current_y > 0 and adventure.modalFreeze == 0:
                    adventure.targets = []
                    # <for>
                    for i in range(len(adventure.room)):
                        layers = []
                        # <for>
                        for layer in ["ex", "say", "op", "go"]:
                            # <if>
                            if adventure_active_value(adventure.room[i][layer]) != "":
                                layers.append(layer)
                            # </if>
                        # </for>
                        # </if>
                        if (
                            adventure.room[i]["type"] == "polygon"
                            and (len(adventure.room[i]["points"]) > 2)
                            and adventure_tool_applies(adventure.active_tool, layers)
                            and adventure_check_condition(adventure.room[i]["condition"])
                        ):
                            # <if>
                            if adventure_point_in_polygon(adventure.mousex, adventure.mousey, adventure.room[i]["points"]):
                                adventure.targets.append((i, ""))
                                adventure.hover_icon = None
                            # </if>
                        # </if polygon with at least 3 points>
                    # </for all polygons in room>
                    best_icon = None
                    best_distance = 99999
                    # <for>
                    for icon in adventure.screen_icons:
                        if icon["active"] and adventure_point_in_icon(current_x, current_y, icon):
                            adventure.hover_icon = (icon["interactableId"], icon["verb"])
                            adventure.targets = [(icon["interactableId"], icon["verb"])]
                        if len(adventure.targets) == 0 and icon["active"]:
                            icon_distance = adventure_icon_distance(current_x, current_y, icon)
                            # <if>
                            if icon_distance < adventure.icon_grace_radius and icon_distance < best_distance:
                                best_icon = (icon["interactableId"], icon["verb"])
                                best_distance = icon_distance
                            # </if>
                        # </if>
                    # </for>
                    # <if>
                    if len(adventure.targets) == 0 and best_icon is not None:
                        adventure.hover_icon = best_icon
                        adventure.targets = [best_icon]
                    # </if>
                    # <if>
                    if adventure.hover_icon != adventure.last_hover_icon:
                        need_res = True
                    # </if>
                    # <if>
                    if clicking and ev.button == 1:
                        adventure.considered_targets = adventure.targets
                    # </if>
                    if clicked and ev.button == 1 and adventure.targets == adventure.considered_targets:
                        adventure.target_x = adventure.mousex
                        adventure.target_y = adventure.mousey
                        adventure._temp_return = "clicked"
                        adventure.screen_should_exit = True
                        renpy.restart_interaction()
                        raise renpy.IgnoreEvent()
                    elif (adventure.targets != adventure.last_targets) and adventure.action_tip:
                        adventure.gathering_hints = True
                        hint = ""
                        # <for>
                        for act in adventure.actions:
                            hint = player_chooses_to(act)
                            # <if>
                            if hint != "":
                                break
                            else:
                                hint = ""
                            # </if>
                        # </for>
                        if hint != adventure.last_hint:
                            adventure.last_hint = hint
                            adventure.gathering_hints = False
                            need_res = True
                    # </if>
                # </if valid point and not modalFreeze>
            # </if MOUSEBUTTONDOWN, MOUSEBUTTONUP, or MOUSEMOTION>
            # <if>
            if need_res:
                renpy.restart_interaction()
            # </if>
        # </def event>

        # <def>
        def render(self, width, height, st, at):
            return renpy.Render(1, 1)
        # </def render>
    # </class AdventureGetMousePosition>

    # Initialize the mouse position variables
    adventure.mouse_position = AdventureGetMousePosition()
    
    # <def>
    def adventure_measure_text_height(text_content, width, **text_properties):
        # Create a Text displayable with your properties
        text_obj = Text(text_content, **text_properties)
        
        # Render it at the specified width
        rendered = renpy.render(text_obj, width, 999999, 0, 0)
        
        # Get the actual height
        text_width, text_height = rendered.get_size()
        return text_height
    # </def>
    
    # <def>
    def adventure_measure_height_at_width(displayable, constrained_width, constrained_height=9999):
        # Render with constrained width but unlimited height
        rendered = renpy.render(displayable, constrained_width, constrained_height, 0, 0)
        
        # Get the height it needs at that width
        width, height = rendered.get_size()
        return height
    # </def>

    # <def>
    def adventure_point_in_icon(x, y, icon):
        center_x, center_y = icon["position"]
        width, height = icon["size"]
        half_width = (width // 2)
        half_height = (height // 2)
        left = center_x - half_width
        right = center_x + half_width
        top = center_y - half_height
        bottom = center_y + half_height
        return left <= x <= right and top <= y <= bottom
    # </def>
    
    # <def>
    def adventure_icon_distance(x, y, icon):
        center_x, center_y = icon["position"]
        # Calculate Euclidean distance from point to center
        distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
        return distance
    # </def>

    # <def>
    def adventure_point_in_polygon(x, y, points):
        """
        Determine if a point is inside a polygon using the ray casting algorithm.
        
        Args:
            x, y: Coordinates to test
            points: List of (x, y) tuples defining the polygon vertices
            
        Returns:
            True if point is inside polygon, False otherwise
        """

        # <if>
        if len(points) < 3:
            return False
        # </if>
        
        n = len(points)
        inside = False
        
        p1x, p1y = points[0]
        # <for>
        for i in range(1, n + 1):
            p2x, p2y = points[i % n]
            # <if>
            if y > min(p1y, p2y):
                # <if>
                if y <= max(p1y, p2y):
                    # <if>
                    if x <= max(p1x, p2x):
                        # <if>
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        # </if>
                        # <if>
                        if p1x == p2x or x <= xinters:
                            inside = not inside
                        # </if>
                    # </if x le>
                # </if y le>
            # </if y gt>
            p1x, p1y = p2x, p2y
        # </for>
        return inside
    # </def adventure_point_in_polygon>

    # <def>
    def adventure_escape_renpy(text):
        """Escapes characters with special meaning in Ren'Py text."""
        # Ren'Py's string interpolation and text tag delimiters
        text = text.replace('{', '{{')
        text = text.replace('[', '[[')
        
        # Percent sign for variable interpolation
        text = text.replace('%', '%%')
        
        # Handle single and double quotes if needed, though usually unnecessary
        text = text.replace("'", "\\'")
        text = text.replace('"', '\\"')

        # The backslash must be escaped last, after other escape sequences are handled.
        # This replaces a literal backslash with two backslashes.
        text = text.replace('\\', '\\\\')
        return text
    # </def>

    # <def>
    def adventure_get_image_dimensions(image_path):
        """Get dimensions using renpy.render()"""
        # <try>
        try:
            img = Image(image_path)
            # Render the image to get its surface
            rendered = renpy.render(img, 0, 0, 0, 0)
            width, height = rendered.get_size()
            return width, height
        except Exception as e:
            renpy.log(f"Error getting size for {image_path}: {e}")
            return None, None
        # </try>
    # </def>

    # <def>
    def adventure_refresh_icon_dimensions():
        # <for>
        for tool in adventure.verb_icons:
            # <for>
            for verb in adventure.verb_icons[tool]:
                icon_name = adventure.images_base + "/" + adventure.iconset + "/" + adventure.verb_icons[tool][verb][0]
                real_icon_name = icon_name
                if not adventure_cached_exists(icon_name):
                    real_icon_name = "adventure/images/" + adventure.iconset + "/" + adventure.verb_icons[tool][verb][0]
                if not adventure_cached_exists(icon_name):
                    real_icon_name = "adventure/images/free-icons/" + adventure.verb_icons[tool][verb][0]
                adventure.iconSizes[real_icon_name] = adventure_get_image_dimensions(real_icon_name)
            # </for>
        # </for>

        icon_name = adventure.images_base + "/" + adventure.iconset + "/hover-glow.png"
        real_icon_name = icon_name
        if not adventure_cached_exists(icon_name):
            real_icon_name = "adventure/images/" + adventure.iconset + "/hover-glow.png"
        if not adventure_cached_exists(icon_name):
            real_icon_name = "adventure/images/free-icons/hover-glow.png"
        adventure.iconSizes[real_icon_name] = adventure_get_image_dimensions(real_icon_name)

        icon_name = adventure.toolbar_icons_base + "/" + adventure.toolbar_iconset + "/toolbar-active.png"
        real_icon_name = icon_name
        if not adventure_cached_exists(icon_name):
            real_icon_name = "adventure/images/" + adventure.toolbar_iconset + "/toolbar-active.png"
        adventure.iconSizes[real_icon_name] = adventure_get_image_dimensions(real_icon_name)
        icon_name = adventure.toolbar_icons_base + "/" + adventure.toolbar_iconset + "/toolbar-inactive.png"
        real_icon_name = icon_name
        if not adventure_cached_exists(icon_name):
            real_icon_name = "adventure/images/" + adventure.toolbar_iconset + "/toolbar-inactive.png"
        adventure.iconSizes[real_icon_name] = adventure_get_image_dimensions(real_icon_name)
    # </def>
    
    # <def>
    def adventure_init():
        # <if>
        if not adventure.initialized:
            # <if>
            if adventure.do_logging:
                gui.history_allow_tags.update({"b", "i"})
            # </lif>
            author_message_1 = """
This game is built using \"Adventure for Ren'Py\" by Jeffrey R. Day:
A free (MIT Licensed) module to add point-and-click adventure game support to RenPy.
https://github.com/phroun/adventure-for-renpy

Please consider supporting development of the \"Adventure for Ren'Py\" module by donating to me on ko-fi:
https://ko-fi.com/jeffday
            """
            print(author_message_1)
            # <try>
            try:
                store.roomData.update(room_definitions)
            except:
                print("\nWARNING: No room data loaded")
            # </try>
            adventure_refresh_icon_dimensions()
            adventure.initialized = True
            # <if>
            if adventure.prompt_icons:
                # <try>
                try:
                    adventure_icon_setup_continue()
                except:
                    pass
                # </try>
            # </if>
        # </if>
    # </def adventure_init>

    # <def>
    def adventure_canonize_phrase(phrase, aliases):
        # Split the phrase into words
        words = phrase.split()

        # Convert each word to canonical form if it exists in aliases
        canonical_words = []
        # <for>
        for word in words:
            # Check for case-insensitive match in aliases
            lowercase_word = word.lower()
            # <if>
            if lowercase_word in aliases:
                canonical_words.append(aliases[lowercase_word])
            else:
                # Preserve original case if no match found
                canonical_words.append(word)
            # </if>
        # </for>
        return " ".join(canonical_words)
    # </def>

    # <def>
    def adventure_apply_tag_aliases(these_nouns, tag_aliases, room_name):
        possible_nouns = these_nouns[:]  # Start with a copy of original nouns

        # Get aliases to apply - global "*" section plus room-specific
        aliases_to_apply = {}
        # <if>
        if "*" in tag_aliases:
            aliases_to_apply.update(tag_aliases["*"])
        # </if>
        # <if>
        if room_name in tag_aliases:
            aliases_to_apply.update(tag_aliases[room_name])
        # </if>

        # Process each alias rule
        # <for>
        for alias_key, alias_value in aliases_to_apply.items():
            key_has_tilde = alias_key.startswith("~")
            value_has_tilde = alias_value.startswith("~")

            # Clean keys/values of tildes for processing
            clean_key = alias_key[1:] if key_has_tilde else alias_key
            clean_value = alias_value[1:] if value_has_tilde else alias_value

            # <for>
            for noun in these_nouns[:]:  # Iterate over copy to avoid modification issues
                matched = False

                # <if>
                if key_has_tilde:
                    # Check if clean_key is contained as whole words within noun
                    noun_words = noun.split()
                    noun_words_lower = [word.lower() for word in noun_words]
                    clean_key_lower = clean_key.lower()
                    
                    # <if>
                    if clean_key_lower in noun_words_lower:
                        matched = True
                        # <if>
                        if value_has_tilde:
                            # Replace the matching portion with clean_value, preserving case of non-matching words
                            new_noun_words = []
                            # <for>
                            for word in noun_words:
                                # <if>
                                if word.lower() == clean_key_lower:
                                    new_noun_words.append(clean_value)
                                else:
                                    new_noun_words.append(word)
                                # </if>
                            # </for>
                            new_noun = " ".join(new_noun_words)
                            # <if>
                            if new_noun not in possible_nouns:
                                possible_nouns.append(new_noun)
                            # </if>
                        else:
                            # Add clean_value alone
                            # <if>
                            if clean_value not in possible_nouns:
                                possible_nouns.append(clean_value)
                            # </if>
                        # </if value has tilde else>
                    # </if clean_key in noun_words>
                else:
                    # Exact match required (case-insensitive)
                    # <if>
                    if noun.lower() == clean_key.lower():
                        matched = True
                        # <if>
                        if clean_value not in possible_nouns:
                            possible_nouns.append(clean_value)
                        # </if>
                    # </if noun matches clean_key>
                # </if key has tilde else>
            # </for>
        # </for>
        return possible_nouns
    # </def adventure_apply_tag_aliases>
    
    # <def>
    def adventure_multi_tools(tool):
        # <if>
        if not tool in adventure.multiToolCache:
            active_tools = [tool]
            # <if>
            if tool in adventure.tool_verbs:
                # <for>
                for verb in adventure.tool_verbs[tool]:
                    # <if>
                    if verb.startswith('*'):
                        active_tools.append(verb[1:])
                    if verb.startswith('.*'):
                        active_tools.append(verb[2:])
                    # </if>
                # </for>
            # </if>
            adventure.multiToolCache[tool] = active_tools
        # </if>
        return adventure.multiToolCache[tool]
    # </def>

    # <def>
    def player_chooses_to(command, read_as = None):
        # <if>
        if adventure.action_collector:
            adventure.actions.append(command)
            return False
        # </if>
        cmd_words = command.split()
        cmdc = " ".join(cmd_words)
        cmd = cmdc.lower()
        sentences = []

        active_tools = adventure_multi_tools(adventure.active_tool)

        # <for>
        for tool in active_tools:
            verbs = adventure.tool_verbs[tool]
            toolgroup = '*' + tool
            # <for>
            for idx, iconverb in adventure.targets:
                # <if>
                if iconverb != "" or tool in adventure.room[idx]:
                    # <if>
                    if iconverb != "":
                        group_bits = [iconverb]
                    else:
                        group_bits = adventure.room[idx][tool].lower().split("//", 1)
                    # </if>
                    # <if>
                    if len(group_bits) > 0:
                        inter_verbs = group_bits[0].split(";")
                        these_verbs = []
                        # <for>
                        for inter_verb in inter_verbs:
                            # <if>
                            if inter_verb.startswith('*') or inter_verb.startswith('.*'):
                                # expand group to list of verbs
                                these_verbs.extend(adventure.tool_verbs[inter_verb[1:]])
                            else:
                                # <if>
                                if inter_verb != "":
                                    these_verbs.append(inter_verb)
                                # </if>
                            # </if>
                        # </for>
                        these_nouns = []
                        targ_bits = adventure.room[idx]["tag"].split("//", 1)
                        # <if>
                        if len(targ_bits) > 0:
                            these_nouns.extend(targ_bits[0].split(";"))
                        # </if>
                        possible_nouns = adventure_apply_tag_aliases(these_nouns, adventure.tag_aliases, adventure.roomName)
                        # <for>
                        for verb in these_verbs:
                            # <for>
                            for noun in possible_nouns:
                                canonical_verb = adventure_canonize_phrase(verb.lower(), adventure.verb_aliases)
                                sentences.append((canonical_verb.lower(), noun if noun != "." else ""))
                            # </for>
                        # </for groups>
                    # </if>
                # </if valid tool>
            # <for targets>
        # </for>
        matches = []

        # <for>
        for sentence in sentences:
            verb, noun = sentence
            # <if>
            if cmd.endswith(" " + noun.lower()) or noun == "":
                # <if>
                if noun == "":
                    remainder = cmd
                    crem = cmdc
                else:
                    remainder = cmd[:-(len(noun)+1)]
                    crem = cmdc[:-(len(noun)+1)]
                # </if>
                canonical_cmd = adventure_canonize_phrase(crem, adventure.verb_aliases)
                # <if>
                if canonical_cmd.lower().startswith(verb):
                    slurry = canonical_cmd[len(verb):]
                    matches.append((verb + slurry + " " + noun, len(noun)))
                # <if>
            # </if ends with noun>
        # </for>

        # <if>
        if False and read_as and len(matches) != 0:
           bestmatch = read_as
        else:
            highest = -1
            bestmatch = ""
            # <for>
            for match, nl in matches:
                # <if>
                if nl > highest:
                    highest = nl
                    bestmatch = match
                # </if>
            # </for>
        # </if>

        # <if>
        if not adventure.gathering_hints:
            # <if>
            if adventure.first_person != None:
                # <if>
                if adventure.first_person:
                    person = "I "
                else:
                    person = "You "
                # </if>
                # <if>
                if bestmatch.strip() != "":
                    adventure.matched_action = True
                    logtext = "{b}{i}" + person + adventure_escape_renpy(bestmatch) + "{/i}{/b}"
                    ADVENTURE_LOG.add_history(kind="adv", what=logtext, who=ADVENTURE_LOG.name)
                # </if>
            # </if>
            return len(matches) != 0
        else:
            return bestmatch  # this goes to the hint collector!
        # </if>
    # </def>

    # <def>
    def player_examines(*targets_and_responses):
        # <if>
        if len(targets_and_responses) == 1 and isinstance(targets_and_responses[0], (list, tuple, set)):
            data = targets_and_responses[0]
        else:
            data = targets_and_responses
        # </if>
        # <for>
        for target, response in data:
            # <if>
            if player_chooses_to("examine " + target):
                # Force proper text display
                renpy.say(ADVENTURE_NARRATOR, response)
                return True
            # </if>
        # </for>
        return False
    # </def>

    # <def>
    def adventure_active_value(value):
        # <if>
        if value == "":
            return ""
        else:
            # <if>
            if value[0] == "/":
                return ""
            else:
                return value
            # </if>
        # </if>
    # </def>
    
    # <def>
    def adventure_set_tool(new_tool):
        adventure.active_tool = new_tool
    # <def>

    # <def>
    def adventure_fix_message():
        # <try>
        try:
            if not "adventure-for-renpy" in gui.about:
                author_message = f"""
Built using {{a=https://github.com/phroun/adventure-for-renpy}}Adventure for Ren'Py{{/a}} v{ADVENTURE_VERSION_MAJOR}.{ADVENTURE_VERSION_MINOR}.{ADVENTURE_VERSION_REVISION} (MIT Licensed)
by Jeffrey R. Day ({{a=https://ko-fi.com/F2F61JR2B4}}Donate to Support{{/a}})"""
                if gui.about.strip() != "":
                    gui.about += f"\n"
                if gui.about == None:
                    gui.about = ""
                gui.about += author_message
                if renpy.get_screen("about"):
                    renpy.restart_interaction()
                renpy.restart_interaction()
            # </if>
        except:
            pass
        # </try>
    # </def>    

    # <def>
    def adventure_tooltip():
        return GetTooltip() or (None if adventure.last_hint == None else adventure_capitalize_first_letter(adventure.last_hint))
    # </def>

    # <def>
    def adventure_extract_tag(tag_name, text):
        """
        Extract custom tag from text.
        Returns:
        - False: tag not present
        - True: tag exists but has no value (e.g., {custom})
        - string: tag value (e.g., {custom=box} returns "box")
        """
        
        # Pattern for tag with value: {custom=value}
        value_pattern = r'\{' + tag_name + r'=([^}]+)\}'
        # Pattern for tag without value: {custom}
        no_value_pattern = r'\{' + tag_name + r'\}'
        
        # Check for tag with value first
        value_match = re.search(value_pattern, text)
        # <if>
        if value_match:
            return value_match.group(1)
        # </if>
        
        # Check for tag without value
        # <if>
        if re.search(no_value_pattern, text):
            return True
        # </if>
        
        # Tag not present
        return False
    # </def>
    
    # Register tag as invisible in text display
    config.custom_text_tags["prompt"] = lambda tag, argument, contents: contents
    config.custom_text_tags["event"] = lambda tag, argument, contents: contents
    config.custom_text_tags["cancel"] = lambda tag, argument, contents: contents
    config.custom_text_tags["done"] = lambda tag, argument, contents: contents
    config.custom_text_tags["disabled"] = lambda tag, argument, contents: contents

    adventure.old_context_callback = config.context_callback
    config.context_callback = adventure_fix_message
# </init>

# <init>
init 999 python:  # Very late in the init process
    ADVENTURE_NARRATOR = DynamicCharacter("adventure.narratorName")
    # <if>
    if renpy.has_screen("about"):
        adventure_fix_message()
    # </if>
# </init>

# <screen>
screen adventure_toolbar():
    # <if>
    if adventure.toolbar_position in ["top", "bottom", "left", "right"]:
        python:
            tbiconbase = adventure.toolbar_icons_base + "/" + adventure.toolbar_iconset
            if not adventure_cached_exists(tbiconbase + "/toolbar-inactive.png"):
                tbiconbase = "adventure/images/" + adventure.toolbar_iconset
            if tbiconbase in adventure.plugin_metrics:
                metrics = adventure.plugin_metrics[tbiconbase]
            else:
                metrics = {}
            if not "toolbar_top_padding" in metrics:
                metrics["toolbar_top_padding"] = 0
            if not "toolbar_left_padding" in metrics:
                metrics["toolbar_left_padding"] = 0
            if not "toolbar_right_padding" in metrics:
                metrics["toolbar_right_padding"] = 0
            if not "toolbar_bottom_padding" in metrics:
                metrics["toolbar_bottom_padding"] = 0
            if not "toolbar_vertical_spacing" in metrics:
                metrics["toolbar_vertical_spacing"] = 0
            if not "toolbar_horizontal_spacing" in metrics:
                metrics["toolbar_horizontal_spacing"] = 0
            if not "toolbar_active_icon_offset" in metrics:
                metrics["toolbar_active_icon_offset"] = (0, 0)
            if not "toolbar_inactive_icon_offset" in metrics:
                metrics["toolbar_inactive_icon_offset"] = (0, 0)
            if not "toolbar_active_button_offset" in metrics:
                metrics["toolbar_active_button_offset"] = (0, 0)
            if not "toolbar_inactive_button_offset" in metrics:
                metrics["toolbar_inactive_button_offset"] = (0, 0)
            if not "toolbar_draw_order_vertical_reversed" in metrics:
                metrics["toolbar_draw_order_vertical_reversed"] = False
            if not "toolbar_draw_order_horizontal_reversed" in metrics:
                metrics["toolbar_draw_order_horizontal_reversed"] = False

            order_reversed = False
            vertical_padding = (metrics["toolbar_top_padding"] + metrics["toolbar_bottom_padding"]);
            horizontal_padding = (metrics["toolbar_left_padding"] + metrics["toolbar_right_padding"]);
            vertical = adventure.toolbar_position in ["right", "left"]
            # <if>
            if vertical:
                length_padding = vertical_padding
                depth_padding = horizontal_padding
                order_reversed = metrics["toolbar_draw_order_vertical_reversed"] == True
            else:
                length_padding = horizontal_padding
                depth_padding = vertical_padding
                order_reversed = metrics["toolbar_draw_order_horizontal_reversed"] == True
            # </if>
            toolbar_length = int(length_padding * adventure.toolbar_iconzoom/0.1)
            toolbar_depth_pad = int(depth_padding * adventure.toolbar_iconzoom/0.1)
            toolbar_left_pad = int(metrics["toolbar_left_padding"] * adventure.toolbar_iconzoom / 0.1)
            toolbar_top_pad = int(metrics["toolbar_top_padding"] * adventure.toolbar_iconzoom / 0.1)
            valid_icons = []
            # <try>
            try:
                icon_width = adventure.toolbar_iconzoom * adventure.iconSizes[
                        adventure_toolbar_icon("toolbar-inactive.png")
                    ][0]
                icon_height = adventure.toolbar_iconzoom * adventure.iconSizes[
                        adventure_toolbar_icon("toolbar-inactive.png")
                    ][1]
            except:
                # Fallbacks just to prevent crash
                icon_width = 20
                icon_height = 20
            # </try>
            icon_length = icon_height if vertical else icon_width
            icon_depth = icon_width if vertical else icon_height
            toolbar_spacing = (metrics["toolbar_vertical_spacing"] if vertical else metrics["toolbar_horizontal_spacing"]) * (adventure.toolbar_iconzoom/0.1)
            # <for>
            for icon in adventure.toolbar_icons:
                # <if>
                if icon in adventure.tool_icons:
                    if len(valid_icons):
                        toolbar_length += toolbar_spacing
                    valid_icons.append(icon)
                    toolbar_length += icon_length
                else:
                    pass
                # </if>
            # </for>

            toolbar_flip = 1
            toolbar_base = 0
            # <if>
            if adventure.toolbar_position == "bottom" or adventure.toolbar_position == "right":
                toolbar_flip = -1
                toolbar_base = 1
            # </if>

            # <if>
            if vertical:
                toolbar_max_length = config.screen_height - adventure.toolbar_margin_start - adventure.toolbar_margin_end
                toolbar_width = int(icon_depth) + toolbar_depth_pad
                toolbar_height = int(toolbar_length)
                toolbar_anchor_indent = (toolbar_max_length - toolbar_length) * adventure.toolbar_anchor
                toolbar_x = int(
                    + toolbar_base * config.screen_width # far edge
                    + toolbar_flip * (adventure.toolbar_margin_edge + toolbar_base*toolbar_width) # optional -depth
                )
                toolbar_y = int(
                    + adventure.toolbar_margin_start # or margin
                    + toolbar_anchor_indent # plus indent
                )
                # where we begin drawing icons in drawing order
                toolbar_start_x = toolbar_x + toolbar_left_pad
                toolbar_start_y = toolbar_y + toolbar_top_pad
                # <if>
                if metrics["toolbar_draw_order_vertical_reversed"]:
                    toolbar_start_y += toolbar_length - icon_length - length_padding
                # </if>
                toolbar_inc_x = 0
                toolbar_inc_y = icon_length + toolbar_spacing
            else:
                toolbar_max_length = config.screen_width - adventure.toolbar_margin_start - adventure.toolbar_margin_end
                toolbar_width = int(toolbar_length)
                toolbar_height = int(icon_depth) + toolbar_depth_pad
                toolbar_anchor_indent = (toolbar_max_length - toolbar_length) * adventure.toolbar_anchor
                toolbar_y = int(
                    + toolbar_base * config.screen_height # far edge
                    + toolbar_flip * (adventure.toolbar_margin_edge + toolbar_base*toolbar_height) # optional -depth
                )
                toolbar_x = int(
                    + adventure.toolbar_margin_start # or margin
                    + toolbar_anchor_indent # plus indent
                )
                toolbar_start_x = toolbar_x + toolbar_left_pad
                toolbar_start_y = toolbar_y + toolbar_top_pad
                # <if>
                if metrics["toolbar_draw_order_horizontal_reversed"]:
                    toolbar_start_x += toolbar_length - icon_length - length_padding
                # </if>
                toolbar_inc_x = icon_length + toolbar_spacing
                toolbar_inc_y = 0
            # </if>

            this_x = toolbar_start_x
            this_y = toolbar_start_y
        # </python>

        # <frame>
        frame:
            background Transform(AdventureNineSliceFrame((adventure_toolbar_icon("toolbar-bg.png")), bgzoom = adventure.toolbar_iconzoom), alpha=adventure.toolbar_bg_opacity)
            xpos int(toolbar_x - 1)
            ypos int(toolbar_y - 1)
            xsize int(toolbar_width)
            ysize int(toolbar_height)
        # </frame>

        # <for>
        for icon in (reversed(valid_icons) if order_reversed else valid_icons):
            # <python>
            python:
                status = "active" if icon == adventure.active_tool else "inactive"
            # </python>
            add (adventure_toolbar_icon("toolbar-" + status + ".png")):
                xpos int(this_x + metrics["toolbar_" + status + "_button_offset"][0] * adventure.toolbar_iconzoom / 0.1)
                ypos int(this_y + metrics["toolbar_" + status + "_button_offset"][1] * adventure.toolbar_iconzoom / 0.1)
                xanchor 1
                yanchor 1
                zoom adventure.toolbar_iconzoom
            add (adventure_toolbar_icon(adventure.tool_icons[icon])):
                xpos int(this_x + metrics["toolbar_" + status + "_icon_offset"][0] * adventure.toolbar_iconzoom/0.1 + icon_width / 2)
                ypos int(this_y + metrics["toolbar_" + status + "_icon_offset"][1] * adventure.toolbar_iconzoom/0.1 + icon_height / 2)
                zoom adventure.toolbar_iconzoom
                xanchor 0.5
                yanchor 0.5
                # fit "contain"
                # xsize int(icon_width)
                # ysize int(icon_height)
            button:
                xpos int(this_x)
                ypos int(this_y)
                xsize int(icon_width)
                ysize int(icon_height)
                background None
                tooltip adventure.toolbar_hints[icon]
                action Function(adventure_set_tool, icon)
            # <python>
            python:
                # <if>
                if order_reversed: 
                    this_x -= toolbar_inc_x
                    this_y -= toolbar_inc_y
                else:
                    this_x += toolbar_inc_x
                    this_y += toolbar_inc_y
                # </if>
            # </python>
        # </for>

    # </if valid toolbar position>
# </screen>

# <screen>
screen adventure_editor():
    pass
# </screen adventire_editor>

# <screen>
screen adventure_underlay():
    pass
# </screen adventure_underlay>

# <screen>
screen adventure_tooltip():
    # <if>
    if adventure_tooltip():
        # <frame>
        frame:
            background Solid("#000000", alpha=adventure.tooltip_bg_opacity)
            xalign adventure.tooltip_xpos
            ypos adventure.tooltip_ypos
            padding (20, 10)
            # <text>
            text adventure_tooltip():
                size adventure.tooltip_size
                color "#ffffff"
                bold True
                text_align 0.5
            # </text>
        # </frame>
    # </if>
# </screen>

# <screen>
screen adventure_overlay():
    use adventure_toolbar
    use adventure_tooltip
    pass
# </screen adventure_overlay>

# <screen>
screen adventure_interaction():

    # <if>
    if adventure.screen_should_exit and adventure.modalFreeze == 0 and adventure._temp_return:
        $ adventure.screen_should_exit = False  # Reset flag
        $ adventure.actual_return = adventure._temp_return if hasattr(adventure, '_temp_return') else None
        $ adventure.result = adventure.actual_return
        $ adventure._temp_return = None
        $ Return(adventure.actual_return)
        timer 0.01 action Return(adventure.actual_return)
    # </if _temp_return and no modalFreeze>

    use adventure_underlay
    $ adventure.screen_icons = []
    $ atool = adventure.active_tool if adventure.visibleMode == "default" else adventure.visibleMode
    $ tools = [atool]
    python:
        # <if>
        if atool in adventure.tool_verbs:
            toolset = adventure.tool_verbs[atool]
            # <for>
            for tool in toolset:
                # <if>
                if tool.startswith('*'):
                    tools.append(tool[1:])
                # </if>
            # </for>
        # </if>
    # <for>
    for interactableId, interactable in enumerate(adventure.room):
        # <if>
        if interactable["type"] == "icon":
            $ this_active = adventure_check_condition(interactable["condition"])
            $ icons_found = []
            $ icon_verbs = []
            $ icon_verb_images = []
            $ icon_verb_ids = []
            # <for>
            for point in interactable["points"]:
                $ x, y = point
                $ xoffs = 0
                # <for>
                for tool in tools:
                    # <if>
                    if tool in interactable and tool in adventure.verb_icons:
                        $ iconname = interactable[tool]
                        # <if>
                        if not iconname.startswith("/") and not iconname in icons_found:
                            # <if>
                            if iconname in adventure.verb_icons[tool]:
                                # <python>
                                python:
                                    icons_found.append(iconname)
                                    icon_verb_images.append(adventure.verb_icons[tool][iconname][0])
                                    icon_verbs.append(adventure.verb_icons[tool][iconname][1])
                                    icon_verb_ids.append(interactableId)
                                # </python>
                            # </if>
                        # </if not commented and not already in list>
                    # </if in the data record>
                # </for>
                # <python>
                python:
                    total_width = 0
                    # <for>
                    for verbimage in reversed(icon_verb_images):
                        this_width = adventure.iconSizes[adventure_icon(verbimage)][0] * adventure.iconzoom
                        total_width += this_width if this_width != None else 20
                    # </for>
                    total_width += (len(icon_verb_images) - 1) * adventure.icon_padding
                    xoffs -= total_width // 2
                # </python>
                # <for>
                for i in range(len(icon_verb_images) - 1, -1, -1):
                    $ verbimage = icon_verb_images[i]
                    $ this_verb = icon_verbs[i]
                    $ this_id = icon_verb_ids[i]
                    # <if>
                    if this_active or adventure.debug_show_inactive:
                        python:
                            real_icon_name = adventure_icon(verbimage)
                        # <if>
                        if adventure.hover_icon == (interactableId, this_verb):
                            $ adventure.last_hover_icon = adventure.hover_icon
                            $ hwidth = adventure.iconSizes[adventure_icon("hover-glow.png")][0] * adventure.iconzoom
                            # <add>
                            add (adventure_icon("hover-glow.png")):
                                xpos int(x - (hwidth // 2))
                                ypos y
                                xanchor 0
                                yanchor 0.5
                                zoom (adventure.iconzoom)
                            # </add>
                        # </if>
                        # <add>
                        add (real_icon_name):
                            xpos int(x + xoffs)
                            ypos y
                            xanchor 0
                            yanchor 0.5
                            alpha (1 if this_active else 0.3)
                            zoom (adventure.iconzoom)
                        # </add>
                    # </if>
                    # <python>
                    python:
                        this_size_raw = adventure.iconSizes[adventure_icon(verbimage)]
                        this_size = (
                            (this_size_raw[0] * adventure.iconzoom) if this_size_raw[0] != None else 20,
                            (this_size_raw[1] * adventure.iconzoom) if this_size_raw[1] != None else 20
                        )
                        
                        adventure.screen_icons.append({
                            "interactableId": this_id,
                            "active": this_active,
                            "verb": this_verb,
                            "tag": interactable["tag"],
                            "position": (int(x + xoffs + (this_size[0]//2)), y),
                            "size": this_size
                        })
                        xoffs += this_size[0] + adventure.icon_padding
                    # </python>
                # </for>
            # </for>
        # </if icon>
    # </for interactables>
    add adventure.mouse_position
    use adventure_editor
    use adventure_overlay
# </screen adventure_interaction>

# <label>
label adventure_input(room):
    # <python>
    python:
        adventure.roomName = room
        adventure.matched_action = False
        # <if>
        if adventure.action_tip:
            adventure.action_collector = not adventure.action_collector
            # <if>
            if adventure.action_collector:
                adventure.actions = []
                renpy.return_statement(adventure.result);
            # </if>
        # </if>
        adventure_init()
        if not adventure.roomName in roomData:
            roomData[adventure.roomName] = []
        adventure.room = roomData[adventure.roomName]
        adventure.screen_should_exit = False
        adventure.result = ""
    # </python>

    call screen adventure_interaction

    # <python>
    python:
        adventure.result = _return
        # <if>
        if adventure.result == "":
            renpy.jump("adventure_input")
        else:
            renpy.return_statement(adventure.result);
        # </if>
    # </python>
# </label>

# <screen>
# Adventure Icon Prompt Screen
screen adventure_icon_prompt(question, icon_options, iconpadding=20, labelpadding=20, labelheight=30, iconwidth=None, iconheight=None):
    if not iconwidth:
        $ iconwidth = 128
    if not iconheight:
        $ iconheight = iconwidth
    if not iconpadding:
        $ iconpadding = 42
    if not labelheight:
        $ labelheight = 30
    if not labelpadding:
        $ labelpadding = 20
    # Semi-transparent background
    add "#000000" alpha 0.8
    
    # Main container
    # <frame>
    frame:
        background AdventureNineSliceFrame(adventure.confirm_frame, matrixcolor=AdventureThemeColorizeMatrix(gui.accent_color), bgzoom=0.6)
        xalign 0.5
        yalign 0.5
        xpadding 40
        ypadding 30
        
        # <vbox>
        vbox:
            spacing 20
            xalign 0.5
            
            # Title
            text question style "confirm_prompt" xalign 0.5
            null height 5
            # Icon grid
            # <hbox>
            hbox:
                spacing 0
                xalign 0.5
                
                # <for>
                for i, (icon_file, icon_label) in enumerate(icon_options):
                    # Container for each icon option
                    # <fixed>
                    fixed:
                        xsize (iconwidth + iconpadding + labelpadding)
                        ysize (iconheight + 10 + labelheight)
                        xalign 0.5
                        
                        # Content vbox (non-interactive)
                        # <vbox>
                        vbox:
                            spacing 10
                            xalign 0.5
                            yalign 0.5
                            xsize (iconwidth + iconpadding)
                            ysize (iconheight)
                            
                            null height 20
                            
                            $ icon_image = Image(icon_file)
                            if icon_image is not None:
                                add Transform(icon_image, size=(iconwidth, iconheight)) xalign 0.5
                            else:
                                # Fallback if image can't be loaded
                                frame:
                                    xsize iconwidth
                                    ysize iconheight
                                    xalign 0.5
                                    background "#333333"
                                    text "Icon {}".format(i+1):
                                        xalign 0.5
                                        yalign 0.5
                            
                            frame:
                                background None
                                xpadding labelpadding
                                xalign 0.5
                                xsize iconwidth + iconpadding
                                # Label text
                                text icon_label:
                                    style "confirm_prompt"
                                    xalign 0.5
                                    text_align 0.5
                                    size 18
                                    xsize (iconwidth + iconpadding)
                                # </text>
                            # </frame>
                            null height 20
                        # </vbox>
                        # Transparent overlay button
                        # <button>
                        button:
                            xsize (iconwidth + iconpadding + labelpadding)
                            ysize (iconheight + labelheight + 50)
                            background None  # Completely transparent
                            hover_background Frame(Solid("#ffffff22"), 2, 2, 2, 2)  # Light border on hover
                            action Return(i)
                            xalign 0.5
                            yalign 0.5
                        # </button>
                    # </fixed>
                # <for>
                
            # </hbox>
            
            null height 5
        # </vbox>
    # </frame>
# </screen>

# <label>
label adventure_icon_prompt(question, icon_options, iconpadding=None,
    labelheight=None, labelpadding=None, iconwidth=None, iconheight=None
):
    # Validate input
    if not icon_options:
        "No icon options provided!"
        return -1

    # Show the selection screen
    call screen adventure_icon_prompt(question, icon_options,
        iconpadding=iconpadding,
        labelpadding=labelpadding,
        labelheight=labelheight,
        iconwidth=iconwidth,
        iconheight=iconheight
    )
    
    # Return the selected index
    return _return
# </label>

# <screen>
screen adventure_alert_box(message, ok_action):
    # Set the screen to be modal, blocking other interactions.
    modal True
    # The zorder value ensures this screen is drawn on top of others.
    zorder 100 

    # A dark overlay to dim the game's background.
    add "gui/overlay/confirm.png"

    # Use a frame to create a visual box for the alert.
    frame:
        # Center the frame on the screen.
        align (0.5, 0.5)

        # A vertical box to arrange the text and button.
        vbox:
            # Set spacing between elements.
            spacing 20

            frame:
                background None  # Transparent background
                xpadding 20
                ypadding 10
                xalign 0.5
                # Display the message passed to the screen.
                text message:
                    size 24
                    # Align the text to the center.
                    xalign 0.5
                    text_align 0.5
                    xmaximum 800

            # The "OK" button to close the alert.
            textbutton _("OK"):
                # Center the button.
                xalign 0.5
                # The action to take when the button is clicked.
                action ok_action

            null height 10
# </screen>

# <screen>
screen choice(items):
    modal True
    $ geom = adventure.choice_positions[adventure.choice_position]
    # <python>
    python:
        parsed_items = []
        # <for>
        for i in items:
            parsed_items.append({
                "caption": i.caption,
                "action": i.action,
                "icon": "choice"
            })
        # </for>
    # </python>
    
    # <frame>
    frame:
        xpos (geom["xpos"])
        ypos (geom["ypos"])
        xanchor geom["xanchor"]
        yanchor geom["yanchor"]
        xsize int(geom["width"] * config.screen_width)  # Fixed width
        ysize (None if geom["height"] == None else int(geom["height"] * config.screen_height))
        background "#00000066"
        padding (20, 5)
        
        # <vbox>
        vbox:
            xalign 0.5
            spacing 5
            ysize None
            xfill True
            # <for>
            for i in parsed_items:
                $ choice_type = "normal"
                $ prompt = adventure_extract_tag("prompt", i["caption"])
                $ isevent = adventure_extract_tag("event", i["caption"])
                $ iscancel = adventure_extract_tag("cancel", i["caption"])
                # <python>
                python:
                    if isevent:
                        choice_type = "event"
                    elif iscancel:
                        choice_type = "cancel"
                    else:
                        choice_type = "normal"
                # </python>
                # <if>
                if prompt:
                    null height 5
                    text (i["caption"]):
                        size 38
                        color "#ffffff"
                        xalign 0.5
                        xfill True
                        yfill False
                        bold False
                else:
                    python:
                        choice_icon = "adventure/images/choice-" + choice_type + ".png"
                        
                        my_width = int(geom["width"] * config.screen_width) - 50
                        crazy_vbox = AdventureNineSliceFrame(adventure.choice_frame, bgzoom = 0.2, child=VBox(
                            HBox(
                                VBox(HBox(Transform(Image(choice_icon),
                                zoom=0.09, xanchor=0.5, yalign=0.5), ysize=50,
                                xanchor=0, yanchor=0), xpos=-5, xsize=10, yfill=False,
                                yminimum=50, xmaximum=20, xanchor=0),
                                Null(width=30, height=1),
                                VBox(
                                    Null(height=5),
                                    Text(i["caption"], size=24, color="#000000", bold=True, ypos=0.5, yanchor=0.5, yfill=False),
                                    Null(height=5),
                                    yfill=False, xfill=True,
                                    padding=(10,0)
                                ),
                                Null(width=10, height=1),
                                xanchor=0, xmaximum=(my_width - 80),
                                yalign=0.5, yminimum=40,
                                padding=(0,0)
                            ), spacing=0, xanchor=0
                        ))
                        my_height = max(50, int(adventure_measure_height_at_width(crazy_vbox, my_width, 10)))
                        
                    # <button>
                    button:
                        xsize (my_width - 80)
                        ysize my_height
                        padding (0, 0, 0, 0)
                        action i["action"]
                        background AdventureNineSliceFrame(adventure.choice_frame, bgzoom = 1, child=VBox(
                            HBox(
                                VBox(HBox(Transform(Image(choice_icon),
                                zoom=0.09, xanchor=0.5, yalign=0.5), ysize=50,
                                xanchor=0, yanchor=0), xpos=-5, xsize=10, yfill=False,
                                yminimum=50, xmaximum=20, xanchor=0),
                                Null(width=30, height=1),
                                VBox(
                                    Null(height=5),
                                    Text(i["caption"], size=24, color="#000000", bold=True, ypos=0.5, yanchor=0.5, yfill=True),
                                    Null(height=5),
                                    yfill=True, xfill=True,
                                    padding=(10,0)
                                ),
                                Null(width=10, height=1),
                                xanchor=0, xmaximum=(my_width), yfill=False,
                                yalign=0.5, yminimum=40,
                                background="#ff0000",
                                padding=(0,0)
                            ), spacing=0, ysize=(my_height), xanchor=0
                        ))
                        hover_background AdventureNineSliceFrame(adventure.choice_frame_hover, bgzoom = 1, child=VBox(
                            HBox(
                                VBox(HBox(Transform(Image(choice_icon),
                                zoom=0.09, xanchor=0.5, yalign=0.5), ysize=50,
                                xanchor=0, yanchor=0), xpos=-5, xsize=10, yfill=False,
                                yminimum=50, xmaximum=20, xanchor=0),
                                Null(width=30, height=1),
                                VBox(
                                    Null(height=5),
                                    Text(i["caption"], size=24, color="#ffff00", bold=True, ypos=0.5, yanchor=0.5, yfill=True),
                                    Null(height=5),
                                    yfill=True, xfill=True,
                                    padding=(10,0)
                                ),
                                Null(width=10, height=1),
                                xanchor=0, xmaximum=(my_width), yfill=False,
                                yalign=0.5, yminimum=40,
                                padding=(0,0)
                            ), spacing=0, ysize=(my_height), xanchor=0
                        ))
                    # </button>
                    null height 5
                # </if>
                null height 5
            # </for>
        # </vbox>
    # </frame>
# </screen choice>

# <screen>
screen confirm(message, yes_action, no_action):
    modal True
    zorder 200

    # <python>
    python:
        bgz = 0.3
        inversion = 1
        # <if>
        if not adventure_is_dark_theme():
            inversion = 1 - inversion
        # </if>
    # </python>

    # <frame>
    frame:
        background AdventureNineSliceFrame(adventure.confirm_frame, bgzoom = 0.6,
            matrixcolor=AdventureThemeColorizeMatrix(gui.accent_color)
        )

        padding (50, 30)
        xalign 0.5
        yalign 0.5
        
        # <vbox>
        vbox:
            spacing 30
            xalign 0.5
            yalign 0.5
            
            # <text>
            text message:
                style "confirm_prompt"
                xalign 0.5
            # </text>
                
            # Buttons
            # <hbox>
            hbox:
                spacing 50
                xalign 0.5
                yalign 0.5

                # Custom Yes button
                # <button>
                button:
                    action yes_action
                    xysize (100, 60)
                    
                    # Normal state background
                    background Transform(
                        AdventureNineSliceFrame("button", bgzoom=bgz,
                        matrixcolor=AdventureThemeColorizeMatrix(gui.hover_muted_color))
                    )
                    
                    # Hover state background
                    hover_background Transform(
                        AdventureNineSliceFrame("button-hover", bgzoom=bgz,
                        matrixcolor=AdventureThemeColorizeMatrix(gui.accent_color))
                    )
                    
                    # Selected state (if needed)
                    selected_background Transform(
                        AdventureNineSliceFrame("button", bgzoom=bgz,
                        matrixcolor=AdventureThemeColorizeMatrix(gui.selected_color))
                    )
                    
                    # <text>
                    text _("Yes"):
                        xalign 0.5
                        yalign 0.5
                        color gui.interface_text_color
                        hover_color gui.interface_text_color
                        selected_color gui.interface_text_color
                        size 24
                    # </text>
                # </button>

                # Custom Yes button
                # <button>
                button:
                    action no_action
                    xysize (100, 60)
                    
                    # Normal state background
                    background Transform(
                        AdventureNineSliceFrame("button", bgzoom=bgz,
                        matrixcolor=AdventureThemeColorizeMatrix(gui.hover_muted_color))
                    )
                    
                    # Hover state background
                    hover_background Transform(
                        AdventureNineSliceFrame("button-hover", bgzoom=bgz,
                        matrixcolor=AdventureThemeColorizeMatrix(gui.accent_color))
                    )
                    
                    # Selected state (if needed)
                    selected_background Transform(
                        AdventureNineSliceFrame("button-selected", bgzoom=bgz,
                        matrixcolor=AdventureThemeColorizeMatrix(gui.selected_color))
                    )
                    
                    # <text>
                    text _("No"):
                        xalign 0.5
                        yalign 0.5
                        color gui.interface_text_color
                        hover_color gui.interface_text_color
                        selected_color gui.interface_text_color
                        size 24
                    # </text>
                # </button>
            # </hbox>
        # </vbox>
    # </frame>
# </screen confirm>

# <style>
style confirm_prompt:
    size 24
    color ("#FFFFFF" if adventure_is_dark_theme() else "#000000")
# </style>
