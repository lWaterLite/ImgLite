# Generated by Django 4.1.7 on 2023-03-16 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImgIndex',
            fields=[
                ('imgIndex', models.CharField(db_column='img_index', max_length=16, primary_key=True, serialize=False)),
                ('imgName', models.CharField(db_column='img_name', max_length=127)),
                ('imgUploadDate', models.DateField(db_column='img_upload_date')),
                ('imgUUID', models.CharField(db_column='img_uuid', max_length=32, unique=True)),
            ],
            options={
                'db_table': 'img_index',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ImgType',
            fields=[
                ('imgType', models.AutoField(db_column='img_type', primary_key=True, serialize=False)),
                ('imgTypeName', models.CharField(db_column='img_type_name', max_length=3)),
            ],
            options={
                'db_table': 'img_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserIndex',
            fields=[
                ('userIndex', models.CharField(db_column='user_index', max_length=16, primary_key=True, serialize=False)),
                ('userAccount', models.CharField(db_column='user_account', max_length=10, unique=True)),
                ('userPassword', models.CharField(db_column='user_password', max_length=15)),
                ('userUUID', models.CharField(db_column='user_uuid', max_length=32, unique=True)),
            ],
            options={
                'db_table': 'user_index',
                'managed': False,
            },
        ),
    ]
