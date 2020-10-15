from django.shortcuts import render, redirect
from loginApp.models import UserManager, User #import in order to use in error validations
from django.contrib import messages #in order to create error messages during validation
import bcrypt #to hash passwords

# Create your views here.
def index(request):
    #displays login/registration page
    return render(request, 'index.html')

def process_reg(request):
    #will process a new registration
    #first check if receiving a POST request
    #if not a POST request:
    if (request.method != "POST"):
        return redirect('/')

    #if a valid POST request, continues with checking for errors
    else:
        #check if registration object is valid
        #import list of errors found
        errors = User.objects.regValidator(request.POST)

        #add the error messages to each error if any errors found in the errors list - checks if list is empty or not - uses python message library - need to import at the top
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags = key)# value is the error message string created in models.py
                # extra_tags is optional and used if we want the error messages by key so we can position them in the HTML is specific locations
            return redirect('/')

        #check if email is already in the database
        user = User.objects.filter(email = request.POST['email'])

        if user: #if user does exist
            messages.error(request, "Email already exists", extra_tags = 'email')
            return redirect('/')

        #at this point, all checks pass and we can store the user's data into the database:
        #hash password with Bcrypt - need to import above
        raw_pw = request.POST['password']
        hashed_pw = bcrypt.hashpw(raw_pw.encode(), bcrypt.gensalt()).decode()

        #add user to database:
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_pw,
            birthday = request.POST['birthday']
        )

        #place the user ID into session - set to the last user created:
        request.session['user_id'] = User.objects.last().id

        return redirect('/success')


def process_login(request):
    #will log in the user
    #first check if receiving a POST request
    #if not a POST request:
    if (request.method != "POST"):
        return redirect('/')

    #if a valid POST request, continues with checking for errors
    else:
        #check if login object is valid
        #import list of errors found
        errors = User.objects.loginValidator(request.POST)

        #add the error messages to each error if any errors found in the errors list - checks if list is empty or not - uses python message library - need to import at the top
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags = key)# value is the error message string created in models.py
            return redirect('/')

        #check if email is already in the database
        user = User.objects.filter(email = request.POST['login_email'])

        if len(user) == 0: #if user does NOT exist
            messages.error(request, "Invalid email address or password!", extra_tags = 'login')
            return redirect('/')
    
        #at this point, all checks pass and we can now unhash the password
        #unhash password with Bcrypt - need to import above
        login_raw_pw = request.POST['login_password']

        #checks if the entered password does not match the one in the database
        if not bcrypt.checkpw(login_raw_pw.encode(), user[0].password.encode()):
            messages.error(request, "Invalid email address or password!", extra_tags = 'login')
            return redirect ('/')

        #place the user ID into session - set to the last user created:
        request.session['user_id'] = User.objects.get(email = request.POST['login_email']).id

        return redirect('/success')


def success(request):
    #displays a successful login/registered page
    #first check that user is logged in and didn't bypass the login page aka check that the user id is in session
    if 'user_id' not in request.session:
        return redirect('/')

    context = {
        'user' : User.objects.get(id = request.session['user_id'])
    }

    return render(request, "success.html", context)

def logout(request):
    #log user out of session and redirect to the home page
    #if you try to delete something not in session, you will get an error
    if ('user_id' in request.session):
        del request.session['user_id']
    return redirect('/')