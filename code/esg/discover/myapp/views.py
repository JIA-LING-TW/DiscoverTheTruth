from .models import ShareholderRisk
from .models import Investor_Communication_Risk
from .models import Hr_Develop_Risk
from .models import Functiona_Committee_Risk
from .models import BoardOfDirectorsRisk
from django.http import JsonResponse
import locale
import requests
from .models import WaterResourceRisk, EnergyResourceRisk, WasteManagementRisk, GreenRisk
from django.shortcuts import render
import os
# import time
import string
import random
import pandas as pd

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages

# 專案中的模型匯入
from .models import (
    GreenRisk, WaterResourceRisk, EnergyResourceRisk, WasteManagementRisk,
    WaterResourceManagement, EnergyManagement, GreenhouseGasEmission, WasteManagement,
    ClimateRiskAndOpportunity, CompanyBoard, CorporateGovernance, EmployeeDevelop,
    CompanyGovernance, Shareholder, SustainabilityReport
)


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
        'emission': GreenhouseGasEmission,
        'climate': ClimateRiskAndOpportunity,
        'board': CompanyBoard,
        'governance': CorporateGovernance,  # 公司治理
        'investor_communication': CompanyGovernance,  # 投資人溝通
        'employee': EmployeeDevelop,
        'shareholder': Shareholder,
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
            filters['company_code__icontains'] = company_code

        data = selected_model.objects.filter(**filters)

        # 提取字段名稱和顯示名稱
        fields = [(field.name, field.verbose_name)
                  for field in selected_model._meta.fields]

    # 顯示的篩選條件
    categories = [
        ('water', '水資源管理'),
        ('waste', '廢棄物管理'),
        ('energy', '能源管理'),
        ('emission', '溫室氣體排放'),
        ('climate', '氣候相關議題'),
        ('board', '董事會'),
        ('governance', '公司治理'),
        ('investor_communication', '投資人溝通'),  # 新增投資人溝通分類
        ('employee', '人力資源發展'),
        ('shareholder', '持股及控制力'),
    ]
    market_types = ['上市', '上櫃']
    years = [2021, 2022, 2023]

    context = {
        'data': data,
        'fields': fields,
        'category': category,
        'market_type': market_type,
        'year': year,
        'company_name': company_name,
        'company_code': company_code,
        'categories': categories,
        'market_types': market_types,
        'years': years,
    }

    return render(request, 'ESGEachCompany.html', context)


def ESGReal(request):
    return render(request, 'ESGReal.html')


# 設定地區為台灣，使用台灣的金額格式
locale.setlocale(locale.LC_ALL, 'zh_TW.UTF-8')


def ESGRisk(request):
    # 取得篩選選項
    selected_year = request.GET.get('report_year')
    selected_topic = request.GET.get('risk_topic')
    company_id = request.GET.get('company_id', '').strip()  # 去除多餘空白

    risks = []  # 初始化風險資料
    api_data = []  # 初始化 API 資料
    message = None  # 提示訊息

    # 風險議題與模型的對應
    topic_model_map = {
        "water": WaterResourceRisk,
        "energy": EnergyResourceRisk,
        "waste": WasteManagementRisk,
        "carbon": GreenRisk,
    }

    if selected_topic and selected_topic in topic_model_map:
        # 根據議題篩選對應模型
        model = topic_model_map[selected_topic]
        risks = model.objects.all()

        # 篩選報告年度
        if selected_year:
            risks = risks.filter(report_year=selected_year)

        # 篩選公司代碼
        if company_id:
            risks = risks.filter(company_id=company_id)

        # 檢查資料是否存在
        if not risks.exists():
            message = "目前無相關風險資料"

        # 向 API 發送請求
        try:
            api_url = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"
            response = requests.get(api_url)
            response.raise_for_status()  # 確保請求成功
            raw_api_data = response.json()  # 假設 API 返回 JSON 資料

            # 篩選 API 資料
            for item in raw_api_data:
                if not company_id or item.get("公司代號") == company_id:
                    # 格式化實收資本額
                    capital = item.get("實收資本額")
                    formatted_capital = locale.format_string(
                        "%d", int(capital), grouping=True) if capital else None

                    api_data.append({
                        "company_name": item.get("公司簡稱"),
                        "year": item.get("年度"),
                        "company_id": item.get("公司代號"),
                        "market_category": item.get("市場別"),
                        "chairman": item.get("董事長"),  # 董事長
                        "ceo": item.get("總經理"),  # 總經理
                        "capital": formatted_capital,  # 格式化的實收資本額
                    })

            if not api_data:
                message = "API 無符合條件的資料"
        except requests.RequestException as e:
            api_data = []
            message = f"無法取得 API 資料：{e}"
    else:
        message = "請選擇一個議題進行查詢"

    # 渲染篩選後的結果
    return render(request, 'ESGRisk.html', {
        'risks': risks,
        'api_data': api_data,
        'selected_year': selected_year,
        'selected_topic': selected_topic,
        'company_id': company_id,
        'message': message,
    })


def forget(request):
    return render(request, 'forget.html')


def contact(request):
    return render(request, 'contact.html')


# 生成隨機驗證碼

def generate_captcha():
    characters = string.ascii_uppercase + string.digits  # 可使用字母和數字
    captcha = ''.join(random.choices(characters, k=6))  # 生成6位隨機字符
    return captcha


def login(request):
    if request.method == "POST":
        # 獲取表單輸入
        username = request.POST.get('username')
        password = request.POST.get('password')
        captcha_input = request.POST.get('captcha_input')  # 用戶輸入的驗證碼

        # 獲取 session 中的正確驗證碼
        captcha = request.session.get('captcha', '')

        # 驗證用戶輸入的驗證碼
        if captcha_input != captcha:
            messages.error(request, "驗證碼錯誤，請重新輸入。")
            return redirect('login')  # 驗證碼錯誤，重新載入頁面

        # 驗證用戶名和密碼
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')  # 登入成功，跳轉到首頁或其他頁面
        else:
            messages.error(request, "使用者名稱或密碼錯誤，請重新輸入。")

    # 生成並儲存新的驗證碼到 session
    captcha = generate_captcha()
    request.session['captcha'] = captcha

    return render(request, 'login.html', {'captcha': captcha, 'message': messages.get_messages(request)})


@csrf_exempt  # 暫時禁用 CSRF 驗證，用於測試 AJAX，正式部署時應移除
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('passwd')
        confirm_password = request.POST.get('passwd1')

        # 密碼不一致檢查
        if password != confirm_password:
            return JsonResponse({'message': '密碼不一致！'})

        # 使用者名稱是否已存在
        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': '使用者名稱已存在！'})

        # Email 是否已被使用
        if User.objects.filter(email=email).exists():
            return JsonResponse({'message': 'Email 已被使用！'})

        # 建立新使用者
        User.objects.create(
            username=username,
            email=email,
            password=make_password(password)  # 加密密碼
        )

        return JsonResponse({'message': '註冊成功！'})

    return render(request, 'register.html')


# def report(request):

#     market_type = request.GET.get('market_type')
#     year = request.GET.get('year')
#     company_code = request.GET.get('company_code')


