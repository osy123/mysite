from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from user.models import *
from user import models

# Create your views here.

def joinform(request):
    return render(request, 'user/joinform.html')

def join(request):
    name = request.POST["name"]
    email = request.POST["email"]
    password = request.POST["password"]
    gender = request.POST["gender"]

    models.insert((name, email, password, gender))

    return HttpResponseRedirect('/user/joinsuccess')

def joinsuccess(request):
    return render(request, 'user/joinsuccess.html')


def loginform(request):
    return render(request, 'user/loginform.html')

def login(request):
    email = request.POST["email"]
    password = request.POST["password"]

    user = models.get(email, password)

    # 로그인 실패!!!!! ***** 짱중요
    if user is None:
        return HttpResponseRedirect('/user/loginform?result=fail')

    # 로그인 성공(처리)
    request.session['authuser'] = user      # 현재 코드만 써주게 되면 쿠키를 메모리에 저장 -> 그래서 브라우저를 껐다 켜면 로그아웃됨
                                            #  -> settings 제일 밑에 SESSION_EXPIRE_AT_BROWSER_CLOSE = True 추가 해주면 ->
                                            # 메모리가 아니라 db에 데이터를 저장 -> 껐다 켜도 계속 로그인 상태 유지

    # 장고가 브라우저에 쿠키 생성 요청-> 쿠키 생성(쿠키 저장할때는 위에 주석 참고) -> 쿠키를 서버로 보내줌 ->
    # 서버에서 장고 세션에 데이터 저장 -> 리퀘스트에 데이터 담아서 서버에 요청 -> 서버가 장고로 데이터를 다시 보내줌
    # 쿠키 생성은 브라우저에 최초로 들어갈때 생성됬다가 일정 기간이 지나면 삭제해버림.

    # main으로 redirect
    return HttpResponseRedirect('/')


def logout(request):
    del request.session['authuser']

    return HttpResponseRedirect('/')


def checkemail(request):

    email = request.POST["email"]
    address = models.check(email)

    if address is None:
        return HttpResponseRedirect('/user/joinform?check=pass')

    request.session['passemail'] = address

    return HttpResponseRedirect('/user/joinform')
