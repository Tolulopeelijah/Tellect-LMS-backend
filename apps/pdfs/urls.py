from django.urls import path
from .views import PdfsHomeView, CoursePDFsView, PDFDetailView, PDFUploadView, UpdatePDFProgressView, MyPDFProgressView

urlpatterns = [
    path('', PdfsHomeView.as_view(), name='pdfs-home'),
    path('course/<int:course_id>/', CoursePDFsView.as_view(), name='course-pdfs'),
    path('upload/', PDFUploadView.as_view(), name='pdf-upload'),
    path('my-progress/', MyPDFProgressView.as_view(), name='pdf-my-progress'),
    path('<int:pk>/', PDFDetailView.as_view(), name='pdf-detail'),
    path('<int:pk>/update-progress/', UpdatePDFProgressView.as_view(), name='pdf-update-progress'),
]
