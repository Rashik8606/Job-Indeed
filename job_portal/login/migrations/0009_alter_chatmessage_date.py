# Generated by Django 5.1.4 on 2024-12-21 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]