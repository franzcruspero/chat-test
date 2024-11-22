
from allauth.account.views import confirm_email
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from oauth2_provider import urls as oauth2_urls
from django.views.generic import TemplateView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.api.v1.views import JWTLoginView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/oauth2/", include(oauth2_urls, namespace="oauth2_provider")),
    path("accounts/", include("allauth.urls")),

    path(
        "password/reset/confirm/<uidb64>/<token>/",
        TemplateView.as_view(template_name="accounts/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),

    # v1 APIs
    path(
        "api/v1/",
        include(
            (
                [
                    path("auth/login/", JWTLoginView.as_view(), name="rest_login"),
                    path("auth/", include("dj_rest_auth.urls")),
                    path("auth/registration/account-confirm-email/<str:key>/", confirm_email),
                    path("auth/registration/", include("dj_rest_auth.registration.urls")),
                    path(
                        "auth/token/",
                        TokenObtainPairView.as_view(),
                        name="token_obtain_pair",
                    ),
                    path(
                        "auth/token/refresh/",
                        TokenRefreshView.as_view(),
                        name="token_refresh",
                    ),
                    path(
                        "constance/",
                        include(
                            ("chat_app.api.v1.urls", "constance"),
                            namespace="constance",
                        ),
                    ),
                ],
                "v1",
            ),
            namespace="v1",
        ),
    ),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Swagger
api_info = openapi.Info(
    title="chat-app API",
    default_version="v1",
    description="API documentation for chat-app",
)

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(JWTAuthentication,),
)


urlpatterns += [
    path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="api_docs"),
]


admin.site.site_header = "chat-app"
admin.site.site_title = "chat-app Admin Portal"
admin.site.index_title = "chat-app Admin"
