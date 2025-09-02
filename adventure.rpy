"""
**************************************************************************
**
**   adventure.rpy - Adventure Module (for RenPy)
**
**   Version 0.1 revision 6
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
define ADVENTURE_VERSION_REVISION = 6

default adventure.iconset = "free-icons"
default adventure.iconzoom = 0.05
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
        "go": "verb-go.png",
    },
    "ex": {
        "ex": "verb-hint.png",
        "taste": "verb-taste.png",
        "look": "verb-look.png",
        "read": "verb-read.png",
    },
    "op": {
        "op": "verb-hint.png",
        "hit": "verb-hit.png",
        "eat": "verb-eat.png",
        "wait": "verb-wait.png",
        "taste": "verb-taste.png",
    },
    "say": {
        "speak": "verb-speak.png",
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
      "lift": "elevator",
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
         "*go", "*op", ".*ex"
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
default adventure.interactableId = 0
default adventure.editorPos = 0
default adventure.result = ""
default adventure.lastRoom = "nowhere"
default adventure.screen_should_exit = False
default adventure._temp_return = ""

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
                        targ = []
                        # <for>
                        for i in range(len(adventure.room)):
                            # <if>
                            if (len(adventure.room[i]["points"]) > 2):
                                # <if>
                                if point_in_polygon(adventure.mousex, adventure.mousey, adventure.room[i]["points"]):
                                    # <if>
                                    if adventure.room[i]["tag"] != "":
                                        targ.append(adventure.room[i]["tag"])
                                    else:
                                        targ.append("Poly " + str(i))
                                    # </if>
                                # </if>
                            # </if at least 3 points>
                        # </for all polygons in room>
                        # <if>
                        if len(targ) > 0:
                            adventure._temp_return = "*" + "*".join(targ) + "*"
                            adventure.screen_should_exit = True
                        else:
                            adventure._temp_return = "(" + str(adventure.mousex) + "," + str(adventure.mousey) + ")"
                            adventure.screen_should_exit = True
                        # </if>
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
    def point_in_polygon(x, y, points):
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
    # </def point_in_polygon>

    # <def>
    def checkEvent():
        # Create text showing the actual coordinates
        coordinates_text = "Mouse: ({}, {})".format(adventure.mousex, adventure.mousey)
        return Text(coordinates_text, color="#FF0000", size=30)
    # </def checkEvent>

    config.overlay_functions.append(checkEvent)
    
    # Helper functions for screen-based mouse tracking
    # <def>
    def update_mouse_pos():
        pos = renpy.get_mouse_pos()
        adventure.mousex = pos[0]
        adventure.mousey = pos[1]
    # </def update_mouse_pos>

    # <def>    
    def click_mouse_pos():
        pos = renpy.get_mouse_pos()
        adventure.mousex = pos[0]
        adventure.mousey = pos[1]
        print("Screen click at: ({}, {})".format(pos[0], pos[1]))
    # </def click_mouse_pos>

    # <def>
    def adventure_init():
        try:
            store.roomData.update(room_definitions)
        except:
            print("No room data loaded")
    # </def adventure_init>
    
    # <def>
    def player_chooses_to(command) {
        # gather noun list, match longest noun with given command
        # canonize verb words
        # gather verb list, match longest verb with given command
        # return result
    }
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
