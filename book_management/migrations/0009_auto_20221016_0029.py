# Generated by Django 3.2.6 on 2022-10-15 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_management', '0008_rename_issued_book_issued_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='issue',
            name='issued_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