#     reports = SustainabilityReport.objects.all()
#     if market_type:
#         reports = reports.filter(market_type=market_type)
#     if year:
#         reports = reports.filter(year=year)
#     if company_code:
#         reports = reports.filter(company_code__icontains=company_code)


#     available_years = ['2021', '2022', '2023']


#     context = {
#         'reports': reports,
#         'market_type': market_type,
#         'year': year,
#         'company_code': company_code,
#         'available_years': available_years,
#     }
#     return render(request, 'report.html', context)


def report(request):
    # 取得篩選參數
    market_type = request.GET.get('market_type')
    year = request.GET.get('year')
    company_code = request.GET.get('company_code')

    # 依據篩選條件過濾報告書
    reports = SustainabilityReport.objects.all()
    if market_type:
        reports = reports.filter(market_type=market_type)
    if year:
        reports = reports.filter(year=year)
    if company_code:
        reports = reports.filter(company_code__icontains=company_code)

    # 分頁設定：每頁顯示 20 筆資料
    paginator = Paginator(reports, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 傳遞年度選項
    years = [2021, 2022, 2023]

    # 渲染模板並傳遞分頁後的報告書資料
    context = {
        'page_obj': page_obj,
        'market_type': market_type,
        'year': year,
        'company_code': company_code,
        'years': years,  # 傳遞年度選項
    }
    return render(request, 'report.html', context)


def upload_water_resource_management_data(request):
    # file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/2021-2023_ESG/water_resource_management.xlsx"  # 請替換為實際檔案路徑
    file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "2021-2023_ESG(E)", "water_resource_management.xlsx"))

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
    # file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/2021-2023_ESG/waste_management.xlsx"  # 替換為實際檔案路徑
    file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "2021-2023_ESG(E)", "waste_management.xlsx"))

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
    # 定義文件路徑（替換為實際的檔案路徑）
    file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "2021-2023_ESG(E)", "energy_management.xlsx"))

    try:
        # 讀取 Excel 檔案
        df = pd.read_excel(file_path)

        # 檢查 Excel 是否包含所有必要欄位
        required_columns = [
            "市場別", "年份", "公司代號", "公司名稱",
            "使用率(再生能源/總能源)", "資料範圍", "取得驗證"
        ]
        if not all(column in df.columns for column in required_columns):
            return JsonResponse({"error": "Excel 檔案格式錯誤，缺少必要欄位。"}, status=400)

        # 數據清理函數：處理 NaN 和無效值
        def clean_value(value):
            if pd.isna(value):  # 如果是 NaN，返回 None
                return None
            if isinstance(value, str) and value.strip() in ["無", "無統計相關數據", "無，無統計相關數據"]:
                return None
            return value.strip() if isinstance(value, str) else value

        # 清理年份欄位，轉換為整數並移除無效年份行
        df["年份"] = pd.to_numeric(df["年份"], errors="coerce")  # 將年份轉為數字類型
        df = df.dropna(subset=["年份"])  # 移除年份為 NaN 的行
        df["年份"] = df["年份"].astype(int)  # 確保年份為整數

        # 清理公司代號，將其轉為字串並去除小數點
        df["公司代號"] = df["公司代號"].apply(
            lambda x: str(int(x)) if pd.notna(x) else None)

        # 清理其他數據欄位
        for column in ["使用率(再生能源/總能源)"]:
            if column in df.columns:
                df[column] = df[column].apply(clean_value)

        # 去除重複數據（基於年份、公司代號、公司名稱、和市場別）
        df = df.drop_duplicates(subset=["年份", "公司代號", "公司名稱", "市場別"])

        # 將數據導入資料庫
        for _, row in df.iterrows():
            # 檢查資料是否已存在
            if EnergyManagement.objects.filter(
                market_type=row["市場別"],  # 修改此處以匹配資料庫中的正確欄位名稱
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"]
            ).exists():
                print(f"重複資料跳過：{row['年份']} - {row['公司代號']} - {row['公司名稱']}")
                continue  # 若資料已存在，跳過此行

            # 建立新記錄
            EnergyManagement.objects.create(
                market_type=row["市場別"],  # 確保欄位名稱與資料庫模型一致
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"],
                usage_rate=row.get("使用率(再生能源/總能源)", None),
                data_scope=row.get("資料範圍", None),
                certification=row.get("取得驗證", None),
            )

        return JsonResponse({"success": "資料成功導入！"})

    except Exception as e:
        # 返回錯誤訊息
        return JsonResponse({"error": f"處理檔案時發生錯誤：{str(e)}"}, status=500)


