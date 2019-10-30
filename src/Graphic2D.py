import pygame
from pygame import Color
import numpy as np
from Text import Text
import copy
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (211,211,211)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
PINK = (240,128,128)
class Graphic2D():
   
  def __init__(self):
    pygame.init()
    self.running = True
    self.screen = pygame.display.set_mode((SCREEN_WIDTH+50,SCREEN_HEIGHT+50))
  
  
  def setup(self,width,height,start,end,polygons,moving,pick_up_points,path,trace = None):
    caption = 'CHI PHI DI CHUYEN NGAN NHAT: '+ str(len(path)-1) if len(path)!=0 else 'No solution'
    pygame.display.set_caption(caption)
    
    self.screen.fill(BACKGROUND_COLOR)
    self.screen.set_alpha(255)

    self.width = int(SCREEN_WIDTH/width)
    self.height = int(SCREEN_HEIGHT/height)
    self.black_points = []
    self.pink_points = []
    self.moving = moving
    self.polygons = polygons
    self.polygons_color = []
    for polygon in self.polygons : 
      color = tuple(np.random.choice(range(256), size=3))
      self.polygons_color.append(color)
    self.path = path
    self.start = start 
    self.end = end 
    self.pick_up_points = pick_up_points
    self.trace = trace
    
  def draw(self) : 
    self.screen.fill(BACKGROUND_COLOR)
    self.draw_points(self.pink_points,PINK)
    self.draw_points(self.black_points,BLACK)
    for i in range(0,len(self.polygons)) :
      self.draw_polygon(self.polygons[i],self.polygons_color[i])
    self.draw_text([self.start],'S')
    self.draw_text([self.end],'G')
    self.draw_text(self.pick_up_points,'P')

  def run(self):
    self.draw()
    while self.running :
      if(self.trace) : 
        current = self.trace[0]
        if self.moving : 
          self.polygons = self.moving[0]
          self.moving.pop(0)
        self.draw()
        self.draw_points([current])
        self.pink_points.append(current)
        self.trace.pop(0)
      else :
        if self.path : 
          current = self.path[0]
          self.draw()
          self.draw_points([current],BLUE)
          self.black_points.append(current)
          self.path.pop(0)
      pygame.display.update()
      pygame.time.delay(500)    
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
  
  def draw_polygon(self,points,color = RED):
    points = self.convert(points)
    for point in points : 
      pygame.draw.polygon(self.screen,color,self.transform(point))
  
  def draw_text(self,points,text = None) :
    points = self.convert(points)
    for point in points :
      if(text) : Text(text,point).draw(self.screen)
   
  def draw_points(self,points,color = RED):
    if not points : 
      return
    points = self.convert(points)
    for point in points :
      x,y = point
      pygame.draw.circle(self.screen,color,(x,y),int(self.height/2))

