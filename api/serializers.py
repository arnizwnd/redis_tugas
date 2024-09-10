from rest_framework import serializers
from .models import *

class InstitutionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institutions
        fields = '__all__'
        # fields = ['symbol', 'top_sellers']

class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = '__all__'

class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = '__all__'

class ReportsCompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = ['sub_sector','total_companies']