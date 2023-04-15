import csv

from django.core.management.base import BaseCommand

from reviews.models import Genre


class Command(BaseCommand):
    help = 'Import genres from CSV file'

    def handle(self, *args, **options):
        file_path = 'static/data/genre.csv'
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                genre = Genre(id=row['id'], name=row['name'], slug=row['slug'])
                genre.save()
        self.stdout.write(self.style.SUCCESS('Genres imported successfully'))
