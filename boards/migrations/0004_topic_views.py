# Generated by Django 2.2.16 on 2021-02-17 10:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('boards', '0003_auto_20210217_0858'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]