import csv
import os
from django.core.management.base import BaseCommand
from reviews.models import Genre, Category, Title, TitleGenre


class Command(BaseCommand):
    """Команда для импорта данных из CSV файлов по указанной
    директории в определённые модели"""

    def handle(self, *args, **kwargs):

        directory = os.path.join(
            os.path.dirname(__file__), '../../../static/data')
        os.chdir(directory)

        # Импорт данных в модель Genre
        with open(
            'genre.csv', mode='r', encoding='utf-8', newline=''
        ) as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                obj, created = Genre.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Добавлен жанр "{obj}"'))
                else:
                    self.stdout.write(f'Жанр "{obj}" уже существует!')

        # Импорт данных в модель Category
        with open(
            'category.csv', mode='r', encoding='utf-8', newline=''
        ) as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                obj, created = Category.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Добавлена категория "{obj}"'))
                else:
                    self.stdout.write(f'Категория "{obj}" уже существует!')

        # Импорт данных в модель Title
        with open(
            'titles.csv', mode='r', encoding='utf-8', newline=''
        ) as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                obj, created = Title.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(id=row['category'])
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Добавлено произведение "{obj}"'))
                else:
                    self.stdout.write(f'Произведение "{obj}" уже существует!')

        # Импорт данных в модель TitleGenre
        with open(
            'genre_title.csv', mode='r', encoding='utf-8', newline=''
        ) as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                obj, created = TitleGenre.objects.get_or_create(
                    id=row['id'],
                    genre=Genre.objects.get(id=row['genre_id']),
                    title=Title.objects.get(id=row['title_id'])
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Добавлена связь "{obj}"'))
                else:
                    self.stdout.write(f'Связь "{obj}" уже существует!')

        self.stdout.write(
            self.style.SUCCESS('Импорт данных из CSV файлов завершен.'))
