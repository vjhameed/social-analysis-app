# Generated by Django 2.1.1 on 2019-03-14 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_project_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagetoken',
            name='page_id',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
