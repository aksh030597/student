from modulefinder import IMPORT_NAME
import re
from urllib import response
from urllib import request
from urllib.request import Request
from django.http import JsonResponse
from .models import School, Payments
from .serializers import Paymentserializers, Schoolserializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from student import serializers
from django.db import transaction


@api_view(['GET', 'POST'])
def emp_list(request):
    if request.method == 'GET':
        emp = School.objects.all()
        serializer = Schoolserializers(emp, many=True)
        return Response({'emp': serializer.data})

    if request.method == 'POST':
      
        serializer = Schoolserializers(data=request.data)
      
        if serializer.is_valid()==True:
            serializer.save()
            messages.success(request, "record added successfully!!!")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def std_detail(request, id):

    try:
        emp= School.objects.get(pk=id)
    except School.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializers = Schoolserializers(emp)
        return Response(serializers.data)

    elif request.method == 'PUT':
        serializers = Schoolserializers(emp, data=request.data)
    
        if serializers.is_valid()==True:
            serializers.save()
            messages.success(request, "record added successfully!!!")
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method=='DELETE':
        emp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def api_portal(request):
    return Response({
        "message" :"this is an API portal of student",
        "admin link": "  http://127.0.0.1:8000/admin/  ",
        "student api link": "  http://127.0.0.1:8000/student/  ",
        "users detail": "http://127.0.0.1:8000/send/ "
        })

@api_view(['POST', 'GET'])
def transaction(request):
    if request.method=='POST':
        try:
            user_one = request.POST.get('user_one')
            user_two = request.POST.get('user_two')
            amount = int(request.POST.get('amount'))
            with transaction.atomic():
                user_one_payment_obj = Payments.objects.get(user = user_one)

                user_one_payment_obj.amount -= amount
                user_one_payment_obj.save()

                user_two_payment_obj = Payments.objects.get(user = user_two)

                user_two_payment_obj.amount += amount
                user_two_payment_obj.save()


            messages.success(request,'Amount transferred successfully')
        except Exception as e:
            print(e)
            messages.success(request, 'something went wrong')



    if request.method == 'GET':
        user = Payments.objects.all()
        serializer = Paymentserializers(user, many=True)
        return Response({ 'detail' : serializer.data })