def upload_greenhouse_gas_emission_data(request):
    # 定義文件路徑（替換為實際的檔案路徑）
    file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "2021-2023_ESG(E)", "greenhouse_gas_emissions.xlsx"))

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

        # 數據清理函數：處理 NaN 和無效值
        def clean_value(value):
            if pd.isna(value):
                return None
            if isinstance(value, str) and value.strip() in ["無", "無統計相關數據", "無，無統計相關數據"]:
                return None
            return value.strip() if isinstance(value, str) else value

        # 清理年份欄位，確保為有效整數
        df["年份"] = pd.to_numeric(df["年份"], errors="coerce")
        df = df.dropna(subset=["年份"])  # 移除年份為 NaN 的行
        df["年份"] = df["年份"].astype(int)

        # 清理公司代號，轉為字串並去掉小數點
        df["公司代號"] = df["公司代號"].apply(
            lambda x: str(int(x)) if pd.notna(x) else None)

        # 清理數據欄位，將非數字值轉為 None
        numeric_columns = [
            "範疇一-排放量(噸CO2e)", "範疇二-排放量(噸CO2e)", "範疇三-排放量(噸CO2e)",
            "溫室氣體排放密集度-密集度(噸CO2e/單位)"
        ]
        for column in numeric_columns:
            if column in df.columns:
                df[column] = pd.to_numeric(df[column], errors="coerce")

        # 清理其他數據欄位
        text_columns = [
            "範疇一-資料邊界", "範疇一-取得驗證",
            "範疇二-資料邊界", "範疇二-取得驗證",
            "範疇三-資料邊界", "範疇三-取得驗證",
            "溫室氣體排放密集度-單位"
        ]
        for column in text_columns:
            if column in df.columns:
                df[column] = df[column].apply(clean_value)

        # 去除重複數據（基於市場別、年份、公司代號和公司名稱）
        df = df.drop_duplicates(subset=["市場別", "年份", "公司代號", "公司名稱"])

        # 將數據寫入資料庫
        for _, row in df.iterrows():
            # 檢查資料是否已存在
            if GreenhouseGasEmission.objects.filter(
                market_type=row["市場別"],  # 確保欄位名稱與資料庫模型一致
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"]
            ).exists():
                print(f"重複資料跳過：{row['年份']} - {row['公司代號']} - {row['公司名稱']}")
                continue

            # 建立新記錄
            GreenhouseGasEmission.objects.create(
                market_type=row["市場別"],
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
        # 捕獲異常並返回錯誤訊息
        return JsonResponse({"error": f"處理檔案時發生錯誤：{str(e)}"}, status=500)


# def upload_excel(request):
#     if request.method == "POST":
#         form = ExcelUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             # 獲取上傳的 Excel 檔案
#             excel_file = request.FILES['file']

#             try:
#                 # 使用 pandas 讀取 Excel 檔案
#                 df = pd.read_excel(excel_file, engine='openpyxl')

#                 # 處理布林欄位，將空值或 NaT 轉為 False
#                 df['修正後報告書'] = df['修正後報告書'].fillna(False).astype(bool)
#                 df['英文版修正後報告書'] = df['英文版修正後報告書'].fillna(False).astype(bool)

#                 # 處理日期欄位，將 NaT 轉為 None
#                 date_columns = [
#                     '上傳日期',
#                     '修正後報告書上傳日期',
#                     '英文版上傳日期',
#                     '英文版修正後報告書上傳日期'
#                 ]
#                 for col in date_columns:
#                     if col in df.columns:
#                         df[col] = pd.to_datetime(
#                             df[col], errors='coerce').dt.date

#                 # 迭代 DataFrame，將資料存入資料庫
#                 for _, row in df.iterrows():
#                     SustainabilityReport.objects.create(
#                         market_type=row.get('市場別'),
#                         year=row.get('年份'),
#                         company_code=row.get('公司代號'),
#                         company_name=row.get('公司名稱'),
#                         company_abbreviation=row.get('英文簡稱'),
#                         declaration_reason=row.get('申報原因'),
#                         industry_category=row.get('產業類別'),
#                         report_period=row.get('報告書內容涵蓋期間'),
#                         guidelines=row.get('編製依循準則'),
#                         third_party_verifier=row.get('第三方驗證單位'),
#                         upload_date=row.get('上傳日期') or None,
#                         revised_report=row.get('修正後報告書', False),
#                         revised_report_upload_date=row.get(
#                             '修正後報告書上傳日期') or None,
#                         english_report_url=row.get('永續報告書英文版網址'),
#                         english_report_upload_date=row.get('英文版上傳日期') or None,
#                         english_revised_report=row.get('英文版修正後報告書', False),
#                         english_revised_report_upload_date=row.get(
#                             '英文版修正後報告書上傳日期') or None,
#                         contact_info=row.get('報告書聯絡資訊'),
#                         remarks=row.get('備註'),
#                     )

#                 # 導向成功頁面或顯示成功訊息
#                 return redirect('success_page')

#             except Exception as e:
#                 # 若發生錯誤，顯示錯誤訊息
#                 return render(request, 'upload.html', {'form': form, 'error': str(e)})

#     else:
#         form = ExcelUploadForm()

#     return render(request, 'upload.html', {'form': form})


def upload_weather_management_data(request):
    # 替換為實際的檔案路徑
    # file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/2021-2023_ESG(E)/weather_management.xlsx"
    file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "2021-2023_ESG(E)", "weather_management.xlsx"))

    try:
        # 讀取 Excel 檔案
        df = pd.read_excel(file_path)

        # 檢查必要欄位是否存在
        required_columns = [
            "市場別", "年份", "公司代號", "公司名稱",
            "董事會與管理階層對於氣候相關風險與機會之監督及治理-董事會與管理階層對於氣候相關風險與機會之監督及治理",
            "辨識之氣候風險與機會如何影響企業之業務、策略及財務 (短期、中期、長期)-辨識之氣候風險與機會如何影響企業之業務、策略及財務 (短期、中期、長期)",
            "極端氣候事件及轉型行動對財務之影響-極端氣候事件及轉型行動對財務之影響",
            "氣候風險之辨識、評估及管理流程如何整合於整體風險管理制度-氣候風險之辨識、評估及管理流程如何整合於整體風險管理制度",
            "若使用情境分析評估面對氣候變遷風險之韌性，應說明所使用之情境、參數、假設、分析因子及主要財務影響。-若使用情境分析評估面對氣候變遷風險之韌性，應說明所使用之情境、參數、假設、分析因子及主要財務影響。",
            "若有因應管理氣候相關風險之轉型計畫，說明該計畫內容，及用於辨識及管理實體風險及轉型風險之指標與目標。-若有因應管理氣候相關風險之轉型計畫，說明該計畫內容，及用於辨識及管理實體風險及轉型風險之指標與目標。",
            "若使用內部碳定價作為規劃工具，應說明價格制定基礎。-若使用內部碳定價作為規劃工具，應說明價格制定基礎。",
            "若有設定氣候相關目標，應說明所涵蓋之活動、溫室氣體排放範疇、規劃期程，每年達成進度等資訊；若使用碳抵換或再生能源憑證(RECs)以達成相關目標，應說明所抵換之減碳額度來源及數量或再生能源憑證(RECs)數量。-若有設定氣候相關目標，應說明所涵蓋之活動、溫室氣體排放範疇、規劃期程，每年達成進度等資訊；若使用碳抵換或再生能源憑證(RECs)以達成相關目標，應說明所抵換之減碳額度來源及數量或再生能源憑證(RECs)數量。"
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
            "董事會與管理階層對於氣候相關風險與機會之監督及治理-董事會與管理階層對於氣候相關風險與機會之監督及治理",
            "辨識之氣候風險與機會如何影響企業之業務、策略及財務 (短期、中期、長期)-辨識之氣候風險與機會如何影響企業之業務、策略及財務 (短期、中期、長期)",
            "極端氣候事件及轉型行動對財務之影響-極端氣候事件及轉型行動對財務之影響",
            "氣候風險之辨識、評估及管理流程如何整合於整體風險管理制度-氣候風險之辨識、評估及管理流程如何整合於整體風險管理制度",
            "若使用情境分析評估面對氣候變遷風險之韌性，應說明所使用之情境、參數、假設、分析因子及主要財務影響。-若使用情境分析評估面對氣候變遷風險之韌性，應說明所使用之情境、參數、假設、分析因子及主要財務影響。",
            "若有因應管理氣候相關風險之轉型計畫，說明該計畫內容，及用於辨識及管理實體風險及轉型風險之指標與目標。-若有因應管理氣候相關風險之轉型計畫，說明該計畫內容，及用於辨識及管理實體風險及轉型風險之指標與目標。",
            "若使用內部碳定價作為規劃工具，應說明價格制定基礎。-若使用內部碳定價作為規劃工具，應說明價格制定基礎。",
            "若有設定氣候相關目標，應說明所涵蓋之活動、溫室氣體排放範疇、規劃期程，每年達成進度等資訊；若使用碳抵換或再生能源憑證(RECs)以達成相關目標，應說明所抵換之減碳額度來源及數量或再生能源憑證(RECs)數量。-若有設定氣候相關目標，應說明所涵蓋之活動、溫室氣體排放範疇、規劃期程，每年達成進度等資訊；若使用碳抵換或再生能源憑證(RECs)以達成相關目標，應說明所抵換之減碳額度來源及數量或再生能源憑證(RECs)數量。"
        ]:
            if column in df.columns:
                df[column] = df[column].apply(clean_value)

        # 去除重複項
        df = df.drop_duplicates(subset=["市場別", "年份", "公司代號", "公司名稱"])

        # 將資料寫入資料庫
        for _, row in df.iterrows():
            if ClimateRiskAndOpportunity.objects.filter(
                market_type=row["市場別"],
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"]
            ).exists():
                print(f"重複資料跳過：{row['年份']} - {row['公司代號']} - {row['公司名稱']}")
                continue

            ClimateRiskAndOpportunity.objects.create(
                market_type=row["市場別"],
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"],
                board_and_management_supervision=row.get(
                    "董事會與管理階層對於氣候相關風險與機會之監督及治理-董事會與管理階層對於氣候相關風險與機會之監督及治理", None),
                impact_on_business_strategy_financials=row.get(
                    "辨識之氣候風險與機會如何影響企業之業務、策略及財務 (短期、中期、長期)-辨識之氣候風險與機會如何影響企業之業務、策略及財務 (短期、中期、長期)", None),
                impact_of_extreme_weather_and_transformation_on_financials=row.get(
                    "極端氣候事件及轉型行動對財務之影響-極端氣候事件及轉型行動對財務之影響", None),
                climate_risk_identification_and_management_process=row.get(
                    "氣候風險之辨識、評估及管理流程如何整合於整體風險管理制度-氣候風險之辨識、評估及管理流程如何整合於整體風險管理制度", None),
                scenario_analysis_and_assumptions=row.get(
                    "若使用情境分析評估面對氣候變遷風險之韌性，應說明所使用之情境、參數、假設、分析因子及主要財務影響。-若使用情境分析評估面對氣候變遷風險之韌性，應說明所使用之情境、參數、假設、分析因子及主要財務影響。", None),
                transformation_plan_for_climate_risks=row.get(
                    "若有因應管理氣候相關風險之轉型計畫，說明該計畫內容，及用於辨識及管理實體風險及轉型風險之指標與目標。-若有因應管理氣候相關風險之轉型計畫，說明該計畫內容，及用於辨識及管理實體風險及轉型風險之指標與目標。", None),
                internal_carbon_pricing_basis=row.get(
                    "若使用內部碳定價作為規劃工具，應說明價格制定基礎。-若使用內部碳定價作為規劃工具，應說明價格制定基礎。", None),
                climate_related_goals_and_progress=row.get(
                    "若有設定氣候相關目標，應說明所涵蓋之活動、溫室氣體排放範疇、規劃期程，每年達成進度等資訊；若使用碳抵換或再生能源憑證(RECs)以達成相關目標，應說明所抵換之減碳額度來源及數量或再生能源憑證(RECs)數量。-若有設定氣候相關目標，應說明所涵蓋之活動、溫室氣體排放範疇、規劃期程，每年達成進度等資訊；若使用碳抵換或再生能源憑證(RECs)以達成相關目標，應說明所抵換之減碳額度來源及數量或再生能源憑證(RECs)數量。", None)
            )

        return JsonResponse({"success": "資料成功導入！"})

    except Exception as e:
        return JsonResponse({"error": f"處理檔案時發生錯誤：{str(e)}"}, status=500)


