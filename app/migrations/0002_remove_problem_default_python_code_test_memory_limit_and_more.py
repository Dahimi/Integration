# Generated by Django 4.0.5 on 2022-08-13 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='Default_Python_Code',
        ),
        migrations.AddField(
            model_name='test',
            name='Memory_Limit',
            field=models.FloatField(default='256'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='test',
            name='Time_Limit',
            field=models.FloatField(default='2'),
            preserve_default=False,
        ),
    ]
