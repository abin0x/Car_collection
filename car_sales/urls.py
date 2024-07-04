from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cars.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='cars/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='cars/logout.html'), name='logout'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
