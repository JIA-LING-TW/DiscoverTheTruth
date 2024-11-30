from .models import GreenhouseGasEmission
from .models import EnergyManagement
from .models import WasteManagement
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import WaterResourceManagement, EnergyManagement, GreenhouseGasEmission, WasteManagement
from django.db.models import Q
from django.shortcuts import render
from django.forms.models import model_to_dict
from myapp.models import GreenhouseGasEmission  # 替換為實際的 app 名稱
from myapp.models import EnergyManagement  # 替換為實際的 app 名稱
from myapp.models import WasteManagement
from .models import WaterResourceManagement
from django.db import transaction
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
    # 接收篩選條件
    market_type = request.GET.get('market_type', '')
    year = request.GET.get('year', '')
    company_name = request.GET.get('company_name', '')
    company_code = request.GET.get('company_code', '')
    category = request.GET.get('category', '')

    # 根據類別篩選模型
    models = {
        'water': WaterResourceManagement,
        'waste': WasteManagement,
        'energy': EnergyManagement,
        'emission': GreenhouseGasEmission
    }
    selected_model = models.get(category, None)

    data = None
    fields = []
    if selected_model:
        # 篩選數據
        filters = {}
        if market_type:
            filters['market_type'] = market_type
        if year:
            filters['year'] = year
        if company_name:
            filters['company_name__icontains'] = company_name
        if company_code:
            filters['company_code'] = company_code

        data = selected_model.objects.filter(**filters)
        # 提取字段名稱和顯示名稱
        fields = [(field.name, field.verbose_name)
                  for field in selected_model._meta.fields]

    return render(request, 'ESGEachCompany.html', {
        'data': data,
        'fields': fields,
        'category': category,
        'market_type': market_type,
        'year': year,
        'company_name': company_name,
        'company_code': company_code
    })


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


def upload_water_resource_management_data(request):
    file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/2021-2023_ESG/water_resource_management.xlsx"  # 請替換為實際檔案路徑

    try:
        # 讀取 Excel 檔案
        df = pd.read_excel(file_path)

        # 檢查必要欄位是否存在
        required_columns = [
            "市場別", "年份", "公司代號", "公司名稱",
            "用水量(公噸)", "資料範圍", "用水密集度(公噸/單位)",
            "用水密集度-單位", "取得驗證"
        ]
        if not all(column in df.columns for column in required_columns):
            return JsonResponse({"error": "Excel 檔案格式錯誤，缺少必要欄位。"}, status=400)

        # 清理數據：處理 NaN 和非數字值
        def clean_value(value):
            if pd.isna(value):  # 如果是 NaN，返回 None
                return None
            if isinstance(value, str) and value.strip() in ["無", "無統計相關數據", "無，無統計相關數據"]:
                return None  # 對無效數據返回 None
            try:
                return float(value)  # 嘗試轉換為浮點數
            except ValueError:
                return None  # 如果無法轉換為數字，返回 None

        # 清理年份欄位：將無效的年份轉為 None 並移除無效年份行
        df["年份"] = pd.to_numeric(df["年份"], errors="coerce")
        df = df.dropna(subset=["年份"])  # 移除年份為 NaN 的行
        df["年份"] = df["年份"].astype(int)  # 確保年份是整數

        # 清理公司代號：轉為字串並去掉小數點
        df["公司代號"] = df["公司代號"].apply(
            lambda x: str(int(x)) if pd.notna(x) else None)

        # 清理其他數據欄位
        for column in ["用水量(公噸)", "用水密集度(公噸/單位)"]:
            if column in df.columns:
                df[column] = df[column].apply(clean_value)

        # 去除重複資料：依年份和公司代號去重
        df = df.drop_duplicates(subset=["年份", "公司代號"])

        # 插入資料到資料庫
        for _, row in df.iterrows():
            # 檢查資料是否已存在
            if WaterResourceManagement.objects.filter(year=row["年份"], company_code=row["公司代號"]).exists():
                continue  # 如果資料已存在，跳過此行

            # 創建新記錄
            WaterResourceManagement.objects.create(
                market_type=row["市場別"],
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"],
                water_usage=row.get("用水量(公噸)", None),
                data_scope=row.get("資料範圍", None),
                water_intensity=row.get("用水密集度(公噸/單位)", None),
                water_intensity_unit=row.get("用水密集度-單位", None),
                certification=row.get("取得驗證", None),
            )

        return JsonResponse({"success": "資料成功導入！"})

    except Exception as e:
        return JsonResponse({"error": f"處理檔案時發生錯誤：{str(e)}"}, status=500)


