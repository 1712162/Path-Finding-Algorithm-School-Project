def show_menu():
	for i in range(4):
		level=i+1
		display_line=str(level)+'. level '+str(level)
		print(display_line)

def create_graph2d(width,height):
	graph2D = Graph2d(width+1,height+1)
	graph2D.polygons_to_coordinate(polygons)
	return graph2D

def main():
	while 1:
		#nhap file
		file=input('Enter your file path: ')

		#get data from file
		width,height,start,end,polygons = read_file(file)

		graph2d=create_graph2d(width,height)
		shortest_path=ShortestPath(graph2D)
		print('\n')
	
		#show menu + get number_of_function
		show_menu()
		number_of_function=input('Function: ')
		print ('\n')

		#run function selected
		function_switcher=fs.Function_switcher(shortest_path,start,end,width,height,polygons)
		run_function=function_switcher.get_function(number_of_function)
		wait=input('Press any key to continue\n')

if __name__ == "__main__":
    main()