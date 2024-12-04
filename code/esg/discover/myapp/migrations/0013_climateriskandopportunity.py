# Generated by Django 4.2.16 on 2024-12-03 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0012_sustainabilityreport_delete_report"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClimateRiskAndOpportunity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("market_type", models.CharField(max_length=10, verbose_name="市場別")),
                ("year", models.PositiveIntegerField(verbose_name="年份")),
                ("company_code", models.CharField(max_length=10, verbose_name="公司代號")),
                ("company_name", models.CharField(max_length=100, verbose_name="公司名稱")),
                (
                    "board_and_management_supervision",
                    models.TextField(
                        blank=True, null=True, verbose_name="董事會與管理階層對於氣候相關風險與機會之監督及治理"
                    ),
                ),
                (
                    "impact_on_business_strategy_financials",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="辨識之氣候風險與機會如何影響企業之業務、策略及財務 (短期、中期、長期)",
                    ),
                ),
                (
                    "impact_of_extreme_weather_and_transformation_on_financials",
                    models.TextField(
                        blank=True, null=True, verbose_name="極端氣候事件及轉型行動對財務之影響"
                    ),
                ),
                (
                    "climate_risk_identification_and_management_process",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="氣候風險之辨識、評估及管理流程如何整合於整體風險管理制度",
                    ),
                ),
                (
                    "scenario_analysis_and_assumptions",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="若使用情境分析評估面對氣候變遷風險之韌性，應說明所使用之情境、參數、假設、分析因子及主要財務影響",
                    ),
                ),
                (
                    "transformation_plan_for_climate_risks",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="若有因應管理氣候相關風險之轉型計畫，說明該計畫內容，及用於辨識及管理實體風險及轉型風險之指標與目標",
                    ),
                ),
                (
                    "internal_carbon_pricing_basis",
                    models.TextField(
                        blank=True, null=True, verbose_name="若使用內部碳定價作為規劃工具，應說明價格制定基礎"
                    ),
                ),
                (
                    "climate_related_goals_and_progress",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="若有設定氣候相關目標，應說明所涵蓋之活動、溫室氣體排放範疇、規劃期程，每年達成進度等資訊；若使用碳抵換或再生能源憑證(RECs)以達成相關目標，應說明所抵換之減碳額度來源及數量或再生能源憑證(RECs)數量",
                    ),
                ),
            ],
            options={
                "verbose_name": "氣候風險與機會",
                "verbose_name_plural": "氣候風險與機會",
            },
        ),
    ]