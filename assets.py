#file para carregar todas as imagens, fontes e sons 
# tudo vai p um dicionário chamado 'assets'
# assets['templo'] é a imagem do templo 

import os
import pygame
from config import LARGURA, ALTURA, PASTA_IMAGENS, PASTA_SONS, PASTA_DO_PERSONAGEM, QUADROS

def carregar_imagem(caminho, largura, altura):
    # PNG COM fundo transparente (personagens), já no tamanho pedido
    imagem = pygame.image.load(caminho).convert_alpha()
    return pygame.transform.scale(imagem, (largura, altura))


def carregar_cenario(caminho):
    # PNG de cenário (sem transparência = desenha mais rápido), do tamanho da tela
    imagem = pygame.image.load(caminho).convert()
    return pygame.transform.scale(imagem, (LARGURA, ALTURA))


def carregar_assets():
    assets = {}

    #personagens
    # assets["personagens"]["ninja1"]["andando"] = lista com as 6 imagens do Enzo andando
    assets["personagens"] = {}
    for nome in PASTA_DO_PERSONAGEM:                        # "ninja1", "ninja2", "samurai"
        pasta = PASTA_DO_PERSONAGEM[nome]                   # "enzo", "lucas", "resina"
        animacoes = {}
        for estado in QUADROS:                              # "parado", "andando", "correndo"
            lista = []
            for i in range(QUADROS[estado]):
                caminho = os.path.join(PASTA_IMAGENS, pasta, estado + "_" + str(i) + ".png")
                lista.append(carregar_imagem(caminho, 32, 32))   # desenho original: 32x32
            animacoes[estado] = lista
        assets["personagens"][nome] = animacoes

    #caretas do resina 
    assets["caretas"] = {}
    for careta in ["bravo", "kiai", "desconfiado", "dentes"]:
        # Monta o "endereço" (caminho) da imagem da careta.
        # os.path.join junta os pedaços colocando a barra (/).
        #   PASTA_IMAGENS     -> pasta principal das imagens
        #   "resina_caretas"  -> subpasta onde ficam as caretas
        #   careta + ".png"   -> nome do arquivo (ex: "feliz" + ".png" = "feliz.png")
        # Resultado exemplo: imagens/resina_caretas/feliz.png
        # Obs: essa linha NÃO abre a imagem, só guarda o endereço em "caminho".
        caminho = os.path.join(PASTA_IMAGENS, "resina_caretas", careta + ".png")
        assets["caretas"][careta] = carregar_imagem(caminho, 48, 48)   # original: 48x48