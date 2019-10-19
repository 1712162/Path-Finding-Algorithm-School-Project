import arcade
import numpy as np
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Shortest path"
class Graphic2D(arcade.Window):
   
  def __init__(self,x_axis,y_axis):
    super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    self.cell_width = int(SCREEN_WIDTH/x_axis)
    self.cell_height = int(SCREEN_HEIGHT/y_axis)
    arcade.set_background_color(arcade.color.WHITE)

  def setup(self):
    pass

  def points_to_cells(self,points):
    cells = []
    for p in points:
      x,y = p
      cells.append([x*self.cell_width,y*self.cell_height])
    return cells

  
  def draw_points(self,points,text = None):
    color = tuple(np.random.choice(range(256), size=3))
    cells = self.points_to_cells(points)
    for cell in cells :
      x,y = cell
      if(text): arcade.draw_text(text,x-self.cell_width/2,y-self.cell_height,arcade.color.BLACK,20)
      else : arcade.draw_polygon_filled([[x,y],[x-self.cell_width+2,y],[x-self.cell_width+2,y-self.cell_height+2],[x,y-self.cell_height+2]],color)


  def draw_text(self):
    arcade.start_render()
    arcade.draw_text("No solution",SCREEN_WIDTH/3,SCREEN_HEIGHT/2,arcade.color.BLACK,20)

  def draw_output(self,start,end,polygons,pick_up_points,path):

    arcade.start_render()
   
    # Draw polygon
    for polygon in polygons:
      self.draw_points(polygon)
    
    # Draw path
    self.draw_points(path) 

    #Draw begin,end
    self.draw_points([start],"S")
    self.draw_points([end],"G")

    #Draw pickup points
    self.draw_points(pick_up_points,"P")

    arcade.finish_render()

