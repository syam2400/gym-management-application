# Generated by Django 4.0 on 2024-03-13 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_students', '0006_alter_studentprofile_assigned_trainer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='student_profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]
