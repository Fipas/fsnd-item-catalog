from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response
from flask_toastr import Toastr
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Game, User
from flask import session as login_session
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_dance.contrib.google import make_google_blueprint, google
import functools
import os
import random
import string
import requests
import json

app = Flask(__name__)
app.secret_key = 'super_secret_key'
toastr = Toastr(app)

# Connect to Database and create database session
engine = create_engine('postgresql+psycopg2://catalog_admin:catalog_admin_password@localhost/catalog_db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Allow OAuth on http
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

# Configure facebook OAuth
app.config["FACEBOOK_OAUTH_CLIENT_ID"] = '2252988094796731'
app.config["FACEBOOK_OAUTH_CLIENT_SECRET"] = '7ba225c3065f191b744301e8b55db1eb'
facebook_bp = make_facebook_blueprint(scope=['email'], redirect_to='login_facebook')
app.register_blueprint(facebook_bp)

app.config["GOOGLE_OAUTH_CLIENT_ID"] = '214897511770-56qt4huj6864ds1cf2g5l260sfa9c88h.apps.googleusercontent.com'
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = '-MlaOE56H8qUqRoINr6UsHHY'
google_bp = make_google_blueprint(scope=["email profile"], redirect_to='login_google')
app.register_blueprint(google_bp)


# Loading categories to build pages. Categories are static.
categories = categories = session.query(Category).all()
@app.context_processor
def inject_categories():
    return {'categories': categories}

# Injecting session
@app.context_processor
def inject_session():
    return {'session': login_session}

# Login decorator
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in login_session:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view


@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/login/facebook', methods=['GET', 'POST'])
def login_facebook():
    if not facebook.authorized:
        return redirect(url_for("facebook.login"))

    try:
        resp = facebook.get("/me?fields=id,name,picture,email")
        assert resp.ok, resp.text
    except:
        return redirect(url_for("facebook.login"))

    login_session['provider'] = 'facebook'
    login_session['username'] = resp.json()['name']
    login_session['email'] = resp.json()['email']
    login_session['facebook_id'] = resp.json()['id']
    login_session['picture'] = resp.json()['picture']['data']['url']

    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    flash('Login successful. Welcome %s!' % login_session['username'], 'success')

    return redirect(url_for('get_games'))


@app.route('/login/google', methods=['GET', 'POST'])
def login_google():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text
    #return "You are {} on Google".format(resp.json())

    login_session['provider'] = 'google'
    login_session['username'] = resp.json()['name']
    login_session['email'] = resp.json()['email']
    login_session['google_id'] = resp.json()['id']
    login_session['picture'] = resp.json()['picture']

    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    flash('Login successful. Welcome %s!' % login_session['username'], 'success')

    return redirect(url_for('get_games'))


@login_required
@app.route('/logout')
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'facebook':
            facebook_logout()
            del login_session['facebook_id']

        if login_session['provider'] == 'google':
            google_logout()
            del login_session['google_id']

        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.", 'success')
        return redirect(url_for('get_games'))
    else:
        pass


def facebook_logout():
    facebook_id = login_session['facebook_id']
    access_token = facebook_bp.token['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    requests.delete(url)
    del facebook_bp.token


def google_logout():
    token = google_bp.token["access_token"]
    resp = google.post(
        "https://accounts.google.com/o/oauth2/revoke",
        params={"token": token},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    #assert resp.ok, resp.text
    del google_bp.token  # Delete


def create_user(login_session):
    new_user = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/')
@app.route('/games/')
def get_games():
    games = session.query(Game).order_by(Game.id.desc()).limit(10).all()
    return render_template('games.html', games=games)


@login_required
@app.route('/games/new', methods=['GET', 'POST'])
def add_game():
    if request.method == 'GET':
        return render_template('add_game.html')

    if request.method == 'POST':
        print(request.form)
        game = Game(name=request.form['name'],
                    description=request.form['description'],
                    category_id=request.form['category'],
                    user_id=login_session['user_id'])
        session.add(game)
        session.commit()
        flash("New game added!", 'success')
        return redirect(url_for('get_games'))


@login_required
@app.route('/games/update/<int:game_id>', methods=['GET', 'POST'])
def update_game(game_id):
    game = session.query(Game).filter_by(id=game_id).one()

    if request.method == 'GET':
        return render_template('update_game.html', game=game)

    if request.method == 'POST':
        if request.form['name']:
            game.name = request.form['name']
        if request.form['description']:
            game.description = request.form['description']
        if request.form['category']:
            game.category_id = request.form['category']
        session.add(game)
        session.commit()
        flash('Game successfully updated!', 'success')
        return redirect(url_for('get_games'))


@login_required
@app.route('/games/delete/<int:game_id>', methods=['GET', 'POST'])
def delete_game(game_id):
    game = session.query(Game).filter_by(id=game_id).one()

    if request.method == 'GET':
        return render_template('delete_game.html', game=game)

    if request.method == 'POST':
        session.delete(game)
        session.commit()
        flash('Game successfully deleted!', 'success')
        return redirect(url_for('get_games'))


@app.route('/games/category/<int:category_id>/')
def get_games_by_category(category_id):
    categories = session.query(Category).all()
    games = session.query(Game).filter(Game.category_id == category_id).order_by(Game.id.desc()).all()

    for category in categories:
        if category.id == category_id:
            chosen_category = category
            break

    return render_template('games.html', games=games, categories=categories, chosen_category=chosen_category)


# JSON API Endpoints
@app.route('/games/json')
def get_games_json():
    games = session.query(Game).all()
    return jsonify(Games=[game.serialize for game in games])


@app.route('/games/<int:game_id>/json')
def get_game_json(game_id):
    game = session.query(Game).filter_by(id=game_id).one()
    return jsonify(Games=game.serialize)


@app.route('/games/category/<int:category_id>/json')
def get_games_by_category_json(category_id):
    games = session.query(Game).filter_by(category_id=category_id).all()
    return jsonify(Games=[game.serialize for game in games])


@app.route('/categories/json')
def get_categories_json():
    return jsonify(Categories=[category.serialize for category in categories])


@app.route('/users/json')
def get_users_json():
    users = session.query(User).all()
    return jsonify(Users=[user.serialize for user in users])


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0')
