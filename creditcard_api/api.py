
from datetime import datetime, timedelta

from rest_framework import serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework.response import Response

from creditcard_api.models import Creditcard

from creditcard import CreditCard as CreditCardValidator

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 50

class CreditcardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['exp_date', 'holder', 'number', 'cvv']
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
    permission_classes = [permissions.IsAuthenticated]
    result = { 
        'success': True, 
        'message':'' 
    }

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
        
        serializer.create(data)
        self.result['message'] = 'Creditcard created successfully!'

        return Response(self.result, status=201)

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
    