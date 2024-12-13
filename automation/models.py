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