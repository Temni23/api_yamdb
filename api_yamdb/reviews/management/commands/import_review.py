import csv

from django.core.management.base import BaseCommand

from reviews.models import Review, Title
from users.models import User


class Command(BaseCommand):
    help = 'Import reviews from CSV file'

    def handle(self, *args, **options):
        file_path = 'static/data/review.csv'
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                review = Review(
                    id=row['id'],
                    title=Title.objects.get(id=row['title_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date']
                )
                review.save()
        self.stdout.write(self.style.SUCCESS('Reviews imported successfully'))
