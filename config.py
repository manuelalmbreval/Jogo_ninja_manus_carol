#config -> todos os números e nomes
import os

PASTA = os.path.dirname(os.path.abspath(__file__))
PASTA_IMAGENS = os.path.join(PASTA, "imagens")
PASTA_SONS = os.path.join(PASTA, "sons")

# TELA
LARGURA = 1920        # o jogo é desenhado sempre em 1920x1080
ALTURA = 1080
FPS = 60              # quadros por segundo
CX = LARGURA // 2     # centro da tela
CY = ALTURA // 2

# CORES
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
DOURADO = (250, 200, 60)
VERMELHO = (220, 40, 40)
LARANJA = (255, 130, 50)
AMARELO = (255, 230, 80)
CINZA = (120, 120, 130)
PRATA = (200, 205, 215)

# Qual tela aparece
ESCOLHA = 0
LABIRINTO = 1
TEMPLO = 2
VITORIA = 3
GAME_OVER = 4
SAIR = 5

# Personagens
PASTA_DO_PERSONAGEM = {"ninja1": "enzo", "ninja2": "lucas", "samurai": "resina"}
NOMES = {"ninja1": "Enzo ninja", "ninja2": "Lucas ninja", "samurai": "Resina samurai"}
QUADROS = {"parado": 4, "andando": 6, "correndo": 6}                   # quantas imagens cada animação tem
VELOCIDADE_ANIMACAO = {"parado": 180, "andando": 100, "correndo": 70}  # ms que cada imagem fica na tela

# Fase 1 - > labirinto
TEMPO_FASE1 = 240                  # segundos para terminar o labirinto
INICIO = (960, 1064)               # entrada, embaixo
GONGO = (910, 527)                 # no meio, do lado do torii
LUGARES_ESTRELAS = [(1425, 509), (1152, 92), (672, 131), (462, 527), (627, 872), (1284, 863)]
# bolas de fogo espalhadas: 3 no anel de fora (onde estão as estrelas),
# 4 nos anéis do meio e 1 perto do centro (vigiando o gongo)
LUGARES_BOLAS = [(960, 53), (1347, 773), (524, 320),
                 (1238, 406), (700, 702), (774, 254), (1101, 792),
                 (890, 675)]
VELOCIDADE_BOLA = 1.6              # a primeira bola anda 1.6 por quadro...
AUMENTO_VELOCIDADE = 0.15          # ...e cada uma anda um pouquinho mais rápido que a anterior
# as 8 direções que uma bola de fogo pode andar: (pro lado, pra cima/baixo)
DIRECOES = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

# Fase 2 - > Templo
LUGARES_BURACOS = [(765, 905), (895, 905), (1025, 905), (1155, 905),     # andar de baixo
                   (802, 747), (907, 747), (1012, 747), (1117, 747),     # andar do meio
                   (840, 605), (920, 605), (1000, 605), (1080, 605)]     # andar de cima
ESTRELAS_NA_MAO = 6
PE_DO_SAMURAI = 527                # em cima do telhado mais alto
SAMURAI_X = CX
LANCADOR_X = 540                   # de onde o seu personagem joga as estrelas
LANCADOR_Y = 930

