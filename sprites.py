import random
import pygame
from config import (LARGURA, ALTURA, VELOCIDADE_ANIMACAO, INICIO, GONGO, DIRECOES,
                    LANCADOR_X, LANCADOR_Y, SAMURAI_X, PE_DO_SAMURAI,
                    PRETO, DOURADO, AMARELO, VERMELHO, LARANJA, CINZA)
from desenho import fazer_estrela, desenha_estrela


def eh_parede(mapa, x, y):
    # Olha a COR do mapa de colisão nesse ponto. Branco = chão, preto = parede.
    if x < 0 or x >= LARGURA or y < 0 or y >= ALTURA:      # fora da tela = parede
        return True
    cor = mapa.get_at((int(x), int(y)))                     # cor = (vermelho, verde, azul, transparência)
    return cor[0] < 128                                     # escuro (perto do preto) = parede



class Personagem(pygame.sprite.Sprite):
    # Um personagem animado PARADO num lugar (tela de escolha, templo, vitória).
    def __init__(self, assets, nome, x, y, escala=1, estado="parado"):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Aumenta as imagens UMA vez só, aqui no começo
        self.animacoes = {}
        for nome_estado in assets["personagens"][nome]:
            lista = []
            for imagem in assets["personagens"][nome][nome_estado]:
                lista.append(pygame.transform.scale(imagem, (32 * escala, 32 * escala)))
            self.animacoes[nome_estado] = lista

        self.estado = estado              # "parado", "andando" ou "correndo"
        self.esquerda = False             # olhando pra esquerda?
        self.frame = 0                    # qual imagem da animação está aparecendo
        self.ultima_troca = pygame.time.get_ticks()

        self.image = self.animacoes[self.estado][0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def mudar_estado(self, novo_estado):
        if novo_estado != self.estado:
            self.estado = novo_estado
            self.frame = 0                # começa a nova animação do início

    def animar(self):
        # Mesma ideia da Explosion da Navinha: troca de imagem de tempos em tempos
        agora = pygame.time.get_ticks()
        if agora - self.ultima_troca > VELOCIDADE_ANIMACAO[self.estado]:
            self.ultima_troca = agora
            self.frame = self.frame + 1

        lista = self.animacoes[self.estado]
        self.frame = self.frame % len(lista)      # chegou no fim? volta pro começo
        imagem = lista[self.frame]
        if self.esquerda:
            imagem = pygame.transform.flip(imagem, True, False)   # espelha na horizontal

        centro = self.rect.center                 # guarda o centro pra imagem não "pular"
        self.image = imagem
        self.rect = self.image.get_rect()
        self.rect.center = centro

    def update(self):
        self.animar()


class Ninja(Personagem):
    # O personagem que ANDA no labirinto.
    # "Ninja(Personagem)" = o Ninja é um Personagem, com tudo que ele tem,
    # mais o movimento pelas setas.
    def __init__(self, assets, nome):
        Personagem.__init__(self, assets, nome, INICIO[0], INICIO[1])
        self.mapa = assets["mapa"]
        self.radius = 8                   # tamanho do "círculo de colisão"

    def voltar_pro_inicio(self):
        self.rect.center = INICIO

    def update(self):
        teclas = pygame.key.get_pressed()
        correndo = teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]
        if correndo:
            passo = 5
        else:
            passo = 3

        dx = 0
        dy = 0
        if teclas[pygame.K_LEFT]:
            dx = -passo
        if teclas[pygame.K_RIGHT]:
            dx = passo
        if teclas[pygame.K_UP]:
            dy = -passo
        if teclas[pygame.K_DOWN]:
            dy = passo

        # qual animação usar
        if dx == 0 and dy == 0:
            self.mudar_estado("parado")
        elif correndo:
            self.mudar_estado("correndo")
        else:
            self.mudar_estado("andando")
        if dx < 0:
            self.esquerda = True
        if dx > 0:
            self.esquerda = False

        # olha a cor do MAPA um pouco à frente (3 passos); se for parede, não anda
        x, y = self.rect.center
        if not eh_parede(self.mapa, x + dx * 3, y + dy * 3):
            x = x + dx
            y = y + dy
        # se não deu na diagonal, tenta só pro lado ou só pra cima/baixo ("escorrega" na parede)
        elif dx != 0 and not eh_parede(self.mapa, x + dx * 3, y):
            x = x + dx
        elif dy != 0 and not eh_parede(self.mapa, x, y + dy * 3):
            y = y + dy
        self.rect.center = (x, y)

        self.animar()

