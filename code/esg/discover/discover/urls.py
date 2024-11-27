# from django.contrib import admin


# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("index", index),
# ]

from django.urls import path
import myapp.views as views

urlpatterns = [
    path('', views.index, name='index'),  # 首頁
    path('about/', views.about, name='about'),  # 關於
    path('chart/', views.chart, name='chart'),  # 圖表頁
    path('esg-each-company/', views.ESGEachCompany,
         name='esg_each_company'),  # 每家公司 ESG 資訊
    path('esg-real/', views.ESGReal, name='esg_real'),  # 真實 ESG 資訊
    path('esg-risk/', views.ESGRisk, name='esg_risk'),  # ESG 風險
    path('forget/', views.forget, name='forget'),  # 忘記密碼
    path('login/', views.login, name='login'),  # 登入頁
    path('register/', views.register, name='register'),  # 註冊頁
    path('report/', views.report, name='report'),  # 報告頁
]
