# =====================================================================
#   tela_templo.py  ->  FASE 2: o templo do samurai (estilo Pula Pirata)
# =====================================================================
import random
import pygame
from config import (FPS, ALTURA, CX, BRANCO, DOURADO, AMARELO,
                    LUGARES_BURACOS, ESTRELAS_NA_MAO, SAMURAI_X, PE_DO_SAMURAI,
                    LANCADOR_X, LANCADOR_Y, TEMPLO, VITORIA, GAME_OVER, SAIR)
from assets import tocar
from sprites import Buraco, EstrelaVoando, Samurai, Personagem
from desenho import escreve, desenha_estrela

# frases que aparecem quando a estrela cai num buraco seguro
FRASES_ALIVIO = ["Ufa! Escapou!", "Por pouco!", "O samurai nem piscou!", "Continua...", "Que sorte!"]


def tela_templo(tela, assets, dados):
    relogio = pygame.time.Clock()

    # ----- Grupos de sprites
    todos = pygame.sprite.Group()
    buracos = pygame.sprite.Group()

    for x, y in LUGARES_BURACOS:
        buraco = Buraco(x, y)
        todos.add(buraco)
        buracos.add(buraco)

    armadilha = random.choice(buracos.sprites())   # sorteia o buraco que faz o samurai pular
    armadilha.armadilha = True

    samurai = Samurai(assets)
    todos.add(samurai)

    lancador = Personagem(assets, dados["personagem"], LANCADOR_X, LANCADOR_Y, 3)
    todos.add(lancador)

    voando = None                  # a estrela que está voando agora (ou None)
    estrelas_na_mao = ESTRELAS_NA_MAO
    venceu = False
    momento_vitoria = 0
    mensagem = ""                  # frase que aparece por um tempinho
    momento_mensagem = 0

    estado = TEMPLO
    while estado == TEMPLO:
        relogio.tick(FPS)
        agora = pygame.time.get_ticks()

        # ----- Qual buraco está embaixo do mouse?
        pode_jogar = voando is None and not samurai.pulou and estrelas_na_mao > 0
        embaixo_do_mouse = None
        for buraco in buracos:
            buraco.destacado = False
            if pode_jogar and not buraco.cheio and buraco.rect.collidepoint(pygame.mouse.get_pos()):
                embaixo_do_mouse = buraco
                buraco.destacado = True

        # ----- Trata eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                estado = SAIR
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                estado = SAIR
            # clique num buraco joga uma estrela
            if evento.type == pygame.MOUSEBUTTONDOWN and embaixo_do_mouse is not None:
                voando = EstrelaVoando(embaixo_do_mouse)
                todos.add(voando)
                estrelas_na_mao = estrelas_na_mao - 1
                samurai.preocupado = True
                mensagem = ""
                tocar(assets, "pulo")

        # o personagem se mexe enquanto a estrela voa
        if voando is not None:
            lancador.mudar_estado("andando")
        else:
            lancador.mudar_estado("parado")

        # ----- Atualiza
        todos.update()

        # ----- A estrela chegou no buraco?
        if voando is not None and voando.chegou:
            voando.buraco.cheio = True
            samurai.preocupado = False
            if voando.buraco.armadilha:
                samurai.pular()
                voando.buraco.revelado = True          # mostra em vermelho qual era
                tocar(assets, "boing")
            else:
                tocar(assets, "estrela")
                if estrelas_na_mao == 0:
                    venceu = True
                    momento_vitoria = agora
                    mensagem = "Você venceu o samurai!"
                else:
                    mensagem = random.choice(FRASES_ALIVIO)
                momento_mensagem = agora
            voando = None

        # ----- Fim da fase
        if samurai.pulou and samurai.segundos_desde_o_pulo() > 2:
            dados["motivo"] = "A estrela caiu na armadilha e o samurai pulou!"
            tocar(assets, "erro")
            estado = GAME_OVER
        if venceu and agora - momento_vitoria > 1500:
            dados["tempo_final"] = (agora - dados["inicio"]) / 1000
            tocar(assets, "vitoria")
            estado = VITORIA

        # ----- Desenha
        tela.blit(assets["templo"], (0, 0))

        # título e contador de estrelas, lá em cima (antes dos sprites,
        # assim o samurai passa NA FRENTE do título quando pula)
        escreve(tela, "FASE 2: TEMPLO DO SAMURAI", assets["fonte_titulo"], DOURADO, CX, 60)
        escreve(tela, "Estrelas na mão:", assets["fonte"], BRANCO, CX - 160, 135)
        for i in range(estrelas_na_mao):
            desenha_estrela(tela, CX + i * 45, 135, agora // 10, 1.5)

        todos.draw(tela)

        # BOING quando o samurai pula
        if samurai.pulou:
            escreve(tela, "BOING!", assets["fonte_titulo"], AMARELO, SAMURAI_X + 180, PE_DO_SAMURAI - 130)

        # frase de alívio (aparece por 1 segundo e meio)
        if mensagem != "" and agora - momento_mensagem < 1500:
            escreve(tela, mensagem, assets["fonte"], AMARELO, LANCADOR_X - 70, LANCADOR_Y - 90)

        escreve(tela, "Clique num buraco para jogar uma estrela. Um deles faz o samurai pular!",
                assets["fonte_pequena"], BRANCO, CX, ALTURA - 40)

        pygame.display.flip()

    return estado
