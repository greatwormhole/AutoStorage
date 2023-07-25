from factory.django import DjangoModelFactory
import factory

from .models import *

class WorkerFactory(DjangoModelFactory):

    id = factory.Sequence(lambda num: num)
    name = factory.Faker('name')
    storage_right = factory.Faker('boolean', chance_of_getting_true=50)
    plan_right = factory.Faker('boolean', chance_of_getting_true=50)
    quality_control_right = factory.Faker('boolean', chance_of_getting_true=50)
    status = factory.Faker('boolean', chance_of_getting_true=100)

    class Meta:
        model = Worker

class NomenclatureFactory(DjangoModelFactory):

    article = factory.Faker('bothify', text='?#?#?#?#?#?')
    title = factory.Faker('sentence', nb_words=5)
    maximum = factory.Faker('numerify', text='$#######!!')
    minimum = factory.Faker('numerify', text='%#######!!')
    mass = factory.Faker('numerify', text='%##!!')

    class Meta:
        model = Nomenclature

class StorageFactory(DjangoModelFactory):
    
    adress = factory.Sequence(lambda x: x)
    cell_size = factory.Faker('numerify', text='%!!!!!x%!!!!!x%!!!!!')
    mass = factory.Faker('numerify', text='%##!!!')

    class Meta:
        model = Storage

class CrateFactory(DjangoModelFactory):

    amount = factory.Faker('numerify', text='%##!')
    size = factory.Faker('numerify', text='%!!!x%!!!x%!!!')

    class Meta:
        model = Crates