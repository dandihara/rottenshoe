
from django.db.models.query_utils import Q
from django.http import response
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect, request
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.views.generic import RedirectView
from django.db.utils import IntegrityError


from rottenshoe.forms import BoardForm,UserForm
from rottenshoe.token import create_token,decoder

import json
import re

from .models import Comment, Sneakers, User, Keyword

#req => JsonResponse 객체   
def index(req):
    shoeList = Sneakers.objects.all()
    return render(req,'index.html', context = {'lists' : shoeList})


def detail(req,id):
    if req.method == 'GET':
        board = Sneakers.objects.get(id = id)
        comments = Comment.objects.filter(board_id = id)
        if board is None :
            return redirect('rotten:index')

        return render(req,'detail.html',{'data' : board, 'comments' : comments})

def login(req):
    if req.method == "POST":
        data = json.loads(req.body.decode('utf-8'))
        client = authenticate(email = data['email'], password = data['password'])
        if client is not None:
            auth_login(req,client)
            #access_token 발생 => 유저 확인용
            access_token =  create_token(client.nickname,client.email,client.id)
            req.session['access_token'] = access_token
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
            try:
                newUser = User(
                    email = data['email'],
                    password = hashed_password,
                    nickname = data['nickname']
                )
                newUser.save()
                auth_login(req,newUser)
            except IntegrityError:
                return JsonResponse({'result':'이미 가입 된 이메일입니다.'})
            return JsonResponse({'result':'ok'})
        if data['password'] != data['confirm_password']:
            return JsonResponse({'result' : 'password'})
        if not re.search(regEmail,data['email']):
            return JsonResponse({'result':'email'})

def comment(req):
    if req.method == 'POST':
        try:
            token = req.session['access_token']
            data = json.loads(req.body.decode('utf-8'))
            # get => == first / limit 1
            # filter => result to list / where ~
            board = Sneakers.objects.get(id = int(data['board_id']))
            user = get_object_or_404(User,pk=decoder(token)['id']) # 있거나 없음 error
        
            co = Comment(
                board_id = board,
                user_id = user,
                comment = data['comment']
            )
            co.save()
            return JsonResponse({'result' : 'ok'})
        except KeyError:
            return JsonResponse({'result' : 'token값 없음'})


def myPage(req):
    pass


def search(req,q):
    result = []
    word_list = q.split(" ")
    keyword_list = [t.keyword for t in Keyword.objects.all()]
    
    for word in word_list:
        # keyword에 들어오는 단어 값인 경우, 대부분 단일형의 단어로 들어오기에 바로 반환되도록 처리.
        if word in keyword_list:
            model_number_list = list(Keyword.objects.filter(keyword = word))
            result = [Sneakers.objects.get(model_number = s.sneaker_id)
                        for s in model_number_list]
            return render(req,'search.html',{'lists': result, 'keyword' : word})
        
        result += list(Sneakers.objects.filter(Q(sneaker_name__icontains = word) | 
                                                    Q(brand__icontains = word) |
                                                    Q(sneaker_name_ko__icontains = word)).distinct())
    context = {'lists':result, 'keyword':q}
    
    return render(req,'search.html',context)

