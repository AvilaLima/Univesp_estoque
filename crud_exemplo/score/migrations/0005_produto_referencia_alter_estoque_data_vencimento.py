# Generated by Django 5.0.4 on 2024-05-14 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0004_alter_estoque_options_alter_funcionario_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='referencia',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='estoque',
            name='data_vencimento',
            field=models.DateField(null=True),
        ),
    ]
