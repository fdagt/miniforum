# Generated by Django 4.1.3 on 2023-04-26 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('miniforum', '0005_alter_post_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.CharField(max_length=100)),
                ('dealt_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('content', models.CharField(max_length=1000)),
                ('thread', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='miniforum.thread')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
