from .validators import ArticleJSONValidator, JSONSCHEMA

from django.db import models
from django.contrib.postgres.fields import ArrayField

from datetime import datetime

class Nomenclature(models.Model):
    article = models.CharField(max_length=250, primary_key=True)
    title = models.CharField(max_length=250)
    units = models.CharField(max_length=60)
    maximum = models.FloatField(null=True)
    minimum = models.FloatField(null=True)
    mass = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Номенклатура"
        verbose_name_plural = "Номенклатура"

class Specification(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    article_list = models.JSONField(default=dict,
                                    validators=[ArticleJSONValidator(limit_value=JSONSCHEMA)])
    production_time = models.TimeField()

    def __str__(self):
        return self.id
    
    class Meta:
        verbose_name = "Спецификация"
        verbose_name_plural = "Спецификации"

class Crates(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.RESTRICT)
    amount = models.FloatField()
    size = models.CharField(max_length=60)

    def __str__(self):
        return self.nomenclature
    
    class Meta:
        verbose_name = "Коробка"
        verbose_name_plural = "Коробки"

class Worker(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    storage_right = models.BooleanField()
    plan_right = models.BooleanField()
    quality_control_right = models.BooleanField()
    status = models.BooleanField()

    def  __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

class DeliveryNote(models.Model):
    number = models.PositiveBigIntegerField(primary_key=True)
    datetime = models.DateTimeField(default=datetime.now())
    worker_id = models.ForeignKey(Worker, on_delete=models.RESTRICT)
    article_list = models.JSONField(default=dict,
                                    validators=[ArticleJSONValidator(limit_value=JSONSCHEMA)])

    def __str__(self):
        return self.number
    
    class Meta:
        verbose_name = "Накладная"
        verbose_name_plural = "Накладные"

class Storage(models.Model):
    adress = models.CharField(max_length=250, primary_key=True)
    crate_list = ArrayField(base_field=models.IntegerField(), default=list)
    cell_size = models.CharField(max_length=60)
    size_left = models.FloatField()
    storage_name = models.CharField(max_length=60)
    mass = models.PositiveIntegerField(default=700)

    def __str__(self):
        return self.adress
    
    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"

class ProductionStorage(models.Model):
    article = models.CharField(max_length=60, primary_key=True)
    amount = models.FloatField()

    def __str__(self):
        return self.article
    
    class Meta:
        verbose_name = "Склад производства"
        verbose_name_plural = "Склады производства"
    
class Flaw(models.Model):
    id = models.PositiveBigIntegerField()
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.RESTRICT)
    amount = models.FloatField()
    datetime = models.DateTimeField(primary_key=True, default=datetime.now())
    worker_add = models.ForeignKey(Worker, on_delete=models.RESTRICT, related_name='worker_addition')
    worker_decision = models.ForeignKey(Worker, on_delete=models.RESTRICT, related_name='worker_decision', blank=True)
    decision = models.BooleanField(blank=True)
    
    def __str__(self):
        return self.nomenclature
    
    class Meta:
        verbose_name = "Брак"
        verbose_name_plural = "Бракованные детали"
        ordering=['-datetime']


class THD(models.Model):
    THD_number = models.PositiveIntegerField()
    ip = models.CharField(max_length=250)
    is_using = models.BooleanField(default=False)
    is_comp = models.BooleanField(default=False)
    worker_id = models.ForeignKey(Worker, on_delete=models.RESTRICT, blank=True, null=True)

    def __str__(self):
        return str(self.THD_number)

    class Meta:
        verbose_name = "Номер ТСД"
        verbose_name_plural = "Номер ТСД"