class BolaDeFogo(pygame.sprite.Sprite):
    def __init__(self, assets, x, y, velocidade):
        pygame.sprite.Sprite.__init__(self)
        self.mapa = assets["mapa"]
        # guardamos x e y com vírgula (1.6, 1.8...) porque o rect só aceita número inteiro
        self.x = x
        self.y = y
        self.dx, self.dy = random.choice(DIRECOES)
        self.velocidade = velocidade
        self.radius = 8

        # desenho da bola: 3 círculos, um dentro do outro (feito uma vez só)
        self.image = pygame.Surface((26, 26), pygame.SRCALPHA)   # SRCALPHA = fundo transparente
        pygame.draw.circle(self.image, VERMELHO, (13, 13), 10)
        pygame.draw.circle(self.image, LARANJA, (13, 13), 7)
        pygame.draw.circle(self.image, AMARELO, (13, 13), 3)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def livre(self, dx, dy):
        # a bola pode ir nessa direção? olha 4, 8 e 12 pixels à frente
        for passo in [4, 8, 12]:
            if eh_parede(self.mapa, self.x + dx * passo, self.y + dy * passo):
                return False
        return True

    def update(self):
        # vai bater (ou 1% de chance de mudar sozinha)? sorteia outra direção livre
        if not self.livre(self.dx, self.dy) or random.random() < 0.01:
            livres = []
            for d in DIRECOES:
                voltando = d[0] == -self.dx and d[1] == -self.dy    # é por onde ela veio?
                if self.livre(d[0], d[1]) and not voltando:
                    livres.append(d)
            if len(livres) == 0:                                    # beco sem saída
                livres = [(-self.dx, -self.dy)]                     # então volta
            self.dx, self.dy = random.choice(livres)

        if self.livre(self.dx, self.dy):
            self.x = self.x + self.dx * self.velocidade
            self.y = self.y + self.dy * self.velocidade
        self.rect.center = (int(self.x), int(self.y))


class Estrela(pygame.sprite.Sprite):
    # Estrela ninja girando no chão do labirinto
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 10
        self.original = fazer_estrela()       # a imagem "reta", sem girar
        self.angulo = 0
        self.image = self.original
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # gira 3 graus por quadro (sempre a partir da original, pra não borrar)
        self.angulo = self.angulo + 3
        centro = self.rect.center
        self.image = pygame.transform.rotate(self.original, self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = centro


class Gongo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.aberto = False               # vira True quando pegar todas as estrelas
        self.radius = 12

        # imagem do gongo FECHADO: cinza com cadeado
        self.imagem_fechado = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.imagem_fechado, CINZA, (15, 15), 15)
        pygame.draw.rect(self.imagem_fechado, PRETO, (10, 12, 10, 9))
        pygame.draw.circle(self.imagem_fechado, PRETO, (15, 11), 4, 2)

        # imagem do gongo ABERTO: dourado com o meio vermelho
        self.imagem_aberto = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.imagem_aberto, DOURADO, (15, 15), 15)
        pygame.draw.circle(self.imagem_aberto, VERMELHO, (15, 15), 7)

        self.image = self.imagem_fechado
        self.rect = self.image.get_rect()
        self.rect.center = GONGO

    def update(self):
        if self.aberto:
            self.image = self.imagem_aberto
        else:
            self.image = self.imagem_fechado


