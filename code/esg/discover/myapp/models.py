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


class SustainabilityReport(models.Model):
    market_type = models.CharField(max_length=50, verbose_name="市場別")
    year = models.PositiveIntegerField(verbose_name="年份")
    company_code = models.CharField(max_length=20, verbose_name="公司代號")
    company_name = models.CharField(max_length=100, verbose_name="公司名稱")
    company_abbreviation = models.CharField(
        max_length=100, verbose_name="英文簡稱", blank=True, null=True)
    declaration_reason = models.TextField(
        verbose_name="申報原因", blank=True, null=True)
    industry_category = models.CharField(max_length=100, verbose_name="產業類別")
    report_period = models.CharField(
        max_length=50, verbose_name="報告書內容涵蓋期間", blank=True, null=True)
    guidelines = models.TextField(verbose_name="編製依循準則", blank=True, null=True)
    third_party_verifier = models.CharField(
        max_length=100, verbose_name="第三方驗證單位", blank=True, null=True)
    upload_date = models.DateField(verbose_name="上傳日期", blank=True, null=True)
    revised_report = models.BooleanField(verbose_name="修正後報告書", default=False)
    revised_report_upload_date = models.DateField(
        verbose_name="修正後報告書上傳日期", blank=True, null=True)
    english_report_url = models.URLField(
        verbose_name="永續報告書英文版網址", blank=True, null=True)
    english_report_upload_date = models.DateField(
        verbose_name="英文版上傳日期", blank=True, null=True)
    english_revised_report = models.BooleanField(
        verbose_name="英文版修正後報告書", default=False)
    english_revised_report_upload_date = models.DateField(
        verbose_name="英文版修正後報告書上傳日期", blank=True, null=True)
    contact_info = models.TextField(
        verbose_name="報告書聯絡資訊", blank=True, null=True)
    remarks = models.TextField(verbose_name="備註", blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} ({self.year})"

    class Meta:
        verbose_name = "永續報告書"
        verbose_name_plural = "永續報告書"
        ordering = ['-year', 'company_name']


class ClimateRiskAndOpportunity(models.Model):
    market_type = models.CharField(max_length=10, verbose_name="市場別")
    year = models.PositiveIntegerField(verbose_name="年份")
    company_code = models.CharField(max_length=10, verbose_name="公司代號")
    company_name = models.CharField(max_length=100, verbose_name="公司名稱")

    # 5. 董事會與管理階層對於氣候相關風險與機會之監督及治理
    board_and_management_supervision = models.TextField(
        verbose_name="董事會與管理階層對於氣候相關風險與機會之監督及治理", blank=True, null=True)

    # 6. 辨識之氣候風險與機會如何影響企業之業務、策略及財務 (短期、中期、長期)
    impact_on_business_strategy_financials = models.TextField(
        verbose_name="辨識之氣候風險與機會如何影響企業之業務、策略及財務 (短期、中期、長期)", blank=True, null=True)

    # 7. 極端氣候事件及轉型行動對財務之影響
    impact_of_extreme_weather_and_transformation_on_financials = models.TextField(
        verbose_name="極端氣候事件及轉型行動對財務之影響", blank=True, null=True)

    # 8. 氣候風險之辨識、評估及管理流程如何整合於整體風險管理制度
    climate_risk_identification_and_management_process = models.TextField(
        verbose_name="氣候風險之辨識、評估及管理流程如何整合於整體風險管理制度", blank=True, null=True)

    # 9. 若使用情境分析評估面對氣候變遷風險之韌性，應說明所使用之情境、參數、假設、分析因子及主要財務影響
    scenario_analysis_and_assumptions = models.TextField(
        verbose_name="若使用情境分析評估面對氣候變遷風險之韌性，應說明所使用之情境、參數、假設、分析因子及主要財務影響", blank=True, null=True)

    # 10. 若有因應管理氣候相關風險之轉型計畫，說明該計畫內容，及用於辨識及管理實體風險及轉型風險之指標與目標
    transformation_plan_for_climate_risks = models.TextField(
        verbose_name="若有因應管理氣候相關風險之轉型計畫，說明該計畫內容，及用於辨識及管理實體風險及轉型風險之指標與目標", blank=True, null=True)

    # 11. 若使用內部碳定價作為規劃工具，應說明價格制定基礎
    internal_carbon_pricing_basis = models.TextField(
        verbose_name="若使用內部碳定價作為規劃工具，應說明價格制定基礎", blank=True, null=True)

    # 12. 若有設定氣候相關目標，應說明所涵蓋之活動、溫室氣體排放範疇、規劃期程，每年達成進度等資訊；若使用碳抵換或再生能源憑證(RECs)以達成相關目標，應說明所抵換之減碳額度來源及數量或再生能源憑證(RECs)數量
    climate_related_goals_and_progress = models.TextField(
        verbose_name="若有設定氣候相關目標，應說明所涵蓋之活動、溫室氣體排放範疇、規劃期程，每年達成進度等資訊；若使用碳抵換或再生能源憑證(RECs)以達成相關目標，應說明所抵換之減碳額度來源及數量或再生能源憑證(RECs)數量", blank=True, null=True)

    class Meta:
        verbose_name = "氣候風險與機會"
        verbose_name_plural = "氣候風險與機會"

    def __str__(self):
        return f"{self.company_name} ({self.year})"


class CompanyBoard(models.Model):
    market_type = models.CharField(max_length=10, verbose_name="市場別")
    year = models.PositiveIntegerField(verbose_name="年份")
    company_code = models.CharField(max_length=10, verbose_name="公司代號")
    company_name = models.CharField(max_length=100, verbose_name="公司名稱")

    # Board seats (including independent directors)
    board_seats_total = models.PositiveIntegerField(
        verbose_name="董事席次(含獨立董事)(席)", blank=True, null=True)

    # Independent board seats
    independent_board_seats = models.PositiveIntegerField(
        verbose_name="獨立董事席次(席)", blank=True, null=True)

    # Female board seats
    female_director_seats = models.PositiveIntegerField(
        verbose_name="女性董事席次及比率-席", blank=True, null=True)

    # Female board ratio
    female_director_ratio = models.FloatField(
        verbose_name="女性董事席次及比率-比率", blank=True, null=True)

    # Board attendance rate
    board_attendance_rate = models.FloatField(
        verbose_name="董事出席董事會出席率", blank=True, null=True)

    # Training hours compliance rate
    training_hours_compliance_rate = models.FloatField(
        verbose_name="董事進修時數符合進修要點比率", blank=True, null=True)

    class Meta:
        verbose_name = "公司董事會"
        verbose_name_plural = "公司董事會"

    def __str__(self):
        return f"{self.company_name} ({self.year})"
