# Generated by Django 4.0 on 2021-12-17 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminology', '0006_alter_guideversion_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guideversion',
            name='version',
            field=models.CharField(max_length=100),
        ),
        migrations.AddConstraint(
            model_name='guideversion',
            constraint=models.CheckConstraint(check=models.Q(('version', ''), _negated=True), name='non_empty_version'),
        ),
    ]