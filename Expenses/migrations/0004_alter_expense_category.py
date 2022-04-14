# Generated by Django 3.2.4 on 2022-04-11 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Expenses', '0003_auto_20220411_0346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(choices=[('ONLINE_SERVICES', 'os'), ('TRAVEL', 'tr'), ('FOOD', 'foo'), ('RENT', 're'), ('OTHERS', 'oth')], max_length=255),
        ),
    ]