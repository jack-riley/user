from django.shortcuts import redirect, redirect, render
import bcrypt, secrets
from .models import User, Message, Comment
from django.contrib import messages

# Create your views here.

def index(request):

    if not 'user' in request.session:
        request.session['user'] = ''
    
    user = User.objects.filter(user_id = request.session['user'])
    
    if user:
        return redirect('/wall')
    
    else:
        request.session['user'] = ''
    return render (request, 'login.html')

def error(request):

    if not 'user' in request.session:
        request.session['user'] = ''
    
    else:
        request.session['user'] = ''
    return render (request, 'error.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    
    errors = User.objects.validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session["user"] = new_user.user_id
        messages.success(request, "You have successfully registered!")
        return redirect ('/wall')

def login(request):
    if request.method == "GET":
        return redirect('/')
    
    if not User.objects.authenticate(request.POST['email2'], request.POST['password2']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email2'])
    request.session['user'] = user.user_id
    messages.success(request, "You have successfully logged in!")
    return redirect('/wall')
        

def wall(request):
    check = User.objects.filter(user_id = request.session["user"])
    if check:
        context = {"message": Message.objects.all(),
        "current_user" : check[0]}
        return render(request, 'wall.html', context)
    else:
        return redirect ('/')

def process_message(request):
    errors = Message.objects.message_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wall')
    else:
        mess = request.POST['message']
        Message.objects.create(message = mess, user_id = User.objects.get(user_id = request.session["user"] ))
        return redirect('/wall')

def process_comment(request):
    errors = Comment.objects.comment_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wall')
    else:
        comm = request.POST['comment']
        mess_id = request.POST['mess_id']
        Comment.objects.create(comment = comm, message_id = Message.objects.get(id = mess_id), user_id = User.objects.get(user_id = request.session["user"] ))
        return redirect('/wall')

def logout(request):
    request.session.flush()
    messages.success(request, "You have successfully logged out")

    return redirect("/")

    