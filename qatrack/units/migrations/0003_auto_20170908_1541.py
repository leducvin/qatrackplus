# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-09-08 19:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0002_029_to_030_first'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitavailabletime',
            name='hours_friday',
            field=models.DurationField(help_text='Duration of available time on Fridays'),
        ),
        migrations.AlterField(
            model_name='unitavailabletime',
            name='hours_monday',
            field=models.DurationField(help_text='Duration of available time on Mondays'),
        ),
        migrations.AlterField(
            model_name='unitavailabletime',
            name='hours_saturday',
            field=models.DurationField(help_text='Duration of available time on Saturdays'),
        ),
        migrations.AlterField(
            model_name='unitavailabletime',
            name='hours_sunday',
            field=models.DurationField(help_text='Duration of available time on Sundays'),
        ),
        migrations.AlterField(
            model_name='unitavailabletime',
            name='hours_thursday',
            field=models.DurationField(help_text='Duration of available time on Thursdays'),
        ),
        migrations.AlterField(
            model_name='unitavailabletime',
            name='hours_tuesday',
            field=models.DurationField(help_text='Duration of available time on Tuesdays'),
        ),
        migrations.AlterField(
            model_name='unitavailabletime',
            name='hours_wednesday',
            field=models.DurationField(help_text='Duration of available time on Wednesdays'),
        ),
    ]
