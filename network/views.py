from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from .models import User,Post,Follow,Like
from django.core.paginator import Paginator
import json

def index(request):
    posts = Post.objects.all().order_by("id").reverse()
    likes =  Like.objects.all()
    check = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                check.append(like.post_liked.id)

    except:
        check = []
    postsv2 = Paginator(posts, 10)
    page_posts = postsv2.get_page(request.GET.get('page'))
    return render(request, "network/index.html",{
        'posts':postsv2,
        'page_posts': page_posts,
        'likes':likes,
        'check': check
    })

def edit(request, post_id):
    if request.method == 'POST':
       data = json.loads(request.body)
       editpost = Post.objects.get(pk=post_id)
       editpost.content = data["content"]
       editpost.save()
       return JsonResponse({"message": "Change successful", "data": data["content"]})



def follow_sec(request):
    user = User.objects.get(pk=request.user.id)
    following = Follow.objects.filter(user=user)
    
    posts = Post.objects.all().order_by("id").reverse()
    all_posts = []
    for post in posts:
        for follow in following:
            if follow.user_follower == post.user:
                all_posts.append(post)

    postsv2 = Paginator(all_posts, 10)
    page_posts = postsv2.get_page(request.GET.get('page'))
    return render(request, "network/index.html",{
        'posts':postsv2,
        'page_posts': page_posts
    })
    
def create(request):
    if request.method == 'POST':
       content = request.POST['content']
       user = User.objects.get(pk=request.user.id)
       newpost= Post(user=user, content=content)
       newpost.save()
       return HttpResponseRedirect(reverse("index"))
    

def profile(request, id):

    user = User.objects.get(pk=id)
    following = Follow.objects.filter(user=user)
    follower = Follow.objects.filter(user_follower=user)
    likes =  Like.objects.all()
    check = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                check.append(like.post_liked.id)

    except:
        check = []
    #Check if our user is following this user

    try:
        check_follow = follower.filter(user=User.objects.get(pk=request.user.id))
        if len(check_follow) != 0:
            check_follow = True
        else:
            check_follow = False
    except:
        check_follow = False

    posts = Post.objects.filter(user=user).order_by("id").reverse()
    postsv2 = Paginator(posts, 10)
    page_posts = postsv2.get_page(request.GET.get('page'))
    return render(request, "network/profile.html",{
        'posts':postsv2,
        'page_posts': page_posts,
        'user':user,
        'follower':follower,
        'following':following,
        'check': check_follow,
        'checks':check
        
    })
def follow(request, userid,followerid):

    user = User.objects.get(pk=userid)
    follower = User.objects.get(pk=followerid)
    follow_action= Follow(user=follower,user_follower=user)
    follow_action.save()
    return HttpResponseRedirect(reverse("profile", kwargs={"id":userid}))

def unfollow(request, userid,unfollowerid):
    user = User.objects.get(pk=userid)
    unfollower = User.objects.get(pk=unfollowerid)
    follow_action= Follow.objects.get(user=unfollower,user_follower=user)
    follow_action.delete()
    return HttpResponseRedirect(reverse("profile", kwargs={"id":userid}))
 


def like(request, postid):

    user = User.objects.get(pk=request.user.id)
    post = Post.objects.get(pk=postid)
    like_action= Like(user=user,post_liked=post)
    like_action.save()
    
    return JsonResponse({"message": "liked successful"})





def unlike(request,postid):

    user = User.objects.get(pk=request.user.id)
    post = Post.objects.get(pk=postid)
    like_action= Like.objects.get(user=user,post_liked=post)
    like_action.delete()
    return JsonResponse({"message": " unliked successful",})






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
