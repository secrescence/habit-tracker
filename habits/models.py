from django.db import models
from django.contrib.auth.models import User

# Create your models here.

frequency_choices = [
    ("daily", "Daily"),
    ("weekly", "Weekly"),
    ("monthly", "Monthly"),
]


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    name = models.CharField(max_length=100)
    description = models.TextField()
    frequency = models.CharField(max_length=10, choices=frequency_choices)

    def __str__(self):
        return self.name


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="logs")
    date = models.DateField()
    status = models.BooleanField(
        default=False
    )  # True = Completed, False = Not Completed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.habit.name} - {self.date}"
