# =====================================================================
#   tela_final.py  ->  a tela de VITÓRIA ou de GAME OVER
# =====================================================================
import pygame
from config import FPS, CX, CY, BRANCO, DOURADO, VERMELHO, NOMES, ESCOLHA, VITORIA, SAIR
from sprites import Personagem
from desenho import escreve, painel


def tela_final(tela, assets, dados, resultado):
    # resultado = VITORIA ou GAME_OVER
    relogio = pygame.time.Clock()

    # na vitória, o personagem aparece grandão correndo
    personagens = pygame.sprite.Group()
    if resultado == VITORIA:
        personagens.add(Personagem(assets, dados["personagem"], CX, CY - 10, 4, "correndo"))

    estado = resultado
    while estado == resultado:
        relogio.tick(FPS)

        # ----- Trata eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                estado = SAIR
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado = SAIR
                if evento.key == pygame.K_r:
                    estado = ESCOLHA          # joga de novo

        # ----- Atualiza
        personagens.update()

        # ----- Desenha
        tela.blit(assets["fundo"], (0, 0))    # o mesmo jardim do começo

        if resultado == VITORIA:
            painel(tela, CX - 450, CY - 210, 900, 390)
            escreve(tela, "VOCÊ VENCEU!", assets["fonte_titulo"], DOURADO, CX, CY - 140)
            personagens.draw(tela)
            texto = NOMES[dados["personagem"]] + " completou em " + str(round(dados["tempo_final"], 1)) + " segundos"
            escreve(tela, texto, assets["fonte"], BRANCO, CX, CY + 100)
            escreve(tela, "R para jogar de novo    ESC para sair", assets["fonte_pequena"], BRANCO, CX, CY + 145)
        else:
            painel(tela, CX - 450, CY - 120, 900, 220)
            escreve(tela, "GAME OVER", assets["fonte_titulo"], VERMELHO, CX, CY - 60)
            escreve(tela, dados["motivo"], assets["fonte"], BRANCO, CX, CY + 10)
            escreve(tela, "R para tentar de novo    ESC para sair", assets["fonte_pequena"], BRANCO, CX, CY + 60)

        pygame.display.flip()

    return estado
