# Generated by Django 4.1.7 on 2023-03-14 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_user_role_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('1', 'Dean'), ('2', 'Vice'), ('3', 'Head'), ('4', 'Dr'), ('4', 'TA')], default=1, max_length=1),
            preserve_default=False,
        ),
    ]
