from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.authentication.permissions import IsAdmin
from apps.courses.models import CourseEnrollment
from .models import Certificate
from .serializers import CertificateSerializer, CertificateVerifySerializer


class CertificatesHomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'name': 'Tellect LMS Certificates API',
            'status': 'active',
            'endpoints': {
                'my_certificates': 'my/',
                'generate': 'generate/',
                'detail': '<id>/',
                'verify': 'verify/<code>/',
            },
        })


class MyCertificatesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        certificates = Certificate.objects.filter(student=request.user, is_valid=True)
        return Response(CertificateSerializer(certificates, many=True).data)


class GenerateCertificateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({'error': 'course_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            enrollment = CourseEnrollment.objects.get(
                student=request.user,
                course_id=course_id,
                is_completed=True,
            )
        except CourseEnrollment.DoesNotExist:
            return Response(
                {'error': 'Course not found or not completed.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        certificate, created = Certificate.objects.get_or_create(
            student=request.user,
            course=enrollment.course,
        )
        if not created:
            return Response(
                {'message': 'Certificate already exists.', 'certificate': CertificateSerializer(certificate).data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {'message': 'Certificate generated.', 'certificate': CertificateSerializer(certificate).data},
            status=status.HTTP_201_CREATED,
        )


class CertificateDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            certificate = Certificate.objects.get(pk=pk)
        except Certificate.DoesNotExist:
            return Response({'error': 'Certificate not found.'}, status=status.HTTP_404_NOT_FOUND)

        if certificate.student != request.user and request.user.role != 'ADMIN':
            return Response({'error': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)

        return Response(CertificateSerializer(certificate).data)


class VerifyCertificateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, code):
        try:
            certificate = Certificate.objects.get(verification_code=code)
        except Certificate.DoesNotExist:
            return Response({'error': 'Certificate not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(CertificateVerifySerializer(certificate).data)


class RevokeCertificateView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request, pk):
        try:
            certificate = Certificate.objects.get(pk=pk)
        except Certificate.DoesNotExist:
            return Response({'error': 'Certificate not found.'}, status=status.HTTP_404_NOT_FOUND)
        certificate.is_valid = False
        certificate.save()
        return Response({'message': 'Certificate revoked.'})
