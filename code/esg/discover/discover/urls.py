# from django.contrib import admin


# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("index", index),
# ]

from myapp.views import upload_water_resource_management_data, upload_waste_management_data, upload_energy_management_data, upload_greenhouse_gas_emission_data
from django.urls import path
import myapp.views as views
from django.contrib import admin
from myapp.views import ESGEachCompany
from myapp.views import upload_excel, upload_weather_management_data, upload_company_board_data, upload_function_committee_data, upload_employee_develop_data, upload_investor_communication_data, upload_shareholder_data

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name='index'),  # 首頁
    path('about/', views.about, name='about'),  # 關於
    path('chart/', views.chart, name='chart'),  # 圖表頁
    path('contact/', views.contact, name='contact'),  # 圖表頁
    path("esg_each_company/", ESGEachCompany,
         name="ESGEachCompany"),  # 每家公司 ESG 資訊
    path('esg-real/', views.ESGReal, name='esg_real'),  # 真實 ESG 資訊
    path('esg-risk/', views.ESGRisk, name='esg_risk'),  # ESG 風險
    path('forget/', views.forget, name='forget'),  # 忘記密碼
    path('login/', views.login, name='login'),  # 登入頁
    path('register/', views.register, name='register'),  # 註冊頁
    path('report/', views.report, name='report'),  # 報告頁
    path("upload_water_resource_management_data/", upload_water_resource_management_data,
         name="upload_water_resource_management_data"),
    path('upload_waste_management_data/', upload_waste_management_data,
         name='upload_waste_management_data'),
    path("upload_energy_management_data/", upload_energy_management_data,
         name="upload_energy_management_data"),
    path("upload-greenhouse-gas/", upload_greenhouse_gas_emission_data,
         name="upload_greenhouse_gas"),
    path('upload_excel/', upload_excel, name='upload_excel'),
    path('upload_weather_management_data/', upload_weather_management_data,
         name='upload_weather_management_data'),
    path('upload_company_board_data/', upload_company_board_data,
         name='upload_company_board_data'),
    path('upload_function_committee_data/', upload_function_committee_data,
         name='upload_function_committee_data'),
    path('upload_employee_develop_data/', upload_employee_develop_data,
         name='upload_employee_develop_data'),
    path('upload_investor_communication_data/', upload_investor_communication_data,
         name='upload_investor_communication_data'),
    path('upload_shareholder_data/', upload_shareholder_data,
         name='upload_shareholder_data'),
]
