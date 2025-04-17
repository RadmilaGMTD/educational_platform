from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig

from .views import (CourseViewSet, LessonCreateApiView, LessonDestroyApiView, LessonListApiView, LessonRetrieveApiView,
                    LessonUpdateApiView)

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r"", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
    path("lessons/", LessonListApiView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lessons_get"),
    path("lessons/update/<int:pk>/", LessonUpdateApiView.as_view(), name="lessons_update"),
    path("lessons/delete/<int:pk>/", LessonDestroyApiView.as_view(), name="lessons_delete"),
] + router.urls
