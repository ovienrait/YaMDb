# Generated by Django 3.2 on 2024-06-21 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ('id',)},
        ),
    ]