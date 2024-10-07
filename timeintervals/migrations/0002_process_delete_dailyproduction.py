# Generated by Django 5.0.3 on 2024-09-25 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeintervals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('project_name', models.CharField(max_length=100)),
                ('process_name', models.CharField(max_length=255)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='DailyProduction',
        ),
    ]