from flask import render_template

import random
names = ["Donald","Yoda","LeBron James", 
         "Theme", "Davide", "David", 
         "Jonas", "Santi", "World", 
         "Insect Overlords"]

def show_homepage():
    return render_template('index.html', name = random.choice(names))

def show_registration_form():
    return render_template('registration.html')

def register_new_user():
    def login():
        if request.method == 'POST':
            do_the_login()
        else:
            show_the_login_form()
    return 404
