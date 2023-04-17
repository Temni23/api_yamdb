import csv

from django.core.management.base import BaseCommand

from reviews.models import Category


class Command(BaseCommand):
    help = 'Import categories from CSV file'

    def handle(self, *args, **options):
        file_path = 'static/data/category.csv'
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                category = Category(id=row['id'], name=row['name'],
                                    slug=row['slug'])
                category.save()
        self.stdout.write(
            self.style.SUCCESS('Categories imported successfully'))
