from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def chart(request):
    return render(request, 'chart.html')


def ESGEachCompany(request):
    return render(request, 'ESGEachCompany')


def ESGReal(request):
    return render(request, 'ESGReal.html')


def ESGRisk(request):
    return render(request, 'ESGRisk.html')


def forget(request):
    return render(request, 'forget.html')


def login(request):
    if request.method == "POST":
        # 從表單獲取輸入
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 驗證使用者帳密
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')  # 登入成功，導向首頁或其他頁面
        else:
            messages.error(request, "電子信箱或密碼不正確，請重新輸入。")

    return render(request, 'login.html', {'message': messages.get_messages(request)})


def register(request):
    return render(request, 'register.html')


def report(request):
    return render(request, 'report.html')
