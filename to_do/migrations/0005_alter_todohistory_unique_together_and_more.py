# Generated by Django 5.1.5 on 2025-02-19 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('to_do', '0004_rename_complete_date_todohistory_date_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='todohistory',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='todohistory',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterUniqueTogether(
            name='todohistory',
            unique_together={('todo', 'date', 'status')},
        ),
    ]
