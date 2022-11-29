from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import WeatherApiView
app_name = "api-v1"


urlpatterns = [   
    path("weather/", WeatherApiView.as_view(), name="weather"),
]

router = DefaultRouter()
router.register("task", views.TaskModelViewSet, basename="task")

urlpatterns += router.urls

