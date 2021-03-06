# Generated by Django 3.1.2 on 2020-10-29 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productquestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
        migrations.AddField(
            model_name='productinformation',
            name='packing_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.packingtype'),
        ),
        migrations.AddField(
            model_name='productinformation',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
        migrations.AddField(
            model_name='productinformation',
            name='shipping_classification',
            field=models.ManyToManyField(through='product.ProductShipping', to='product.ShippingClassification'),
        ),
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.discount'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_question',
            field=models.ManyToManyField(related_name='product_questions', through='product.ProductQuestion', to='user.User'),
        ),
        migrations.AddField(
            model_name='product',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.subcategory'),
        ),
    ]
