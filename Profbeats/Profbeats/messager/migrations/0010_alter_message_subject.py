# Generated by Django 3.2.12 on 2022-03-06 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messager', '0009_auto_20220306_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(blank=True, default='(no subject)', max_length=50),
        ),
    ]