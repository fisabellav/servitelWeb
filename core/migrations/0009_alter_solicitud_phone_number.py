# Generated by Django 5.0.4 on 2024-06-13 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_solicitudproducto_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='phone_number',
            field=models.CharField(max_length=15, verbose_name='TELÉFONO'),
        ),
    ]
