# Generated by Django 4.2.4 on 2023-10-29 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_transactionlog_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='businesscontribution',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='transactionfile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='transactionlog',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
