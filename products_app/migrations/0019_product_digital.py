# Generated by Django 4.1.1 on 2023-09-07 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0018_alter_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='digital',
            field=models.BooleanField(default=True),
        ),
    ]