# Generated by Django 5.0.3 on 2024-09-25 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeintervals', '0006_remove_process_end_info_remove_process_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='end_info',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='process',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='process',
            name='start_info',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='process',
            name='start_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='process',
            name='main_process',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='process',
            name='sub_process',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='TimeInterval',
        ),
    ]
