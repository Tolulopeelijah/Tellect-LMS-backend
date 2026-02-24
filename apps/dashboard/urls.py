from django.urls import path
from .views import DashboardView, TimetableView, TimetableDetailView, TodoListView, TodoDetailView, CompleteTodoView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('timetable/', TimetableView.as_view(), name='timetable-list'),
    path('timetable/<int:pk>/', TimetableDetailView.as_view(), name='timetable-detail'),
    path('todos/', TodoListView.as_view(), name='todo-list'),
    path('todos/<int:pk>/', TodoDetailView.as_view(), name='todo-detail'),
    path('todos/<int:pk>/complete/', CompleteTodoView.as_view(), name='todo-complete'),
]
