from django.http import JsonResponse
from django.views.generic import TemplateView
import random


def generate_name(char_count):
    name = ""
    for character in range(char_count):
        name += chr(random.randint(65, 90))
    return name


def generate_node_list(total_nodes_required):
    node_list = []
    for node in range(total_nodes_required):
        current_node_data = {
            "id": node,
            "yPos": random.randint(0, 600),
            "xPos": random.randint(0, 1350),
            "text": generate_name(3)
        }
        node_list.append(current_node_data)
    return node_list


class GenerateNodes(TemplateView):

    def get(self, request, *args, **kwargs):
        global nodeData

        total_nodes_required = int(request.GET.get('totalNodesRequired', 0))

        response = {
            "NodeData": generate_node_list(total_nodes_required)
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
    pass
    # counter = 0
