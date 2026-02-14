pokemon_types = [
  'Grass', 'Poison', 'Fire', 'Flying', 'Water',
  'Bug', 'Normal', 'Electric', 'Ground', 'Fairy',
  'Fighting', 'Psychic', 'Rock', 'Steel', 'Ice',
  'Ghost', 'Dragon', 'Dark'
]

from pokemon.models import PokemonType
types = [PokemonType(name=name) for name in pokemon_types]

