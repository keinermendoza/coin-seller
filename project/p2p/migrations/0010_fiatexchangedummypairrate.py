# Generated by Django 5.0.7 on 2025-04-17 20:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p2p', '0009_fiatexchangepair_maximum_margin_limit'),
    ]

    operations = [
        migrations.CreateModel(
            name='FiatExchangeDummyPairRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('rate', models.DecimalField(decimal_places=3, max_digits=10)),
                ('fiat_exchange_pair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dummy_rates', to='p2p.fiatexchangepair')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
