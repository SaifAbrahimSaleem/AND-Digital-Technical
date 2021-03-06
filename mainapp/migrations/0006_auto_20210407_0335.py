# Generated by Django 3.1.7 on 2021-04-07 03:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20210407_0257'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='shie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.shoe'),
        ),
        migrations.AlterField(
            model_name='shoe',
            name='gender_category',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('U', 'Unisex')], max_length=20),
        ),
        migrations.AlterField(
            model_name='shoe',
            name='shoe_category',
            field=models.CharField(choices=[('C', 'Casual'), ('H', 'Highheels'), ('SA', 'Sandals'), ('P', 'Pumps'), ('E', 'Evening Wear'), ('S', 'Sport'), ('SL', 'Slippers')], max_length=20),
        ),
    ]
