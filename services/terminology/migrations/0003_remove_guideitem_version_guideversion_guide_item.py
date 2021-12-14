# Generated by Django 4.0 on 2021-12-13 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminology', '0002_alter_guideversion_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guideitem',
            name='version',
        ),
        migrations.AddField(
            model_name='guideversion',
            name='guide_item',
            field=models.ManyToManyField(to='terminology.GuideItem'),
        ),
    ]