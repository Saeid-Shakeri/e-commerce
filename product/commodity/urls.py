from django.urls import path
from .views import (CategoryListView, ProductListView,
        ProductDetailView, ProductSearchView, ProductDetailAdminView, ProductListCreateView,
        CategoryListCreateView)


urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('product_search/', ProductSearchView.as_view(), name='product-search'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('category-admin', CategoryListCreateView.as_view(), name='category-admin'),
    path('product-list-admin/', ProductListCreateView.as_view(), name='product-list-admin'),
    path('product-detail-admin/', ProductDetailAdminView.as_view(), name='product-detail-admin'),

]
