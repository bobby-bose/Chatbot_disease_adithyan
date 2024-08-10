import os
import string

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.http import JsonResponse
from .forms import MessageForm
from .models import UserProfile, Session, Message
from nltk.tokenize import word_tokenize


# Load the JSON data


class RegisterUserView(View):
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('register')
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

    def get(self, request):
        return render(request, 'register.html')


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


class LoginUserView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            print("Invalid username or password")
            return redirect('login')

    def get(self, request):
        return render(request, 'login.html')

def contains_bad_words(content):
    # Define a list of bad words
    bad_words = ["bad", "inappropriate", "offensive"]

    # Check if any bad words are present in the content
    for word in bad_words:
        if word in content:
            return True  # Bad word found
    return False  # No bad words found


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import random

# Read the dataset
df = pd.read_json("G:/2024 projects/Adithyan Chatbot disease/project/app/output.json")

# Convert symptoms to tokenized format
symptoms = df.drop(columns=['prognosis', 'drug'])
symptoms_text = symptoms.apply(lambda x: ' '.join(map(str, x)), axis=1)

# Tokenize symptoms
vectorizer = CountVectorizer(binary=True)
X = vectorizer.fit_transform(symptoms_text)

# Target variable
y = df['prognosis']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)

import json
import random

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .models import UserProfile, Message
from .forms import MessageForm

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
import string
from nltk.corpus import stopwords
def find_matching_prognosis(prompt, data):
    keywords = [
        'acidity', 'indigestion', 'headache', 'blurred_and_distorted_vision',
        'excessive_hunger', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
        'movement_stiffness', 'depression', 'irritability', 'visual_disturbances',
        'painful_walking', 'abdominal_pain', 'nausea', 'vomiting', 'blood_in_mucus',
        'Fatigue', 'Fever', 'Dehydration', 'loss_of_appetite', 'cramping',
        'blood_in_stool', 'gnawing', 'upper_abdomain_pain', 'fullness_feeling',
        'hiccups', 'abdominal_bloating', 'heartburn', 'belching', 'burning_ache'
    ]

    # Split the prompt into words and convert them to lowercase
    prompt = prompt.replace(",", "").replace(".", "")
    prompt_words = prompt.lower().split()
    print(prompt_words)

    # Initialize variables to store age, gender, and severity
    age = None
    gender = None
    severity = None

    # Extract age, gender, and severity from the prompt
    for word in prompt_words:
        if word.isdigit():
            age = int(word)
        elif word == 'female' or word == 'male':
            gender = word
        elif word in ['normal', 'low', 'high','NORMAL','LOW','HIGH']:
            severity = word

    # Filter data based on age, gender, and severity
    filtered_data = [entry for entry in data if entry['age'] == age and entry['gender'] == gender and entry['severity'].lower() == severity]
    print("filtered_data",filtered_data[0])

    matching_prognosis = filtered_data[0]["prognosis"]
    matching_drug = filtered_data[0]["drug"]


    return matching_prognosis, matching_drug



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
                matching_prognosis, matching_drug = find_matching_prognosis(content, data)
                response = f"You are diagnosed with: {matching_prognosis} and the prescribed drug for this condition is: {matching_drug}. Thank you for using our service."
                Message.objects.create(sender=user_profile, content=response)
                return JsonResponse({'content': response})
    except UserProfile.DoesNotExist:
        return JsonResponse({'content': 'User profile does not exist'})
    except Exception as e:
        return JsonResponse({'content': f'An error occurred: {str(e)}'})

    form = MessageForm()
    return render(request, 'chat.html', {'form': form, 'messages': messages, 'user_profile': user_profile})

# Load data from output.json
data = load_data("G:/2024 projects/Adithyan Chatbot disease/project/app/output.json")
