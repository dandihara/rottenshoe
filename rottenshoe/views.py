from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect, request
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from rottenshoe.forms import BoardForm,UserForm
from rottenshoe.token import create_token

import json
import re



# Create your views here.
from .models import Comment, SneakerBoard, User

#req => JsonResponse 객체   
def index(req):
    shoeList = SneakerBoard.objects.all()

    return render(req,'index.html', context = {'lists' : shoeList})


def boardPost(req):
    if req.method == 'GET':
        form = BoardForm()
        return render(req,'board.html',{'form':form})

    elif req.method == 'POST':
        form = BoardForm(req.POST)
        if form.is_valid():
            board = form.save(commit = False)
            board.save()
            return redirect('rotten:index')
        else:
            form = BoardForm()
        context = {'form': form}
        return render(req, 'board.html', context)


def detail(req,id):
    if req.method == 'GET':
        board = SneakerBoard.objects.get(id = id)
        comments = Comment.objects.filter(board_id = id)
        if board is None :
            return redirect('rotten:index')
        return render(req,'detail.html',{'data' : board})


def login(req):
    if req.method == "POST":
        data = json.loads(req.body.decode('utf-8'))
        client = authenticate(email = data['email'], password = data['password'])
        if client is not None:
            auth_login(req,client)
            #access_token 발생 => 유저 확인용
            access_token =  create_token(client.nickname,client.email,client.id).decode('utf-8')
            req.session['access_token'] = access_token
            print(req.session['access_token'])
            return JsonResponse({'result':'ok', 'access_token' : access_token})
        else:
            return JsonResponse({'result':'not exist'})
    elif req.method == 'GET':
        return render(req, 'login.html')

def logout(req):
    auth_logout(req)
    return redirect('rotten:index')

def register(req):
    if req.method == 'GET':
        return render(req,'signup.html')
    else:
        regEmail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        data = json.loads(req.body.decode('utf-8'))

        if data['password'] == data['confirm_password'] and re.search(regEmail,data['email']):
            hashed_password = make_password(data['password'])
            newUser = User(
                email = data['email'],
                password = hashed_password,
                nickname = data['nickname']
            )
            newUser.save()
            auth_login(req,newUser)
            return JsonResponse({'result':'ok'})
        if data['password'] != data['confirm_password']:
            return JsonResponse({'result' : 'password'})
        if not re.search(regEmail,data['email']):
            return JsonResponse({'result':'email'})
