import pygame
import numpy as np
from pygame.locals import *
class Text:
  """Create a text object."""
  def __init__(self, text, pos):
    self.text = text
    self.pos = pos
    self.fontname = None
    self.fontsize = 40
    self.fontcolor = Color('black')
    self.set_font()
    self.render()

  def set_font(self):
    """Set the Font object from name and size."""
    self.font = pygame.font.Font(self.fontname, self.fontsize)

  def render(self):
    """Render the text into an image."""
    background_color = tuple(np.random.choice(range(256), size=3))
    self.img = self.font.render(self.text,True, self.fontcolor,background_color)
    self.rect = self.img.get_rect()
    self.rect.center = self.pos

  def draw(self,screen):
    screen.blit(self.img, self.rect)