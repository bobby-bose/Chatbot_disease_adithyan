from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Session(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

class Question(models.Model):
    question_text = models.TextField()
    # Add any additional fields you need for questions, such as category, difficulty, etc.




class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer_text = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to '{self.question}' by {self.user.user.username}"


class CustomGPTModel(models.Model):
    name = models.TextField()
    # Add any additional fields you need for custom GPT models, such as description, parameters, etc.

class CustomGPTPrompt(models.Model):

    model = models.ForeignKey(CustomGPTModel, on_delete=models.CASCADE)
    prompt = models.TextField()
    # Add any additional fields you need for custom GPT prompts, such as category, difficulty, etc.