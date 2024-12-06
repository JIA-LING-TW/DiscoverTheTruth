from django.contrib import admin
from django.urls import path
import myapp.views as views
from myapp.views import (
    ESGEachCompany,
    upload_water_resource_management_data,
    upload_waste_management_data,
    upload_energy_management_data,
    upload_greenhouse_gas_emission_data,
    upload_weather_management_data,
    upload_company_board_data,
    upload_function_committee_data,
    upload_employee_develop_data,
    upload_investor_communication_data,
    upload_shareholder_data,
    upload_sustainability_report_data,
    load_csv_to_database_board
)

urlpatterns = [
    # 管理後台
    path("admin/", admin.site.urls),

    # 前台頁面
    path("", views.index, name="index"),                      # 首頁
    path("about/", views.about, name="about"),                # 關於
    path("chart/", views.chart, name="chart"),                # 圖表頁
    path("contact/", views.contact, name="contact"),          # 聯繫頁面
    path("login/", views.login, name="login"),                # 登入頁
    path("register/", views.register, name="register"),       # 註冊頁
    path("forget/", views.forget, name="forget"),             # 忘記密碼頁
    path("report/", views.report, name="report"),             # 報告頁

    # ESG 資訊
    path("esg_each_company/", ESGEachCompany,
         name="ESGEachCompany"),  # 每家公司 ESG 資訊
    path("esg-real/", views.ESGReal, name="esg_real"),                 # 真實 ESG 資訊
    path("esg-risk/", views.ESGRisk, name="esg_risk"),                 # ESG 風險頁

    # 資料上傳頁面
    path("upload_water_resource_management_data/", upload_water_resource_management_data,
         name="upload_water_resource_management_data"),
    path("upload_waste_management_data/", upload_waste_management_data,
         name="upload_waste_management_data"),
    path("upload_energy_management_data/", upload_energy_management_data,
         name="upload_energy_management_data"),
    path("upload-greenhouse-gas/", upload_greenhouse_gas_emission_data,
         name="upload_greenhouse_gas"),
    path("upload_weather_management_data/", upload_weather_management_data,
         name="upload_weather_management_data"),
    path("upload_company_board_data/", upload_company_board_data,
         name="upload_company_board_data"),
    path("upload_function_committee_data/", upload_function_committee_data,
         name="upload_function_committee_data"),
    path("upload_employee_develop_data/", upload_employee_develop_data,
         name="upload_employee_develop_data"),
    path("upload_investor_communication_data/", upload_investor_communication_data,
         name="upload_investor_communication_data"),
    path("upload_shareholder_data/", upload_shareholder_data,
         name="upload_shareholder_data"),
    path("upload_sustainability_report_data/", upload_sustainability_report_data,
         name="upload_sustainability_report_data"),
    path('load-data/', views.load_csv_to_database, name='load_data'),
    path('load-data_a/', views.load_csv_to_database_energy, name='load_data'),
    path('load-data_b/', views.load_csv_to_database_waste, name='load_data'),
    path('load-data_c/', views.load_csv_to_database_green, name='load_data'),
    path('load-data_e/', views.load_csv_to_database_board, name='load_data'),
    path('load-data_f/', views.load_csv_to_database_functiona, name='load_data'),
    path('load-data_g/', views.load_csv_to_database_employee_safety, name='load_data'),
    path('load-data_h/', views.load_csv_to_database_investor_communication,
         name='load_data'),
    path('load-data_i/', views.load_csv_to_database_shareholder_risk,
         name='load_data'),
    path('emissions-chart/', views.emissions_chart, name='emissions_chart'),
    path('energy-chart/', views.energy_chart, name='energy_chart'),
    path('water-usage-chart/', views.water_usage_chart, name='water_usage_chart'),
    path('waste-management-chart', views.waste_management_chart,
         name='waste_management_chart'),
    path('get-company-name/', views.get_company_name, name='get_company_name'),
]
