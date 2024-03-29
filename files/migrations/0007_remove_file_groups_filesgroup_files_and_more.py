# Generated by Django 5.0 on 2023-12-16 19:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0006_filesgroup_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='groups',
        ),
        migrations.AddField(
            model_name='filesgroup',
            name='files',
            field=models.ManyToManyField(blank=True, to='files.file'),
        ),
        migrations.AlterField(
            model_name='file',
            name='editor_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='filesgroup',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='filesgroup',
            name='users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