def upload_company_board_data(request):
    # file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/2021-2023_ESG(G)/board_of_directors.xlsx"
    file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "2021-2023_ESG(G)", "board_of_directors.xlsx"))
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)

        # Check that required columns exist in the file
        required_columns = [
            "市場別", "年份", "公司代號", "公司名稱",
            "董事席次(含獨立董事)(席)", "獨立董事席次(席)", "女性董事席次及比率-席",
            "女性董事席次及比率-比率", "董事出席董事會出席率", "董事進修時數符合進修要點比率"
        ]
        if not all(column in df.columns for column in required_columns):
            return JsonResponse({"error": "Excel 檔案格式錯誤，缺少必要欄位。"}, status=400)

        # Clean data: Handle NaN and invalid values
        def clean_value(value):
            if pd.isna(value):  # If NaN, return None
                return None
            if isinstance(value, str) and value.strip() in ["無", "無統計相關數據", "無，無統計相關數據"]:
                return None
            return value.strip() if isinstance(value, str) else value

        # Clean the "年份" column, convert invalid years to None, and drop invalid year rows
        df["年份"] = pd.to_numeric(df["年份"], errors="coerce")
        df = df.dropna(subset=["年份"])  # Remove rows where "年份" is NaN
        df["年份"] = df["年份"].astype(int)  # Ensure the year is an integer

        # Clean the "公司代號" column, convert it to a string, and remove any decimals
        df["公司代號"] = df["公司代號"].apply(
            lambda x: str(int(x)) if pd.notna(x) else None)

        # Clean other numeric data columns
        numeric_columns = [
            "董事席次(含獨立董事)(席)", "獨立董事席次(席)", "女性董事席次及比率-席",
            "女性董事席次及比率-比率", "董事出席董事會出席率", "董事進修時數符合進修要點比率"
        ]
        for column in numeric_columns:
            if column in df.columns:
                df[column] = pd.to_numeric(
                    df[column], errors="coerce")  # Ensure numeric values
                # Fill NaN with 0 (or None if you prefer)
                df[column] = df[column].fillna(0)

        # Drop duplicates based on key fields
        df = df.drop_duplicates(subset=["年份", "公司代號", "公司名稱", "市場別"])

        # Insert data into the database
        for _, row in df.iterrows():
            # Check if data already exists based on key fields
            if CompanyBoard.objects.filter(
                market_type=row["市場別"],
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"]
            ).exists():
                print(f"重複資料跳過：{row['年份']} - {row['公司代號']} - {row['公司名稱']}")
                continue  # Skip this row if data already exists

            # Create a new record
            CompanyBoard.objects.create(
                market_type=row["市場別"],
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"],
                board_seats_total=row.get(
                    "董事席次(含獨立董事)(席)", 0),  # Default to 0 if NaN
                independent_board_seats=row.get("獨立董事席次(席)", 0),
                female_director_seats=row.get("女性董事席次及比率-席", 0),
                female_director_ratio=row.get("女性董事席次及比率-比率", 0),
                board_attendance_rate=row.get("董事出席董事會出席率", 0),
                training_hours_compliance_rate=row.get("董事進修時數符合進修要點比率", 0),
            )

        return JsonResponse({"success": "資料成功導入！"})

    except Exception as e:
        return JsonResponse({"error": f"處理檔案時發生錯誤：{str(e)}"}, status=500)


