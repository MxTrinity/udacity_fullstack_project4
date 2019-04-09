#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model import Base, User, Category, Item
from flask import Flask, jsonify, request, url_for, flash
from flask import abort, g, render_template, redirect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import create_engine, desc
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
from flask import session as login_session
import requests
import json
from flask_httpauth import HTTPBasicAuth
import httplib2
from oauth2client import client


auth = HTTPBasicAuth()
CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
Session = scoped_session(DBSession)
app = Flask(__name__)


@app.route('/')
def index():
    # call a session from the scoped session to avoid thread errors on
    # refresh. saved me a lot of headaches
    session = Session()
    items = session.query(Item).order_by(desc(Item.id)).limit(9)
    categories = session.query(Category).all()
    if 'username' not in login_session or login_session['username'] is None:
        # print("serving public page")
        Session.remove()
        return render_template('Index.html', categories=categories,
                               items=items, title="Recently Added Items",
                               login=0)
    else:
        # print("serving private page")
        # print(login_session['username'])
        Session.remove()
        return render_template('Index.html', categories=categories,
                               items=items, title="Recently Added Items",
                               login=1)


@app.route('/<category>/items')
def category(category):
    session = Session()
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category).one()
    items = session.query(Item).filter_by(
        category_id=category.id).all()
    # session.expunge_all()
    # not exactly sure how to gracefully terminate these
    # because terminating before a return that uses the
    # items from the session screws up lazy loading
    # but i presume that ending the function terminates the thread
    # maybe not so cleanly
    if 'username' not in login_session or login_session['username'] is None:
        # Session.remove()
        return render_template('Index.html', categories=categories,
                               items=items, title=category.name, login=0)
    else:
        # Session.remove()
        return render_template('Index.html', categories=categories,
                               items=items, title=category.name, login=1)


@app.route('/<category>/<item>')
def item(category, item):
    session = Session()
    itemName = item.replace('%20', ' ')
    selectedItem = session.query(Item).filter_by(name=itemName).one()
    if 'username' not in login_session or login_session['username'] is None:
        # capture the login state to persist the banner
        user = False
        logstate = 0
    elif selectedItem.user.username == login_session['username']:
        user = True
        logstate = 1
    else:
        user = False
        logstate = 1
    Session.remove()
    return render_template('item.html', name=itemName,
                           description=selectedItem.description, user=user,
                           login=logstate)


@app.route('/addItem', methods=['GET', 'POST'])
def addItem():
    session = Session()
    if 'username' not in login_session or login_session['username'] is None:
        return redirect(url_for('index'))
    elif request.method == 'POST':
        # check if there's an item that already has this name
        itemName = request.form['name']
        # don't let the user add empty items
        if itemName == '':
            itemName = 'Empty'
        # this will also bounce users if they try to enter
        #  too many items with the name empty
        existingItem = session.query(Item).filter_by(name=itemName).count()
        if existingItem > 0:
            Session.remove()
            return redirect(url_for('index'))
        else:
            # build item from form
            itemDescription = request.form['description']
            itemCategoryName = request.form['category']
            itemCategory = session.query(Category).filter_by(
                name=itemCategoryName).one()
            itemUsername = login_session['username']
            itemUser = session.query(User).filter_by(
                username=itemUsername).one()

            item = Item(name=itemName, description=itemDescription,
                        category=itemCategory, user=itemUser)
            session.add(item)
            session.commit()
            # Session.remove()
            return redirect(url_for('category',
                                    category=itemCategoryName, login=1))
    else:
        categories = session.query(Category).all()
        # Session.remove()
        # I don't want users changing their login state during an add
        # failsafes are there for expired tokens but it's annoying
        return render_template('addEditItem.html', categories=categories,
                               type='add')


@app.route('/<item>/edit', methods=['GET', 'POST'])
def editItem(item):
    session = Session()
    selectedItem = session.query(Item).filter_by(name=item).one()
    if 'username' not in login_session or login_session['username'] is None:
        # you gotta be logged in to edit
        Session.remove()
        return redirect(url_for('index'))
    elif login_session['username'] != selectedItem.user.username:
        # can't edit someone else's item
        Session.remove()
        return redirect(url_for('index'))
    else:
        categories = session.query(Category).all()
        if request.method == 'POST':
            selectedItem.name = request.form['name']
            # avoid 404 errors, don't let the user drop the item name
            # have to add on the id to avoid someone editing in
            # multiple empty items
            if selectedItem.name == '':
                selectedItem.name = 'Empty ' + str(selectedItem.id)
            selectedItem.description = request.form['description']
            selectedItem.category = session.query(Category).filter_by(
                name=request.form['category']).one()
            session.add(selectedItem)
            session.commit()
            # Session.remove()
            return redirect(url_for('item',
                                    category=selectedItem.category.name,
                                    item=selectedItem.name))
        else:
            # print('editing item: ' + str(selectedItem.name))
            # Session.remove()
            # no changing logins during edits
            return render_template('addEditItem.html', item=selectedItem,
                                   categories=categories, type='edit')


