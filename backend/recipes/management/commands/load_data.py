"""
Пополнение базы данных информацией по продуктам.
"""

import json
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """
    Класс пополнения базы данных
    информацией по продуктам.
    """

    def handle(self, *args, **options):
        with open('data/ingredients.json', 'rb') as f:
            data = json.load(f)
            for i in data:
                ingredient = Ingredient()
                ingredient.name = i['name']
                ingredient.measurement_unit = i['measurement_unit']
                ingredient.save()
                print(i['name'], i['measurement_unit'])
