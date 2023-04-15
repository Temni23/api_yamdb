import csv

from django.core.management.base import BaseCommand

from reviews.models import Review, Comment
from users.models import User


class Command(BaseCommand):
    help = 'Import comments from CSV file'

    def handle(self, *args, **options):
        file_path = 'static/data/comments.csv'
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                comment = Comment(
                    id=row['id'],
                    review=Review.objects.get(id=row['review_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    pub_date=row['pub_date']
                )
                comment.save()
        self.stdout.write(self.style.SUCCESS('Comments imported successfully'))
