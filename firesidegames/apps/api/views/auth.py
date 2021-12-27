from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils import JWTAuthentication


class AuthenticateUser(APIView):
    """
    JWT authentication for external services

    - post data should include jwt in the body
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = []

    def post(self, request):
        return Response(request.data)
