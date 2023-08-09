from django.urls import path
from . import views

urlpatterns = [
    path('', views.userregister, name="user-register"),
    path('login/', views.userlogin, name="user-login"),
    path('logout/', views.userlogout, name="user-logout"),
    path('product_list/<str:userid>/',views.product_list, name="product-list"),
    path('product_list/<str:userid>/addproduct/',views.add_product,name="add-product")
]