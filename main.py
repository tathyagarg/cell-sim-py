import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import pygame.locals as game_locs
from data import *

# CONSTANTS
FPS = 30
clock = pygame.time.Clock()
tick = 50

# Pygame initialization
pygame.init()
surface = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Cell Simulation")

C = Element(COLORS["BLACK"], 4, 10000)
H = Element(COLORS["WHITE"], 1, 1)
N = Element(COLORS["BLUE"], 5, 14)
O = Element(COLORS["RED"], 6, 16)

c = Atom(C, x=1000, y=500)
h = Atom(H, x=900, y=550)
n = Atom(N, x=1100, y=600)
o = Atom(O, x=1000, y=650)

atoms = [c, h, n, o]


while True:
    surface.fill(COLORS["BG_BEIGE"])
    apply_gravity(atoms)
    apply_speed(atoms, 1/tick)
    update_atoms(atoms, 1/tick)
    render(atoms, surface)

    for event in pygame.event.get():
        if event.type == game_locs.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    clock.tick(FPS)
