from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import FileUploadForm
from .models import UploadedFile

from django.conf import settings

from joblib import load
import os
from PIL import Image
import pandas as pd

emotions_list = ['essai','surprise', 'sad', 'neutral', 'happy','fear','disgust','angry']

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with the URL name of your homepage
        else:
            error_message = 'Invalid username or password'
            return render(request, 'myapp/login.html', {'error_message': error_message})
    else:
        return render(request, 'myapp/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
    
def home_view(request):
    user = request.user
    latest_files = UploadedFile.objects.select_related('user').order_by('-uploaded_time')[:10]
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(username__icontains=query).exclude(is_staff=True)
    else:
        query = ""
        users = User.objects.all().exclude(is_staff=True)
    return render(request, 'myapp/home.html', {'users': users, 'query': query, 'emotions':emotions_list, 'latest_files':latest_files})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Replace 'login' with the URL name of your login page
    else:
        form = UserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})

def user_profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    retour = {}
    for em in emotions_list:
        pict = UploadedFile.objects.filter(user_id=user_id,emotion=em)
        for phot in pict: 
            phot.file = settings.MEDIA_URL + str(phot.file)
        retour[em] = pict
    return render(request, 'myapp/user_profile.html', {'user_profile': user, 'albums':retour})

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file = form.save(commit=False) 
            upload_file.user = request.user

            #on peut maintenant charger le modèle en utilisant le fichier joblib 
            reg_loaded = load('model_saved.joblib')

            pixel_number = 2305
            im = Image.open(upload_file.file).convert("L")
            im = im.resize((48, 48))
            pixels = list(im.getdata())

            numbers = ["pixel"+str(x) for x in range(1,2305)]
            for_test = pd.DataFrame([pixels], columns=numbers)
            prediction = reg_loaded.predict(for_test)

            upload_file.emotion = prediction[0]
            upload_file.save()
            return redirect('home')  # Replace 'upload_success' with the URL name for success page or redirect to desired page
    else:
        form = FileUploadForm()

    return render(request, 'myapp/upload.html', {'form': form})
    

def my_album_view(request, emotion):
    if emotion:
        photos = UploadedFile.objects.filter(user_id=request.user.id,emotion=emotion)
        for phot in photos: 
            phot.file = settings.MEDIA_URL + str(phot.file)
    return render(request, 'myapp/albums.html', {'photos_list': photos,'emotion':emotion})

    
    