@app.route('/<item>/delete', methods=['POST', 'GET'])
def deleteItem(item):
    session = Session()
    selectedItem = session.query(Item).filter_by(name=item).one()
    if 'username' not in login_session or login_session['username'] is None:
        Session.remove()
        return redirect(url_for('index'))
    # don't delete other people's stuff!
    elif login_session['username'] != selectedItem.user.username:
        Session.remove()
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            session.delete(selectedItem)
            session.commit()
            Session.remove()
            return redirect(url_for('index'))
        else:
            # Session.remove()
            # Defintiely no changing during deletes!
            return render_template('deleteItem.html', item=selectedItem)


@app.route('/catalog.json', methods=['GET'])
def getJSON():
    session = Session()
    categories = session.query(Category).all()
    x = {}

    x['Category'] = [i.serialize for i in categories]

    for j in x['Category']:
        items = session.query(Item).filter_by(category_id=int(j['id']))
        j['Item'] = [t.serialize for t in items]
    Session.remove()
    return jsonify(x)

@app.route('/catalog/item/<int:item_id>.json', methods=['GET'])
def getJSON2(item_id):
    session = Session()
    item = session.query(Item).filter_by(id=item_id).one()
    Session.remove()
    return jsonify(item.serialize)

@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


# Oauth login flow
# this might get verbose cause it confused me
@app.route('/oauth', methods=['POST'])
def login():
    session = Session()
    # STEP 1: parse the auth code
    auth_code = request.data
    # print('user auth_code: ' + str(auth_code))
    # STEP 2: exhange auth_code for google token
    try:
            # Upgrade the user's auth code into a credentials object
            # from google's server
            # print("stuff1")
        oauth_flow = flow_from_clientsecrets('client_secret.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        # print("stuff2")
        credentials = oauth_flow.step2_exchange(auth_code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorizate code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    # print("stuff")
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
    # Verify that the access token is for the user that made the request.
    # This is to help avoid forged requests by preventing a different
    # user from gaining acces from sending a malformed request
    # Warning! G+ is depreciated, but the api is still active
    # consider using a newer google sign-in code
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
                                 "Token's user ID doesn't match given" +
                                 "user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token for this applciation.
    # This also helps to avoid forged requests trying to
    # explot a preauthorized user on a different grabbing access to this
    # applciation
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does " +
                                            " not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already ' +
                                            'connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    # print("Access Token : %s " % credentials.access_token)
    # STEP 3: Find User or make a new one
    # Get user information
    h = httplib2.Http()
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    name = data['name']
    picture = data['picture']
    email = data['email']
    # See if user already exists in db, create a new if not
    user = session.query(User).filter_by(email=email).first()
    if not user:
        user = User(username=name, picture=picture, email=email)
        session.add(user)
        session.commit()
    # print("user: " + str(user.username))
    g.user = user
    login_session['username'] = name
    login_session['picture'] = picture
    login_session['email'] = email
    # STEP 4: Make token
    token = user.generate_auth_token(600)
    login_session['token'] = token
    login_session['access_token'] = credentials.access_token
    Session.remove()
    # flash("Now logged in as %s" % login_session['username'])
    # STEP 5: send something back to front end... or not
    return redirect(url_for('index'))


@app.route('/logout', methods=['POST'])
def logout():
    access_token = login_session['access_token']
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s',  access_token)
    u = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % (access_token)
    h = httplib2.Http()
    result = h.request(u, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        print('setting login_session to None')
        login_session['username'] = None
        flash("You have been been successfully logged out")
        return redirect(url_for('index'))
    else:
        response = make_response(json.dumps('Failed to revoke token for' +
                                            'given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        # flash("There was an error logging you out, please try again")
        return redirect(url_for('index'))


@auth.verify_password
def verify_password(username_or_token, password):
    session = Session()
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
    else:
        user = session.query(User).filter_by(
            username=username_or_token).first()
        if not user or not user.verify_password(password):
            Session.remove()
            return False
    g.user = user
    Session.remove()
    return True


if __name__ == '__main__':
    app.secret_key = 'dat_key_doe'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
