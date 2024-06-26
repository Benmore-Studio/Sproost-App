# Generated by Django 5.0.4 on 2024-06-08 15:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_agentprofile_registration_id'),
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quoterequest',
            name='created_by_agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agent_quote_requests', to='profiles.agentprofile'),
        ),
    ]
