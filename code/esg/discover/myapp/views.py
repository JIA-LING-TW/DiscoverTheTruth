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
    # 獲取篩選參數
    year = request.GET.get("year")
    company_code = request.GET.get("company_code")
    company_name = request.GET.get("company_name")
    database = request.GET.get("database")  # 取得使用者選擇的資料庫

    # 構建篩選條件
    filters = Q()
    if year:
        filters &= Q(year=year)
    if company_code:
        filters &= Q(company_code__icontains=company_code)
    if company_name:
        filters &= Q(company_name__icontains=company_name)

    # 根據選擇的資料庫查詢相應的資料
    if database == 'water':
        results = WaterResourceManagement.objects.filter(filters)
        fields = [
            'year', 'company_code', 'company_name', 'water_usage',
            'data_scope', 'water_density', 'density_unit', 'certification'
        ]
    elif database == 'energy':
        results = EnergyManagement.objects.filter(filters)
        fields = [
            'year', 'company_code', 'company_name', 'renewable_energy_usage_rate',
            'data_scope', 'certification'
        ]
    elif database == 'greenhouse':
        results = GreenhouseGasEmission.objects.filter(filters)
        fields = [
            'year', 'company_code', 'company_name', 'scope_1_emissions',
            'scope_2_emissions', 'scope_3_emissions', 'intensity', 'intensity_unit'
        ]
    elif database == 'waste':
        results = WasteManagement.objects.filter(filters)
        fields = [
            'year', 'company_code', 'company_name', 'hazardous_waste',
            'non_hazardous_waste', 'total_weight', 'data_scope',
            'waste_density', 'waste_density_unit', 'certification'
        ]
    else:
        # 如果資料庫選擇無效，返回空結果或錯誤
        results = []
        fields = []

    # 將查詢結果轉換成字典格式
    results_dict = [model_to_dict(item) for item in results]

    # 將篩選結果傳遞給模板
    context = {
        "results": results_dict,
        "year": year,
        "company_code": company_code,
        "company_name": company_name,
        "database": database,  # 讓模板知道使用的是哪個資料庫
        "fields": fields,  # 顯示的欄位名稱
    }
    return render(request, 'ESGEachCompany.html', context)


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

        # 確保公司代號是字串格式，並去除小數點
        df["公司代號"] = df["公司代號"].apply(lambda x: str(
            int(x)) if pd.notna(x) else '')  # 去除小數點並轉為字串

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


def upload_waste_management_data(request):
    file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/2021-2023_ESG/waste_management.xlsx"  # 替換成實際檔案路徑

    try:
        # 讀取 XLSX 檔案
        df = pd.read_excel(file_path)

        # 確保公司代號是字串格式，並去除小數點
        df["公司代號"] = df["公司代號"].apply(lambda x: str(
            int(x)) if pd.notna(x) else '')  # 去除小數點並轉為字串

        # 檢查必要欄位是否存在
        required_columns = [
            "年份", "公司代號", "公司名稱", "有害廢棄物量(公噸)", "非有害廢棄物量(公噸)",
            "總重量(有害+非有害)(公噸)", "資料範圍", "廢棄物密集度(公噸/單位)", "廢棄物密集度-單位", "取得驗證"
        ]
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
        df["有害廢棄物量(公噸)"] = df["有害廢棄物量(公噸)"].apply(clean_value)
        df["非有害廢棄物量(公噸)"] = df["非有害廢棄物量(公噸)"].apply(clean_value)
        df["總重量(有害+非有害)(公噸)"] = df["總重量(有害+非有害)(公噸)"].apply(clean_value)
        df["廢棄物密集度(公噸/單位)"] = df["廢棄物密集度(公噸/單位)"].apply(clean_value)

        # 處理年份欄位，將無效的年份轉為 None
        df["年份"] = pd.to_numeric(df["年份"], errors="coerce")

        # 去除原始資料中的重複項
        df = df.drop_duplicates(subset=["年份", "公司代號"])

        # 將資料寫入資料庫
        for _, row in df.iterrows():
            # 檢查資料是否已存在：根據 "年份" 和 "公司代號"
            if WasteManagement.objects.filter(year=row["年份"], company_code=row["公司代號"]).exists():
                print(f"資料已存在：{row['年份']} - {row['公司代號']}")
                continue  # 如果資料已存在，跳過此行

            # 創建新記錄
            WasteManagement.objects.create(
                year=int(row["年份"]) if pd.notna(
                    row["年份"]) else None,  # 只在年份有效時才插入
                company_code=row["公司代號"],  # 確保是字串格式
                company_name=row["公司名稱"],
                hazardous_waste=row.get("有害廢棄物量(公噸)", None),
                non_hazardous_waste=row.get("非有害廢棄物量(公噸)", None),
                total_weight=row.get("總重量(有害+非有害)(公噸)", None),
                data_scope=row.get("資料範圍", None),
                waste_density=row.get("廢棄物密集度(公噸/單位)", None),
                waste_density_unit=row.get("廢棄物密集度-單位", None),
                certification=row.get("取得驗證", None),
            )

        return JsonResponse({"success": "資料成功導入！"})

    except Exception as e:
        return JsonResponse({"error": f"處理檔案時發生錯誤：{str(e)}"}, status=500)


