from django.db import models


class ImgIndex(models.Model):
    imgIndex = models.CharField(primary_key=True, db_column='img_index', max_length=16)
    imgName = models.CharField(max_length=127, db_column='img_name')
    imgType = models.ForeignKey('ImgType', models.DO_NOTHING, db_column='img_type')
    imgUploadDate = models.DateField(db_column='img_upload_date')
    imgUUID = models.CharField(max_length=32, db_column='img_uuid', unique=True)
    userIndex = models.ForeignKey('UserIndex', models.DO_NOTHING, db_column='user_index')

    class Meta:
        managed = False
        db_table = 'img_index'


class ImgType(models.Model):
    imgType = models.AutoField(primary_key=True, db_column='img_type')
    imgTypeName = models.CharField(max_length=3, db_column='img_type_name')

    class Meta:
        managed = False
        db_table = 'img_type'


class UserIndex(models.Model):
    userIndex = models.CharField(primary_key=True, max_length=16, db_column='user_index')
    userAccount = models.CharField(unique=True, max_length=10, db_column='user_account')
    userPassword = models.CharField(max_length=15, db_column='user_password')
    userUUID = models.CharField(unique=True, max_length=32, db_column='user_uuid')

    class Meta:
        managed = False
        db_table = 'user_index'
