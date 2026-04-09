import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geektext.settings')
django.setup()

from books.models import Author, Book

Book.objects.all().delete()
Author.objects.all().delete()

a1 = Author.objects.create(first_name="John", last_name="Smith", biography="Fantasy author", publisher="Penguin")
a2 = Author.objects.create(first_name="Sarah", last_name="Lee", biography="Tech writer", publisher="O'Reilly")
a3 = Author.objects.create(first_name="Mike", last_name="Johnson", biography="Sci-fi expert", publisher="HarperCollins")

Book.objects.create(isbn="978000000001", name="Dragon Moon", description="Fantasy adventure", price=19.99, genre="Fantasy", publisher="Penguin", year_published=2021, copies_sold=1200, rating=4.5, author=a1)
Book.objects.create(isbn="978000000002", name="Shadow Realm", description="Dark fantasy", price=18.99, genre="Fantasy", publisher="Penguin", year_published=2020, copies_sold=900, rating=4.2, author=a1)
Book.objects.create(isbn="978000000003", name="Python for Beginners", description="Learn Python", price=29.99, genre="Education", publisher="O'Reilly", year_published=2020, copies_sold=500, rating=4.0, author=a2)
Book.objects.create(isbn="978000000004", name="Advanced Python", description="Deep Python", price=39.99, genre="Education", publisher="O'Reilly", year_published=2022, copies_sold=800, rating=4.7, author=a2)
Book.objects.create(isbn="978000000005", name="Space Odyssey", description="Sci-fi", price=24.99, genre="Sci-Fi", publisher="HarperCollins", year_published=2019, copies_sold=1500, rating=4.8, author=a3)
Book.objects.create(isbn="978000000006", name="AI Revolution", description="AI future", price=34.99, genre="Tech", publisher="MIT Press", year_published=2023, copies_sold=1100, rating=4.6, author=a3)

print("🔥 Sample books inserted successfully!")