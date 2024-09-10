from .views import *
from django.urls import path

urlpatterns = [
    # path('', InstitutionsView.as_view(), name='get-institution-trade'),
    path('get-institution-trade', InstitutionsView.as_view(), name='get-institution-trade'),
    path('get-metadata-trade', MetadataView.as_view(), name='get-metadata-trade'),
    path('get-reports-trade', ReportsView.as_view(), name='get-reports-trade'),
    path('get-reports-companies-trade', ReportsCompaniesView.as_view(), name='get-reports-companies-trade'),
]