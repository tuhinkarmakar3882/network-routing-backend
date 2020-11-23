# Network-Routing-Visualizer-Backend

## About the Project
This is a custom made Network Routing Visualizer which is completely made from scratch using Python and JavaScript. This aim to solve the problem of simulating the routing algorithms with maximum possible extensibility.

To Implement Your Custom Discovery Logic, Use this Template

```python
from collections import defaultdict


class Graph:
    # Todo - Include Your Own Content....

    def discover_routes(self, graph, src):
        route_array = []
        # Todo - Add your own Logic
        return self.serialize_into_json(route_array)

    def serialize_into_json(self, route_array):
        json_path = defaultdict(list)

        #   Todo - Make This json_path Look like this.
        """
        [
            {
                "source": Source Node ID,
                "destination": Dest. Node ID,
                "weightData": value,
            },
            {
                "source": <Integer>,
                "destination": <Integer>,
                "weightData": <Integer>,
            },
            .
            ..
            ...
        ]
        """

        return json_path

    def initializeMatrix(self, totalVertices):
        blankList = []
        for i in range(totalVertices):
            tempArray = []
            for j in range(totalVertices):
                tempArray.append(0)
            blankList.append(tempArray)
        return blankList

    def generateAdjacencyMatrix(self, nodeStateData, topologyStateData):
        adjacencyMatrix = self.initializeMatrix(len(nodeStateData))

        #   Todo
        #    - Either Create The Matrix
        #    - OR -
        #    - Do your Own Stuff... may be Adjacency List??.. Whichever makes more sense...

        return adjacencyMatrix

    '''
    Global Node Data Looks Like = [
            {
                "id": node,
                "yPos": NOT INTERESTED,
                "xPos": NOT INTERESTED,
                "text": NOT INTERESTED
            },
        ]

    Global Topology Data Looks Like = [
            {
                "source":source,
                "destination": destination,
                "weightData": weightValue
            },
        ]
    '''
```
