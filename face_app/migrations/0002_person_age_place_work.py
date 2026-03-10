# Migration to add age, place, and work fields to Person model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='age',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='place',
            field=models.CharField(max_length=255, null=True, blank=True, help_text='Location/City'),
        ),
        migrations.AddField(
            model_name='person',
            name='work',
            field=models.CharField(max_length=255, null=True, blank=True, help_text='Job title or occupation'),
        ),
    ]
