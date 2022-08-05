import pygame
import vars
vars.NUM_COLS = 5
vars.NUM_ROWS = 30
import tetris_game as tt
from tetris_game import start_game
tt.HORIZON = 1
tt.FALL_SPEED =2
tt.GAME_MODE = 2
tt.init_board ="11110011111100000011"
tt.J = 1
cus_arr = ["1010", "1110", "0000", "0000"]
tt.shapes.append(cus_arr)
tt.shape.append([cus_arr, tt.rotate(cus_arr), tt.rotate(tt.rotate(cus_arr)), tt.rotate(tt.rotate(tt.rotate(cus_arr)))])

tt.FALL_SPEED =9
tt.HORIZON = 0


start_game()
