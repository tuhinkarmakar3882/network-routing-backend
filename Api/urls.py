"""API BackEnd URL Configuration"""
from django.urls import path, include
from .views import GenerateNodes, ClearState

urlpatterns = [
    path('', GenerateNodes.as_view()),
    path('clear/', ClearState.as_view()),
]
