from client.models import SubMaterials
from django.core.management.base import BaseCommand
from pathlib import Path

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

        # Since the CSV headers match the model fields,
        # you only need to provide the file's path (or a Python file object)
        file = open(str(BASE_DIR) + '/megastroy/floor_coverings/dataset/laminats.csv', encoding="utf8")
        insert_count = SubMaterials.objects.from_csv(file)
        print("{} records inserted".format(insert_count))
