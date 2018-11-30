from PIL import ImageGrab
from PIL import Image 
from time import sleep 
import sys 
import json 
import requests 
import atexit 
import coreHue

# To make sure it works on high DPI displays
user32 = windll.user32
user32.SetProcessDPIAware() 

# Find the average color of a column
def get_avg_color(img, light_pos):
    width, height = img.size 

    pixel_count = 0

    r_total = 0
    g_total = 0
    b_total = 0

    x = light_pos

    for y in range(0, width):
        r, g, b = img.getpixel((x,y))
        r_total += r
        g_total += g 
        b_total += b 
        pixel_count += 1
    
    return (int(r_total/pixel_count), int(g_total/pixel_count), int(b_total/pixel_count))   


def on_exit(lights):
    for light in lights:
        coreHue.change_state('0', light) 


def main():
    lights = coreHue.get_available_lights()

    avg_color = [(0,0,0) for i in range(len(lights))]

    # Used to set how reactive the update should be
    threshold = 30
    
    # Turn all lights on
    for light in lights:
        coreHue.change_state('1', light)

    img = ImageGrab.grab()
    img = img.resize((len(lights), len(lights)))

    while(True):
        try:
            img = ImageGrab.grab()
            img = img.resize((len(lights), len(lights)))
        # If the computer is locked, etc
        except OSError:
            pass
        
        for i in range(len(lights)):
            old_avg = avg_color[i]
            r1, g1, b1 = old_avg
            avg_color[i] = get_avg_color(img, i)
            r2, g2, b2 = avg_color[i]

            # only update the lights 
            # if the color is different by +- threshold1
            if (abs(r2-r1) > threshold or abs(g2-g1) > threshold or abs(b2-b1) > threshold):
                coreHue.update_color(avg_color[i], lights[i])
                # print(avg_color[i])


atexit.register(on_exit, lights=coreHue.get_available_lights())

if __name__ == '__main__':
    main()
