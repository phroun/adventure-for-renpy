"""
**************************************************************************
**
**   adventure-editor.rpy - Editor for Adventure Module (for RenPy)
**
**   Version 0.1 revision 4
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
define ADVENTURE_EDITOR_VERSION_REVISION = 4

define editor_width = 126
default adventure.editor_last_targids = []
default adventure.pointId = 0
default adventure.pointMode = 0

# <init>
init python:
    import math
    import pygame
    import renpy.display.render as render
    from renpy.display.core import Displayable
    import math

    # <def>
    def examine_save_file(slot):
        """Read save file using public Ren'Py functions"""
        # <try>
        try:
            # First, save current state to a temp location
            current_vars = {}
            # <for>
            for name, value in store.__dict__.items():
                # <if>
                if not name.startswith('_') and not callable(value):
                    current_vars[name] = value
                # </if>
            # </for>
            print("=== CURRENT STORE VARIABLES ===")
            # <for>
            for name, value in current_vars.items():
                print("{}: {} = {}".format(name, type(value).__name__, repr(value)[:100]))
            # </for>
            # Try to get save info
            import renpy
            save_info = renpy.list_saved_games()
            print("=== AVAILABLE SAVES ===")
            # <for>
            for save in save_info:
                print("Slot: {}, Time: {}".format(save[0], save[1]))
            # </for>
        except Exception as e:
            print("Error: {}".format(e))
        # </try>
    # </def examine_save_file>

    # <def>
    def get_polygon_weighted_center(points, density_radius=50):
        """
        Get the perceptual center of a polygon, weighted toward thicker sections.
        
        Args:
            points: List of (x, y) coordinate tuples
            density_radius: Radius to check for local point density (affects weighting)
        
        Returns:
            (center_x, center_y) tuple
        """
        # <if>
        if len(points) < 3:
            # Not enough points for a polygon, return simple average
            # <if>
            if len(points) == 0:
                return (0, 0)
            # </if empty>
            avg_x = sum(p[0] for p in points) / len(points)
            avg_y = sum(p[1] for p in points) / len(points)
            return (avg_x, avg_y)
        # </if not polygon>
        
        # Method 1: Weighted by local point density
        weighted_x = 0
        weighted_y = 0
        total_weight = 0

        # <for>
        for i, point in enumerate(points):
            # Calculate local density around this point
            density = 0
            # <for>
            for j, other_point in enumerate(points):
                # <if>
                if i != j:
                    distance = math.sqrt((point[0] - other_point[0])**2 + (point[1] - other_point[1])**2)
                    # <if>
                    if distance < density_radius:
                        # Closer points contribute more to density
                        density += (density_radius - distance) / density_radius
                    # </if>
                # </if>
            # </for>
            # Weight this point by its local density
            weight = max(1.0, density)  # Minimum weight of 1
            weighted_x += point[0] * weight
            weighted_y += point[1] * weight
            total_weight += weight
        # </for>
        # <if>
        if total_weight > 0:
            return (weighted_x / total_weight, weighted_y / total_weight)
        else:
            # Fallback to geometric centroid
            return get_polygon_centroid(points)
        # </if>
    # </def get_polygon_weighted_center>
    
    # <def>
    def get_polygon_centroid(points):
        """
        Calculate the geometric centroid (center of mass) of a polygon.
        This is more accurate than simple average for irregular shapes.
        """
        # <if>
        if len(points) < 3:
            # <if>
            if len(points) == 0:
                return (0, 0)
            # </if>
            avg_x = sum(p[0] for p in points) / len(points)
            avg_y = sum(p[1] for p in points) / len(points)
            return (avg_x, avg_y)
        # </if>
        # Using the shoelace formula for polygon centroid
        area = 0
        cx = 0
        cy = 0
        # <for>
        for i in range(len(points)):
            j = (i + 1) % len(points)
            xi, yi = points[i]
            xj, yj = points[j]
            
            cross = xi * yj - xj * yi
            area += cross
            cx += (xi + xj) * cross
            cy += (yi + yj) * cross
        # </for>

        # <if>
        if area == 0:
            # Degenerate polygon, use simple average
            avg_x = sum(p[0] for p in points) / len(points)
            avg_y = sum(p[1] for p in points) / len(points)
            return (avg_x, avg_y)
        # </if>
        
        area *= 0.5
        cx /= (6 * area)
        cy /= (6 * area)
        
        return (abs(cx), abs(cy))
    # </def get_polygon_cenroid>
    
    # <def>
    def get_polygon_visual_center(points, method="weighted"):
        """
        Get the visual center using different methods.
        
        Args:
            points: List of (x, y) coordinate tuples
            method: "weighted", "centroid", "average", or "bbox"
        """
        # <if>
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
        # </if>
    # </def get_polygon_visual_center>

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
    # </class AlphaPolygon>

    # <def>
    def create_gradient(width, height, color1, color2, direction="vertical"):
        """
        Create a gradient image dynamically using Ren'Py's displayables
        """
        # Convert hex to RGB if needed
        # <def>
        def hex_to_rgb(hex_color):
            # <if>
            if isinstance(hex_color, str):
                hex_color = hex_color.lstrip('#')
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            # </if>
            return hex_color
        # </def>
        
        c1 = hex_to_rgb(color1)
        c2 = hex_to_rgb(color2)
        
        # Create gradient by layering multiple Solid rectangles
        layers = []
        steps = min(height if direction == "vertical" else width, 20)  # Fewer steps for performance
        
        # <for>
        for i in range(steps):
            # <if>
            if direction == "vertical":
                ratio = i / float(steps - 1) if steps > 1 else 0
                y_pos = int(i * height / steps)
                slice_height = max(1, int(height / steps) + 1)
                
                color = [int(c1[j] + (c2[j] - c1[j]) * ratio) for j in range(3)]
                hex_color = "#{:02x}{:02x}{:02x}".format(*color)
                
                # Add position tuple and displayable separately to layers
                layers.append((0, y_pos))
                layers.append(Transform(Solid(hex_color), xsize=width, ysize=slice_height))
            # </if>
        # </for> 
        return Composite((width, height), *layers)
    # </def create_gradient>

    # <def>
    def set_play_mode():
        adventure.editMode = 0
        adventure.screen_should_exit = True
        renpy.restart_interaction()
    # </def set_play_mode>

    # <def>
    def set_select_mode():
        adventure.editMode = 1
        adventure.screen_should_exit = True
        renpy.restart_interaction()
    # </def set_select_mode>

    # <def>
    def set_pointedit_mode():
        adventure.editMode = 2
        adventure.pointMode = 0
        adventure.screen_should_exit = True
        renpy.restart_interaction()
    # </def set_pointedit_mode>

    # <def>
    def set_pointmode():
        adventure.pointMode = 1 - adventure.pointMode
        adventure.screen_should_exit = True
        renpy.restart_interaction()
    # </def set_pointmode>

    # <def>
    def delete_point():
        # <if>
        if adventure.pointId > 0 or len(adventure.room[adventure.interactableId]["points"]) > 1:
          del adventure.room[adventure.interactableId]["points"][adventure.pointId]
          # <if>
          if adventure.pointId > 0:
              adventure.pointId -= 1
          else:
              adventure.pointId = len(adventure.room[adventure.interactableId]["points"]) - 1
          # </if>
        # </if>
        adventure.screen_should_exit = True
        renpy.restart_interaction()
    # </def set_pointmode>

    # <def>
    def delete_interactable():
        # <if>
        if adventure.interactableId > 0 or len(adventure.room) > 0:
            del adventure.room[adventure.interactableId]
            # <if>
            if adventure.interactableId > 0:
                adventure.interactableId -= 1
            else:
                adventure.interactableId = 0
            # </if>
        # </if>
        adventure.editMode = 1
        adventure.screen_should_exit = True
        renpy.restart_interaction()
    # </def deleter_interactable>

    # <class>
    class Line(renpy.Displayable):
        # <def>
        def __init__(self, start_pos, end_pos, color, width, **kwargs):
            super(Line, self).__init__(**kwargs)
            self.start_pos = start_pos
            self.end_pos = end_pos
            self.color = color
            self.width = width
        # </def __init__>
        
        # <def>
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
        # </def render>
    # </class Line>
    
    # <class>
    class PolyLine(renpy.Displayable):
        """
        A displayable that draws a polygon outline using connected line segments.
        Automatically closes the polygon by connecting the last point to the first.
        """
        # <def>
        def __init__(self, points, color, width, **kwargs):
            super(PolyLine, self).__init__(**kwargs)
            self.points = points
            self.color = color
            self.width = width
        # </def>
        
        # <def>
        def render(self, width, height, st, at):
            # Create a render surface
            render_surface = renpy.Render(width, height)
            
            # Don't draw if we have fewer than 2 points
            # <if>
            if len(self.points) < 2:
                return render_surface
            # </if>
            
            # <for>
            # Draw lines between consecutive points
            for i in range(len(self.points) - 1):
                start_point = self.points[i]
                end_point = self.points[i + 1]
                line = Line(start_point, end_point, self.color, self.width)
                line_render = renpy.render(line, width, height, st, at)
                render_surface.blit(line_render, (0, 0))
            # </for>
            
            # <if>
            # Close the polygon by connecting last point to first point
            if len(self.points) > 2:  # Only close if we have at least 3 points
                last_point = self.points[-1]
                first_point = self.points[0]
                closing_line = Line(last_point, first_point, self.color, self.width)
                closing_render = renpy.render(closing_line, width, height, st, at)
                render_surface.blit(closing_render, (0, 0))
            # </if>
            
            return render_surface
        # </def render>
    # </class PolyLine>
    
    # <class>
    class Circle(renpy.Displayable):
        # <def>
        def __init__(self, radius, color=(255, 255, 255), line_width=0, **kwargs):
            super(Circle, self).__init__(**kwargs)
            self.radius = radius
            self.color = color
            self.line_width = line_width  # 0 for filled circle, >0 for outline only
        # </def __init__>
        # <def>
        def render(self, width, height, st, at):
            # Create a surface large enough for the circle
            diameter = self.radius * 2
            render = renpy.Render(diameter + 1, diameter + 1)
            
            # Get the canvas to draw on
            canvas = render.canvas()
            
            # Draw the circle using canvas methods
            # Center is at (radius, radius) since our surface is diameter x diameter
            canvas.circle(self.color, (self.radius, self.radius), self.radius, self.line_width)
            
            return render
        # </def render>
        # <def>
        def visit(self):
            return []
        # </def visit>
    # </class Circle>

    # <def>
    def adventure_editor_mouse(current_x, current_y):
        # Debug print to console
        current_mode = adventure.editMode
        print("EDITOR - Click detected at: ({}, {}) mode {}".format(current_x, current_y, current_mode))
        # <while>
        while len(adventure.room) <= adventure.interactableId:
            adventure.room.append({
                "points": [],
                "tag": "",
                "type": "polygon",
                "condition": "",
                "go": "",
                "ex": "",
                "op": "",
                "say": ""
            })
        # </while>
        
        # <if>
        if current_x > 0 and current_y > 0 and adventure.modalFreeze == 0:
            # <match>
            match current_mode:
                # <case>
                case 1: # Select Select Tool
                    print("doing other handler")
                    targids = []
                    # <for>
                    for i in range(len(adventure.room)):
                        # <if>
                        if (len(adventure.room[i]["points"]) > 2):
                            print(adventure.room[i]["points"])
                            # <if>
                            if point_in_polygon(adventure.mousex, adventure.mousey, adventure.room[i]["points"]):
                                targids.append(i)
                            # </if>
                        # </if at least 3 points>
                    # </for all polygons in room>
                    # <if>
                    if len(targids) > 0:
                        # <if>
                        if targids == adventure.editor_last_targids:
                            # cycle to next item
                            adventure.interactableId = targids[(targids.index(adventure.interactableId) + 1) % len(targids)]
                        else:
                            adventure.interactableId = targids[0]
                        # </if>
                        adventure.editor_last_targids = targids
                    # </if>
                    renpy.restart_interaction()
                    return True
                # </case 1>
                # <case>
                case 2: # Edit Point Tool
                    print("Collecting Point")
                    # <if>
                    if adventure.pointMode == 1 or len(adventure.room[adventure.interactableId]["points"]) == 0:
                        adventure.room[adventure.interactableId]["points"].insert(adventure.pointId + 1, (current_x, current_y))
                        adventure.pointId += 1
                        # <if>
                        if adventure.pointId > len(adventure.room[adventure.interactableId]["points"]) - 1:
                            adventure.pointId = 0
                        # </if>
                    else:
                        adventure.room[adventure.interactableId]["points"][adventure.pointId] = (current_x, current_y)
                    # </if>
                    store.roomData[adventure.roomName] = adventure.room
                    # Force a global redraw to update all screen elements
                    adventure.screen_should_exit = True
                    renpy.restart_interaction()
                    return True
                # </case 2>
                # <case>
                case _:
                    return False
                # </case default>
            # </match>
        # </if>

        return False
    # </def adventure_editor_mouse>

    # <def>
    def priorPoint():
        # <if>
        if adventure.pointId > 0:
            adventure.pointId -= 1
        else:
            adventure.pointId = max(0, len(adventure.room[adventure.interactableId]["points"]) - 1)
        # </if>
    # </def priorPoint>

    # <def>
    def nextPoint():
        # <if>
        if adventure.pointId < len(adventure.room[adventure.interactableId]["points"]) - 1:
            adventure.pointId += 1
        else:
            adventure.pointId = 0
        # </if>
    # </def nextPoint>

    # <def>
    def priorInteractable():
        adventure.mousex = -1
        # <if>
        if adventure.interactableId > 0:
             adventure.interactableId -= 1
        else:
             adventure.interactableId = len(adventure.room) - 1
        # </if>
        adventure.pointId = 0
        store.roomData[adventure.roomName] = adventure.room
        adventure.screen_should_exit = True
        renpy.restart_interaction()
    # </def priorInteractable>
    
    # <def>
    def nextInteractable():
        adventure.mousex = -1
        # <if>
        if adventure.interactableId == len(adventure.room) - 1:
            adventure.interactableId = 0
        else:
            adventure.interactableId += 1
        # </if>
        adventure.pointId = 0
        store.roomData[adventure.roomName] = adventure.room
        adventure.screen_should_exit = True
        renpy.restart_interaction()
    # </def nextInteractable>
    
    # <def>
    def create_new_polygon():
        adventure.room.append({
                "points": [],
                "tag": "",
                "type": "polygon",
                "condition": "",
                "go": "",
                "ex": "",
                "op": "",
                "say": ""
        })
        adventure.interactableId = len(adventure.room) - 1
        adventure.pointId = 0
        adventure.pointMode = 1
        adventure.editMode = 2
        adventure.screen_should_exit = True
        renpy.restart_interaction()
    # </def create_new_polygon>
    
    # <def>
    def toggle_editor_pos():
        print("TOGGLE EDITOR POS")
        adventure.editorPos = 1 - adventure.editorPos
        adventure.screen_should_exit = True
        renpy.restart_interaction()
    # </def toggle_editor_pos>

    # <def>
    def get_interactable_tag():
        # <if>
        if adventure.modalFreeze == 0:
            adventure.modalFreeze = 1
            adventure.room[adventure.interactableId]["tag"] = renpy.call_in_new_context("get_interactable_tag_inner", "Tag:", default=adventure.room[adventure.interactableId]["tag"], length=40)
            adventure.modalFreeze = 0
            adventure.screen_should_exit = True
            renpy.restart_interaction()
        # </if>
    # </def get_interactable_tag>
    
    # <def>
    def debug_save_contents():
        print("=== SAVE DEBUG ===")
        # <for>
        for name, value in store.__dict__.items():
            # <if>
            if not name.startswith('_') and not callable(value):
                # <try>
                try:
                    # Test if it's serializable (save-safe)
                    import pickle
                    pickle.dumps(value)
                    print("SAVEABLE: {} = {} (type: {})".format(name, repr(value)[:100], type(value).__name__))
                except:
                    print("NOT SAVEABLE: {} (type: {})".format(name, type(value).__name__))
                # </try>
            # </if>
        # </for>
    # </def debug_save_contents>

    # <def>
    def adventure_editor_input():
        print("editor input")
    # </def>

    # <def>
    def get_mode_text(mode):
        # <match>
        match mode:
            # <case>
            case 0:
                return "Play Game"
            case 1:
                return "Select Interactables"
            case 2:
                return "Edit Points"
            case _:
                return "Unknown"
            # </case>
        # </match>
    # </def>

    # <def>
    def export_room_data_readable():
        """Export roomData in a more readable format"""
        import os
        
        # <try>
        try:
            game_dir = renpy.config.gamedir
            output_file = os.path.join(game_dir, "room_data.rpy")
            
            # <with>
            with open(output_file, 'w') as f:
                f.write('# Auto-generated room data export\n')
                f.write('# Generated by Adventure Editor\n\n')
                
                f.write('init python:\n')
                f.write('    # Room data definitions\n')
                f.write('    room_definitions = {\n')
                
                # <for>
                for room_name, room_interactables in store.roomData.items():
                    f.write('        "{}": [\n'.format(room_name))
                    # <for>
                    for interactable in room_interactables:
                        f.write('            {\n')
                        f.write('                "points": {},\n'.format(repr(interactable["points"])))
                        f.write('                "tag": "{}",\n'.format(interactable["tag"]))
                        f.write('                "type": "{}",\n'.format(interactable["type"]))
                        f.write('                "condition": "{}",\n'.format(interactable["condition"]))
                        f.write('                "go": "{}",\n'.format(interactable["go"]))
                        f.write('                "ex": "{}",\n'.format(interactable["ex"]))
                        f.write('                "op": "{}",\n'.format(interactable["op"]))
                        f.write('                "say": "{}"\n'.format(interactable["say"]))
                        f.write('            },\n')
                    # </for>
                    f.write('        ],\n')
                # </for>
                f.write('    }\n\n')
            # </with>
            
            print("Room data exported to: {}".format(output_file))
            renpy.notify("Room data exported successfully!")
        except Exception as e:
            print("Export failed: {}".format(e))
            renpy.notify("Export failed: {}".format(str(e)))
        # </try>
    # </def export_room_data_readable>

