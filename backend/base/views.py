from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

from .models import Product
from .products import products
from .serializers import ProductSerializer

# Create your views here.
@api_view(['GET'])
def getRoutes(request):
  return Response('Hello')

#PRODUCTS
@api_view(['GET'])
def getProducts(request):
  products = Product.objects.all()
  serializer = ProductSerializer(products, many=True)
  return Response(serializer.data)

#PRODUCT
@api_view(['GET'])
def getProduct(request, pk):
  product = Product.objects.get(_id=pk)
  serializer = ProductSerializer(product, many=False)
  # for i in products:
  #   if i['_id'] == pk:
  #     product = i
  return Response(serializer.data)