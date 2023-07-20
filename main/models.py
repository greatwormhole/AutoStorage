from .validators import ArticleJSONValidator, JSONSCHEMA

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime

TEXT_ID_RANK = 8

class Nomenclature(models.Model):
    article = models.CharField(max_length=250, primary_key=True)
    title = models.CharField(max_length=250, unique=True)
    units = models.CharField(max_length=60)
    maximum = models.FloatField(null=True, blank=True)
    minimum = models.FloatField(null=True, blank=True)
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
    id = models.CharField(primary_key=True, max_length=150, default='')
    datetime = models.DateTimeField(auto_now_add=True)
    worker = models.ForeignKey(Worker, on_delete=models.RESTRICT)
    article_list = models.TextField(null=True, blank=True)
    provider = models.CharField(max_length=150, default='')

    def __str__(self):
        return self.id
    
    class Meta:
        verbose_name = "Накладная"
        verbose_name_plural = "Накладные"

class Storage(models.Model):
    adress = models.PositiveIntegerField(primary_key=True)
    cell_size = models.CharField(max_length=60)
    size_left = models.FloatField()
    storage_name = models.CharField(max_length=60)
    mass = models.PositiveIntegerField(default=700)

    def __str__(self):
        return f'{self.adress}'
    
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

class Crates(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    text_id = models.CharField(max_length=15, blank=True, null=True)
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.RESTRICT)
    amount = models.FloatField()
    size = models.CharField(max_length=80)
    cell = models.ForeignKey(Storage, on_delete=models.RESTRICT, blank=True, null=True, related_name='crates')

    @property
    def rank(self):
        id = self.id
        counter = 1
        while id != 0:
            id //= 10
        return counter

    def __str__(self):
        return f'Коробка {self.nomenclature.title} - {self.amount} {self.nomenclature.units}'
    
    class Meta:
        verbose_name = "Коробка"
        verbose_name_plural = "Коробки"
    
class Flaw(models.Model):
    id = models.PositiveBigIntegerField()
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.RESTRICT)
    amount = models.FloatField()
    datetime = models.DateTimeField(primary_key=True, auto_now_add=True)
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
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'ТСД №{self.THD_number}'

    class Meta:
        verbose_name = "Номер ТСД"
        verbose_name_plural = "Номер ТСД"

@receiver(post_save, sender=Crates)
def fill_text_id(sender, instance, created, **kwargs):
    zero_amount = TEXT_ID_RANK - instance.rank
    instance.text_id = zero_amount * '0' + str(instance.id)