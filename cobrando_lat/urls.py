from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from bank_details.views import public_profile
from home.views import index, about, contact, terms

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", index, name="home"),  # Landing Page
    path("about/", about, name="about"),
    path("contact/", contact, name="contact"),
    path("dashboard/", include("bank_details.urls")),
    path("terms/", terms, name="terms"),
    path("u/<slug:public_slug>/", public_profile, name="public_profile"), # Public profile configured with slug 
]

if settings.DEBUG:
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]