# Generated by Django 3.1.5 on 2021-02-15 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgeting', '0005_auto_20210204_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetitem',
            name='spent',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]