# <label>
label get_interactable_tag_inner(prompt, default, length=20):
  show screen adventure_interaction
  $ result = renpy.input(prompt, default, length=length)
  return result
# </label get_interactable_tag_inner>

# <screen>
screen adventure_editor():

    modal True

    # <python>
    python:
        # <if>
        if adventure.roomName != adventure.lastRoom:
            # Initialize the new room:
            adventure.interactableId = 0
            adventure.lastRoom = adventure.roomName
        # </if>
        editor_x = 20 if (adventure.editorPos == 0) else (config.screen_width - (editor_width + 20))
        # <while>
        while len(adventure.room) <= adventure.interactableId:
            adventure.room.append({ "points": [], "tag": "", "type": "polygon", "condition": "", "go": "", "ex": "", "op": "", "say": "" })
        # </while>
    # </python>

    $ print(adventure.room)
    $ print(adventure.interactableId)

    # <if>
    if adventure.editMode != 0:
        # <for>
        for i in range(len(adventure.room)):
            # <if>
            if (i != adventure.interactableId):
                add AlphaPolygon(adventure.room[i]["points"], (0, 0, 255, 128))
                add PolyLine(adventure.room[i]["points"], "#0000ff", 2)
                $ center_x, center_y = get_polygon_weighted_center(adventure.room[i]["points"])
                # <text>
                text adventure.room[i]["tag"]:
                    color "#ffffff"
                    xpos center_x
                    ypos center_y
                    xanchor 0.5
                    yanchor 0.5
                # </text>
            # </if>
        # </for>

        # <if>
        if len(adventure.room[adventure.interactableId]["points"]) >= 1:
            $ current_polygon = AlphaPolygon(adventure.room[adventure.interactableId]["points"], (255, 0, 0, 128))
            # show expression current_polygon as curent_poly
            add current_polygon
            add PolyLine(adventure.room[adventure.interactableId]["points"], "#ff0000", 3)
        # </if>
        
        # <if>
        if adventure.editMode == 2 and adventure.interactableId < len(adventure.room) and adventure.pointId < len(adventure.room[adventure.interactableId]["points"]):
            $ this_point = adventure.room[adventure.interactableId]["points"][adventure.pointId]
            # <if>
            if adventure.pointId > 0:
                $ last_point = adventure.room[adventure.interactableId]["points"][adventure.pointId - 1]
                add Line(this_point, last_point, (255, 255, 255), 3)
            else:
                $ last_point = adventure.room[adventure.interactableId]["points"][-1]
                $ mid_point = ((this_point[0] + last_point[0]) / 2, (this_point[1] + last_point[1]) / 2)
                add Line(last_point, mid_point, (0, 0, 0), 3)
                add Line(this_point, mid_point, (255, 255, 255), 3)
            # </if>
            add Circle(10, (255, 255, 255), 3) xpos this_point[0] ypos this_point[1] xanchor 0.5 yanchor 0.5
        # </if>
    # </if>

    # <if>
    if GetTooltip():
        # <frame>
        frame:
            background Solid("#000000", alpha=0.8)
            xalign 0.5
            ypos 20
            padding (20, 10)
            # <text>
            text GetTooltip():
                size 18
                color "#ffffff"
                bold True
                text_align 0.5
            # </text>
        # </frame>
    # </if>

    # <frame>
    frame:
        background Frame(Solid("#FFFFFF"), 2, 2, tile=False)
        xpos editor_x - 5
        ypos 80
        xsize (editor_width + 10)
        ysize 300
        padding (2, 2)  # Border Thickness

        # <vbox>
        vbox:
            # Title bar with background
            # <button>
            button:
                background create_gradient(editor_width + 6, 20, "#00FFBB", "#006633", "vertical")
                action Function(toggle_editor_pos)
                tooltip "Toggle Editor Position"
                xfill True
                ysize 20
                padding (5, 2)

                # <if>
                if adventure.editorPos == 0:
                    text "Editor ▷" size 12 bold True color "#FFFFFF" xalign 0.5 yalign 0.5
                else:
                    text "◁ Editor" size 12 bold True color "#FFFFFF" xalign 0.5 yalign 0.5
                # </if>
            # </button>

            # Main content with NullAction button
            # <frame>
            frame:
                xfill True
                yfill True
                background None
                padding (0, 0)
                
                add Solid("#000000")

                # <vbox>
                vbox:
                    # <hbox>
                    # Tool icons section - horizontal layout
                    hbox:
                        spacing 2  # Space between icons
                        xpos 2    # Position from left edge
                        ypos 2    # Position from top edge
                        ysize 60

                        # <button>
                        button:
                            action Function(set_play_mode)
                            tooltip "Play Test Mode"
                            background (Solid("#ccffee") if adventure.editMode == 0 else Solid("#cccccc"))
                            hover_background Solid("#ffffff")
                            xysize (24, 24)  # Size of the button
                            padding (0, 0)   # Internal padding
                            
                            # <add>
                            add "images/editor-icons/editor-play.png":
                                fit "contain"
                                xalign 0.5
                                yalign 0.5
                            # </add>
                        # </button>
                        # <button>
                        button:
                            action Function(set_select_mode)
                            tooltip "Select Polygons or Icons"
                            background (Solid("#ccffee") if adventure.editMode == 1 else Solid("#cccccc"))
                            hover_background Solid("#ffffff")
                            xysize (24, 24)  # Size of the button
                            padding (0, 0)   # Internal padding
                            
                            # <add>
                            add "images/editor-icons/editor-select.png":
                                fit "contain"
                                xalign 0.5
                                yalign 0.5
                            # </add>
                        # </button>
                        # <button>
                        button:
                            action Function(set_pointedit_mode)
                            tooltip "Edit Points or Position"
                            background (Solid("#ccffee") if adventure.editMode == 2 else Solid("#cccccc"))
                            hover_background Solid("#ffffff")
                            xysize (24, 24)
                            padding (0, 0)
                            
                            # <add>
                            add "images/editor-icons/editor-edit-point.png":
                                fit "contain"
                                xalign 0.5
                                yalign 0.5
                            # </add>
                        # </button>
                        # <button>
                        button:
                            action NullAction()
                            tooltip "Create New Interaction Icon"
                            background Solid("#cccccc")
                            hover_background Solid("#ffffff")
                            xysize (24, 24)
                            padding (0, 0)
                            
                            # <add>
                            add "images/editor-icons/editor-new-icon.png":
                                fit "contain"
                                xalign 0.5
                                yalign 0.5
                            # </add>
                        # </button>
                        # <button>
                        button:
                            action Function(create_new_polygon)
                            tooltip "Create New Polygon"
                            background Solid("#cccccc")
                            hover_background Solid("#ffffff")
                            xysize (24, 24)
                            padding (0, 0)
                            
                            # <add>
                            add "images/editor-icons/editor-new-polygon.png":
                                fit "contain"
                                xalign 0.5
                                yalign 0.5
                            # </add>
                        # </button>
                    # </hbox> 
                    # <if>
                    if adventure.editMode > 0:
                        # <button>
                        button:
                            background create_gradient(editor_width + 6, 20, "#330000", "#660000", "vertical")
                            hover_background create_gradient(editor_width + 6, 20, "#660000", "#990000", "vertical")
                            action Function(get_interactable_tag)
                            tooltip "Set Object Tag"
                            xfill True
                            #ypos 35
                            ysize 20

                            $ cur_interactabletag = adventure.room[adventure.interactableId]["tag"]
                            # <if>
                            if cur_interactabletag == "":
                                text "[[untagged]" size 12 bold True color "#999999" xpos (editor_width // 2) xanchor 0.5 ypos 0
                            else:
                                text cur_interactabletag size 12 bold False color "#FFFFFF" xpos ((editor_width // 2) - 2) xanchor 0.5 ypos 0
                            # </if>
                        # </button>
                    else:
                        # <button>
                        button:
                            action NullAction()
                            background None  # Transparent
                            xfill True
                            ysize 20
                        # </button>
                    # </if>

                    # <button>
                    button:
                        action NullAction()
                        background None  # Transparent
                        xfill True
                        ysize 30
                    # </button>

                    # <if>
                    if adventure.editMode == 2:
                        # <hbox>
                        # Tool icons section - horizontal layout
                        hbox:
                            spacing 2  # Space between icons
                            xpos 2    # Position from left edge
                            ypos 2    # Position from top edge

                            # <button>
                            button:
                                action Function(set_pointmode)
                                tooltip "New Point After"
                                background (Solid("#ff3333") if adventure.pointMode == 1 else Solid("#cccccc"))
                                hover_background (Solid("#ffcc33") if adventure.pointMode == 1 else Solid("#ffffff"))
                                xysize (24, 24)  # Size of the button
                                padding (0, 0)   # Internal padding
                                
                                # <add>
                                add "images/editor-icons/editor-new-point.png":
                                    fit "contain"
                                    xalign 0.5
                                    yalign 0.5
                                # </add>
                            # </button>
                            # <button>
                            button:
                                action Function(delete_point)
                                tooltip "Delete This Point"
                                background Solid("#cccccc")
                                hover_background Solid("#ffffff")
                                xysize (24, 24)  # Size of the button
                                padding (0, 0)   # Internal padding
                                
                                # <add>
                                add "images/editor-icons/editor-delete-point.png":
                                    fit "contain"
                                    xalign 0.5
                                    yalign 0.5
                                # </add>
                            # </button>
                            # <button>
                            button:
                                action NullAction()
                                background Solid("#666666")  # Transparent
                                ysize 25
                                xsize 50
                            # </button>
                            # <button>
                            button:
                                action Function(delete_interactable)
                                tooltip "Delete This Polygon"
                                background Solid("#cccccc")
                                hover_background Solid("#ffffff")
                                xysize (24, 24)
                                padding (0, 0)
                                
                                # <add>
                                add "images/editor-icons/editor-delete-polygon.png":
                                    fit "contain"
                                    xalign 0.5
                                    yalign 0.5
                                # </add>
                            # </button>
                        # </hbox>
                    # </if>
                    # <button>
                    button:
                        action NullAction()
                        background None  # Transparent
                        xfill True
                        ysize 25
                    # </button>
                    # <button>
                    button:
                        action NullAction()
                        background None  # Transparent
                        xfill True
                        yfill True
                    # </button>
                # </vbox>
            # </frame>
        # </vbox>
    # </frame>

    # <if>
    if adventure.modalFreeze == 0 and adventure.editMode > 0:
        # <textbutton>
        textbutton "◂◂":
            action Function(priorInteractable)
            tooltip "Select Prior Interactable"
            text_size 12
            xpos editor_x
            text_color "#999999"
            text_hover_color "#99ffee"
            background Solid("#000000")
            hover_background Solid("#333333")
            ypos 135
        # </textbutton>
        # <textbutton>
        textbutton "▸▸":
            action Function(nextInteractable)
            tooltip "Select Next Interactable"
            text_size 12
            xpos (editor_x + editor_width)
            xanchor 1.0
            text_color "#999999"
            text_hover_color "#99ffee"
            background Solid("#000000")
            hover_background Solid("#333333")
            ypos 135
        # </textbutton>
        # <if>
        if adventure.editMode == 2:
            # <textbutton>
            textbutton "◂◂":
                action Function(priorPoint)
                tooltip "Select Prior Point"
                text_size 12
                xpos editor_x
                text_color "#999999"
                text_hover_color "#99ffee"
                background Solid("#000000")
                hover_background Solid("#333333")
                ypos 244
            # </textbutton>
            # <textbutton>
            textbutton "▸▸":
                action Function(nextPoint)
                tooltip "Select Next Point"
                text_size 12
                xpos (editor_x + editor_width)
                xanchor 1.0
                text_color "#999999"
                text_hover_color "#99ffee"
                background Solid("#000000")
                hover_background Solid("#333333")
                ypos 244
            # </textbutton>
        # </if point editor>

    # </if not modalFreeze>

    # <if>
    if adventure.editMode > 0:
        text ("Poly " + str(adventure.interactableId + 1)) size 15 xpos (editor_x + editor_width // 2) xanchor 0.5 ypos 138 color "#00cc66"
    # </if>

    $ mode_text = get_mode_text(adventure.editMode)
    text mode_text size 12 xpos (editor_x + editor_width // 2) xanchor 0.5 ypos 190 color "#999999"

    # <if>
    if adventure.editMode == 2:
        text ("Pt. " + str(adventure.pointId + 1)) size 15 xpos (editor_x + editor_width // 2) xanchor 0.5 ypos 247 color "#00cc66"
    # </if>

    # <text>
    text "Room:":
        ypos 310
        xpos (editor_x + editor_width // 2)
        xanchor 0.5
        bold True
        size 14
    # </text>
    # <text>
    text "[adventure.roomName]":
        ypos 325
        xpos (editor_x + editor_width // 2)
        xanchor 0.5
        size 14
    # </text>
    # <button>
    # <textbutton>
    textbutton "Save Changes":
        action Function(export_room_data_readable)
        tooltip "Permanently Save Room Data"
        text_size 12
        xpos (editor_x + editor_width // 2)
        xanchor 0.5
        ypos 350
    # </textbutton> 
# </screen adventure_editor>
