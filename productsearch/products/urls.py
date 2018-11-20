from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('search/advanced/', views.advanced_search, name='advanced_search'),
]
