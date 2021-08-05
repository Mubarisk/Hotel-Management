from django.urls import path,include
from . import views
urlpatterns=[
   path('login/',views.login_view,name='login'),
   path('register',views.register_view,name='register'),
   path('forgot_password',views.forgot,name='forgot'),
   path('reset_password/<str:mail>/',views.reset,name='reset-password'),
]