# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-05 17:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import web_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='name')),
                ('email', models.EmailField(max_length=50, verbose_name='email')),
                ('phone', models.CharField(blank=True, max_length=15, verbose_name='phone number')),
                ('message', models.TextField(verbose_name='message')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
            ],
        ),
        migrations.AlterField(
            model_name='address',
            name='address_line',
            field=models.CharField(max_length=100, verbose_name='address line'),
        ),
        migrations.AlterField(
            model_name='address',
            name='county',
            field=models.CharField(max_length=50, verbose_name='county'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.Address'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='mobile',
            field=models.CharField(blank=True, max_length=15, verbose_name='mobile'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='telephone',
            field=models.CharField(blank=True, max_length=15, verbose_name='telephone'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.Address'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='goal',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True, verbose_name='goal'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', upload_to=web_app.models.get_organisation_logo_path),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='primary_contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.Contact'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='raised',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True, verbose_name='raised'),
        ),
        migrations.AlterField(
            model_name='organisationuser',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web_app.Contact', verbose_name='Contact details'),
        ),
        migrations.AlterField(
            model_name='organisationuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User account details'),
        ),
    ]
