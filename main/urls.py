from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='dashboard'),
    path('categoria/<int:id>', views.categoria, name='categoria'),
    path('categorie/', views.categorie, name='categorie'),
    path('categorie/create', views.categorie_create, name='categorie_create'),
    path('prodotto/create', views.prodotto_create, name='prodotto_create'),
    path('prodotti/', views.prodotti, name='prodotti'),
    path('prodotto/<int:id>', views.prodotto, name='prodotto'),
    path('prodotto/<int:id>/update', views.prodotto_update, name='prodotto'),
]
