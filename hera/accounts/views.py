from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .models import IncidentReport
from .serializers import IncidentReportSerializer,ReadOnlyUserSerializer,PasswordChangeSerializer
from .permissions import IsPoliceStationUser
from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import RetrieveUpdateAPIView

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