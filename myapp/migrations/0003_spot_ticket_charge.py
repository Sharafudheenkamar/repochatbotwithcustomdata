# Generated by Django 5.1.3 on 2025-01-07 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_restauranttable_delete_restaurantcomplainttable'),
    ]

    operations = [
        migrations.AddField(
            model_name='spot',
            name='ticket_charge',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]