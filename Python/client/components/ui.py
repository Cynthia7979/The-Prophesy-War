import pygame


class Button(object):
    def __init__(self, surface:pygame.Surface, rect:pygame.Rect, action):
        self._surface = surface
        self._rect = rect
        self._action = action

    def clicked(self, mousepos:tuple):
        return self._rect.collidepoint(mousepos)

    def activate(self):
        return self._action

    def draw(self, destSurface):
        destSurface.blit(self._surface, self._rect)


class TextButton(Button):
    def __init_(self, font:pygame.font.Font, text:str, rect:pygame.Rect, action, color=(0,0,0), aa=True, background=None):

        Button.__init__(self, font.render(text, aa, color, background), rect, action)
