from folder2048.classes import Grid
from folder2048.objects import *
from folder2048.constants import *
import pygame, sys
from pygame.locals import *
import os

# --------------------------- Setup pygame/window ------------------------------------- #
mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('2048')


class Game:
    def __init__(self, size):
        # parameters
        self.size = size  # for grid
        self.starting_tiles = 2
        self.score = 0

        # objects
        self.grid = Grid(size)
        self.initialize_grid()
        # self.grid.print_grid()
        # self.grid.swipe_left()
        # print()
        # self.grid.print_grid()

    def initialize_grid(self):
        self.grid.add_start_cells(self.starting_tiles)

    def main_menu(self):
        click = False
        while True:

            screen.fill((187, 173, 160))
            draw_text('main menu', screen, color=(0, 0, 0), x=20, y=20)

            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(50, 100, 200, 50)
            button_2 = pygame.Rect(50, 200, 200, 50)
            if button_1.collidepoint((mx, my)):
                if click:
                    self.game()
                    pygame.display.flip()
            if button_2.collidepoint((mx, my)):
                if click:
                    self.options()
                    pygame.display.flip()

            pygame.draw.rect(screen, (187, 173, 180), button_1)
            pygame.draw.rect(screen, (187, 173, 180), button_2)
            draw_text('game', screen, color=(255, 255, 255), x=button_1.x, y=button_1.y)
            draw_text('options', screen, color=(255, 255, 255), x=button_2.x, y=button_2.y)

            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # mouse 1
                        click = True

                    # if event.button == 3:  # mouse 2 if i want to do something with this
                    #     pass

            pygame.display.update()
            mainClock.tick(1)

    def options(self):
        running = True
        while running:
            screen.fill((0, 0, 0))

            draw_text('Hi there, I do nothing: esc to go back', screen, color=(255, 255, 255), x=0, y=20)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            pygame.display.update()
            mainClock.tick(60)

    def fadein(self):
        fade = pygame.Surface(SCREENSIZE)
        fade.fill((187, 173, 160))  # color of the board
        for alpha_val in range(100, -1, -1):
            fade.set_alpha(alpha_val)
            screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(40)

    def fade(self):
        fade = pygame.Surface(SCREENSIZE)
        fade.fill((187, 173, 160))  # color of the board
        for alpha_val in range(0, 80):
            fade.set_alpha(alpha_val)
            screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(40)

    def game_over(self):
        screen.fill((187, 173, 160))  # fill with board color

        score = 0
        for i in range(len(self.grid.cells)):
            for j in range(len(self.grid.cells)):
                score += self.grid.cells[i][j].value

        font = pygame.font.SysFont("Times New Roman", 30)
        textobj = font.render("Sucks To Be You; score: " + str(score), 1, (255, 255, 255))
        textrect = textobj.get_rect()
        textrect.x = 0  # (SCREENSIZE[0] / 2)
        textrect.y = 0  # (SCREENSIZE[1] / 2)

        screen.blit(pygame.transform.scale(screen, SCREENSIZE), (0, 0))
        screen.blit(textobj, textrect)
        pygame.display.update()
        pygame.time.wait(1500)

    def game(self):
        running = True
        while running:
            screen.fill((0, 0, 0))
            self.grid.draw()

            if not self.grid.available_cells():
                self.fade()
                self.game_over()
                break

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_UP:
                        self.grid.swipe_up()
                    elif event.key == K_DOWN:
                        self.grid.swipe_down()
                    elif event.key == K_RIGHT:
                        self.grid.swipe_right()
                    elif event.key == K_LEFT:
                        self.grid.swipe_left()
                    self.grid.place_random_cell()

            pygame.display.update()
            mainClock.tick(60)

    def start_game(self):
        self.main_menu()


g = Game(4)
g.start_game()
