from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import UserProfile, Session
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
        # If UserProfile does not exist, create one
        user_profile = UserProfile.objects.create(user=request.user)
    sessions = Session.objects.filter(user=user_profile)
    return render(request, 'home.html', {'sessions': sessions})



def end_session(request, session_id):
    session = Session.objects.get(id=session_id)
    session.end_time = timezone.now()
    session.save()
    return redirect('home')


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Redirect the user to the home page after successful login
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def chat(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        print("User Profile:", user_profile)  # Debugging statement
        messages = Message.objects.all()

        if request.method == 'POST':
            form = MessageForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                print("Message Content:", content)  # Debugging statement
                if contains_bad_words(content):
                    warning_message = "Please behave properly"
                    Message.objects.create(sender=user_profile, content=warning_message)
                    return JsonResponse({'content': warning_message})
                response = get_nlp_response(content)
                print("NLP Response:", response)  # Debugging statement
                Message.objects.create(sender=user_profile, content=response)
                return JsonResponse({'content': response})
    except UserProfile.DoesNotExist:
        return JsonResponse({'content': 'User profile does not exist'})
    except Exception as e:
        return JsonResponse({'content': f'An error occurred: {str(e)}'})

    form = MessageForm()
    return render(request, 'chat.html', {'form': form, 'messages': messages, 'user_profile': user_profile})

def contains_bad_words(content):
    # Define a list of bad words


    # Check if any bad words are present in the content
    for word in bad_words:
        if word in content:
            return True  # Bad word found
    return False  # No bad words found

from nltk.tokenize import word_tokenize

from nltk.tokenize import word_tokenize

def get_nlp_response(content):
    # Tokenize the input content
    tokens = word_tokenize(content.lower())

    # Check if the input is a simple greeting
    if content.lower() == "hello":
        return "Hi"

    # Check if any disease name is mentioned
    for word in tokens:
        if word in NLPModule().disease_responses:
            return NLPModule().disease_responses[word]

    # If the input is a sentence, print the tokens
    print("Tokenized input:", tokens)
    return "I received your message."
    