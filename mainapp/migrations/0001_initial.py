# Generated by Django 2.0.6 on 2018-06-22 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('image', models.ImageField(blank=True, upload_to='prod_images')),
                ('short_desc', models.CharField(blank=True, max_length=128, verbose_name='short_description')),
                ('description', models.TextField(blank=True, verbose_name='long_description')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='prod_price')),
                ('quantity', models.PositiveIntegerField(verbose_name='остаток')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='имя')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.ProductCategory'),
        ),
    ]
