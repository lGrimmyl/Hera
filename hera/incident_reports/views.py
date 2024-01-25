from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from accounts.permissions import IsPoliceStationUser
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import generics
from .models import IncidentReport, Suspect, Victim, ChildConflict, Notification, IncidentSubcategory
from .serializers import IncidentReportSerializer, SuspectSerializer, VictimSerializer, ChildConflictSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser,JSONParser

class DailyReportCountView(APIView):
    permission_classes = [IsAuthenticated, IsPoliceStationUser]

    def get(self, request, format=None):
        today = timezone.now().date()
        count = IncidentReport.objects.filter(datetime_reported__date=today).count()
        return Response({"daily_report_count": count})

class ReportsNeedingResponseView(APIView):
    permission_classes = [IsAuthenticated, IsPoliceStationUser]

    def get(self, request, format=None):
        count = IncidentReport.objects.filter(status = 'Open').count()
        return Response({"reports_needing_response": count})

class ResolvedReportsCountView(APIView):
    permission_classes = [IsAuthenticated, IsPoliceStationUser]

    def get(self, request, format=None):
        count = IncidentReport.objects.filter(status='Closed').count()
        return Response({"resolved_reports_count": count})
    
class EmergencyReportCountView(APIView):
    permission_classes = [IsAuthenticated, IsPoliceStationUser]

    def get(self, request):
        # Count only if the user is a police station user
        if request.user.is_authenticated and request.user.is_police_station:
            emergency_count = IncidentReport.objects.filter(is_emergency=True).count()
            return Response({"emergency_report_count": emergency_count})
        else:
            return Response({"error": "Unauthorized"}, status=403)
        
class CombinedReportMetricsView(APIView):
    permission_classes = [IsAuthenticated, IsPoliceStationUser]

    def get(self, request, format=None):
        today = timezone.now().date()

        daily_count = IncidentReport.objects.filter(datetime_reported__date=today).count()
        needing_response_count = IncidentReport.objects.filter(status='Open').count()
        resolved_count = IncidentReport.objects.filter(status='Closed').count()
        emergency_count = IncidentReport.objects.filter(is_emergency=True).count()

        return Response({
            "daily_report_count": daily_count,
            "reports_needing_response_count": needing_response_count,
            "resolved_reports_count": resolved_count,
            "emergency_report_count": emergency_count
        })









class ReportListView(generics.ListAPIView):
    serializer_class = IncidentReportSerializer
    def get_queryset(self):
        user = self.request.user
        queryset = IncidentReport.objects.all()

        if user.is_authenticated:
            # Filter for police station user or regular user
            if not user.is_police_station:
                queryset = queryset.filter(user=user)

            # Check for 'is_emergency' query parameter
            is_emergency = self.request.query_params.get('is_emergency')
            if is_emergency is not None:
                is_emergency = is_emergency.lower() == 'true'
                queryset = queryset.filter(is_emergency=is_emergency)

        else:
            queryset = IncidentReport.objects.none()

        return queryset
    
class ReportCreateView(generics.CreateAPIView):
    queryset = IncidentReport.objects.all()
    serializer_class = IncidentReportSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, JSONParser)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        Notification.objects.create(
            recipient=self.request.user,
            title="Report Submission Successful",
            message="Your report has been successfully submitted and is now being processed.",
            read=False  # Default value is False, but explicitly stating for clarity
        )
class ReportDetailView(generics.RetrieveAPIView):
    serializer_class = IncidentReportSerializer
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_police_station:
                return IncidentReport.objects.all()
            else:
                return IncidentReport.objects.filter(user=user)
        return IncidentReport.objects.none()
    

class ReportSuspectCreateView(generics.CreateAPIView):
    queryset = Suspect.objects.all()
    serializer_class = SuspectSerializer

class ReportVictimCreateView(generics.CreateAPIView):
    queryset = Victim.objects.all()
    serializer_class = VictimSerializer

class ReportChildConflictCreateView(generics.CreateAPIView):
    queryset = ChildConflict.objects.all()
    serializer_class = ChildConflictSerializer



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_emergency_report(request):
    user = request.user
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')

    is_emergency = request.data.get('is_emergency', False)
    if is_emergency:
        try:
            emergency_subcategory = IncidentSubcategory.objects.get(id=9)
        except IncidentSubcategory.DoesNotExist:
            return Response({'error': 'Emergency subcategory not found'}, status=404)
    
    # Create the emergency report
    report = IncidentReport.objects.create(
        user=user,
        is_emergency=True,
        latitude=latitude,
        longitude=longitude,
    )
    report.subcategories.set([emergency_subcategory])
    # Additional logic (e.g., notifying the nearest police station)
    
    return Response({'message': 'Emergency report created successfully', 'report_id': report.id})

class EmergencyReportList(APIView):
    def get(self, request):
        reports = IncidentReport.objects.filter(is_emergency=True)
        serializer = IncidentReportSerializer(reports, many=True)
        return Response(serializer.data)


    


@api_view(['PATCH'])
@permission_classes([IsPoliceStationUser])
def update_report_status(request, report_id):

    try:
        report = IncidentReport.objects.get(id=report_id)
    except IncidentReport.DoesNotExist:
        return Response({'error': 'Incident report not found'}, status=404)


    new_status = request.data.get('status')
    if new_status in dict(IncidentReport.STATUS_CHOICES):
        report.status = new_status
        report.save()
       
        Notification.objects.create(
            recipient=report.user,
            title='Incident Report Status Updated',
            message=f'Your incident report status has been updated to {report.get_status_display()}.'
        )
        return Response({'message': 'Report status updated successfully'})
    else:

        return Response({'error': 'Invalid status'}, status=400)
    
@api_view(['GET'])    
@permission_classes([IsAuthenticated])
def get_user_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return Response({'notifications': [{'title': n.title, 'message': n.message, 'read': n.read, 'created_at': n.created_at} for n in notifications]})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.read = True
        notification.save()
        return Response({'status': 'success'})
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=404)