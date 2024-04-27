# Generated by Django 5.0.4 on 2024-04-27 21:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_merge_0005_product_0005_provider'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.pet')),
                ('vet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.vet')),
            ],
        ),
    ]
