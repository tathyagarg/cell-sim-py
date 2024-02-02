import pygame, sys
import pygame.locals as game_locs
from data import *

# CONSTANTS
FPS = 30
clock = pygame.time.Clock()

# Pygame initialization
pygame.init()
surface = pygame.display.set_mode((680, 420))
pygame.display.set_caption("Cell Simulation")

C = Element(COLORS.BLACK, 4)
H = Element(COLORS.WHITE, 1)
N = Element(COLORS.BLUE, 5)
O = Element(COLORS.RED, 6)

c = Atom(C)
h = Atom(H, y=50)
n = Atom(N, y=100)
o = Atom(O, y=150)

atoms = [c, h, n, o]

while True:
    surface.fill(COLORS.BG_BEIGE)
    render(atoms, surface)

    for event in pygame.event.get():
        if event.type == game_locs.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    clock.tick(FPS)
