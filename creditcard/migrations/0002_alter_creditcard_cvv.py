# Generated by Django 4.1.7 on 2023-03-08 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditcard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcard',
            name='cvv',
            field=models.IntegerField(verbose_name='cvv'),
        ),
    ]