def upload_function_committee_data(request):
    # 請替換為實際檔案路徑
    # file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/2021-2023_ESG(G)/functional_committee.xlsx"
    file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "2021-2023_ESG(G)", "functional_committee.xlsx"))

    try:
        # 讀取 Excel 檔案
        df = pd.read_excel(file_path)

        # 檢查必要欄位是否存在
        required_columns = [
            "市場別", "年份", "公司代號", "公司名稱",
            "薪酬委員會席次(席)", "薪酬委員會獨立董事席次(席)", "薪酬委員會出席率",
            "審計委員會席次(席)", "審計委員會出席率"
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
        for column in ["薪酬委員會席次(席)", "薪酬委員會獨立董事席次(席)", "薪酬委員會出席率",
                       "審計委員會席次(席)", "審計委員會出席率"]:
            if column in df.columns:
                df[column] = df[column].apply(clean_value)

        # 去除重複資料：依年份和公司代號去重
        df = df.drop_duplicates(subset=["年份", "公司代號"])

        # 插入資料到資料庫
        for _, row in df.iterrows():
            # 檢查資料是否已存在
            if CorporateGovernance.objects.filter(year=row["年份"], company_code=row["公司代號"]).exists():
                continue  # 如果資料已存在，跳過此行

            # 創建新記錄
            CorporateGovernance.objects.create(
                market_type=row["市場別"],
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"],
                compensation_committee_seats=row.get("薪酬委員會席次(席)", None),
                independent_compensation_committee_seats=row.get(
                    "薪酬委員會獨立董事席次(席)", None),
                compensation_committee_attendance_rate=row.get(
                    "薪酬委員會出席率", None),
                audit_committee_seats=row.get("審計委員會席次(席)", None),
                audit_committee_attendance_rate=row.get("審計委員會出席率", None),
            )

        return JsonResponse({"success": "資料成功導入！"})

    except Exception as e:
        return JsonResponse({"error": f"處理檔案時發生錯誤：{str(e)}"}, status=500)


def upload_employee_develop_data(request):
    # 替換為實際檔案路徑
    # file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/2021-2023_ESG(S)/hr_develop.xlsx"
    file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "2021-2023_ESG(S)", "hr_develop.xlsx"))

    try:
        # 讀取 Excel 檔案
        df = pd.read_excel(file_path)

        # 檢查必要欄位是否存在
        required_columns = [
            "市場別", "年份", "公司代號", "公司名稱",
            "員工福利平均數(仟元/人)(每年6/2起公開)", "員工薪資平均數(仟元/人)(每年6/2起公開)",
            "非擔任主管職務之全時員工薪資平均數(仟元/人)(每年7/1起公開)", "非擔任主管職務之全時員工薪資中位數(仟元/人)(每年7/1起公開)",
            "管理職女性主管占比", "職業災害人數及比率-人數", "職業災害人數及比率-比率", "職業災害-類別",
            "火災-件數", "火災-死傷人數", "火災-比率(死傷人數/員工總人數)"
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
        for column in [
            "員工福利平均數(仟元/人)(每年6/2起公開)", "員工薪資平均數(仟元/人)(每年6/2起公開)",
            "非擔任主管職務之全時員工薪資平均數(仟元/人)(每年7/1起公開)", "非擔任主管職務之全時員工薪資中位數(仟元/人)(每年7/1起公開)",
            "管理職女性主管占比", "職業災害人數及比率-比率", "火災-比率(死傷人數/員工總人數)"
        ]:
            if column in df.columns:
                df[column] = df[column].apply(clean_value)

        # 針對其他需要處理的數字欄位，確保 NaN 轉為 None
        for column in [
            "職業災害人數及比率-人數", "火災-件數", "火災-死傷人數"
        ]:
            if column in df.columns:
                df[column] = df[column].apply(lambda x: clean_value(x))

        # 去除重複資料：依年份和公司代號去重
        df = df.drop_duplicates(subset=["年份", "公司代號"])

        # 插入資料到資料庫
        for _, row in df.iterrows():
            # 檢查資料是否已存在
            if EmployeeDevelop.objects.filter(year=row["年份"], company_code=row["公司代號"]).exists():
                continue  # 如果資料已存在，跳過此行

            # 確保火災相關欄位處理為 None 或 0，避免插入 NaN
            occupational_accident_count = row.get("職業災害人數及比率-人數", None)
            fire_incidents_count = row.get("火災-件數", None)
            fire_incidents_injury_count = row.get("火災-死傷人數", None)
            fire_incidents_rate = row.get("火災-比率(死傷人數/員工總人數)", None)

            # 若為 NaN 轉為 None
            if pd.isna(occupational_accident_count):
                occupational_accident_count = None
            if pd.isna(fire_incidents_count):
                fire_incidents_count = None
            if pd.isna(fire_incidents_injury_count):
                fire_incidents_injury_count = None
            if pd.isna(fire_incidents_rate):
                fire_incidents_rate = None

            # 創建新記錄
            EmployeeDevelop.objects.create(
                market_type=row["市場別"],
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"],
                employee_benefits_avg=row.get("員工福利平均數(仟元/人)(每年6/2起公開)", None),
                employee_salary_avg=row.get("員工薪資平均數(仟元/人)(每年6/2起公開)", None),
                non_supervisor_salary_avg=row.get(
                    "非擔任主管職務之全時員工薪資平均數(仟元/人)(每年7/1起公開)", None),
                non_supervisor_salary_median=row.get(
                    "非擔任主管職務之全時員工薪資中位數(仟元/人)(每年7/1起公開)", None),
                female_manager_ratio=row.get("管理職女性主管占比", None),
                occupational_accident_count=occupational_accident_count,
                occupational_accident_rate=row.get("職業災害人數及比率-比率", None),
                occupational_accident_category=row.get("職業災害-類別", None),
                fire_incidents_count=fire_incidents_count,
                fire_incidents_injury_count=fire_incidents_injury_count,
                fire_incidents_rate=fire_incidents_rate,
            )

        return JsonResponse({"success": "資料成功導入！"})

    except Exception as e:
        return JsonResponse({"error": f"處理檔案時發生錯誤：{str(e)}"}, status=500)


def upload_investor_communication_data(request):
    # 替換為實際檔案路徑
    # file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/2021-2023_ESG(G)/investor_communication.xlsx"
    file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "2021-2023_ESG(G)", "investor_communication.xlsx"))

    try:
        # 讀取 Excel 檔案
        df = pd.read_excel(file_path)

        # 檢查必要欄位是否存在
        required_columns = [
            "市場別", "年份", "公司代號", "公司名稱",
            "公司年度召開法說會次數(次)",
            "利害關係人或公司治理專區連結"
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

        # 清理數據欄位
        for column in [
            "公司年度召開法說會次數(次)"
        ]:
            if column in df.columns:
                df[column] = df[column].apply(clean_value)

        # 清理網址欄位
        df["利害關係人或公司治理專區連結"] = df[
            "利害關係人或公司治理專區連結"].apply(
            lambda x: x.strip() if isinstance(x, str) else None
        )

        # 去除重複資料：依年份和公司代號去重
        df = df.drop_duplicates(subset=["年份", "公司代號"])

        # 插入資料到資料庫
        for _, row in df.iterrows():
            # 檢查資料是否已存在
            if CompanyGovernance.objects.filter(year=row["年份"], company_code=row["公司代號"]).exists():
                continue  # 如果資料已存在，跳過此行

            # 確保 annual_conference_count 是有效數字或 None
            annual_conference_count = row.get("公司年度召開法說會次數(次)", None)
            if pd.isna(annual_conference_count):
                annual_conference_count = None  # 將 NaN 轉為 None

            # 創建新記錄
            CompanyGovernance.objects.create(
                market_type=row["市場別"],
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"],
                annual_conference_count=annual_conference_count,
                governance_link=row.get("利害關係人或公司治理專區連結", None),
            )

        return JsonResponse({"success": "資料成功導入！"})

    except Exception as e:
        return JsonResponse({"error": f"處理檔案時發生錯誤：{str(e)}"}, status=500)


def upload_shareholder_data(request):
    # 替換為實際檔案路徑
    # file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/2021-2023_ESG(G)/shareholding_and_control.xlsx"
    file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "2021-2023_ESG(G)", "shareholding_and_control.xlsx"))

    try:
        # 讀取 Excel 檔案
        df = pd.read_excel(file_path)

        # 檢查必要欄位是否存在
        required_columns = [
            "市場別", "年份", "公司代號", "公司名稱", "前10大股東持股情況"
        ]
        if not all(column in df.columns for column in required_columns):
            return JsonResponse({"error": "Excel 檔案格式錯誤，缺少必要欄位。"}, status=400)

        # 清理數據：處理 NaN 和無效數據
        def clean_value(value):
            if pd.isna(value) or isinstance(value, str) and value.strip() in ["無", "無統計相關數據"]:
                return None  # 將無效數據轉換為 None
            return value

        # 清理年份欄位：將無效的年份轉為 None 並移除無效年份行
        df["年份"] = pd.to_numeric(df["年份"], errors="coerce")
        df = df.dropna(subset=["年份"])  # 移除年份為 NaN 的行
        df["年份"] = df["年份"].astype(int)  # 確保年份是整數

        # 清理公司代號：轉為字串並去掉小數點
        df["公司代號"] = df["公司代號"].apply(
            lambda x: str(int(x)) if pd.notna(x) else None)

        # 清理股東資料欄位
        df["前10大股東持股情況"] = df["前10大股東持股情況"].apply(clean_value)

        # 去除重複資料：依年份和公司代號去重
        df = df.drop_duplicates(subset=["年份", "公司代號"])

        # 插入資料到資料庫
        for _, row in df.iterrows():
            # 檢查資料是否已存在
            if Shareholder.objects.filter(year=row["年份"], company_code=row["公司代號"]).exists():
                continue  # 如果資料已存在，跳過此行

            # 創建新記錄
            Shareholder.objects.create(
                market_type=row["市場別"],
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"],
                top_10_shareholders=row.get("前10大股東持股情況", None),
            )

        return JsonResponse({"success": "資料成功導入！"})

    except Exception as e:
        return JsonResponse({"error": f"處理檔案時發生錯誤：{str(e)}"}, status=500)


