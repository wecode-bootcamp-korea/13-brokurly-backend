# Generated by Django 3.1.1 on 2020-10-21 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_delete_address'),
        ('product', '0004_auto_20201021_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_question',
            field=models.ManyToManyField(related_name='product_questions', through='product.ProductQuestion', to='user.User'),
        ),
    ]
