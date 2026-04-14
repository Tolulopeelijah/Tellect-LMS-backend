from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CBTExam, Question, CBTAttempt, QuestionAnswer
from .serializers import CBTExamSerializer, QuestionSerializer, CBTAttemptSerializer


class CbtHomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "name": "Tellect LMS CBT API",
            "endpoints": {
                "course_exams": "course/<int:course_id>/",
                "exam_detail": "<int:exam_id>/",
                "start_exam": "<int:exam_id>/start/",
                "attempt_detail": "attempt/<int:attempt_id>/",
                "save_answer": "attempt/<int:attempt_id>/answer/",
                "submit": "attempt/<int:attempt_id>/submit/",
                "auto_submit": "attempt/<int:attempt_id>/auto-submit/",
            },
        })


class CourseExamsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        exams = CBTExam.objects.filter(course_id=course_id, is_active=True)
        return Response(CBTExamSerializer(exams, many=True).data)


class ExamDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, exam_id):
        try:
            exam = CBTExam.objects.get(pk=exam_id, is_active=True)
        except CBTExam.DoesNotExist:
            return Response({'error': 'Exam not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(CBTExamSerializer(exam).data)


class StartExamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, exam_id):
        try:
            exam = CBTExam.objects.get(pk=exam_id, is_active=True)
        except CBTExam.DoesNotExist:
            return Response({'error': 'Exam not found.'}, status=status.HTTP_404_NOT_FOUND)

        existing = CBTAttempt.objects.filter(student=request.user, exam=exam, status='in_progress').first()
        if existing:
            questions = Question.objects.filter(exam=exam)
            data = CBTAttemptSerializer(existing).data
            data['questions'] = QuestionSerializer(questions, many=True).data
            return Response(data)

        attempt = CBTAttempt.objects.create(
            student=request.user,
            exam=exam,
            total_questions=exam.questions.count()
        )
        questions = Question.objects.filter(exam=exam)
        for q in questions:
            QuestionAnswer.objects.create(attempt=attempt, question=q)

        data = CBTAttemptSerializer(attempt).data
        data['questions'] = QuestionSerializer(questions, many=True).data
        return Response(data, status=status.HTTP_201_CREATED)


class AttemptDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, attempt_id):
        try:
            attempt = CBTAttempt.objects.get(pk=attempt_id, student=request.user)
        except CBTAttempt.DoesNotExist:
            return Response({'error': 'Attempt not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(CBTAttemptSerializer(attempt).data)


class SaveAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, attempt_id):
        try:
            attempt = CBTAttempt.objects.get(pk=attempt_id, student=request.user, status='in_progress')
        except CBTAttempt.DoesNotExist:
            return Response({'error': 'Active attempt not found.'}, status=status.HTTP_404_NOT_FOUND)

        question_id = request.data.get('question_id')
        selected_option = request.data.get('selected_option')
        time_taken = request.data.get('time_taken_seconds', 0)

        try:
            question = Question.objects.get(pk=question_id, exam=attempt.exam)
        except Question.DoesNotExist:
            return Response({'error': 'Question not found.'}, status=status.HTTP_404_NOT_FOUND)

        answer, _ = QuestionAnswer.objects.update_or_create(
            attempt=attempt,
            question=question,
            defaults={'selected_option': selected_option, 'is_correct': selected_option == question.correct_option, 'time_taken_seconds': time_taken}
        )
        return Response({'message': 'Answer saved.'})


def _calculate_and_submit(attempt, timed_out=False):
    answers = QuestionAnswer.objects.filter(attempt=attempt)
    correct = answers.filter(is_correct=True).count()
    total = attempt.total_questions
    score = int((correct / total * 100)) if total > 0 else 0
    time_taken = int((timezone.now() - attempt.started_at).total_seconds())

    attempt.correct_answers = correct
    attempt.score = score
    attempt.time_taken_seconds = time_taken
    attempt.submitted_at = timezone.now()
    attempt.status = 'timed_out' if timed_out else 'submitted'
    attempt.save()
    return attempt


class SubmitExamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, attempt_id):
        try:
            attempt = CBTAttempt.objects.get(pk=attempt_id, student=request.user, status='in_progress')
        except CBTAttempt.DoesNotExist:
            return Response({'error': 'Active attempt not found.'}, status=status.HTTP_404_NOT_FOUND)

        attempt = _calculate_and_submit(attempt)
        return Response({
            'message': 'Exam submitted.',
            'score': attempt.score,
            'correct_answers': attempt.correct_answers,
            'total_questions': attempt.total_questions,
            'passed': attempt.score >= attempt.exam.pass_score,
            'attempt': CBTAttemptSerializer(attempt).data,
        })


class AutoSubmitExamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, attempt_id):
        try:
            attempt = CBTAttempt.objects.get(pk=attempt_id, student=request.user, status='in_progress')
        except CBTAttempt.DoesNotExist:
            return Response({'error': 'Active attempt not found.'}, status=status.HTTP_404_NOT_FOUND)

        attempt = _calculate_and_submit(attempt, timed_out=True)
        return Response({
            'message': 'Exam timed out and submitted.',
            'score': attempt.score,
            'correct_answers': attempt.correct_answers,
            'total_questions': attempt.total_questions,
            'passed': attempt.score >= attempt.exam.pass_score,
            'attempt': CBTAttemptSerializer(attempt).data,
        })
