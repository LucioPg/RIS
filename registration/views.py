from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm



# Create your views here.

def register(request):
    print(request.POST)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid() and 'reset' not in request.POST:
            form.save()
            return redirect("/")
        else:
            form = UserCreationForm()
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration.html', {'form':form})