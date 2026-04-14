from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class AnnouncementsHomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "name": "Tellect LMS Announcements API",
            "status": "placeholder",
            "endpoints": {},
        })

