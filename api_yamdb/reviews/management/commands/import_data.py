import csv
import os
from django.core.management.base import BaseCommand
from reviews.models import Genre, Category, Title, TitleGenre, Review, Comment
from users.models import CustomUser


class Command(BaseCommand):
    """Команда для импорта данных из CSV файлов по указанной
    директории в определённые модели"""

    def handle(self, *args, **kwargs):
        try:
            directory = os.path.join(
                os.path.dirname(__file__), '../../../static/data')
            os.chdir(directory)

            self.import_data('genre.csv', self.import_genre)
            self.import_data('category.csv', self.import_category)
            self.import_data('titles.csv', self.import_title)
            self.import_data('genre_title.csv', self.import_title_genre)
            self.import_data('users.csv', self.import_user)
            self.import_data('review.csv', self.import_review)
            self.import_data('comments.csv', self.import_comment)

            self.stdout.write(
                self.style.SUCCESS('Импорт данных из CSV файлов завершен.'))

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Произошла ошибка при импорте данных: {e}'))

    def import_data(self, file_name, import_function):
        """Общий метод для импорта данных из CSV файла"""
        with open(
                file_name, mode='r', encoding='utf-8', newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                import_function(row)

    def import_genre(self, row):
        """Импорт данных в модель Genre"""
        obj, created = Genre.objects.get_or_create(
            id=row['id'],
            name=row['name'],
            slug=row['slug']
        )
        self.log_result(obj, created, 'жанр')

    def import_category(self, row):
        """Импорт данных в модель Category"""
        obj, created = Category.objects.get_or_create(
            id=row['id'],
            name=row['name'],
            slug=row['slug']
        )
        self.log_result(obj, created, 'категория')

    def import_title(self, row):
        """Импорт данных в модель Title"""
        obj, created = Title.objects.get_or_create(
            id=row['id'],
            name=row['name'],
            year=row['year'],
            category=Category.objects.get(id=row['category'])
        )
        self.log_result(obj, created, 'произведение')

    def import_title_genre(self, row):
        """Импорт данных в модель TitleGenre"""
        obj, created = TitleGenre.objects.get_or_create(
            id=row['id'],
            genre=Genre.objects.get(id=row['genre_id']),
            title=Title.objects.get(id=row['title_id'])
        )
        self.log_result(obj, created, 'связь')

    def import_user(self, row):
        """Импорт данных в модель CustomUser"""
        obj, created = CustomUser.objects.get_or_create(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            role=row['role'],
            bio=row['bio'],
            first_name=row['first_name'],
            last_name=row['last_name']
        )
        self.log_result(obj, created, 'пользователь')

    def import_review(self, row):
        """Импорт данных в модель Review"""
        obj, created = Review.objects.get_or_create(
            id=row['id'],
            title=Title.objects.get(id=row['title_id']),
            text=row['text'],
            author=CustomUser.objects.get(id=row['author']),
            score=row['score'],
            pub_date=row['pub_date']
        )
        self.log_result(obj, created, 'отзыв')

    def import_comment(self, row):
        """Импорт данных в модель Comment"""
        obj, created = Comment.objects.get_or_create(
            id=row['id'],
            review=Review.objects.get(id=row['review_id']),
            text=row['text'],
            author=CustomUser.objects.get(id=row['author']),
            pub_date=row['pub_date']
        )
        self.log_result(obj, created, 'комментарий')

    def log_result(self, obj, created, model_name):
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Добавлен {model_name} "{obj}"'))
        else:
            self.stdout.write(
                f'{model_name.capitalize()} "{obj}" уже существует!')
