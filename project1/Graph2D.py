import copy

class Graph2D :
  def __init__(self,width,height) : 
    self.width  = width
    self.height = height
    self.polygons = []
    self.coordinate = [ [ 0 for x in range(0,width)] for y in range(0,height)]
    self.backup = [ [ 0 for x in range(0,width)] for y in range(0,height)]
    self.direct = [ [0,-1],[-1,0],[0,1],[1,0]]

  def set_state(self,point) :
    x,y = point
    self.coordinate[y][x] = 1 - self.coordinate[y][x]

  def get_state(self,x,y) :
    return self.coordinate[y][x] 

  def out_of_bounds(self,x,y) :
    return not (0< x and x < self.width and 0 < y and y < self.height)
  
  def reset(self) : 
    self.coordinate = copy.deepcopy(self.backup)
 
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
    self.backup = copy.deepcopy(coordinate)
  
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
      x_min,x_max=self.polygon_limit(i,1)
      y_min,y_max=self.polygon_limit(i,0)
      x,y=current
      if x<=x_max and x>=x_min and y<=y_max and y>=y_min:
        return True
    return False