from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('filter/', views.filter_news,name='filter_news'),
    path('saved/',views.saved_news,name='saved_news'),
    path('login/',views.LoginView.as_view(), name="login"),
    path('logout/',views.logout,name="logout"),
    path('signup/', views.signup_view, name="signup"),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('preferences/', views.preferences,name='preferences'),
]