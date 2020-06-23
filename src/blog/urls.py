from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from posts.views import index, blog, post, post_update, post_delete, post_create
from .api.viewsets import PostViewSet
from rest_framework import routers


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('', index, name="index"),
    path('blog/', blog, name="blog"),
    path('create', post_create, name="post-create"),
    path('post/<int:id>', post, name="post-detail"),
    path('post/<int:id>/update', post_update, name="post-update"),
    path('post/<int:id>/delete', post_delete, name="post-delete"),
]

router = routers.DefaultRouter()
router.register('api', PostViewSet)
urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
