# Generated by Django 4.0 on 2024-03-13 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0003_trainerprofile_trainer_bio_and_more'),
        ('gym_students', '0005_room_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='assigned_trainer',
            field=models.ManyToManyField(blank=True, to='trainer.TrainerProfile'),
        ),
    ]
