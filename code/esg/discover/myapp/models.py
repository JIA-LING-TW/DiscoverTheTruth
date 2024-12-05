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
        verbose_name = "氣候相關議題"
        verbose_name_plural = "氣候相關議題"

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
        verbose_name = "董事會"
        verbose_name_plural = "董事會"

    def __str__(self):
        return f"{self.company_name} ({self.year})"

# 功能性委員會


class CorporateGovernance(models.Model):
    market_type = models.CharField(max_length=50, verbose_name="市場別")
    year = models.PositiveIntegerField(verbose_name="年份")
    company_code = models.CharField(
        max_length=20, verbose_name="公司代號", blank=True, null=True)
    company_name = models.CharField(max_length=100, verbose_name="公司名稱")
    compensation_committee_seats = models.IntegerField(
        verbose_name="薪酬委員會席次", blank=True, null=True)
    independent_compensation_committee_seats = models.IntegerField(
        verbose_name="薪酬委員會獨立董事席次", blank=True, null=True)
    compensation_committee_attendance_rate = models.FloatField(
        verbose_name="薪酬委員會出席率", blank=True, null=True)
    audit_committee_seats = models.IntegerField(
        verbose_name="審計委員會席次", blank=True, null=True)
    audit_committee_attendance_rate = models.FloatField(
        verbose_name="審計委員會出席率", blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} ({self.year})"

    class Meta:
        verbose_name = "功能性委員會"
        verbose_name_plural = "功能性委員會"


class EmployeeDevelop(models.Model):
    market_type = models.CharField(max_length=50, verbose_name="市場別")
    year = models.PositiveIntegerField(verbose_name="年份")
    company_code = models.CharField(
        max_length=20, verbose_name="公司代號", blank=True, null=True)
    company_name = models.CharField(max_length=100, verbose_name="公司名稱")
    employee_benefits_avg = models.FloatField(
        verbose_name="員工福利平均數(仟元/人)(每年6/2起公開)", blank=True, null=True)
    employee_salary_avg = models.FloatField(
        verbose_name="員工薪資平均數(仟元/人)(每年6/2起公開)", blank=True, null=True)
    non_supervisor_salary_avg = models.FloatField(
        verbose_name="非擔任主管職務之全時員工薪資平均數(仟元/人)(每年7/1起公開)", blank=True, null=True)
    non_supervisor_salary_median = models.FloatField(
        verbose_name="非擔任主管職務之全時員工薪資中位數(仟元/人)(每年7/1起公開)", blank=True, null=True)
    female_manager_ratio = models.FloatField(
        verbose_name="管理職女性主管占比", blank=True, null=True)
    occupational_accident_count = models.IntegerField(
        verbose_name="職業災害人數及比率-人數", blank=True, null=True)
    occupational_accident_rate = models.FloatField(
        verbose_name="職業災害人數及比率-比率", blank=True, null=True)
    occupational_accident_category = models.CharField(
        max_length=255, verbose_name="職業災害-類別", blank=True, null=True)
    fire_incidents_count = models.IntegerField(
        verbose_name="火災-件數", blank=True, null=True)
    fire_incidents_injury_count = models.IntegerField(
        verbose_name="火災-死傷人數", blank=True, null=True)
    fire_incidents_rate = models.FloatField(
        verbose_name="火災-比率(死傷人數/員工總人數)", blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} ({self.year})"

    class Meta:
        verbose_name = "人力資源發展"
        verbose_name_plural = "人力資源發展"


# 投資人溝通
class CompanyGovernance(models.Model):
    market_type = models.CharField(max_length=50, verbose_name="市場別")
    year = models.PositiveIntegerField(verbose_name="年份")
    company_code = models.CharField(
        max_length=20, verbose_name="公司代號", blank=True, null=True)
    company_name = models.CharField(max_length=100, verbose_name="公司名稱")
    annual_conference_count = models.PositiveIntegerField(
        verbose_name="公司年度召開法說會次數(次)", blank=True, null=True
    )
    governance_link = models.URLField(
        verbose_name="利害關係人或公司治理專區連結", blank=True, null=True
    )

    def __str__(self):
        return f"{self.company_name} ({self.year})"

    class Meta:
        verbose_name = "投資人溝通"
        verbose_name_plural = "投資人溝通"


