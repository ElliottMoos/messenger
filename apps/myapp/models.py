from django.db import models
import bcrypt, re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def login_validator(self, request):
        errors = {}
        is_logged_in = False
        user = User.objects.filter(email=request.POST['email'])

        if len(user) < 1:
            errors['email'] = "We couldn't find a match for that email"
        else:
            if not bcrypt.checkpw(request.POST['password'].encode(), User.objects.get(email=request.POST['email']).password.encode()):
                errors['password'] = "That seems to be the wrong password, please try again"

        if len(errors) < 1:
            user = User.objects.get(email=request.POST['email'])
            request.session['user_id'] = user.id
            is_logged_in = True
        info = [errors, is_logged_in]
        return info
            

    def reg_validator(self, request):

        errors = {}
        is_logged_in = False

        user = User.objects.filter(email=request.POST['email'])

        if not EMAIL_REGEX.match(request.POST['email']):
            errors['email'] = "Please enter a valid email address"

        if len(user) > 0:
            errors['email'] = "An account with that email already exists"

        if len(request.POST['first_name']) < 2:
            errors['first_name'] = "First name must be at aleast 2 characters long"

        if len(request.POST['last_name']) < 2:
            errors['last_name'] = "Last name must be at aleast 2 characters long"

        if len(request.POST['password']) < 8:
            errors['password'] = "Password must be at aleast 8 characters long"

        elif request.POST['password'] != request.POST['confirm_password']:
            errors['password'] = "Passwords do not match"

        if len(errors) < 1:
            hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=hashedpw.decode())
            request.session['user_id'] = user.id
            is_logged_in = True

        info = [errors, is_logged_in]
        return info

class MessageManager(models.Manager):
    def message_validator(self, request):
        pass


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    sender = models.ForeignKey(User, related_name="sent", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = MessageManager()

