# Generated by Django 5.0.1 on 2024-02-15 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='age',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='fitness_level',
            field=models.CharField(blank=True, choices=[('Beginner', 'Beginner'), ('Intemediate', 'Intemediate'), ('Advanced', 'Advanced')], max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='goal',
            field=models.CharField(blank=True, choices=[('LOSE', 'Weight lose'), ('FIT', 'Maintain weight'), ('GAIN', 'Weight gain')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='place',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='qualification',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
