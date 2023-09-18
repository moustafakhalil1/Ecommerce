# Generated by Django 4.1.1 on 2022-09-30 01:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='PRDCost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='product cost'),
        ),
        migrations.AlterField(
            model_name='product',
            name='PRDDescription',
            field=models.TextField(verbose_name='product description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='PRDName',
            field=models.CharField(max_length=100, verbose_name='product name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='PRDPric',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='product pric'),
        ),
        migrations.AlterField(
            model_name='product',
            name='PRDcreated',
            field=models.DateTimeField(verbose_name='product date'),
        ),
        migrations.CreateModel(
            name='productimage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PRDimage', models.ImageField(upload_to='product_photo', verbose_name='product image')),
                ('PRDIproduct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products_app.product', verbose_name='product')),
            ],
        ),
    ]
