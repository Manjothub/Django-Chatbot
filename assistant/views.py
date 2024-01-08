from django.shortcuts import render,redirect
from django.http import JsonResponse
from openai import OpenAI
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

OPENAI_API_KEY = "your api key"
client = OpenAI(api_key=OPENAI_API_KEY)
def ask_openai(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ],
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].message["content"]

@login_required(login_url = 'login')
def CHATBOT(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request,'chatbot.html')


def LOGIN(request):
    return render(request, 'login.html')


def REGISTER(request):
    return render(request,'register.html')

def LOGOUT(request):
    logout(request)
    return render(request,'login.html')

def DOREGISTER(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        confrim_pass = request.POST['password2']
        if password == confrim_pass:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')


def DOLOGIN(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')