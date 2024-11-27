from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


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
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def report(request):
    return render(request, 'report.html')
