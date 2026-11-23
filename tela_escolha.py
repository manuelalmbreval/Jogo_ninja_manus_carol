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

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                estado = SAIR
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado = SAIR
                if evento.key == pygame.K_1:
                    dados["personagem"] = "ninja1"
                    estado = LABIRINTO
                if evento.key == pygame.K_2:
                    dados["personagem"] = "ninja2"
                    estado = LABIRINTO
                if evento.key == pygame.K_3:
                    dados["personagem"] = "samurai"
                    estado = LABIRINTO
        personagens.update()

         #Desenha
        tela.blit(assets["fundo"], (0, 0))           # o jardim de cerejeiras no fundo
        painel(tela, CX - 420, 70, 840, 100)         # retângulos escuros atrás dos textos
        painel(tela, CX - 330, CY - 160, 660, 300)
        painel(tela, CX - 620, ALTURA - 135, 1240, 80)
        escreve(tela, "RESINA STRIKES BACK", assets["fonte_titulo"], DOURADO, CX, 120)
        escreve(tela, "Escolha 1, 2 ou 3", assets["fonte"], BRANCO, CX, CY - 125)
        personagens.draw(tela)
        escreve(tela, "1 - " + NOMES["ninja1"], assets["fonte_pequena"], BRANCO, CX - 200, CY + 110)
        escreve(tela, "2 - " + NOMES["ninja2"], assets["fonte_pequena"], BRANCO, CX, CY + 110)
        escreve(tela, "3 - " + NOMES["samurai"], assets["fonte_pequena"], BRANCO, CX + 200, CY + 110)
        escreve(tela, "Fase 1: pegue as 6 estrelas ninja, fuja das bolas de fogo e chegue no gongo",
                assets["fonte_pequena"], BRANCO, CX, ALTURA - 110)
        

        pygame.display.flip()

    return estado



