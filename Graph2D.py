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
					polygon.append(t,int(t*a+b))
		return polygon
	def __points_to_polygons(self,list_of_list_of_tube):
		for x in list_of_list_of_tube:
			self.__polygons.append(self.__points_to_polygon(x))
		return self.__polygons
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
	
	def get_coordinate(self):
		return self.__coordinate
			
				
