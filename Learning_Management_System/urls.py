from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Learning_Management_System import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),
    path('', include('accounts.urls')),
    path('', include('enroll.urls')),
    path('', include('courses.urls')),
    path('summernote/', include('django_summernote.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)