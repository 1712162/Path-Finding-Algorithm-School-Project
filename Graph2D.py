class Graph2d:
	__coordinate=[]
	__width=0
	__height=0
	__polygons=[]
	def __init__(self,width,height):
		self.__height=height
		self.__width=width
 		
	def __points_to_polygon(self,list_of_tuple):
		medium_y_polygon=sum([x[1] for x in list_of_tuple])/len(list_of_tuple)
		polygon=[[],[],[]]

		for i in range(0,len(list_of_tuple)):
			x1,y1=list_of_tuple[i]
			if(i+1>=len(list_of_tuple)):
				x2,y2=list_of_tuple[0]
			else:
				x2,y2=list_of_tuple[i+1]
			if(x1==x2):
				for t in range(min([y1,y2]),max([y1,y2])+1):
					polygon[2].append((x1,t))
			else:
				a=(y2-y1)/(x2-x1)
				b=(int)(y1-x1*a)
				for t in range(min([x1,x2]),max([x1,x2])+1):
					h=int(t*a+b)
					if(h<medium_y_polygon):
						polygon[0].append((t,h))
					else:
						polygon[1].append((t,h))
		return polygon
	def points_to_polygons(self,list_of_list_of_tube):
		for x in list_of_list_of_tube:
			self.__polygons.append(self.__points_to_polygon(x))
		return self.__polygons
	def __create_map(self,width,height):
		map=[[0 for j in range(width+1)] for i in range(height+1)] #init map(0) with width and height

		for i in range(height+1):
			map[i][0]=1
			map[i][width]=1

		for i in range(width+1):
			map[0][i]=1
			map[height][i]=1
		return map
	def polygons_to_map(self,list_of_list_of_tube):
		self.__coordinate=self.__create_map(self.__width,self.__height)
		self.__polygons=self.points_to_polygons(list_of_list_of_tube)
		for i in range(len(self.__polygons)):
			for j in range(len(self.__polygons[i])):
				for t in range(len(self.__polygons[i][j])):
					x,y=self.__polygons[i][j][t]
					print(x,y)
					self.__coordinate[y][x]=1
		return self.__coordinate
	def __up_down_test(self,list_of_tube,up_or_down):
		for i in range(len(list_of_tube)):
			x,y=list_of_tube[i]
			if(self.__coordinate[y+up_or_down][x]==1):
				return False
		return True
	
				
