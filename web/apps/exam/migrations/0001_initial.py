# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-24 05:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('division', '0001_initial'),
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssesmentWeight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accuracy', models.FloatField(default=0.0)),
                ('speed', models.FloatField(default=0.0)),
                ('technique', models.FloatField(default=0.0)),
                ('knowledge', models.FloatField(default=0.0)),
                ('physic', models.FloatField(default=0.0)),
                ('mental', models.FloatField(default=0.0)),
                ('level', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='division.Level')),
            ],
            options={
                'db_table': 'assesment_weight',
            },
        ),
        migrations.CreateModel(
            name='Levelling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('accuracy_point', models.FloatField(default=0.0)),
                ('speed_point', models.FloatField(default=0.0)),
                ('technique_point', models.FloatField(default=0.0)),
                ('knowledge_point', models.FloatField(default=0.0)),
                ('physic_point', models.FloatField(default=0.0)),
                ('mental_point', models.FloatField(default=0.0)),
            ],
            options={
                'db_table': 'levelling',
            },
        ),
        migrations.CreateModel(
            name='LevellingInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('location', models.CharField(max_length=255)),
                ('accuracy_weight', models.FloatField(default=0.0)),
                ('speed_weight', models.FloatField(default=0.0)),
                ('technique_weight', models.FloatField(default=0.0)),
                ('knowledge_weight', models.FloatField(default=0.0)),
                ('physic_weight', models.FloatField(default=0.0)),
                ('mental_weight', models.FloatField(default=0.0)),
                ('division', models.CharField(max_length=100)),
                ('level', models.CharField(max_length=100)),
                ('pass_score', models.FloatField(max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
                ('profile', models.ManyToManyField(related_name='lev_info', through='exam.Levelling', to='member.Profile')),
            ],
            options={
                'db_table': 'levelling_info',
            },
        ),
        migrations.AddField(
            model_name='levelling',
            name='lev_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='levellings', to='exam.LevellingInfo'),
        ),
        migrations.AddField(
            model_name='levelling',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='levellings', to='member.Profile'),
        ),
    ]
