# Generated by Django 4.2.16 on 2024-12-03 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0017_companygovernance"),
    ]

    operations = [
        migrations.CreateModel(
            name="Shareholder",
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
                ("market_type", models.CharField(max_length=50, verbose_name="市場別")),
                ("year", models.PositiveIntegerField(verbose_name="年份")),
                (
                    "company_code",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="公司代號"
                    ),
                ),
                ("company_name", models.CharField(max_length=100, verbose_name="公司名稱")),
                (
                    "top_10_shareholders",
                    models.TextField(blank=True, null=True, verbose_name="前10大股東持股情況"),
                ),
            ],
            options={
                "verbose_name": "股東資料",
                "verbose_name_plural": "股東資料",
            },
        ),
    ]
