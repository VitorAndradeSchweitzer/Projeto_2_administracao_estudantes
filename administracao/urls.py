from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from cadastroaluno.api import viewsets

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from cadastroaluno.views import EmailTokenObtainView

router = routers.DefaultRouter()
router.register(r"students", viewsets.StudentViewSet, basename='students')
router.register(r"teacher", viewsets.TeacherViewSet, basename='teachers')
router.register(r"class", viewsets.ClassViewSet, basename='class')
router.register(r'users', viewsets.UserViewSet)
router.register(r'moderator', viewsets.ModeratorViewSet)
 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cadastroaluno.urls')),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
