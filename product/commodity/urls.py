from django.urls import path
from .views import (CategoryListView, ProductListView,
        ProductDetailView, ProductSearchView, ProductDetailAdminView, ProductListCreateView)


urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('product_search/', ProductSearchView.as_view(), name='product-search'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product_create/', ProductListCreateView.as_view(), name='product-create'),
    path('product_detail_admin/', ProductDetailAdminView.as_view(), name='product-detail-admin'),

]
