from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.messages import get_messages
from .models import *

def index(request):
    return render(request, 'myapp/index.html')

def register(request):
    info = User.objects.reg_validator(request)

    if info[1]:
        return redirect('/home')
    else:
        for key, value in info[0].items():
            messages.error(request, value)
        return redirect('/')

def login(request):
    info = User.objects.login_validator(request)
    if info[1]:
        return redirect('/home')
    else:
        for key, value in info[0].items():
            messages.error(request, value)
        return redirect('/')

def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        if 'search_term' not in request.session:
            if 'receiver_id' not in request.session:
                user = User.objects.get(id=request.session['user_id'])
                people = User.objects.exclude(id=request.session['user_id'])
                conversations = {}

                for person in people:
                    conversation = {}
                    messages = Message.objects.filter(Q(sender=user.id, receiver=person.id) | Q(receiver=user.id, sender=person.id)).order_by('created_at')
                    if len(messages) == 0:
                        last_message = False
                        conversation['messages'] = messages
                        conversation['last_message'] = last_message
                    else:
                        last_message = messages[len(messages)-1]
                        conversation['messages'] = messages
                        conversation['last_message'] = last_message

                    conversations[f'{person.id}'] = conversation

                context = {
                    'user': user,
                    'people': people,
                    'conversations': conversations,
                    'active1': 'active'
                }
                return render(request, 'myapp/home.html', context)
            else:
                user = User.objects.get(id=request.session['user_id'])
                people = User.objects.exclude(id=request.session['user_id'])
                conversations = {}

                for person in people:
                    conversation = {}
                    messages = Message.objects.filter(Q(sender=user.id, receiver=person.id) | Q(receiver=user.id, sender=person.id)).order_by('created_at')
                    if len(messages) == 0:
                        last_message = False
                        conversation['messages'] = messages
                        conversation['last_message'] = last_message
                    else:
                        last_message = messages[len(messages)-1]
                        conversation['messages'] = messages
                        conversation['last_message'] = last_message

                    conversations[f'{person.id}'] = conversation

                context = {
                    'user': user,
                    'people': people,
                    'conversations': conversations,
                    'active1': '',
                    'currentReceiver': request.session['receiver_id']
                }
                return render(request, 'myapp/home.html', context)
        else:
            if 'receiver_id' not in request.session:
                user = User.objects.get(id=request.session['user_id'])
                people = User.objects.exclude(id=request.session['user_id'])
                conversations = {}

                for person in people:
                    conversation = {}
                    messages = Message.objects.filter(message__contains=request.session['search_term']).filter(Q(sender=user.id, receiver=person.id) | Q(receiver=user.id, sender=person.id)).order_by('created_at')
                    if len(messages) == 0:
                        last_message = False
                        conversation['messages'] = messages
                        conversation['last_message'] = last_message
                    else:
                        last_message = messages[len(messages)-1]
                        conversation['messages'] = messages
                        conversation['last_message'] = last_message

                    conversations[f'{person.id}'] = conversation

                context = {
                    'user': user,
                    'people': people,
                    'conversations': conversations,
                    'active1': 'active'
                }
                return render(request, 'myapp/home.html', context)
            else:
                user = User.objects.get(id=request.session['user_id'])
                people = User.objects.exclude(id=request.session['user_id'])
                conversations = {}

                for person in people:
                    conversation = {}
                    messages = Message.objects.filter(message__contains=request.session['search_term']).filter(Q(sender=user.id, receiver=person.id) | Q(receiver=user.id, sender=person.id)).order_by('created_at')
                    if len(messages) == 0:
                        last_message = False
                        conversation['messages'] = messages
                        conversation['last_message'] = last_message
                    else:
                        last_message = messages[len(messages)-1]
                        conversation['messages'] = messages
                        conversation['last_message'] = last_message

                    conversations[f'{person.id}'] = conversation

                context = {
                    'user': user,
                    'people': people,
                    'conversations': conversations,
                    'active1': '',
                    'currentReceiver': request.session['receiver_id']
                }
                return render(request, 'myapp/home.html', context)

def create(request, person_id):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        receiver = User.objects.get(id=person_id)
        user = User.objects.get(id=request.session['user_id'])
        request.session['receiver_id'] = receiver.id
        Message.objects.create(message=request.POST['message'], sender=user, receiver=receiver)
        return redirect('/home')

def change(request, new_id):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        request.session['receiver_id'] = new_id
        return redirect('/home')

def clear(request):
    if 'receiver_id' in request.session:
        if 'search_term' in request.session:
            request.session.pop('receiver_id')
            request.session.pop('search_term')
            return redirect('/home')
        else:
            request.session.pop('receiver_id')
            return redirect('/home')
    else:
        if 'search_term' in request.session:
            request.session.pop('search_term')
            return redirect('/home')
        else:
            return redirect('/home')

def search(request):
    request.session['search_term'] = request.POST['search']
    return redirect('/home')

def profile(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user
        }
        return render(request, 'myapp/profile.html', context)

    
def logout(request):
    request.session.clear()
    return redirect('/')