from django.urls import path
from . import viewsets

urlpatterns = [
    path('get-endpoints/', viewsets.GetEndpointsViewSet.as_view(), name='get_endpoints'),
]