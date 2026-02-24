from rest_framework import serializers
from .models import CBTExam, Question, CBTAttempt, QuestionAnswer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'order']


class CBTExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = CBTExam
        fields = ['id', 'course', 'title', 'description', 'duration_minutes', 'total_questions', 'pass_score', 'is_active']


class QuestionAnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = QuestionAnswer
        fields = ['id', 'question', 'selected_option', 'is_correct', 'time_taken_seconds']


class CBTAttemptSerializer(serializers.ModelSerializer):
    answers = QuestionAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = CBTAttempt
        fields = ['id', 'exam', 'started_at', 'submitted_at', 'status', 'score', 'total_questions', 'correct_answers', 'time_taken_seconds', 'answers']
