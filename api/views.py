from django.shortcuts import render
from .models import Metadata, Reports, Institutions
from .serializers import *
from rest_framework.generics import ListAPIView
from django.core.cache import cache
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class InstitutionsView(ListAPIView):
    queryset = Institutions.objects.all()
    serializer_class = InstitutionsSerializer
    permission_classes = [IsAuthenticated,]

    def list(self, request):
        institution_name = request.query_params.get('name', None)
        symbol = request.query_params.get('symbol', None)
        date = request.query_params.get('date', None)
        # cache_key = self.request.get_full_path()  # Define a unique cache key for this data
        cache_key = f'institution-trade:{institution_name}:{symbol}:{date}'
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
        
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset(institution_name,symbol,date)  # Query the database for the data
            print(result.values())  # Log the retrieved data (for debugging purposes)
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response
    
    def get_queryset(self,institution_name=None, symbol=None, date=None):
        queryset = super().get_queryset()
        # institution_name = self.request.query_params.get('name', None)
        # symbol = self.request.query_params.get('symbol', None)
        # date = self.request.query_params.get('date', None)
        if institution_name:
            queryset = queryset.filter(Q(top_sellers__contains=[{'name': institution_name}]) | 
                                       Q(top_buyers__contains=[{'name': institution_name}]))
        if symbol:
            queryset = queryset.filter(symbol__icontains=symbol)
        if date:
            queryset = queryset.filter(date=date)
        return queryset
    
class MetadataView(ListAPIView):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer
    permission_classes = [IsAuthenticated,]

    def list(self, request):
        slug_name = request.query_params.get('slug', None)
        sector_name = request.query_params.get('sector', None)
        id_sub = request.query_params.get('id', None)
        # cache_key = self.request.get_full_path()  # Define a unique cache key for this data
        cache_key = f'institution-trade:{slug_name}:{sector_name}:{id_sub}'
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
        
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset(slug_name,sector_name,id_sub)  # Query the database for the data
            print(result.values())  # Log the retrieved data (for debugging purposes)
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response
    
    def get_queryset(self, slug_name=None, sector_name=None, id_sub=None):
        queryset = super().get_queryset()
        # slug_name = self.request.query_params.get('slug', None)
        # sector_name = self.request.query_params.get('sector', None)
        # id_sub = self.request.query_params.get('id', None)
        if slug_name:
            slug_name_list = slug_name.split(',')
            queryset = queryset.filter(slug__in=slug_name_list)
        if sector_name:
            sector_name_list = sector_name.split(',')
            queryset = queryset.filter(sector__in=sector_name_list)
        if id_sub:
            id_sub_list = id_sub.split(',')
            queryset = queryset.filter(sub_sector_id__in=id_sub_list)
        return queryset

class ReportsView(ListAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer
    permission_classes = [IsAuthenticated,]

    def list(self, request):
        revenue_type = request.query_params.get('type', None)
        # cache_key = self.request.get_full_path()  # Define a unique cache key for this data
        cache_key = f'institution-trade:{revenue_type}'
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
        
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset(revenue_type)  # Query the database for the data
            print(result.values())  # Log the retrieved data (for debugging purposes)
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response
    
    def get_queryset(self,revenue_type=None):
        # revenue_type = self.request.query_params.get('type', None)
        if revenue_type == 'positive':
            queryset = queryset.filter(avg_yoy_q_revenue_growth__gt=0).order_by('-sub_sector')
        elif revenue_type == 'negatif':
            queryset = queryset.filter(avg_yoy_q_revenue_growth__lt=0).order_by('-sub_sector')
        return revenue_type
    
class ReportsCompaniesView(ListAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsCompaniesSerializer

    def list(self, request):
        cache_key = self.request.get_full_path() # Define a unique cache key for this data
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
        
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset()  # Query the database for the data
            print(result.values())  # Log the retrieved data (for debugging purposes)
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response

    def get_queryset(self):
        reports_companies= Reports.objects.filter(total_companies__range=(20,50))
        return reports_companies