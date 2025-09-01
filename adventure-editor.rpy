"""
**************************************************************************
**
**   adventure-editor.rpy - Editor for Adventure Module (for RenPy)
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

define ADVENTURE_EDITOR_VERSION_MAJOR = 0
define ADVENTURE_EDITOR_VERSION_MINOR = 1
define ADVENTURE_EDITOR_VERSION_REVISION = 0

init python:
    import math
    import pygame
    import renpy.display.render as render
    from renpy.display.core import Displayable
    import math

    def examine_save_file(slot):
        """Read save file using public Ren'Py functions"""
        try:
            # First, save current state to a temp location
            current_vars = {}
            for name, value in store.__dict__.items():
                if not name.startswith('_') and not callable(value):
                    current_vars[name] = value
            
            print("=== CURRENT STORE VARIABLES ===")
            for name, value in current_vars.items():
                print("{}: {} = {}".format(name, type(value).__name__, repr(value)[:100]))
            
            # Try to get save info
            import renpy
            save_info = renpy.list_saved_games()
            print("=== AVAILABLE SAVES ===")
            for save in save_info:
                print("Slot: {}, Time: {}".format(save[0], save[1]))
            
        except Exception as e:
            print("Error: {}".format(e))


    def get_polygon_weighted_center(points, density_radius=50):
        """
        Get the perceptual center of a polygon, weighted toward thicker sections.
        
        Args:
            points: List of (x, y) coordinate tuples
            density_radius: Radius to check for local point density (affects weighting)
        
        Returns:
            (center_x, center_y) tuple
        """
        if len(points) < 3:
            # Not enough points for a polygon, return simple average
            if len(points) == 0:
                return (0, 0)
            avg_x = sum(p[0] for p in points) / len(points)
            avg_y = sum(p[1] for p in points) / len(points)
            return (avg_x, avg_y)
        
        # Method 1: Weighted by local point density
        weighted_x = 0
        weighted_y = 0
        total_weight = 0
        
        for i, point in enumerate(points):
            # Calculate local density around this point
            density = 0
            for j, other_point in enumerate(points):
                if i != j:
                    distance = math.sqrt((point[0] - other_point[0])**2 + (point[1] - other_point[1])**2)
                    if distance < density_radius:
                        # Closer points contribute more to density
                        density += (density_radius - distance) / density_radius
            
            # Weight this point by its local density
            weight = max(1.0, density)  # Minimum weight of 1
            weighted_x += point[0] * weight
            weighted_y += point[1] * weight
            total_weight += weight
        
        if total_weight > 0:
            return (weighted_x / total_weight, weighted_y / total_weight)
        else:
            # Fallback to geometric centroid
            return get_polygon_centroid(points)
    
    def get_polygon_centroid(points):
        """
        Calculate the geometric centroid (center of mass) of a polygon.
        This is more accurate than simple average for irregular shapes.
        """
        if len(points) < 3:
            if len(points) == 0:
                return (0, 0)
            avg_x = sum(p[0] for p in points) / len(points)
            avg_y = sum(p[1] for p in points) / len(points)
            return (avg_x, avg_y)
        
        # Using the shoelace formula for polygon centroid
        area = 0
        cx = 0
        cy = 0
        
        for i in range(len(points)):
            j = (i + 1) % len(points)
            xi, yi = points[i]
            xj, yj = points[j]
            
            cross = xi * yj - xj * yi
            area += cross
            cx += (xi + xj) * cross
            cy += (yi + yj) * cross
        
        if area == 0:
            # Degenerate polygon, use simple average
            avg_x = sum(p[0] for p in points) / len(points)
            avg_y = sum(p[1] for p in points) / len(points)
            return (avg_x, avg_y)
        
        area *= 0.5
        cx /= (6 * area)
        cy /= (6 * area)
        
        return (abs(cx), abs(cy))
    
    def get_polygon_visual_center(points, method="weighted"):
        """
        Get the visual center using different methods.
        
        Args:
            points: List of (x, y) coordinate tuples
            method: "weighted", "centroid", "average", or "bbox"
        """
        if method == "weighted":
            return get_polygon_weighted_center(points)
        elif method == "centroid":
            return get_polygon_centroid(points)
        elif method == "average":
            if not points:
                return (0, 0)
            avg_x = sum(p[0] for p in points) / len(points)
            avg_y = sum(p[1] for p in points) / len(points)
            return (avg_x, avg_y)
        elif method == "bbox":
            if not points:
                return (0, 0)
            min_x = min(p[0] for p in points)
            max_x = max(p[0] for p in points)
            min_y = min(p[1] for p in points)
            max_y = max(p[1] for p in points)
            return ((min_x + max_x) / 2, (min_y + max_y) / 2)
        else:
            return get_polygon_weighted_center(points)

    # <class>
    class AlphaPolygon(renpy.Displayable):
        """
        A Ren'Py displayable that draws a filled polygon with alpha transparency.
        
        Args:
            points: List of (x, y) coordinate tuples defining the polygon vertices
            color: Color as (r, g, b, a) tuple where values are 0-255
            width: Width of the displayable (optional, auto-calculated if not provided)
            height: Height of the displayable (optional, auto-calculated if not provided)
        """
        
        def __init__(self, points, color, width=None, height=None):
            super(AlphaPolygon, self).__init__()
            
            self.original_points = points
            self.color = color
            
            # Calculate bounds if width/height not provided
            if points:
                min_x = min(point[0] for point in points)
                max_x = max(point[0] for point in points)
                min_y = min(point[1] for point in points)
                max_y = max(point[1] for point in points)
                
                self.width = width if width is not None else int(max_x - min_x*0) + 1
                self.height = height if height is not None else int(max_y - min_y*0) + 1
                
                # Store offset to normalize coordinates
                self.offset_x = min_x
                self.offset_y = min_y
                
                # Pre-calculate normalized points (relative to 0,0)
                self.normalized_points = [
                    (point[0] - self.offset_x*0, point[1] - self.offset_y*0) 
                    for point in points
                ]
            else:
                self.width = width or 100
                self.height = height or 100
                self.offset_x = 0
                self.offset_y = 0
                self.normalized_points = []
        
        def render(self, width, height, st, at):
            # Create a render with the specified dimensions
            r = render.Render(self.width, self.height)
            
            # Create a surface with per-pixel alpha
            surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            surf = surf.convert_alpha()
            
            # Use the pre-calculated normalized points
            if len(self.normalized_points) >= 3:  # Need at least 3 points for a polygon
                pygame.draw.polygon(surf, self.color, self.normalized_points)
            
            # Blit the surface to the render
            r.blit(surf, (0, 0))
            
            return r
        
        def event(self, ev, x, y, st):
            # Handle events if needed (e.g., clicks within the polygon)
            return None
    # </class>

    # <def>
    def create_gradient(width, height, color1, color2, direction="vertical"):
        """
        Create a gradient image dynamically using Ren'Py's displayables
        """
        # Convert hex to RGB if needed
        def hex_to_rgb(hex_color):
            if isinstance(hex_color, str):
                hex_color = hex_color.lstrip('#')
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            return hex_color
        
        c1 = hex_to_rgb(color1)
        c2 = hex_to_rgb(color2)
        
        # Create gradient by layering multiple Solid rectangles
        layers = []
        steps = min(height if direction == "vertical" else width, 20)  # Fewer steps for performance
        
        for i in range(steps):
            if direction == "vertical":
                ratio = i / float(steps - 1) if steps > 1 else 0
                y_pos = int(i * height / steps)
                slice_height = max(1, int(height / steps) + 1)
                
                color = [int(c1[j] + (c2[j] - c1[j]) * ratio) for j in range(3)]
                hex_color = "#{:02x}{:02x}{:02x}".format(*color)
                
                # Add position tuple and displayable separately to layers
                layers.append((0, y_pos))
                layers.append(Transform(Solid(hex_color), xsize=width, ysize=slice_height))
                
        return Composite((width, height), *layers)
    # </def>

    # <def>
    def clear_current_poly():
        if 0 <= adventure.polyId < len(adventure.room):
            adventure.mousex = -1
            adventure.room[adventure.polyId] = { "points": [], "label": '' }
            store.roomData[adventure.roomName] = adventure.room
            adventure.screen_should_exit = True
            renpy.restart_interaction()
    # </def>
    
    # <class>
    class Line(renpy.Displayable):
        def __init__(self, start_pos, end_pos, color, width, **kwargs):
            super(Line, self).__init__(**kwargs)
            self.start_pos = start_pos
            self.end_pos = end_pos
            self.color = color
            self.width = width

        def render(self, width, height, st, at):
            # Create a new render object.
            render = renpy.Render(width, height)
            
            # Get the canvas object to draw on.
            canvas = render.canvas()
            
            # Draw the line using Pygame's aaline function for antialiasing.
            # You can also use canvas.line() if you don't need antialiasing.
            canvas.circle(self.color, self.start_pos, self.width / 2)
            canvas.circle(self.color, self.end_pos, self.width / 2)

            canvas.line(
                self.color,
                self.start_pos,
                self.end_pos,
                self.width
            )
            
            # Return the render object.
            return render
    # </class>
    
    # <class>
    class PolyLine(renpy.Displayable):
        """
        A displayable that draws a polygon outline using connected line segments.
        Automatically closes the polygon by connecting the last point to the first.
        """
        
        def __init__(self, points, color, width, **kwargs):
            super(PolyLine, self).__init__(**kwargs)
            self.points = points
            self.color = color
            self.width = width
        
        def render(self, width, height, st, at):
            # Create a render surface
            render_surface = renpy.Render(width, height)
            
            # Don't draw if we have fewer than 2 points
            if len(self.points) < 2:
                return render_surface
            
            # Draw lines between consecutive points
            for i in range(len(self.points) - 1):
                start_point = self.points[i]
                end_point = self.points[i + 1]
                line = Line(start_point, end_point, self.color, self.width)
                line_render = renpy.render(line, width, height, st, at)
                render_surface.blit(line_render, (0, 0))
            
            # Close the polygon by connecting last point to first point
            if len(self.points) > 2:  # Only close if we have at least 3 points
                last_point = self.points[-1]
                first_point = self.points[0]
                closing_line = Line(last_point, first_point, self.color, self.width)
                closing_render = renpy.render(closing_line, width, height, st, at)
                render_surface.blit(closing_render, (0, 0))
            
            return render_surface
    # </class>

    # <def>
    def adventure_editor_mouse(current_x, current_y):
        # Debug print to console
        current_mode = adventure.editMode
        print("EDITOR - Click detected at: ({}, {}) mode {}".format(current_x, current_y, current_mode))
        while len(adventure.room) <= adventure.polyId:
            adventure.room.append({ "points": [], "label": "" })

        if current_x > 0 and current_y > 0 and adventure.modalFreeze == 0:
            if current_mode == 1:
                print("Collecting Point")
                adventure.room[adventure.polyId]["points"].append((current_x, current_y))
                store.roomData[adventure.roomName] = adventure.room
                # Force a global redraw to update all screen elements
                adventure.screen_should_exit = True
                renpy.restart_interaction()
                return True
            else:
                return False

        return False
    # </def>

    # <def>
    def priorPoly():
        adventure.mousex = -1
        if len(adventure.room) > 0 and len(adventure.room[len(adventure.room)-1]["points"]) == 0 and adventure.room[len(adventure.room)-1]["label"] == "":
            adventure.room.pop()
        if adventure.polyId > 0:
             adventure.polyId -= 1
        else:
             adventure.polyId = len(adventure.room)
        store.roomData[adventure.roomName] = adventure.room
        adventure.screen_should_exit = True
        renpy.restart_interaction()
    # </def>
    
    # <def>
    def nextPoly():
      adventure.mousex = -1
      if adventure.polyId == len(adventure.room) - 1:
          # <if>
          if len(adventure.room[adventure.polyId]["points"]) > 0 or adventure.room[adventure.polyId]["label"] != "":
              adventure.polyId += 1
          else:
              adventure.polyId = 0
              adventure.room.pop()
          # </if>
      else:
          adventure.polyId += 1
      store.roomData[adventure.roomName] = adventure.room
      adventure.screen_should_exit = True
      renpy.restart_interaction()
    # </def>
    
    # <def>
    def toggle_editor_pos():
      print("TOGGLE EDITOR POS")
      adventure.editorPos = 1 - adventure.editorPos
      adventure.screen_should_exit = True
      renpy.restart_interaction()
    # </def>

    # <def>
    def get_poly_label():
      if adventure.modalFreeze == 0:
          adventure.modalFreeze = 1
          adventure.room[adventure.polyId]["label"] = renpy.call_in_new_context("get_poly_label_inner", "Label:", default=adventure.room[adventure.polyId]["label"], length=40)
          adventure.modalFreeze = 0
          adventure.screen_should_exit = True
          renpy.restart_interaction()
      # </def>
    
    # <def>
    def debug_save_contents():
        print("=== SAVE DEBUG ===")
        for name, value in store.__dict__.items():
            if not name.startswith('_') and not callable(value):
                try:
                    # Test if it's serializable (save-safe)
                    import pickle
                    pickle.dumps(value)
                    print("SAVEABLE: {} = {} (type: {})".format(name, repr(value)[:100], type(value).__name__))
                except:
                    print("NOT SAVEABLE: {} (type: {})".format(name, type(value).__name__))
    # </def>

    # <def>
    def adventure_editor_input():
        print("editor input")
    # </def>

    # <def>
    def export_room_data_readable():
        """Export roomData in a more readable format"""
        import os
        
        try:
            game_dir = renpy.config.gamedir
            output_file = os.path.join(game_dir, "room_data.rpy")
            
            with open(output_file, 'w') as f:
                f.write('# Auto-generated room data export\n')
                f.write('# Generated by Adventure Editor\n\n')
                
                f.write('init python:\n')
                f.write('    # Room data definitions\n')
                f.write('    room_definitions = {\n')
                
                for room_name, room_polys in store.roomData.items():
                    f.write('        "{}": [\n'.format(room_name))
                    for poly in room_polys:
                        f.write('            {\n')
                        f.write('                "points": {},\n'.format(repr(poly["points"])))
                        f.write('                "label": "{}"\n'.format(poly["label"]))
                        f.write('            },\n')
                    f.write('        ],\n')
                
                f.write('    }\n\n')
            
            print("Room data exported to: {}".format(output_file))
            renpy.notify("Room data exported successfully!")
            
        except Exception as e:
            print("Export failed: {}".format(e))
            renpy.notify("Export failed: {}".format(str(e)))
    # </def>

