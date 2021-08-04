# Generated by Django 3.2.6 on 2021-08-04 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TasksScheduler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tasks_file', models.FileField(upload_to='files/%Y/%m/%d')),
                ('raw_tasks', models.CharField(max_length=1000)),
                ('best_schedule', models.CharField(max_length=1000)),
            ],
        ),
    ]
