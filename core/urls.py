from django.urls import path

from .views import (HomeView, ProductCreateView, ProductDetailView,
                    ProductListView, ProductStockOutListView, ReviewUpdateView)

app_name = 'core'

urlpatterns = [
    path('produtos/', ProductListView.as_view(), name='product_list'),
    path('produto/novo/', ProductCreateView.as_view(), name='product_create'),
    path('produto/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('produto/<int:pk>/historico/', ProductStockOutListView.as_view(), name='product_stockout_list'),
    path('avaliacao/<int:pk>/editar/', ReviewUpdateView.as_view(), name='review_edit'),
    path('', HomeView.as_view(), name='home'),
]
