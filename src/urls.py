from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from src.apps.notes.urls import router as notes_router
from src.apps.tags.urls import router as tags_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("silk/", include("silk.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("api/", include("src.apps.authentication.urls")),
    path("api/", include("src.apps.users.urls")),
    path("api/", include(notes_router.urls)),
    path("api/", include(tags_router.urls)),
]
