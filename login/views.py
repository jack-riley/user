from django.shortcuts import redirect, redirect, render
import bcrypt, secrets
from .models import User
from django.contrib import messages

# Create your views here.

def index(request):

    if not 'user' in request.session:
        request.session['user'] = ''
    
    else:
        request.session['user'] = ''
    return render (request, 'login.html')

def register(request):
    errors = User.objects.validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        first = request.POST["first"]
        last = request.POST["last"]
        email = request.POST["email"]
        dob = request.POST["dob"]
        password = request.POST["password"]
        user_id = secrets.token_hex(20)
        pw_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()  
        User.objects.create(first_name = first, last_name = last, dob = dob, email = email, user_id = user_id,  password = pw_hash)
        request.session["user"] = user_id
        return redirect ('/success')

def login(request):
    if request.method == ["POST"]:
        user = User.objects.filter(email=request.POST["email2"])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password2'].encode(), logged_user.encode()):
                request.session["user"] = logged_user.user_id
            else:
                errors = User.objects.un_login_validator(request.POST)
                errors['invalid'] = "Email or Password Incorrect"
                for key, value in errors.items():
                    messages.error(request, value)
                return errors, redirect ('/')
        else:
            errors = User.objects.un_login_validator(request.POST)
            for key, value in errors.items():
                messages.error(request, value)
            return errors, redirect ('/')

    return redirect ('/success')
        

def success(request):
    check = User.objects.filter(user_id = request.session["user"])
    if check:
        context = {"current_user": User.objects.get(user_id = request.session["user"]) }
        return render(request, 'success.html', context)
    else:
        return redirect ('/')