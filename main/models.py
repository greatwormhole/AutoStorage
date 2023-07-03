from django.db import models

class Nomenclature(models.Model):
    article = models.CharField(max_length=250, primary_key=True)
    title = models.CharField(max_length=250)
    units = models.CharField(max_length=60)
    comment = models.TextField()

class Specification(models.Model):
    part_number = models.IntegerField(primary_key=True)
    article_list = models.TextField()
    eta = models.TimeField()

class Crates(models.Model):
    id = models.IntegerField(primary_key=True)
    article = models.ForeignKey(Nomenclature)
    amount = models.FloatField()
    size = models.CharField(max_length=60)

class Worker(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    storage_right = models.BooleanField()
    plan_right = models.BooleanField()
    status = models.BooleanField()

class DeliveryNote(models.Model):
    number = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    description = models.TextField()
    worker_id = models.ForeignKey(Worker)

class Storage(models.Model):
    adress = models.CharField(max_length=250, primary_key=True)
    crate_list = models.TextField()
    cell_size = models.CharField(max_length=60)
    size_left = models.FloatField()

class ProductionStorage(models.Model):
    article = models.CharField(max_length=60, primary_key=True)
    amount = models.FloatField()

class Flaw(models.Model):
    article = models.CharField(max_length=60)
    nomenclature = models.ForeignKey(Nomenclature)
    amount = models.FloatField()
    datetime = models.DateTimeField(primary_key=True)
    worker_add_id = models.ForeignKey(Worker)
    worker_decision_id = models.ForeignKey(Worker)
    decision = models.BooleanField()
    crate_id = models.IntegerField()