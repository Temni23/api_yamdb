import csv

from django.core.management.base import BaseCommand

from reviews.models import Title, Genre, Category


class Command(BaseCommand):
    help = 'Import titles from CSV file'

    def handle(self, *args, **options):
        titles_file_path = 'static/data/titles.csv'
        with open(titles_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                title = Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(id=row['category'])
                )
                title.save()

        # Заполнение таблицы для поля genre(ManyToManyField)
        genre_title_file_path = 'static/data/genre_title.csv'
        with open(genre_title_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                title.genre.add(genre)

        self.stdout.write(self.style.SUCCESS('Titles imported successfully'))
