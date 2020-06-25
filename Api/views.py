import random

from django.http import JsonResponse
from django.views.generic import TemplateView

from .graphDataStructure import Graph, parseRoutes, generateAdjacencyMatrix

nodeStateData = []
topologyStateData = []


def generateNodeName(char_count):
    name = ""
    for character in range(char_count):
        name += chr(random.randint(65, 90))
    return name


def generateNodeList(totalNodesRequired, xMax, yMax):
    node_list = []
    for node in range(totalNodesRequired):
        current_node_data = {
            "id": node,
            "yPos": random.randint(0, yMax),
            "xPos": random.randint(0, xMax),
            "text": generateNodeName(3)
        }
        node_list.append(current_node_data)
    return node_list


class GenerateNodes(TemplateView):

    def get(self, request, *args, **kwargs):
        totalNodesRequired = int(float(request.GET.get('totalNodesRequired', 0)))
        xMax = int(float(request.GET.get('maxX', 0)))
        yMax = int(float(request.GET.get('maxY', 0)))

        global nodeStateData
        nodeStateData = generateNodeList(totalNodesRequired, xMax, yMax)

        response = {
            "NodeData": nodeStateData,
        }

        return JsonResponse(response, status=200)


class ClearState(TemplateView):
    def get(self, request, *args, **kwargs):
        reset()
        response = {
            "message": "Success"
        }
        return JsonResponse(response, status=200)


def reset():
    global nodeStateData
    global topologyStateData
    nodeStateData = []
    topologyStateData = []


class GenerateTopology(TemplateView):
    def get(self, request, *args, **kwargs):
        iterations = request.GET.get('', 1)
        global topologyStateData
        topologyStateData = generateConnections(iterations)
        response = {
            "pathData": topologyStateData
        }
        return JsonResponse(response, status=200)


def generateConnections(iterations=1):
    global nodeStateData

    if len(nodeStateData) == 0:
        return "First, Create a Set of Nodes. Then Try Again"

    pathData = []

    for i in range(iterations):
        unvisitedNodes = [node for node in range(len(nodeStateData))]
        visitedNodes = []

        totalNodes = len(unvisitedNodes)
        remainingNodes = len(unvisitedNodes)

        while len(visitedNodes) < totalNodes - 1:
            source = unvisitedNodes[random.randint(0, remainingNodes - 1)]
            destination = unvisitedNodes[random.randint(0, remainingNodes - 1)]

            while destination == source:
                destination = unvisitedNodes[random.randint(0, remainingNodes - 1)]

            if random.randint(0, 1):
                visitedNodes.append(source)
                unvisitedNodes.remove(source)
            else:
                visitedNodes.append(destination)
                unvisitedNodes.remove(destination)

            remainingNodes -= 1
            pathData.append({
                "source": source,
                "destination": destination,
                "weightData": random.randint(5, 50)
            })

    return pathData


class DiscoverRoute(TemplateView):

    def get(self, request, *args, **kwargs):
        sourceId = int(float(request.GET.get('sourceId', 0)))
        destinationId = int(float(request.GET.get('destinationId', 0)))

        global nodeStateData
        global topologyStateData

        routeData = discoverRoute(sourceId, destinationId, nodeStateData, topologyStateData)

        response = {
            "RouteData": routeData,
        }

        return JsonResponse(response, status=200)


def discoverRoute(sourceId, destinationId, nodeData, topologyData):
    graph = Graph()

    adjacencyMatrix = generateAdjacencyMatrix(nodeData, topologyData)

    # print(adjacencyMatrix)
    allPaths = graph.discoverRoutes(adjacencyMatrix, sourceId)

    pathTo = parseRoutes(allPaths)

    # print("\n\n\n", pathTo, "\n\n\n")
    # print("\n\n\n", destinationId, pathTo[int(destinationId)], "\n\n\n")

    return pathTo[int(destinationId)]
