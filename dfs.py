
def dfs(matrix,x_start,y_start,x_end,y_end):
	path=[]
	queue=[(x_start,y_start)]
	while (len(queue)!=0):
		current=queue.pop(0)
		path.append(current)
		x,y=current
		if(x==x_end and y==y_end):
			print(1)
			break
		matrix[y][x]=1
		if(matrix[y][x-1]!=0 and matrix[y-1][x]!=0 and matrix[y+1][x]!=0 and matrix[y][x+1]!=0):
			path.pop(len(path)-1)
		if(matrix[y][x-1]==0):
			queue.insert(0,(x-1,y))
		if(matrix[y-1][x]==0):
			queue.insert(0,(x,y-1))
		if(matrix[y][x+1]==0):
			queue.insert(0,(x+1,y))
		if(matrix[y+1][x]==0):
			queue.insert(0,(x,y+1))
	return path
