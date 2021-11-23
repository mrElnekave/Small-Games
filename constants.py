import pygame
pygame.init()
BOARDSIZE = 8
if BOARDSIZE > 5:
    BOARDSIZE = 5

WINVALUE = 2048

SCREENSIZE = (500, 500)

def draw_text(text, surface, font = pygame.font.SysFont(None, 40), color=(0,0,0), x=0, y=0):
    """

    :param text: what you want written
    :param surface: usually the program screen or any surface you want to draw on
    :param font: the font :)
    :param color: RGB color tuple
    :param x: Xpos
    :param y: Ypos
    :return: returns the object it drew if you want it to interact with stuff
    """
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    return textrect
