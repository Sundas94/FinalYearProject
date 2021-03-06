import random
import sys, thread, time, math
import os, inspect
import pyglet
from pyglet.window import key
from os import chdir
from time import *


src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import logging

from Leap import CircleGesture, SwipeGesture, ScreenTapGesture, KeyTapGesture


music = pyglet.resource.media('tetris.mp3')
music.play()

BLOCK_EMPTY = 0
BLOCK_FULL = 1
BLOCK_ACTIVE = 2


block = 'images/block.png'
yellow = 'images/yellow.png'
purple = 'images/purple.png'
orange = 'images/orange.png'
blue = 'images/blue.png'
red = 'images/red.png'
green = 'images/green.png'


list = [block, yellow, purple, orange, blue, red, green]
choice = random.choice(list)

BLOCK_IMG_FILE = choice


block = pyglet.image.load(BLOCK_IMG_FILE)

bckgrnd_image = pyglet.image.load('tetris.png')



BOARD_WIDTH = 30
BOARD_HEIGHT = 30
BLOCK_WIDTH = block.width
BLOCK_HEIGHT = block.height

window = pyglet.window.Window(width=BOARD_WIDTH*BLOCK_WIDTH,
                              height=BOARD_HEIGHT*BLOCK_HEIGHT)


class LeapMotionListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_connect(self, controller):
        logging.debug("Motion Sensor Connected!")

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);



    def on_disconnect(self, controller):
        logging.debug("Motion Sensor Disconnected")

    def on_frame(self, controller):
        frame = controller.frame()

        for gesture in frame.gestures():


            """
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)
                logging.debug("rotate")
                board.rotate_shape(rotate())
                print "Rotate"


            """

            #if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
             #   keytap = KeyTapGesture(gesture)
            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                screentap = ScreenTapGesture(gesture)
                game.toggle_pause()
                print "pause"
            elif gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                swipeDir = swipe.direction
                if (swipeDir.x > 0 and math.fabs(swipeDir.x) > math.fabs(swipeDir.y)):
                    logging.debug("Swiped Right")
                    board.move_right()
                    print "Right"
                elif (swipeDir.x < 0 and math.fabs(swipeDir.x) > math.fabs(swipeDir.y)):
                    logging.debug("Swiped Left")
                    board.move_left()
                    print "Left"
                elif (swipeDir.y < 0 and math.fabs(swipeDir.x) < math.fabs(swipeDir.y)):
                    logging.debug("Swiped Down")
                    board.move_down()
                    print "Swiped down"



    def main(self):
        listener = LeapMotionListener()
        controller = Leap.Controller()

        controller.add_listener(listener)

        print "Press enter to quit"

        try:
            sys.stdin.readline()
        except KeyboardInterrupt:
            pass
        finally:
            controller.remove_listener(listener)

        if __name__ == "__main__":
            main()


class Shape(object):

    _shapes = [
        [[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]],

        [[0, 0, 0, 0],
         [0, 1, 1, 0],
         [0, 1, 1, 0],
         [0, 0, 0, 0]],

        [[0, 0, 0, 0],
         [0, 0, 1, 0],
         [0, 0, 1, 0],
         [0, 1, 1, 0]],

        [[0, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 1, 0]],

        [[0, 0, 0, 0],
         [0, 0, 1, 0],
         [0, 1, 1, 0],
         [0, 1, 0, 0]],

        [[0, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 1, 0],
         [0, 0, 1, 0]],

        [[0, 0, 0, 0],
         [0, 1, 0, 0],
         [1, 1, 1, 0],
         [0, 0, 0, 0]]
    ]

    leap = LeapMotionListener()
    controller = Leap.Controller()
    controller.add_listener(leap)


    def __init__(self, x=0, y=0):
        self.shape = random.choice(self._shapes)
        self.shape = self.copy_shape()
        #board = Board()
        logging.basicConfig(filename='example.log', level=logging.DEBUG)
        logging.debug('This message should go to the log file')
        self.leap.on_frame(self.controller)
        for i in range(random.choice(range(4))):
            self.rotate()

        self.x, self.y = (x,y)

    def copy_shape(self):
        new_shape = []
        for row in self.shape:
            new_shape.append(row[:])
        return new_shape


    def copied(self):
        copied = Shape()
        copied.shape = self.copy_shape()
        copied.x = self.x
        copied.y = self.y
        return copied

    def rotate(self):
        new_shape = self.copy_shape()
        for j in range(0, 4):
            for i in range(0, 4):
                new_shape[i][j] = self.shape[4 - j - 1][i]
        self.shape = new_shape

    @property
    def left_edge(self):
        for x in range(0, 4):
            for y in range(0, 4):
                if self.shape[y][x] == BLOCK_FULL:
                    return x

    @property
    def right_edge(self):
        for x in range(3, -1, -1):
            for y in range(0, 4):
                if self.shape[y][x] == BLOCK_FULL:
                    return x

    @property
    def bottom_edge(self):
        for y in range(3, -1, -1):
            for x in range(0, 4):
                if self.shape[y][x] == BLOCK_FULL:
                    return y


