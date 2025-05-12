from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Habit, HabitLog
from .serializers import HabitSerializer, HabitLogSerializer

# Create your views here.


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing habit instances.
    """

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view returns a list of all habits
        for the currently authenticated user.
        """
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Save the user when creating a new habit.
        """
        serializer.save(user=self.request.user)


class HabitLogViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing habit log instances.
    """

    serializer_class = HabitLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Enable filtering and ordering
    # by date and status
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["habit", "date", "status"]
    ordering_fields = ["date", "created_at"]

    def get_queryset(self):
        """
        This view returns a list of all logs
        for the habits of the currently authenticated user.
        """
        return HabitLog.objects.filter(habit__user=self.request.user)

    def perform_create(self, serializer):
        """
        Handle creating a habit log with the habit ID from the request.
        """
        habit_id = self.request.data.get("habit_id")
        if not habit_id:
            from rest_framework.exceptions import ValidationError

            raise ValidationError({"habit_id": "This field is required."})

        try:
            habit = Habit.objects.get(id=habit_id, user=self.request.user)
            serializer.save(habit=habit)
        except Habit.DoesNotExist:
            from rest_framework.exceptions import NotFound

            raise NotFound(f"No habit found with ID {habit_id}.")
