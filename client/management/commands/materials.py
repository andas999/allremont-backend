from client.models import Materials
from django.core.management.base import BaseCommand
from pathlib import Path

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        # print(BASE_DIR)

        # Since the CSV headers match the model fields,
        # you only need to provide the file's path (or a Python file object)
        insert_count = Materials.objects.from_csv(str(BASE_DIR) + '/megastroy/floor_coverings/floor_coverings/dataset/materials.csv')
        print("{} records inserted".format(insert_count))