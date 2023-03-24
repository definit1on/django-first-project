from django.urls import path
from . import views

app_name = 'telemart'

urlpatterns = [
    path('', views.index, name='index'),
    path('company/all/', views.CompanyListView.as_view(), name='company-list'),
    path('company/<int:pk>/', views.CompanyDetailView.as_view(), name='company-detail'),
    path('product/all/', views.ProductListView.as_view(), name='product-list'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='wishlist-add'),
    path('wishlist/rmv/<int:product_id>/', views.remove_from_wishlist, name='wishlist-rmv'),
    path('search/match/', views.search, name='search'),
    path('logout/user/', views.logout_user, name='logout-user'),
    path('login/page/', views.login_page, name='login-page'),
    path('login/user/', views.login_user, name='login-user'),
    path('comment/add/<int:product_id>/', views.add_comment, name='add-comment'),
    path('add/company/new', views.add_new_company, name='add-new-company'),
    path('add/product/new', views.add_new_product, name='add-new-product'),
    path('settings/config/', views.config, name='config'),
    # API
    path('api/product/all/', views.ProductListAPIView.as_view(), name='api-product-list')
]