from bottle import run, route, static_file, template, request, response, redirect, app
import os
from beaker.middleware import SessionMiddleware

adminuser = 'admin'
adminpwd = '12345'

@route('/static/<filename>')
def static_server(filename):
    return static_file(filename,root=('./myfiles'))

@route('/')
def index():
    return template('index')

@route('/login')
def login():
    return template('login')

@route('/login', method='post')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')

    if username == adminuser and password == adminpwd:
        response.set_cookie('account', username, secret='my_secret_code')
        return redirect('/restricted')
    else:
        return "Login failed. <br> <a href='/login'>Login</a>"

@route('/restricted')
def restricted():
    user = request.get_cookie('account', secret='my_secret_code')
    print(user)
    if(user):
        return "Restricted area. <br>" \
                "<a href='/signout'>Log off</a>"
    else:
        return "You are not logged in. Access denied."

@route('/signout')
def signout():
    response.set_cookie('account', "", expire=0)
    return "You have been signed out." \
            "<br> <a href='/login'>Log in</a>"

#Session lausn

session_options = {
    'session.type': 'file',
    'session.data_dir': './data'
}

my_session = SessionMiddleware(app(), session_options)

products = [
    {"pid": 1, "name": "Vara A", "price": 100},
    {"pid": 2, "name": "Vara B", "price": 400},
    {"pid": 3, "name": "Vara C", "price": 800},
    {"pid": 4, "name": "Vara D", "price": 300}
]

@route('/shop')
def shop():
    return template('shop', products=products)

@route('/cart/add/<id>')
def add_to_cart(id):
    session = request.environ.get('beaker.session')
    session[id] = products[int(id)-1]['name']
    session.save()

    print(session)
    return redirect('/cart')

@route('/cart')
def cart():
    session = request.environ.get('beaker.session')
    karfa = []
    for i in range(1, len(products)+1):
        i = str(i)
        if session.get(i):
            vara = session.get(i)
            karfa.append(vara)

    return template('cart', karfa=karfa)

@route('/cart/remove')
def remove_cart():
    session = request.environ.get('beaker.session') # ??
    session.delete()    # deletear sessioninu
    return redirect('/shop') #redirectar user a /shop






run(app = my_session)
#run(app = my_session, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))