# Generated by Django 3.1.5 on 2021-03-18 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CCC', '0002_job_gerrit_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='jira_status',
            field=models.CharField(default='Screen', max_length=100),
        ),
    ]
