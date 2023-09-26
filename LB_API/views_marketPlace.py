from rest_framework import viewsets
from .serializer import BookSerializer, BookCategorySerializer, CommentsSerializer
from .models import Book, Comments, BookCategory
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response  
from rest_framework import status

class BookView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all() 
    
class BookCategoryView(viewsets.ModelViewSet):
    serializer_class = BookCategorySerializer
    queryset = BookCategory.objects.all() 
    
class CommentsView(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()

@api_view(['POST'])
def book_create(request):
    if request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def book_update(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
