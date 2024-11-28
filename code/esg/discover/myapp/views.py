import pandas as pd
from .models import WaterResourceManagement  # 引入您的模型
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages


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


def import_water_resource_data(request):
    # 指定要匯入的 Excel 檔案路徑（開發時可用靜態路徑，部署時建議用文件上傳）
    file_path = '/Users/lijialing/Desktop/DiscoverTheTruth/2021-2023_ESG/water_resource_management.xlsx'

    try:
        # 讀取 Excel 檔案
        df = pd.read_excel(file_path)

        # 遍歷每一列資料，並存入資料庫
        for _, row in df.iterrows():
            WaterResourceManagement.objects.create(
                year=row['年份'],
                company_code=row['公司代號'],
                company_name=row['公司名稱'],
                water_usage=row['用水量(公噸)'],
                data_scope=row.get('資料範圍', None),
                water_density=row.get('用水密集度(公噸/單位)', None),
                density_unit=row.get('用水密集度-單位', None),
                certification=row.get('取得驗證', None),
            )

        return JsonResponse({"status": "success", "message": "資料匯入成功！"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
