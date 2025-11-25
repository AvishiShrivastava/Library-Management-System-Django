from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Book, Member, IssueRecord

admin.site.register(Book)
admin.site.register(Member)
admin.site.register(IssueRecord)

