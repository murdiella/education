# Generated by Django 3.2 on 2021-04-21 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0005_preliminaryform_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='ref',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