def upload_waste_management_data(request):
    file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/2021-2023_ESG/waste_management.xlsx"  # 替換為實際檔案路徑

    try:
        # 讀取 Excel 檔案
        df = pd.read_excel(file_path)

        # 檢查必要欄位是否存在
        required_columns = [
            "市場別", "年份", "公司代號", "公司名稱",
            "有害廢棄物量(公噸)", "非有害廢棄物量(公噸)",
            "總重量(有害+非有害)(公噸)", "資料範圍",
            "廢棄物密集度(公噸/單位)", "廢棄物密集度-單位", "取得驗證"
        ]
        if not all(column in df.columns for column in required_columns):
            return JsonResponse({"error": "Excel 檔案格式錯誤，缺少必要欄位。"}, status=400)

        # 清理數據：處理 NaN 和非數字值
        def clean_value(value):
            if pd.isna(value):  # 如果是 NaN，返回 None
                return None
            if isinstance(value, str) and value.strip() in ["無", "無統計相關數據", "無，無統計相關數據"]:
                return None
            # 嘗試轉為數字
            return float(value) if isinstance(value, (int, float)) else value

        # 清理年份欄位，將無效的年份轉為 None 並移除無效年份行
        df["年份"] = pd.to_numeric(df["年份"], errors="coerce")
        df = df.dropna(subset=["年份"])  # 移除年份為 NaN 的行
        df["年份"] = df["年份"].astype(int)  # 確保年份是整數

        # 清理公司代號，轉為字串並去掉小數點
        df["公司代號"] = df["公司代號"].apply(
            lambda x: str(int(x)) if pd.notna(x) else None)

        # 清理其他數據欄位
        for column in ["有害廢棄物量(公噸)", "非有害廢棄物量(公噸)", "總重量(有害+非有害)(公噸)", "廢棄物密集度(公噸/單位)"]:
            if column in df.columns:
                df[column] = df[column].apply(clean_value)

        # 去除原始資料中的重複項
        df = df.drop_duplicates(subset=["年份", "公司代號"])

        # 將資料寫入資料庫
        for _, row in df.iterrows():
            # 檢查資料是否已存在
            if WasteManagement.objects.filter(year=row["年份"], company_code=row["公司代號"]).exists():
                print(f"資料已存在：{row['年份']} - {row['公司代號']}")
                continue  # 如果資料已存在，跳過此行

            # 創建新記錄
            WasteManagement.objects.create(
                market_type=row["市場別"],
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"],
                hazardous_waste=row.get("有害廢棄物量(公噸)", None),
                non_hazardous_waste=row.get("非有害廢棄物量(公噸)", None),
                total_weight=row.get("總重量(有害+非有害)(公噸)", None),
                data_scope=row.get("資料範圍", None),
                waste_intensity=row.get("廢棄物密集度(公噸/單位)", None),
                waste_intensity_unit=row.get("廢棄物密集度-單位", None),
                certification=row.get("取得驗證", None),
            )

        return JsonResponse({"success": "資料成功導入！"})

    except Exception as e:
        return JsonResponse({"error": f"處理檔案時發生錯誤：{str(e)}"}, status=500)


def upload_energy_management_data(request):
    file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/2021-2023_ESG/energy_management.xlsx"  # 替換為實際的檔案路徑

    try:
        # 讀取 Excel 檔案
        df = pd.read_excel(file_path)

        # 檢查必要欄位是否存在
        required_columns = [
            "市場別", "年份", "公司代號", "公司名稱",
            "使用率(再生能源/總能源)", "資料範圍", "取得驗證"
        ]
        if not all(column in df.columns for column in required_columns):
            return JsonResponse({"error": "Excel 檔案格式錯誤，缺少必要欄位。"}, status=400)

        # 清理數據：處理 NaN 和非數字值
        def clean_value(value):
            if pd.isna(value):  # 如果是 NaN，返回 None
                return None
            if isinstance(value, str) and value.strip() in ["無", "無統計相關數據", "無，無統計相關數據"]:
                return None
            return value.strip() if isinstance(value, str) else value

        # 清理年份欄位，將無效的年份轉為 None 並移除無效年份行
        df["年份"] = pd.to_numeric(df["年份"], errors="coerce")
        df = df.dropna(subset=["年份"])  # 移除年份為 NaN 的行
        df["年份"] = df["年份"].astype(int)  # 確保年份是整數

        # 清理公司代號，轉為字串並去掉小數點
        df["公司代號"] = df["公司代號"].apply(
            lambda x: str(int(x)) if pd.notna(x) else None)

        # 清理其他數據欄位
        for column in ["使用率(再生能源/總能源)"]:
            if column in df.columns:
                df[column] = df[column].apply(clean_value)

        # 去除原始資料中的重複項
        df = df.drop_duplicates(subset=["年份", "公司代號", "公司名稱", "市場別"])

        # 將資料寫入資料庫
        for _, row in df.iterrows():
            # 檢查資料是否已存在（基於主要欄位）
            if EnergyManagement.objects.filter(
                market=row["市場別"],
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"]
            ).exists():
                print(f"重複資料跳過：{row['年份']} - {row['公司代號']} - {row['公司名稱']}")
                continue  # 如果資料已存在，跳過此行

            # 創建新記錄
            EnergyManagement.objects.create(
                market=row["市場別"],
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"],
                usage_rate=row.get("使用率(再生能源/總能源)", None),
                data_scope=row.get("資料範圍", None),
                certification=row.get("取得驗證", None),
            )

        return JsonResponse({"success": "資料成功導入！"})

    except Exception as e:
        return JsonResponse({"error": f"處理檔案時發生錯誤：{str(e)}"}, status=500)


