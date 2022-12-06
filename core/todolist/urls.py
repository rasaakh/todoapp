from django.urls import path, include
from .views import (
    TaskListAll,
    TaskCreate,
    TaskComplete,
    TaskUpdate,
    DeleteView,
    TaskListUser,
    test,
)

app_name = "todolist"
urlpatterns = [
    path("", TaskListAll.as_view(), name="index"),
    path("task/", TaskListUser.as_view(), name="task_list_user"),
    path("create/", TaskCreate.as_view(), name="create_task"),
    path("update/<int:pk>/", TaskUpdate.as_view(), name="update_task"),
    path("complete/<int:pk>/", TaskComplete.as_view(), name="complete_task"),
    path("delete/<int:pk>/", DeleteView.as_view(), name="delete_task"),
    path("test-weather/", test, name="test"),
    path("api/v1/", include("todolist.api.v1.urls")),
]
