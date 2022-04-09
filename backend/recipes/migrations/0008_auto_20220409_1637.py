# Generated by Django 2.2.19 on 2022-04-09 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20220409_1259'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipes'), name='unique_favorite'),
        ),
    ]
