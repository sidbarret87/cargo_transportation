import csv
from django.core.management import BaseCommand
from cargos.models import Location

class Command(BaseCommand):
    help = 'Загружает данные из файла uszips.csv'
    def handle(self, *args, **options):
        with open('uszips.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Location.objects.create(
                    city = row['city'],
                    state_id = row['state_id'],
                    state_name= row['state_name'],
                    zip_code =row['zip'],
                    latitude =row['lat'],
                    longitude = row['lng']

                )
