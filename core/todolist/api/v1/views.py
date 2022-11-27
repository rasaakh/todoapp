# from rest_framework.response import Response
from .serializers import TaskSerializer
from ...models import Task
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from .permission import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

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
