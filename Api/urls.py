"""API BackEnd URL Configuration"""
from django.urls import path, include
from .views import GenerateNodes, ClearState, GenerateTopology

urlpatterns = [
    path('', GenerateNodes.as_view()),
    path('generateTopology/', GenerateTopology.as_view()),
    path('clear/', ClearState.as_view()),
]
