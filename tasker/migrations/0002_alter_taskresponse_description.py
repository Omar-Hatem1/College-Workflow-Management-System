# Generated by Django 4.2 on 2023-04-15 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskresponse',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]