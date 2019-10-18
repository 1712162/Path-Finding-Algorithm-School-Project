class Function_switcher(object):
	def __init__(self,shortest_path,start,end,width,height,polygons):
		self.shortest_path=shortest_path
		self.start=start
		self.end=end
		self.width=width
		self.height=height
		self.polygons=polygons

	def get_function(self,i):
		method_name='level_'+str(i)
		method=getattr(self,method_name,lambda :print('Invalid Function'))
		return method()

	def __draw_path(self,path):
		if(path) :
			window = Graphic2D(self.width,self.height)
			window.setup()
			window.draw_output(self.start,self.end,Graph2D.points_to_polygons(polygons),path)
			arcade.run()
		else :
			print("No solution")

	def level_0(self):
		return exit()

	def level_1(self):
		path =  shortestPath.a_start_search( self.start,self.end )
		self.__draw_path(path)

	def level_2(self):
		path1 =  shortestPath.a_start_search( self.start,self.end )
		path2 =  shortestPath.BFS( self.start,self.end )
		path3 =  shortestPath.DFS( self.start,self.end )
		self.__draw_path(path1)
		self.__draw_path(path2)
		self.__draw_path(path3)
		print('two')
		
	def level_3(self):
		print('three')

	def level_4(self):
		print('four')
