from django.db import models
from django.db.models import Q

from functools import reduce

from .validators import *

TEXT_ID_RANK = 7

class Nomenclature(models.Model):
    article = models.CharField(max_length=250, primary_key=True, verbose_name='Артикул')
    title = models.CharField(max_length=100, unique=True,verbose_name='Наименование')
    units = models.CharField(max_length=20, verbose_name='Единицы измерения')
    maximum = models.FloatField(null=True, blank=True, verbose_name='Максимум продукции')
    minimum = models.FloatField(null=True, blank=True, verbose_name='Минимум продукцииё')
    mass = models.FloatField(blank=True, null=True, verbose_name='Масса одного изделия')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Номенклатура"
        verbose_name_plural = "Номенклатура"
        constraints = [
                        models.CheckConstraint(
                check=(
                    Q(units__exact='кг') | Q(units__exact='шт')
                ),
                name='Значение единиц измерения необходимо указывать в килограммах или штуках в формате кг или шт'
            ),
            models.CheckConstraint(
                check=((
                    Q(units__exact='шт') &
                    Q(mass__isnull=False)
                ) | (
                    Q(units__exact='кг')
                ) 
                ),
                name='Если изделие измеряется поштучно необходимо указать массу одного изделия'
            )
        ]

class Specification(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    nomenclatures = models.ManyToManyField(Nomenclature, verbose_name='Содержимое спецификации')
    production_time = models.TimeField(verbose_name='Время производства')

    def __str__(self):
        return f'{self.id}'
    
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
    number = models.CharField(max_length=150, default='')
    datetime = models.DateTimeField(auto_now_add=True)
    worker = models.ForeignKey(Worker, on_delete=models.RESTRICT)
    article_list = models.TextField(null=True, blank=True)
    provider = models.CharField(max_length=150, default='')

    def __str__(self):
        return self.number
    
    class Meta:
        verbose_name = "Накладная"
        verbose_name_plural = "Накладные"
        
class RejectionAct(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    worker = models.ForeignKey(Worker, on_delete=models.RESTRICT)
    article_list = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.datetime}'
    
    class Meta:
        verbose_name = 'Акт выбраковки'
        verbose_name_plural = 'Акты выбраковки'

class Storage(models.Model):
    adress = models.PositiveIntegerField(primary_key=True)
    x_cell_size = models.PositiveIntegerField(default=0)
    y_cell_size = models.PositiveIntegerField(default=0)
    z_cell_size = models.PositiveIntegerField(default=0)
    x_cell_coord = models.PositiveIntegerField(default=0)
    y_cell_coord = models.PositiveIntegerField(default=0)
    z_cell_coord = models.PositiveIntegerField(default=0)
    storage_name = models.CharField(max_length=60, validators=[validate_no_spaces])
    mass = models.PositiveIntegerField(default=700)
    visualization_x = models.IntegerField(default=20)
    visualization_y = models.IntegerField(default=20)
    visualization_z = models.IntegerField(default=3000)

    def __str__(self):
        return f'Storage: {self.storage_name}, cell#{self.adress}'
    
    @property
    def is_blocked(self):
        neighbour_cells = self.neighboring_cells()
        if len(neighbour_cells) < 4:
            return False
        elif len(neighbour_cells) == 4 and not False in [cell.full_percent > 80 for cell in neighbour_cells]:
            return True
        return False
    
    @property
    def size_left(self):
        size = self.volume
        for el in self.crates.all():
            size -= el.volume
        return size
    
    @property
    def volume(self):
        return self.x_cell_size * self.y_cell_size * self.z_cell_size
    
    @property
    def full_percent(self):
        try:
            return round(reduce(lambda i, j: i + j, [crate.volume for crate in self.crates.all()]) / self.volume * 100)
        except TypeError:
            return 0
    
    def neighboring_cells(self):
        return self.__class__.objects.filter(
            Q(storage_name=self.storage_name) &
            (
                (Q(x_cell_coord=self.x_cell_coord - 1) & Q(y_cell_coord=self.y_cell_coord) & Q(z_cell_coord=self.z_cell_coord)) |
                (Q(x_cell_coord=self.x_cell_coord + 1) & Q(y_cell_coord=self.y_cell_coord) & Q(z_cell_coord=self.z_cell_coord)) |
                (Q(x_cell_coord=self.x_cell_coord) & Q(y_cell_coord=self.y_cell_coord - 1) & Q(z_cell_coord=self.z_cell_coord)) | 
                (Q(x_cell_coord=self.x_cell_coord) & Q(y_cell_coord=self.y_cell_coord + 1) & Q(z_cell_coord=self.z_cell_coord))
            )
        )
    
    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"

class ProductionStorage(models.Model):
    title = models.CharField(max_length=250, primary_key=True, default='')
    amount = models.FloatField()
    units = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Склад производства"
        verbose_name_plural = "Склады производства"

class Crates(models.Model):
    text_id = models.CharField(max_length=15, blank=True, null=True)
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.RESTRICT)
    amount = models.FloatField()
    size = models.CharField(max_length=80)
    cell = models.ForeignKey(Storage, on_delete=models.RESTRICT, blank=True, null=True, related_name='crates')
    
    @property
    def rank(self):
        id = self.id
        counter = 0
        while id != 0:
            id //= 10
            counter += 1
        return counter
    
    @property
    def volume(self):
        return reduce(lambda i, j: float(i) * float(j), self.size.split('x'))

    def get_same_nomenclature(self):
        return self.__class__.objects.filter(nomenclature=self.nomenclature)
    
    def __str__(self):
        return f'Коробка {self.nomenclature.title} - {self.amount} {self.nomenclature.units}'
    
    class Meta:
        verbose_name = "Коробка"
        verbose_name_plural = "Коробки"
    
class Flaw(models.Model):
    datetime = models.DateTimeField(primary_key=True, auto_now_add=True)
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.RESTRICT)
    amount = models.FloatField()
    rejection_act = models.ForeignKey(RejectionAct, on_delete=models.CASCADE, null=True)
    worker_decision = models.ForeignKey(Worker, on_delete=models.RESTRICT, related_name='worker_decision', blank=True, null=True)
    decision = models.BooleanField(blank=True, null=True)
    
    def __str__(self):
        return self.nomenclature.title
    
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
        
class TempCrate(models.Model):
    crate = models.ForeignKey(Crates, on_delete=models.RESTRICT)
    text_id = models.CharField(max_length=15, blank=True, null=True)
    amount = models.FloatField()
    size = models.CharField(max_length=80)
    
    def __str__(self):
        return f' Временная коробка к {self.crate.__str__()}'

    @property
    def rank(self):
        id = self.id
        counter = 0
        while id != 0:
            id //= 10
            counter += 1
        return counter
    
    class Meta:
        verbose_name = 'Временная коробка'
        verbose_name_plural = 'Временные коробки'


class settings(models.Model):
    setting_name = models.CharField(max_length=250)
    value = models.CharField(max_length=250)

    def __str__(self):
        return self.setting_name

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'