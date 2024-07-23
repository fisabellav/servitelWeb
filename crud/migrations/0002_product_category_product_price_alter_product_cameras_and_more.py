# Generated by Django 5.0.4 on 2024-07-15 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('CA', 'Cámaras'), ('KI', 'Kits'), ('AC', 'Accesorios')], default='KI', max_length=2, verbose_name='Categoría'),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Precio'),
        ),
        migrations.AlterField(
            model_name='product',
            name='cameras',
            field=models.IntegerField(blank=True, null=True, verbose_name='Cámaras'),
        ),
        migrations.AlterField(
            model_name='product',
            name='channels',
            field=models.IntegerField(blank=True, null=True, verbose_name='Canales'),
        ),
    ]
