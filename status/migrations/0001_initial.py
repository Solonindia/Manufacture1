# Generated by Django 5.0.3 on 2024-09-30 06:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_process', models.CharField(max_length=100, null=True)),
                ('sub_process', models.CharField(max_length=100, null=True)),
                ('additional_info', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProcessInterval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(null=True)),
                ('end_time', models.TimeField(null=True)),
                ('startend_time', models.TimeField(null=True)),
                ('start_info', models.CharField(blank=True, max_length=100)),
                ('end_info', models.CharField(blank=True, max_length=100)),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intervals', to='status.process')),
            ],
        ),
    ]