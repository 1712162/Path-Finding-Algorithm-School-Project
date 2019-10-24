from collections import deque
from PriorityQueue import PriorityQueue
from Graphic2D import Graphic2D
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
    self.graph2D.reset()
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
    self.graph2D.reset()
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
    self.graph2D.reset()
    if mode == 1:
      window = Graphic2D()
    speed = 1

    path=[start]
    queue=[start]
    while (queue):
      current=queue.pop(0)      
      if(current == end):
        break
      x,y = current
      #If mode=1 move polygons in coordinate
      if mode == 1:
        self.graph2D.coordinate=self.graph2D.move_all_polygons(speed,current)
        window.setup(self.graph2D.width,self.graph2D.height,start,end,self.graph2D.polygons,[],path)
        window.draw_point([current])

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
