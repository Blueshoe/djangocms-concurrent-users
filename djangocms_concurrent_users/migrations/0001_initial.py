# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PageIndicator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('edited_on', models.DateTimeField()),
                ('started_editing', models.DateTimeField(null=True)),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('page', models.ForeignKey(to='cms.Page')),
            ],
        ),
    ]
