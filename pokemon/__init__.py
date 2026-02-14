import os
from flask import Flask
from pokemon.extension import db, migrate, login_manager, bcrypt
# from pokemon.models import User
from pokemon.core.routes import core_bp
from pokemon.users.routes import user_bp
from pokemon.pokedex.routes import pokedex_bp


def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
  app.secret_key = os.environ.get('MY_SECRET_KEY')
  # postgresql://pokemon_db_r8nk_user:JeY0BQmwQUw2BAOZFZoEvE4AUaij3muC@dpg-d682c30gjchc73bagsg0-a.oregon-postgres.render.com/pokemon_db_r8nk

  db.init_app(app)
  migrate.init_app(app, db)
  login_manager.init_app(app)
  bcrypt.init_app(app)

  app.register_blueprint(core_bp, url_prefix='/')
  app.register_blueprint(user_bp, url_prefix='/users')
  app.register_blueprint(pokedex_bp, url_prefix='/pokedex')

  return app