import csv

from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Import users from CSV file'

    def handle(self, *args, **options):
        file_path = 'static/data/users.csv'
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                user = User(
                    id=row['id'], username=row['username'],
                    email=row['email'], role=row['role'],
                )
                user.save()
        self.stdout.write(self.style.SUCCESS('Users imported successfully'))
