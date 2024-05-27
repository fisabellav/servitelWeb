# Generated by Django 5.0.4 on 2024-05-23 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=50, verbose_name='Producto')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('image', models.ImageField(blank=True, null=True, upload_to='productos', verbose_name='Imagen')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha actualización')),
            ],
            options={
                'verbose_name': 'producto',
                'verbose_name_plural': 'productos',
                'ordering': ['product'],
            },
        ),
    ]
