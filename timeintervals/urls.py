from django.urls import path
from .views import Home,process_list, process_add, process_edit,process_list1, process_add1, process_edit1,process_full,process_edit2,compare_process_view
from .import views
urlpatterns = [
    path('standard/', process_list, name='process_list'),
    path('standard/add/', process_add, name='process_add'),
    path('standard/edit/<int:pk>/', process_edit, name='process_edit'),
    path('sample/list/', process_list1, name='process_list1'),
    path('sample/add/', process_add1, name='process_add1'),
    path('sample/edit/<int:pk>/', process_edit1, name='process_edit1'),
    path('sample/full/',process_full, name='process_full'),
    path('sample/status/<int:pk>/', process_edit2, name='process_edit2'),
    path('result/',compare_process_view,name='analysis'),
    path('home/',Home,name='home' ),
    path('superuser/UserRegister/', views.signup_view, name='signup'),
    path('user/login/', views.login_view, name='loginu'),
    path('superuser/login/', views.login1_view, name='login'),
    path('', views.button_page, name='button_page'),
]
