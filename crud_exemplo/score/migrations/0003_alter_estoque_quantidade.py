# Generated by Django 4.2.2 on 2024-05-06 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0002_produto_setor_alter_score_options_funcionario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estoque',
            name='quantidade',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
