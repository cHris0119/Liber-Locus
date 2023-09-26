from rest_framework import viewsets
from .serializer import BookSerializer
from .models import Book  
from .serializer import BookCategorySerializer  
from .serializer import CommentsSerializer
from .models import Comments 
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response  
from .models import Book  
from .models import BookCategory


class BookView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all() 
    
class BookCategoryView(viewsets.ModelViewSet):
    serializer_class = BookCategorySerializer
    queryset = BookCategory.objects.all() 
    
class CommentsView(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()