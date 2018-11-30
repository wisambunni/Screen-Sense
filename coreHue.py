import json 
import requests 

#TODO: Dynamically get the number of lights in a room
#TODO: Use Streaming API instead of HTTP (once it's out)
def get_available_lights():
    api_key = 'YOUR_KEY'
    ip_address = 'xxx.xxx.xx.xx'
    lights = [
        'http://%s/api/%s/lights/6/state/' % (ip_address, api_key),
        'http://%s/api/%s/lights/4/state/' % (ip_address, api_key),
        'http://%s/api/%s/lights/7/state/' % (ip_address, api_key),
        'http://%s/api/%s/lights/3/state'  % (ip_address, api_key),
        'http://%s/api/%s/lights/5/state/' % (ip_address, api_key)
    ]
    return lights 


def change_state(state, light):
    data = json.dumps({'on': True}) if state == '1' else json.dumps({'on': False})
    requests.put(light, data)


def update_brightness(brightness, light):
    data = json.dumps({'bri': brightness})
    requests.put(light, data)


def update_color(color, light):
    red, green, blue = color

    brightness = max([red, green, blue])

    # Apply gamma correction
    red = pow((red + 0.055) / (1.0 + 0.055), 2.4) if (red > 0.04045) else (red / 12.92)
    green = pow((green + 0.055) / (1.0 + 0.055), 2.4) if (green > 0.04045) else (green / 12.92)
    blue = pow((blue + 0.055) / (1.0 + 0.055), 2.4) if (blue > 0.04045) else (blue / 12.92)

    # Convert RGB to XYZ (Using Wide RGB D65 formula)
    X = red * 0.664511 + green * 0.154324 + blue * 0.162028 # Red parity
    Y = red * 0.283881 + green * 0.668433 + blue * 0.047685 # Green Parity
    Z = red * 0.000088 + green * 0.072310 + blue * 0.986039 # Blue parity

    # Convert XYZ to xy
    try:
        x = X / (X + Y + Z)
        y = Y / (X + Y + Z) 
    except ZeroDivisionError:
        return

    data = json.dumps({'xy': (x,y),
                       'bri': brightness
                      })
    requests.put(light, data)

 

