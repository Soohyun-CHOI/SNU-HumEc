# Generated by Django 3.2.6 on 2021-09-15 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0003_alter_communitypost_hits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communitypost',
            name='market_tag',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
