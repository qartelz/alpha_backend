# Generated by Django 5.1 on 2024-08-10 10:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opstmt', '0002_rename_cpmpany_year_company_alter_year_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='year',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='years', to='opstmt.company'),
        ),
    ]
