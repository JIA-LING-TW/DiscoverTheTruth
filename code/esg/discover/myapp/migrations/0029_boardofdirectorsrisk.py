# Generated by Django 4.2.16 on 2024-12-05 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0028_greenrisk"),
    ]

    operations = [
        migrations.CreateModel(
            name="BoardOfDirectorsRisk",
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
                ("market", models.CharField(max_length=50, verbose_name="市場別")),
                ("year", models.IntegerField(verbose_name="年份")),
                (
                    "company_code",
                    models.CharField(max_length=10, verbose_name="公司代號"),
                ),
                (
                    "company_name",
                    models.CharField(max_length=100, verbose_name="公司名稱"),
                ),
                ("total_seats", models.IntegerField(verbose_name="董事席次")),
                ("independent_seats", models.IntegerField(verbose_name="獨立董事席次")),
                ("female_seats", models.IntegerField(verbose_name="女性董事席次")),
                ("female_ratio", models.FloatField(verbose_name="女性董事比例")),
                ("attendance_rate", models.FloatField(verbose_name="董事會出席率")),
                ("training_rate", models.FloatField(verbose_name="董事進修比率")),
                ("centrality", models.FloatField(verbose_name="網絡中心性")),
                (
                    "risk_level",
                    models.CharField(max_length=20, verbose_name="風險等級"),
                ),
                (
                    "anomaly_label",
                    models.CharField(max_length=20, verbose_name="異常標籤"),
                ),
            ],
            options={
                "verbose_name": "董事會風險資訊",
                "verbose_name_plural": "董事會風險資訊",
                "db_table": "board_of_directors_risk",
            },
        ),
    ]