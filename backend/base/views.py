from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status


from .models import Product
from .products import products
from .serializers import ProductSerializer, UserSerializer, UserSerializerWithToken

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  def validate(self, attrs):

    data = super().validate(attrs)
    
    serializer = UserSerializerWithToken(self.user).data

    for k, v in serializer.items():
      data[k] = v

    return data 
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Create your views here.
# REGISTER THE USER

@api_view(['POST'])
def registerUser(request):
  data = request.data

  try:
    user = User.objects.create(
      first_name=data['name'],
      username=data['email'],
      email = data['email'],
      password = make_password(data['password'])
    )
    serializer = UserSerializerWithToken(user, many = False)
    return Response(serializer.data) 
  
  except:
    message = {"detail" : "User with this email already exists"}
    return Response(message, status=status.HTTP_400_BAD_REQUEST)


#UPDATING USER DATA
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
  user = request.user
  serializer = UserSerializerWithToken(user, many=False)

  data = request.data

  user.first_name = data['name']
  user.username = data['email']
  user.email = data['email']

  if data['password'] != '':
    user.password = make_password(data['password'])

  user.save()


  return Response(serializer.data) 

#User
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
  user = request.user
  serializer = UserSerializer(user, many=False)
  return Response(serializer.data)

#GETTING USERS
@api_view(['GET'])
@permission_classes([IsAdminUser])

def getUsers(request):
  users = User.objects.all()
  serializer = UserSerializer(users, many=True)
  return Response(serializer.data)

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