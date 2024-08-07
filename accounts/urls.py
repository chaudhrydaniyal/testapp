from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from accounts import views
router = routers.DefaultRouter()
router.register(r'register', views.RegisterViewset, 'register')

urlpatterns = [
    path("", include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token-verify/', TokenVerifyView.as_view(), name='token_verify'),

]
