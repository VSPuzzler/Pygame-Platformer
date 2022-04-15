from games import Game
import pygame
import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

g = Game()
while g.running:
    g.curr_menu.display_menu()
    start = time.time()
    pygame.mixer.music.stop()
    g.game_loop()
