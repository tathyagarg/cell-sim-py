import os
import random
import string
import math

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

found_atoms = {}


class CONSTANTS:
    ATOM = (16, 16)
    GRAVITATIONAL_THRESHOLD = 0.1
    RADIUS_STEP = 0.2
    ROUNDING_THRESHOLD = 0.001


COLORS = {
    "WHITE": (0xff, 0xff, 0xff),
    "BG_BEIGE": (0xe8, 0xdc, 0xb5),
    "BLACK": (0x00, 0x00, 0x00),
    "BLUE": (0x41, 0x69, 0xe1),
    "RED": (0xed, 0x29, 0x39)
}


def convert(color: tuple[int, int, int]) -> str | None:
    for name, c in COLORS.items():
        if c == color:
            return name
    return None


class Element:
    def __init__(self, color: tuple[int, int, int], valence_electrons: int, mass: int) -> None:
        self.color = color
        self.valence_electrons = valence_electrons
        self.mass = mass
        self.asset = fetch(color)

    def __repr__(self) -> str:
        return f"Element<valence_electrons={self.valence_electrons}>"


class Atom(pygame.sprite.Sprite):
    def __init__(self, element: Element, **kwargs):
        super().__init__()
        self.id = "".join(random.choices(string.printable, k=12))
        self.element = element

        # Velocity and acceleration are vector quantities, have both magnitude and direction
        # The first value (float) represents the magnitude
        # Whereas the second value (float) represents the direction in degrees
        self.velocity: float = 0

        self.acceleration: tuple[float, float] = 0, 0

        self.bonded_atoms: list[Atom] = []

        self.x = kwargs.get('x', 10)
        self.y = kwargs.get('y', 10)
        self.rect = self.element.asset.get_rect(topleft=(self.x, self.y))

    @property
    def acceleration_mag(self) -> float:
        return self.acceleration[0]

    @acceleration_mag.setter
    def acceleration_mag(self, value):
        self.acceleration = value, self.acceleration_dir

    @property
    def acceleration_dir(self) -> float:
        return self.acceleration[1]

    @acceleration_dir.setter
    def acceleration_dir(self, value):
        self.acceleration = self.acceleration_mag, value

    def render(self, surface):
        print(self.rect.x, self.rect.y)
        surface.blit(self.element.asset, (self.rect.x, self.rect.y))

    def bond(self, other):
        self.bonded_atoms.append(other)
        other.bonded_atoms.append(self)

    def simplified_repr(self) -> str:
        return f"Atom<element={self.element!r},x={self.x},y={self.y}>"

    def fetch_force_at(self, location: tuple[float, float]) -> float:
        r_2 = (location[0] ** 2) + (location[1] ** 2)  # r^2
        return self.element.mass / r_2  # Returns M/r^2

    def fetch_direction(self, other) -> float:
        delta_y = other.rect.y - self.rect.y
        delta_x = other.rect.x - self.rect.x
        if not delta_y: delta_y = 0.0000001
        if not delta_x: delta_x = 0.0000001
        print(f"Returning dir: {math.degrees(math.atan2(delta_y, delta_x))}")
        return math.degrees(math.atan2(delta_y, delta_x))

    def attractive_force(self) -> float | int:
        """
        ===GRAVITY===
        Use formula g = GM/r^2
        Such that lim r^2->0 g = 0
        But, G = 1 => g = M/r^2

        ===GRAVITATIONAL SOI===
        SoI is a circle, with radius r
        Formula for such a circle:
            (x+self.x)^2 + (y+self.y)^2 = r^2
        So, to check if a point is in the SoI,
            (p.x+self.x)^2 + (p.y+self.y)^2 <= r^2

        :return:
        """
        r: float = 1.0
        force: float = self.element.mass / r ** 2

        while force > CONSTANTS.GRAVITATIONAL_THRESHOLD:
            r += CONSTANTS.RADIUS_STEP
            force = self.element.mass / r ** 2

        return round_if_needed(r)

    def __repr__(self) -> str:
        return f"Atom<element={self.element!r}," \
               f"bonded_atoms=[{','.join(atm.simplified_repr() for atm in self.bonded_atoms)}]," \
               f"x={self.x},y={self.y}>"

    def __eq__(self, other):
        return self.id == other.id


class PolyAtom:
    def __init__(self, atoms: list[Atom]):
        self.atoms = atoms
        self.valence_electrons = sum([atom.element.valence_electrons for atom in atoms]) % 8
        self.rect = self.atoms[0].rect.copy()
        self.surface = None

    def initialize_at(self):
        self.rect = self.atoms[0].rect.copy()
        for atom in self.atoms[1:]:
            self.rect.union_ip(atom.rect)

        self.surface = pygame.Surface(self.rect.size)
        render(self.atoms, self.surface)


def round_if_needed(val: float) -> float | int:
    if abs(round(val, 3) - val) <= CONSTANTS.ROUNDING_THRESHOLD:
        return round(val, 3)
    return val


def fetch(color: tuple[int, int, int]):
    if existing := found_atoms.get(color):
        return existing
    colored = pygame.Surface(CONSTANTS.ATOM).convert_alpha()
    colored.fill(color)
    return colored


def render(items: list[Atom], surface):
    for item in items:
        item.render(surface)


def apply_gravity(atoms: list[Atom]):
    for atom in atoms:
        field = atom.attractive_force()
        for other in atoms:
            if other == atom: continue
            delta = (abs(atom.rect.x - other.rect.x), abs(atom.rect.y - other.rect.y))
            if (delta[0] ** 2 + delta[1] ** 2) ** 0.5 <= field:
                div = (bool(other.acceleration_dir)) + 1
                other.acceleration = (other.acceleration_mag + atom.fetch_force_at(delta),
                                      (other.acceleration_dir + other.fetch_direction(atom))/div)


def apply_speed(atoms: list[Atom], time_period: float):
    """
    Use formula v = u + at
    """
    for atom in atoms:
        print(f"velocity: {atom.velocity}")
        atom.velocity += (atom.acceleration_mag * time_period)


def update_atoms(atoms: list[Atom], time_period: float):
    """
    Using formulas:
        x' = x + v * cos(theta) * T
        y' = y + v * sin(theta) * T
    """
    for atom in atoms:
        print(f"{convert(atom.element.color)} has dir: {atom.acceleration_dir}")
        atom.rect.x = atom.rect.x + atom.velocity * -math.cos(atom.acceleration_dir) * time_period
        atom.rect.y = atom.rect.y + atom.velocity * -math.sin(atom.acceleration_dir) * time_period
