"""
**************************************************************************
**
**   adventure.rpy - Adventure Module (for Ren'Py)
**
**   Version 0.2 revision 4
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
define ADVENTURE_VERSION_REVISION = 4

define ADVENTURE_UNSET = "unset"

# <init>
init -10 python:

    import time
    import math
    import pygame
    import renpy.display.render as render
    from renpy.display.core import Displayable
    import math

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

    adventure.do_logging = True
    adventure.first_person = False  # False = You, True = I
    adventure.narratorName = ""

    adventure.tooltip_xpos = 0.5
    adventure.tooltip_ypos = 20
    adventure.tooltip_size = 18
    adventure.tooltip_bg_opacity = 0.5
    adventure.action_tip = True

    adventure.iconset = "free-icons"
    adventure.iconzoom = 0.1
    adventure.icon_padding = 5

    adventure.toolbar_position = "bottom"
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
    adventure.toolbar_draw_order_reversed = False

    adventure.toolbar_hints = {

        # These are the tooltips for the toolbar icons:

        "go": "Go (Walk, Travel)",
        "ex": "Examine (Look, Listen, etc.)",
        "op": "Use",
        "say": "Talk",
        "auto": "Action",
    }

    adventure.tool_icons = {

        # These are the image filename associated with each verb mode tool:

        "go": "mode-go.png",
        "ex": "mode-examine.png",
        "op": "mode-operate.png",
        "say": "mode-talk.png",
        "auto": "mode-auto.png",
    }

    adventure.verb_icons = {  # organized by tool mode

        # These are the image filenames and verb(s) associated with
        # each overlay icon:

        "go": {
            "go": ("verb-go.png", "*go")
        },
        "ex": {
            "ex": ("verb-hint.png", "*ex"),
            "taste": ("verb-taste.png", "taste;lick"),
            "look": ("verb-look.png", "look"),
            "read": ("verb-read.png", "read")
        },
        "op": {
            "op": ("verb-hint.png", "*op"),
            "hit": ("verb-hit.png", "hit"),
            "eat": ("verb-eat.png", "eat"),
            "wait": ("verb-wait.png", "wait"),
            "taste": ("verb-taste.png", "taste;lick"),
            "read": ("verb-read.png", "read")
        },
        "say": {
            "speak": ("verb-speak.png", "*say")
        }
    }

    adventure.verb_aliases = {

        # The parser will extract the fullest possible tag from the right
        # end of the command string first, then will replace these words
        # (left side of list below) in the remaining verb part to the
        # canonical form (right side) before performing verb matching:
        
        "climb": "go",
        "move": "go",
        "walk": "go",
        "op": "operate",
        "ex": "examine"
    }

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
          "Elevator": "Lift",
          "Lift": "Elevator",
          "armor": "armour"
        }

    }

    adventure.tool_verbs = {

        # A click with each of these tools will register as
        # any or all of the verbs listed here:

        "go": [
             "go", "go through",
             "enter", "go in", "go into",
             "exit", "go out", "go out of",
             "go across",
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
    adventure.visibleMode = "   "
    adventure.interactableId = 0
    adventure.editorPos = 0
    adventure.result = ""
    adventure.lastRoom = "nowhere"
    adventure.screen_should_exit = False
    adventure.targets = []
    adventure.considered_targets = []
    adventure.target_x = -1
    adventure.target_y = -1
    adventure._temp_return = ""
    adventure.iconSizes = {}
    adventure.screen_icons = []
    adventure.debug_show_inactive = False
    adventure.active_tool = "auto"
    adventure.last_target_stamp = 0
    adventure.last_targets = []
    adventure.last_hint = None
    adventure.gathering_hints = False
    adventure.actions = []

    build.classify('game/adventure/adventure-editor.rpy', None)
    build.classify('game/adventure/adventure-editor.rpyc', None)
    build.classify('game/adventure/images/editor-icons/**', None)

    # <def>
    def adventure_custom_link(target):
        webbrowser.open(target)
    # </def>

    #  config.hyperlink_handlers['advlink'] = adventure_custom_link

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
    class getMousePosition(renpy.Displayable):

        # <def>
        def __init__(self):
            renpy.Displayable.__init__(self)
        # </def __init__>

        # <def>
        def event(self, ev, x, y, st):
            import pygame
            need_res = False
            # <if>
            this_stamp = time.time()
            waited = abs(this_stamp - adventure.last_target_stamp) > 0.1
            if (ev.type == pygame.MOUSEMOTION and waited) or ev.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
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
                        if (
                            adventure.room[i]["type"] == "polygon"
                            and (len(adventure.room[i]["points"]) > 2)
                            and adventure_check_condition(adventure.room[i]["condition"])
                        ):
                            # <if>
                            if adventure_point_in_polygon(adventure.mousex, adventure.mousey, adventure.room[i]["points"]):
                                adventure.targets.append((i, ""))
                            # </if>
                        # </if polygon with at least 3 points>
                    # </for all polygons in room>
                    # <for>
                    for icon in adventure.screen_icons:
                        if icon["active"] and adventure_point_in_icon(current_x, current_y, icon):
                            adventure.targets = [(icon["interactableId"], icon["verb"])]
                        # </if>
                    # </for>
                    # <if>
                    if clicking and ev.button == 1:
                        adventure.considered_targets = adventure.targets
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
                            print(act)
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
    # </class>

    # Initialize the mouse position variables
    store.mousePosition = getMousePosition()
    
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
                icon_name = "images/" + adventure.iconset + "/" + adventure.verb_icons[tool][verb][0]
                adventure.iconSizes[icon_name] = adventure_get_image_dimensions(icon_name)
            # </for>
        # </for>
        icon_name = "images/" + adventure.toolbar_iconset + "/toolbar-active.png"
        adventure.iconSizes[icon_name] = adventure_get_image_dimensions(icon_name)
        icon_name = "images/" + adventure.toolbar_iconset + "/toolbar-inactive.png"
        adventure.iconSizes[icon_name] = adventure_get_image_dimensions(icon_name)
    # </def>

    # <def>
    def adventure_init():
        # <if>
        if not adventure.initialized:
            # <if>
            if adventure.do_logging:
                gui.history_allow_tags.update({"b", "i"})
            # </lif>
            # <try>
            try:
                store.roomData.update(room_definitions)
            except:
                print("No room data loaded")
            # </try>

            author_message_1 = """
