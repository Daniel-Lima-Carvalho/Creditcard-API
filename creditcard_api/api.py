
import os
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from dotenv import load_dotenv
load_dotenv()

from rest_framework import serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from creditcard_api.models import Creditcard

from creditcard import CreditCard as CreditCardValidator

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 50
    authentication_classes = [TokenAuthentication]

class CreditcardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['exp_date', 'holder', 'number', 'cvv', 'brand', 'id']
        model = Creditcard
    
    def validate_holder(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("holder must have 2 or more characters")
        return value
    
    def validate_cvv(self, value):
        if len(str(value)) != 3 and len(str(value)) != 4:
            raise serializers.ValidationError("cvv must have 3 or 4 characters")
        return value

    def validate_number(self, value):
        cc = CreditCardValidator(value)
        if not cc.is_valid():
            raise serializers.ValidationError("card number is not valid")
        return value

class CreditcardViewSet(viewsets.ModelViewSet):
    queryset = Creditcard.objects.all()
    serializer_class = CreditcardSerializer
    pagination_class = StandardResultsSetPagination
    

    result = { 
        'success': True, 
        'message':'' 
    }

    def retrieve(self, request, pk=None):
        creditcard = Creditcard.objects.get(id=pk)
        creditcard.number = self.decrypt_number(creditcard.number)
        serializer = CreditcardSerializer(creditcard)
        return Response(serializer.data)

    def list(self, request):
        queryset = self.get_queryset()
        
        for cc in queryset:
            cc.number = self.decrypt_number(cc.number)
        
        serializer = CreditcardSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        
        error_validation_message = self.check_if_date_is_valid(data['exp_date'])
        if error_validation_message:
            self.result['success'] = False
            self.result['message'] = error_validation_message
            return Response(self.result, status=400)
        
        data['exp_date'] = self.transform_date_field(data['exp_date'])

        serializer = CreditcardSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        try:
            data['brand'] = self.get_brand(data['number'])
        except Exception as error_validation_message:
            self.result['success'] = False
            self.result['message'] = str(error_validation_message)
            return Response(self.result, status=400)
        
        data['number'] = self.encrypt_number(data['number'])

        serializer.create(data)
        self.result['message'] = 'Creditcard created successfully!'

        return Response(self.result, status=201)

    def get_brand(self, card_number):
        cc = CreditCardValidator(card_number)
        return cc.get_brand()

    def check_if_date_is_valid(self, date_text):
        try:
            input_date = datetime.strptime(date_text, '%m/%Y')
            today = datetime.now()
            self.check_if_date_is_lower_than_today(input_date, today)
        except Exception as error:
            return str(error)
    
    def check_if_date_is_lower_than_today(self, input_date, today):
        input_date = self.normalize_date(input_date)
        today = self.normalize_date(today)

        if input_date < today:
            raise Exception("exp_date can't be lower than today's date")
    
    def normalize_date(self, date):
        return date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    def transform_date_field(self, date_text):
        input_date = datetime.strptime(date_text, '%m/%Y')
        next_month = input_date.replace(day=28) + timedelta(days=4)
        new_date = next_month - timedelta(days=next_month.day)
     
        return new_date.strftime('%Y-%m-%d')

    def encrypt_number(self, number):
        key = os.environ.get("SECRET_KEY")
        fernet = Fernet(key.encode())
        encrypt_number = fernet.encrypt(number.encode())
        return encrypt_number.decode()

    def decrypt_number(self, number):
        key = os.environ.get("SECRET_KEY")
        fernet = Fernet(key.encode())
        encrypt_number = fernet.decrypt(number).decode()
        return encrypt_number
    

    