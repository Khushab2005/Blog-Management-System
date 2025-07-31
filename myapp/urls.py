from django.urls import path
from myapp.views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout, name='logout'),
    path('thank_you/', thank_you, name='thank_you'),
    path('updateblog/<int:id>/', updateblog, name='updateblog'),
    path('deleteblog/<int:id>/', deleteblog, name='deleteblog'),
]