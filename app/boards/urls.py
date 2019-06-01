from django.urls import path, include
from rest_framework.routers import DefaultRouter
from boards import views

router = DefaultRouter()
router.register('modules', views.ModuleViewSet)
router.register('locations', views.LocationViewSet)
router.register('lessons', views.LessonViewSet)
router.register('whiteboards', views.BoardViewSet)
router.register('lecturers', views.LecturerViewSet)

app_name = 'boards'

# print(router.urls)

urlpatterns = [
    path('', include(router.urls))
]

