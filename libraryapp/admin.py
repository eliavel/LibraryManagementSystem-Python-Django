from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, Librarian, Book, BorrowTransaction

# Register your models here so they appear in the Admin Dashboard
admin.site.register(Student)
admin.site.register(Librarian)
admin.site.register(Book)
admin.site.register(BorrowTransaction)