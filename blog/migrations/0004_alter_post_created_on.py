# Generated by Django 5.1.4 on 2025-01-07 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_post_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_on',
            field=models.DateTimeField(),
        ),
    ]
