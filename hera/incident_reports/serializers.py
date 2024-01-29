from django.db import transaction
from rest_framework import serializers
from .models import IncidentReport, Suspect, Victim, ChildConflict, IncidentSubcategory,IncidentCategory
import filetype
import json
from google.cloud import storage
from django.conf import settings
from datetime import datetime, timedelta


class SuspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suspect
        exclude = ('incident_report',)

class VictimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Victim
        exclude = ('incident_report',)

class ChildConflictSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildConflict
        exclude = ('incident_report',)

class IncidentReportSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        from accounts.serializers import ReadOnlyUserSerializer
        super().__init__(*args, **kwargs)
        self.fields['user'] = ReadOnlyUserSerializer(read_only=False, required=False)
    suspects = SuspectSerializer(many=True, read_only=False, required=False)
    victims = VictimSerializer(many=True, read_only=False, required=False)
    child_conflicts = ChildConflictSerializer(many=True, read_only=False, required=False)
    media_url = serializers.SerializerMethodField()
    main_category = serializers.SerializerMethodField()
    subcategories = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=IncidentSubcategory.objects.all(),
        required=False
    )
    jsonData = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = IncidentReport
        fields = ['user','is_user_victim','status','id', 'media','media_url', 'description', 'datetime_reported','closed_at','longitude','latitude', 'narrative','main_category','subcategories', 'suspects', 'victims', 'child_conflicts', 'jsonData']
        extra_kwargs = {
            'media': {'required': False}
        }
    def validate_media(self, value):
    
        file_type = filetype.guess(value)

        if not file_type:
            raise serializers.ValidationError("Cannot determine file type.")

    
        allowed_types = ['image/jpeg', 'image/png', 'video/mp4']
        if file_type.mime not in allowed_types:
            raise serializers.ValidationError("Unsupported file type.")

    # File size validation remains the same
        max_file_size = 10 * 1024 * 1024  # 10 MB
        if value.size > max_file_size:
            raise serializers.ValidationError("File too large. Size should not exceed 10 MB.")

        return value
    def create(self, validated_data):
        jsonData = validated_data.pop('jsonData', None)
        if jsonData:
            additional_data = json.loads(jsonData)
            # Process your additional JSON data here. For example, merge it into validated_data
            validated_data.update(additional_data)
        with transaction.atomic():
            subcategories_data = validated_data.pop('subcategories', [])
            suspects_data = validated_data.pop('suspects', [])
            victims_data = validated_data.pop('victims', [])
            child_conflicts_data = validated_data.pop('child_conflicts', [])
        
            incident_report = IncidentReport.objects.create(**validated_data)

            incident_report.subcategories.set(subcategories_data)

            for suspect_data in suspects_data:
                Suspect.objects.create(incident_report=incident_report, **suspect_data)
            for victim_data in victims_data:
                Victim.objects.create(incident_report=incident_report, **victim_data)
            for child_conflict_data in child_conflicts_data:
                ChildConflict.objects.create(incident_report=incident_report, **child_conflict_data)

            return incident_report
        
    def get_media_url(self, obj):
        if obj.media:  
            
            storage_client = storage.Client(credentials=settings.GCS_CREDENTIALS)
            bucket = storage_client.bucket(settings.GS_BUCKET_NAME)
            blob = bucket.blob(obj.media.name)

            expiration_time = datetime.utcnow() + timedelta(hours=1)
            signed_url = blob.generate_signed_url(expiration=expiration_time)
            return signed_url
        return None

    def get_main_category(self, obj):
        categories = set()
        for subcategory in obj.subcategories.all():
            if subcategory.category:
                categories.add(subcategory.category.name)
        return list(categories)