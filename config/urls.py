from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


#Added url condconfigurations for our Api and Authentications
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('vendor_api.urls')),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),    
]
