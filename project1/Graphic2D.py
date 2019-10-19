import pygame
import numpy as np
from Text import Text
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (211,211,211)
class Graphic2D():
   
  def __init__(self):
    pygame.init()
    self.running = True
    self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
  
  def setup(self,width,height,start,end,polygons,pick_up_points,path):
    self.screen.fill(BACKGROUND_COLOR)
    self.pixel_x = SCREEN_WIDTH/width
    self.pixel_y = SCREEN_HEIGHT/height
    self.draw_points([start,end],'S')
    for polygon in polygons :
      self.draw_polygon(polygon)
    self.draw_points(pick_up_points,'P')
    path.pop(0)
    path.pop()
    self.path = path

  def run(self):
    self.draw_path(self.path)
    while self.running :
      for event in pygame.event.get() :
        if event.type == pygame.QUIT:
          self.running = False
    pygame.quit()

  def transform_XY(self,coords):
    points = []
    for p in coords:
      x,y = p
      points.append((x*self.pixel_x,SCREEN_HEIGHT - y*self.pixel_y))
    return points
  
  def draw_polygon(self,points):
    color = tuple(np.random.choice(range(256), size=3))
    pygame.draw.polygon(self.screen,color,self.transform_XY(points))
    pygame.display.update()
  
  def draw_points(self,points,text = None) :
    color = tuple(np.random.choice(range(256), size=3))
    points = self.transform_XY(points)
    for point in points :
      if(text) : Text(text,point).draw(self.screen)
      pygame.draw.line(self.screen,color,point,point)
      pygame.display.update()
   
  def draw_path(self,path):
    color = tuple(np.random.choice(range(256), size=3))
    path = self.transform_XY(path)
    for point in path :
      x,y = point
      pygame.draw.rect(self.screen,color,(x,y,self.pixel_x,self.pixel_y))
      pygame.display.update()
      pygame.time.delay(1000)

  #def draw_output(self,start,end,polygons,pick_up_points,path):

