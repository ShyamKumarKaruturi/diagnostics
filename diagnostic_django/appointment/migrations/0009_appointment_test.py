# Generated by Django 4.1.1 on 2022-09-28 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0008_remove_appointment_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='test',
            field=models.ManyToManyField(blank=True, null=True, to='appointment.test'),
        ),
    ]
