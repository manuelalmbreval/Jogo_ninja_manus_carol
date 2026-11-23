import pygame
from config import FPS, ESCOLHA, SAIR


def tela_inicio(tela):
    relogio = pygame.time.Clock()

    capa = pygame.image.load("imagens/começo.png").convert()
    capa = pygame.transform.scale(capa, tela.get_size())

    while True:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return SAIR

            # Espaço sai da capa e abre a escolha
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return ESCOLHA

        tela.blit(capa, (0, 0))
        pygame.display.flip()