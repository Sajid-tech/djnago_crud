from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm , UserRegistrationForm
from django.shortcuts import get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login



# Create your views here.

def index(request):
    return render(request,  'index.html')

# to list all tweet 

def tweet_list(request):
    tweets =Tweet.objects.all().order_by('-create_at')
    #------------(request, 'kaha pe serve krna hai', {all data})
    return render(request, 'tweet_list.html' ,{'tweets':tweets})

# To create Tweet
@login_required
def tweet_create(request):
    if request.method == "POST":  # when form is filled send(req) from user
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False) # here commit means i don't want to save it in database just keep it upto you
            tweet.user = request.user
            tweet.save() # now tweet save in db
            return redirect('tweet_list') # redirect is in string
    else:  # when form is empty
        form = TweetForm()
    return render(request,'tweet_form.html',{'form':form})

# edit the tweet 
@login_required
def tweet_edit(request,tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)  # to get data ( here object get kro( Tweet(model se), pk= tweet_id(konse id mein ), user = request.user(only own user can get their data)))
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet) # here i am giving instansce tweet becuz edit mein kuch prefilled data toh rhega for that case yah tweet de rha hu 
    return render(request,'tweet_form.html',{'form':form})

# to delete the tweet
@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk= tweet_id, user= request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html',{'tweet':tweet})



# for registration user

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1']) # [password1] is field
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request,'registration/register.html',{'form':form})


