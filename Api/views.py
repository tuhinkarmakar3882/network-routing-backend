import random

from django.http import JsonResponse
from django.views.generic import TemplateView

nodeStateData = []
topologyStateData = []
name_to_id_mapping = {}


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


def createMapping(data):
    global name_to_id_mapping
    for i in range(len(data)):
        name_to_id_mapping[data[i]['text']] = i


class GenerateNodes(TemplateView):

    def get(self, request, *args, **kwargs):
        try:
            totalNodesRequired = int(float(request.GET.get('totalNodesRequired', 0)))
            xMax = int(float(request.GET.get('maxX', 0)))
            yMax = int(float(request.GET.get('maxY', 0)))

            global nodeStateData
            nodeStateData = generateNodeList(totalNodesRequired, xMax, yMax)

            createMapping(nodeStateData)

            response = {
                "NodeData": nodeStateData,
                "message": 'Nodes Generated'
            }
            return JsonResponse(response, status=200)
        except:
            response = {
                "message": 'Error!'
            }
            return JsonResponse(response, status=404)


class TestConnection(TemplateView):
    def get(self, request, *args, **kwargs):
        response = {
            "message": "Ready!"
        }
        return JsonResponse(response, status=200)


def generateConnections(iterations):
    global nodeStateData

    pathData = []

    for i in range(int(iterations)):
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


class GenerateTopology(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            iterations = request.GET.get('totalIterations', 1)
            # print(iterations, request.GET['totalIterations'])
            global topologyStateData
            if len(nodeStateData) != 0:
                topologyStateData = generateConnections(iterations)
                response = {
                    "pathData": topologyStateData,
                    "message": 'Topology Generated'
                }
                return JsonResponse(response, status=200)
            else:
                response = {
                    "message": 'First, Create a Set of Nodes. Then Try Again'
                }
                return JsonResponse(response, status=404)
        except:
            response = {
                "message": 'Invalid Request!'
            }
            return JsonResponse(response, status=404)


def consumable(route):
    if len(route) > 1:
        global name_to_id_mapping
        routeData = []

        for node in range(len(route) - 1):
            edge = {
                "source": name_to_id_mapping[route[node]],
                "destination": name_to_id_mapping[route[node + 1]],
                "weightData": 1
            }
            routeData.append(edge)
        return routeData
    else:
        return False


def discoverRoute(source_name, destination_name, nodeData, maxRange):
    import time
    def ReturnCoordinates(D):
        L = (D[(list(D.keys())[0])])
        L1 = []
        for i in range(len(L)):
            L1.append([L[i]["xPos"], L[i]["yPos"]])
        return (L1)

    def ReturnNodeNameAccess(D):
        L = (D[(list(D.keys())[0])])
        L1 = []
        for i in range(len(L)):
            L1.append(L[i]["text"])
        return (L1)

    D = {"NodeData": nodeData}
    n = len(nodeData)  # no. of nodes
    Coord = (ReturnCoordinates(D))
    Names = (ReturnNodeNameAccess(D))
    print(Coord)
    print(Names)
    S = source_name
    k = Names.index(S)
    D = destination_name
    Route = [S]
    Dest = str()
    max_range = int(maxRange)
    stop_searching = False
    Discard = []
    r = 1  # neighbourhood_radius
    start_time = time.time()

    while Route[len(Route) - 1] != D:
        k = Names.index(S)
        Pingn = {}
        print("r=>", r)
        print("Currently Prcessing =>", S)
        for i in range(n):
            if i != k and Names[i] not in Route and Names[i] not in Discard:
                dist = ((Coord[k][0] - Coord[i][0]) ** 2 + (Coord[k][1] - Coord[i][
                    1]) ** 2) ** 0.5  # Distance_of_two_nodes (Euclidean for higher dimensions)
                if dist <= r:
                    Pingn[Names[i]] = dist
                    print(Pingn)
        if len(Pingn) == 0:
            if stop_searching and len(Route) == 1:
                print("No nodes in current range for this source")
                print("No path exists, taking this node as the source.")
                break
            elif len(Route) > 1:
                S = Route.pop()
                Discard.append(S)
                S = Route[len(Route) - 1]
                print("Route", Route)
                print("Discard", Discard)
            else:
                print("Checking till max range...")
                r += (max_range - r)
                if r >= max_range:
                    stop_searching = True
        elif D in (list(Pingn.keys())):
            Route.append(D)
        else:
            Mindist = min(list(Pingn.values()))
            print("Nodes available in ping range of source:", Pingn)
            print(Mindist)
            Dest = (list(Pingn.keys())[list(Pingn.values()).index(Mindist)])
            Route.append(Dest)
            S = Route[len(Route) - 1]
    else:
        print("GreyWolf suggests the route order:", (Route))

    end_time = time.time()

    print("Total Time Taken {} seconds".format(abs(start_time - end_time)))
    print("Final Route =>", Route)
    # GreyWolf Begins
    # MZU -> XOP
    print("I worked")
    return consumable(Route)

    # graph = Graph()

    # adjacencyMatrix = generateAdjacencyMatrix(nodeData, topologyData)

    # print(adjacencyMatrix)
    # allPaths = graph.discoverRoutes(adjacencyMatrix, sourceId)

    # pathTo = parseRoutes(allPaths)

    # print("\n\n\n", pathTo, "\n\n\n")
    # print("\n\n\n", destinationId, pathTo[int(destinationId)], "\n\n\n")

    # return pathTo[int(destinationId)]


class DiscoverRoute(TemplateView):

    def get(self, request, *args, **kwargs):
        import json
        sourceName = str(request.GET.get('sourceId', 0))
        destinationName = str(request.GET.get('destinationId', 0))
        maxRange = str(request.GET.get('maxRange', 100))
        nodeData = request.GET.get('nodeData', [])

        global nodeStateData
        print(json.loads(nodeData) == nodeStateData)
        print(sourceName, destinationName)
        # global nodeStateData
        global topologyStateData
        try:
            routeData = discoverRoute(sourceName, destinationName, json.loads(nodeData), maxRange)
            if not routeData:
                raise IOError
            response = {
                "RouteData": routeData,
                "message": "Done",
            }
            return JsonResponse(response, status=200)
        except:
            response = {
                "message": "No Route Found!",
            }
            return JsonResponse(response, status=404)


def reset():
    global nodeStateData
    global topologyStateData
    nodeStateData = []
    topologyStateData = []


class ClearState(TemplateView):
    def get(self, request, *args, **kwargs):
        reset()
        response = {
            "message": "Success"
        }
        return JsonResponse(response, status=200)