class Shareholder(models.Model):
    market_type = models.CharField(max_length=50, verbose_name="市場別")  # 市場別
    year = models.PositiveIntegerField(verbose_name="年份")  # 年份
    company_code = models.CharField(
        max_length=20, verbose_name="公司代號", blank=True, null=True
    )  # 公司代號
    company_name = models.CharField(
        max_length=100, verbose_name="公司名稱")  # 公司名稱
    top_10_shareholders = models.URLField(
        verbose_name="前10大股東持股情況", blank=True, null=True)  # 前10大股東持股情況

    def __str__(self):
        return f"{self.company_name} ({self.year})"  # 顯示公司名稱和年份

    class Meta:
        verbose_name = "持股及控制力"  # 顯示在管理介面中的名稱
        verbose_name_plural = "持股及控制力"  # 顯示在管理介面中的複數名稱


class SustainabilityReport(models.Model):
    market_type = models.CharField(max_length=50, verbose_name="市場別")  # 市場別
    year = models.PositiveIntegerField(verbose_name="年份")  # 年份
    company_code = models.CharField(
        max_length=20, verbose_name="公司代號", blank=True, null=True)  # 公司代號
    company_name = models.CharField(
        max_length=100, verbose_name="公司名稱")  # 公司名稱
    english_abbreviation = models.CharField(
        max_length=100, verbose_name="英文簡稱", blank=True, null=True)  # 英文簡稱
    report_reason = models.TextField(
        verbose_name="申報原因", blank=True, null=True)  # 申報原因
    industry_type = models.CharField(
        max_length=100, verbose_name="產業類別", blank=True, null=True)  # 產業類別
    report_period = models.CharField(
        max_length=100, verbose_name="報告書內容涵蓋期間", blank=True, null=True)  # 報告期間
    compliance_guideline = models.TextField(
        verbose_name="編製依循準則", blank=True, null=True)  # 編製準則
    verification_unit = models.CharField(
        max_length=100, verbose_name="第三方驗證單位", blank=True, null=True)  # 驗證單位
    verification_standard = models.CharField(
        max_length=200, verbose_name="第三方採用標準", blank=True, null=True)  # 第三方採用標準
    cpa_assurance_unit = models.CharField(
        max_length=100, verbose_name="會計師確信驗證單位", blank=True, null=True)  # 確信驗證單位
    cpa_assurance_standard = models.CharField(
        max_length=200, verbose_name="會計師確信採用標準", blank=True, null=True)  # 確信採用標準
    cpa_assurance_opinion = models.CharField(
        max_length=100, verbose_name="會計師確信意見類型", blank=True, null=True)  # 確信意見類型
    report_url = models.URLField(
        verbose_name="永續報告書網址", blank=True, null=True)  # 報告書網址
    upload_date = models.CharField(
        max_length=20, verbose_name="上傳日期", blank=True, null=True)  # 上傳日期
    revised_upload_date = models.CharField(
        max_length=20, verbose_name="修正後報告書上傳日期", blank=True, null=True)  # 修正後上傳日期
    english_report_url = models.URLField(
        verbose_name="永續報告書英文版網址", blank=True, null=True)  # 英文版網址
    english_upload_date = models.CharField(
        max_length=20, verbose_name="英文版上傳日期", blank=True, null=True)  # 英文版上傳日期
    english_revised_upload_date = models.CharField(
        max_length=20, verbose_name="英文版修正後報告書上傳日期", blank=True, null=True)  # 英文版修正後上傳日期
    contact_info = models.TextField(
        verbose_name="報告書聯絡資訊", blank=True, null=True)  # 聯絡資訊
    remarks = models.TextField(verbose_name="備註", blank=True, null=True)  # 備註

    def __str__(self):
        return f"{self.company_name} ({self.year})"  # 顯示公司名稱和年份

    class Meta:
        verbose_name = "永續報告書"  # 管理介面中的名稱
        verbose_name_plural = "永續報告書"  # 管理介面中的複數名稱


