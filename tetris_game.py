import copy
from tracemalloc import start
import pygame
import random
import numpy as np
import vars
from vars import NUM_COLS as NUM_COLS
from vars import NUM_ROWS as NUM_ROWS
from vars import FALL_SPEED as FALL_SPEED
from vars import GAME_MODE as GAME_MODE
"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
HORIZON = 1

I = 0
J = 0
T = 0
L = 0
SQ = 0

SCORE = 0

MOVE_LEFT=pygame.K_LEFT
MOVE_RIGHT=pygame.K_RIGHT
ROT_C=pygame.K_UP
ROT_AC=pygame.K_DOWN


s_width = 1400
s_height = 750
global play_width  # meaning 300 // 10 = 30 width per block
global play_height  # meaning 600 // 20 = 20 height per blo ck
block_size = 20

global top_left_x
global top_left_y

play_width = 30 * NUM_COLS  # meaning 300 // 10 = 30 width per block
play_height = 30 * NUM_ROWS  # meaning 600 // 20 = 20 height per blo ck

top_left_x = (s_width - play_width) / 2
top_left_y = s_height - play_height - 50

shape = list()
shapes = list()
init_board = ""
pygame.font.init()


# class Game:
#     def __init__(self) -> None:
#         self.shape = list()
#         self.win = pygame.display.set_mode((s_width, s_height))
#         self.init_shapes()
#         self.shapes = [x for x in self.shape]

def initialize():
    change_params(NUM_ROWS, NUM_COLS)
    s_width = 100 * NUM_COLS
    s_height = 100 * NUM_ROWS
    play_width = 30 * NUM_COLS  # meaning 300 // 10 = 30 width per block
    play_height = 30 * NUM_ROWS  # meaning 600 // 20 = 20 height per blo ck
    block_size = 20

    top_left_x = (s_width - play_width) / 2
    top_left_y = s_height - play_height - 50

def init_shapes():
    shape_I = [["0010",
                "0010",
                "0010",
                "0010"],
               ["0000",
                "1111",
                "0000",
                "0000"]]

    shape_J = [["0000",
                "0100",
                "0111",
                "0000"],
               ["0000",
                "0011",
                "0010",
                "0010"],
               ["0000",
                "0000",
                "0111",
                "0001"],
               ["0000",
                "0010",
                "0010",
                "0110"]]

    shape_T = [["0000",
                "0010",
                "0111",
                "0000"],
               ["0000",
                "0010",
                "0011",
                "0010"],
               ["0000",
                "0000",
                "0111",
                "0010"],
               ["0000",
                "0010",
                "0110",
                "0010"]]

    shape_L = [["0000",
                "0001",
                "0111",
                "0000"],
               ["0000",
                "0010",
                "0010",
                "0011"],
               ["0000",
                "0000",
                "0111",
                "0100"],
               ["0000",
                "0110",
                "0010",
                "0010"]]

    shape_SQ = [["0000",
                 "0110",
                 "0110",
                 "0000"]]

    if (I == 1):
        shape.append(shape_I)
    if (J == 1):
        shape.append(shape_J)
    if (L == 1):
        shape.append(shape_L)
    if (T == 1):
        shape.append(shape_T)
    if (SQ == 1):
        shape.append(shape_SQ)


# shapes = [x for x in shape]

class Piece(object):
    row = 0
    column = 0

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = (129, 200, 128)
        self.rotation = 0  # number from 0-3


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for x in range(NUM_COLS)] for x in range(NUM_ROWS)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == "1":
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(NUM_COLS) if grid[i][j] == (0, 0, 0)] for i in range(NUM_ROWS)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    global shapes, shape_colors

    return Piece(int(NUM_COLS / 2), 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (
    top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))


def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (255, 255, 255), (sx, sy + i * 30),
                         (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (255, 255, 255), (sx + j * 30, sy),
                             (sx + j * 30, sy + play_height))  # vertical lines


def clear_rows(grid, locked):
    # need to see if row is clear the shift every other row above down one
    global SCORE
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            SCORE += 10*GAME_MODE
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)


def draw_next_shape(shape, surface):
    if (HORIZON == 1):

        font = pygame.font.SysFont("arial", 25)
        label = font.render("Next Shape", 1, (255, 255, 255))

        sx = top_left_x + play_width + 100
        sy = top_left_y + play_height / 2 - 100

        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == "1":
                    pygame.draw.rect(surface, shape.color, (sx + j * 30, sy + i * 30, 30, 30), 0)

        surface.blit(label, (sx + 10, sy - 30))
    else:
        return


def draw_window(surface):
    surface.fill((100, 0, 0))
    # Tetris Title
    font = pygame.font.SysFont("arial", 30)
    label = font.render(str(SCORE), 1, (255, 255, 255))
    surface.blit(label, (top_left_x - 50 - (label.get_width()), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)

    # draw grid and border
    draw_grid(surface, NUM_ROWS, NUM_COLS)
    pygame.draw.rect(surface, (255, 255, 255), (top_left_x, top_left_y, play_width, play_height), 5)
    # pygame.display.update()


def rotate(arr):
    ar1 = copy.deepcopy(arr)
    a = ""
    b = ""
    c = ""
    d = ""
    for i in arr:
        d = d + i[0]
        c = c + i[1]
        b = b + i[2]
        a = a + i[3]
    ar1 = [a, b, c, d]
    return ar1


def main():
    global grid

    locked_positions = {}  # (x,y):(255,0,0)
    
#     for i in range((len(init_board) % NUM_ROWS)):
#         init_board = init_board + '0'
#     init_board = init_board + ('0' * (len(init_board) % NUM_ROWS))

    lock_len = len(init_board)
    for i in range(lock_len):
        if init_board[i] == '1':
#             locked_positions[(2,2)] = (129,200,128)
            locked_positions[((i % NUM_COLS), (NUM_ROWS - (i // NUM_COLS) - 1))] = (129,200,128)
    
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        fall_speed = 1 - (FALL_SPEED / 10.0)

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # PIECE FALLING CODE
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == MOVE_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == MOVE_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == ROT_C:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                if event.key == ROT_AC:
                    # move shape down
                    current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                # if event.key == pygame.K_SPACE:
                #     while valid_space(current_piece, grid):
                #         current_piece.y += 1
                #     current_piece.y -= 1
                    # print(convert_shape_format(current_piece))"""  # todo fix

        shape_pos = convert_shape_format(current_piece)

        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            # call four times to check for multiple clear rows
            clear_rows(grid, locked_positions)

        draw_window(win)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        # Check if user lost
        if check_lost(locked_positions):
            run = False

    win.fill((0, 0, 0))
    draw_text_middle("You Lost", 25, (255, 255, 255), win)
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle("Press Any Key to Begin", 30, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


# ------------- Executable Commands ---------------------
def change_params(rows, cols):
    global NUM_ROWS, NUM_COLS
    NUM_ROWS = rows
    NUM_COLS = cols


def start_game():
    initialize()
    global win
    win = pygame.display.set_mode((s_width, s_height))
    # win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    init_shapes()
    global shapes
    shapes = [x for x in shape]
    pygame.display.set_caption("Tetris")
    main_menu()


if __name__ == "__main__":
    start_game()
