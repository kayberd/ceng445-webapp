# Generated by Django 4.0.1 on 2022-01-20 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0002_event'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='isInstructor',
            new_name='is_instructor',
        ),
    ]
