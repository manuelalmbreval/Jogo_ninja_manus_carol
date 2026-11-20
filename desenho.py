#funções pequenas de desenho usadas em várias telas 

import pygame #traz a biblioteca do jogo inteira
from config import VERMELHO, PRATA, CINZA #pega só as cores que estão definidas na file config.py
#obs importante: cor no PYGAME é uma tupla RGB (r, g , b), cada valor de 0 a 255

#coordenadas na tela: 
# (0,0) é o canto superior esquerdo 
# o x cresce p a direira 
# o y cresce p baixo, ao contrario da matemática 
#ex: no coração o y + 14 é a ponta de baixo, e na estrela o c - p é a ponta de cima.

def escreve(tela, texto, fonte, cor, x, y): #escreve um texto centralizado em x e y
    # Escreve um texto com o CENTRO em (x, y)
    imagem = fonte.render(texto, True, cor) #transforma o texto em uma imagem. o True liga o antialiasing, q deixa as bordas lisas
    tela.blit(imagem, imagem.get_rect(center=(x, y))) #cola a imagem na tela 
    #imagem.get_rect(center=(x, y)) cria o retângulo da imagem com o centro em (x, y). Sem isso, o (x, y) seria o canto superior esquerdo.

def painel(tela, x, y, largura, altura): #desenha um retangulo escuro atrás do texto p ele ficar legível
    # retângulo escuro atrás do texto, pra dar pra ler em cima do cenário
    pygame.draw.rect(tela, (30, 6, 12), (x, y, largura, altura), border_radius=8) #border_radius = 8 arredonda os cantos







