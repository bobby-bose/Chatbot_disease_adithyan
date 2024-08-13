# This should be deleted
import os
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

def get_nlp_response(content):
    # Select a random row from the dataset
    random_index = random.randint(0, len(df) - 1)
    random_row = df.iloc[random_index]

    # Predict prognosis and use the selected drug
    symptoms_str = content.lower()
    symptoms_vectorized = vectorizer.transform([symptoms_str])
    prognosis = rf_classifier.predict(symptoms_vectorized)[0]
    drug = random_row['drug']

    # Construct response
    response = f"You are diagnosed with: {prognosis} and the prescribed drug for this condition is: {drug}. Thank you for using our service."

    # Print response
    print(response)

    # Calculate accuracy
    y_pred = rf_classifier.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # Plot confusion matrix
    conf_matrix = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap="Blues", xticklabels=rf_classifier.classes_,
                yticklabels=rf_classifier.classes_)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()

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
