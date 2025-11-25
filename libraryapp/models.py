from django.db import models

# Create your models here.
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    isbn = models.CharField(max_length=20, unique=True)
    quantity = models.IntegerField(default=1)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Member(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class IssueRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} issued to {self.member.name}"
