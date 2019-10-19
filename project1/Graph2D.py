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