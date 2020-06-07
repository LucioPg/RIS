from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='dashboard'),
    path('categoria/<int:id>', views.categoria, name='categoria'),
    path('categoria/<int:id>/update', views.categoria_update, name='categoria_update'),
    path('categoria/<int:id>/delete', views.categoria_delete, name='categoria_delete'),
    path('categorie/', views.categorie, name='categorie'),
    path('categorie/create', views.categorie_create, name='categorie_create'),
    path('prodotto/create', views.prodotto_create, name='prodotto_create'),
    path('prodotti/', views.prodotti, name='prodotti'),
    path('prodotto/<int:id>', views.prodotto, name='prodotto'),
    path('prodotto/<int:id>/update', views.prodotto_update, name='prodotto_update'),
    path('prodotto/<int:id>/delete', views.prodotto_delete, name='prodotto_delete'),
    path('inventario/', views.InventarioListView.as_view(), name='categoria_changelist'),
    path('inventario/add/', views.InventarioCreateView.as_view(), name='item_add'),
    path('inventario/<int:pk>/', views.InventarioUpdateView.as_view(), name='item_change'),
    path('ajax/load_products/', views.ajax_load_products, name='ajax_load_products'),
]
