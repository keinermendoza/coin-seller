# Generated by Django 5.0.7 on 2025-04-26 14:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p2p', '0022_exchange_traderequest'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFiatPreferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('side_operation', models.CharField(choices=[('B', 'Buy'), ('S', 'Sell')], default='B', max_length=1)),
                ('pair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_fiat_preferences', to='p2p.fiatexchangepair')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fiat_preferences', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='userfiatpreferences',
            constraint=models.UniqueConstraint(fields=('user', 'pair', 'side_operation'), name='unique_user_pair_side'),
        ),
    ]
