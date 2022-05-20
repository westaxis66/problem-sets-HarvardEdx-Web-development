from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from network.models import User, Post, Follower, Like
from django.db.models import Count
from django.core.paginator import Paginator
import json

MAX_POSTS_PER_PAGE = 10
POST_MAX_LENGTH = 240


def index(request):

    if request.user.is_authenticated:
        auth_user = request.session['_auth_user_id']
        likes = Like.objects.filter(post__isnull=True, user_id=auth_user)
        posts = Post.objects.filter().order_by(
            '-post_date').annotate(current_like=Count(likes.values('id')))
    else:
        posts = Post.objects.order_by('-post_date').all()

    paginator = Paginator(posts, MAX_POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        'posts': page,
        
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, username):

    try:
        following = 0
        user_profile = User.objects.get(username=username)
        auth_user = request.session['_auth_user_id']
        following = Follower.objects.filter(follower=auth_user, following=user_profile).count()
        likes = Like.objects.filter(post__isnull=True, user_id=auth_user)
        posts = Post.objects.filter(user=user_profile).order_by(
            '-post_date').annotate(current_like=Count(likes.values('id')))
    except:
        return render(request, 'network/profile.html', {"error": True})
    
    paginator = Paginator(posts, MAX_POSTS_PER_PAGE)
    posts = Post.objects.filter(user=user_profile).order_by('-post_date').all()
    if request.GET.get("page") != None:
        try:
            posts = paginator.page(request.GET.get("page"))
        except:
            page = paginator.page(1)
    else:
        posts = paginator.page(1)
    
    total_following = Follower.objects.filter(follower=user_profile).count()

    total_followers = Follower.objects.filter(following=user_profile).count()

    return render(request, "network/profile.html", {
        "user_profile": user_profile, 
        "posts": posts, 
        "following": following, 
        'total_following': total_following, 
        'total_followers': total_followers, 
    }) 
       




def post(request, post_id=None):
    if request.method == "POST":
        if not post_id:
            auth_user = User.objects.get(id=request.session['_auth_user_id'])
            text = request.POST["textarea"] 
            user_post = Post.objects.create(
                user=auth_user, text=text
            )
            
            user_post.save()

            return HttpResponseRedirect(reverse("index"))

        post = Post.objects.get(id=post_id)

        data = json.loads(request.body)

        if len(data.get("message", "")) <= 0:
            return JsonResponse({"message": "Please fill out this field"}, status=406)

        if len(data.get("message")) > POST_MAX_LENGTH:
            return JsonResponse(
                {"message": "240 characters only"}, status=406
            )

        post.text = data.get("message")
        post.save()

        return JsonResponse({"saved": True}, status=200)

    return render(request, "network/post.html", {"post_max_length": POST_MAX_LENGTH})


def follow(request, id):
    
    try:
        result = 'follow'
        auth_user = User.objects.get(id=request.session['_auth_user_id'])
        user_follower = User.objects.get(id=id)
        get_follow_obj = Follower.objects.get(follower=auth_user, following=user_follower)
    except Follower.DoesNotExist:
        try:
            User.objects.get(id=request.session['_auth_user_id'])
        except User.DoesNotExist:
            return HttpResponse(status=404)
        else:
            new_follow_obj = Follower(follower=auth_user, following=user_follower)
            new_follow_obj.save()
    else:
        result = 'unfollow'
        get_follow_obj.delete()

    total_followers = Follower.objects.filter(following=user_follower).count()
    
    return JsonResponse({"result": result, "total_followers": total_followers})


def following(request):
    
    auth_user = request.session['_auth_user_id']
    following = Follower.objects.filter(follower=auth_user)
    likes = Like.objects.filter(post__isnull=True, user_id=auth_user)
    posts = Post.objects.filter(user_id__in=following.values(
            'following_id')).order_by('-post_date').annotate(current_like=Count(likes.values('id')))

    for post in posts:
        post.save()

    paginator = Paginator(posts, MAX_POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "posts": page
    })


def like(request, id):

    if request.method == "POST":
        auth_user = User.objects.get(id=request.session['_auth_user_id'])
        post = Post.objects.get(id=id)
        
        if auth_user in post.likes.all():
            post.likes.remove(auth_user)
            post.save()
            return JsonResponse({"liked": "False", "id": id}, status=200)

        post.likes.add(auth_user)
        post.save()
        return JsonResponse({"liked": "True", "id": id}, status=200)


def delete(request, post_id=None):
    auth_user = User.objects.get(id=request.session['_auth_user_id'])
    post_to_delete=Post.objects.get(id=post_id, user=auth_user)
    post_to_delete.delete()
    return HttpResponseRedirect(reverse("index"))



