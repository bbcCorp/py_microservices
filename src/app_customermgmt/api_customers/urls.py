from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view

from api_customers import views, views_advanced

schema_view = get_schema_view(title='Customers API')

urlpatterns = [
    path('customers/', views_advanced.CustomerList.as_view()),
    path('customers/<int:pk>/', views_advanced.CustomerDetails.as_view()),
    path('schema/', schema_view),
]

urlpatterns = format_suffix_patterns(urlpatterns)