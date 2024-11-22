from dj_rest_auth.views import LoginView
from rest_framework_simplejwt.tokens import RefreshToken


class JWTLoginView(LoginView):
    def get_response(self):
        response = super().get_response()

        refresh = RefreshToken.for_user(self.user)

        response.data["tokens"] = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return response
