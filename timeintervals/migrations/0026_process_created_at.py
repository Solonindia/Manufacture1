# Generated by Django 5.0.3 on 2024-09-27 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeintervals', '0025_alter_processinterval_end_info_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]