# Generated by Django 5.1.5 on 2025-02-07 23:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myShop', '0004_product_breite_product_farbe_product_höhe_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vorname', models.CharField(max_length=50)),
                ('nachname', models.CharField(max_length=50)),
                ('adresse', models.CharField(max_length=50)),
                ('plz', models.IntegerField()),
                ('ort', models.CharField(max_length=50)),
                ('agb', models.BooleanField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
