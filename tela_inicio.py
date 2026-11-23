import pygame
import os
from config import FPS, ESCOLHA, SAIR, PASTA_IMAGENS


def tela_inicio(tela):
    relogio = pygame.time.Clock()

    capa = pygame.image.load(os.path.join(PASTA_IMAGENS, "começo.png")).convert()
    capa = pygame.transform.scale(capa, tela.get_size())

    while True:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return SAIR

            # Espaço sai da capa e abre a escolha
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return SAIR
                if evento.key == pygame.K_SPACE:
                    return ESCOLHA

        tela.blit(capa, (0, 0))
        pygame.display.flip()