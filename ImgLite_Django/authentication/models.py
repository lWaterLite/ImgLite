from django.db import models


class UserIndex(models.Model):
    userIndex = models.CharField(primary_key=True, max_length=16, db_column='user_index')
    userAccount = models.CharField(unique=True, max_length=10, db_column='user_account')
    userPassword = models.CharField(max_length=15, db_column='user_password')
    userUUID = models.CharField(unique=True, max_length=32, db_column='user_uuid')

    class Meta:
        managed = False
        db_table = 'user_index'


class InviteCode(models.Model):
    inviteCode = models.CharField(primary_key=True, db_column='invite_code', max_length=5)

    class Meta:
        managed = False
        db_table = 'invite_code'
