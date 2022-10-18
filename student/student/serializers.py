
from dataclasses import field, fields
from .models import Payments, School
from rest_framework import serializers
import re


class Paymentserializers(serializers.ModelSerializer):
    
    class Meta:
        model = Payments
        fields = ['user', 'amount']



class Schoolserializers(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ['id', 'name', 'div']


    def validate_name(self, data):
                
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')


        if len(data)<3:
                
            raise serializers.ValidationError("name should be greater than three letters")
        if not regex.search(data) == None:
            raise serializers.ValidationError('name cannot contains any special characters')            

        return data