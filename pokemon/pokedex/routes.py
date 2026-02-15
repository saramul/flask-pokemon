from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from pokemon.extension import db
from pokemon.models import Pokemon, PokemonType, User

pokedex_bp = Blueprint('pokedex', __name__, template_folder='templates')

@pokedex_bp.route('/')
@login_required
def index():
  query = db.select(Pokemon).where(Pokemon.user_id==current_user.id)
  pokemons = db.session.scalars(query).all()
  return render_template('pokedex/index.html', title='Pokedex Page', pokemons=pokemons)

@pokedex_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_pokemon():
  query = db.select(PokemonType)
  pokemon_types = db.session.scalars(query).all()
  if request.method == 'POST':
    name = request.form.get('name')
    weight = request.form.get('weight')
    height = request.form.get('height')
    description = request.form.get('description')
    img_url = request.form.get('img_url')
    pokemon_types = request.form.getlist('pokemon_types')

    query = db.select(Pokemon).where(Pokemon.name == name)
    pokemon = db.session.scalar(query)
    if pokemon:
      flash(f'Pokemon: {name} is already exist!', 'warning')
      return redirect(url_for('pokedex.new_pokemon'))
    else:
      p_types = []
      for id in pokemon_types:
        p_types.append(db.session.get(PokemonType, id))

      pokemon = Pokemon(name=name, weight=weight, height=height, description=description,
                        img_url=img_url, editor=current_user, types=p_types)
      db.session.add(pokemon)
      db.session.commit()
      flash('Add new pokemon successfully!', 'success')
      return redirect(url_for('pokedex.index'))
    
  return render_template('pokedex/new_pokemon.html', title='New Pokemon Page', pokemon_types=pokemon_types)