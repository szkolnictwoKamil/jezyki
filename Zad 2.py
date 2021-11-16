visited = []

class Graph:
    def __init__(self):
        self.graph = {"45": ["Anna", "1a"], "Anna": ["45"], "1a": ["45"]}

    def add_v(self, v):
        if v not in self.graph:
            self.graph[v] = []
        else:
            print("Wierzchołek już istnieje")

    def add_e(self, e):
        e = set(e)
        v1, v2 = tuple(e)
        for x, y in [(v1, v2), (v2, v1)]:
            if x in self.graph and y in self.graph:
                self.graph[x].append(y)
            else:
                print("Krawędź nie może zostać dodana")

    def edges(self, v):
        return self.graph[v]
        
    def all_vertices(self):
        return set(self.graph.keys())

    def remove_v(self, v):
        if v  in self.graph:
            self.graph.pop(v)
            for v2 in self.graph:
                if v in self.graph[v2]:
                    self.graph[v2].remove(v)
        else:
            print("Wierzchołek nie istnieje")

    def remove_e(self,e):
        e = set(e)
        v1, v2 = tuple(e)
        for x, y in [(v1, v2), (v2, v1)]:
            if x in self.graph and y in self.graph:
                self.graph[x].remove(y)
            else:
                print("Krawędź nie może zostać usunięta")

    def __iter__(self, list0):
        self.list0 = iter(list0)
        return self.list0
    
    def __next__(self):
        return next(self.list0)

    def DFS(self, v):
        if v not in visited:
            visited.append(v)
            for v2 in self.graph[v]:
                self.DFS(v2)
        return self.__iter__(visited)

    def BFS(self, v):
        visited = []
        queue = []
        queue.append(v)
        visited.append(v)
        self.list1 = []
        while len(queue) > 0:
            s = queue.pop(0)
            self.list1.append(s)
            for i in self.graph[s]:
                if i not in visited:
                    queue.append(i)
                    visited.append(i)
        self.iterator = iter(self.list1)
        return self.iterator
 

graph = Graph()
print(graph.graph)
graph.add_v(2)
print(graph.graph)
graph.add_e(("45",2))
print(graph.graph)
graph.remove_e(("45",2))
print(graph.graph)
print(graph.edges("45"))
print(graph.all_vertices())
per = graph.DFS("45")
try:
    while per :
        print(next(per))
except StopIteration:
    pass
iterator = graph.BFS("45")
try:
    while iterator :
        print(next(iterator))
except StopIteration:
    pass
