app_name = 'shop'
from django.urls import path
from shop import views
from django.conf import settings
from django.conf.urls.static import static
from shop.views import IndexView, ProductDetailView
from shop.views import (
    IndexView,
    ProductDetailView,
    ProductListView,
    ProductImagesView,
    ECustomersView,
    CustomerCreateView,
    CustomersDetailView,
    CustomerUpdateView,
    CustomerDeleteView,
)


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('product/details/<int:pk>', ProductDetailView.as_view(), name='product_details'),
    path('product/details/html/',   views.product_details_html, name='product_details_html'),
    path('product/details/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('products-of-category/<int:category_id>/', ProductListView.as_view(), name='product_list'),
    path('products-of-category/<int:category_id>/', ProductListView.as_view(), name='product_of_category'),
    path('product/images/<int:pk>/', ProductImagesView.as_view(), name='product_images'),
    path('e_customers/', ECustomersView.as_view(), name='e_customers'),
    path('customer_add/', CustomerCreateView.as_view(), name='customers_add'),
    path('customer_details/<int:pk>/', CustomersDetailView.as_view(), name='customer_details'),
    path('customer_update/<int:pk>/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customer_delete/<int:pk>/', CustomerDeleteView.as_view(), name='customer_delete'),
    path('product_list/', views.product_list_html, name='product_list_html'),
    path('export-data/',views.export_data,name='export_data'),





]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