def upload_sustainability_report_data(request):
    # file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/2021-2023_report/report.xlsx"  # 替換為實際的檔案路徑
    file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "2021-2023_report", "report.xlsx"))

    try:
        # 讀取 Excel 檔案
        df = pd.read_excel(file_path, engine='openpyxl')

        # 檢查必要欄位是否存在
        required_columns = [
            "市場別", "年份", "公司代號", "公司名稱", "英文簡稱", "申報原因",
            "產業類別", "報告書內容涵蓋期間", "編製依循準則", "第三方驗證單位",
            "第三方採用標準", "會計師確信驗證單位", "會計師確信採用標準",
            "會計師確信意見類型", "永續報告書網址", "上傳日期", "修正後報告書上傳日期",
            "永續報告書英文版網址", "英文版上傳日期", "英文版修正後報告書上傳日期",
            "報告書聯絡資訊", "備註"
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
            "上傳日期", "修正後報告書上傳日期", "英文版上傳日期", "英文版修正後報告書上傳日期"
        ]:
            if column in df.columns:
                df[column] = pd.to_datetime(df[column], errors='coerce')

        # 去除重複項
        df = df.drop_duplicates(subset=["市場別", "年份", "公司代號", "公司名稱"])

        # 將資料寫入資料庫
        for _, row in df.iterrows():
            if SustainabilityReport.objects.filter(
                market_type=row["市場別"],
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"]
            ).exists():
                print(f"重複資料跳過：{row['年份']} - {row['公司代號']} - {row['公司名稱']}")
                continue

            SustainabilityReport.objects.create(
                market_type=row["市場別"],
                year=row["年份"],
                company_code=row["公司代號"],
                company_name=row["公司名稱"],
                english_abbreviation=row.get("英文簡稱", None),
                report_reason=row.get("申報原因", None),
                industry_type=row.get("產業類別", None),
                report_period=row.get("報告書內容涵蓋期間", None),
                compliance_guideline=row.get("編製依循準則", None),
                verification_unit=row.get("第三方驗證單位", None),
                verification_standard=row.get("第三方採用標準", None),
                cpa_assurance_unit=row.get("會計師確信驗證單位", None),
                cpa_assurance_standard=row.get("會計師確信採用標準", None),
                cpa_assurance_opinion=row.get("會計師確信意見類型", None),
                report_url=row.get("永續報告書網址", None),
                upload_date=row.get("上傳日期", None),
                revised_upload_date=row.get("修正後報告書上傳日期", None),
                english_report_url=row.get("永續報告書英文版網址", None),
                english_upload_date=row.get("英文版上傳日期", None),
                english_revised_upload_date=row.get("英文版修正後報告書上傳日期", None),
                contact_info=row.get("報告書聯絡資訊", None),
                remarks=row.get("備註", None)
            )

        return JsonResponse({"success": "資料成功導入！"})

    except Exception as e:
        return JsonResponse({"error": f"處理檔案時發生錯誤：{str(e)}"}, status=500)


def load_csv_to_database(request):
    # 絕對路徑：請替換成您的 CSV 文件的實際路徑
    # csv_file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/result/Water_risk.csv"
    csv_file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "result", "Water_risk.csv"))

    # 讀取 CSV 檔案
    try:
        data = pd.read_csv(csv_file_path)
    except Exception as e:
        return JsonResponse({"error": f"讀取 CSV 文件失敗: {e}"})

    # 將資料插入資料庫
    records_created = 0
    for _, row in data.iterrows():
        # 使用 get_or_create 來避免重複插入資料
        obj, created = WaterResourceRisk.objects.get_or_create(
            market_category=row["市場別"],
            report_year=row["報告年度"],
            company_id=row.get("公司代號", None),
            company_name=row.get("公司名稱", None),
            water_usage=row["用水量"],
            data_scope=row.get("資料範圍", None),
            water_intensity=row["用水密集度"],
            water_intensity_unit=row.get("用水密集度-單位", None),
            verification_status=row["驗證狀態"],
            network_centrality=row["網絡中心性"],
            greenwashing_label=row["漂綠標籤"],
            risk_level=row["風險等級"],
            anomaly_label=row["異常標籤"],
        )
        if created:
            records_created += 1

    return JsonResponse({"message": f"成功載入 {records_created} 筆資料到資料庫中！"})


def load_csv_to_database_energy(request):
    # 絕對路徑：請替換成您的 CSV 文件的實際路徑
    # csv_file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/result/energy_risk.csv"
    # 使用 os.path.abspath 將檔案路徑轉為絕對路徑
    csv_file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "result", "energy_risk.csv"))

    # 讀取 CSV 檔案
    try:
        data = pd.read_csv(csv_file_path)
    except Exception as e:
        return JsonResponse({"error": f"讀取 CSV 文件失敗: {e}"})

    # 將資料插入資料庫
    records_created = 0
    for _, row in data.iterrows():
        # 使用 get_or_create 來避免重複插入資料
        obj, created = EnergyResourceRisk.objects.get_or_create(
            market_category=row["市場別"],
            report_year=row["報告年度"],
            company_id=row.get("公司代號", None),
            company_name=row.get("公司名稱", None),
            renewable_energy_rate=row.get("再生能源使用率", None),
            data_scope=row.get("資料範圍", None),
            verification_status=row["驗證狀態"],
            network_centrality=row["網絡中心性"],
            greenwashing_label=row["漂綠標籤"],
            risk_level=row["風險等級"],
            anomaly_label=row["異常標籤"],
        )
        if created:
            records_created += 1

    return JsonResponse({"message": f"成功載入 {records_created} 筆資料到資料庫中！"})

    from django.shortcuts import render


