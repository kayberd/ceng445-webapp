# Generated by Django 4.0.1 on 2022-01-20 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0003_rename_isinstructor_person_is_instructor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.room'),
        ),
    ]
