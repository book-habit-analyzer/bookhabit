from django.db import models

# User model
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    is_profile_public = models.BooleanField(default=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username

# Book model
class Book(models.Model):
    STATUS_CHOICES = [
        ('Currently Reading', 'Currently Reading'),
        ('Completed', 'Completed'),
        ('Abandoned', 'Abandoned'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

# ReadingGoals model
class ReadingGoal(models.Model):
    GOAL_TYPE_CHOICES = [
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPE_CHOICES)
    target_pages = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.goal_type} Goal"

# ReadingLogs model
class ReadingLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateField()
    pages_read = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    reflection = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} on {self.date}"

# AnalyticsSummary model (optional caching)
class AnalyticsSummary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_books_read = models.IntegerField(default=0)
    total_pages_read = models.IntegerField(default=0)
    avg_pages_per_day = models.FloatField(default=0.0)
    most_read_genre = models.CharField(max_length=100, blank=True, null=True)
    current_streak = models.IntegerField(default=0)

    def __str__(self):
        return f"Analytics for {self.user.username}"

# CalendarHeatmapData model (for calendar streaks visualization)
class CalendarHeatmapData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    pages_read = models.IntegerField()

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.pages_read} pages"
