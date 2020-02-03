from django.urls import path
from core import views


urlpatterns = [
    path('', views.all_bonuses, name='rating'),

    # Ajax endpoints
    path('ajax-search/', views.search_ajax),
    path('ajax-filter/', views.filter_ajax),
]



