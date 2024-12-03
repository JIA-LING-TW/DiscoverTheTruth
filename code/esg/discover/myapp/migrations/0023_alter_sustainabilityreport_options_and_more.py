# Generated by Django 4.2.16 on 2024-12-03 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0022_alter_shareholder_top_10_shareholders"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sustainabilityreport",
            options={"verbose_name": "永續報告書", "verbose_name_plural": "永續報告書"},
        ),
        migrations.RenameField(
            model_name="sustainabilityreport",
            old_name="guidelines",
            new_name="compliance_guideline",
        ),
        migrations.RenameField(
            model_name="sustainabilityreport",
            old_name="company_abbreviation",
            new_name="english_abbreviation",
        ),
        migrations.RenameField(
            model_name="sustainabilityreport",
            old_name="english_revised_report_upload_date",
            new_name="english_revised_upload_date",
        ),
        migrations.RenameField(
            model_name="sustainabilityreport",
            old_name="english_report_upload_date",
            new_name="english_upload_date",
        ),
        migrations.RenameField(
            model_name="sustainabilityreport",
            old_name="declaration_reason",
            new_name="report_reason",
        ),
        migrations.RenameField(
            model_name="sustainabilityreport",
            old_name="revised_report_upload_date",
            new_name="revised_upload_date",
        ),
        migrations.RenameField(
            model_name="sustainabilityreport",
            old_name="third_party_verifier",
            new_name="verification_unit",
        ),
        migrations.RemoveField(
            model_name="sustainabilityreport",
            name="english_revised_report",
        ),
        migrations.RemoveField(
            model_name="sustainabilityreport",
            name="industry_category",
        ),
        migrations.RemoveField(
            model_name="sustainabilityreport",
            name="revised_report",
        ),
        migrations.AddField(
            model_name="sustainabilityreport",
            name="cpa_assurance_opinion",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="會計師確信意見類型"
            ),
        ),
        migrations.AddField(
            model_name="sustainabilityreport",
            name="cpa_assurance_standard",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="會計師確信採用標準"
            ),
        ),
        migrations.AddField(
            model_name="sustainabilityreport",
            name="cpa_assurance_unit",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="會計師確信驗證單位"
            ),
        ),
        migrations.AddField(
            model_name="sustainabilityreport",
            name="industry_type",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="產業類別"
            ),
        ),
        migrations.AddField(
            model_name="sustainabilityreport",
            name="report_url",
            field=models.URLField(blank=True, null=True, verbose_name="永續報告書網址"),
        ),
        migrations.AddField(
            model_name="sustainabilityreport",
            name="verification_standard",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="第三方採用標準"
            ),
        ),
        migrations.AlterField(
            model_name="sustainabilityreport",
            name="company_code",
            field=models.CharField(
                blank=True, max_length=20, null=True, verbose_name="公司代號"
            ),
        ),
        migrations.AlterField(
            model_name="sustainabilityreport",
            name="report_period",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="報告書內容涵蓋期間"
            ),
        ),
    ]
