# Generated by Django 4.1.3 on 2023-04-26 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniforum', '0002_post_thread'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='ip_address',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
