# Generated by Django 4.2.4 on 2023-08-27 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_alter_record_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='profile_pic',
            field=models.ImageField(blank=True, default='woman2.png', null=True, upload_to='images/'),
        ),
    ]
