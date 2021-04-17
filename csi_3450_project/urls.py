"""csi_3450_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from classicmodels import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='classicmodels/userLogin.html'),name="Login"),
    path('productdetails/', views.product_details_view, name='productdetails'),
    path('userproductquery', views.user_product_query_view, name = 'userproductquery'),
    path('userproductdetails', views.user_product_details_view, name = 'userproductdetails'),
    path('conversion/', views.conversion, name='conversion'),
    path('deposit/', views.deposit, name='deposit'),
    path('details/', views.details, name='details'),
    path('homepage/', views.homepage, name='homepage'),
    path('logout/', views.logout, name='logout'),
    path('transfer/', views.transfer, name='transfer'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('signup/', views.signup, name='signup'),
    

]
