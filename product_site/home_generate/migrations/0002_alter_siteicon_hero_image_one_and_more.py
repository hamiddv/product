# Generated by Django 4.2 on 2023-05-26 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_generate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteicon',
            name='hero_image_one',
            field=models.ImageField(blank=True, null=True, upload_to='./media/hero_section/'),
        ),
        migrations.AlterField(
            model_name='siteicon',
            name='hero_image_two',
            field=models.ImageField(blank=True, null=True, upload_to='./media/hero_section/'),
        ),
        migrations.AlterField(
            model_name='siteicon',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='./media/site_icon/'),
        ),
    ]