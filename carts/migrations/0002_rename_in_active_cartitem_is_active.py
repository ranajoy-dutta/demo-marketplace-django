# Generated by Django 3.2.8 on 2021-11-07 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='in_active',
            new_name='is_active',
        ),
    ]
