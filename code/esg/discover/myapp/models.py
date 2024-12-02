from django.db import models


class WaterResourceManagement(models.Model):
    market_type = models.CharField(max_length=50, verbose_name="市場別")
    year = models.PositiveIntegerField(verbose_name="年份")
    company_code = models.CharField(
        max_length=20, verbose_name="公司代號", blank=True, null=True)
    company_name = models.CharField(max_length=100, verbose_name="公司名稱")
    water_usage = models.FloatField(
        verbose_name="用水量(公噸)", blank=True, null=True)
    data_scope = models.TextField(verbose_name="資料範圍", blank=True, null=True)
    water_intensity = models.FloatField(
        verbose_name="用水密集度(公噸/單位)", blank=True, null=True)
    water_intensity_unit = models.CharField(
        max_length=100, verbose_name="用水密集度-單位", blank=True, null=True)
    certification = models.CharField(
        max_length=255, verbose_name="取得驗證", blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} ({self.year})"

    class Meta:
        verbose_name = "水資源管理"
        verbose_name_plural = "水資源管理"


class WasteManagement(models.Model):
    market_type = models.CharField(max_length=50, verbose_name="市場別")
    year = models.PositiveIntegerField(verbose_name="年份")
    company_code = models.CharField(
        max_length=20, verbose_name="公司代號", blank=True, null=True)
    company_name = models.CharField(max_length=100, verbose_name="公司名稱")
    hazardous_waste = models.CharField(
        max_length=255, verbose_name="有害廢棄物量(公噸)", blank=True, null=True)
    non_hazardous_waste = models.CharField(
        max_length=255, verbose_name="非有害廢棄物量(公噸)", blank=True, null=True)
    total_weight = models.CharField(
        max_length=255, verbose_name="總重量(有害+非有害)(公噸)", blank=True, null=True)
    data_scope = models.TextField(verbose_name="資料範圍", blank=True, null=True)
    waste_intensity = models.CharField(
        max_length=255, verbose_name="廢棄物密集度(公噸/單位)", blank=True, null=True)
    waste_intensity_unit = models.CharField(
        max_length=100, verbose_name="廢棄物密集度-單位", blank=True, null=True)
    certification = models.CharField(
        max_length=255, verbose_name="取得驗證", blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} ({self.year})"

    class Meta:
        verbose_name = "廢棄物管理"
        verbose_name_plural = "廢棄物管理"


class EnergyManagement(models.Model):
    market_type = models.CharField(max_length=50, verbose_name="市場別")
    year = models.IntegerField(verbose_name="年份")
    company_code = models.CharField(max_length=20, verbose_name="公司代號")
    company_name = models.CharField(max_length=100, verbose_name="公司名稱")
    usage_rate = models.CharField(
        max_length=255, verbose_name="使用率(再生能源/總能源)", null=True, blank=True)
    data_scope = models.TextField(verbose_name="資料範圍", null=True, blank=True)
    certification = models.CharField(
        max_length=100, verbose_name="取得驗證", null=True, blank=True)

    def __str__(self):
        return f"{self.company_name} ({self.year})"

    class Meta:
        verbose_name = "能源管理"
        verbose_name_plural = "能源管理"
        unique_together = ("market_type", "year", "company_code")


class GreenhouseGasEmission(models.Model):
    market_type = models.CharField(max_length=10, verbose_name="市場別")
    year = models.PositiveIntegerField(verbose_name="年份")
    company_code = models.CharField(max_length=10, verbose_name="公司代號")
    company_name = models.CharField(max_length=100, verbose_name="公司名稱")

    scope_1_emissions = models.FloatField(
        verbose_name="範疇一-排放量(噸CO2e)", blank=True, null=True)
    scope_1_boundary = models.TextField(
        verbose_name="範疇一-資料邊界", blank=True, null=True)
    scope_1_verification = models.CharField(
        max_length=50, verbose_name="範疇一-取得驗證", blank=True, null=True)

    scope_2_emissions = models.FloatField(
        verbose_name="範疇二-排放量(噸CO2e)", blank=True, null=True)
    scope_2_boundary = models.TextField(
        verbose_name="範疇二-資料邊界", blank=True, null=True)
    scope_2_verification = models.CharField(
        max_length=50, verbose_name="範疇二-取得驗證", blank=True, null=True)

    scope_3_emissions = models.CharField(
        max_length=50, verbose_name="範疇三-排放量(噸CO2e)", blank=True, null=True)
    scope_3_boundary = models.TextField(
        verbose_name="範疇三-資料邊界", blank=True, null=True)
    scope_3_verification = models.CharField(
        max_length=50, verbose_name="範疇三-取得驗證", blank=True, null=True)

    emission_intensity = models.FloatField(
        verbose_name="溫室氣體排放密集度-密集度(噸CO2e/單位)", blank=True, null=True)
    intensity_unit = models.CharField(
        max_length=50, verbose_name="溫室氣體排放密集度-單位", blank=True, null=True)

    class Meta:
        verbose_name = "溫室氣體排放"
        verbose_name_plural = "溫室氣體排放"
        constraints = [
            models.UniqueConstraint(
                fields=['market_type', 'year', 'company_code'], name='unique_market_year_company')
        ]

    def __str__(self):
        return f"{self.company_name} ({self.year})"


class Report(models.Model):
    market_type = models.CharField(max_length=255)  # 市場別
    year = models.IntegerField()  # 年份
    company_code = models.IntegerField()  # 公司代號
    company_name = models.CharField(max_length=255)  # 公司名稱
    english_abbreviation = models.CharField(max_length=255)  # 英文簡稱
    declaration_reason = models.CharField(max_length=255)  # 申報原因
    industry_category = models.CharField(max_length=255)  # 產業類別
    report_period = models.CharField(max_length=255)  # 報告書內容涵蓋期間
    preparation_guidelines = models.CharField(max_length=255)  # 編製依循準則
    third_party_verification = models.CharField(
        max_length=255, null=True, blank=True)  # 第三方驗證單位
    upload_date = models.DateTimeField()  # 上傳日期
    revised_report = models.DateTimeField(null=True, blank=True)  # 修正後報告書
    revised_report_upload_date = models.DateTimeField(
        null=True, blank=True)  # 修正後報告書上傳日期
    english_report_url = models.CharField(
        max_length=255, null=True, blank=True)  # 永續報告書英文版網址
    english_report_file = models.DateTimeField(
        null=True, blank=True)  # 永續報告書英文版檔案
    english_report_upload_date = models.DateTimeField(
        null=True, blank=True)  # 英文版上傳日期
    revised_english_report = models.DateTimeField(
        null=True, blank=True)  # 英文版修正後報告書
    revised_english_report_upload_date = models.DateTimeField(
        null=True, blank=True)  # 英文版修正後報告書上傳日期
    report_contact_info = models.CharField(max_length=255)  # 報告書聯絡資訊
    remarks = models.CharField(max_length=255, null=True, blank=True)  # 備註

    created_at = models.DateTimeField(auto_now_add=True)  # 自動生成創建時間
    updated_at = models.DateTimeField(auto_now=True)  # 自動生成更新時間

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "永續報告書"
        verbose_name_plural = "永續報告書"
        unique_together = ("market_type", "year", "company_code")
