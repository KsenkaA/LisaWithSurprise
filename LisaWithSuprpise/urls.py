"""LisaWithSuprpise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from data import views
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', views.test),
    path('', views.index),
    path('current_sprint/', views.current_sprint),
    path('all_sprints_states/', views.all_sprints_states),
    path('all_sprints_states/<str:state>/', views.all_sprints_state),
    path('zones_of_growth/', views.zones_of_growth),
    path('achieves/states/', views.achieves_states),
    path('achieves/shop/', views.achieves_shop),
    path('buy/<str:achieve_name>/', views.buy),
    url(r'^logout/$', views.logout_view),
]
