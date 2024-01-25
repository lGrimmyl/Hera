from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .models import IncidentReport
from .serializers import IncidentReportSerializer,ReadOnlyUserSerializer,PasswordChangeSerializer,CitizenUserCreateSerializer
from .permissions import IsPoliceStationUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
import json
from django.http import JsonResponse

from rest_framework.generics import RetrieveUpdateAPIView


class CreateUserView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Parse the JSON string from 'data' key in request.POST
        json_data = json.loads(request.POST.get('data'))
        
        # Combine the parsed JSON data with the file data in request.FILES
        combined_data = {**json_data, 'Valid_ID': request.FILES.get('Valid_ID'), 'UserValid': request.FILES.get('UserValid')}
        
        serializer = CitizenUserCreateSerializer(data=combined_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

class IncidentReportViewSet(viewsets.ModelViewSet):
    queryset = IncidentReport.objects.all()
    serializer_class = IncidentReportSerializer
    permission_classes = [IsPoliceStationUser]

class CustomUserView(RetrieveUpdateAPIView):
    serializer_class = ReadOnlyUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def post(self, request, *args, **kwargs):
        
        if 'change-password' in request.path:
            return self.change_password(request)
       

    def change_password(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({"message": "Password updated successfully."})