def load_csv_to_database_waste(request):
    # 絕對路徑：請替換成您的 CSV 文件的實際路徑
    # csv_file_path = "/Users/lijialing/Desktop/DiscoverTheTruth/result/waste_risk.csv"
    # 使用 os.path.abspath 將檔案路徑轉為絕對路徑
    csv_file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "result", "waste_risk.csv"))

    # 檢查 CSV 檔案是否存在
    if not os.path.exists(csv_file_path):
        return JsonResponse({"error": f"檔案不存在: {csv_file_path}"})

    # 讀取 CSV 檔案
    try:
        data = pd.read_csv(csv_file_path)
    except Exception as e:
        return JsonResponse({"error": f"讀取 CSV 文件失敗: {e}"})

    # 將資料插入資料庫
    records_created = 0
    for _, row in data.iterrows():
        # 使用 get_or_create 來避免重複插入資料
        obj, created = WasteManagementRisk.objects.get_or_create(
            market_category=row["市場別"],
            report_year=row["報告年度"],
            company_id=row.get("公司代號", None),
            company_name=row.get("公司名稱", None),
            hazardous_waste_amount=row.get("有害廢棄物量", None),
            non_hazardous_waste_amount=row.get("非有害廢棄物量", None),
            total_waste_amount=row.get("廢棄物總量", None),
            data_scope=row.get("資料範圍", None),
            waste_intensity=row.get("廢棄物密集度", None),
            waste_intensity_unit=row.get("廢棄物密集度-單位", None),
            verification_status=row["驗證狀態"],
            network_centrality=row["網絡中心性"],
            greenwashing_label=row["漂綠標籤"],
            risk_level=row["風險等級"],
            anomaly_label=row["異常標籤"],
        )
        if created:
            records_created += 1

    return JsonResponse({"message": f"成功載入 {records_created} 筆資料到資料庫中！"})


def load_csv_to_database_green(request):
    # 使用 os.path.abspath 將檔案路徑轉為絕對路徑
    csv_file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "result", "green_risk.csv"))

    # 檢查 CSV 檔案是否存在
    if not os.path.exists(csv_file_path):
        return JsonResponse({"error": f"檔案不存在: {csv_file_path}"})

    # 讀取 CSV 檔案
    try:
        data = pd.read_csv(csv_file_path)
    except Exception as e:
        return JsonResponse({"error": f"讀取 CSV 文件失敗: {e}"})

    # 將資料插入資料庫
    records_created = 0
    for _, row in data.iterrows():
        try:
            # 使用 get_or_create 來避免重複插入資料
            obj, created = GreenRisk.objects.get_or_create(
                market_category=row["市場別"],
                report_year=row["年份"],
                company_id=row.get("公司代號", None),
                company_name=row.get("公司名稱", None),
                scope_1_emission=row.get("範疇一排放量", None),
                scope_1_data_boundary=row.get("範疇一-資料邊界", None),
                scope_1_verification=row.get("範疇一-取得驗證", None),
                scope_2_emission=row.get("範疇二排放量", None),
                scope_2_data_boundary=row.get("範疇二-資料邊界", None),
                scope_2_verification=row.get("範疇二-取得驗證", None),
                scope_3_emission=row.get("範疇三排放量", None),
                scope_3_data_boundary=row.get("範疇三-資料邊界", None),
                scope_3_verification=row.get("範疇三-取得驗證", None),
                emission_intensity=row.get("排放密集度", None),
                emission_intensity_unit=row.get("溫室氣體排放密集度-單位", None),
                network_centrality=row["網絡中心性"],
                greenwashing_label=row["漂綠標籤"],
                risk_level=row["風險等級"],
                anomaly_label=row["異常標籤"],
            )
            if created:
                records_created += 1
        except Exception as e:
            # 若某一行資料插入失敗，記錄下錯誤但不終止整個流程
            return JsonResponse({"error": f"資料插入失敗，錯誤訊息: {e}"})

    return JsonResponse({"message": f"成功載入 {records_created} 筆資料到資料庫中！"})


def load_csv_to_database_board(request):
    # 使用 os.path.abspath 將檔案路徑轉為絕對路徑
    csv_file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "result", "board_of_directors_risk.csv"))

    # 檢查 CSV 檔案是否存在
    if not os.path.exists(csv_file_path):
        return JsonResponse({"error": f"檔案不存在: {csv_file_path}"})

    # 讀取 CSV 檔案
    try:
        data = pd.read_csv(csv_file_path)
    except Exception as e:
        return JsonResponse({"error": f"讀取 CSV 文件失敗: {e}"})

    # 將資料插入資料庫
    records_created = 0
    for _, row in data.iterrows():
        try:
            # 使用 get_or_create 來避免重複插入資料
            obj, created = BoardOfDirectorsRisk.objects.get_or_create(
                market=row.get("市場別", None),
                year=row.get("年份", None),
                company_code=row.get("公司代號", None),
                defaults={  # 預設填充的字段
                    "company_name": row.get("公司名稱", None),
                    "total_seats": row.get("董事席次", None),
                    "independent_seats": row.get("獨立董事席次", None),
                    "female_seats": row.get("女性董事席次", None),
                    "female_ratio": row.get("女性董事比例", None),
                    "attendance_rate": row.get("董事會出席率", None),
                    "training_rate": row.get("董事進修比率", None),
                    "centrality": row.get("網絡中心性", None),
                    "risk_level": row.get("風險等級", None),
                    "anomaly_label": row.get("異常標籤", None),
                },
            )
            if created:
                records_created += 1
        except Exception as e:
            # 若某一行資料插入失敗，記錄下錯誤但不終止整個流程
            return JsonResponse({"error": f"資料插入失敗，錯誤訊息: {e}"})

    return JsonResponse({"message": f"成功載入 {records_created} 筆資料到資料庫中！"})


def load_csv_to_database_functiona(request):
    # 使用 os.path.abspath 將檔案路徑轉為絕對路徑
    csv_file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "result", "functional_committee_risk.csv"))

    # 檢查 CSV 檔案是否存在
    if not os.path.exists(csv_file_path):
        return JsonResponse({"error": f"檔案不存在: {csv_file_path}"}, status=400)

    # 讀取 CSV 檔案
    try:
        data = pd.read_csv(csv_file_path)
    except Exception as e:
        return JsonResponse({"error": f"讀取 CSV 文件失敗: {e}"}, status=500)

    # 將資料插入資料庫
    records_created = 0
    errors = []
    for index, row in data.iterrows():
        try:
            # 使用 get_or_create 來避免重複插入資料
            obj, created = Functiona_Committee_Risk.objects.get_or_create(
                company_code=row["公司代號"],  # 使用公司代號作為唯一標識
                report_year=row["報告年度"],  # 同一年份同公司
                defaults={  # 如果條件不滿足則更新以下字段
                    "market": row["市場別"],
                    "company_name": row["公司名稱"],
                    "compensation_committee_seats": int(row["薪酬委員會席次"]),
                    "compensation_committee_independent_seats": int(row["薪酬委員會獨立董事席次"]),
                    "compensation_committee_attendance_rate": float(row["薪酬委員會出席率"]),
                    "audit_committee_seats": int(row["審計委員會席次"]),
                    "audit_committee_attendance_rate": float(row["審計委員會出席率"]),
                    "network_centrality": float(row["網絡中心性"]),
                    "risk_level": row["風險等級"],
                    "anomaly_label": row["異常標籤"],
                },
            )
            if created:
                records_created += 1
        except Exception as e:
            # 若某一行資料插入失敗，記錄下錯誤但不終止整個流程
            errors.append({"row": index, "error": str(e)})

    # 返回結果
    return JsonResponse({
        "message": f"成功載入 {records_created} 筆資料到資料庫中！",
        "errors": errors,
    })


