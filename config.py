from sys import platform

if platform == "linux" or platform == "linux2":
    PLATFORM = 'linux'
elif platform == "darwin":
    PLATFORM = 'mac'
else:
    PLATFORM = 'windows'

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500

SCREEN_SIZE = f"{SCREEN_HEIGHT}x{SCREEN_WIDTH}+0+0"
FULL_SCREEN_MODE = True
TRANSPARENCY = 0.4
BACKGROUND_COLOR = 'systemTransparent'
MOUSE_ICON = '0.png'
PEN_WIDTH = 5

SCREENSHOT_PATH = '/Users/maksim/PycharmProjects/screenshot_creator/screenshots/'
SCREENSHOT_FORMAT = 'PNG'
