# Generated by Django 5.1.7 on 2025-03-20 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uat', '0002_teststep_attachment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teststep',
            name='attachment',
        ),
    ]
