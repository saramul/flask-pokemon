from pokemon.extension import db, login_manager
from flask_login import UserMixin
from sqlalchemy import String, Integer, ForeignKey, Text, DateTime, Table, Column, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime

# from pokemon import login_manager

@login_manager.user_loader
def load_user(user_id):
  return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
  email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
  password: Mapped[str] = mapped_column(String, nullable=False)
  firstname: Mapped[str] = mapped_column(String, nullable=True)
  lastname: Mapped[str] = mapped_column(String, nullable=True)
  avatar: Mapped[str] = mapped_column(String(50), nullable=False, default='default.png')
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=True)
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

  pokemons: Mapped[List['Pokemon']] = relationship(back_populates='editor')
  
  def __repr__(self):
    return f'<User: {self.username}>'
  
pokedex = Table(
  'pokedex',
  db.metadata,
  Column('type_id', Integer, ForeignKey('pokemon_type.id'), primary_key=True),
  Column('pokemon_id', Integer, ForeignKey('pokemon.id'), primary_key=True)
)

class PokemonType(db.Model):
  __tablename__ = 'pokemon_type'
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

  pokemons: Mapped[List['Pokemon']] = relationship(back_populates='types', secondary=pokedex)

  def __repr__(self):
    return f'<PokemonType: {self.name}>'
  
class Pokemon(db.Model):
  __tablename__ = 'pokemon'
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
  weight: Mapped[str] = mapped_column(String(25), nullable=False)
  height: Mapped[str] = mapped_column(String(25), nullable=False)
  description: Mapped[str] = mapped_column(Text, nullable=False)
  img_url: Mapped[str] = mapped_column(Text, nullable=False)
  user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), index=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=True)
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

  types: Mapped[List[PokemonType]] = relationship(back_populates='pokemons', secondary=pokedex)
  editor: Mapped[User] = relationship(back_populates='pokemons')

  def __repr__(self):
    return f'<Pokemon: {self.name}>'
