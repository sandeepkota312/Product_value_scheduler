# Generated by Django 4.2.4 on 2023-08-10 12:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='URLs_Feed',
            fields=[
                ('url_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('Url', models.TextField()),
                ('product_name', models.TextField()),
                ('Original_price', models.IntegerField()),
                ('Current_price', models.IntegerField()),
                ('lowest_price', models.IntegerField()),
                ('users', models.ManyToManyField(default=None, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='userList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Urls', models.ManyToManyField(default=None, to='product_alerts.urls_feed')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
