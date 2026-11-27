from django.db import models
from django.utils import timezone

class Student(models.Model):
    std_id = models.CharField(max_length=20, unique=True)
    std_name = models.CharField(max_length=100)
    std_dept = models.CharField(max_length=100)
    std_email = models.CharField(max_length=150, unique=True)
    unpaid_fines = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.std_id} - {self.std_name}"

class Librarian(models.Model):
    librarian_id = models.CharField(max_length=20, unique=True)
    librarian_name = models.CharField(max_length=100)
    librarian_email = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.librarian_name

class Book(models.Model):
    book_tag = models.CharField(max_length=50, unique=True)
    book_name = models.CharField(max_length=200)
    book_category = models.CharField(max_length=100)
    book_author = models.CharField(max_length=150)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.book_name} ({self.book_tag})"

class BorrowTransaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    librarian = models.ForeignKey(Librarian, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    late_fee = models.IntegerField(default=0)

    def can_checkout(self):
        has_overdue = BorrowTransaction.objects.filter(
            student=self.student,
            return_date__isnull=True,
            due_date__lt=timezone.now().date()
        ).exists()
        return self.student.unpaid_fines == 0 and not has_overdue and self.book.is_available

    def process_return(self, daily_rate=20):
        self.return_date = timezone.now().date()
        if self.return_date > self.due_date:
            overdue_days = (self.return_date - self.due_date).days
            self.late_fee = overdue_days * daily_rate
            self.student.unpaid_fines += self.late_fee
            self.student.save()
        self.book.is_available = True
        self.book.save()
        self.save()

    def __str__(self):
        return f"{self.student.std_name} borrowed {self.book.book_name}"