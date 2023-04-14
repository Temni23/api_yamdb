import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Import all data'

    def handle(self, *args, **options):
        os.system('python manage.py import_category')
        os.system('python manage.py import_genre')
        os.system('python manage.py import_title')
