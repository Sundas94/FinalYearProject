import pyglet
from time import *

BOARD_WIDTH = 20
BOARD_HEIGHT = 30


# help from online 
def convert_hashColor_to_RGBA(color):
    if '#' in color:
        c = color.lstrip("#")
        c = max(6-len(c),0)*"0" + c
        r = int(c[:2], 16)
        g = int(c[2:4], 16)
        b = int(c[4:], 16)
        color = (r,g,b,255)
    return color

# generates a background image for the intro screen 
class BckGrndImg(pyglet.sprite.Sprite):
    def __init__(self, texture=None, width=BOARD_WIDTH, height=BOARD_HEIGHT, color='#000000', x=0, y=0):
        if texture is None:
            self.texture = pyglet.image.SolidColorImagePattern(convert_hashColor_to_RGBA(color)).create_image(width,height)
        else:
            self.texture = texture
        super(BckGrndImg, self).__init__(self.texture)

        self.image.anchor_x = self.image.width 
        self.image.anchor_y = self.image.height

        # set the position
        # position should be middle of screen not bottom
        self.x = x
        self.y = y

    def _draw(self):
        self.draw()

        
# inherits the background from BckGrndImg class 
class IntroScreen(BckGrndImg):
    def __init__(self, texture=None, width=300, height = 150, x = 10, y = 10, color='#000000'):
        super(IntroScreen, self).__init__(texture, width=width, height=height, x=x, y=y, color=color)

        self.intro_text = pyglet.text.Label('Starting Game', font_size=8, font_name=('Verdana',
                                                                                     'Calibri',
                                                                                     'Arial'),
                                            x=x, y=y, multiline=False, width=width, height=height,
                                            color=(100, 100, 100, 255), anchor_x='center')
        self.has_been_visible_since = time()

    # function that adds the functionality from pyglet library 
    def _draw(self): 
        self.draw()
        self.intro_text.draw()
        if time() - 2 > self.has_been_visible_since:
            self.intro_text.text = 'Tetris Game'
            
# should display 'main menu' after 'tetris game'
class MenuScreen(BckGrndImg):
    def __init__(self, texture=None, width=300, height = 150, x = 10, y = 10, color='#000000'):
        super(MenuScreen, self).__init__(texture, width=width, height=height, x=x, y=y, color=color)

        self.screen_text = pyglet.text.Label('Main menu screen', font_size=8, font_name=('Verdana',
                                                                                         'Calibri',
                                                                                         'Arial'),
                                             x=x, y=y+height/2-20, multiline=False, width=300, height=height,
                                             color=(100, 100, 100, 255), anchor_x='center')

    def _draw(self):
        self.draw()
        self.screen_text.draw()

class Window(pyglet.window.Window):
    def __init__(self, refreshrate):
        super(Window, self).__init__(vsync = False)
        self.alive = 1
        self.refreshrate = refreshrate

        self.currentScreen = IntroScreen(x=320, y=BOARD_HEIGHT/2, width=50) 
        self.screen_has_been_shown_since = time()

    def on_draw(self):
        self.render()


    def render(self):
        self.clear()
        
         # screen changes after 5 seconds
        if time() - 5 > self.screen_has_been_shown_since and type(self.currentScreen) is not MenuScreen:
            self.currentScreen = MenuScreen(x=320, y=BOARD_HEIGHT-210, color='#FF0000')

        self.currentScreen._draw() # draws the current screen
        self.flip()

    def on_close(self):
        self.alive = 0

    def run(self):
        while self.alive:
            self.render()
            event = self.dispatch_events()
            sleep(1.0/self.refreshrate)

win = Window(23) # set the fps
win.run()
