from collections import deque
import heapq
import arcade
import numpy as np
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Shortest path"
####################################################################
def read_file(path):
  with open(path) as input_file:
      # Get all lines from input file
      lines = [line for line in input_file]
    
      # Convert line to attribute
      width, height = [int(x) for x in lines[0].split()]
     
      # Start, End , Pick-up points
      points = [int(x) for x in lines[1].split()]
      length = len(points)
      x = [points[i] for i in range(length) if i % 2 == 0]
      y = [points[i] for i in range(length) if i % 2 == 1]
    
      start = (x[0], y[0])
      end = (x[1], y[1])
      pick_up_points = [(x[i], y[i]) for i in range(2, length//2)]
    
      # Get polygons
      length = len(lines)
      polygons = [[int(x) for x in lines[i].split()] for i in range(3, length)]
    
      # Convert type of polygons from list of list to list of list of tuple
      new_polygons = []
      for polygon in polygons:
        temp_polygon = []
      
        for i in range(len(polygon)):
          if i % 2 == 0:
            x = polygon[i]
          
          if i % 2 == 1:
            y = polygon[i]
            temp_polygon.append((x, y))
          
        new_polygons.append(temp_polygon)
  return width, height, start, end, new_polygons, pick_up_points
####################################################################
# Create Priority Queue
class PriorityQueue:
    def __init__(self):
        self.elements = []
    #Checking priority queue is empty
    def empty(self):
        return len(self.elements) == 0

    # Push item with priority into queue
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    # Pop and get first item out of queue
    def get(self):
        return heapq.heappop(self.elements)[1]

####################################################################
class Graph2D :
  def __init__(self,width,height) : 
    self.width  = width
    self.height = height
    self.polygons = []
    self.coordinate = [ [ 0 for x in range(0,width)] for y in range(0,height)]
    self.direct = [ [0,-1],[0,1],[-1,0],[1,0]]

  def set_state(self,point) :
    x,y = point
    self.coordinate[y][x] = 1 - self.coordinate[y][x]

  def get_state(self,x,y) :
    return self.coordinate[y][x] 

  def out_of_bounds(self,x,y) :
    return not (0< x and x < self.width and 0 < y and y < self.height)
  
 
  def points_to_polygon(self,points):
    polygon = []
    number_of_points = len(points)
    for i in range(0,number_of_points):
			# current point
      x1,y1 = points[i]

      # next point
      x2,y2 = points[0] if (i+1 >= number_of_points) else points[i+1]
			
      # if there is a x-axis line
      if(x1 == x2):
        for y in range(min([y1,y2]),max([y1,y2])+1):
          polygon.append((x1,y))
      else:
        a=(y2-y1)/(x2-x1)
        b=(int)(y1-x1*a)
        for x in range(min([x1,x2]),max([x1,x2])+1):
          polygon.append((x,int(x*a+b)))

    polygon = list(set(polygon)) 
    return polygon

  def points_to_polygons(self,points):
    polygons = []
    for p in points:
      polygons.append(self.points_to_polygon(p))
    return polygons

  def polygons_to_coordinate(self,polygons):
    coordinate = [ [ 0 for x in range(0,self.width)] for y in range(0,self.height)]
    self.polygons = self.points_to_polygons(polygons)
    for polygon in self.polygons:
      for (x,y) in polygon :
        coordinate[y][x] = 1
    self.coordinate = coordinate
  
  def get_neighbors(self,current):
    neighbors = []
    for i in range(0,4) :
      x,y = self.direct[i][0]+current[0], self.direct[i][1]+current[1]
      if( not self.out_of_bounds(x,y) and self.get_state(x,y)!=1 ):
        neighbors.append((x,y))
    return neighbors

#######################################
class ShortestPath : 
  def __init__(self,graph2D) :
    self.graph2D = graph2D

  def backtrace(self,parent,start,end) :
    if not parent[end]:
      return []
    path = [end]
    while path[-1] != start:
      path.append(parent[path[-1]])
    path.reverse()
    return path
  
  def heuristic(self, a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

  def a_star_search(self, start, goal):
    #Push start into frontier
    frontier = PriorityQueue()
    frontier.put(start, 0)
    
    # Create a dictionary that contains previous position of current position   
    parent = {}
    # Create a dictionary that contains cost_so_far[current_position] = sum up cost from start to current_position
    cost_so_far = {}
    
    # Initilization dictionary 
    parent[start] = None
    parent[end] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        # Get position from front positions (previous position)
      current = frontier.get()

      # If you are standing at goal to stop
      if current == goal:
        break

      # Get adjacent vertices
      for next in self.graph2D.get_neighbors(current):
        #Update new_cost 
        new_cost = cost_so_far[current] + 1
        # Checking is in cost_so_far or new_cost is smaller than old_cost
        if next not in cost_so_far or new_cost < cost_so_far[next]:
          #Update new cost
          cost_so_far[next] = new_cost
          priority = new_cost + self.heuristic(goal, next)
          #Update frontier and parent
          frontier.put(next, priority)
          parent[next] = current
    return self.backtrace(parent, start, goal)

  # BFS
  def BFS(self,start,end) :
    queue = deque([])
    queue.append(start)
    parent = {}
    parent[start] = None
    parent[end] = None
    graph2D = self.graph2D

    graph2D.set_state(start)

    while queue : 
      current = queue.popleft()
      if(current == end): 
        break

      for next in self.graph2D.get_neighbors(current):
        graph2D.set_state(next)
        queue.append(next)
        parent[next] = (current)
    return self.backtrace(parent,start,end)

  #DFS
  def DFS(self,start,end):
    path=[]
    queue=[start]
    while (queue):
      current=queue.pop(0)
      path.append(current)
      if(current == end):
        break
      self.graph2D.set_state(current)
      for next in self.graph2D.get_neighbors(current):
        queue.insert(0,next)
    return path

  # Pick-up points 
  def sort_by_distance(self,pick_up_points, start, end):
    result = [start]
    points = list(pick_up_points)
  
    while len(points) != 0:
      # Init variables
      point_min = points[0]
      min_value = self.heuristic(result[-1], point_min)
      
      for point in points:
        # Find point that has heuristic(result[-1], point) is minimum
        if self.heuristic(result[-1], point) < min_value:
          point_min = point
          min_value = self.heuristic(result[-1], point)
      
      # Update point_list
      result.append(point_min)
      # Deleted Out of pick_up points
      points.remove(point_min)
      
    # Add end point
    result.append(end)
    
    return result

  def shortest_path_with_pickup_points(self, start, end, pick_up_points):
    point_list = self.sort_by_distance(pick_up_points, start, end)
    result = []
    
    # Find first period
    path = self.a_star_search(point_list[0], point_list[1])
    if path != -1:
      result = path
    else:
      return -1
    
    length = len(point_list)
    for i in range(1, length - 1):
      path =  self.a_star_search(point_list[i], point_list[i + 1])
      
      if path != -1:
        for i in range(1, len(path)):
          result.append(path[i])
      else:
        return -1
      
    return result

#######################################
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
    for x in range(0, SCREEN_WIDTH, self.cell_width ):
      arcade.draw_line(x, 0, x, SCREEN_HEIGHT, arcade.color.BLACK, 2)
    for y in range(0,SCREEN_HEIGHT, self.cell_height ):
      arcade.draw_line(0, y,SCREEN_WIDTH, y, arcade.color.BLACK, 2)

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


#######################################
width,height,start,end,polygons,pick_up_points = read_file("/home/voquocthang/Python/test.txt")

graph2D = Graph2D(width+1,height+1)
graph2D.polygons_to_coordinate(polygons)

shortestPath = ShortestPath(graph2D)
path =  shortestPath.shortest_path_with_pickup_points(start,end,pick_up_points)

window = Graphic2D(width,height)
window.setup()
window.draw_output(start,end,graph2D.points_to_polygons(polygons),pick_up_points,path)
arcade.run()


        

