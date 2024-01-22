from django.db import models
import uuid
import datetime  
from user.models import User

# Create your models here.
BOOK_GENRE = [
        ("fiction", "Fiction"),
        ("novel", "Novel"),
        ("fantasy", "Fantasy"),
        ("horror", "Horror"),
        ("history", "History")  
        ]

class Book(models.Model):
    name = models.CharField(max_length=80,unique=True)
    book_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    author = models.CharField(max_length=80)
    book_genre = models.CharField(choices=BOOK_GENRE, max_length=15, default='fiction')
    price = models.IntegerField()
    book_count = models.IntegerField()
    book_issue_date = models.DateField()
    book_status = models.BooleanField(default=True)

    def __str__(self):
        return "{}   -   {}".format(self.name,self.author)


class Booklog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_holder')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_taken')
    issue_date = models.DateTimeField(blank=True, default=None)
    due_date = models.DateField(null=True, blank=True, default=None)
    return_date = models.DateField(blank=True, null=True)
    total_fine = models.CharField(default=0)

    def __str__(self):
        return "{}-{}".format(self.user,self.book)
    