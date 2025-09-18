init python:
     """
**************************************************************************
**
**   adventure-editor.rpy - Editor for Adventure Module (for Ren'Py)
**
**   Version 0.2 revision 13
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
define ADVENTURE_EDITOR_VERSION_MINOR = 2
define ADVENTURE_EDITOR_VERSION_REVISION = 13

define ADVENTURE_EDITOR_TOOL_PLAY = 0
define ADVENTURE_EDITOR_TOOL_SELECT = 1
define ADVENTURE_EDITOR_TOOL_EDIT = 2

define ADVENTURE_EDITOR_POINT_MOVE = 0
define ADVENTURE_EDITOR_POINT_ADD = 1

define ADVENTURE_EDITOR_LAYER_EX = 0
define ADVENTURE_EDITOR_LAYER_SAY = 1
define ADVENTURE_EDITOR_LAYER_OP = 2
define ADVENTURE_EDITOR_LAYER_GO = 3
define ADVENTURE_EDITOR_LAYER_COND = 4

# <init>
init python:
    import math
    import pygame
    import renpy.display.render as render
    from renpy.display.core import Displayable
    import math

    adventure.editor_width = int(126 * adventure.guiscale)
    adventure.editor_height = int(360 * adventure.guiscale)
    adventure.editor_top = (config.screen_height - adventure.editor_height) // 2
    adventure.editor_left = 20
    adventure.editor_last_targids = []
    adventure.editorLayer = ADVENTURE_EDITOR_LAYER_EX
    adventure.editorTool = ADVENTURE_EDITOR_TOOL_PLAY
    adventure.pointMode = ADVENTURE_EDITOR_POINT_MOVE
    adventure.pointId = 0
    adventure.editor_icons = "adventure/images/editor-icons"
    adventure.editor_hidden = False
    adventure.dragging = False
    adventure.dragging_origin_x = 0
    adventure.dragging_origin_y = 0
    adventure.dragging_start_x = 0
    adventure.dragging_start_y = 0
    adventure.alphaPolyCache = {}
    adventure.polyLineCache = {}

    # <def>
    def adventure_get_polygon_weighted_center(points, density_radius=50):
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
            return adventure_get_polygon_centroid(points)
        # </if>
    # </def adventure_get_polygon_weighted_center>
    
    # <def>
    def adventure_get_polygon_centroid(points):
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
    # </def adventure_get_polygon_cenroid>
    
    # <def>
    def adventure_get_polygon_visual_center(points, method="weighted"):
        """
        Get the visual center using different methods.
        
        Args:
            points: List of (x, y) coordinate tuples
            method: "weighted", "centroid", "average", or "bbox"
        """
        # <if>
        if method == "weighted":
            return adventure_get_polygon_weighted_center(points)
        elif method == "centroid":
            return adventure_get_polygon_centroid(points)
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
            return adventure_get_polygon_weighted_center(points)
        # </if>
    # </def adventure_get_polygon_visual_center>

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
        # <def>
        def __init__(self, points, color, width=None, height=None, cacheId=None):
            super(AlphaPolygon, self).__init__()
            
            self.original_points = points
            self.color = color
            self.cacheId = cacheId
            
            # Calculate bounds if width/height not provided
            # <if>
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
            # </if>
        # </def>
        
        # <def>
        def render(self, width, height, st, at):
            # <if>
            if self.cacheId is not None and (self.cacheId in adventure.alphaPolyCache):
                cr = adventure.alphaPolyCache[self.cacheId]
                # <if>
                if cr["points"] == self.normalized_points and cr["color"] == self.color:
                    return cr["render"]
                # </if>
            # </if>
            
            # Create a render with the specified dimensions
            r = render.Render(self.width, self.height)
            
            # Create a surface with per-pixel alpha
            surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            surf = surf.convert_alpha()
            
            # Use the pre-calculated normalized points
            # <if>
            if len(self.normalized_points) >= 3:  # Need at least 3 points for a polygon
                pygame.draw.polygon(surf, self.color, self.normalized_points)
            # </if>
            # Blit the surface to the render
            r.blit(surf, (0, 0))
            
            # <if>
            if self.cacheId is not None:
                adventure.alphaPolyCache[self.cacheId] = {
                    "points": self.normalized_points,
                    "color": self.color,
                    "render": r
                }
            # </if>

            return r
        # </def>

        # <def>
        def event(self, ev, x, y, st):
            # Handle events if needed (e.g., clicks within the polygon)
            return None
        # </def>
    # </class AlphaPolygon>

    # <def>
    def adventure_create_gradient(width, height, color1, color2, direction="vertical"):
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
    # </def adventure_create_gradient>

    # <def>
    def adventure_hide_editor():
        adventure.editor_hidden = True
        renpy.restart_interaction()
    # </def>

    # <def>
    def set_play_mode():
        # <if>
        if adventure.modalFreeze == 0:
            adventure.editorTool = ADVENTURE_EDITOR_TOOL_PLAY
            adventure.visibleMode = "default"
            adventure.screen_should_exit = True
            adventure.debug_show_inactive = False
            renpy.restart_interaction()
        # </if>
    # </def set_play_mode>
    
    # <def>
    def set_select_mode():
        # <if>
        if adventure.modalFreeze == 0:
            adventure.editorTool = ADVENTURE_EDITOR_TOOL_SELECT
            adventure.visibleMode = get_edit_tool_mode()
            adventure.debug_show_inactive = True
            adventure.screen_should_exit = True
            renpy.restart_interaction()
        # </if>
    # </def set_select_mode>

    # <def>
    def set_pointedit_mode():
        # <if>
        if adventure.modalFreeze == 0:
            adventure.editorTool = ADVENTURE_EDITOR_TOOL_EDIT
            adventure.visibleMode = get_edit_tool_mode()
            adventure.debug_show_inactive = True
            adventure.pointMode = 0
            adventure.screen_should_exit = True
            renpy.restart_interaction()
        # </if>
    # </def set_pointedit_mode>

    # <def>
    def set_pointmode():
        # <if>
        if adventure.modalFreeze == 0:
            adventure.pointMode = 1 - adventure.pointMode
            adventure.screen_should_exit = True
            renpy.restart_interaction()
        # </if>
    # </def set_pointmode>

    # <def>
    def change_ex_icon():
        # <if>
        if adventure.modalFreeze == 0:
            adventure.editorLayer = ADVENTURE_EDITOR_LAYER_EX
            adventure.visibleMode = get_edit_tool_mode()
            adventure.screen_should_exit = True
            renpy.restart_interaction()
        # </if>
    # </def change_ex_icon>

    # <def>
    def change_say_icon():
        # <if>
        if adventure.modalFreeze == 0:
            adventure.editorLayer = ADVENTURE_EDITOR_LAYER_SAY
            adventure.visibleMode = get_edit_tool_mode()
            adventure.screen_should_exit = True
            renpy.restart_interaction()
        # </if>
    # </def change_say_icon>

    # <def>
    def change_op_icon():
        # <if>
        if adventure.modalFreeze == 0:
            adventure.editorLayer = ADVENTURE_EDITOR_LAYER_OP
            adventure.visibleMode = get_edit_tool_mode()
            adventure.screen_should_exit = True
            renpy.restart_interaction()
        # </if>
    # </def change_op_icon>

    # <def>
    def change_go_icon():
        # <if>
        if adventure.modalFreeze == 0:
            adventure.editorLayer = ADVENTURE_EDITOR_LAYER_GO
            adventure.visibleMode = get_edit_tool_mode()
            adventure.screen_should_exit = True
            renpy.restart_interaction()
        # </if>
    # </def change_go_icon>

    # <def>
    def change_condition():
        # <if>
        if adventure.modalFreeze == 0:
            adventure.editorLayer = ADVENTURE_EDITOR_LAYER_COND
            adventure.visibleMode = get_edit_tool_mode()
            adventure.screen_should_exit = True
            renpy.restart_interaction()
        # </if>
    # </def change_condition>

    # <def>
    def adventure_field_value(field):
        # <if>
        if adventure.interactableId <= len(adventure.room) - 1:
            this_interactable = adventure.room[adventure.interactableId]
            # <if>
            if field in this_interactable:
                return adventure_active_value(this_interactable[field])
            else:
                return ""
            # </if>
        else:
            return ""
        # </if>
    # </def>

    # <def>
    def get_edit_tool_mode():
        # <match>
        match adventure.editorLayer:
            # <case>
            case store.ADVENTURE_EDITOR_LAYER_EX:
                return "ex"
            # </case ex>
            # <case>
            case store.ADVENTURE_EDITOR_LAYER_SAY:
                return "say"
            # </case say>
            # <case>
            case store.ADVENTURE_EDITOR_LAYER_OP:
                return "op"
            # </case op>
            # <case>
            case store.ADVENTURE_EDITOR_LAYER_GO:
                return "go"
            # </case go>
            # <case>
            case store.ADVENTURE_EDITOR_LAYER_COND:
                return "condition"
            # </case cond>
            # <case>
            case _:
                return ADVENTURE_EDITOR_LAYER_GO
            # </case default>
        # </match>        
    # </def>

    # <def>
    def get_active_verb_field():
        # <if>
        if adventure.interactableId <= len(adventure.room) - 1:
            return adventure.room[adventure.interactableId][get_edit_tool_mode()]
        else:
            return ""
    # </def>
    
    # <def>
    def adventure_set_verb(field, verb):
        # <if>
        if adventure.interactableId <= len(adventure.room) - 1:
            this_interactable = adventure.room[adventure.interactableId]
            this_interactable[field] = verb
        # </if>
    # </def>

    # <def>
    def toggle_check_icon(field):
        # <if>
        if adventure.interactableId <= len(adventure.room) - 1:
            this_interactable = adventure.room[adventure.interactableId]
            default = "*" + field
            # <if>
            if this_interactable["type"] == "icon":
                # <try>
                try:
                    default = list(adventure.verb_icons[field].keys())[0]
                except:
                    pass
                # </try>
            # <if>
            if this_interactable[field] == "":
                this_interactable[field] = default
            else:
                # <if>
                if this_interactable[field][0] == "/":
                    # <while>
                    while this_interactable[field][0] == "/":
                        this_interactable[field] = this_interactable[field][1:]
                    # </while>
                else:
                    # <if>
                    if this_interactable[field] == default:
                        this_interactable[field] = ""
                    else:
                        this_interactable[field] = "//" + this_interactable[field]
                    # </if default else>
                # </if commented else>
            # </if blank else>
        # </if valid interactable>
    # </def>
    
    # <def>
    def toggle_ex_icon():
        # <if>
        if adventure.modalFreeze == 0:
            adventure.editorLayer = ADVENTURE_EDITOR_LAYER_EX
            adventure.screen_should_exit = True
            toggle_check_icon("ex")
            renpy.restart_interaction()
        # </if>
    # </def toggle_ex_icon>

    # <def>
    def toggle_say_icon():
        # <if>
        if adventure.modalFreeze == 0:
            adventure.editorLayer = ADVENTURE_EDITOR_LAYER_SAY
            adventure.screen_should_exit = True
            toggle_check_icon("say")
            renpy.restart_interaction()
        # </if>
    # </def toggle_say_icon>

    # <def>
    def toggle_op_icon():
        # <if>
        if adventure.modalFreeze == 0:
            adventure.editorLayer = ADVENTURE_EDITOR_LAYER_OP
            adventure.screen_should_exit = True
            toggle_check_icon("op")
            renpy.restart_interaction()
        # </if>
    # </def toggle_op_icon>

    # <def>
    def toggle_go_icon():
        # <if>
        if adventure.modalFreeze == 0:
            adventure.editorLayer = ADVENTURE_EDITOR_LAYER_GO
            adventure.screen_should_exit = True
            toggle_check_icon("go")
            renpy.restart_interaction()
        # </if>
    # </def toggle_go_icon>

    # <def>
    def adventure_delete_point():
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
    # </def adventure_delete_point>

    # <def>
    def delete_interactable():
        # <if>
        if adventure.modalFreeze == 0:
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
            adventure.editorTool = ADVENTURE_EDITOR_TOOL_SELECT
            adventure.screen_should_exit = True
            renpy.restart_interaction()
        # </if>
    # </def delete_interactable>

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

    # <def>
    def adventure_pygame_color(color):
        pygame_color = color
        # <if>
        if isinstance(color, str):
            pygame_color = pygame.Color(color)
        elif len(color) == 3:
            pygame_color = (*color, 255)
        # </if>
        return pygame_color
    # </def>
    
    # <class>
    class PolyLine(renpy.Displayable):
        """
        A displayable that draws a polygon outline using connected line segments.
        Automatically closes the polygon by connecting the last point to the first.
        """
        # <def>
        def __init__(self, points, color, line_width, cacheId=None):  # , **kwargs):
            super(PolyLine, self).__init__() # **kwargs)
            self.cacheId = cacheId
            self.points = points
            self.color = color
            self.line_width = line_width
        # </def>
        
        # <def>
        def render(self, width, height, st, at):
            # <if>
            if self.cacheId is not None and (self.cacheId in adventure.polyLineCache):
                cr = adventure.polyLineCache[self.cacheId]
                # <if>
                if cr["points"] == self.points and cr["color"] == self.color and cr["line_width"] == self.line_width:
                    ren = cr["render"]
                    return ren
                # </if>
            # </if>

            # Create a render surface
            render_surface = renpy.Render(width, height)
            surf = pygame.Surface((width, height), pygame.SRCALPHA)
            surf.fill((0, 0, 0, 0))
            line_buffer = []
            
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
                pygame.draw.line(surf, adventure_pygame_color(self.color), start_point, end_point, self.line_width)
            # </for>

            render_surface.blit(surf, (0, 0))
            
            # <if>
            # Close the polygon by connecting last point to first point
            if len(self.points) > 2:  # Only close if we have at least 3 points
                last_point = self.points[-1]
                first_point = self.points[0]
                pygame.draw.line(surf, adventure_pygame_color(self.color), last_point, first_point, self.line_width)
            # </if>

            # <if>
            if self.cacheId is not None:
                if self.cacheId in adventure.polyLineCache:
                    del adventure.polyLineCache[self.cacheId]
                adventure.polyLineCache[self.cacheId] = {
                    "points": self.points[:],
                    "color": self.color,
                    "line_width": self.line_width,
                    "render": render_surface
                }
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
    
    # <class>
    class AdventureMouseDragHandle(renpy.Displayable):
        def __init__(self, width, height, child, down_action, tooltip=None):
            super(AdventureMouseDragHandle, self).__init__()
            self.width = width
            self.height = height
            self.child = child
            self.down_action = down_action
            self.tooltip = tooltip
            self.hovered = False
            
        def render(self, width, height, st, at):
            child_render = renpy.render(self.child, self.width, self.height, st, at)
            return child_render
            
        def event(self, ev, x, y, st):
            mouse_in_bounds = 0 <= x < self.width and 0 <= y < self.height
            
            # Handle cursor changes with pygame
            if mouse_in_bounds and not self.hovered:
                self.hovered = True
                default_mouse = "hand"
            elif not mouse_in_bounds and self.hovered:
                self.hovered = False
                default_mouse = "default"

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.down_action()
                    renpy.redraw(self, 0)
                    return True
            
            return None
    # </class>

    # <def>
    def adventure_editor_mouse(current_x, current_y):
        current_mode = adventure.editorTool
        # <if>
        if current_x > 0 and current_y > 0 and adventure.modalFreeze == 0:
            # <match>
            match current_mode:
                # <case>
                case store.ADVENTURE_EDITOR_TOOL_SELECT:
                    targids = []
                    # <if>
                    for icon in adventure.screen_icons:
                        # <if>
                        if adventure_point_in_icon(adventure.mousex, adventure.mousey, icon):
                            targids.append(icon["interactableId"])
                        # </if>
                    # </if>
                    # <for>
                    for i in range(len(adventure.room)):
                        # <if>
                        if (len(adventure.room[i]["points"]) > 2) and adventure.room[i]["type"] == "polygon":
                            # <if>
                            if adventure_point_in_polygon(adventure.mousex, adventure.mousey, adventure.room[i]["points"]):
                                targids.append(i)
                            # </if>
                        # </if polygon and at least 3 points>
                    # </for all interactables in room>
                    # <if>
                    if len(targids) > 0:
                        # <if>
                        if adventure.interactableId in targids:
                            # if targids == adventure.editor_last_targids:
                            # cycle to next item
                            adventure.interactableId = targids[(targids.index(adventure.interactableId) + 1) % len(targids)]
                        else:
                            adventure.interactableId = targids[0]
                        # </if>
                        adventure.editor_last_targids = targids
                    # </if>
                    renpy.restart_interaction()
                    return True
                # </case ADVENTURE_EDITOR_TOOL_SELECT>
                # <case>
                case store.ADVENTURE_EDITOR_TOOL_EDIT:
                    # <if>
                    this_interactable = adventure.room[adventure.interactableId]
                    if (adventure.pointMode == ADVENTURE_EDITOR_POINT_ADD and this_interactable["type"] == "polygon") or len(this_interactable["points"]) == 0:
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
                # </case ADVENTURE_EDITOR_TOOL_EDIT>
                # <case>
                case _:
                    return False
                # </case default>
            # </match>
        # </if>

        return False
    # </def adventure_editor_mouse>

    # <def>
    def adventure_prior_point():
        # <if>
        if adventure.pointId > 0:
            adventure.pointId -= 1
        else:
            adventure.pointId = max(0, len(adventure.room[adventure.interactableId]["points"]) - 1)
        # </if>
    # </def adventure_prior_point>

    # <def>
    def adventure_next_point():
        # <if>
        if adventure.pointId < len(adventure.room[adventure.interactableId]["points"]) - 1:
            adventure.pointId += 1
        else:
            adventure.pointId = 0
        # </if>
    # </def adventure_next_point>

    # <def>
    def priorInteractable():
        adventure.mousex = -1
        # <if>
        if adventure.interactableId > 0:
             adventure.interactableId -= 1
        else:
             adventure.interactableId = max(0, len(adventure.room) - 1)
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
        if adventure.interactableId >= len(adventure.room) - 1:
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
    def adventure_create_new_polygon():
        # <if>
        if adventure.modalFreeze == 0:
            adventure.room.append({
                    "points": [],
                    "tag": "",
                    "type": "polygon",
                    "condition": "",
                    "go": "*go",
                    "ex": "*ex",
                    "op": "*op",
                    "say": "*say"
            })
            adventure.interactableId = len(adventure.room) - 1
            adventure.editorTool = ADVENTURE_EDITOR_TOOL_EDIT
            adventure.pointMode = ADVENTURE_EDITOR_POINT_ADD
            adventure.pointId = 0
            adventure.screen_should_exit = True
            renpy.restart_interaction()
        # </if>
    # </def adventure_create_new_polygon>

    # <def>
    def adventure_create_new_icon():
        # <if>
        if adventure.modalFreeze == 0:
            adventure.room.append({
                    "points": [],
                    "tag": "",
                    "type": "icon",
                    "condition": "",
                    "go": "",
                    "ex": "",
                    "op": "",
                    "say": ""
            })
            adventure.interactableId = len(adventure.room) - 1
            adventure.editorTool = ADVENTURE_EDITOR_TOOL_EDIT
            adventure.pointMode = ADVENTURE_EDITOR_POINT_MOVE
            adventure.pointId = 0
            adventure.screen_should_exit = True
            renpy.restart_interaction()
        # </if>
    # </def adventure_create_new_icon>

    # <def>
    def adventure_begin_drag_editor():
        adventure.dragging_origin_x = adventure.mousex
        adventure.dragging_origin_y = adventure.mousey
        adventure.dragging_start_x = adventure.editor_left
        adventure.dragging_start_y = adventure.editor_top
        adventure.dragging = True
        # adventure.screen_should_exit = True
        renpy.restart_interaction()
    # </def adventure_toggle_editor_pos>

    # <def>
    def adventure_end_drag_editor():
        adventure.dragging = False

        if adventure.editor_left + adventure.editor_width < 40:
            adventure.editor_left = 40 - adventure.editor_width
        if adventure.editor_top < 0:
            adventure.editor_top = 0
        if adventure.editor_left > config.screen_width - 40:
            adventure.editor_left = config.screen_width - 40
        if adventure.editor_top > config.screen_height - 40:
            adventure.editor_top = config.screen_height - 40
        
        # adventure.screen_should_exit = True
    # </def adventure_toggle_editor_pos>
    
    # <def>
    def adventure_toggle_editor_pos():
        adventure.editorPos = 1 - adventure.editorPos
        adventure.screen_should_exit = True
        renpy.restart_interaction()
    # </def adventure_toggle_editor_pos>

    # <def>
    def get_interactable_tag():
        # <if>
        if adventure.modalFreeze == 0:
            adventure.modalFreeze = 1
            adventure.room[adventure.interactableId]["tag"] = renpy.call_in_new_context("get_editor_text_inner", "Tag:", default=adventure.room[adventure.interactableId]["tag"], length=40)
            adventure.modalFreeze = 0
            adventure.screen_should_exit = True
            renpy.restart_interaction()
        # </if>
    # </def get_interactable_tag>

    # <def>
    def get_interactable_verb():
        # <if>
        if adventure.modalFreeze == 0:
            adventure.modalFreeze = 1
            prompt_text = "[[*]Verb:"
            # <if>
            if adventure.editorLayer == ADVENTURE_EDITOR_LAYER_COND:
                prompt_text = "Condition Flag(s):"
            # </if>
            adventure.room[adventure.interactableId][get_edit_tool_mode()] = renpy.call_in_new_context("get_editor_text_inner", prompt_text, default=adventure.room[adventure.interactableId][get_edit_tool_mode()], length=40)
            adventure.modalFreeze = 0
            adventure.screen_should_exit = True
            renpy.restart_interaction()
        # </if>
    # </def get_interactable_tag>


    # <def>
    def adventure_editor_event(ev, x, y, st):
        # <if>
        if ev.type in [pygame.MOUSEBUTTONDOWN]:
            adventure.editor_hidden = False
        # </if>
        # <if>
        if adventure.dragging and ev.type == pygame.MOUSEMOTION:
            adventure.editor_top = adventure.dragging_start_y - adventure.dragging_origin_y + y
            adventure.editor_left = adventure.dragging_start_x - adventure.dragging_origin_x + x
            renpy.restart_interaction()
        # </if>
        # <if>
        if adventure.dragging and ev.type == pygame.MOUSEBUTTONUP:
            adventure_end_drag_editor()
        # </if>
    # </def>
    
    # <def>
    def adventure_editor_input():
        pass
    # </def>

    # <def>
    def get_interactable_type():
        # <if>
        if 0 <= adventure.interactableId <= len(adventure.room) - 1:
            return adventure.room[adventure.interactableId]["type"]
        else:
            return "none"
        # </if>
    # </def get_interactable_type>

    # <def>
    def interactable_type_text(inter):
        # <match>
        match inter:
            # <case>
            case "polygon":
                return "Poly"
            case "icon":
                return "Icon"
            case "none":
                return "None"
            case _:
                return "Unkn"
            # </case>
        # </match>
    # </def interactable_type_text>

    # <def>
    def adventure_get_mode_text(mode):
        # <match>
        match mode:
            # <case>
            case store.ADVENTURE_EDITOR_TOOL_PLAY:
                return "Play Game"
            # </case ADVENTURE_EDITOR_TOOL_PLAY>
            # <case>
            case store.ADVENTURE_EDITOR_TOOL_SELECT:
                return "Select Interactables"
            # </case ADVENTURE_EDITOR_TOOL_SELECT>
            # <case>
            case store.ADVENTURE_EDITOR_TOOL_EDIT:
                # <match>
                match get_interactable_type():
                    # <case>
                    case "polygon":
                        return "Edit Points"
                    # </case polygon>
                    # <case>
                    case "icon":
                        return "Reposition Icon"
                    # </case icon>
                    # <case>
                    case _:
                        return "Unknown"
                    # </case default>
                # </match>
            # </case ADVENTURE_EDITOR_TOOL_EDIT>
            # <case>
            case _:
                return "Unknown"
            # </case>
        # </match>
    # </def adventure_get_mode_text>

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
                        f.write('                "type": "{}",\n'.format(interactable["type"]))
                        f.write('                "tag": "{}",\n'.format(interactable["tag"]))
                        f.write('                "points": {},\n'.format(repr(interactable["points"])))
                        f.write('                "condition": "{}",\n'.format(interactable["condition"]))
                        f.write('                "ex": "{}",\n'.format(interactable["ex"]))
                        f.write('                "say": "{}",\n'.format(interactable["say"]))
                        f.write('                "op": "{}",\n'.format(interactable["op"]))
                        f.write('                "go": "{}",\n'.format(interactable["go"]))
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

    # <def>
    def adventure_chunk_dict(original_dict, max_size):
        # <if>
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        # </if>
        items = list(original_dict.items())
        chunks = []
        # <for>
        for i in range(0, len(items), max_size):
            chunk = dict(items[i:i + max_size])
            chunks.append(chunk)
        # </for>
        return chunks
    # </def>

# </init python>

# <label>
label get_editor_text_inner(prompt, default, length=20):
  show screen adventure_interaction
  $ result = renpy.input(prompt, default, length=length)
  return result
# </label get_editor_text_inner>

# <screen>
screen adventure_editor():

    modal True

    # <python>
    python:
        icon_browse = False
        adventure.editor_width = int(126 * adventure.guiscale)
        adventure.editor_height = int(360 * adventure.guiscale)
        # adventure.editor_top = (config.screen_height - adventure.editor_height) // 2
        
        # <def>
        def guiscale(pix):
            return int(pix * adventure.guiscale)
        # </def>
        
        # <if>
        if adventure.roomName != adventure.lastRoom:
            # Initialize the new room:
            adventure.interactableId = 0
            adventure.lastRoom = adventure.roomName
        # </if>
        editor_x = adventure.editor_left
        # 20 if (adventure.editorPos == 0) else (config.screen_width - (adventure.editor_width + 20))
        adventure.debug_show_inactive = adventure.editorTool != ADVENTURE_EDITOR_TOOL_PLAY
    # </python>
    
    # ROOM/LOCATION AREA VISUAL ELEMENTS:

    $ adventure.visibleMode = "default" if adventure.editorTool == ADVENTURE_EDITOR_TOOL_PLAY else get_edit_tool_mode()
    # <if>
    if adventure.editorTool != ADVENTURE_EDITOR_TOOL_PLAY and not adventure.dragging:
        # <for>
        for i in range(len(adventure.room)):
            # <if>
            if (i != adventure.interactableId):
                $ this_active = adventure_check_condition(adventure.room[i]["condition"])
                add AlphaPolygon(adventure.room[i]["points"], (0, 0, 255, 128) if this_active else (64, 64, 64, 128), cacheId=str(i)+("a" if this_active else ""))
                add PolyLine(    adventure.room[i]["points"], "#0000ff" if this_active else "#666666", 2, cacheId=str(i)+("La" if this_active else "L"))
                $ center_x, center_y = adventure_get_polygon_weighted_center(adventure.room[i]["points"])
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
        if len(adventure.room) > 0 and len(adventure.room[adventure.interactableId]["points"]) >= 1:
            $ this_interactable = adventure.room[adventure.interactableId]
            # <if>
            if this_interactable["type"] == "polygon":
                $ this_active = adventure_check_condition(this_interactable["condition"])
                $ current_polygon = AlphaPolygon(this_interactable["points"], (255, 0, 0, 128) if this_active else (128, 0, 0, 128), cacheId=str(adventure.interactableId)+"fa" if this_active else "f")
                # show expression current_polygon as curent_poly
                add current_polygon
                $ this_line = PolyLine(this_interactable["points"], "#ff0000" if this_active else "#996666", 3, cacheId=str(adventure.interactableId)+("Lfa" if this_active else "Lf"))
                add this_line
            # </if polygon>
            if this_interactable["type"] == "icon" and adventure.editorTool == ADVENTURE_EDITOR_TOOL_SELECT:
                # <for>
                $ found_icon = False
                for icon in adventure.screen_icons:
                    # <if>
                    if icon["interactableId"] == adventure.interactableId:
                        # <python>
                        python:
                            found_icon = True
                            outline = []
                            outline.append((icon["position"][0] - 3 - icon["size"][0]//2, icon["position"][1] - 3 - icon["size"][1]//2))
                            outline.append((icon["position"][0] + 3 + icon["size"][0]//2, icon["position"][1] - 3 - icon["size"][1]//2))
                            outline.append((icon["position"][0] + 3 + icon["size"][0]//2, icon["position"][1] + 3 + icon["size"][1]//2))
                            outline.append((icon["position"][0] - 3 - icon["size"][0]//2, icon["position"][1] + 3 + icon["size"][1]//2))
                        # </python>
                        add PolyLine(outline, "#ffff00", 3)
                    # </if>
                # </for>
                # <if>
                if not found_icon and len(this_interactable["points"]) > 0:
                    $ this_point = this_interactable["points"][0]
                    add Circle(10, (255, 255, 0), 3) xpos this_point[0] ypos this_point[1] xanchor 0.5 yanchor 0.5
                # </if>
            # </if icon>
        # </if>
        
        # <if>
        if adventure.editorTool == ADVENTURE_EDITOR_TOOL_EDIT and adventure.interactableId < len(adventure.room) and adventure.pointId < len(adventure.room[adventure.interactableId]["points"]):
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
            $ rad = 10 if adventure.room[adventure.interactableId]["type"] == "polygon" else 40
            $ color = (255, 255, 255) if rad == 3 else (255, 255, 0)
            add Circle(rad, color, 3) xpos this_point[0] ypos this_point[1] xanchor 0.5 yanchor 0.5
        # </if>
    # </if>
    
    # EDITOR GUI ELEMENTS:

    # <if>
    if not adventure.editor_hidden:
        # <frame>
        frame:
            background Frame(Solid("#FFFFFF"), guiscale(2), guiscale(2), tile=False)
            xpos editor_x - guiscale(5)
            ypos adventure.editor_top
            xsize (adventure.editor_width + guiscale(10))
            ysize (adventure.editor_height + guiscale(4))
            padding (guiscale(2), guiscale(2))

            # <vbox>
            vbox:
                # Title bar with background
                add AdventureMouseDragHandle(
                    adventure.editor_width + guiscale(6),
                    guiscale(20),
                    Fixed(
                        adventure_create_gradient(adventure.editor_width + guiscale(6), guiscale(20), "#00FFBB", "#006633", "vertical"),
                        Text("Location Editor", size=int(11 * adventure.guiscale), bold=True, color="#FFFFFF", xalign=0.5, yalign=0.5)
                    ),
                    adventure_begin_drag_editor,
                    tooltip="Drag to Position Editor"
                )

                # <if>
                # if adventure.editorPos == 0:
                #     text "Location Editor ▷" size (11 * adventure.guiscale) bold True color "#FFFFFF" xalign 0.5 yalign 0.5
                # else:
                #     text "◁ Location Editor" size (11 * adventure.guiscale) bold True color "#FFFFFF" xalign 0.5 yalign 0.5
                # </if>

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
                            spacing guiscale(2)  # Space between icons
                            xpos guiscale(2)    # Position from left edge
                            ypos guiscale(2)    # Position from top edge
                            ysize guiscale(60)
                            #yfill True

                            # <button>
                            button:
                                action Function(set_play_mode)
                                tooltip "Play Test Mode"
                                background (Solid("#ccffee") if adventure.editorTool == ADVENTURE_EDITOR_TOOL_PLAY else Solid("#cccccc"))
                                hover_background Solid("#ffffff")
                                xysize (guiscale(24), guiscale(24))  # Size of the button
                                padding (0, 0)   # Internal padding
                                
                                # <add>
                                add (adventure.editor_icons + "/editor-play.png"):
                                    fit "contain"
                                    xalign 0.5
                                    yalign 0.5
                                # </add>
                            # </button>
                            # <button>
                            button:
                                action Function(set_select_mode)
                                tooltip "Select Polygons or Icons"
                                background (Solid("#ccffee") if adventure.editorTool == ADVENTURE_EDITOR_TOOL_SELECT else Solid("#cccccc"))
                                hover_background Solid("#ffffff")
                                xysize (guiscale(24), guiscale(24))  # Size of the button
                                padding (0, 0)   # Internal padding
                                
                                # <add>
                                add (adventure.editor_icons + "/editor-select.png"):
                                    fit "contain"
                                    xalign 0.5
                                    yalign 0.5
                                # </add>
                            # </button>
                            # <button>
                            button:
                                action Function(set_pointedit_mode)
                                tooltip "Edit Points or Position"
                                background (Solid("#ccffee") if adventure.editorTool == ADVENTURE_EDITOR_TOOL_EDIT else Solid("#cccccc"))
                                hover_background Solid("#ffffff")
                                xysize (guiscale(24), guiscale(24))
                                padding (0, 0)
                                
                                # <add>
                                add (adventure.editor_icons + "/editor-edit-point.png"):
                                    fit "contain"
                                    xalign 0.5
                                    yalign 0.5
                                # </add>
                            # </button>
                            # <button>
                            button:
                                action Function(adventure_create_new_icon)
                                tooltip "Create New Interaction Icon"
                                background Solid("#cccccc")
                                hover_background Solid("#ffffff")
                                xysize (guiscale(24), guiscale(24))
                                padding (0, 0)
                                
                                # <add>
                                add (adventure.editor_icons + "/editor-new-icon.png"):
                                    fit "contain"
                                    xalign 0.5
                                    yalign 0.5
                                # </add>
                            # </button>
                            # <button>
                            button:
                                action Function(adventure_create_new_polygon)
                                tooltip "Create New Polygon"
                                background Solid("#cccccc")
                                hover_background Solid("#ffffff")
                                xysize (guiscale(24), guiscale(24))
                                padding (0, 0)
                                
                                # <add>
                                add (adventure.editor_icons + "/editor-new-polygon.png"):
                                    fit "contain"
                                    xalign 0.5
                                    yalign 0.5
                                # </add>
                            # </button>
                        # </hbox>
                        # <if>
                        if adventure.editorTool != ADVENTURE_EDITOR_TOOL_PLAY and len(adventure.room) > 0:
                            # <button>
                            button:
                                background adventure_create_gradient(adventure.editor_width + guiscale(6), guiscale(20), "#330000", "#660000", "vertical")
                                hover_background adventure_create_gradient(adventure.editor_width + guiscale(6), guiscale(20), "#660000", "#990000", "vertical")
                                action Function(get_interactable_tag)
                                tooltip "Set Object Tag"
                                xfill True
                                ysize guiscale(20)

                                $ cur_interactabletag = adventure_escape_renpy(adventure.room[adventure.interactableId]["tag"])
                                # <if>
                                if cur_interactabletag == "":
                                    text "[[untagged]" size (12 * adventure.guiscale) bold True color "#999999" xpos (adventure.editor_width // 2) xanchor 0.5 ypos 0
                                else:
                                    text cur_interactabletag size (12 * adventure.guiscale) bold False color "#FFFFFF" xpos ((adventure.editor_width // 2) - guiscale(2)) xanchor 0.5 ypos 0
                                # </if>
                            # </button>
                        else:
                            # <button>
                            button:
                                action NullAction()
                                background None  # Transparent
                                xfill True
                                ysize guiscale(20)
                            # </button>
                        # </if>

                        # <button>
                        button:
                            action NullAction()
                            background None  # Transparent
                            xfill True
                            ysize guiscale(30)
                        # </button>
                        # <if>
                        if get_interactable_type() == "polygon":
                            # <if>
                            if adventure.editorTool == ADVENTURE_EDITOR_TOOL_EDIT:
                                # <hbox>
                                # Tool icons section - horizontal layout
                                hbox:
                                    spacing guiscale(2)  # Space between icons
                                    xpos guiscale(2)    # Position from left edge
                                    ypos guiscale(2)    # Position from top edge
                                    # <button>
                                    button:
                                        action Function(set_pointmode)
                                        tooltip "New Point After"
                                        background (Solid("#ff3333") if adventure.pointMode == ADVENTURE_EDITOR_POINT_ADD else Solid("#cccccc"))
                                        hover_background (Solid("#ffcc33") if adventure.pointMode == ADVENTURE_EDITOR_POINT_ADD else Solid("#ffffff"))
                                        xysize (guiscale(24), guiscale(24))  # Size of the button
                                        padding (0, 0)   # Internal padding
                                        
                                        # <add>
                                        add (adventure.editor_icons + "/editor-new-point.png"):
                                            fit "contain"
                                            xalign 0.5
                                            yalign 0.5
                                        # </add>
                                    # </button>
                                    # <button>
                                    button:
                                        action Function(adventure_delete_point)
                                        tooltip "Delete This Point"
                                        background Solid("#cccccc")
                                        hover_background Solid("#ffffff")
                                        xysize (guiscale(24), guiscale(24))  # Size of the button
                                        padding (0, 0)   # Internal padding
                                        
                                        # <add>
                                        add (adventure.editor_icons + "/editor-delete-point.png"):
                                            fit "contain"
                                            xalign 0.5
                                            yalign 0.5
                                        # </add>
                                    # </button>
                                    # <button>
                                    button:
                                        action NullAction()
                                        background Solid("#666666")  # Transparent
                                        ysize guiscale(24)+1
                                        xsize (adventure.editor_width - (guiscale(24) + guiscale(1))*3) - guiscale(1)
                                    # </button>
                                    # <button>
                                    button:
                                        action Function(delete_interactable)
                                        tooltip "Delete This Polygon"
                                        background Solid("#cccccc")
                                        hover_background Solid("#ffffff")
                                        xysize (guiscale(24), guiscale(24))
                                        padding (0, 0)
                                        
                                        # <add>
                                        add (adventure.editor_icons + "/editor-delete-polygon.png"):
                                            fit "contain"
                                            xalign 0.5
                                            yalign 0.5
                                        # </add>
                                    # </button>
                                # </hbox>
                            # </if editorTool ADVENTURE_EDITOR_TOOL_EDIT>
                        # </if polygon>
                        # <if>
                        if (
                            (get_interactable_type() == "icon" and adventure.editorTool != ADVENTURE_EDITOR_TOOL_PLAY)
                            or
                            (get_interactable_type() == "polygon" and adventure.editorTool == ADVENTURE_EDITOR_TOOL_SELECT)
                        ):
                            $ vtype = "Icons" if get_interactable_type() == "icon" else "Verb"

                            # <hbox>
                            hbox:
                                spacing guiscale(2)  # Space between icons
                                xpos guiscale(2)    # Position from left edge
                                ypos guiscale(2)    # Position from top edge
                                
                                # TOOL SEQUENCE
                                
                                # <button>
                                button:
                                    action Function(toggle_ex_icon)
                                    background Solid("#333333")
                                    hover_background Solid("#999999")
                                    xysize (guiscale(24), guiscale(24))
                                    padding (0, 0)
                                    # <add>
                                    add (adventure.editor_icons + "/editor-" + ("un" if adventure_field_value("ex") == "" else "") + "checked.png"):
                                        fit "contain"
                                        xalign 0.5
                                        yalign 0.5
                                    # </add>
                                # </button>

                                # <button>
                                button:
                                    action Function(toggle_say_icon)
                                    background Solid("#333333")
                                    hover_background Solid("#999999")
                                    xysize (guiscale(24), guiscale(24))
                                    padding (0, 0)
                                    # <add>
                                    add (adventure.editor_icons + "/editor-" + ("un" if adventure_field_value("say") == "" else "") + "checked.png"):
                                        fit "contain"
                                        xalign 0.5
                                        yalign 0.5
                                    # </add>
                                # </button>

                                # <button>
                                button:
                                    action Function(toggle_op_icon)
                                    background Solid("#333333")
                                    hover_background Solid("#999999")
                                    xysize (guiscale(24), guiscale(24))
                                    padding (0, 0)
                                    # <add>
                                    add (adventure.editor_icons + "/editor-" + ("un" if adventure_field_value("op") == "" else "") + "checked.png"):
                                        fit "contain"
                                        xalign 0.5
                                        yalign 0.5
                                    # </add>
                                # </button>

                                # <button>
                                button:
                                    action Function(toggle_go_icon)
                                    background Solid("#333333")
                                    hover_background Solid("#999999")
                                    xysize (guiscale(24), guiscale(24))
                                    padding (0, 0)
                                    # <add>
                                    add (adventure.editor_icons + "/editor-" + ("un" if adventure_field_value("go") == "" else "") + "checked.png"):
                                        fit "contain"
                                        xalign 0.5
                                        yalign 0.5
                                    # </add>
                                # </button>

                                # <button>
                                button:
                                    action NullAction()
                                    background Solid("#333333")
                                    hover_background Solid("#333333")
                                    xysize (guiscale(24), guiscale(24))
                                    padding (0, 0)
                                    # <add>
                                    add (adventure.editor_icons + "/editor-" + ("un" if adventure_field_value("condition") == "" else "") + "checked.png"):
                                        fit "contain"
                                        xalign 0.5
                                        yalign 0.5
                                    # </add>
                                # </button>
                            # </hbox>

                            # <hbox>
                            hbox:
                                spacing guiscale(2)  # Space between icons
                                xpos guiscale(2)    # Position from left edge
                                ypos guiscale(2)    # Position from top edge
                                
                                # TOOL SEQUENCE

                                # <button>
                                button:
                                    action Function(change_ex_icon)
                                    tooltip ("Examine Tool " + vtype)
                                    background (Solid("#ccffee") if adventure.editorLayer == ADVENTURE_EDITOR_LAYER_EX else Solid("#cccccc"))
                                    hover_background Solid("#ffffff")
                                    xysize (guiscale(24), guiscale(24))
                                    padding (0, 0)
                                    # <add>
                                    add (adventure.editor_icons + "/editor-mode-ex.png"):
                                        fit "contain"
                                        xalign 0.5
                                        yalign 0.5
                                    # </add>
                                # </button>

                                # <button>
                                button:
                                    action Function(change_say_icon)
                                    tooltip ("Say Tool " + vtype)
                                    background (Solid("#ccffee") if adventure.editorLayer == ADVENTURE_EDITOR_LAYER_SAY else Solid("#cccccc"))
                                    hover_background Solid("#ffffff")
                                    xysize (guiscale(24), guiscale(24))
                                    padding (0, 0)
                                    # <add>
                                    add (adventure.editor_icons + "/editor-mode-say.png"):
                                        fit "contain"
                                        xalign 0.5
                                        yalign 0.5
                                    # </add>
                                # </button>

                                # <button>
                                button:
                                    action Function(change_op_icon)
                                    tooltip ("Operate Tool " + vtype)
                                    background (Solid("#ccffee") if adventure.editorLayer == ADVENTURE_EDITOR_LAYER_OP else Solid("#cccccc"))
                                    hover_background Solid("#ffffff")
                                    xysize (guiscale(24), guiscale(24))
                                    padding (0, 0)
                                    # <add>
                                    add (adventure.editor_icons + "/editor-mode-op.png"):
                                        fit "contain"
                                        xalign 0.5
                                        yalign 0.5
                                    # </add>
                                # </button>

                                # <button>
                                button:
                                    action Function(change_go_icon)
                                    tooltip ("Go Tool " + vtype)
                                    background (Solid("#ccffee") if adventure.editorLayer == ADVENTURE_EDITOR_LAYER_GO else Solid("#cccccc"))
                                    hover_background Solid("#ffffff")
                                    xysize (guiscale(24), guiscale(24))
                                    padding (0, 0)
                                    # <add>
                                    add (adventure.editor_icons + "/editor-mode-go.png"):
                                        fit "contain"
                                        xalign 0.5
                                        yalign 0.5
                                    # </add>
                                # </button>

                                # <if>
                                if adventure.editorTool == ADVENTURE_EDITOR_TOOL_EDIT:
                                    # <button>
                                    button:
                                        action Function(delete_interactable)
                                        tooltip "Delete This Icon"
                                        background Solid("#cccccc")
                                        hover_background Solid("#ffffff")
                                        xysize (guiscale(24), guiscale(24))
                                        padding (0, 0)
                                        # <add>
                                        add (adventure.editor_icons + "/editor-delete-icon.png"):
                                            fit "contain"
                                            xalign 0.5
                                            yalign 0.5
                                        # </add>
                                    # </button>
                                else:
                                    # <button>
                                    button:
                                        action Function(change_condition)
                                        tooltip ("Condition")
                                        background (Solid("#ccffee") if adventure.editorLayer == ADVENTURE_EDITOR_LAYER_COND else Solid("#cccccc"))
                                        hover_background Solid("#ffffff")
                                        xysize (guiscale(24), guiscale(24))
                                        padding (0, 0)
                                        # <add>
                                        add (adventure.editor_icons + "/editor-mode-condition.png"):
                                            fit "contain"
                                            xalign 0.5
                                            yalign 0.5
                                        # </add>
                                    # </button>
                                # </if>
                            # </hbox>

                            # <button>
                            button:
                                ypos 4
                                ysize 8
                                xsize (adventure.editor_width)
                            # </button>

                            # <if>
                            if adventure.editorTool == ADVENTURE_EDITOR_TOOL_SELECT and ((vtype == "Verb") or
                            (vtype == "Icons" and adventure.editorLayer == ADVENTURE_EDITOR_LAYER_COND)):
                                # <button>
                                button:
                                    background adventure_create_gradient(adventure.editor_width + guiscale(6), adventure.guiscale * 20, "#330000", "#660000", "vertical")
                                    hover_background adventure_create_gradient(adventure.editor_width + guiscale(6), adventure.guiscale * 20, "#660000", "#990000", "vertical")
                                    action Function(get_interactable_verb)
                                    tooltip ("Set Condition" if adventure.editorLayer == ADVENTURE_EDITOR_LAYER_COND else "Set Verb")
                                    xfill True
                                    ysize guiscale(20)

                                    $ cur_verb = adventure_escape_renpy(adventure.room[adventure.interactableId][get_edit_tool_mode()])
                                    text cur_verb size (adventure.guiscale * 12) bold False color "#FFFFFF" xpos ((adventure.editor_width // 2) - guiscale(2)) xanchor 0.5 ypos 0
                                # </button>
                            else:
                                # <if>
                                if adventure.editorTool in [ADVENTURE_EDITOR_TOOL_SELECT, ADVENTURE_EDITOR_TOOL_EDIT] and vtype == "Icons" and adventure.editorLayer != ADVENTURE_EDITOR_LAYER_COND:
                                    python:
                                        icon_browse = True
                                        base_list = { "none": ("verb-none.png", "none") }
                                        base_list.update(adventure.verb_icons[get_edit_tool_mode()])
                                        chunked_list = adventure_chunk_dict(base_list, 3)
                                        sel_value = adventure_field_value(get_edit_tool_mode())
                                        sel_verb = adventure.room[adventure.interactableId][get_edit_tool_mode()]
                                        # <if>
                                        if sel_value == "":
                                            sel_value = "none"
                                        # </if>
                                    # <for>
                                    for minilist in chunked_list:
                                        # <hbox>
                                        hbox:
                                            spacing guiscale(3)  # Space between icons
                                            xpos guiscale(3)    # Position from left edge
                                            ypos 0    # Position from top edge
                                            ysize guiscale(43)
                                            # <for>
                                            for iconname in minilist:
                                                # <python>
                                                python:
                                                    # <try>
                                                    try:
                                                        verb = base_list[iconname][1]
                                                        this_selected = sel_value == iconname
                                                    except:
                                                        this_selected = False
                                                    # </try>
                                                # </python
                                                # <button>
                                                button:
                                                    action Function(adventure_set_verb, get_edit_tool_mode(), iconname if iconname != "none" else "")
                                                    tooltip (verb.replace(";", " / "))
                                                    background (Solid("#ccffee") if this_selected else Solid("#666666"))
                                                    hover_background (Solid("#ccff99") if this_selected else Solid("#999999"))
                                                    xysize (guiscale(40), guiscale(40))
                                                    padding (0, 0)
                                                    # <add>
                                                    add (adventure_icon(base_list[iconname][0])):
                                                        fit "contain"
                                                        xalign 0.5
                                                        yalign 0.5
                                                    # </add>
                                                # </button>
                                            # </for>
                                        # </hbox>
                                    # </for chunked list>
                                # </if>

                                # <button>
                                button:
                                    action NullAction()
                                    background None  # Transparent
                                    xfill True
                                    ysize 20
                                # </button>
                            # </if>


                        # </if icon>
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

        $ interactable_type = get_interactable_type()

        # <if>
        if adventure.modalFreeze == 0 and adventure.editorTool != ADVENTURE_EDITOR_TOOL_PLAY:
            # <textbutton>
            textbutton "◂◂":
                action Function(priorInteractable)
                tooltip "Select Prior Interactable"
                text_size (adventure.guiscale * 12)
                xpos editor_x
                text_color "#999999"
                text_hover_color "#99ffee"
                background Solid("#000000")
                hover_background Solid("#333333")
                ypos (adventure.editor_top + guiscale(55))
            # </textbutton>
            # <textbutton>
            textbutton "▸▸":
                action Function(nextInteractable)
                tooltip "Select Next Interactable"
                text_size (adventure.guiscale * 12)
                xpos (editor_x + adventure.editor_width)
                xanchor 1.0
                text_color "#999999"
                text_hover_color "#99ffee"
                background Solid("#000000")
                hover_background Solid("#333333")
                ypos (adventure.editor_top + guiscale(55))
            # </textbutton>
            # <if>
            if adventure.editorTool == ADVENTURE_EDITOR_TOOL_EDIT and interactable_type == "polygon":
                # <textbutton>
                textbutton "◂◂":
                    action Function(adventure_prior_point)
                    tooltip "Select Prior Point"
                    text_size (adventure.guiscale * 12)
                    xpos editor_x
                    text_color "#999999"
                    text_hover_color "#99ffee"
                    background Solid("#000000")
                    hover_background Solid("#333333")
                    ypos (adventure.editor_top + guiscale(164))
                # </textbutton>
                # <textbutton>
                textbutton "▸▸":
                    action Function(adventure_next_point)
                    tooltip "Select Next Point"
                    text_size (adventure.guiscale * 12)
                    xpos (editor_x + adventure.editor_width)
                    xanchor 1.0
                    text_color "#999999"
                    text_hover_color "#99ffee"
                    background Solid("#000000")
                    hover_background Solid("#333333")
                    ypos (adventure.editor_top + guiscale(164))
                # </textbutton>
            # </if point editor>

        # </if not modalFreeze>

        # <if>
        if adventure.editorTool != ADVENTURE_EDITOR_TOOL_PLAY:
            text ("#" + str(adventure.interactableId + 1) + " (" + interactable_type_text(interactable_type) + ")" ) size (adventure.guiscale * 15) xpos (editor_x + adventure.editor_width // 2) xanchor 0.5 ypos (adventure.editor_top + guiscale(58)) color "#00cc66"
            $ mode_text = adventure_get_mode_text(adventure.editorTool)
            text mode_text size (adventure.guiscale * 12) xpos (editor_x + adventure.editor_width // 2) xanchor 0.5 ypos (adventure.editor_top + guiscale(110)) color "#999999"
        # </if>

        # <if>
        if adventure.editorTool == ADVENTURE_EDITOR_TOOL_EDIT and interactable_type == "polygon":
            text ("Pt. " + str(adventure.pointId + 1)) size (adventure.guiscale * 15) xpos (editor_x + adventure.editor_width // 2) xanchor 0.5 ypos (adventure.editor_top + guiscale(168)) color "#00cc66"
        # </if>

        # <if>
        if not icon_browse:
            # <text>
            text "Room:":
                ypos (adventure.editor_top + adventure.editor_height - guiscale(70))
                xpos (editor_x + adventure.editor_width // 2)
                xanchor 0.5
                yanchor 0
                bold True
                size (adventure.guiscale * 14)
            # </text>
            # <text>
            text "[adventure.roomName]":
                ypos (adventure.editor_top + adventure.editor_height - guiscale(70 - 18))
                xpos (editor_x + adventure.editor_width // 2)
                xanchor 0.5
                yanchor 0
                size (adventure.guiscale * 14)
            # </text>
            # <button>
        # </if>

        # <if>
        if adventure.editorTool == ADVENTURE_EDITOR_TOOL_PLAY:
            # <textbutton>
            textbutton "Hide Editor":
                action Function(adventure_hide_editor)
                tooltip "Temporarily Hide the Editor GUI"
                text_size (adventure.guiscale * 12)
                xpos (editor_x + adventure.editor_width // 2)
                xanchor 0.5
                yanchor 1
                ypos int(adventure.editor_top + adventure.editor_height - guiscale(95))
            # </textbutton>
        # </if>

        # <textbutton>
        textbutton "Save Changes":
            action Function(export_room_data_readable)
            tooltip "Permanently Save Room Data"
            text_size (adventure.guiscale * 12)
            xpos (editor_x + adventure.editor_width // 2)
            xanchor 0.5
            yanchor 1
            ypos int(adventure.editor_top + adventure.editor_height - guiscale(25))
        # </textbutton>
    # </if not_hidden>
# </screen adventure_editor>


# </init>
init 900 python:

    # <def>
    def adventure_icon_setup_continue():
        cand = os.path.join(renpy.config.gamedir, "gui/window_icon_candidate.png")
        existing = os.path.join(renpy.config.gamedir, "gui/window_icon.png")
        #  prompt for icon replace
        selected_index = renpy.call_in_new_context("adventure_icon_prompt",
            "Development Mode:  Install new icon in project?",
            ((adventure_get_relative_path(existing), "Keep Current Icon"),
            (adventure_get_relative_path(cand), "Install New Icon")),
#            iconpadding=120, labelpadding=10, labelheight=20, iconwidth=128
        )
        
        # <if>
        if selected_index > 0:
            adventure_compare_install_icons(os.path.join(renpy.config.gamedir, adventure.game_icon), True)
        else:
            renpy.call_screen("adventure_alert_box", """
{size=-4}To prevent this prompt from appearing again, you must add one of the following to the init python section of your script.rpy file:{/size}

adventure.game_icon = "images/your_icon.png"
{size=-8}{i}(replace your_icon with the filename of the icon to install){/i}{/size}

{size=-8}-or-{/size}

adventure.generate_icons = False
""", Return(True))
        # </if>
    # </def>

    # <def>
    def adventure_icon_setup():
        # <if>
        if adventure.generate_icons:
            # <if>
            if not adventure_compare_install_icons(os.path.join(renpy.config.gamedir, adventure.game_icon)):
                adventure.prompt_icons = True
            # </if>
        # </if>
    # </def>
    
    adventure_icon_setup()

# </init>
