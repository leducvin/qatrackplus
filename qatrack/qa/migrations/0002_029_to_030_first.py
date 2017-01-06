# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-07 15:55
from __future__ import unicode_literals

import re

from django.core.validators import RegexValidator
from django.db import migrations, models
import django.utils.timezone

script_regex = re.compile(r'(<script[\sa-zA-Z0-9"\';-_=/]*>([\s\S]+?)</script>)')


def migrate_script_tags_to_javascript(apps, schema_editor):

    TestList = apps.get_model('qa', 'TestList')
    TestListCycle = apps.get_model('qa', 'TestListCycle')

    for tl in TestList.objects.all():

        if tl.description and script_regex.search(tl.description) is not None:
            js = script_regex.search(tl.description).groups(0)[1]
            js_tags = script_regex.search(tl.description).groups(0)[0]
            tl.javascript = js
            tl.description = tl.description.replace(js_tags, '')
            tl.save()

    for tlc in TestListCycle.objects.all():

        if tlc.description and script_regex.search(tlc.description) is not None:
            js = script_regex.search(tlc.description).groups(0)[1]
            js_tags = script_regex.search(tlc.description).groups(0)[0]
            tlc.javascript = js
            tlc.description = tlc.description.replace(js_tags, '')
            tlc.save()


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autoreviewrule',
            name='pass_fail',
            field=models.CharField(choices=[('not_done', 'Not Done'), ('ok', 'OK'), ('tolerance', 'Tolerance'), ('action', 'Action'), ('no_tol', 'No Tol Set')], max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='reference',
            name='type',
            field=models.CharField(choices=[('numerical', 'Numerical'), ('boolean', 'Yes / No')], default='numerical', max_length=15),
        ),
        migrations.AlterField(
            model_name='test',
            name='chart_visibility',
            field=models.BooleanField(default=True, verbose_name='Test item visible in charts?'),
        ),
        migrations.AlterField(
            model_name='test',
            name='display_image',
            field=models.BooleanField(default=False, help_text='Image uploads only: Show uploaded images under the testlist', verbose_name='Display image'),
        ),
        migrations.AlterField(
            model_name='test',
            name='slug',
            field=models.SlugField(help_text='A short variable name consisting of alphanumeric characters and underscores for this test (to be used in composite calculations). ', max_length=128, verbose_name='Macro name'),
        ),
        migrations.AlterField(
            model_name='test',
            name='type',
            field=models.CharField(choices=[('boolean', 'Boolean'), ('simple', 'Simple Numerical'), ('multchoice', 'Multiple Choice'), ('constant', 'Constant'), ('composite', 'Composite'), ('string', 'String'), ('scomposite', 'String Composite'), ('upload', 'File Upload')], default='simple', help_text='Indicate if this test is a Boolean,Simple Numerical,Multiple Choice,Constant,Composite,String,String Composite,File Upload', max_length=10),
        ),
        migrations.AlterField(
            model_name='testinstance',
            name='pass_fail',
            field=models.CharField(choices=[('not_done', 'Not Done'), ('ok', 'OK'), ('tolerance', 'Tolerance'), ('action', 'Action'), ('no_tol', 'No Tol Set')], db_index=True, editable=False, max_length=20),
        ),
        migrations.AlterField(
            model_name='testinstance',
            name='work_completed',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, help_text='Format DD-MM-YY hh:mm (hh:mm is 24h time e.g. 31-05-12 14:30)'),
        ),
        migrations.AlterField(
            model_name='testlist',
            name='warning_message',
            field=models.CharField(default='Do not treat', help_text='Message given when a test value is out of tolerance', max_length=255),
        ),
        migrations.AlterField(
            model_name='testlistcycle',
            name='day_option_text',
            field=models.CharField(choices=[('day', 'Day'), ('tlname', 'Test List Name')], default='day', max_length=8),
        ),
        migrations.AlterField(
            model_name='testlistcycle',
            name='drop_down_label',
            field=models.CharField(default='Choose Day', max_length=128),
        ),
        migrations.AlterField(
            model_name='tolerance',
            name='type',
            field=models.CharField(choices=[('absolute', 'Absolute'), ('percent', 'Percentage'), ('multchoice', 'Multiple Choice')], help_text='Select whether this will be an absolute or relative tolerance criteria', max_length=20),
        ),
        migrations.AddField(
            model_name='testinstancestatus',
            name='colour',
            field=models.CharField(default='rgba(60,141,188,1)', max_length=22, validators=[RegexValidator(re.compile('^rgba\\(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]),(0(\\.[0-9][0-9]?)?|1)\\)$', 32), 'Enter a valid color.', 'invalid')]),
        ),
        migrations.AddField(
            model_name='testlist',
            name='javascript',
            field=models.TextField(blank=True, help_text='Any extra javascript to run when loading perform page', null=True),
        ),
        migrations.AddField(
            model_name='testlistcycle',
            name='javascript',
            field=models.TextField(blank=True, help_text='Any extra javascript to run when loading perform page', null=True),
        ),
        migrations.RunPython(migrate_script_tags_to_javascript),
    ]
