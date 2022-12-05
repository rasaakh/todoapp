# from rest_framework.response import Response
from .serializers import TaskSerializer,WeatherSerializer
from ...models import Task
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from .permission import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import requests

# from .pagenations import DefultPagination


class TaskModelViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = {"title": ["exact"]}
    search_fields = ["title"]
    ordering_fields = ["updated_date"]


class WeatherApiView(generics.RetrieveAPIView):
    serializer_class = WeatherSerializer
    @method_decorator(cache_page(timeout=60 * 20))
    def get(self, request, *args, **kwargs):
        response = requests.get(
            "http://api.openweathermap.org/data/2.5/weather?q=Tehran&APPID=274bc6d6b1bf85c2abf70a4b9e2634c3"
        ).json()
        return Response(response)
