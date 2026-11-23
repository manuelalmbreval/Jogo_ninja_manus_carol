#jogo.py é o arquivo principal: a file que 'roda' o código 

import pygame
from config import LARGURA, ALTURA, ESCOLHA, LABIRINTO, TEMPLO, VITORIA, GAME_OVER, SAIR
from assets import carregar_assets
from tela_escolha import tela_escolha
from tela_labirinto import tela_labirinto
from tela_templo import tela_templo
from tela_final import tela_final
from tela_inicio import tela_inicio





#inicializacao 
pygame.init()
pygame.mixer.init()

# SCALED = o pygame estica o 1920x1080 sozinho pro tamanho do seu monitor
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Resina Strikes Back")

assets = carregar_assets()                 # tem que ser DEPOIS de abrir a tela
if len(assets["sons"]) > 0:
    pygame.mixer.music.play(-1)            # -1 = repete para sempre

# Informações que passam de uma tela pra outra
dados = {
    "personagem": "ninja1",   # quem foi escolhido
    "motivo": "",             # por que perdeu
    "inicio": 0,              # quando começou a fase 1
    "tempo_final": 0,         # quanto tempo levou pra ganhar
}

# Troca de telas 

estado = tela_inicio(tela)

if estado == ESCOLHA:
    estado = tela_escolha(tela, assets, dados)


estado = ESCOLHA
while estado != SAIR:
    if estado == ESCOLHA:
        estado = tela_escolha(tela, assets, dados)
    elif estado == LABIRINTO:
        estado = tela_labirinto(tela, assets, dados)
    elif estado == TEMPLO:
        estado = tela_templo(tela, assets, dados)
    elif estado == VITORIA or estado == GAME_OVER:
        estado = tela_final(tela, assets, dados, estado)
    else:
        estado = SAIR

#finalizacao 
pygame.quit()