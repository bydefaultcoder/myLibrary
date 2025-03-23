from requests import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ViewSet

class StudentViewSet(ViewSet):
    authentication_classes = [TokenAuthentication]  # Require Token
    permission_classes = [IsAuthenticated]  # Require Authentication

    def list(self, request):
        return Response({"message": "Authenticated!"})