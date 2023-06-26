import os
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.conf import settings
from django.db.models import Q

def logout_user(request):
    if request.user != None:
        logout(request)
    return redirect(reverse('login_page'))

def login_page( request):
    if request.user.is_authenticated :
        return redirect(reverse ('home'))
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse ('home'))
        if 'next' in request.GET:
            #return redirect(self.request.GET.get('next'))
            return redirect(request.GET.get('next'))
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
        
    return render(request, 'registration/login.html')

@login_required
def home(request):
    query = request.GET.get('q') #get the query from the search form
    # Get all the stories from the database
    stories = Story.objects.all().order_by('-date_posted')
    # Iterate over each story to fetch its comments
    if query:
        # Filter stories that contain the search query in their tag, or story
        stories = stories.filter(
            Q(tag__icontains=query) |
            Q(story__icontains=query) 
        )
    for story in stories:
        # Retrieve the comments for the current story
        comments = story.comment_set.all()
        c = comments.count()
        # Add the comments to the story object as an attribute
        story.comments = comments
        story.comments.count = c
    
    # Pass the stories to the template for rendering
    context = {
        'stories': stories,
    }
    
    return render(request, 'home.html', context)

@login_required
def mystory(request):
    query = request.GET.get('qq') #get the query from the search form
    # Get the stories from the database
    stories = Story.objects.filter(author=request.user).order_by('-date_posted')
    # Iterate over each story to fetch its comments
    if query:
        # Filter stories that contain the search query in their tag, or story
        stories = stories.filter(
            Q(tag__icontains=query) |
            Q(story__icontains=query) 
        )
    for story in stories:
        # Retrieve the comments for the current story
        comments = story.comment_set.all()
        c = comments.count()
        # Add the comments to the story object as an attribute
        story.comments = comments
        story.comments.count = c

    # Pass the stories to the template for rendering
    context = {
        'stories': stories,
    }
    
    return render(request, 'mystory.html', context)


def signup(request):
    form = CustomUserForm(request.POST or None, request.FILES or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            picture = form.cleaned_data.get('picture_pic')
            fname = form.cleaned_data.get('first_name')
            lname = form.cleaned_data.get('last_name')
            gender = form.cleaned_data.get('gender')
            address = form.cleaned_data.get('address')
            user = CustomUser.object.create_user(email=email,password=password, profile_pic=picture,
                                                 first_name=fname, last_name=lname,gender=gender,address=address)
            if picture:
                user.profile_pic = picture
                picture_path = os.path.join(settings.MEDIA_ROOT, picture.name)
                with open(picture_path, 'wb') as file:
                    for chunk in picture.chunks():
                        file.write(chunk)
            user.save()
            return redirect(reverse('login_page'))
    return render(request, 'registration/signup.html', context)

@login_required
def addstory(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user  # Assigning the current user as the author
            story.save()
            return redirect(reverse('home'))
    else:
        form = StoryForm(initial={'author': request.user})  # Setting the initial value for the author field
    
    context = {
        'form': form,
    }
    
    return render(request, 'addstory.html', context)

@login_required
def addcomment(request, id):
    post = Story.objects.get(id=id)  # Use get() instead of filter() to retrieve a single object
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  # Assign the current user as the author
            comment.story = post  # Assign the story object to the comment
            comment.save()
            return redirect(reverse('home'))
        else:
            print(form.errors)
    else:
        form = CommentForm(initial={'author': request.user, 'story': post})
    
    context = {
        'form': form,
    }
    
    return render(request, 'addcomment.html', context)

@login_required
def deletecomment(request, id):
    comment = get_object_or_404(Comment, id=id)
    try:
        comment.delete()
    except IntegrityError as e:
        print("Error, Integrity", e)
    return redirect(reverse('home'))

@login_required
def deletestory(request, id):
    story = get_object_or_404(Story, id=id)
    try:
        story.delete()
    except IntegrityError as e:
        print("Error, Integrity", e)
    return redirect(reverse('home'))

@login_required
def editstory(request, id):
    story = get_object_or_404(Story, id=id, author=request.user)
    form = StoryForm(request.POST or None, instance=story)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
    
    return render(request, 'editstory.html', context)


@login_required
def editcomment(request, id):
    comment = get_object_or_404(Comment, id=id, author=request.user) #get the actual comment for the editing
    form = CommentForm(request.POST or None, instance=comment)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
    
    return render(request, 'editcomment.html', context)

@login_required
def editaccount(request, id):
    usr = get_object_or_404(CustomUser, id=id) #get the actual user's account for editing
    form = CustomUserForm(request.POST or None, instance=usr, initial={'password': " "})
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
    
    return render(request, 'editaccount.html', context)
