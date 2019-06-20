from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,"application/index.html")

def register(request):
    print(request)
    errors = User.objects.basicValidatorReg(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, key)
        return redirect("/")
    else:
        fn = request.POST['firstName']
        ln = request.POST['lastName']
        email = request.POST['email']
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        newUser = User.objects.create(firstName=fn, lastName=ln, email=email, password=password)
        request.session['userid'] = newUser.id
    return redirect("/wall")

def login(request):
    print(request.POST['password'])
    errors = User.objects.basicValidatorLogin(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, key)
        return redirect("/")
    else:
        user = User.objects.filter(email=request.POST['email'])
        request.session['userid'] = user[0].id
        return redirect(reverse('wall:myWall'))

def success(request):
    if 'userid' in request.session:
        user = User.objects.get(id=request.session['userid'])
        context = {
            "user": user
        }
        return render(request, "application/success.html", context)
    else:
        return redirect("/")

def logout(request):
    del request.session['userid']
    return redirect("/")
