# Generated by Django 3.2 on 2021-04-15 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0004_applicant_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='preliminaryform',
            name='sent',
            field=models.BooleanField(default=False),
        ),
    ]
