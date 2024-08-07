from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from control import views
router = routers.DefaultRouter()
router.register(r'passages', views.PassagesViewSet, 'passages')
router.register(r'topics', views.TopicViewSet, 'topics')
router.register(r'sources', views.SourceViewSet, 'sources')
router.register(r'documents', views.DocumentViewSet, 'documents')
router.register(r'accessability', views.AccessabilityViewSet, 'accessability')
router.register(r'accessabilities-delete',
                views.AccessabilitiesViewSet, 'accessabilities-delete')

urlpatterns = [
    path("", include(router.urls)),
    # path("accessabilities/delete/", views.delete_accessability),

]
