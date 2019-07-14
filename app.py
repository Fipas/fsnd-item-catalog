from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask_toastr import Toastr
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Game, User
from flask import session as login_session

app = Flask(__name__)
toastr = Toastr(app)

# Connect to Database and create database session
engine = create_engine('sqlite:///gamecatalog.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Loading categories to build pages. Categories are static.
categories = categories = session.query(Category).all()
@app.context_processor
def inject_categories():
    return {'categories': categories}

@app.route('/')
@app.route('/games/')
def get_games():
    games = session.query(Game).order_by(Game.id.desc()).limit(10).all()
    return render_template('games.html', games=games)

@app.route('/games/new', methods=['GET', 'POST'])
def add_game():
    if request.method == 'GET':
        return render_template('add_game.html')

    if request.method == 'POST':
        print(request.form)
        game = Game(name=request.form['name'],
                    description=request.form['description'],
                    category_id=request.form['category'],
                    user_id=1)
        session.add(game)
        session.commit()
        flash("New game added!", 'success')
        return redirect(url_for('get_games'))

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
@app.route('/games/JSON')
def get_games_JSON():
    games = session.query(Game).all()
    return jsonify(Games=[game.serialize for game in games])

@app.route('/games/<int:game_id>/JSON')
def get_game_JSON(game_id):
    game = session.query(Game).filter_by(id=game_id).one()
    return jsonify(Games=game.serialize)

@app.route('/games/category/<int:category_id>/JSON')
def get_games_by_category_JSON(category_id):
    games = session.query(Game).filter_by(category_id=category_id).all()
    return jsonify(Games=[game.serialize for game in games])

@app.route('/categories/JSON')
def get_categories_JSON():
    return jsonify(Categories=[category.serialize for category in categories])

@app.route('/users/JSON')
def get_users_JSON():
    users = session.query(User).all()
    return jsonify(Users=[user.serialize for user in users])




if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0')
