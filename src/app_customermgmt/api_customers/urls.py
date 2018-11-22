from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api_customers import views

urlpatterns = [
    path('customers/', views.CustomerList.as_view()),
    path('customers/<int:pk>/', views.CustomerDetails.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)