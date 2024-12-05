# Generated by Django 4.2.16 on 2024-12-04 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0027_wastemanagementrisk"),
    ]

    operations = [
        migrations.CreateModel(
            name="GreenRisk",
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
                (
                    "market_category",
                    models.CharField(max_length=10, verbose_name="市場別"),
                ),
                ("report_year", models.IntegerField(verbose_name="年份")),
                (
                    "company_id",
                    models.FloatField(blank=True, null=True, verbose_name="公司代號"),
                ),
                (
                    "company_name",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="公司名稱"
                    ),
                ),
                (
                    "scope_1_emission",
                    models.FloatField(blank=True, null=True, verbose_name="範疇一排放量"),
                ),
                (
                    "scope_1_data_boundary",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="範疇一-資料邊界"
                    ),
                ),
                (
                    "scope_1_verification",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="範疇一-取得驗證"
                    ),
                ),
                (
                    "scope_2_emission",
                    models.FloatField(blank=True, null=True, verbose_name="範疇二排放量"),
                ),
                (
                    "scope_2_data_boundary",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="範疇二-資料邊界"
                    ),
                ),
                (
                    "scope_2_verification",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="範疇二-取得驗證"
                    ),
                ),
                (
                    "scope_3_emission",
                    models.FloatField(blank=True, null=True, verbose_name="範疇三排放量"),
                ),
                (
                    "scope_3_data_boundary",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="範疇三-資料邊界"
                    ),
                ),
                (
                    "scope_3_verification",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="範疇三-取得驗證"
                    ),
                ),
                (
                    "emission_intensity",
                    models.FloatField(blank=True, null=True, verbose_name="排放密集度"),
                ),
                (
                    "emission_intensity_unit",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="溫室氣體排放密集度-單位",
                    ),
                ),
                ("network_centrality", models.FloatField(verbose_name="網絡中心性")),
                (
                    "greenwashing_label",
                    models.CharField(max_length=50, verbose_name="漂綠標籤"),
                ),
                ("risk_level", models.CharField(max_length=50, verbose_name="風險等級")),
                ("anomaly_label", models.CharField(max_length=50, verbose_name="異常標籤")),
            ],
            options={
                "verbose_name": "碳排放風險",
                "verbose_name_plural": "碳排放風險",
            },
        ),
    ]