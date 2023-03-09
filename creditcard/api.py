
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
    
    '''def validate_exp_date(self, value):
        if len(value) > 2 :
            raise serializers.ValidationError("exp_date is invalid")
        return value'''

    def validate_holder(self, value):
        if len(value) > 2 :
            raise serializers.ValidationError("holder is invalid")
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
    
    def check_if_date_is_valid(self, date_text):
        try:
            datetime.strptime(date_text, '%m/%Y')
        except Exception as error:
            return str(error)
            
    def create(self, request):
        data = request.data
        
        error_validation_message = self.check_if_date_is_valid(data['exp_date'])
        if error_validation_message:
            self.result['success'] = False
            self.result['message'] = error_validation_message
            return Response(self.result, status=400)

        