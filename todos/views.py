from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from .models import todo

from django.utils import timezone
from django.contrib import messages

from django.core.mail import send_mail
import jwt
import base64
import time

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        tod = todo.objects.filter(username=request.user.username)
        return render(request, './home.html', {'tod': tod})
    else:
        context = {
            'msg': "Please Login to Continue"
        }
        return render(request, './error.html', context)


def addform(request):

    now = timezone.now()
    tod = todo.objects.filter(username=request.user.username)
    return render(request, './add.html', {'date': now, 'tod': tod})


def add(request):
    tod = todo(title=request.POST['title'],
               description=request.POST['description'], username=request.user.username)

    tod.save()
    return HttpResponseRedirect(reverse('home'))


def delete(request, pk_id):
    tod = todo.objects.get(pk=pk_id).delete()
    return HttpResponseRedirect(reverse('home'))


def loginform(request):
    return render(request, './login.html')


def login(request):

    u = request.POST
    user = authenticate(request, username=u['name'], password=u['password'])
    if user is not None:
        auth_login(request, user)
        messages.info(request, 'Login Successfull')
        return HttpResponseRedirect(reverse('home'))

    else:
        messages.info(request, 'Error User is not registered/invalid')
        return HttpResponseRedirect(reverse('loginform'))


def registerform(request):
    return render(request, './register.html')


def sendmail(request):

    tod = User.objects.filter(username=request.POST['name'])
    if len(tod):
        messages.info(
            request, 'Username already exists')
        return HttpResponseRedirect(reverse('registerform'))

    tod = User.objects.filter(email=request.POST['email'])
    if len(tod):
        messages.info(
            request, 'Email already exists')
        return HttpResponseRedirect(reverse('registerform'))

    now = int(time.time())
    encoded_token = jwt.encode({'name': request.POST['name'], 'email': request.POST['email'],
                                'password': request.POST['password'], 'exp': now + 3600 * 24}, '1734662377', algorithm='HS256')
    print(encoded_token)
    check=send_mail(
        'Click to register',
        "http://127.0.0.1:8000/todos/verify/" +
        encoded_token.decode('utf-8')+'/',
        '************@gmail.com',
        [request.POST['email']],
        fail_silently=False
    )
    if check:
        messages.info(request, 'Verification Link sent to '+request.POST['email'])
        return HttpResponseRedirect(reverse('loginform'))
    else:
        messages.info(
        request, 'Error ! Mail not sent')
        return HttpResponseRedirect(reverse('registerform'))


def register(request, token):

    token = bytes(token, 'utf-8')
    user = jwt.decode(token, '1734662377', algorithms=['HS256'])

    print(user)
    u = User.objects.create_user(
        user['name'], user['email'], user['password'])
    u.save()

    messages.info(request, "Registeration Successfull")
    return HttpResponseRedirect(reverse('loginform'))


def logout(request):
    auth_logout(request)

    messages.info(request, 'Thank You')
    return HttpResponseRedirect(reverse('home'))
