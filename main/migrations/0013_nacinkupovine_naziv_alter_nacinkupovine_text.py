# Generated by Django 5.0.3 on 2024-04-05 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_nacinkupovine'),
    ]

    operations = [
        migrations.AddField(
            model_name='nacinkupovine',
            name='naziv',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='nacinkupovine',
            name='text',
            field=models.CharField(blank=True, max_length=1000, null=True, unique=True),
        ),
    ]
