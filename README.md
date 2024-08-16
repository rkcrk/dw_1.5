\_Standalone Guide Document
# **Finding a debugger to find a bug in a Z layering code! (Line 479 in parser.py)**
While deleting the image/decal from the memory and the level, the decal is STILL in the `zlayerimage`. In the current (& the meantime!) I an unable to figure this bug out.


# **Display Flags**
There are 6 flags – I, H, L, X, T and S. None of them are affecting the exporting file.

1. I stands for Image; it toggles the image displaying. Toggles by pressing 1 on keyboard.
1. H stands for Hitbox; it toggles the gray boxes displaying. Toggles by pressing 2 on keyboard.
1. L stands for Link; it toggles the linking boxes displaying. Toggles by pressing 3 on keyboard.
1. X stands for teXt; it toggles the text displaying. Toggles by pressing 4 on keyboard.
1. T stands for Trigger; it toggles the trigger boxes displaying. Toggles by pressing 5 on keyboard.
1. S stands for Special; it toggles the sources for the images displaying. Toggles by pressing 0 on keyboard.

# **Script API**
The API for the current version (1.1 \_Standalone, 1.5 Dwarf) is a bit of incomplete. But the current variables available right now are

- `playerpos`  – player position in level
- `playervel`  – player velocity in level
- `platf`  – platforms in the level

The current functions are

- `init`  – executed once at the initialization of the level
- `tick`  – executed 60 times per frame
- `trigger(id)`  – executed 60 times per frame if the player position is in the trigger area

Functions and variables should be backwards compatible w/ each other. Scripts MUST use the  pygame  modules.
# **Snap**
Snap is a feature that allows to place aligned by X and Y positions. You can resize snap grid using Q and E keys on the keyboard.
