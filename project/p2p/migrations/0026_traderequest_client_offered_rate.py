# Generated by Django 5.0.7 on 2025-05-02 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p2p', '0025_traderequest_message_alter_traderequest_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='traderequest',
            name='client_offered_rate',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True),
        ),
    ]
