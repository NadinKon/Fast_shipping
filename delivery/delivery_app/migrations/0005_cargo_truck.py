# Generated by Django 4.2.1 on 2023-05-24 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_app', '0004_alter_location_zip_alter_truck_unique_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='cargo',
            name='truck',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cargos', to='delivery_app.truck'),
            preserve_default=False,
        ),
    ]
