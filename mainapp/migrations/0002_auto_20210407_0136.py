# Generated by Django 3.1.7 on 2021-04-07 01:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='review',
            name='date_published',
        ),
        migrations.RemoveField(
            model_name='review',
            name='shoe',
        ),
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
        migrations.AddField(
            model_name='review',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.customer'),
        ),
        migrations.AddField(
            model_name='review',
            name='date_added',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='review',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='shoe',
            name='gender_category',
            field=models.CharField(choices=[('M', 'Male'), ('U', 'Unisex'), ('F', 'Female')], max_length=20),
        ),
        migrations.AlterField(
            model_name='shoe',
            name='shoe_category',
            field=models.CharField(choices=[('H', 'Highheels'), ('E', 'Evening Wear'), ('C', 'Casual'), ('S', 'Sport'), ('SL', 'Slippers'), ('P', 'Pumps'), ('SA', 'Sandals')], max_length=20),
        ),
    ]