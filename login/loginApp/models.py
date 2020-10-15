from django.db import models
import re #in order to use the regex module
from datetime import date, datetime, timedelta#to use the current date

# Create your models here.
class UserManager(models.Manager):
    #create validations - one for registration, one for login
    def regValidator(self, postData):
        errors = {}

        #regex imported above
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        # test whether a field matches the pattern
        # The EMAIL_REGEX object has a method called .match() that will return None if no match can be found. If the argument matches the regular expression, a match object instance is returned.
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"

        # First Name - required; at least 2 characters; letters only
        if (len(postData['first_name']) == 0):
            errors['first_name'] = "First name required"

        if (len(postData['first_name']) < 2):
            errors['first_name'] = "First name must be at least 2 characters"

        # returns a boolean that shows whether a string contains only alphabetic characters
        if (not str.isalpha(postData['first_name'])):
            errors['first_name'] = "First name must be letters only"

        # Last Name - required; at least 2 characters; letters only
        if (len(postData['last_name']) == 0):
            errors['last_name'] = "Last name required"

        if (len(postData['last_name']) < 2):
            errors['last_name'] = "Last name must be at least 2 characters"

        # returns a boolean that shows whether a string contains only alphabetic characters
        if (not str.isalpha(postData['last_name'])):
            errors['last_name'] = "Last name must be letters only"    

        # Password - required; at least 8 characters; matches password confirmation 
        if (len(postData['password']) < 8):
            errors['password'] = "Password must be at least 8 characters"

        if (postData['password'] != postData['pw_confirm']):
            errors['pw_confirm'] = "Passwords must match"

        # NINJA BONUS: Add a birthday field and validate that the user's birthday is in the past
        # a birthdate is required
        if (postData['birthday'] == ''):
            errors['birthday'] = "Please enter birthday"

        # need to import datetime and date
        else:
            convert_date = datetime.strptime(str(postData['birthday']), '%Y-%m-%d').date()
            if (convert_date > date.today()):
                errors['birthday'] = "Please enter a birthday in the past"  

            # SENSEI BONUS: Add a birthday field and validate that the user is at least 13 years old (COPPA compliant!) 
            #13 years = 365 * 13  = 4745 days
            if convert_date > date.today() - timedelta(days=4745): #'if birthday is less than current 13-year-old birthday'
                errors['birthday'] = "Must be 13 years of age to register"
        
        return errors

    def loginValidator(self, postData):
        errors = {}

        #regex imported above
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        # test whether a field matches the pattern
        # The EMAIL_REGEX object has a method called .match() that will return None if no match can be found. If the argument matches the regular expression, a match object instance is returned.
        if not EMAIL_REGEX.match(postData['login_email']):
            errors['login'] = "Invalid email address or password!"
       
        # Password - required; at least 8 characters; matches password confirmation 
        if (len(postData['login_password']) < 8):
            errors['login'] = "Invalid email address or password!"

        return errors



class User(models.Model):
    #user information
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    birthday = models.DateField(default = '1900-01-01')

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    #add for manager validator
    objects = UserManager()