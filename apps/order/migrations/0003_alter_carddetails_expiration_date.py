# Generated by Django 5.1.4 on 2025-07-21 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_carddetails_payme_token_carddetails_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carddetails',
            name='expiration_date',
            field=models.CharField(max_length=4, verbose_name='Дата истечения (MMYY)'),
        ),
    ]
