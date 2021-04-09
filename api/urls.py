from django.urls import path
from api.views import CompanyEmployee, PeopleInfo, Relations, CompanyEmployeeWithoutPagination

urlpatterns = [
    path('companies/<int:pk>/employees/', CompanyEmployee.as_view()),
    path('companies/<int:pk>/all_employees/', CompanyEmployeeWithoutPagination.as_view()),
    path('relations/<int:id1>/<int:id2>/', Relations.as_view()),
    path('people/<str:pk>/', PeopleInfo.as_view()),
]
