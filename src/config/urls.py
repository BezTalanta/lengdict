from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .start_view import StartView

urlpatterns = [
    path('', StartView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('dict/', include('word.urls')),
    path('run/', include('run.urls')),
    path('card/', include('card.urls')),
    path('account/', include('account.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
