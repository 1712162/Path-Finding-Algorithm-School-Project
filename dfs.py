import numpy as np
file=open("in.txt","r")
mn=file.readline()
se=file.readline()

n=file.readline()
ob=[]
for i in range(0,int(n)):
	ob.append(file.readline());
file.close()
se=se.split()
mn=mn.split()
for i in range(0,int(n)):
	ob[i]=ob[i].split();
#vẽ viền của bản đồ
def createbox(n,m):
	a=np.zeros((n,m),int)
	for i in range(0,n):
		a[i][0]=-1
		a[i][m-1]=-1
	for i in range(0,m):
		a[0][i]=-1
		a[n-1][i]=-1
	return a

map=createbox(int(mn[1])+1,int(mn[0])+1)


#vẽ vật thể
for i in range(0,len(ob)):
	for j in range(0,len(ob[i]),2):
		
		x1=int(ob[i][j])
		y1=int(ob[i][j+1])
		map[y1][x1]=-1
		if(j+2>=len(ob[i])):
			x2=int(ob[i][0])
			y2=int(ob[i][1])
		else:
			x2=int(ob[i][j+2])
			y2=int(ob[i][j+3])
		if(x1==x2):
			if(y1<y2):
				for t in range(y1,y2+1):
					map[t][x1]=-1
			else:
				for t in range(y2,y1+1):
					map[t][x1]=-1
		else:
			a=(y2-y1)/(x2-x1)
			b=(int)(y1-x1*a)
			if(x1<x2):
				for t in range(x1,x2+1):
					map[int(t*a+b)][t]=-1
			else:
				for t in range(x2,x1+1):
					map[int(t*a+b)][t]=-1

#phần xác định vật thể di chuyển
#medium xác định cạnh trên cạnh dưới
medium=0
for i in range (1,len(ob[0]),2):
	medium=medium+int(ob[0][i])
medium=medium/(len(ob[0])/2)

ob1=[[],[],[]] #vật thể di chuyển
#thêm điểm theo nguyên tắc, thêm vào ob1[0] nếu cạnh trên, 1 nếu cạnh dưới, 2 là cá điểm còn lại
for j in range(0,len(ob[0]),2):
	x1=int(ob[0][j])
	y1=int(ob[0][j+1])
	
	if(j+2>=len(ob[0])):
		x2=int(ob[0][0])
		y2=int(ob[0][1])
	else:
		x2=int(ob[0][j+2])
		y2=int(ob[0][j+3])
	if(x1==x2):
		if(y1<y2):
			for t in range(y1,y2+1):
				ob1[2].append(x1)
				ob1[2].append(t)
		else:
			for t in range(y2,y1+1):
				ob1[2].append(x1)
				ob1[2].append(t)
	else:
		a=(int(y2-y1)/(x2-x1))
		b=(int)(y1-x1*a)
		if(x1<x2):
			for t in range(x1,x2+1):
				h=int(t*a+b)
				if(h<medium):
					ob1[0].append(t)
					ob1[0].append(h)
				else:
					ob1[1].append(t)
					ob1[1].append(h)
		else:
			for t in range(x2,x1+1):
				h=int(t*a+b)
				if(h<medium):
					ob1[0].append(t)
					ob1[0].append(h)
				else:
					ob1[1].append(t)
					ob1[1].append(h)

#xét xem có thể lên hay xuống
def updown(a,b,t):
	for i in range(0,len(b),2):
		x=b[i]
		y=b[i+1]+t
		if(a[y][x]!=0):
			return False
	return True
#hàm di chuyển
def move(a,b,n,m):
	t=0
	if(updown(a,b[1],1)):
		t=1
	elif(updown(a,b[0],-1)):
		t=-1
	if(t!=0):
		for i in range(0,len(b)):
			for j in range(1,len(b[i]),2):
				a[b[i][j]][b[i][j-1]]=0
		for i in range(0,len(b)):
			for j in range(1,len(b[i]),2):
				b[i][j]+=t
		for i in range(0,len(b)):
			for j in range(1,len(b[i]),2):
				a[b[i][j]][b[i][j-1]]=-1
	for i in range(0,n):
		a[i][0]=-1
		a[i][m-1]=-1
	for i in range(0,m):
		a[0][i]=-1
		a[n-1][i]=-1

#dfs với vật thể di chuyển
def find(matrix,o,x,y,x1,y1,t):

	if(matrix[y][x]==0):
		matrix[y][x]=t
	else:
		return
	t=t+1
	if(x==x1 and y==y1):
		return True
	move(matrix,ob1,len(matrix),len(matrix[0])) #hàm di chuyển
	if(matrix[y+1][x]==0 ):
		if(find(matrix,o,x,y+1,x1,y1,t)):return True
	if(matrix[y][x+1]==0 ):
		if(find(matrix,0,x+1,y,x1,y1,t)):return True
	if(matrix[y-1][x]==0):
		if(find(matrix,0,x,y-1,x1,y1,t)):return True
	if(matrix[y][x-1]==0 ):
		if(find(matrix,0,x-1,y,x1,y1,t)):return True
	

t=1
find(map,ob1,int(se[0]),int(se[1]),int(se[2]),int(se[3]),t)
print(map)