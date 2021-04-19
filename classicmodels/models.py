# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_of_birth = models.IntegerField(blank=True, null=True)
    date_joined = models.DateTimeField()
    somenum = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class ConversionRate(models.Model):
    conversion_rate_id = models.IntegerField(db_column='CONVERSION_RATE_ID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=10)  # Field name made lowercase.
    value = models.FloatField(db_column='VALUE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'conversion_rate'


class DebitCards(models.Model):
    debit_card_id = models.IntegerField(db_column='DEBIT_CARD_ID', primary_key=True)  # Field name made lowercase.
    debit_card_num = models.BigIntegerField(db_column='DEBIT_CARD_NUM', blank=True, null=True)  # Field name made lowercase.
    cvv = models.IntegerField(db_column='CVV')  # Field name made lowercase.
    expiration_date = models.CharField(max_length=7)
    fk_debit_cards_monetary_info1 = models.ForeignKey('MonetaryInfo', models.DO_NOTHING, db_column='fk_DEBIT_CARDS_MONETARY_INFO1', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'debit_cards'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class MonetaryInfo(models.Model):
    monetary_id = models.AutoField(db_column='MONETARY_ID', primary_key=True)  # Field name made lowercase.
    usd_sum = models.DecimalField(max_digits=65, decimal_places=2, blank=True, null=True)
    cad_sum = models.DecimalField(db_column='CAD_SUM', max_digits=65, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    bank_account_number = models.BigIntegerField(blank=True, null=True)
    conversion_rate_conversion_rate = models.ForeignKey(ConversionRate, models.DO_NOTHING, db_column='CONVERSION_RATE_CONVERSION_RATE_ID', blank=True, null=True)  # Field name made lowercase.
    auth_user = models.OneToOneField(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monetary_info'


class Transaction(models.Model):
    transaction_id = models.IntegerField(db_column='TRANSACTION_ID', primary_key=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='AMOUNT', max_digits=2, decimal_places=0)  # Field name made lowercase.
    date = models.DateField(db_column='DATE')  # Field name made lowercase.
    currency = models.CharField(db_column='CURRENCY', max_length=3)  # Field name made lowercase.
    transfers_transfer = models.ForeignKey('Transfers', models.DO_NOTHING, db_column='TRANSFERS_TRANSFER_ID')  # Field name made lowercase.
    monetary_info_monetary = models.ForeignKey(MonetaryInfo, models.DO_NOTHING, db_column='MONETARY_INFO_MONETARY_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'transaction'


class Transfers(models.Model):
    transfer_id = models.IntegerField(db_column='TRANSFER_ID', primary_key=True)  # Field name made lowercase.
    recipient = models.IntegerField(db_column='RECIPIENT')  # Field name made lowercase.
    sender = models.IntegerField(db_column='SENDER')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'transfers'
