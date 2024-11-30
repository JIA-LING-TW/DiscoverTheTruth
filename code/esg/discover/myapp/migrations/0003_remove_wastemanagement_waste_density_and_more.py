# Generated by Django 4.2.16 on 2024-11-30 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0002_alter_waterresourcemanagement_water_usage"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="wastemanagement",
            name="waste_density",
        ),
        migrations.RemoveField(
            model_name="wastemanagement",
            name="waste_density_unit",
        ),
        migrations.AddField(
            model_name="wastemanagement",
            name="market_type",
            field=models.CharField(
                default="default_value_here", max_length=50, verbose_name="市場別"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="wastemanagement",
            name="waste_intensity",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="廢棄物密集度(公噸/單位)"
            ),
        ),
        migrations.AddField(
            model_name="wastemanagement",
            name="waste_intensity_unit",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="廢棄物密集度-單位"
            ),
        ),
        migrations.AlterField(
            model_name="wastemanagement",
            name="company_code",
            field=models.CharField(
                blank=True, max_length=20, null=True, verbose_name="公司代號"
            ),
        ),
        migrations.AlterField(
            model_name="wastemanagement",
            name="company_name",
            field=models.CharField(max_length=100, verbose_name="公司名稱"),
        ),
        migrations.AlterField(
            model_name="wastemanagement",
            name="year",
            field=models.PositiveIntegerField(verbose_name="年份"),
        ),
        migrations.AlterUniqueTogether(
            name="waterresourcemanagement",
            unique_together={("year", "company_code")},
        ),
    ]