This game is built using \"Adventure for Ren'Py\" by Jeffrey R. Day:
A free (MIT Licensed) module to add point-and-click adventure game support to RenPy.
https://github.com/phroun/adventure-for-renpy

Please consider supporting development of the \"Adventure for Ren'Py\" module by donating to me on ko-fi:
https://ko-fi.com/jeffday
            """
            print(author_message_1)
            adventure_refresh_icon_dimensions()
            adventure.initialized = True
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
    def player_chooses_to(command, read_as = None):
        # <if>
        if adventure.action_collector:
            adventure.actions.append(command)
            print("gathering", adventure.actions)
            return False
        # </if>
        cmd_words = command.split()
        cmdc = " ".join(cmd_words)
        cmd = cmdc.lower()
        sentences = []
        # <for>
        for tool in adventure.tool_verbs:
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
                            if inter_verb.startswith('*'):
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
        print(cmd, " -vs- ", sentences)
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
        return GetTooltip() or None if adventure.last_hint == None else adventure_capitalize_first_letter(adventure.last_hint)
    # </def>

    adventure.old_context_callback = config.context_callback
    config.context_callback = adventure_fix_message
# </init>

# <init>
init 1500 python:  # Very late in the init process
    ADVENTURE_NARRATOR = DynamicCharacter("adventure.narratorName")
    # <if>
    if renpy.has_screen("about"):
        adventure_fix_message()
    # </if>
# </init>

# <screen>
screen adventure_toolbar():

    python:
        toolbar_length = 10
        valid_icons = []
        vertical = adventure.toolbar_position in ["right", "left"]
        icon_width = adventure.toolbar_iconzoom * adventure.iconSizes[
                "images/" + adventure.toolbar_iconset + "/toolbar-inactive.png"
            ][0]
        icon_height = adventure.toolbar_iconzoom * adventure.iconSizes[
                "images/" + adventure.toolbar_iconset + "/toolbar-inactive.png"
            ][1]
        icon_length = icon_height if vertical else icon_width
        icon_depth = icon_width if vertical else icon_height
        # <for>
        for icon in adventure.toolbar_icons:
            # <if>
            if icon in adventure.tool_icons:
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
            toolbar_width = int(icon_depth + 10)
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
            toolbar_start_x = toolbar_x + 5
            toolbar_start_y = toolbar_y + 5
            toolbar_inc_x = 0
            toolbar_inc_y = icon_depth
        else:
            toolbar_max_length = config.screen_width - adventure.toolbar_margin_start - adventure.toolbar_margin_end
            toolbar_width = int(toolbar_length)
            toolbar_height = int(icon_depth + 10)
            toolbar_anchor_indent = (toolbar_max_length - toolbar_length) * adventure.toolbar_anchor
            toolbar_y = int(
                + toolbar_base * config.screen_height # far edge
                + toolbar_flip * (adventure.toolbar_margin_edge + toolbar_base*toolbar_height) # optional -depth
            )
            toolbar_x = int(
                + adventure.toolbar_margin_start # or margin
                + toolbar_anchor_indent # plus indent
            )
            toolbar_start_x = toolbar_x + 5
            toolbar_start_y = toolbar_y + 5
            toolbar_inc_x = icon_depth
            toolbar_inc_y = 0
        # </if>

        this_x = toolbar_start_x
        this_y = toolbar_start_y
    # </python>

    # <add>
    
    add ("images/" + adventure.toolbar_iconset + "/toolbar-bg.png"):
        fit "fill"
        xpos toolbar_x
        ypos toolbar_y
        xsize toolbar_width
        ysize toolbar_height
        alpha adventure.toolbar_bg_opacity
    # </add>

    # <for>
    for icon in valid_icons:
        # <python>
        python:
            status = "active" if icon == adventure.active_tool else "inactive"
        # </python>
        add ("images/" + adventure.toolbar_iconset + "/toolbar-" + status + ".png"):
            xpos int(this_x)
            ypos int(this_y)
            fit "fill"
            xsize int(icon_width)
            ysize int(icon_height)
        add ("images/" + adventure.toolbar_iconset + "/" + adventure.tool_icons[icon]):
            xpos int(this_x + icon_width // 2)
            ypos int(this_y + icon_height // 2)
            fit "fill"
            zoom adventure.toolbar_iconzoom
            xanchor 0.5
            yanchor 0.5
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
            this_x += toolbar_inc_x
            this_y += toolbar_inc_y
        # </python>
    # </for>

#    adventure.toolbar_draw_order_reversed = False
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
                if tool.startswith("*"):
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
                        this_width = adventure.iconSizes["images/" + adventure.iconset + "/" + verbimage][0] * adventure.iconzoom
                        total_width += this_width if this_width != "None" else 20
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
                        # <add>
                        add ("images/" + adventure.iconset + "/" + verbimage):
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
                        this_size_raw = adventure.iconSizes["images/" + adventure.iconset + "/" + verbimage]
                        this_size = (
                            (this_size_raw[0] * adventure.iconzoom) if this_size_raw[0] != "None" else 20,
                            (this_size_raw[1] * adventure.iconzoom) if this_size_raw[1] != "None" else 20
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
    add mousePosition
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
screen choice(items):
    modal True
    
    # Black semi-transparent background
    add "#000000" alpha 0.3
    
    # Choice container at bottom
    # <frame>
    frame:
        xalign 0.5
        ypos 0.8  # Fixed position from top
        xsize 800  # Fixed width
        
        # <vbox>
        vbox:
            spacing 15
            # <for>
            for i in items:
                # <textbutton>
                textbutton i.caption:
                    action i.action
                    hover_sound "audio/hover.ogg"  # if you have hover sounds
                    xfill True
                # </textbutton>
            # </for>
        # </vbox>
    # </frame>
# </screen choice>


# <style>
style choice_vbox:
    xalign 0.5
    spacing 10
# </style choice_vbox>

# <style>
style choice_button:
    xminimum 400  # Minimum button width
    xalign 0.5
# </style choice_button>

# <style>
style choice_button_text:
    xalign 0.5
    color "#ffffff"
    hover_color "#ffff00"  # Yellow on hover
    size 24
# </style choice_button_text>
