# Generated by Django 2.1 on 2018-08-11 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('department', models.IntegerField()),
                ('text', models.TextField(max_length=500)),
                ('status', models.IntegerField()),
                ('date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
