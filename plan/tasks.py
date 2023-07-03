import time

from Apro.celery import app

import json
import sys

import os
from django.core import serializers

# db_list = [CURPOS, SFTYSIG, IOSTATE, ERRALL, NUMREG]

@app.task
def test():
   print('jkjh')