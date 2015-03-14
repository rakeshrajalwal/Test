# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignForGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('groupID', models.IntegerField()),
                ('startDate', models.DateField()),
            ],
            options={
                'db_table': 'campaignforgroup',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Campaigns',
            fields=[
                ('campaignID', models.AutoField(serialize=False, primary_key=True)),
                ('campaignName', models.CharField(max_length=200)),
                ('timeStamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'campaigns',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomerGroup',
            fields=[
                ('groupID', models.AutoField(serialize=False, primary_key=True)),
                ('groupName', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200, null=True, blank=True)),
                ('country', models.CharField(max_length=200, null=True, blank=True)),
                ('salesRepEmployeeNumber', models.CharField(max_length=200, null=True, blank=True)),
                ('creditLimit', models.DecimalField(null=True, max_digits=32, decimal_places=8, blank=True)),
                ('timeStamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'customergroup',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('customer_id', models.TextField(verbose_name=b'customer id')),
                ('group_id', models.ForeignKey(to='classic_models.CustomerGroup')),
            ],
            options={
                'db_table': 'grouplist',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='campaignforgroup',
            name='campaignID',
            field=models.ForeignKey(to='classic_models.Campaigns'),
            preserve_default=True,
        ),
    ]
