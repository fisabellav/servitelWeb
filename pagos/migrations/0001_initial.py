# Generated by Django 5.0.4 on 2024-10-03 18:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0004_delete_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_number', models.PositiveIntegerField(verbose_name='Número de cuota')),
                ('amount', models.PositiveIntegerField(verbose_name='Monto pagado')),
                ('payment_date', models.DateField(verbose_name='Fecha de pago')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha actualización')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Comentarios')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.order', verbose_name='Pedido')),
            ],
            options={
                'verbose_name': 'Pago cuotas',
                'verbose_name_plural': 'Pagos cuotas',
            },
        ),
    ]
