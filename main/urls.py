from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='dashboard'),
    path('categoria/<int:id>', views.categoria, name='categoria'),
    path('categorie/', views.categorie, name='categorie'),
]
