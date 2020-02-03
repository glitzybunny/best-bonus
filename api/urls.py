from django.urls import path, include
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register('user', views.UserViewSet)
router.register('group', views.GroupViewSet)
router.register('suplier', views.SuplierViewSet)
router.register('bonus', views.BonusViewSet)

# API
urlpatterns = [
    path('', include(router.urls)),
    path('auth', include('rest_framework.urls')),
    path('search', views.SearchView.as_view()),
    path('filter', views.FilterView.as_view()),
]