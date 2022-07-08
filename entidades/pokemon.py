from random import randint
from typing_extensions import Self
from controllers.constantes.constantes import BatalhaPokemom


class HabilidadePokemon():
    def __init__(self):
        self.id = 0
        self.nome = ''
        self.chance_acerto = 0
        self.tipo_dano = ''
        self.poder = 0
        self.is_especial = False
        self.efeito = ''
        self.causa_stun = False


class Pokemon():
    def __init__(self):
        self.id = 0
        self.nome = ''
        self.imagem = ''
        self.arte_oficial = ''
        self.imagem_costas = ''
        self.tamanho = 0
        self.peso = 0
        self.tipo = []
        self.debuffs = []
        self.stunado = False

        # Status do pokemon
        self.hp = 0
        self.ataque = 0
        self.defesa = 0
        self.velocidade = 0
        self.especial_ataque = 0
        self.especial_defesa = 0

        # Lista de habilidades do Pokemon
        self.habilidades = []

        # Lista de danos que o pokemon toma
        self.dano_dobrado = []
        self.dano_medio = []
        self.dano_reduzido = []

    def add_habilidade(self, habilidade: HabilidadePokemon):
        ''' Add um objeto contendo informações de cada habilidade do pokemon '''
        self.habilidades.append(habilidade)

    def calcula_dano(self, habilidade: HabilidadePokemon, inimigo: Self):
        ''' Calcula a quantidade de dano '''
        multiplicador_dano = 1

        # calcula a váriavel de dano pelo tipo
        if habilidade.tipo_dano in inimigo.dano_dobrado:
            multiplicador_dano = 2
        elif habilidade.tipo_dano in inimigo.dano_medio:
            multiplicador_dano = 0.5
        elif habilidade.tipo_dano in inimigo.dano_reduzido:
            multiplicador_dano = 0.5

        if habilidade.is_especial:
            return round((((((2 / 5+2) * self.especial_ataque * habilidade.poder / inimigo.especial_defesa) / 40) + 2) * multiplicador_dano))
        else:
            return round(((((2 / 5+2) * self.ataque * habilidade.poder / inimigo.defesa) / 40) + 2) * multiplicador_dano)

    def calcula_chance_acerto(self, habilidade: HabilidadePokemon) -> bool:
        ''' Verifica se o pokemon irá atingir o alvo '''
        numero_sorteio = randint(0, 100)

        return habilidade.chance_acerto <= numero_sorteio

    def verifica_stun(self, inimigo: Self, habilidade: HabilidadePokemon) -> bool:
        numero_sorteio = randint(0, 100)

        if numero_sorteio <= 80 and habilidade.causa_stun:
            inimigo.stunado = True
            return True

        return False

    def atacar(self, inimigo: Self, habilidade: HabilidadePokemon):
        ''' Ataca um pokemon inimigo reduzindo a vida '''
        print(habilidade.efeito)
        info_debuff = ''

        if len(self.debuffs) != 0:
            for debuff in self.debuffs:
                vida = self.get_hp()
                dano = self.calcula_dano(habilidade=debuff, inimigo=self)
                dano_debuff = round(dano / 100 * 35)
                self.set_hp(vida - dano_debuff)

                info_debuff += BatalhaPokemom.INFO_DEBBUF.format(
                    self.get_nome(), dano_debuff, debuff.nome)

        if self.stunado:
            self.stunado = False
            return BatalhaPokemom.STUNADO.format(self.get_nome()) + info_debuff

        # verifica se o pokemon acertou
        if self.calcula_chance_acerto(habilidade):
            return BatalhaPokemom.ERROU.format(self.get_nome(), habilidade.nome)

        if self.verifica_stun(inimigo, habilidade):
            info_debuff += BatalhaPokemom.STUN.format(inimigo.get_nome())

        return self.trata_efeito_habilidade(habilidade, inimigo, info_debuff)

    def trata_efeito_habilidade(self, habilidade: HabilidadePokemon, inimigo: Self, info_debuff=''):
        ''' Trata as habilidades com efeitos especiais '''
        if habilidade.efeito == 'damage' or habilidade.efeito == 'unique':
            vida_inimigo = inimigo.get_hp()
            dano = self.calcula_dano(habilidade=habilidade, inimigo=inimigo)
            inimigo.set_hp(vida_inimigo - dano)

            return BatalhaPokemom.DANO.format(self.get_nome(), habilidade.nome, dano) + info_debuff

        if habilidade.efeito == 'heal':
            vida = self.get_hp()
            heal = self.calcula_dano(habilidade=habilidade, inimigo=inimigo)
            self.set_hp(vida + heal)

            return BatalhaPokemom.HEAL.format(self.get_nome(), habilidade.nome, heal) + info_debuff

        if habilidade.efeito == 'damage+ailment':
            vida_inimigo = inimigo.get_hp()
            dano = self.calcula_dano(habilidade=habilidade, inimigo=inimigo)
            inimigo.set_hp(vida_inimigo - dano)
            inimigo.debuffs.append(habilidade)

            return BatalhaPokemom.DANO_DEBBUF.format(self.get_nome(), habilidade.nome, dano) + info_debuff

        if habilidade.efeito == 'damage+lower':
            vida_inimigo = inimigo.get_hp()
            dano = self.calcula_dano(habilidade=habilidade, inimigo=inimigo)
            inimigo.set_hp(vida_inimigo - dano)

            # reduz armadura do inimigo
            defesa = inimigo.get_defesa()
            especial_defesa = inimigo.get_especial_defesa()

            porcentagem_defesa = defesa / 100 * 30
            porcentagem_especial_defesa = especial_defesa / 100 * 30

            inimigo.set_defesa(defesa - porcentagem_defesa)
            inimigo.set_especial_defesa(
                especial_defesa - porcentagem_especial_defesa)

            return BatalhaPokemom.DANO_REDUCAO.format(self.get_nome(), habilidade.nome, dano) + info_debuff

        if habilidade.efeito == 'ailment':
            inimigo.debuffs.append(habilidade)

            return BatalhaPokemom.DEBBUF.format(self.get_nome(), habilidade.nome) + info_debuff

        if habilidade.efeito == 'damage+raise':
            vida_inimigo = inimigo.get_hp()
            dano = self.calcula_dano(habilidade=habilidade, inimigo=inimigo)
            inimigo.set_hp(vida_inimigo - dano)

            # aumenta os status do pokemon
            ataque = self.get_ataque()
            especial_ataque = self.get_especial_ataque()

            porcentagem_ataque = ataque / 100 * 30
            porcentagem_ataque_especial = especial_ataque / 100 * 30

            self.set_ataque(ataque + porcentagem_ataque)
            self.set_especial_ataque(
                especial_ataque + porcentagem_ataque_especial)

            return BatalhaPokemom.DANO_AUMENTO.format(self.get_nome(), habilidade.nome, dano) + info_debuff

        if habilidade.efeito == 'damage+heal':
            vida_inimigo = inimigo.get_hp()
            vida = self.get_hp()

            heal_dano = self.calcula_dano(
                habilidade=habilidade, inimigo=inimigo)

            self.set_hp(vida + heal_dano)
            inimigo.set_hp(vida_inimigo - heal_dano)

            return BatalhaPokemom.DANO_HEAL.format(self.get_nome(), habilidade.nome, heal_dano) + info_debuff

        if habilidade.efeito == 'ohko':
            vida = inimigo.get_hp()
            inimigo.set_hp(vida - vida)

            return BatalhaPokemom.OKO.format(self.get_nome(), habilidade.nome) + info_debuff

    # Getters e setters

    def get_nome(self):
        return self.nome

    def get_imagem(self):
        return self.imagem

    def get_arte_oficial(self):
        return self.arte_oficial

    def get_tamanho(self):
        return self.tamanho

    def get_peso(self):
        return self.peso

    def get_tipo(self):
        return self.tipo

    def get_hp(self):
        return self.hp

    def get_imagem_costas(self):
        return self.imagem_costas

    def get_dano_dobrado(self):
        return self.dano_dobrado

    def get_dano_medio(self):
        return self.dano_medio

    def get_dano_reduzido(self):
        return self.dano_reduzido

    def get_defesa(self):
        return self.defesa

    def get_especial_defesa(self):
        return self.especial_defesa

    def get_ataque(self):
        return self.ataque

    def get_especial_ataque(self):
        return self.especial_ataque

    def set_nome(self, value):
        self.nome = value

    def set_imagem(self, value):
        self.imagem = value

    def set_arte_oficial(self, value):
        self.arte_oficial = value

    def set_tamanho(self, value):
        self.tamanho = value

    def set_peso(self, value):
        self.peso = value

    def set_tipo(self, value):
        self.tipo = value

    def set_hp(self, value):
        self.hp = value

    def set_dano_dobrado(self, value):
        self.dano_dobrado.append(value)

    def set_dano_medio(self, value):
        self.dano_medio.append(value)

    def set_imagem_costas(self, value):
        self.imagem_costas = value

    def set_dano_reduzido(self, value):
        self.dano_reduzido = value

    def set_defesa(self, value):
        self.defesa = value

    def set_especial_defesa(self, value):
        self.especial_defesa = value

    def set_ataque(self, value):
        self.ataque = value

    def set_especial_ataque(self, value):
        self.especial_ataque = value
