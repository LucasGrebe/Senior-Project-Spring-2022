# Generated by Django 3.2.12 on 2022-03-06 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messager', '0008_auto_20220306_0118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='track_url',
        ),
        migrations.AddField(
            model_name='message',
            name='track_id',
            field=models.CharField(blank=True, default='', max_length=22),
        ),
    ]