class Board(pyglet.event.EventDispatcher):
    active_shape = None
    pending_shape = None
    board = None
    leap = None

    def __init__(self, width, height, block):
        self.width, self.height = width, height
        self.block = block
        self.calculated_height = self.height * BLOCK_HEIGHT
        self.calculated_width = self.width * BLOCK_WIDTH
        self.reset()

        #self.leap.__init__()

    def reset(self):
        self.board = []
        for row in range(self.height):
            self.board.append([0] * self.width)

        self.pending_shape = Shape()
        self.add_shape()

    def add_shape(self):
        self.active_shape = self.pending_shape.copied()
        self.active_shape.x = self.width // 2 - self.active_shape.left_edge
        self.active_shape.y = -1
        self.pending_shape = Shape()

        if self.is_collision():
            self.reset()
            self.dispatch_event('game_over')

    def rotate_shape(self):
        rotated_shape = self.active_shape.copied()
        rotated_shape.rotate()

        if rotated_shape.left_edge + rotated_shape.x < 0:
            rotated_shape.x = -rotated_shape.left_edge

        elif rotated_shape.right_edge + rotated_shape.x >= self.width:
            rotated_shape.x = self.width - rotated_shape.right_edge - 1

        if rotated_shape.bottom_edge + rotated_shape.y > self.height:
            return False

        if not self.is_collision(rotated_shape):
            self.active_shape = rotated_shape

    def move_left(self):
        self.active_shape.x -= 1
        if self.out_of_bounds() or self.is_collision():
            self.active_shape.x += 1
            return False
        return True

    def move_right(self):
        self.active_shape.x += 1
        if self.out_of_bounds() or self.is_collision():
            self.active_shape.x -= 1
            return False
        return True

    def move_down(self):
        self.active_shape.y += 1

        if self.check_bottom() or self.is_collision():
            self.active_shape.y -= 1
            self.shape_to_board()
            self.add_shape()
            return False
        return True

    def out_of_bounds(self, shape=None):
        shape = shape or self.active_shape
        if shape.x + shape.left_edge < 0:
            return True
        elif shape.x + shape.right_edge >= self.width:
            return True
        return False

    def check_bottom(self, shape=None):
        shape = shape or self.active_shape
        if shape.y + shape.bottom_edge >= self.height:
            return True
        return False

    def is_collision(self, shape=None):
        shape = shape or self.active_shape
        for y in range(4):
            for x in range(4):
                if y + shape.y < 0:
                    continue
                if shape.shape[y][x] and self.board[y + shape.y][x + shape.x]:
                    return True
        return False

    def test_for_line(self):
        for y in range(self.height - 1, -1, -1):
            counter = 0
            for x in range(self.width):
                if self.board[y][x] == BLOCK_FULL:
                    counter += 1
            if counter == self.width:
                self.process_line(y)
                return True
        return False

    def process_line(self, y_to_remove):
        for y in range(y_to_remove - 1, -1, -1):
            for x in range(self.width):
                self.board[y + 1][x] = self.board[y][x]

    def shape_to_board(self):
        for y in range(4):
            for x in range(4):
                dx = x + self.active_shape.x
                dy = y + self.active_shape.y
                if self.active_shape.shape[y][x] == BLOCK_FULL:
                    self.board[dy][dx] = BLOCK_FULL

        lines_found = 0
        while self.test_for_line():
            lines_found += 1

        if lines_found:
            self.dispatch_event('on_lines', lines_found)

    def move_piece(self, motion_state):
        if motion_state == key.MOTION_LEFT:
            self.move_left()
        elif motion_state == key.MOTION_RIGHT:
            self.move_right()
        elif motion_state == key.MOTION_UP:
            self.rotate_shape()
        elif motion_state == key.MOTION_DOWN:
            self.move_down()


    def draw_game_board(self):
        for y, row in enumerate(board.board):
            for x, col in enumerate(row):
                if col == BLOCK_FULL or col == BLOCK_ACTIVE:
                    self.draw_block(x, y)

        for y in range(4):
            for x in range(4):
                dx = x + self.active_shape.x
                dy = y + self.active_shape.y
                if self.active_shape.shape[y][x] == BLOCK_FULL:
                    self.draw_block(dx, dy)

    def draw_block(self, x, y):
        y += 1
        self.block.blit(x * BLOCK_WIDTH, self.calculated_height - y * BLOCK_HEIGHT)


