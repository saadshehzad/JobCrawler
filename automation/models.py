from django.db import models


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Website(TimeStampedMixin):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class SkillSet(TimeStampedMixin):
    skill_name = models.CharField(max_length=100)
    country_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.skill_name} -- {self.country_name}"


class MyMessage(TimeStampedMixin):
    name = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return f"{self.name}"

class CurrentJobState(TimeStampedMixin):
    STATE_CHOICES = (
        ("Login", "Login"),
        ("Searching Jobs", "Searching Jobs"),
        ("Opening Company Link", "Opening Company Link"),
        ("Submitting Application", "Submitting Application"),
        ("Application Submitted", "Application Submitted"),
        ("Error Occurred", "Error Occurred"),
    )

    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    state = models.CharField(max_length=50, choices=STATE_CHOICES)
    failure_reason = models.TextField(blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    is_successful = models.BooleanField(default=False)
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)