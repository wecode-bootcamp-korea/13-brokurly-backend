# Generated by Django 3.1.2 on 2020-10-22 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20201022_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frequentlypurchasedproduct',
            name='description',
            field=models.CharField(max_length=50),
        ),
    ]
