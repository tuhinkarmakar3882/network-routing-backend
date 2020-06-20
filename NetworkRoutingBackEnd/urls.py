"""NetworkRoutingBackEnd URL Configuration"""
from django.contrib import admin
from django.urls import path, include

import Api.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(Api.urls)),
]
