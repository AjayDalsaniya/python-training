from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
class BookRetriveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):  
    queryset = Book.objects.all()
    serializer_class = BookSerializer
     
    

"""
@api_view(['GET'])
def getallUserData(request):
    user =UserInfo.objects.all()
    if user:
        userSerializer = UserSerializer(user,many=True)
        return Response(userSerializer.data)
        """