def upload_greenhouse_gas_emission_data(request):
    file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/2021-2023_ESG/greenhouse_gas_emissions.xlsx"  # 替換為實際的檔案路徑

    try:
        # 讀取 Excel 檔案
        df = pd.read_excel(file_path)

        # 檢查必要欄位是否存在
        required_columns = [
            "市場別", "年份", "公司代號", "公司名稱",
            "範疇一-排放量(噸CO2e)", "範疇一-資料邊界", "範疇一-取得驗證",
            "範疇二-排放量(噸CO2e)", "範疇二-資料邊界", "範疇二-取得驗證",
            "範疇三-排放量(噸CO2e)", "範疇三-資料邊界", "範疇三-取得驗證",
            "溫室氣體排放密集度-密集度(噸CO2e/單位)", "溫室氣體排放密集度-單位"
        ]
        if not all(column in df.columns for column in required_columns):
            return JsonResponse({"error": "Excel 檔案格式錯誤，缺少必要欄位。"}, status=400)

        # 清理數據：處理 NaN 和非數字值
        def clean_value(value):
            if pd.isna(value):
                return None
            if isinstance(value, str) and value.strip() in ["無", "無統計相關數據", "無，無統計相關數據"]:
                return None
            return value.strip() if isinstance(value, str) else value

        # 清理年份欄位，將無效的年份轉為 None 並移除無效年份行
        df["年份"] = pd.to_numeric(df["年份"], errors="coerce")
        df = df.dropna(subset=["年份"])
        df["年份"] = df["年份"].astype(int)

        # 清理公司代號，轉為字串並去掉小數點
        df["公司代號"] = df["公司代號"].apply(
            lambda x: str(int(x)) if pd.notna(x) else None)

        # 清理其他數據欄位
        for column in [
            "範疇一-排放量(噸CO2e)", "範疇二-排放量(噸CO2e)", "範疇三-排放量(噸CO2e)",
            "溫室氣體排放密集度-密集度(噸CO2e/單位)"
        ]:
            if column in df.columns:
                df[column] = pd.to_numeric(df[column], errors="coerce")

        # 去除重複項
        df = df.drop_duplicates(subset=["市場別", "年份", "公司代號", "公司名稱"])

        # 將資料寫入資料庫
        for _, row in df.iterrows():
            if GreenhouseGasEmission.objects.filter(
                market=row["市場別"],
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"]
            ).exists():
                print(f"重複資料跳過：{row['年份']} - {row['公司代號']} - {row['公司名稱']}")
                continue

            GreenhouseGasEmission.objects.create(
                market=row["市場別"],
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"],
                scope_1_emissions=row.get("範疇一-排放量(噸CO2e)", None),
                scope_1_boundary=row.get("範疇一-資料邊界", None),
                scope_1_verification=row.get("範疇一-取得驗證", None),
                scope_2_emissions=row.get("範疇二-排放量(噸CO2e)", None),
                scope_2_boundary=row.get("範疇二-資料邊界", None),
                scope_2_verification=row.get("範疇二-取得驗證", None),
                scope_3_emissions=row.get("範疇三-排放量(噸CO2e)", None),
                scope_3_boundary=row.get("範疇三-資料邊界", None),
                scope_3_verification=row.get("範疇三-取得驗證", None),
                emission_intensity=row.get("溫室氣體排放密集度-密集度(噸CO2e/單位)", None),
                intensity_unit=row.get("溫室氣體排放密集度-單位", None)
            )

        return JsonResponse({"success": "資料成功導入！"})

    except Exception as e:
        return JsonResponse({"error": f"處理檔案時發生錯誤：{str(e)}"}, status=500)
