from .models import WaterResourceManagement
from django.http import JsonResponse
from django.db import transaction
from .models import WasteManagement, WaterResourceManagement
import pandas as pd
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


def upload_xlsx_from_path(request):
    file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/2021-2023_ESG/water_resource_management.xlsx"  # 替換成實際檔案路徑

    try:
        # 讀取 XLSX 檔案
        df = pd.read_excel(file_path)

        # 檢查必要欄位是否存在
        required_columns = ["年份", "公司代號", "公司名稱",
                            "用水量(公噸)", "資料範圍", "用水密集度(公噸/單位)", "用水密集度-單位", "取得驗證"]
        if not all(column in df.columns for column in required_columns):
            return JsonResponse({"error": "Excel 檔案格式錯誤，缺少必要欄位。"}, status=400)

        # 清理數據：將非數字值替換為 None
        def clean_value(value):
            if pd.isna(value):  # 如果是 NaN，返回 None
                return None
            if isinstance(value, str) and value.strip() in ["無", "無統計相關數據", "無，無統計相關數據"]:
                return None
            try:
                return float(value)  # 嘗試轉為浮點數
            except (ValueError, TypeError):
                return None  # 無法轉為數字時返回 None

        # 清理數據
        df["用水量(公噸)"] = df["用水量(公噸)"].apply(clean_value)
        df["用水密集度(公噸/單位)"] = df["用水密集度(公噸/單位)"].apply(clean_value)

        # 處理年份欄位，將無效的年份轉為 None
        df["年份"] = pd.to_numeric(df["年份"], errors="coerce")

        # 去除原始資料中的重複項
        df = df.drop_duplicates(subset=["年份", "公司代號"])

        # 將資料寫入資料庫
        for _, row in df.iterrows():
            # 檢查資料是否已存在
            if WaterResourceManagement.objects.filter(year=row["年份"], company_code=row["公司代號"]).exists():
                print(f"資料已存在：{row['年份']} - {row['公司代號']}")
                continue  # 如果資料已存在，跳過此行

            # 創建新記錄
            WaterResourceManagement.objects.create(
                year=int(row["年份"]) if pd.notna(
                    row["年份"]) else None,  # 只在年份有效時才插入
                company_code=row["公司代號"],
                company_name=row["公司名稱"],
                water_usage=row["用水量(公噸)"],
                data_scope=row.get("資料範圍", None),
                water_density=row["用水密集度(公噸/單位)"],
                density_unit=row.get("用水密集度-單位", None),
                certification=row.get("取得驗證", None),
            )

        return JsonResponse({"success": "資料成功導入！"})

    except Exception as e:
        return JsonResponse({"error": f"處理檔案時發生錯誤：{str(e)}"}, status=500)


def import_waste_management_data(request):
    # 指定 Excel 檔案路徑

    file_path = '/Users/lijialing/Desktop/DiscoverTheTruth/2021-2023_ESG/waste_management_old.xlsx'

    try:
        # 讀取 Excel 檔案
        df = pd.read_excel(file_path)

        # 檢查資料結構
        required_columns = ['年份', '公司代號', '公司名稱', '有害廢棄物量(公噸)', '非有害廢棄物量(公噸)',
                            '總重量(有害+非有害)(公噸)', '資料範圍', '廢棄物密集度(公噸/單位)',
                            '廢棄物密集度-單位', '取得驗證']

        missing_columns = [
            col for col in required_columns if col not in df.columns]
        if missing_columns:
            return JsonResponse({"status": "error", "message": f"缺少欄位: {', '.join(missing_columns)}"})

        # 清理年份欄位，保證其為整數型
        df['年份'] = pd.to_numeric(df['年份'], errors='coerce')
        df = df.dropna(subset=['年份'])  # 移除年份為 NaN 的行
        df['年份'] = df['年份'].astype(int)

        # 清理廢棄物密集度欄位，將非數值替換為 NaN
        df['廢棄物密集度(公噸/單位)'] = pd.to_numeric(df['廢棄物密集度(公噸/單位)'],
                                            errors='coerce')

        # 使用事務來保證資料的一致性
        with transaction.atomic():
            # 遍歷每一列資料，將清理後的資料存入資料庫
            for _, row in df.iterrows():
                # 先檢查資料是否已經存在
                instance, created = WasteManagement.objects.update_or_create(
                    year=row['年份'],
                    company_code=row['公司代號'],
                    defaults={
                        'company_name': row['公司名稱'],
                        'hazardous_waste': row.get('有害廢棄物量(公噸)', None),
                        'non_hazardous_waste': row.get('非有害廢棄物量(公噸)', None),
                        'total_weight': row.get('總重量(有害+非有害)(公噸)', None),
                        'data_scope': row.get('資料範圍', None),
                        'waste_density': row['廢棄物密集度(公噸/單位)'],  # 清理後確保為數字或 NaN
                        'waste_density_unit': row.get('廢棄物密集度-單位', None),
                        'certification': row.get('取得驗證', None),
                    }
                )

            return JsonResponse({"status": "success", "message": "資料匯入並更新成功！"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
