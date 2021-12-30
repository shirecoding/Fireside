from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils import JWTAuthentication


class AuthenticateUser(APIView):
    """
    JWT authentication for external services

    * expects a valid JWT in post.data
    * JWT data must contain user/username key
    * JWT should have a valid expire time
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = []

    def post(self, request):
        return Response(request.data)
