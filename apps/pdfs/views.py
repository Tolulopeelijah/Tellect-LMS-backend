from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import PDFMaterial, PDFReadProgress
from .serializers import PDFMaterialSerializer, PDFReadProgressSerializer


class PdfsHomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "name": "Tellect LMS PDFs API",
            "endpoints": {
                "course_pdfs": "course/<int:course_id>/",
                "upload": "upload/",
                "my_progress": "my-progress/",
                "pdf_detail": "<int:pk>/",
                "update_progress": "<int:pk>/update-progress/",
            },
        })


class CoursePDFsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        pdfs = PDFMaterial.objects.filter(course_id=course_id)
        return Response(PDFMaterialSerializer(pdfs, many=True).data)


class PDFDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            pdf = PDFMaterial.objects.get(pk=pk)
        except PDFMaterial.DoesNotExist:
            return Response({'error': 'PDF not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(PDFMaterialSerializer(pdf).data)


class PDFUploadView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = PDFMaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploaded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePDFProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            pdf = PDFMaterial.objects.get(pk=pk)
        except PDFMaterial.DoesNotExist:
            return Response({'error': 'PDF not found.'}, status=status.HTTP_404_NOT_FOUND)

        pages_read = request.data.get('pages_read', 0)
        total_pages = request.data.get('total_pages', 0)
        time_spent = request.data.get('time_spent_minutes', 0)
        is_completed = total_pages > 0 and pages_read >= total_pages

        progress, _ = PDFReadProgress.objects.update_or_create(
            student=request.user,
            pdf=pdf,
            defaults={'pages_read': pages_read, 'total_pages': total_pages, 'time_spent_minutes': time_spent, 'is_completed': is_completed}
        )
        return Response(PDFReadProgressSerializer(progress).data)


class MyPDFProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        progress = PDFReadProgress.objects.filter(student=request.user).select_related('pdf')
        return Response(PDFReadProgressSerializer(progress, many=True).data)
