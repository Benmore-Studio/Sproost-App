# Generated by Django 5.0.2 on 2024-06-11 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0004_remove_quoterequest_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quoterequest',
            old_name='user',
            new_name='created_by_home_owners',
        ),
    ]
