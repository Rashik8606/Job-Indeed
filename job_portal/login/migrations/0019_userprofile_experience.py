# Generated by Django 5.1.4 on 2025-01-19 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0018_alter_jobvacancies_jobcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='experience',
            field=models.TextField(blank=True, null=True),
        ),
    ]