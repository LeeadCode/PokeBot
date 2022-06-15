import requests
import random
from entidades.pokemon import Pokemon, HabilidadePokemon


class ControllerPokemon():
    def __init__(self):
        self.pokemons = []

    async def add_habilidade(self, pokemon: Pokemon, data):

        while len(pokemon.habilidades) < 10:
            item = data[random.randint(0, len(data) -1)] 

            request = requests.get(item['move']['url']).json()

            poder = request['power']
            tipo_dano = request['type']['name']
            status = request['damage_class']['name']
            causa_stun = request['meta']['ailment']['name']
            habilidades_stun = ['paralysis','sleep','freeze','confusion','trap','perish-song']
            chance_acerto = request['accuracy']
                
            if status == 'status':
                continue   

            if poder == None:
                continue 

            if tipo_dano not in pokemon.tipo:
                continue

            habilidade = HabilidadePokemon()

            habilidade.id = request['id']
            habilidade.nome = item['move']['name']
            habilidade.tipo_dano = tipo_dano
            habilidade.poder = request['power']
            habilidade.efeito = request['meta']['category']['name']

            if chance_acerto == None:
                habilidade.chance_acerto = 100
            else: 
                habilidade.chance_acerto = chance_acerto

            # verifica se a habilidade é especial
            if not status == 'physical':
                habilidade.is_especial = True

            # verifica se a habilidade stuna
            if causa_stun in habilidades_stun:
                habilidade.causa_stun = True
     
            pokemon.add_habilidade(habilidade)
            
            habilidade = None

        print(pokemon.habilidades)

    async def get_pokemon(self, nome_pokemon, get_status=True, get_poder=True, get_relacao_dano=True) -> Pokemon:
        request = requests.get(
            'https://pokeapi.co/api/v2/pokemon/{}'.format(nome_pokemon)).json()

        pokemon = Pokemon()
        pokemon.id = request['id']
        pokemon.nome = request['name']
        pokemon.imagem = request['sprites']['front_default']
        pokemon.arte_oficial = request['sprites']['other']['official-artwork']['front_default']
        pokemon.imagem_costas = request['sprites']['back_default']
        pokemon.tamanho = request['height']
        pokemon.peso = request['weight']

        # pega os tipos
        tipos = request['types']

        for tipo in tipos:
            pokemon.tipo.append(tipo['type']['name']) 

        if get_status:
            status_pokemon = request['stats']
            pokemon.hp = status_pokemon[0]['base_stat']
            pokemon.ataque = status_pokemon[1]['base_stat']
            pokemon.defesa = status_pokemon[2]['base_stat']
            pokemon.especial_ataque = status_pokemon[3]['base_stat']
            pokemon.especial_defesa = status_pokemon[4]['base_stat']
            pokemon.velocidade = status_pokemon[5]['base_stat']

        if get_poder:
            habilidade_pokemon = request['moves']
            await self.add_habilidade(data=habilidade_pokemon, pokemon=pokemon)

        if get_relacao_dano:
            request = requests.get(
                'https://pokeapi.co/api/v2/type/{}'.format(tipo['type']['name'])).json()

            data_dano_dobrado = request['damage_relations']['double_damage_from']
            data_dano_medio = request['damage_relations']['half_damage_from']
            data_dano_reduzido = request['damage_relations']['no_damage_from']

            for tipo in data_dano_dobrado:
                pokemon.set_dano_dobrado(tipo['name'])

            for tipo in data_dano_medio:
                pokemon.set_dano_medio(tipo['name'])

            for tipo in data_dano_reduzido:
                pokemon.set_dano_reduzido(tipo['name'])

        return pokemon

    @staticmethod
    def get_pokemon_aleatorio(quantidade):
        pokemons = []

        request = requests.get(
            'https://pokeapi.co/api/v2/pokemon?offset=0&limit=151').json()
        data = request['results']

        for i in range(quantidade):
            pokemons.append(data[random.randint(0, 151) - 1]['name'])

        return pokemons

    @classmethod
    def get_imagem_tipo(self, pokemon : Pokemon):
        ''' Retorna imagem do tipo '''
        tipos_pokemon = {
            'bug': 964517132874436698,
            'ice': 964517301091184700,
            'rock': 964517346033143889,
            'fire': 964516119065014312,
            'dark': 964517163178291210,
            'fairy': 964532249825538048,
            'steel': 964517358460891156,
            'water': 964517371660337243,
            'ghost': 964517277120725053,
            'grass': 964517288852197376,
            'normal': 964517312436776960,
            'dragon': 964517198360109087,
            'flying': 964517261715079188,
            'psychic': 964517325858562138,
            'electric': 964517216127156264,
            'fighting': 964517235093815298,
            'poison': 964554085099532318,
            'ground': 964554609916006450
        }
    
        resultado = []

        tipos = pokemon.get_tipo()

        for tipo in tipos:
            resultado.append(tipos_pokemon[tipo])

        return resultado