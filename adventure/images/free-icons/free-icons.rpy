# Geometry Configuration for this Adventure for Renpy Icon Set

# <init>
init python:
    import os
    filename, line_number = renpy.get_filename_line()
    relpath = os.path.dirname(filename)
    if relpath.startswith("game/"):
        relpath = relpath[5:]

    adventure.margins[relpath + "/toolbar-bg.png"] = {
       "left": 10, "top": 10, "right": 10, "bottom": 10
    }
    adventure.plugin_metrics[relpath] = {
        "toolbar_top_padding": 5,
        "toolbar_left_padding": 5,
        "toolbar_right_padding": 5,
        "toolbar_bottom_padding": 5,
        "toolbar_horizontal_spacing": 5,
        "toolbar_vertical_spacing": 5,
        "toolbar_inactive_button_offset": (0, 0),
        "toolbar_active_button_offset":  (0, 0),
        "toolbar_inactive_icon_offset": (0, 0),
        "toolbar_active_icon_offset":  (0, 0),
    }

# </init>
