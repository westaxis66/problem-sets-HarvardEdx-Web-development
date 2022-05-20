from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from newsapp.models import User
import requests
import json
import urllib.request
from capstone import settings
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import login
from .forms import subscriptionForm
from .forms import loginForm

 # Create your views here.

def index(request):
    catagory= request.GET.get('search', None)
    
    if catagory =="top": 
       url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
            "us",2,settings.APIKEY
        )
    elif catagory is None:
        url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
            "us",1,settings.APIKEY
        )
    else:
        url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
            catagory,"popularity",2,settings.APIKEY
        )

    get_url = requests.get(url=url)

    info = get_url.json()
    
    article_info = info["articles"]
    content = {
        "success": True,
        "data": [],
        "search": catagory
    }
    
    for i in  article_info:
        content["data"].append({
            "title": i["title"],
            "description":  "" if i["description"] is None else i["description"],
            "url": i["url"],
            "image": "" if i["urlToImage"] is None else i["urlToImage"],
            "publishedat": i["publishedAt"],
      
        })
    
    return render(request, 'newsapp/index.html', context=content)

def login_view(request):
    if request.method == "POST":
        form = loginForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user != None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "newsapp/login.html", {
                    "message": "Invalid username and/or password."
             })
    else:
        return render(request, "newsapp/login.html", {
            "login_form": loginForm()
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def subscribe(request):
    if request.method == "POST":

        form = subscriptionForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            email = request.POST["email"]

        
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
            if password != confirmation:
                return render(request, "newsapp/subscribe.html", {
                    "message": "Passwords must match."
                })

            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                subject = 'welcome to Tengu News'
                message = f'Hi {user}, thank you for registering at Tengu News. Your user name is {user.username}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email,]
                send_mail( subject, message, email_from, recipient_list )
                return render(request, 'newsapp/success.html', {'recepient': recipient_list})
            except IntegrityError:
                return render(request, "newsapp/subscribe.html", {
                    "message": "Username already taken."
                })
        
    else:
        return render(request, "newsapp/subscribe.html",{
            "subscription_form": subscriptionForm()
        })

    

def weather(request):
    if request.method == 'POST':
        city = request.POST['city']
        api = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&units=imperial&appid=1921d8757d51f96a61ce5a8b59cbd148').read()
        
        jsonloads =json.loads(api)
        
        weather_data ={
            'country_code':str(jsonloads['sys']['country']),
            'cor':str(jsonloads["coord"]["lon"]),
            'corlat':str(jsonloads["coord"]["lat"]),
            'temp':str(jsonloads["main"]['temp']),
            'pressure':str(jsonloads['main']["pressure"]),
            'humidity':str(jsonloads['main']['humidity']),
            'main':str(jsonloads["weather"][0]['main']),
            'description':str(jsonloads["weather"][0]['description']),
            'icon':jsonloads["weather"][0]['icon'],
            'temp_min':str(jsonloads["main"]['temp_min']),
            'temp_max':str(jsonloads["main"]['temp_max']),
            'city':city
        }
    else:
        weather_data ={}
    return render(request,'newsapp/weather.html',weather_data)

def contact(request):
    return render(request, "newsapp/contact.html")