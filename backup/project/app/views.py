import os

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse
from .forms import MessageForm
from .models import UserProfile, Session, Message
from nltk.tokenize import word_tokenize
import json

# Load the JSON data
# Get the directory of the current file
current_directory = os.path.dirname(__file__)
with open('G:/2024 projects/Adithyan Chatbot disease/project/app/output.json') as json_file:
    data = json.load(json_file)
# Construct the path to the JSON file
json_file_path = os.path.join(current_directory, 'output.json')

# Load the JSON data
with open(json_file_path) as json_file:
    data = json.load(json_file)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def home(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    sessions = Session.objects.filter(user=user_profile)
    return render(request, 'home.html', {'sessions': sessions})

def end_session(request, session_id):
    session = Session.objects.get(id=session_id)
    session.end_time = timezone.now()
    session.save()
    return redirect('home')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def contains_bad_words(content):
    # Define a list of bad words
    bad_words = ["bad", "inappropriate", "offensive"]

    # Check if any bad words are present in the content
    for word in bad_words:
        if word in content:
            return True  # Bad word found
    return False  # No bad words found
def get_nlp_response(content):
    # Tokenize the input content
    tokens = word_tokenize(content.lower())
    print(tokens)

    # Initialize variables to store the best matching disease and its score
    best_match = None
    best_score = 0

    # Iterate over the diseases in the JSON data
    for disease_info in data:
        # Calculate the score for this disease based on matching words
        score = sum(1 for token in tokens if token in word_tokenize(disease_info["disease"].lower()))

        # Check if gender and severity match
        gender_match = (disease_info["gender"].lower() in tokens)
        severity_match = (disease_info["severity"].lower() in tokens)

        # Update the best match if the score for this disease is higher
        # and if gender and severity match
        if score > best_score and gender_match and severity_match:
            best_match = disease_info
            best_score = score

    # If a best match is found, construct the response
    if best_match:
        response = f"For {best_match['gender']} with {best_match['severity']} severity of {best_match['disease']}, the recommended drug is {best_match['drug']}."
    else:
        response = "No relevant information found."
    print(response)

    return response





@login_required
def chat(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        messages = Message.objects.all()

        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                if contains_bad_words(content):
                    warning_message = "Please behave properly"
                    Message.objects.create(sender=user_profile, content=warning_message)
                    return JsonResponse({'content': warning_message})
                response = get_nlp_response(content)
                Message.objects.create(sender=user_profile, content=response)
                return JsonResponse({'content': response})
    except UserProfile.DoesNotExist:
        return JsonResponse({'content': 'User profile does not exist'})
    except Exception as e:
        return JsonResponse({'content': f'An error occurred: {str(e)}'})

    form = MessageForm()
    return render(request, 'chat.html', {'form': form, 'messages': messages, 'user_profile': user_profile})
