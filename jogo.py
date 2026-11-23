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

