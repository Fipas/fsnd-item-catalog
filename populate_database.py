# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Game, Base, Category, User

engine = create_engine('postgresql+psycopg2://catalog_admin:catalog_admin_password@localhost/catalog_db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
user1 = User(name="Geralt of Rivia", email="whitewolf@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(user1)
session.commit()

# Adding categories
category1 = Category(name="RPG")
session.add(category1)
session.commit()

category2 = Category(name="Shooter")
session.add(category2)
session.commit()

category3 = Category(name="Adventure")
session.add(category3)
session.commit()

category4 = Category(name="RTS")
session.add(category4)
session.commit()

category5 = Category(name="Action")
session.add(category5)
session.commit()

category6 = Category(name="Fighting")
session.add(category6)
session.commit()

category7 = Category(name="Metroidvania")
session.add(category7)
session.commit()

category8 = Category(name="Racing")
session.add(category8)
session.commit()

# Adding some games

game1 = Game(user=user1, name="The Witcher 3: Wild Hunt", description="As war rages on throughout the Northern Realms, you take on the greatest contract of your life — tracking down the Child of Prophecy, a living weapon that can alter the shape of the world.", category=category1)
session.add(game1)
session.commit()

game2 = Game(user=user1, name="DRAGON QUEST XI: Echoes of an Elusive Age", description="DRAGON QUEST® XI: Echoes of an Elusive Age™ follows the perilous journey of a hunted Hero who must uncover the mystery of his fate with the aid of a charismatic cast of supporting characters.", category=category1)
session.add(game2)
session.commit()

game3 = Game(user=user1, name="Sekiro: Shadows Die Twice", description="Carve your own clever path to vengeance in an all-new adventure from developer FromSoftware, creators of Bloodborne and the Dark Souls series. Take Revenge. Restore your honor. Kill Ingeniously.", category=category5)
session.add(game3)
session.commit()

game4 = Game(user=user1, name="Mortal Kombat 11", description="Mortal Kombat is back and better than ever in the next evolution of the iconic franchise.", category=category6)
session.add(game4)
session.commit()

game5 = Game(user=user1, name="Katana ZERO", description="Katana ZERO is a stylish neo-noir, action-platformer featuring breakneck action and instant-death combat. Slash, dash, and manipulate time to unravel your past in a beautifully brutal acrobatic display.", category=category5)
session.add(game5)
session.commit()

game6 = Game(user=user1, name="Bloodstained: Ritual of the Night", description="Bloodstained: Ritual of the Night is an exploration-focused, side-scroller action RPG by Koji Igarashi. Play as Miriam, an orphan scarred by an alchemist's curse that slowly crystallizes her body. Battle through a demon-infested castle and defeat its master to save yourself, and all of humanity!", category=category7)
session.add(game6)
session.commit()


print("Added items to database!")
