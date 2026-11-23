#jogo.py é o arquivo principal: a file que 'roda' o código 

import pygame
from config import LARGURA, ALTURA, ESCOLHA, LABIRINTO, TEMPLO, VITORIA, GAME_OVER, SAIR
from assets import carregar_assets
from tela_escolha import tela_escolha
from tela_labirinto import tela_labirinto
from tela_templo import tela_templo
from tela_final import tela_final

#inicializacao 
pygame.init()
pygame.mixer.init()

# SCALED = o pygame estica o 1920x1080 sozinho pro tamanho do seu monitor
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Resina Strikes Back")

assets = carregar_assets()                 # tem que ser DEPOIS de abrir a tela
if len(assets["sons"]) > 0:
    pygame.mixer.music.play(-1)            # -1 = repete para sempre