def upload_energy_management_data(request):
    file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/2021-2023_ESG/energy_management.xlsx"  # 替換成實際檔案路徑

    try:
        # 讀取 Excel 檔案
        df = pd.read_excel(file_path)

        # 檢查必要欄位是否存在
        required_columns = ["年份", "公司代號", "公司名稱",
                            "使用率(再生能源/總能源)", "資料範圍", "取得驗證"]
        if not all(column in df.columns for column in required_columns):
            return JsonResponse({"error": "Excel 檔案格式錯誤，缺少必要欄位。"}, status=400)

        # 清理數據：將非數字或無效值替換為 None
        def clean_value(value):
            if pd.isna(value):  # 如果是 NaN，返回 None
                return None
            if isinstance(value, str) and value.strip() in ["無", "無統計相關數據", "無，無統計相關數據"]:
                return None
            return value.strip() if isinstance(value, str) else value  # 去除空白

        # 清理年份欄位，將無效的年份轉為 None 並移除無效年份行
        df["年份"] = pd.to_numeric(df["年份"], errors="coerce")
        df = df.dropna(subset=["年份"])  # 移除年份為 NaN 的行
        df["年份"] = df["年份"].astype(int)  # 確保年份是整數

        # 清理其他欄位數據
        df["使用率(再生能源/總能源)"] = df["使用率(再生能源/總能源)"].apply(clean_value)
        df["資料範圍"] = df["資料範圍"].apply(clean_value)
        df["取得驗證"] = df["取得驗證"].apply(clean_value)

        # 去除原始資料中的重複項
        df = df.drop_duplicates(subset=["年份", "公司代號"])

        # 將資料寫入資料庫
        for _, row in df.iterrows():
            # 檢查資料是否已存在
            if EnergyManagement.objects.filter(year=row["年份"], company_code=row["公司代號"]).exists():
                print(f"資料已存在：{row['年份']} - {row['公司代號']}")
                continue  # 如果資料已存在，跳過此行

            # 創建新記錄
            EnergyManagement.objects.create(
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"],
                renewable_energy_usage_rate=row["使用率(再生能源/總能源)"],
                data_scope=row.get("資料範圍", None),
                certification=row.get("取得驗證", None),
            )

        return JsonResponse({"success": "資料成功導入！"})

    except Exception as e:
        return JsonResponse({"error": f"處理檔案時發生錯誤：{str(e)}"}, status=500)


def upload_greenhouse_gas_emission_data(request):
    file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/2021-2023_ESG/greenhouse_gas_emissions.xlsx"

    try:
        # 讀取 Excel 檔案
        df = pd.read_excel(file_path)

        # 檢查必要欄位是否存在
        required_columns = [
            "年份", "公司代號", "公司名稱",
            "範疇一-排放量(噸CO2e)", "範疇一-資料邊界", "範疇一-取得驗證",
            "範疇二-排放量(噸CO2e)", "範疇二-資料邊界", "範疇二-取得驗證",
            "範疇三-排放量(噸CO2e)", "範疇三-資料邊界", "範疇三-取得驗證",
            "溫室氣體排放密集度-密集度(噸CO2e/單位)", "溫室氣體排放密集度-單位"
        ]
        if not all(column in df.columns for column in required_columns):
            return JsonResponse({"error": "Excel 檔案格式錯誤，缺少必要欄位。"}, status=400)

        # 清理數據函數
        def clean_value(value):
            if pd.isna(value):
                return None
            if isinstance(value, str) and value.strip() in ["無", "NA", "無，NA", "無統計相關數據"]:
                return None
            try:
                return float(value)
            except (ValueError, TypeError):
                return None

        def clean_company_code(value):
            if pd.isna(value):
                return None
            if isinstance(value, float):
                return str(int(value))
            return str(value).strip()

        # 清理數據
        df["年份"] = pd.to_numeric(df["年份"], errors="coerce")
        df = df.dropna(subset=["年份"])
        df["年份"] = df["年份"].astype(int)

        df["公司代號"] = df["公司代號"].apply(clean_company_code)
        df = df.dropna(subset=["公司代號"])  # 移除公司代號為空的行

        columns_to_clean = [
            "範疇一-排放量(噸CO2e)", "範疇二-排放量(噸CO2e)",
            "範疇三-排放量(噸CO2e)", "溫室氣體排放密集度-密集度(噸CO2e/單位)"
        ]
        for col in columns_to_clean:
            df[col] = df[col].apply(clean_value)

        df = df.drop_duplicates(subset=["年份", "公司代號"])

        # 將資料寫入資料庫
        for _, row in df.iterrows():
            if GreenhouseGasEmission.objects.filter(year=row["年份"], company_code=row["公司代號"]).exists():
                continue
            GreenhouseGasEmission.objects.create(
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"],
                scope_1_emissions=row["範疇一-排放量(噸CO2e)"],
                scope_1_boundary=row.get("範疇一-資料邊界", None),
                scope_1_verification=row.get("範疇一-取得驗證", None),
                scope_2_emissions=row["範疇二-排放量(噸CO2e)"],
                scope_2_boundary=row.get("範疇二-資料邊界", None),
                scope_2_verification=row.get("範疇二-取得驗證", None),
                scope_3_emissions=row.get("範疇三-排放量(噸CO2e)", None),
                scope_3_boundary=row.get("範疇三-資料邊界", None),
                scope_3_verification=row.get("範疇三-取得驗證", None),
                intensity=row["溫室氣體排放密集度-密集度(噸CO2e/單位)"],
                intensity_unit=row.get("溫室氣體排放密集度-單位", None),
            )

        return JsonResponse({"success": "資料成功導入！"})

    except Exception as e:
        return JsonResponse({"error": f"處理檔案時發生錯誤：{str(e)}"}, status=500)
