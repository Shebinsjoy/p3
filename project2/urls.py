"""
URL configuration for project2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from login import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('signup/',views.signup,name='signup'),

    path('', views.signin,name='signin'),

    path('home/',views.home,name='home'),

    path('logout/',views.signout, name='signout'),

    path('adminn/',views.adminpage,name='admin'),

    path('admin_logout',views.admin_logout,name='admin_logout'),

    path('dashboard',views.dashboard,name = 'dashboard'),

    path('add/',views.add,name='add'),

    path('edit/',views.edit,name = 'edit'),

    path('update/<str:id>',views.update,name='update'),
    
    path('delete/<str:id>',views.delete,name='delete'),

    path('search/', views.search, name='search'),

    
]
