from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path("", include("reports.urls")),
] + debug_toolbar_urls()
