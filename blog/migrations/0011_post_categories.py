# Generated by Django 5.1.4 on 2025-01-24 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_remove_post_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(related_name='posts', through='blog.Connection', to='blog.category'),
        ),
    ]
