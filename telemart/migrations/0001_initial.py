# Generated by Django 4.1.1 on 2022-10-18 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyMake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='companies/')),
            ],
            options={
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='UserAddon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userpic', models.ImageField(blank=True, null=True, upload_to='userpics/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='addon', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('rating', models.FloatField(default=5.0)),
                ('views', models.IntegerField(default=0)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('description', models.FileField(blank=True, null=True, upload_to='descriptions/')),
                ('trailer', models.CharField(blank=True, max_length=11, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='telemart.companymake')),
                ('fans', models.ManyToManyField(blank=True, related_name='wishlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('published', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='telemart.product')),
            ],
            options={
                'ordering': ['-published'],
            },
        ),
    ]