class WaterResourceRisk(models.Model):
    market_category = models.CharField(max_length=10, verbose_name="市場別")
    report_year = models.IntegerField(verbose_name="報告年度")
    company_id = models.FloatField(null=True, blank=True, verbose_name="公司代號")
    company_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="公司名稱")
    water_usage = models.FloatField(verbose_name="用水量")
    data_scope = models.TextField(null=True, blank=True, verbose_name="資料範圍")
    water_intensity = models.FloatField(verbose_name="用水密集度")
    water_intensity_unit = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="用水密集度-單位")
    verification_status = models.CharField(max_length=50, verbose_name="驗證狀態")
    network_centrality = models.FloatField(verbose_name="網絡中心性")
    greenwashing_label = models.CharField(max_length=50, verbose_name="漂綠標籤")
    risk_level = models.CharField(max_length=50, verbose_name="風險等級")
    anomaly_label = models.CharField(max_length=50, verbose_name="異常標籤")

    class Meta:
        verbose_name = "水資源管理風險"
        verbose_name_plural = "水資源管理風險"

    def __str__(self):
        return f"{self.market_category} - {self.company_name} ({self.report_year})"


class EnergyResourceRisk(models.Model):
    market_category = models.CharField(max_length=10, verbose_name="市場別")
    report_year = models.IntegerField(verbose_name="報告年度")
    company_id = models.FloatField(null=True, blank=True, verbose_name="公司代號")
    company_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="公司名稱")
    renewable_energy_rate = models.FloatField(
        null=True, blank=True, verbose_name="再生能源使用率")
    data_scope = models.TextField(null=True, blank=True, verbose_name="資料範圍")
    verification_status = models.CharField(max_length=50, verbose_name="驗證狀態")
    network_centrality = models.FloatField(verbose_name="網絡中心性")
    greenwashing_label = models.CharField(max_length=50, verbose_name="漂綠標籤")
    risk_level = models.CharField(max_length=50, verbose_name="風險等級")
    anomaly_label = models.CharField(max_length=50, verbose_name="異常標籤")

    class Meta:
        verbose_name = "能源管理風險"
        verbose_name_plural = "能源管理風險"

    def __str__(self):
        return f"{self.market_category} - {self.company_name} ({self.report_year})"


class WasteManagementRisk(models.Model):
    market_category = models.CharField(max_length=10, verbose_name="市場別")
    report_year = models.IntegerField(verbose_name="報告年度")
    company_id = models.FloatField(null=True, blank=True, verbose_name="公司代號")
    company_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="公司名稱")
    hazardous_waste_amount = models.FloatField(
        null=True, blank=True, verbose_name="有害廢棄物量")
    non_hazardous_waste_amount = models.FloatField(
        null=True, blank=True, verbose_name="非有害廢棄物量")
    total_waste_amount = models.FloatField(
        null=True, blank=True, verbose_name="廢棄物總量")
    data_scope = models.TextField(null=True, blank=True, verbose_name="資料範圍")
    waste_intensity = models.FloatField(
        null=True, blank=True, verbose_name="廢棄物密集度")
    waste_intensity_unit = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="廢棄物密集度-單位")
    verification_status = models.CharField(max_length=50, verbose_name="驗證狀態")
    network_centrality = models.FloatField(verbose_name="網絡中心性")
    greenwashing_label = models.CharField(max_length=50, verbose_name="漂綠標籤")
    risk_level = models.CharField(max_length=50, verbose_name="風險等級")
    anomaly_label = models.CharField(max_length=50, verbose_name="異常標籤")

    class Meta:
        verbose_name = "廢棄物管理風險"
        verbose_name_plural = "廢棄物管理風險"

    def __str__(self):
        return f"{self.market_category} - {self.company_name} ({self.report_year})"