#fase 2 templo
class Buraco(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.cheio = False                # já tem estrela?
        self.destacado = False            # o mouse está em cima?
        self.armadilha = False            # é o buraco que faz o samurai pular?
        self.revelado = False             # já mostrou que era a armadilha?
        self.image = pygame.Surface((56, 56), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, PRETO, (28, 28), 20)
        if self.revelado:
            pygame.draw.circle(self.image, VERMELHO, (28, 28), 24, 5)   # era a armadilha!
        elif self.destacado:
            pygame.draw.circle(self.image, AMARELO, (28, 28), 24, 4)
        else:
            pygame.draw.circle(self.image, DOURADO, (28, 28), 22, 3)
        if self.cheio:
            desenha_estrela(self.image, 28, 28, 20)


class EstrelaVoando(pygame.sprite.Sprite):
    # A estrela que sai da mão do personagem e voa (em arco) até o buraco
    def __init__(self, buraco):
        pygame.sprite.Sprite.__init__(self)
        self.buraco = buraco              # para qual buraco ela vai
        self.progresso = 0                # 0 = saiu da mão, 1 = chegou
        self.chegou = False
        self.angulo = 0
        self.image = pygame.Surface((44, 44), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (LANCADOR_X, LANCADOR_Y)

    def update(self):
        self.progresso = self.progresso + 0.04
        if self.progresso >= 1:
            self.chegou = True
            self.kill()                   # some da tela (sai de todos os grupos)
            return

        p = self.progresso
        alvo_x, alvo_y = self.buraco.rect.center
        x = LANCADOR_X + (alvo_x - LANCADOR_X) * p
        y = LANCADOR_Y + (alvo_y - LANCADOR_Y) * p
        # o ARCO: p * (1 - p) vale 0 no começo, 0 no fim e o máximo no meio,
        # então a estrela sobe e depois desce até o buraco
        y = y - p * (1 - p) * 4 * 120
        self.rect.center = (int(x), int(y))

        self.angulo = self.angulo + 16        # gira rápido enquanto voa
        self.image.fill((0, 0, 0, 0))
        desenha_estrela(self.image, 22, 22, self.angulo, 1.5)


class Samurai(pygame.sprite.Sprite):
    # O Resina cabeção em cima do templo, fazendo caretas
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)
        self.caretas = {}
        for nome in assets["caretas"]:
            self.caretas[nome] = pygame.transform.scale(assets["caretas"][nome], (144, 144))  # 3x maior

        self.pulou = False
        self.momento_do_pulo = 0
        self.velocidade_y = 0             # velocidade do pulo (negativo = subindo)
        self.preocupado = False           # True enquanto uma estrela está voando

        self.image = self.caretas["desconfiado"]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SAMURAI_X, PE_DO_SAMURAI)   # midbottom = meio do pé

    def pular(self):
        self.pulou = True
        self.momento_do_pulo = pygame.time.get_ticks()
        self.velocidade_y = -15           # dá um impulso pra CIMA

    def segundos_desde_o_pulo(self):
        return (pygame.time.get_ticks() - self.momento_do_pulo) / 1000

    def update(self):
        agora = pygame.time.get_ticks()
        if self.pulou:
            # PULO: a cada quadro ele anda a velocidade, e a "gravidade"
            # vai puxando pra baixo (a velocidade aumenta um pouquinho)
            self.image = self.caretas["kiai"]
            self.rect.y = self.rect.y + self.velocidade_y
            self.velocidade_y = self.velocidade_y + 0.17
        else:
            if self.preocupado:
                careta = "dentes"
            elif (agora // 1500) % 2 == 0:
                careta = "desconfiado"
            else:
                careta = "bravo"
            # treme pro lado: troca entre +2 e -2 a cada 80 ms
            if (agora // 80) % 2 == 0:
                tremida = 2
            else:
                tremida = -2
            self.image = self.caretas[careta]
            self.rect = self.image.get_rect()
            self.rect.midbottom = (SAMURAI_X + tremida, PE_DO_SAMURAI)
