# Generated by Django 3.2.4 on 2021-06-27 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0006_auto_20210626_1304'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (0, 'Sunday')])),
            ],
        ),
        migrations.CreateModel(
            name='WorkTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='master',
            name='work_schedule_parts',
        ),
        migrations.DeleteModel(
            name='WorkSchedulePart',
        ),
        migrations.AddField(
            model_name='workday',
            name='worktimes',
            field=models.ManyToManyField(to='appointments.WorkTime'),
        ),
        migrations.AddField(
            model_name='master',
            name='work_days',
            field=models.ManyToManyField(to='appointments.WorkDay'),
        ),
    ]