def load_csv_to_database_employee_safety(request):
    # 使用 os.path.abspath 將檔案路徑轉為絕對路徑
    csv_file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "result", "hr_develhr_develop_risk.csv"))

    # 檢查 CSV 檔案是否存在
    if not os.path.exists(csv_file_path):
        return JsonResponse({"error": f"檔案不存在: {csv_file_path}"})

    # 讀取 CSV 檔案
    try:
        data = pd.read_csv(csv_file_path)
    except Exception as e:
        return JsonResponse({"error": f"讀取 CSV 文件失敗: {e}"})

    # 將資料插入資料庫
    records_created = 0
    errors = []
    for index, row in data.iterrows():
        try:
            # 使用 get_or_create 來避免重複插入資料
            obj, created = Hr_Develop_Risk.objects.get_or_create(
                company_code=row["公司代號"],  # 使用公司代號作為唯一標識
                report_year=row["報告年度"],  # 同一年份同公司
                defaults={  # 如果條件不滿足則更新以下字段
                    "company_name": row["公司名稱"],
                    "employee_benefits_avg": row.get("員工福利平均數(仟元/人)(每年6/2起公開)", None),
                    "employee_salary_avg": row.get("員工薪資平均數(仟元/人)(每年6/2起公開)", None),
                    "non_supervisor_salary_avg": row.get("非擔任主管職務之全時員工薪資平均數(仟元/人)(每年7/1起公開)", None),
                    "non_supervisor_salary_median": row.get("非擔任主管職務之全時員工薪資中位數(仟元/人)(每年7/1起公開)", None),
                    "female_manager_ratio": row.get("管理職女性主管占比", None),
                    "occupational_hazards_count": row.get("職業災害人數", None),
                    "occupational_hazards_rate": row.get("職業災害人數及比率-比率", None),
                    "occupational_hazards_category": row.get("職業災害-類別", None),
                    "fire_count": row.get("火災-件數", None),
                    "fire_injuries_count": row.get("火災-死傷人數", None),
                    "fire_rate": row.get("火災-比率(死傷人數/員工總人數)", None),
                    "risk_level": row.get("風險等級", None),
                    "network_centrality": row.get("網絡中心性", None),
                    "anomaly_label": row.get("異常標籤", None),
                },
            )
            if created:
                records_created += 1
        except Exception as e:
            # 若某一行資料插入失敗，記錄下錯誤但不終止整個流程
            errors.append({"row": index, "error": str(e)})

    # 返回結果
    return JsonResponse({
        "message": f"成功載入 {records_created} 筆資料到資料庫中！",
        "errors": errors,
    })


def load_csv_to_database_investor_communication(request):
    # 使用 os.path.abspath 將檔案路徑轉為絕對路徑
    csv_file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "result", "investor_communication_risk.csv"))  # 假設檔案名稱為 "investor_communication_risk.csv"

    # 檢查 CSV 檔案是否存在
    if not os.path.exists(csv_file_path):
        return JsonResponse({"error": f"檔案不存在: {csv_file_path}"}, status=400)

    # 讀取 CSV 檔案
    try:
        data = pd.read_csv(csv_file_path)
    except Exception as e:
        return JsonResponse({"error": f"讀取 CSV 文件失敗: {e}"}, status=500)

    # 將資料插入資料庫
    records_created = 0
    errors = []
    for index, row in data.iterrows():
        try:
            # 使用 get_or_create 來避免重複插入資料
            obj, created = Investor_Communication_Risk.objects.get_or_create(
                company_code=row["公司代號"],  # 使用公司代號作為唯一標識
                report_year=row["報告年度"],  # 同一年份同公司
                defaults={  # 如果條件不滿足則更新以下字段
                    "company_name": row["公司名稱"],
                    "earnings_call_count": int(row.get("法說會次數", 0)),
                    "governance_area_link": row.get("治理專區連結", ""),
                    "network_centrality": float(row.get("網絡中心性", 0)),
                    "risk_level": row.get("風險等級", ""),
                    "anomaly_label": row.get("異常標籤", ""),
                },
            )
            if created:
                records_created += 1
        except Exception as e:
            # 若某一行資料插入失敗，記錄下錯誤但不終止整個流程
            errors.append({"row": index, "error": str(e)})

    # 返回結果
    return JsonResponse({
        "message": f"成功載入 {records_created} 筆資料到資料庫中！",
        "errors": errors,
    })


def load_csv_to_database_shareholder_risk(request):
    # 使用 os.path.abspath 將檔案路徑轉為絕對路徑
    csv_file_path = os.path.abspath(os.path.join(
        settings.BASE_DIR, "..", "result", "shareholding_and_control_risk.csv"))  # 假設檔案名稱為 "shareholder_risk.csv"

    # 檢查 CSV 檔案是否存在
    if not os.path.exists(csv_file_path):
        return JsonResponse({"error": f"檔案不存在: {csv_file_path}"}, status=400)

    # 讀取 CSV 檔案
    try:
        data = pd.read_csv(csv_file_path)
    except Exception as e:
        return JsonResponse({"error": f"讀取 CSV 文件失敗: {e}"}, status=500)

    # 將資料插入資料庫
    records_created = 0
    errors = []
    for index, row in data.iterrows():
        try:
            # 使用 get_or_create 來避免重複插入資料
            obj, created = ShareholderRisk.objects.get_or_create(
                company_code=row["公司代號"],  # 使用公司代號作為唯一標識
                report_year=row["報告年度"],  # 同一年份同公司
                defaults={  # 如果條件不滿足則更新以下字段
                    "company_name": row["公司名稱"],
                    "top_10_shareholders": row.get("前十大股東持股情況", ""),
                    "shareholding_concentration": float(row.get("持股集中度", 0)),
                    "network_centrality": float(row.get("網絡中心性", 0)),
                    "risk_level": row.get("風險等級", ""),
                    "anomaly_label": row.get("異常標籤", ""),
                },
            )
            if created:
                records_created += 1
        except Exception as e:
            # 若某一行資料插入失敗，記錄下錯誤但不終止整個流程
            errors.append({"row": index, "error": str(e)})

    # 返回結果
    return JsonResponse({
        "message": f"成功載入 {records_created} 筆資料到資料庫中！",
        "errors": errors,
    })
