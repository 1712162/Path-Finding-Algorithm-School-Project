class Graph2d:
	__coordinate=[]
	__width=0
	__height=0
	__polygons=[]

	def __init__(self,width,height):
		self.__height=height
		self.__width=width
 		
	def __points_to_polygon(self,list_of_tuple):
		polygon=[]
		for i in range(0,len(list_of_tuple)):
			x1,y1=list_of_tuple[i]
			if(i+1>=len(list_of_tuple)):
				x2,y2=list_of_tuple[0]
			else:
				x2,y2=list_of_tuple[i+1]
			if(x1==x2):
				for t in range(min([y1,y2]),max([y1,y2])+1):
					polygon.append((x1,t))
			else:
				a=(y2-y1)/(x2-x1)
				b=(int)(y1-x1*a)
				for t in range(min([x1,x2]),max([x1,x2])+1):
					polygon.append((t,int(t*a+b)))
		return polygon

	def __points_to_polygons(self,list_of_list_of_tube):
		polygons=[]
		for x in list_of_list_of_tube:
			polygons.append(self.__points_to_polygon(x))
		return polygons

	def __create_coordinate(self,width,height):
		coordinate=[[0 for j in range(width+1)] for i in range(height+1)] #init coordinate(0) with width and height

		for i in range(height+1):
			coordinate[i][0]=1
			coordinate[i][width]=1

		for i in range(width+1):
			coordinate[0][i]=1
			coordinate[height][i]=1
		return coordinate

	def polygons_to_coordinate(self,list_of_list_of_tube):
		self.__coordinate=self.__create_coordinate(self.__width,self.__height)
		self.__polygons=self.__points_to_polygons(list_of_list_of_tube)
		for i in range(len(self.__polygons)):
			for j in range(len(self.__polygons[i])):
				x,y=self.__polygons[i][j]
				self.__coordinate[y][x]=1
		return self.__coordinate

	def __polygon_limit(self,polygon,orientation):
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
	def __polygon_move_limit(self,polygon):
		coordinate=self.__coordinate.copy()
		min_x_of_polygon, max_x_of_polygon=self.__polygon_limit(polygon,1)
		min_y_of_polygon, max_y_of_polygon=self.__polygon_limit(polygon,0)
		y_limit_up=[]
		y_limit_down=[]
		for i in range(min_x_of_polygon,max_x_of_polygon+1):
			for j in range(min_y_of_polygon-1,-1,-1):
				if(coordinate[j][i]!=0 and i!=0 and i!=self.__width):
					y_limit_up.append(j)
					break
			for j in range(max_y_of_polygon+1,self.__height+1):
				if(coordinate[j][i]!=0 and i!=0 and i!=self.__width):
					y_limit_down.append(j)
					break
		return (max(y_limit_up),min(y_limit_down))

	def __polygon_can_move(self,polygon,up_down):
		min_y_limit,max_y_limit=self.__polygon_move_limit(polygon)
		min_y_of_polygon,max_y_of_polygon=self.__polygon_limit(polygon,0)
		if(min_y_of_polygon+up_down<=min_y_limit or max_y_of_polygon+up_down>=max_y_limit):
			return False
		return True
	
	def __move_one_polygon(self,polygon_index,up_down):
		
		coordinate=self.__coordinate
		polygon=self.__polygons.pop(polygon_index)
		if((self.__polygon_can_move(polygon,up_down))):
		
			y_limit_up,y_limit_down=self.__polygon_move_limit(polygon)
			polygon_after_move=[]
			for i in polygon:
				x,y=i
				coordinate[y][x]=0
			for i in polygon:
				x,y=i
				polygon_after_move.append((x,y+up_down))
				coordinate[y+up_down][x]=1
			for i in range(0,self.__height+1):
				coordinate[i][0]=1
				coordinate[i][self.__width]=1
			for i in range(0,self.__width+1):
				coordinate[0][i]=1
				coordinate[self.__height][i]=1
			polygon=polygon_after_move
		self.__polygons.insert(polygon_index,polygon)
		return coordinate

	def move_all_polygons(self,up_down):
		coordinate=[]
		number_of_polygons=len(self.__polygons)
		for i in range(number_of_polygons):
			coordinate=self.__move_one_polygon(i,up_down)
		return coordinate

	def get_coordinate(self):
		return self.__coordinate

			
				
