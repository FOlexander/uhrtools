# Generated by Django 4.1.7 on 2023-06-16 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datadownload', '0011_alter_plotfile_plot_hazard12m_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='plotfile',
            name='plot_name',
            field=models.CharField(default=2, max_length=20),
            preserve_default=False,
        ),
    ]