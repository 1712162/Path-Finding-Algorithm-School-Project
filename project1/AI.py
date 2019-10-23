from collections import deque
import heapq
import arcade
import time
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
    self.direct = [ [-1,0],[0,-1],[1,0],[0,1]]

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

  def polygon_limit(self,polygon,orientation):
    xy_of_polygon=[]
    for i in polygon:
      x,y=i
      if(orientation==1):
        xy_of_polygon.append(x)
      else:
        xy_of_polygon.append(y)
    min_xy_of_polygon=min(xy_of_polygon)
    max_xy_of_polygon=max(xy_of_polygon)
    return (min_xy_of_polygon,max_xy_of_polygon)

  def polygon_move_limit(self,polygon,current):
    coordinate=self.coordinate.copy()
    min_x_of_polygon, max_x_of_polygon=self.polygon_limit(polygon,1)
    min_y_of_polygon, max_y_of_polygon=self.polygon_limit(polygon,0)
    y_limit_up=[self.height]
    y_limit_down=[0]
    for i in range(min_x_of_polygon,max_x_of_polygon+1):
      for j in range(min_y_of_polygon-1,0,-1):
        if(self.is_in_polygons((i,j))):
          y_limit_down.append(j)
          break
      for j in range(max_y_of_polygon+1,self.height):
        if(self.is_in_polygons((i,j))):
          y_limit_up.append(j)
          break
    return (max(y_limit_down),min(y_limit_up))
  
  def polygon_can_move(self,polygon,up_down,current):
    min_y_limit,max_y_limit=self.polygon_move_limit(polygon,current)
    min_y_of_polygon,max_y_of_polygon=self.polygon_limit(polygon,0)
    if(min_y_of_polygon+up_down<=min_y_limit or max_y_of_polygon+up_down>=max_y_limit):
      return False
    return True
  
  def move_one_polygon(self,polygon_index,up_down,current):
    coordinate=self.coordinate
    polygon=self.polygons.pop(polygon_index)
    if((self.polygon_can_move(polygon,up_down,current))):
      y_limit_up,y_limit_down=self.polygon_move_limit(polygon,current)
      polygon_after_move=[]
      for i in polygon:
        x,y=i
        coordinate[y][x]=0
      for i in polygon:
        x,y=i
        polygon_after_move.append((x,y+up_down))
        coordinate[y+up_down][x]=1
      polygon=polygon_after_move
    self.polygons.insert(polygon_index,polygon)
    return coordinate

  def move_all_polygons(self,up_down,current):
    coordinate=[]
    number_of_polygons=len(self.polygons)
    for i in range(number_of_polygons):
      coordinate=self.move_one_polygon(i,up_down,current)
    return coordinate
  
  def is_in_polygons(self,current):
    for i in self.polygons:
      if i.count(current) > 0:
        return True
    return False


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
    parent[goal] = None
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
  def DFS(self,start,end,mode):
    #init for moving
    if mode == 1:
      window = Graphic2D(self.graph2D.width-1,self.graph2D.height-1)
      window.setup()
    speed = 1

    path=[]
    queue=[start]
    while (queue):
      current=queue.pop(0)      
      if(current == end):
        break
      x,y = current
      #If mode=1 move polygons in coordinate
      if mode == 1:
        self.graph2D.coordinate=self.graph2D.move_all_polygons(speed,current)
        window.draw_output(start,end,self.graph2D.polygons,[],path)

      neighbors=self.graph2D.get_neighbors(current)
      if (len(neighbors)!=0):
        if(self.graph2D.coordinate[y][x]!=1):
         
          path.append(current)
          self.graph2D.coordinate[y][x]=1
          for next in neighbors:
            queue.insert(0,next)
      else:
        if len(path)>0:
          queue.insert(0,path.pop(len(path)-1))
      speed=0-speed
      
    return path
      
    # return path

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

class Function_switcher(object):
  def __init__(self,shortest_path,start,end,width,height,graph2d, pick_up_points):
    self.shortest_path=shortest_path
    self.start=start
    self.end=end
    self.width=width
    self.height=height
    self.graph2d=graph2d
    self.pick_up_points=pick_up_points

  def get_function(self,i):
	  method_name='level_'+str(i)
	  method=getattr(self,method_name,lambda :print('Invalid Function'))
	  return method()

  def draw_path(self,path):
    window = Graphic2D(self.width,self.height)
    window.setup()
    if(path) :
      window.draw_output(self.start,self.end,self.graph2d.polygons,self.pick_up_points,path)
      arcade.run()
    else :
      window.draw_text()

  def level_0(self):
    return exit()

  def level_1(self):
    path =  self.shortest_path.a_star_search( self.start,self.end )
    self.draw_path(path)

  def level_2(self):
    path1 =  self.shortest_path.a_star_search( self.start,self.end )
    path2 =  self.shortest_path.BFS( self.start,self.end )
    path3 =  self.shortest_path.DFS( self.start,self.end,0 )
    self.draw_path(path1)
    time.sleep(5)
    self.draw_path(path2)
    time.sleep(5)
    self.draw_path(path3)
    time.sleep(5)
		
  def level_3(self):
    path=self.shortest_path.shortest_path_with_pickup_points(self.start,self.end, self.pick_up_points)
    self.draw_path(path)

  def level_4(self):
    path=self.shortest_path.DFS(self.start,self.end,1)
    print(4)


#################################################################
def show_menu():
  for i in range(4):
    level=i+1
    display_line=str(level)+'. level '+str(level)
    print(display_line)

def create_graph2d(width,height,polygons):
  graph2d=Graph2D(width+1,height+1)
  graph2d.polygons_to_coordinate(polygons)
  return graph2d
def main():
  #nhap file
    file=input('Enter your file path: ')

		#get data from file
    width,height,start,end,polygons,pick_up_points = read_file(file)

    graph2d=create_graph2d(width,height,polygons)
    shortest_path=ShortestPath(graph2d)
    print('\n')
	
		#show menu + get number_of_function
    show_menu()
    number_of_function=input('Function: ')
    print ('\n')

		#run function selected
    function_switcher=Function_switcher(shortest_path,start,end,width,height,graph2d,pick_up_points)
    run_function=function_switcher.get_function(number_of_function)

if __name__ == "__main__":
    main()