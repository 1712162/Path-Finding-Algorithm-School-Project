from collections import deque
import heapq
####################################################################
def read_file(path):
  with open(path) as input_file:
      # Get all lines from input file
      lines = [line for line in input_file]
    
      # Convert line to attribute
      width, height = [int(x) for x in lines[0].split()]
      start_x, start_y, end_x, end_y = [int(x) for x in lines[1].split()]
    
      # Get number of polygons
      number_of_polygons = int(lines[2])
    
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
  return width, height, (start_x, start_y), (end_x, end_y), new_polygons
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

  def setState(self,point) :
    x,y = point
    self.coordinate[y][x] = 1 - self.coordinate[y][x]

  def getState(self,x,y) :
    return self.coordinate[y][x] 

  def outOfBounds(self,x,y) :
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
      if( not self.outOfBounds(x,y) and self.getState(x,y)!=1 ):
        neighbors.append((x,y))
    return neighbors

  def printGraph(self) : 
    print(self.coordinate)

#######################################
class ShortestPath : 
  def __init__(self,graph2D) :
    self.graph2D = graph2D

  def backtrace(self,parent,start,end) :
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
    if(parent[end] == None):
      return -1
    return self.backtrace(parent, start, goal)

  def BFS(self,start,end) :
    xa,ya = start
    xb,yb = end
    
    queue = deque([])
    queue.append([start,0])
    parent = {}
    graph2D = self.graph2D

    graph2D.setState(start)

    while queue : 
      current,cost = queue.popleft()
      print(current)
      if(current == end): 
        return self.backtrace(parent,start,end)
     
      for next in self.graph2D.get_neighbors(current):
        graph2D.setState(next)
        queue.append([next,cost+1])
        parent[next] = (current)
    return -1

#######################################
width,height, start, end, polygons = read_file("/home/truongtop14/git_workspace/AI-Searching-Algorithm-Project/TestCase/input_0.txt")

graph2D = Graph2D(width+1,height+1)
graph2D.polygons_to_coordinate(polygons)

shortestPath = ShortestPath(graph2D)

path =  shortestPath.a_star_search( start,end )
if(path != -1) :
  print(len(path) - 1)
  print(path)
else :
  print("No solution")

        

