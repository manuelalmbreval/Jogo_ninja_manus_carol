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

def desenha_coracao(tela, x, y): #montar um coração
    pygame.draw.circle(tela, VERMELHO, (x - 5, y), 6) #circulos lado a lado
    pygame.draw.circle(tela, VERMELHO, (x + 5, y), 6)
    pygame.draw.polygon(tela, VERMELHO, [(x - 11, y + 2), (x + 11, y + 2), (x, y + 14)]) #forma a ponta de baixo

def fazer_estrela(t=1): #cria e devolve a imagem de uma estrela ninja
    # Cria a IMAGEM de uma estrela ninja (t = tamanho: 1 normal, 1.5 maior...)
    # 4 pontas compridas (cima, direita, baixo, esquerda) e 4 cantinhos curtos no meio
    lado = int(28 * t)
    imagem = pygame.Surface((lado, lado), pygame.SRCALPHA)  # fundo transparente
    c = lado / 2                                            # centro da imagem
    p = 13 * t                                              # ponta comprida
    k = 3.5 * t                                             # cantinho curto
    pontos = [(c, c - p), (c + k, c - k),                   # cima
              (c + p, c), (c + k, c + k),                   # direita
              (c, c + p), (c - k, c + k),                   # baixo
              (c - p, c), (c - k, c - k)]                   # esquerda
    pygame.draw.polygon(imagem, PRATA, pontos)
    pygame.draw.circle(imagem, CINZA, (c, c), 3 * t)        # bolinha do meio
    return imagem #devolve uma imagem, sem desenhar na tela 


def desenha_estrela(superficie, x, y, angulo=0, t=1):
    # Desenha uma estrela com o centro em (x, y), girada "angulo" graus
    # "superficie" pode ser a tela OU a imagem de um sprite
    imagem = pygame.transform.rotate(fazer_estrela(t), angulo) #usa a outra funcao fazer_estrela(t), gira a img
    superficie.blit(imagem, imagem.get_rect(center=(x, y))) #usa o get center para manter a estrela centralizada mesmo depois de girar, pois a imagem rotacionada muda de tamanho






