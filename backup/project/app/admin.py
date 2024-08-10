from django.contrib import admin

# Register your models here.

from .models import UserProfile, Message, Session, Question, Answer, CustomGPTModel, CustomGPTPrompt

admin.site.register(UserProfile)
admin.site.register(Message)
admin.site.register(Session)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(CustomGPTModel)

