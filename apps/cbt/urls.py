from django.urls import path
from .views import CbtHomeView, CourseExamsView, ExamDetailView, StartExamView, AttemptDetailView, SaveAnswerView, SubmitExamView, AutoSubmitExamView

urlpatterns = [
    path('', CbtHomeView.as_view(), name='cbt-home'),
    path('course/<int:course_id>/', CourseExamsView.as_view(), name='course-exams'),
    path('<int:exam_id>/', ExamDetailView.as_view(), name='exam-detail'),
    path('<int:exam_id>/start/', StartExamView.as_view(), name='exam-start'),
    path('attempt/<int:attempt_id>/', AttemptDetailView.as_view(), name='attempt-detail'),
    path('attempt/<int:attempt_id>/answer/', SaveAnswerView.as_view(), name='attempt-answer'),
    path('attempt/<int:attempt_id>/submit/', SubmitExamView.as_view(), name='attempt-submit'),
    path('attempt/<int:attempt_id>/auto-submit/', AutoSubmitExamView.as_view(), name='attempt-auto-submit'),
]
