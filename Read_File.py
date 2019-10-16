class Read_File:
	__width=0
	__height=0
	__start_end_points=[]
	__number_of_polygons=0
	__polygons=[]
	
	def __init__(self,File,Mode):
		self.__read(File,Mode)
	def __read(self,File,Mode):
		file=open(File,Mode)
		witdth_height=file.readline().split()
		self.__width=int(witdth_height[0])
		self.__height=int(witdth_height[1])
		self.__start_end_points=file.readline().split()
		self.__number_of_polygons=int(file.readline())
		for i in range(0,self.__number_of_polygons):
			self.__polygons.append(file.readline().split());
		file.close()
	def __string_to_points(self,list_of_string):
		points=[]
		for i in range(0,len(list_of_string),2):
			points.append((int(list_of_string[i]),int(list_of_string[i+1])))
		return points
	def get_width(self):
		return self.__width
	def get_height(self):
		return self.__height
	def get_start_end(self):
		return self.__string_to_points(self.__start_end_points)
	def get_number_of_polygons(self):
		return self.__number_of_polygons
	def get_polygons(self):
		for i in range(0,self.__number_of_polygons):
			self.__polygons[i]=self.__string_to_points(self.__polygons[i])
		return self.__polygons