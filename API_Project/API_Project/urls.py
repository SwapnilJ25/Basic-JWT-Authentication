
from django.contrib import admin
from django.urls import path
from Restapi.views import LoginAPIView,TokenRefreshAPIView
from fetch_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', LoginAPIView.as_view(), name='login'),
    path('refreshtoken/', TokenRefreshAPIView.as_view(), name='login'),
    path('login/', views.login_and_store_tokens, name='fetch'),
    path('show/', views.show, name='show')
]
