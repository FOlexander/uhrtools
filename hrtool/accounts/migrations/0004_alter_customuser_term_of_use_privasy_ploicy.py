# Generated by Django 4.1.7 on 2023-06-07 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_term_of_use_privasy_ploicy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='term_of_use_privasy_ploicy',
            field=models.BooleanField(null=True),
        ),
    ]
