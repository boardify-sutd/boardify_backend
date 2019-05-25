from django.urls import path, include
from rest_framework.routers import DefaultRouter
from boards import views

router = DefaultRouter()
router.register('modules', views.ModuleViewSet)

app_name = 'boards'

# print(router.urls)

urlpatterns = [
    path('', include(router.urls))
]