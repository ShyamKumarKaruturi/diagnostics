# Generated by Django 4.1.1 on 2022-10-02 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0014_appointment_tests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='tests',
            field=models.ManyToManyField(blank=True, null=True, related_name='tests', to='appointment.test'),
        ),
    ]
