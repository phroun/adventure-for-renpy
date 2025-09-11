# The script of the game goes in this file.

init python:

    # Your Adventure for Ren'Py Configuration Options go here:
    
    adventure.toolbar_icons = ["ex", "say", "op", "go"]
    adventure.toolbar_position = "bottom"
    adventure.choice_position = "bottom"

    # Edit the following line to point to your game's icon, and uncomment it:
    # adventure.game_icon = "images/my-game-icon.png"


# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")


# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg room

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show eileen happy

    # These display lines of dialogue.

    e "You've created a new Adventure for Ren'Py game.  Good luck!"

    label .loop:
    call adventure_input("demo room")
    
    if player_chooses_to("exit"):
        jump game_end

    jump .loop

label game_end:

    # This ends the game.

    return
