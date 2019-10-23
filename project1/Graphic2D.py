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
    self.screen = pygame.display.set_mode((SCREEN_WIDTH+50,SCREEN_HEIGHT+50))
    self.path=[]
  
  def setup(self,width,height,start,end,polygons,pick_up_points,path):
    self.screen.fill(BACKGROUND_COLOR)
    self.width = int(SCREEN_WIDTH/width)
    self.height = int(SCREEN_HEIGHT/height)
    self.draw_points([start],'S')
    self.draw_points([end],'G')
    for polygon in polygons :
      self.draw_polygon(polygon)
    self.draw_points(pick_up_points,'P')
    
    self.path = path

  def run(self):
    self.draw_path(self.path)
    while self.running :
      for event in pygame.event.get() :
        if event.type == pygame.QUIT:
          self.running = False
    pygame.quit()
  
  def convert(self,points) :
    new_points = []
    for point in points : 
      x,y = point
      y-=1
      new_points.append((x*self.width,SCREEN_HEIGHT -  y*self.height))
    return new_points
  
  def transform(self,point):
    x,y = point
    return [(x-self.width/2,y-self.height/2),
            (x+self.width/2,y-self.height/2),
            (x+self.width/2,y+self.height/2),
            (x-self.width/2,y+self.height/2)]
  
  def draw_polygon(self,points):
    color = tuple(np.random.choice(range(256), size=3))
    points = self.convert(points)
    for point in points : 
      pygame.draw.polygon(self.screen,color,self.transform(point))
      pygame.display.update()
  
  def draw_points(self,points,text = None) :
    color = tuple(np.random.choice(range(256), size=3))
    points = self.convert(points)
    for point in points :
      if(text) : Text(text,point).draw(self.screen)
      pygame.display.update()
   
  def draw_path(self,path):
    color = tuple(np.random.choice(range(256), size=3))
    path = self.convert(path)
    path.pop(0)
    for point in path :
      x,y = point
      pygame.draw.circle(self.screen,color,(x,y),int(self.height/2))
      pygame.display.update()
      pygame.time.delay(1000)
    
  def draw_point(self,path):
    color = (255,255,255)
    path = self.convert(path)
    path.pop(0)
    for point in path :
      x,y = point
      pygame.draw.circle(self.screen,color,(x,y),int(self.height/2))
      pygame.display.update()
    pygame.time.delay(1000)  

  #def draw_output(self,start,end,polygons,pick_up_points,path):

