"""
**************************************************************************
**
**   adventure.rpy - Adventure Module (for RenPy)
**
**   Version 0.1 revision 9
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
define ADVENTURE_VERSION_MINOR = 1
define ADVENTURE_VERSION_REVISION = 9

default ADVENTURE_LOG = DynamicCharacter(">>>", who_color="#999999", what_color="#999999")

default adventure.do_logging = True
default adventure.first_person = False  # False = You, True = I
default adventure.iconset = "free-icons"
default adventure.iconzoom = 0.05
default adventure.icon_padding = 5
default adventure.active_tool = "auto"
default adventure.toolbar_position = "right"
default adventure.toolbar_iconset = "free-icons"
default adventure.toolbar_iconzoom = 0.1
default adventure.toolbar_anchor = 0
default adventure.toolbar_margin_edge = 10
default adventure.toolbar_margin_start = 5
default adventure.toolbar_margin_end = 5
default adventure.toolbar_icons = ["auto", "ex", "inventory"]
default adventure.toolbar_menu = "touch_only"
default adventure.toolbar_inventory_expand = True # one button per item? False = bag icon
default adventure.toolbar_draw_order_reversed = False

default adventure.tool_icons = {
    "go": "mode-go.png",
    "ex": "mode-examine.png",
    "op": "mode-operate.png",
    "say": "mode-talk.png",
    "auto": "mode-auto.png",
}

default adventure.verb_icons = {  # organized by tool mode
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

default adventure.verb_aliases = {

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

default adventure.tag_aliases = {

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

default adventure.tool_verbs = {

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

default roomData = {}
default adventure.room = []
default adventure.roomName = "demo_room"
default adventure.editing = False
default adventure.modalFreeze = 0
default adventure.mousex = -1
default adventure.mousey = -1
default adventure.editMode = 0
default adventure.visibleMode = "default"
default adventure.interactableId = 0
default adventure.editorPos = 0
default adventure.result = ""
default adventure.lastRoom = "nowhere"
default adventure.screen_should_exit = False
default adventure.targets = []
default adventure.target_x = -1
default adventure.target_y = -1
default adventure._temp_return = ""
default adventure.iconSizes = {}
default adventure.screen_icons = []

# <init>
init python:
    import math
    import pygame
    import renpy.display.render as render
    from renpy.display.core import Displayable
    import math

    build.classify('game/adventure-editor.rpy', None)
    build.classify('game/adventure-editor.rpyc', None)
    build.classify('images/editor-icons/**', None)

    # <class>
    class getMousePosition(renpy.Displayable):

        # <def>
        def __init__(self):
            renpy.Displayable.__init__(self)
        # </def __init__>

        # <def>
        def event(self, ev, x, y, st):
            import pygame
            # <if>
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # <if>
                if ev.button == 1:
                    adventure.mousex = x
                    adventure.mousey = y
                    current_x = adventure.mousex
                    current_y = adventure.mousey
                    # <try>
                    try:
                        current_handled = adventure_editor_mouse(adventure.mousex, adventure.mousey)
                        # if current_handled == True:
                        # Don't consume the event - let it pass through
                        #    raise renpy.IgnoreEvent()
                    except:
                        current_handled = False
                        adventure.editing = False
                    # </try>
                    # <if>
                    if not current_handled and current_x > 0 and current_y > 0 and adventure.modalFreeze == 0:
                        adventure.targets = []
                        # <for>
                        for i in range(len(adventure.room)):
                            if adventure.room[i]["type"] == "polygon" and (len(adventure.room[i]["points"]) > 2):
                                # <if>
                                if adventure_point_in_polygon(adventure.mousex, adventure.mousey, adventure.room[i]["points"]):
                                    adventure.targets.append((i, ""))
                                # </if>
                            # </if polygon with at least 3 points>
                        # </for all polygons in room>
                        # <for>
                        for icon in adventure.screen_icons:
                            if adventure_point_in_icon(current_x, current_y, icon):
                                adventure.targets = [(icon["interactableId"], icon["verb"])]
                            # </if>
                        # </for>
                        adventure.target_x = adventure.mousex
                        adventure.target_y = adventure.mousey
                        adventure._temp_return = "clicked"
                        adventure.screen_should_exit = True
                        renpy.restart_interaction()
                        raise renpy.IgnoreEvent()
                    # </if valid point and not modalFreeze>
                # </if button=1>
            # </if MOUSEBUTTONDOWN>
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
    def adventure_checkEvent():
        # Create text showing the actual coordinates
        coordinates_text = "Mouse: ({}, {})".format(adventure.mousex, adventure.mousey)
        return Text(coordinates_text, color="#FF0000", size=30)
    # </def adventure_checkEvent>

    config.overlay_functions.append(adventure_checkEvent)
    
    # Helper functions for screen-based mouse tracking
    # <def>
    def adventure_update_mouse_pos():
        pos = renpy.get_mouse_pos()
        adventure.mousex = pos[0]
        adventure.mousey = pos[1]
    # </def adventure_update_mouse_pos>

    # <def>    
    def adventure_click_mouse_pos():
        pos = renpy.get_mouse_pos()
        adventure.mousex = pos[0]
        adventure.mousey = pos[1]
        print("Screen click at: ({}, {})".format(pos[0], pos[1]))
    # </def adventure_click_mouse_pos>

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
                dim = adventure_get_image_dimensions(icon_name)
                adventure.iconSizes[icon_name] = dim
            # </for>
        # </for>
    # </def>

    # <def>
    def adventure_init():
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
        
        print("This game is built using \"Adventure for RenPy\" by Jeffrey R. Day:")
        print("A free (MIT Licensed) module to add point-and-click adventure game support to RenPy.")
        print("https://github.com/phroun/adventure-for-renpy")
        print("")
        print("Please consider supporting development of the \"Adventure for RenPy\" module by donating to me on ko-fi:  https://ko-fi.com/jeffday")

        adventure_refresh_icon_dimensions()
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
    def player_chooses_to(command):
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
                                sentences.append((canonical_verb.lower(), noun))
                            # </for>
                        # </for groups>
                    # </if>
                # </if valid tool>
            # <for targets>
        # </for>
        print(sentences)
        matches = []

        # <for>
        for sentence in sentences:
            verb, noun = sentence
            # <if>
            if cmd.endswith(" " + noun.lower()):
                remainder = cmd[:-(len(noun)+1)]
                crem = cmdc[:-(len(noun)+1)]
                canonical_cmd = adventure_canonize_phrase(crem, adventure.verb_aliases)
                # <if>
                if canonical_cmd.lower().startswith(verb):
                    slurry = canonical_cmd[len(verb):]
                    matches.append((verb + slurry + " " + noun, len(noun)))
                # <if>
            # </if ends with noun>
        # </for>

        highest = 0
        bestmatch = ""
        # <for>
        for match, nl in matches:
            # <if>
            if nl > highest:
                highest = nl
                bestmatch = match
            # </if>
        # </for>
        
        # <if>
        if adventure.first_person:
            person = "I "
        else:
            person = "You "
        # </if>
        logtext = "{b}{i}" + person + adventure_escape_renpy(bestmatch) + "{/i}{/b}"
        ADVENTURE_LOG.add_history(kind="adv", what=logtext, who=ADVENTURE_LOG.name)
        return len(matches) != 0
    # </def>
# </init>

# <screen>
screen adventure_editor():
    pass
# </screen adventire_editor>

# <sreen>
screen adventure_underlay():
    pass
# </screen adventure_underlay>

# <sreen>
screen adventure_overlay():
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
                        $ verb = interactable[tool]
                        # <if>
                        if not verb.startswith("/") and not verb in icon_verbs:
                            # <if>
                            if verb in adventure.verb_icons[tool]:
                                # <python>
                                python:
                                    icon_verbs.append(adventure.verb_icons[tool][verb][1])
                                    icon_verb_images.append(adventure.verb_icons[tool][verb][0])
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
                    # <add>
                    add ("images/" + adventure.iconset + "/" + verbimage):
                        xpos int(x + xoffs)
                        ypos y
                        xanchor 0
                        yanchor 0.5
                        zoom (adventure.iconzoom)
                    # </add>
                    # <python>
                    python:
                        this_size_raw = adventure.iconSizes["images/" + adventure.iconset + "/" + verbimage]
                        this_size = (
                            (this_size_raw[0] * adventure.iconzoom) if this_size_raw[0] != "None" else 20,
                            (this_size_raw[1] * adventure.iconzoom) if this_size_raw[1] != "None" else 20
                        )
                        adventure.screen_icons.append({
                            "interactableId": this_id,
                            "verb": this_verb,
                            "tag": interactable["tag"],
                            "position": (int(x + xoffs + (this_size[0]//2)), y),
                            "size": this_size
                        })
                        xoffs += this_size[0] + adventure.icon_padding
                    # </python>
                # </for>
            # </for>
        # </if>
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
