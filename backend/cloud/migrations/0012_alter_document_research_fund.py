# Generated by Django 3.2.23 on 2024-01-19 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0011_rename_abtract_document_abstract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='research_fund',
            field=models.IntegerField(null=True),
        ),
    ]