class GreenRisk(models.Model):
    market_category = models.CharField(max_length=10, verbose_name="市場別")
    report_year = models.IntegerField(verbose_name="年份")
    company_id = models.FloatField(null=True, blank=True, verbose_name="公司代號")
    company_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="公司名稱")
    scope_1_emission = models.FloatField(
        null=True, blank=True, verbose_name="範疇一排放量")
    scope_1_data_boundary = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="範疇一-資料邊界")
    scope_1_verification = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="範疇一-取得驗證")
    scope_2_emission = models.FloatField(
        null=True, blank=True, verbose_name="範疇二排放量")
    scope_2_data_boundary = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="範疇二-資料邊界")
    scope_2_verification = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="範疇二-取得驗證")
    scope_3_emission = models.FloatField(
        null=True, blank=True, verbose_name="範疇三排放量")
    scope_3_data_boundary = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="範疇三-資料邊界")
    scope_3_verification = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="範疇三-取得驗證")
    emission_intensity = models.FloatField(
        null=True, blank=True, verbose_name="排放密集度")
    emission_intensity_unit = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="溫室氣體排放密集度-單位")
    network_centrality = models.FloatField(verbose_name="網絡中心性")
    greenwashing_label = models.CharField(max_length=50, verbose_name="漂綠標籤")
    risk_level = models.CharField(max_length=50, verbose_name="風險等級")
    anomaly_label = models.CharField(max_length=50, verbose_name="異常標籤")

    class Meta:
        verbose_name = "碳排放風險"
        verbose_name_plural = "碳排放風險"

    def __str__(self):
        return f"{self.market_category} - {self.company_name} ({self.report_year})"


class BoardOfDirectorsRisk(models.Model):
    market = models.CharField(max_length=50, verbose_name="市場別")
    report_year = models.IntegerField(verbose_name="年份")
    company_code = models.CharField(max_length=10, verbose_name="公司代號")
    company_name = models.CharField(max_length=100, verbose_name="公司名稱")
    total_seats = models.IntegerField(verbose_name="董事席次")
    independent_seats = models.IntegerField(verbose_name="獨立董事席次")
    female_seats = models.IntegerField(verbose_name="女性董事席次")
    female_ratio = models.FloatField(verbose_name="女性董事比例")
    attendance_rate = models.FloatField(verbose_name="董事會出席率")
    training_rate = models.FloatField(verbose_name="董事進修比率")
    centrality = models.FloatField(verbose_name="網絡中心性")
    risk_level = models.CharField(max_length=20, verbose_name="風險等級")
    anomaly_label = models.CharField(max_length=20, verbose_name="異常標籤")

    class Meta:
        verbose_name = "董事會風險資訊"
        verbose_name_plural = "董事會風險資訊"
        db_table = "board_of_directors_risk"

    def __str__(self):
        return f"{self.company_name} ({self.year})"


class Functiona_Committee_Risk(models.Model):
    market = models.CharField(max_length=50, verbose_name="市場別")
    report_year = models.IntegerField(verbose_name="報告年度")
    company_code = models.CharField(max_length=10, verbose_name="公司代號")
    company_name = models.CharField(max_length=100, verbose_name="公司名稱")
    compensation_committee_seats = models.IntegerField(verbose_name="薪酬委員會席次")
    compensation_committee_independent_seats = models.IntegerField(
        verbose_name="薪酬委員會獨立董事席次")
    compensation_committee_attendance_rate = models.FloatField(
        verbose_name="薪酬委員會出席率")
    audit_committee_seats = models.IntegerField(verbose_name="審計委員會席次")
    audit_committee_attendance_rate = models.FloatField(
        verbose_name="審計委員會出席率")
    network_centrality = models.FloatField(verbose_name="網絡中心性")
    risk_level = models.CharField(max_length=20, verbose_name="風險等級")
    anomaly_label = models.CharField(max_length=20, verbose_name="異常標籤")

    class Meta:
        verbose_name = "董事會風險資訊"
        verbose_name_plural = "董事會風險資訊"
        unique_together = ('company_code', 'report_year')  # 公司代號和報告年度應該是唯一組合

    def __str__(self):
        return f"{self.company_name} ({self.report_year})"


