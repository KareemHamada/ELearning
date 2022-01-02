from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from .models import Room,Topic,Mes
from .forms import RoomForm,UserForm
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except :
            messages.error(request, 'User Not found')

        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'User or password not found')
    page = "login"
    context = {"page":page}
    return render(request,"starting/login_register.html",context)

def register_page(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect("home")
        else:
            messages.error(request, 'An error occurred during registration')
    page = "register"
    context = {"form":form,"page":page}
    return render(request,"starting/login_register.html",context)

def logout_user(request):
    logout(request)
    return redirect("home")

def home(request):
    rooms = Room.objects.all()
    mess = Mes.objects.all()
    q = request.GET.get("q")
    if q != None:
        rooms = Room.objects.filter(
            Q(topic__name__icontains = q) |
            Q(name__icontains=q)  |
            Q(description__icontains=q)
        )
        mess = Mes.objects.filter(Q(room__topic__name__icontains = q))
    
    topics = Topic.objects.all()
    rooms_count = rooms.count()
    
    context = {"rooms": rooms,"topics":topics,"rooms_count":rooms_count,"mess":mess}
    return render(request, 'starting/home.html',context)

def room(request,id):
    room = Room.objects.get(id=id)
    room_mes = room.mes_set.all()
    participarnts = room.participarnts.all()

    if request.method == "POST":
        message_added = request.POST.get("message")
        if message_added != "":
            Mes.objects.create(user=request.user,room=room,body=message_added)
            room.participarnts.add(request.user)
            return redirect("/room/"+id)

    context = {"room":room,"room_mes":room_mes,"participarnts":participarnts}
    return render(request, 'starting/room.html',context)

@login_required(login_url="/login_page")
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            #form.save()
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect("home")
        
    context = {"form":form}
    return render(request,"starting/create_update_room.html",context)

@login_required(login_url="/login_page")
def update_room(request,id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form":form}
    return render(request,"starting/create_update_room.html",context)

@login_required(login_url="/login_page")
def delete_room(request,id):
    obj = Room.objects.get(id=id)

    if request.user != obj.host:
        return HttpResponse("You are not allowed to delete this room")

    if request.method == "POST":
        obj.delete()

        return redirect("home")

    context = {"obj":obj}
    return render(request,"starting/delete_obj.html",context)

@login_required(login_url="/login_page")
def delete_message(request,id):
    obj = Mes.objects.get(id=id)
    if request.user != obj.user:
        return HttpResponse("You are not allowed to delete this message")

    if request.method == "POST":
        obj.delete()
        return redirect("home")
    context = {"obj":obj}
    return render(request,"starting/delete_obj.html",context)

@login_required(login_url="/login_page")
def update_message(request,id):
    mes = Mes.objects.get(id=id)
    if request.user != mes.user:
        return HttpResponse("You are not allowed to delete this message")

    if request.method == "POST":
        updated_message = request.POST["updated_message"]
        mes.body = updated_message
        mes.save()
        return redirect("home")

    context = {"mes":mes}
    return render(request,"starting/update_message.html",context)

@login_required(login_url="/login_page")
def profile(request,id):
    user = User.objects.get(id=id)
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    mess = user.mes_set.all()
    context = {"user":user,"rooms":rooms,"topics":topics,"mess":mess}
    return render(request,"starting/profile.html",context)


#back to previous page
# request.META.HTTP_PEFERER