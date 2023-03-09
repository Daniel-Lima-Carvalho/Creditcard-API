
from datetime import datetime

from django.http import JsonResponse

from rest_framework import serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework.response import Response


from creditcard.models import Creditcard

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 50

class CreditcardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['exp_date', 'holder', 'number', 'cvv']
        model = Creditcard

class CreditcardViewSet(viewsets.ModelViewSet):
    queryset = Creditcard.objects.all()
    serializer_class = CreditcardSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    result = { 
        'success': True, 
        'message':'' 
    }

    def normalize_date(self, date):
        return date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    def check_if_date_is_lower_than_today(self, input_date, today):
        input_date = self.normalize_date(input_date)
        today = self.normalize_date(today)

        if input_date < today:
            raise Exception("exp_date can't be lower than today's date")


    def check_if_date_is_valid(self, date_text):
        try:
            input_date = datetime.strptime(date_text, '%m/%Y')
            today = datetime.now()
            self.check_if_date_is_lower_than_today(input_date, today)
        except Exception as error:
            return str(error)
            
    def create(self, request):
        data = request.data
        
        error_validation_message = self.check_if_date_is_valid(data['exp_date'])
        if error_validation_message:
            self.result['success'] = False
            self.result['message'] = error_validation_message
            return Response(self.result, status=400)