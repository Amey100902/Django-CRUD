from django.contrib import admin
from django.conf import settings 
from django.conf.urls.static import static
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home , name='home'),
    path('morejob/', views.bojerom, name='morejob'),
    path('logout/', views.logout_user , name='logout_user'),
    path('register/',views.register,name='register'),
    path('record/<int:pk>', views.customer_record , name='customer_record'),
    path('delete_record/<int:pk>',views.delete_record,name='delete_record'),
    path('add_record/',views.add_record,name='add_record'),
    path('update_record/<int:pk>',views.update_record,name='update_record'),
   
]
