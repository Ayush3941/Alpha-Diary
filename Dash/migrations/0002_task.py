# Generated by Django 5.1.2 on 2024-11-24 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dash', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
    ]
