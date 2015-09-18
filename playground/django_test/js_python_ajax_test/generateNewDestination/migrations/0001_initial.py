# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('create_time', models.DateTimeField(verbose_name=b'creation time')),
            ],
        ),
        migrations.CreateModel(
            name='PreviousLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lat', models.DecimalField(max_digits=20, decimal_places=10)),
                ('lng', models.DecimalField(max_digits=20, decimal_places=10)),
                ('person', models.ForeignKey(to='generateNewDestination.Person')),
            ],
        ),
    ]