# <label>
label get_poly_label_inner(prompt, default, length=20):
  show screen adventure_interaction
  $ result = renpy.input(prompt, default, length=length)
  return result
# </label>

# <screen>
screen adventure_editor():

    modal True

    python:
        if adventure.roomName != adventure.lastRoom:
            # Initialize the new room:
            adventure.polyId = 0
            adventure.lastRoom = adventure.roomName
        editor_x = 20 if (adventure.editorPos == 0) else (config.screen_width - 120)
        while len(adventure.room) <= adventure.polyId:
            adventure.room.append({ "points": [], "label": "" })

    $ print(adventure.room)
    $ print(adventure.polyId)

    for i in range(len(adventure.room)):
        if (i != adventure.polyId):
            add AlphaPolygon(adventure.room[i]["points"], (0, 0, 255, 128))
            add PolyLine(adventure.room[i]["points"], "#0000ff", 2)
            $ center_x, center_y = get_polygon_weighted_center(adventure.room[i]["points"])
            text adventure.room[i]["label"]:
                color "#ffffff"
                xpos center_x
                ypos center_y
                xanchor 0.5
                yanchor 0.5

    if len(adventure.room[adventure.polyId]["points"]) >= 1:
          
        $ current_polygon = AlphaPolygon(adventure.room[adventure.polyId]["points"], (255, 0, 0, 128))
        # show expression current_polygon as curent_poly
        add current_polygon

        add PolyLine(adventure.room[adventure.polyId]["points"], "#ff0000", 3)

    frame:
        background Frame(Solid("#FFFFFF"), 2, 2, tile=False)
        xpos editor_x - 5
        ypos 80
        xsize 110
        ysize 300
        padding (2, 2)  # Border Thickness

        vbox:
            # Title bar with background
            button:
                background create_gradient(106, 20, "#00FFBB", "#006633", "vertical")
                action Function(toggle_editor_pos)
                xfill True
                ysize 20
                padding (5, 2)

                if adventure.editorPos == 0:
                    text "Editor ▷" size 12 bold True color "#FFFFFF" xalign 0.5 yalign 0.5
                else:
                    text "◁ Editor" size 12 bold True color "#FFFFFF" xalign 0.5 yalign 0.5

            # Main content with NullAction button
            frame:
                xfill True
                yfill True
                background None
                padding (0, 0)
                
                add Solid("#000000")

                vbox:
                    text "Room:":
                        ypos 140
                        xpos 50
                        xanchor 0.5
                        bold True
                        size 14
                    text "[adventure.roomName]":
                        ypos 145
                        xpos 50
                        xanchor 0.5
                        size 14
                    button:
                        action NullAction()
                        background None  # Transparent
                        xfill True
                        ysize 25


                    button:
                        background create_gradient(106, 20, "#330000", "#660000", "vertical")
                        hover_background create_gradient(106, 20, "#660000", "#990000", "vertical")
                        action Function(get_poly_label)
                        xfill True
                        ysize 20

                        $ cur_polylabel = adventure.room[adventure.polyId]["label"]
                        if cur_polylabel == "":
                            text "[[unlabeled]" size 12 bold True color "#999999" xpos 50 xanchor 0.5 ypos 0
                        else:
                            text cur_polylabel size 12 bold False color "#FFFFFF" xpos 50 xanchor 0.5 ypos 0

                    button:
                        action NullAction()
                        background None  # Transparent
                        xfill True
                        yfill True


    if adventure.modalFreeze == 0:

        button:
            background "#000099"
            ypos 285
            xpos editor_x - 3
            xsize 106
            ysize 25
            action [SetVariable("adventure.editMode", 0), Return("ok")]
            text "(Return)" size 12 xpos 48 xanchor 0.5

        # Optional: Add a button to clear/reset coordinates
        textbutton "Reset":
            action Function(clear_current_poly)
            text_size 12
            xpos editor_x
            ypos 100

        if adventure.editMode == 1:
            textbutton "Mode = Draw":
                action [SetVariable("adventure.editMode", 1 - adventure.editMode), Function(debug_save_contents)]
                text_size 12
                xpos editor_x
                ypos 120
        else:
            textbutton "Mode = Play":
                action [SetVariable("adventure.editMode", 1 - adventure.editMode), Function(debug_save_contents)]
                text_size 12
                xpos editor_x
                ypos 120

        textbutton "◂◂":
            action Function(priorPoly)
            text_size 12
            xpos editor_x
            ypos 140

        textbutton "▸▸":
            action Function(nextPoly)
            text_size 12
            xpos (editor_x + 100)
            xanchor 1.0
            ypos 140

        textbutton "Export":
            action Function(export_room_data_readable)
            text_size 12
            xpos editor_x
            ypos 300

    text "Poly " + str(adventure.polyId + 1) size 15 xpos (editor_x + 50) xanchor 0.5 ypos 140 color "#00cc66"

# </screen>

