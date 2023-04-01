# Generated by Django 4.1 on 2023-04-01 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('women', '0004_alter_women_options_women_owner_alter_women_cat_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='women',
            options={'ordering': ['-time_create'], 'verbose_name': 'Famous Women', 'verbose_name_plural': 'Famous Women'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Name of category'),
        ),
        migrations.AlterField(
            model_name='women',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='get_posts', to='women.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='women',
            name='content',
            field=models.TextField(verbose_name='Article text'),
        ),
        migrations.AlterField(
            model_name='women',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='Publication'),
        ),
        migrations.AlterField(
            model_name='women',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='women',
            name='photo',
            field=models.ImageField(upload_to='img/', verbose_name='Photo'),
        ),
        migrations.AlterField(
            model_name='women',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation time'),
        ),
        migrations.AlterField(
            model_name='women',
            name='time_update',
            field=models.DateTimeField(auto_now=True, verbose_name='Correction time'),
        ),
        migrations.AlterField(
            model_name='women',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Title'),
        ),
    ]