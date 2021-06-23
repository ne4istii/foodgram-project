from django.core.management.base import BaseCommand
from recipes.models import Ingredient
import csv


class Command(BaseCommand):
    help = 'Вносим предустановленные ингредиенты в базу'

    def handle(self, *args, **options):
        with open('recipes/data/ingredients.csv') as file:
            file_reader = csv.reader(file)
            for title, dimension in file_reader:
                Ingredient.objects.get_or_create(
                    title=title,
                    dimension=dimension
                )
