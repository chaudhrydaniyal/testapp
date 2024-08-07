"""
URL configuration for wesal_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static
router = DefaultRouter()

# router.register(r'projects', ProjectViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),

    # path('api/login/', TokenObtainPairView.as_view(serializer_class=CustomJWTSerializer), name='token_obtain_pair'),
    # # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(serializer_class=CustomTokenVerifySerializer), name='token_verify'),

    # path('api/token/', CustomObtainTokenView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    # path('api/register/user/', user_registration_view, name='user_registration'),
    # path('api/logout/', LogoutView.as_view(), name='logout'),
    # path('api/user-file/', UserFileView.as_view(), name='user-file'),



    path('', include(router.urls)),

    
    # path('api/', include('topicals.urls')),
    path('api/', include('accounts.urls')),
    path('api/', include('control.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)