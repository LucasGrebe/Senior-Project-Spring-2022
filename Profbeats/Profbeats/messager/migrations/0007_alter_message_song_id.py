# Generated by Django 3.2.12 on 2022-03-06 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messager', '0006_alter_message_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='song_id',
            field=models.CharField(blank=True, default='', max_length=22),
        ),
    ]