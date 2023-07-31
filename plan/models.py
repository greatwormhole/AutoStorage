from django.db import models

class Plans(models.Model):
    
    title = models.CharField(max_length=120, verbose_name='Название плана')
    datetime = models.DateTimeField(primary_key=True, auto_now_add=True, verbose_name='Дата добавления')
    
    def __str__(self):
        return f'{self.title} от {self.datetime}'
    
    class Meta:
        verbose_name = 'План'
        verbose_name_plural = 'Планы'