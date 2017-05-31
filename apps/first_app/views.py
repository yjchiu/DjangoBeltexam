from django.shortcuts import render, redirect
from .models import User, Item
from django.contrib import messages


def index(request):

    return render(request, 'first_app/index.html')


def create(request):
    postData = {
        'name' : request.POST['name'], 
        'username' : request.POST['username'], 
        'pwd' : request.POST['pwd'], 
        'confirm_pwd' : request.POST['confirm_pwd']
    }

    user = User.objects.reg(postData)

    if 'error' in user:
        messages.warning(request, user['error'])
        return redirect('/')
    
    if 'theUser' in user:
        request.session['id'] = user['theUser'].id
        return redirect('/dashboard')

def login_process(request):

    context = { 
        'username' : request.POST['username'], 
        'pwd' : request.POST['pwd'] 
    }
    user = User.objects.login(context)
    
    if 'error' in user:
        messages.warning(request, user['error'])
        return redirect('/')
    
    if 'theUser' in user:
        request.session['id'] = user['theUser'].id
        return redirect('/dashboard')


def showall(request):
    user = User.objects.get(id = request.session['id'])
    other_items = Item.objects.exclude(items_to_user = user)
    context = {
        'user':user, 
        'other_items': other_items
    }
    return render(request, 'first_app/dashboard.html', context)

def addtowishlist(request, item_id):
    User.objects.get(id = request.session['id']).user_wishlist.add(Item.objects.get(id = item_id))

    return redirect('/dashboard')

def show(request,item_id):

    context = {
        'item' : Item.objects.get(id = item_id)
    }
    return render(request,'first_app/show.html', context)





def add(request):

    return render(request, 'first_app/add.html')

def additem(request):
    name = request.POST['item']
    user = User.objects.get(id = request.session['id'])
    items_to_user = User.objects.get(id = request.session['id'])

    context = {
        'name' : name,
        'user' : user,
        'items_to_user' : items_to_user
    }

    item = Item.objects.add(context)
    print item['Item'].name
    if 'error' in item:
        messages.warning(request, item['error'])
        return redirect('/wish_items/create')

    User.objects.get(id = request.session['id']).user_wishlist.add(item['Item'])
    return redirect('/dashboard')


def removefromwishlist(request, item_id):
    item = Item.objects.get(id = item_id)
    User.objects.get(id = request.session['id']).user_wishlist.remove(item)

    return redirect('/dashboard')


def delete(request, item_id):
    Item.objects.get(id = item_id).delete()

    return redirect('/dashboard')

def logoff(request):
    request.session.clear()
    return redirect('/')
