# Generated by Django 3.2.12 on 2022-03-05 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messager', '0002_alter_message_song_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='song_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]