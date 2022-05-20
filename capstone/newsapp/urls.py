from django.urls import path
from . import views




urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("subscribe", views.subscribe, name="subscribe"),
    path("", views.index, name="index"),
    path("weather",views.weather, name="weather"),
    path("contact", views.contact, name="contact"),
     
    
 ]