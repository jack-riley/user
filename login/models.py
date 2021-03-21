import bcrypt, secrets
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Create your models here.

class Validator(models.Manager):
    def validator (self,postData) :
        errors = {}
        if len (postData['first']) < 2:
            errors['first'] = "First name should be at least two (2) characters"
        if len (postData['last']) < 2:
            errors['last'] = "Last name should be at least two (2) characters"  
        email = (User.objects.filter(email =postData['email']))      
        if email:
            errors['email_dup'] = "Email already in use. Please use a different Email."
        try:
            validate_email(postData['email'])
            valid_email = True
        except ValidationError:
            valid_email = False
        if valid_email == False:
            errors['email'] = "Email must be valid"
        valid_date = datetime.today() - relativedelta(years=13)
        c_date =datetime.strftime(valid_date, '%Y,%m,%d')
        if c_date < (postData['dob']) :
            errors['dob'] = "Must be at least 13 years old to register"
        if len (postData['password']) < 8:
            errors['pass'] = "Password must be at least 8 characters"
        if (postData['password']) != (postData['c_password']):
            errors['c_password'] = "Passwords must match"
        
        return errors 
    
    def authenticate(self, email, password):
        users = self.filter(email = email)
        if not users:
            return False
        
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())
    
    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()

        return self.create(
            email = form['email'],
            first_name = form["first"],
            last_name = form["last"],
            dob = form["dob"],
            password = pw,
            user_id = secrets.token_hex(20)

        )

class message_validator(models.Manager):
    def message_validator(self, postData) :
        errors = {}
        if len (postData['message']) <3:
            errors['mess'] = "Messages must have at least 3 Characters"
        return errors

class comment_validator(models.Manager):
    def comment_validator(self, postData) :
        errors = {}
        if len (postData['comment']) <3:
            errors['comm'] = "Comments must have at least 3 Characters"
        return errors



        


class User(models.Model):
    email = models.CharField(max_length=55)
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    dob = models.DateField()
    password = models.CharField(max_length=255)
    user_id = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Validator()

class Message(models.Model):
    user_id = models.ForeignKey(User, related_name= 'messages', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = message_validator()


class Comment(models.Model):
    user_id = models.ForeignKey(User, related_name= 'comments', on_delete=models.CASCADE)
    message_id = models.ForeignKey(Message, related_name= 'comments', on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = comment_validator()






