# Generated by Django 5.0.6 on 2024-05-09 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_rename_image_category_cat_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='cat_image',
            new_name='category_image',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='cat_name',
            new_name='category_name',
        ),
    ]