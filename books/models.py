from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    biography = models.TextField()
    publisher = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    isbn = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    genre = models.CharField(max_length=100)
    publisher = models.CharField(max_length=150)
    year_published = models.IntegerField()
    copies_sold = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return self.name