class Hr_Develop_Risk(models.Model):
    report_year = models.IntegerField(verbose_name="報告年度")
    company_code = models.CharField(max_length=10, verbose_name="公司代號")
    company_name = models.CharField(max_length=100, verbose_name="公司名稱")
    employee_benefits_avg = models.FloatField(
        verbose_name="員工福利平均數(仟元/人)(每年6/2起公開)")
    employee_salary_avg = models.FloatField(
        verbose_name="員工薪資平均數(仟元/人)(每年6/2起公開)")
    non_supervisor_salary_avg = models.FloatField(
        verbose_name="非擔任主管職務之全時員工薪資平均數(仟元/人)(每年7/1起公開)")
    non_supervisor_salary_median = models.FloatField(
        verbose_name="非擔任主管職務之全時員工薪資中位數(仟元/人)(每年7/1起公開)")
    female_manager_ratio = models.FloatField(verbose_name="管理職女性主管占比")
    occupational_hazards_count = models.IntegerField(verbose_name="職業災害人數")
    occupational_hazards_rate = models.FloatField(verbose_name="職業災害人數及比率-比率")
    occupational_hazards_category = models.CharField(
        max_length=100, verbose_name="職業災害-類別")
    fire_count = models.IntegerField(verbose_name="火災-件數")
    fire_injuries_count = models.IntegerField(verbose_name="火災-死傷人數")
    fire_rate = models.FloatField(verbose_name="火災-比率(死傷人數/員工總人數)")
    risk_level = models.CharField(max_length=20, verbose_name="風險等級")
    network_centrality = models.FloatField(verbose_name="網絡中心性")
    anomaly_label = models.CharField(max_length=20, verbose_name="異常標籤")

    class Meta:
        verbose_name = "員工與安全風險資訊"
        verbose_name_plural = "員工與安全風險資訊"
        unique_together = ('company_code', 'report_year')  # 公司代號和報告年度應該是唯一組合

    def __str__(self):
        return f"{self.company_name} ({self.report_year})"


class ShareholderRisk(models.Model):
    market_category = models.CharField(max_length=50, verbose_name="市場別")
    report_year = models.IntegerField(verbose_name="報告年度")
    company_code = models.CharField(max_length=10, verbose_name="公司代號")
    company_name = models.CharField(max_length=100, verbose_name="公司名稱")
    top_10_shareholders = models.TextField(
        verbose_name="前十大股東持股情況")  # 假設這是文字形式描述
    shareholding_concentration = models.FloatField(verbose_name="持股集中度")
    network_centrality = models.FloatField(verbose_name="網絡中心性")
    risk_level = models.CharField(max_length=20, verbose_name="風險等級")
    anomaly_label = models.CharField(max_length=20, verbose_name="異常標籤")

    class Meta:
        verbose_name = "股東風險資訊"
        verbose_name_plural = "股東風險資訊"
        unique_together = ('company_code', 'report_year')  # 公司代號和報告年度應該是唯一組合

    def __str__(self):
        return f"{self.company_name} ({self.report_year})"


class Investor_Communication_Risk(models.Model):
    market = models.CharField(max_length=50, verbose_name="市場別")
    report_year = models.IntegerField(verbose_name="報告年度")
    company_code = models.CharField(max_length=10, verbose_name="公司代號")
    company_name = models.CharField(max_length=100, verbose_name="公司名稱")
    earnings_call_count = models.IntegerField(verbose_name="法說會次數")
    governance_area_link = models.URLField(verbose_name="治理專區連結")
    network_centrality = models.FloatField(verbose_name="網絡中心性")
    risk_level = models.CharField(max_length=20, verbose_name="風險等級")
    anomaly_label = models.CharField(max_length=20, verbose_name="異常標籤")

    class Meta:
        verbose_name = "公司治理風險資訊"
        verbose_name_plural = "公司治理風險資訊"
        unique_together = ('company_code', 'report_year')  # 公司代號和報告年度應該是唯一組合

    def __str__(self):
        return f"{self.company_name} ({self.report_year})"