Board.register_event_type('on_lines')
Board.register_event_type('game_over')

class rotateShape(Board):

    def check(self):

        rotated_shape = self.active_shape.copied()
        rotated_shape.rotate()

        if rotated_shape.left_edge + rotated_shape.x < 0:
            rotated_shape.x = -rotated_shape.left_edge

        elif rotated_shape.right_edge + rotated_shape.x >= self.width:
            rotated_shape.x = self.width - rotated_shape.right_edge - 1

        if rotated_shape.bottom_edge + rotated_shape.y > self.height:
            return False

        if not self.is_collision(rotated_shape):
            self.active_shape = rotated_shape


class moveLeft(Board):

    def check(self):

        self.active_shape.x -= 1
        if self.out_of_bounds() or self.is_collision():
            self.active_shape.x += 1
            return False
        return True

class moveRight(Board):

    def check(self):

        self.active_shape.x += 1
        if self.out_of_bounds() or self.is_collision():
            self.active_shape.x -= 1
            return False
        return True

class moveDown(Board):

    def check(self):

        self.active_shape.y += 1

        if self.check_bottom() or self.is_collision():
            self.active_shape.y -= 1
            self.shape_to_board()
            self.add_shape()
            return False
        return True



class Game(object):
    ticks = 0
    factor = 4
    frame_rate = 60.0

    pause = False

    def __init__(self, window_ref, board, starting_level=1):
        self.window_ref = window_ref
        self.board = board
        self.starting_level = int(starting_level)
        self.register_callbacks()
        self.reset()

    def register_callbacks(self):
        self.board.push_handlers(self)

    def reset(self):
        self.level = self.starting_level
        self.lines = 0
        self.score = 0

    def should_update(self):
        if self.pause:
            return False

        self.ticks += 1
        if self.ticks >= (self.frame_rate - (self.level * self.factor)):
            self.ticks = 0
            return True
        return False

    def draw_handler(self):
        self.window_ref.clear()
        self.board.draw_game_board()

    def keyboard_handler(self, motion):
        self.board.move_piece(motion)

    def on_lines(self, num_lines):
        self.score += (num_lines * self.level)
        self.lines += num_lines
        if self.lines / 10 > self.level:
            self.level = self.lines / 10

    def on_game_over(self):
        self.reset()

    def cycle(self):
        if self.should_update():
            self.board.move_down()
            self.update_caption()

    def toggle_pause(self):
       self.pause = not self.pause

    def update_caption(self):
        self.window_ref.set_caption('Tetris Game')


board = Board(BOARD_WIDTH, BOARD_HEIGHT, block)


if len(sys.argv) > 1:
    starting_level = int(sys.argv[1])
else:
    starting_level = 1

game = Game(window, board, starting_level)

@window.event
def on_draw():
    bckgrnd_image.blit(5, 5)

    game.draw_handler()

@window.event
def on_text_motion(motion):
    game.keyboard_handler(motion)

@window.event
def on_key_press(key_pressed, mod):
    if key_pressed == key.P:
        game.toggle_pause()

def update(dt):
    game.cycle()

pyglet.clock.schedule_interval(update, 1 / game.frame_rate)
pyglet.app.run()
