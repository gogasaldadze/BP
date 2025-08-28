from django.urls import path, include


urlpatterns = [path("token/", include("api.auth.token.urls"))]
