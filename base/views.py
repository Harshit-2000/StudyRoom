from django.db.models import Q
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from base.forms import RoomForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.models import Message, Room, Topic
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def login_user(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exists.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Password and username does not match')

    return render(request, 'base/login_form.html')


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):

    if request.user.is_authenticated:
        return redirect('home')

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('login')

    context = {'form': form}
    return render(request, 'base/register.html', context)


def home_view(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_messages = Message.objects.all().order_by('-created_at')[:4]

    rooms = rooms.order_by('-updated_at', '-created_at')

    room_count = rooms.count()

    topics = Topic.objects.all()
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,
    }
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def create_room_view(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')

    context = {'form': form}

    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room_view(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host and request.user.is_superuser == False:
        return HttpResponse('You are not allowed to do that')

    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}

    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_room_view(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host and request.user.is_superuser == False:
        return HttpResponse('You are not allowed to do that')

    if request.method == "POST":
        room.delete()
        return redirect('home')

    context = {'obj': room}

    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def delete_message_view(request, pk):
    try:
        message = Message.objects.get(id=pk)
    except:
        return redirect('home')

    if request.user != message.user and request.user.is_superuser == False:
        return HttpResponse('You are not allowed to do that')

    if request.method == "POST":
        message.delete()
        return redirect('room', pk=message.room.id)

    context = {'obj': message}

    return render(request, 'base/delete.html', context)


def room_view(request, pk):

    room = Room.objects.get(id=pk)

    participants = room.participants.all()

    messages = room.message_set.all().order_by('-created_at')

    if request.method == "POST":
        message = request.POST.get('message-input')

        Message.objects.create(
            user=request.user,
            room=room,
            body=message
        )
        room.participants.add(request.user)

        return redirect('room', pk=room.id)
    context = {
        'room': room,
        'messages': messages,
        'participants': participants
    }

    return render(request, 'base/room.html', context)


def user_profile_view(request, pk):

    user = User.objects.get(id=pk)

    rooms = user.room_set.all()

    room_messages = user.message_set.all()

    topics = Topic.objects.all()


    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics,
    }

    return render(request, 'base/profile.html', context)
