from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from incidents.views import NetIncidentsLoginView, connexion_demo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('incidents.urls')),
    path('login/', NetIncidentsLoginView.as_view(), name='login'),
    path('login/demo/', connexion_demo, name='connexion_demo'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
