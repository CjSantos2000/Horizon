# Generated by Django 4.2.4 on 2023-10-15 07:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_transactionfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionlog',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='transactionlog',
            name='transaction_id',
            field=models.CharField(default=uuid.uuid4, max_length=255),
        ),
    ]
