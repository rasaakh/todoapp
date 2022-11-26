from django.urls import path, include
from .views import (
    TaskList,
    TaskCreate,
    TaskComplete,
    TaskUpdate,
    DeleteView,
)

app_name = "todolist"
urlpatterns = [
    path("", TaskList.as_view(), name="task_list"),
    path("create/", TaskCreate.as_view(), name="create_task"),
    path("update/<int:pk>/", TaskUpdate.as_view(), name="update_task"),
    path("complete/<int:pk>/", TaskComplete.as_view(), name="complete_task"),
    path("delete/<int:pk>/", DeleteView.as_view(), name="delete_task"),
    path("api/v1/", include("todolist.api.v1.urls")),
]
