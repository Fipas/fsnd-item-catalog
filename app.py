from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Game, User
from flask import session as login_session

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///gamecatalog.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/games/')
def show_all_games():
    categories = session.query(Category).all()
    games = session.query(Game).order_by(Game.id.desc()).limit(10).all()
    return render_template('games.html', games=games, categories=categories)

@app.route('/games/<int:category_id>/')
def show_games_by_category(category_id):
    categories = session.query(Category).all()
    games = session.query(Game).filter(Game.category_id == category_id).order_by(Game.id.desc()).all()

    for category in categories:
        if category.id == category_id:
            chosen_category = category
            break

    return render_template('games.html', games=games, categories=categories, chosen_category=chosen_category)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
