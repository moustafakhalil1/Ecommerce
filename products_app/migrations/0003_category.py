# Generated by Django 4.1.1 on 2022-10-01 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0002_alter_product_prdcost_alter_product_prddescription_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CATName', models.CharField(max_length=100, verbose_name='sup category')),
                ('CATDescription', models.TextField(max_length=1000)),
                ('CATImg', models.ImageField(upload_to='category_image')),
                ('CATParent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products_app.category', verbose_name='Main category')),
            ],
        ),
    ]
