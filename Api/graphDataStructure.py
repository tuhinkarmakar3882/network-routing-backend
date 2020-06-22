from collections import defaultdict


class Graph:
    def minDistance(self,dist,queue): 
        minimum = float("Inf") 
        min_index = -1
        for i in range(len(dist)): 
            if dist[i] < minimum and i in queue: 
                minimum = dist[i] 
                min_index = i 
        return min_index 

    def printPath(self, parent, j, path=""):
        if parent[j] == -1 : 
            path+=' ' + str(j)
            print (path,  end= " ")
            return path
        path+=' '+ (self.printPath(parent , parent[j],path) )
        path+=' ' + str(j)
        print (path) 
        return path
            

    def printSolution(self, dist, parent): 
        src = 0;
        temp = []
        print("Vertex \t\tDistance from Source\tPath") 
        for i in range(1, len(dist)): 
            print("\n{} --> {} \t\t{} \t\t".format(src, i, dist[i]), end="")
            temp.append(self.printPath(parent,i).strip())
        return temp


    def discoverRoutes(self, graph, src): 
        row = len(graph) 
        col = len(graph[0]) 
        dist = [float("Inf")] * row 
        parent = [-1] * row 
        dist[src] = 0
        queue = [] 
        for i in range(row): 
            queue.append(i)
        while queue: 
            u = self.minDistance(dist,queue) 
            queue.remove(u) 
            for i in range(col): 
                if graph[u][i] and i in queue: 
                    if dist[u] + graph[u][i] < dist[i]: 
                        dist[i] = dist[u] + graph[u][i] 
                        parent[i] = u 
        return(self.printSolution(dist,parent))


def parseRoutes(allPaths):
    pathTo = defaultdict(dict)
    pathData = []
    for path in allPaths:
        pathData = path.split(' ')
        source_vertex = int(pathData[0])
        destination_vertex= int(pathData[-1])
        routeJSON = []
        for node in range(len(pathData) - 1):
            edgeJSON = {
                "source": int(pathData[node]),
                "destination": int(pathData[node+1]),
            }
            routeJSON.append(edgeJSON)
        pathTo[destination_vertex] = routeJSON
    
    return pathTo


def generateAdjacencyMatrix(nodeStateData, topologyStateData):
    def initializeMatrix(totalVertices):
        l=[]
        for i in range(len(nodeStateData)):
            temp = []
            for j in range(len(nodeStateData)):
                temp.append(0)
            l.append(temp)
        return l

    adjacencyMatrix = initializeMatrix(len(nodeStateData))
    
    for topologyData in topologyStateData:
        source = topologyData["source"]
        destination = topologyData["destination"]
        weight = topologyData["weightData"]
        adjacencyMatrix[source][destination] = weight
        adjacencyMatrix[destination][source] = weight

    return adjacencyMatrix
    

'''
node_data = [
        {
            "id": node,
            "yPos": NOT INTERESTED,
            "xPos": NOT INTERESTED,
            "text": NOT INTERESTED
        },
    ]

AllPathData = [
        {
            "source":source,
            "destination": destination,
            "weightData": weightValue
        },
    ]
'''        