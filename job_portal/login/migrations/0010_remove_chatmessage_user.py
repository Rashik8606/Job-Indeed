# Generated by Django 5.1.4 on 2024-12-21 21:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_alter_chatmessage_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessage',
            name='user',
        ),
    ]