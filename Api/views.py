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


def generateNodeList(total_nodes_required, max_x, max_y):
    node_list = []
    for node in range(total_nodes_required):
        current_node_data = {
            "id": node,
            "yPos": random.randint(0, max_y),
            "xPos": random.randint(0, max_x),
            "text": generateNodeName(3)
        }
        node_list.append(current_node_data)
    return node_list


class GenerateNodes(TemplateView):

    def get(self, request, *args, **kwargs):
        total_nodes_required = int(float(request.GET.get('totalNodesRequired', 0)))
        max_x = int(float(request.GET.get('maxX', 0)))
        max_y = int(float(request.GET.get('maxY', 0)))

        global nodeStateData
        nodeStateData = generateNodeList(total_nodes_required, max_x, max_y)

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
        global topologyStateData
        topologyStateData = generateConnections()
        response = {
            "pathData": topologyStateData
        }
        return JsonResponse(response, status=200)


def generateConnections():
    global nodeStateData

    if len(nodeStateData) == 0:
        return "First, Create a Set of Nodes. Then Try Again"

    pathData = []

    unvisitiedNodes = [node for node in range(len(nodeStateData))]
    visitedNodes = []

    totalNodes = len(unvisitiedNodes)
    remainingNodes = len(unvisitiedNodes)

    while len(visitedNodes) < totalNodes - 1:
        source = unvisitiedNodes[random.randint(0, remainingNodes - 1)]

        #   Select Destination & Jingalala
        destination = unvisitiedNodes[random.randint(0, remainingNodes - 1)]

        while (destination == source):
            destination = unvisitiedNodes[random.randint(0, remainingNodes - 1)]

        if (random.randint(0, 1)):
            visitedNodes.append(source)
            unvisitiedNodes.remove(source)
        else:
            visitedNodes.append(destination)
            unvisitiedNodes.remove(destination)

        remainingNodes -= 1
        pathData.append({"source": source, "destination": destination, "weightData": random.randint(5, 50)})

    return pathData


class DiscoverRoute(TemplateView):

    def get(self, request, *args, **kwargs):
        global nodeData

        sourceId = int(float(request.GET.get('sourceId', 0)))
        destinationId = int(float(request.GET.get('destinationId', 0)))

        global nodeStateData
        global topologyStateData

        routeData = discoverRoute(sourceId, destinationId, nodeStateData, topologyStateData)

        response = {
            "RouteData": routeData,
        }

        return JsonResponse(response, status=200)


def discoverRoute(sourceId, destinationId, nodeStateData, topologyStateData):
    graph = Graph()

    adjacencyMatrix = generateAdjacencyMatrix(nodeStateData, topologyStateData)

    print(adjacencyMatrix)
    allPaths = graph.discoverRoutes(adjacencyMatrix, sourceId)

    pathTo = parseRoutes(allPaths)

    print("\n\n\n", pathTo, "\n\n\n")
    print("\n\n\n", destinationId, pathTo[int(destinationId)], "\n\n\n")

    return pathTo[int(destinationId)]
