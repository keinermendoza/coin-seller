# Generated by Django 5.0.7 on 2025-07-01 15:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('p2p', '0028_switchmodel_destroy_old_currency_exchange_conditions'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=6, max_digits=10)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_default', models.BooleanField(default=False)),
                ('base_amount', models.DecimalField(decimal_places=6, max_digits=10)),
                ('target_amount', models.DecimalField(decimal_places=6, max_digits=10)),
                ('base_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_rates', to='p2p.currency')),
                ('target_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_rates', to='p2p.currency')),
            ],
        ),
        migrations.AddConstraint(
            model_name='simplerate',
            constraint=models.UniqueConstraint(fields=('base_currency', 'target_currency'), name='unique_currency_pair'),
        ),
    ]
