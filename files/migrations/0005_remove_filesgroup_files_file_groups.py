# Generated by Django 5.0 on 2023-12-16 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0004_alter_filesgroup_files_alter_filesgroup_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filesgroup',
            name='files',
        ),
        migrations.AddField(
            model_name='file',
            name='groups',
            field=models.ManyToManyField(to='files.filesgroup'),
        ),
    ]
