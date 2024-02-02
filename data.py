import pygame

ATOM = (16, 16)

class COLORS:
    WHITE    = (0xff, 0xff, 0xff)
    BG_BEIGE = (0xe8, 0xdc, 0xb5)
    BLACK    = (0x00, 0x00, 0x00)
    BLUE     = (0x41, 0x69, 0xe1)
    RED      = (0xed, 0x29, 0x39)

class Element:
    def __init__(self, color, valence_electrons: int) -> None:
        self.color = color
        self.valence_electrons = valence_electrons
        self.asset = AtomSpriteGenerator.fetch(color)
    
    def __repr__(self) -> str:
        return f"Element<valence_electrons={self.valence_electrons}>"


class Atom:
    def __init__(self, element: Element, **kwargs):
        self.element = element
        self.bonded_atoms: list[Atom] = []

        self.x = kwargs.get('x', 10)
        self.y = kwargs.get('y', 10)

    def render(self, surface):
        surface.blit(self.element.asset, (self.x, self.y))

    def bond(self, other):
        self.bonded_atoms.append(other)
        other.bonded_atoms.append(self)
    
    def simplified_repr(self) -> str:
        return f"Atom<element={self.element!r},x={self.x},y={self.y}>"

    def __repr__(self) -> str:
        return f"Atom<element={self.element!r},bonded_atoms=[{','.join(atm.simplified_repr() for atm in self.bonded_atoms)}],x={self.x},y={self.y}>"


class AtomSpriteGenerator:
    FOUND = {}
    
    @classmethod
    def fetch(self, color: tuple[int, int, int]):
        if (existing := AtomSpriteGenerator.FOUND.get(color)):
            return existing
        colored = pygame.Surface(ATOM).convert_alpha()
        colored.fill(color)
        return colored

def render(items: list[Atom], surface):
    for item in items:
        item.render(surface)
