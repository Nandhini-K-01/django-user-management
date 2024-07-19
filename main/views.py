from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from .forms import RegisterForm, PostForm
from .models import Post
from django.contrib.auth.models import User, Group

# Create your views here.

@login_required(login_url="login")
def home(request):
    posts = Post.objects.all()
    if request.method == "POST":
        post_id = request.POST.get("post-id")
        user_id = request.POST.get("user-id")
        if post_id:
            post = Post.objects.get(id=post_id).first()
            if post and (request.user == post.author or request.user.has_perm("main.delete_post")): # main.delete_post --> app_name.action_modelname
                # print(post)
                post.delete()
            elif user_id:
                user = User.objects.get(id=user_id)
                if user and request.user.is_staff():
                    try:
                        group = Group.objects.get(name="default")
                        group.user_set.remove(user)
                    except:
                        pass

                    try:
                        group = Group.objects.get(name="mod")
                        group.user_set.remove(user)
                    except:
                        pass

    return render(request, 'main/home.html', {"posts":posts})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST) # passing the post method data to the form to validate
        if form.is_valid():
            user = form.save()
            login(request, user) # logins the user
            return redirect("/home")
    else:
        form = RegisterForm() # here, creating an empty form while get method

    return render(request, 'registration/sign_up.html', {"form": form})


@login_required(login_url="login")
@permission_required("main.add_post", login_url="login", raise_exception=True) # main.add_post --> app_name.action_modelname
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) # by default commit is true, why false now? becos v have to add user data, 
                                           # if its true it will CREATE ENTRY IN THE DATABASE
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    
    return render(request, 'main/create_post.html', {"form":form})



# from django.contrib.auth.models import User, Group, Permission
# from django.contrib.contenttypes.models import ContentType

# mod, created = Group.objects.get_or_create(name="mod")
# mod.persmissions.add(*perms) # see below for perms
# mod.user_set.add(user) # get user from User model using id

# ct = ContentType.objects.get_for_model(model=Post)
# perms = Permission.objects.filter(content_type=ct)
