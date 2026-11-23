import pygame
from config import FPS, CX, CY, ALTURA, DOURADO, BRANCO, NOMES, ESCOLHA, LABIRINTO, SAIR
from sprites import Personagem
from desenho import escreve, painel

#telha escolha -> a 1ª tela, de escolha de personagens 
def tela_escolha(tela, assets, dados):
    relogio = pygame.time.Clock()

    # Grupo com os 3 personagens
    personagens = pygame.sprite.Group()
    personagens.add(Personagem(assets, "ninja1", CX - 200, CY - 10, 4))   # 4 = quatro vezes maior
    personagens.add(Personagem(assets, "ninja2", CX, CY - 10, 4))
    personagens.add(Personagem(assets, "samurai", CX + 200, CY - 10, 4))

    estado = ESCOLHA
    while estado == ESCOLHA:
        relogio.tick(FPS)


