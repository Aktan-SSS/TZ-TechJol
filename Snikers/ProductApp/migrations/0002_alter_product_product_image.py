# Generated by Django 5.1.3 on 2024-11-25 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, null=True, upload_to='ProductImages/', verbose_name='Фото продукта'),
        ),
    ]