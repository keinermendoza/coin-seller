# Generated by Django 5.0.7 on 2025-04-17 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p2p', '0004_rename_opertarion_type_for_usdt_currencyexchangeconditions_operation_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fiatexchangepair',
            old_name='minimum_revenue_expected',
            new_name='minimum_margin_expected',
        ),
        migrations.AddField(
            model_name='fiatexchangepair',
            name='optimum_margin_expected',
            field=models.DecimalField(decimal_places=3, default=1, max_digits=8),
            preserve_default=False,
        ),
    ]
