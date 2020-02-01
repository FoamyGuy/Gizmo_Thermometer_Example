import board
import displayio
import terminalio
import time
from adafruit_display_text import label
from adafruit_gizmo import tft_gizmo
display = tft_gizmo.TFT_Gizmo()
from adafruit_circuitplayground import cp

# text scaling factor
TEXT_SCALE = 2

# previous iterature button value
old_a_val = cp.button_a

# boolean for current unit type
show_c_units = True

# function to convert celsius degrees to fahrenheit
def c_to_f(c_val):
   return (c_val * 9/5) + 32

# Open the background image file
with open("/temperature_background.bmp", "rb") as bitmap_file:

    # Setup the file as the bitmap data source
    bitmap = displayio.OnDiskBitmap(bitmap_file)

    # Create a TileGrid to hold the bitmap
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())

    # Create a Group to hold the TileGrid
    group = displayio.Group()

    # Add the TileGrid to the Group
    group.append(tile_grid)

    # variable with initial text value, temperature rounded to 2 places
    text = "%.2f C" % (round(cp.temperature, 2))

    # Create a Group for the text so we can scale it
    text_group = displayio.Group(max_size=1, scale=TEXT_SCALE, x=0, y=0)

    # Create a Label to show the initial temperature value
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)

    # Set the anchor_point for center,top
    text_area.anchor_point = (0.5, 0.0)

    # Set the location to center of display, accounting for text_scale
    text_area.anchored_position = (240/(2*TEXT_SCALE), 240/(2*TEXT_SCALE))

    # Subgroup for text scaling
    text_group.append(text_area)

    # Add the text_group to main Group
    group.append(text_group)

    # Add the main Group to the Display
    display.show(group)

    # Loop forever
    while True:
        cur_a_val = cp.button_a
        if cur_a_val and not old_a_val:
            print('Just released')
            # flip the units boolean to the opposite value
            show_c_units = not show_c_units
        if show_c_units:
            # Update the text
            text_area.text = "%.2f C" % (round(cp.temperature, 2))
        else: # show f units
            # Update the text
            text_area.text = "%.2f F" % (round(c_to_f(cp.temperature), 2))

        old_a_val = cur_a_val
        # Wait a little bit before next time
        time.sleep(0.05)