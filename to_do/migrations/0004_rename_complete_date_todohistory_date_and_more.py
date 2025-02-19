# Generated by Django 5.1.5 on 2025-02-19 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('to_do', '0003_alter_todorepeat_todo_todohistory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todohistory',
            old_name='complete_date',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='todo',
            name='done',
        ),
        migrations.AddField(
            model_name='todohistory',
            name='status',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterUniqueTogether(
            name='todohistory',
            unique_together={('todo', 'date')},
        ),
    ]
