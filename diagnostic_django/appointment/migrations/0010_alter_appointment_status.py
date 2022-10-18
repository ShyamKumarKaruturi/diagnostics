# Generated by Django 4.1.1 on 2022-10-14 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0009_alter_branch_branch_id_alter_lab_lab_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('completed', 'completed'), ('approved', 'approved'), ('rejected', 'rejected'), ('pending', 'pending')], default='pending', max_length=100),
        ),
    ]