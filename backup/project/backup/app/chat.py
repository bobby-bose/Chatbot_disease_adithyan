from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .badwords import bad_words
from .models import UserProfile, Message
from .forms import MessageForm
from .nlpmodule import NLPModule



