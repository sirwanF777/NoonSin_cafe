# Generated by Django 3.2 on 2023-06-23 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('create_time', models.DateField(auto_now_add=True)),
                ('modified_time', models.DateField(auto_now=True)),
                ('pattern', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogue.category')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upc', models.IntegerField(unique=True)),
                ('title', models.CharField(max_length=32, verbose_name='title')),
                ('price', models.IntegerField(verbose_name='price')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('create_time', models.DateField(auto_now_add=True)),
                ('modified_time', models.DateField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='catalogue.category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
        ),
    ]
