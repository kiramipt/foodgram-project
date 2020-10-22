from django.contrib import admin
from django.urls import include, path
from django.contrib.flatpages import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path("about/", include("django.contrib.flatpages.urls")),
    # path("about-author/", views.flatpage, {"url": "/about-author/"}, name="author"),
    # path("about-spec/", views.flatpage, {"url": "/about-spec/"}, name="spec"),
    path('', include('api.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('recipes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)