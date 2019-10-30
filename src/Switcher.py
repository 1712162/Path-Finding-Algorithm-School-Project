from Graph2D import Graph2D
from ShortestPath import ShortestPath
class Switcher():
  def __init__(self,graph2D,start,end,pick_up_points):
    self.start = start 
    self.end = end
    self.pick_up_points = pick_up_points
    self.shortest_path = ShortestPath(graph2D)
    self.history = None
    self.trace = None
    self.graph2D = graph2D

  def execute(self,level):
    method_name = 'level_'+str(level)
    method = getattr(self,method_name)
    return method(),self.history,self.trace
  
  def level_1(self):
    path = self.shortest_path.a_star_search(self.start,self.end)
    return [path]

  def level_2(self):
    DFS = self.shortest_path.DFS(self.start,self.end)
    AStart = self.shortest_path.a_star_search(self.start,self.end)
    BFS = self.shortest_path.BFS(self.start,self.end)
    return AStart,BFS,DFS
    
  def level_3(self) :
    path = self.shortest_path.shortest_path_with_pickup_points(self.start,self.end,self.pick_up_points)
    return [path]

  def level_4(self) :
    path,trace = self.shortest_path.shortest_path_with_moving_polygons(self.start,self.end,self.pick_up_points)
    self.history = self.shortest_path.history
    self.trace = trace
    return [path]