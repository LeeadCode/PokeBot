type_to_emoji = {
    'Normal': '<:normalPokemon:964517312436776960>',
    'Fighting': '<:fightingPokemon:964517235093815298>',
    'Flying': '<:flyingPokemon:964517261715079188>',
    'Poison': '<:poisonPokemon:964554085099532318>',
    'Ground': '<:groundPokemon:964554609916006450>',
    'Rock': '<:rockPokemon:964517346033143889>',
    'Bug': '<:bugPokemon:964517132874436698>',
    'Ghost': '<:ghostPokemon:964517277120725053>',
    'Steel': '<:steelPokemon:964517358460891156>',
    'Fire': '<:firePokemon:964516119065014312>',
    'Water': '<:watherPokemon:964517371660337243>',
    'Grass': '<:grassPokemon:964517288852197376>',
    'Electric': '<:eletricPokemon:964517216127156264>',
    'Ice': '<:icePokemon:964517301091184700>',
    'Dragon': '<:dragonPokemon:964517198360109087>',
    'Dark': '<:darkPokemon:964517163178291210>',
    'Fairy': '<:fairyPokemon:964532249825538048>',
    'Psychic': '<:psychicPokemon:964517325858562138>',
}


def get_type_emojis(types):
    return ' '.join([type_to_emoji.get(type_, '') for type_ in types])
