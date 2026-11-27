from django.shortcuts import render
from .models import Book

def home_view(request):
    # Extract all books from the SQLite database
    all_books = Book.objects.all()
    
    # Package the books into a dictionary to send to the HTML file
    context = {
        'books': all_books
    }
    
    # Render the catalog page using the context
    return render(request, 'libraryapp/catalog.html', context)