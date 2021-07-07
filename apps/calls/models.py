# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CallRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    incoming_number = models.IntegerField(blank=True, null=True)
    outgoing_number = models.IntegerField()
    duration = models.IntegerField()
    dialed_on = models.DateField()

    class Meta:
        managed = False
        db_table = 'call_record'

    def __str__(self):
        return str(self.outgoing_number)


class CustomerDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    subscription_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    phone = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'customer_detail'


class SubscriptionPlan(models.Model):
    id = models.BigAutoField(primary_key=True)
    plan = models.CharField(max_length=255)
    quota = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'subscription_plan'
