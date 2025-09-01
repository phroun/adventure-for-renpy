"""
**************************************************************************
**
**   adventure.rpy - Adventure Module (for RenPy)
**
**   Version 0.1 revision 2
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
define ADVENTURE_VERSION_REVISION = 2

default roomData = {}
default adventure.room = []
default adventure.roomName = "demo_room"
default adventure.editing = False
default adventure.modalFreeze = 0
default adventure.mousex = -1
default adventure.mousey = -1
default adventure.editMode = 0
default adventure.polyId = 0
default adventure.editorPos = 0
default adventure.result = ""
default adventure.lastRoom = "nowhere"
default adventure.screen_should_exit = False
default adventure._temp_return = ""
    
init python:
    import math
    import pygame
    import renpy.display.render as render
    from renpy.display.core import Displayable
    import math

    build.classify('game/adventure-editor.rpy', None)

    # <class>
    class getMousePosition(renpy.Displayable):

        def __init__(self):
            renpy.Displayable.__init__(self)

        def event(self, ev, x, y, st):
            import pygame

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    adventure.mousex = x
                    adventure.mousey = y
                    current_x = adventure.mousex
                    current_y = adventure.mousey
                    try:
                        print("before mouse")
                        current_handled = adventure_editor_mouse(adventure.mousex, adventure.mousey)
                        # if current_handled == True:
                        # Don't consume the event - let it pass through
                        #    raise renpy.IgnoreEvent()
                        print("after mouse", current_handled)
                    except:
                        current_handled = False
                        adventure.editing = False

                    if not current_handled and current_x > 0 and current_y > 0 and adventure.modalFreeze == 0:
                        print("doing other handler")
                        targ = []
                        for i in range(len(adventure.room)):
                            if (len(adventure.room[i]["points"]) > 2):
                              print(adventure.room[i]["points"])
                              if point_in_polygon(adventure.mousex, adventure.mousey, adventure.room[i]["points"]):
                                  if adventure.room[i]["label"] != "":
                                      targ.append(adventure.room[i]["label"])
                                  else:
                                      targ.append("Poly " + str(i))
                              else:
                                  print("Point OUTSIDE")
                        if len(targ) > 0:
                            adventure._temp_return = "*" + "*".join(targ) + "*"
                            adventure.screen_should_exit = True
                            print("SHOULD EXIT: " + adventure._temp_return)
                        else:
                            adventure._temp_return = "(" + str(adventure.mousex) + "," + str(adventure.mousey) + ")"
                            adventure.screen_should_exit = True
                            print("SHOULD EXIT DEFAULT")
                        renpy.restart_interaction()
                        raise renpy.IgnoreEvent()

        def render(self, width, height, st, at):
            return renpy.Render(1, 1)
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
        if len(points) < 3:
            return False
        
        n = len(points)
        inside = False
        
        p1x, p1y = points[0]
        for i in range(1, n + 1):
            p2x, p2y = points[i % n]
            
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    # </def>

    # <def>
    def checkEvent():
        # Create text showing the actual coordinates
        coordinates_text = "Mouse: ({}, {})".format(adventure.mousex, adventure.mousey)
        return Text(coordinates_text, color="#FF0000", size=30)
    # </def>

    config.overlay_functions.append(checkEvent)
    
    # Helper functions for screen-based mouse tracking
    # <def>
    def update_mouse_pos():
        pos = renpy.get_mouse_pos()
        adventure.mousex = pos[0]
        adventure.mousey = pos[1]
    # </def>

    # <def>    
    def click_mouse_pos():
        pos = renpy.get_mouse_pos()
        adventure.mousex = pos[0]
        adventure.mousey = pos[1]
        print("Screen click at: ({}, {})".format(pos[0], pos[1]))
    # </def>

    # <def>
    def adventure_init():
        try:
            store.roomData.update(room_definitions)
        except:
            print("No room data loaded")
    # </def>

# <screen>
screen adventure_editor():
    pass
# </screen>

# <screen>
screen adventure_interaction():

    if adventure.screen_should_exit and adventure.modalFreeze == 0 and adventure._temp_return:
        $ adventure.screen_should_exit = False  # Reset flag
        $ adventure.actual_return = adventure._temp_return if hasattr(adventure, '_temp_return') else None
        $ adventure.result = adventure.actual_return
        $ adventure._temp_return = None
        $ Return(adventure.actual_return)
        timer 0.01 action Return(adventure.actual_return)

    # Add your mouse position tracker
    add mousePosition
    use adventure_editor

# </screen>

# <label>
label adventure_input:
    python:
        adventure_init()
#       try:
#           adventure_editor_input()
#       except:
#           adventure.editing = False
        if not adventure.roomName in roomData:
            roomData[adventure.roomName] = []
        adventure.room = roomData[adventure.roomName]
        adventure.screen_should_exit = False
        adventure.result = ""

    call screen adventure_interaction

    python:
        adventure.result = _return
        if adventure.result == "":
            renpy.jump("adventure_input")
        else:
            renpy.return_statement(adventure.result);
# </label>
