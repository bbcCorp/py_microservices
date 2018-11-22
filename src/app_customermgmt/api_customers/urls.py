from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api_customers import views, views_advanced

urlpatterns = [
    path('customers/', views_advanced.CustomerList.as_view()),
    path('customers/<int:pk>/', views_advanced.CustomerDetails.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)