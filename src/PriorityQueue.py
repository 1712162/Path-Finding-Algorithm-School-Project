import heapq
class PriorityQueue:
    def __init__(self):
        self.elements = []
    #Checking priority queue is empty
    def empty(self):
        return len(self.elements) == 0

    # Push item with priority into queue
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    # Pop and get first item out of queue
    def get(self):
        return heapq.heappop(self.elements)[1]