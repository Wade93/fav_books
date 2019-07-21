from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, Book
from datetime import datetime

def index(request):
    if 'user_id' in request.session:
        return redirect('/all_books')
    if 'fname' not in request.session:
        request.session['fname'] = ""
    if 'lname' not in request.session:
        request.session['lname'] = ""
    if 'email' not in request.session:
        request.session['email'] = ""
    return render(request, 'fb_app/index.html')

def register_new_user(request):
    request.session['fname'] = request.POST['fname']
    request.session['lname'] = request.POST['lname']
    request.session['email'] = request.POST['email']

    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        User.objects.create(first_name = request.POST['fname'], last_name = request.POST['lname'], email = request.POST['email'], date_of_birth = request.POST['bdate'], password = pw_hash)

        request.session['user_id'] = User.objects.get(email = request.POST['email']).id
        return redirect('/all_books')

def login_user(request):
    errors = User.objects.log_in_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect('/')
    else:
        request.session['user_id'] = User.objects.get(email = request.POST['email']).id
        request.session['fname'] = User.objects.get(email = request.POST['email']).first_name
        return redirect('/all_books')

def all_books(request):
    if request.session['fname'] == "":
        return redirect('/')
    
    context = {
        "all_books" : Book.objects.all(),
        "favorited" : User.objects.get(id = request.session['user_id']).books_favorited.all(),
    }
    return render(request, 'fb_app/all_books.html', context)

def add_new_book(request):
    request.session['title'] = request.POST['title']
    request.session['description'] = request.POST['description']

    errors = Book.objects.add_book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect('/all_books')
    else:
        Book.objects.create(title = request.POST['title'], description = request.POST['description'], uploaded_by = User.objects.get(id = request.session['user_id']))

        Book.objects.last().favorited_by.add(User.objects.get(id = request.session['user_id']))
    return redirect('/all_books')

def view_book(request, id):
    
    context = {
        "current_user" : User.objects.get(id = request.session['user_id']),
        "book" : Book.objects.get(id = id),
        "favorited" : User.objects.get(id = request.session['user_id']).books_favorited.all(),
        "users_who_like" : Book.objects.get(id = id).favorited_by.all(),
    }

    return render(request, 'fb_app/view_book.html', context)

def update_book(request, id):
    errors = Book.objects.add_book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect(f'/view_book/{id}') 
    else:
        book_to_update = Book.objects.get(id=id)
        book_to_update.title = request.POST['title']
        book_to_update.description = request.POST['description']
        book_to_update.save()
    return redirect(f'/view_book/{id}')

def delete_book(request, id):
    Book.objects.get(id=id).delete()
    return redirect('/')

def favorite_book(request, id):
    cur_user = User.objects.get(id = request.session['user_id'])
    cur_user.books_favorited.add(Book.objects.get(id = id))
    return redirect('/all_books')

def unfavorite_book(request, id):
    cur_user = User.objects.get(id = request.session['user_id'])
    Book.objects.get(id=id).favorited_by.remove(cur_user)
    return redirect('/all_books')

def log_out_user(request):
    request.session.clear()
    return redirect('/')