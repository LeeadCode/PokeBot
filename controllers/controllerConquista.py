import requests
import json
from entidades.usuarioDiscord import UsuarioDiscord
from entidades.conquista import Conquista


class ControllerConquista():
    def __init__(self):
        pass

    @classmethod
    def get_conquista(self, id) -> Conquista:
        url = f'https://biblebot-api.herokuapp.com/api/v1/Conquista/{id}'

        r = requests.get(url)

        if r.status_code != 200:
            return Conquista()

        r = r.json()

        conquista = Conquista()
        conquista.id = r['id']
        conquista.vitorias = r['vitorias']
        conquista.derrotas = r['derrotas']
        conquista.partidas = r['partidas']

        return conquista

    @classmethod
    def post_conquista(self, usuario: UsuarioDiscord, vitoria=False) -> Conquista:
        id = usuario.id

        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}
        payload = json.dumps({"id": id, "name": usuario.nome})

        if vitoria:
            url = 'https://biblebot-api.herokuapp.com/api/v1/Conquista/vitoria'
        else:
            url = 'https://biblebot-api.herokuapp.com/api/v1/Conquista/derrota'

        r = requests.post(url, data=payload, headers=headers).json()

        conquista = Conquista()
        conquista.id = r['id']
        conquista.vitorias = r['vitorias']
        conquista.derrotas = r['derrotas']
        conquista.partidas = r['partidas']

        return conquista
