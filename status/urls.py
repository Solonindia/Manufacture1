from django.urls import path
from .views import process_list1, process_add1, process_edit1,process_full,process_edit2

urlpatterns = [
    path('', process_list1),
    path('add/', process_add1),
    path('edit1/<int:pk>/', process_edit1),
    path('full/',process_full),
    path('edit2/<int:pk>/', process_edit2),
]
