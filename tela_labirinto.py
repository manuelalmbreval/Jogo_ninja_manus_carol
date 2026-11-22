import pygame
from config import (FPS, LARGURA, ALTURA, CX, BRANCO, DOURADO, VERMELHO, AMARELO, NOMES, TEMPO_FASE1, LUGARES_ESTRELAS, LUGARES_BOLAS, VELOCIDADE_BOLA, AUMENTO_VELOCIDADE, LABIRINTO, TEMPLO, GAME_OVER, SAIR)
from assets import tocar
from sprites import Ninja, BolaDeFogo, Estrela, Gongo, eh_parede
from desenho import escreve, painel, desenha_coracao, desenha_estrela

def tela_labirinto (tela, assets, dados):
    relogio = pygame.time.Clock()

    #GRUPOS DE SPRITES
    todos=pygame.sprite.Group() #tudo que será desenhado
    bolas=pygame.sprite.Group() #aapenas as bolas de fogo pra testar colisões
    estrelas= pygame.sprite.Group() # so as estrelas 

    gongo= Gongo()
    todos.add(gongo)
    for x, y in LUGARES_ESTRELAS:
        estrela= Estrela(x,y)
        todos.add(estrela)
        estrelas.add(estrela)

    velocidade= VELOCIDADE_BOLA
    for x, y in LUGARES_BOLAS:
        bola = BolaDeFogo(assets, x, y, velocidade)
        todos.add(bola)
        bolas.add(bola)
        velocidade= velocidade + AUMENTO_VELOCIDADE #deixa cada bola mais rápida

        ninja = Ninja(assets, dados["personagem"])
        todos.add(ninja)# add por ultimo, ficando desenhado por cima 

        vidas = 3 
        pegas = 0 
        total = len(estrelas)
        dados["inicio"]= pygame.time.get_ticks() # o tempo começa contar agora

        estado = LABIRINTO
        while estado == LABIRINTO:
            relogio.tick(FPS)
            agora = pygame.time.get_ticks()

            #Trata eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    estado = SAIR
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    estado = SAIR
                if evento.type == pygame.MOUSEBUTTONDOWN:
                # DICA: mostra no terminal onde você clicou (bom pra mudar estrela de lugar)
                    print("clicou em:", evento.pos, " é parede?",
                            eh_parede(assets["mapa"], evento.pos[0], evento.pos[1]))


        # ----- Atualiza (chama o update() de TODOS os sprites)
        todos.update()

        # ----- Colisões
        # pegou estrela? (True = a estrela some do jogo)
        pegou = pygame.sprite.spritecollide(ninja, estrelas, True, pygame.sprite.collide_circle)
        for estrela in pegou:
            pegas = pegas + 1
            tocar(assets, "estrela")
        todas = pegas == total
        gongo.aberto = todas

        # encostou numa bola de fogo? perde vida e volta pra entrada
        queimou = pygame.sprite.spritecollide(ninja, bolas, False, pygame.sprite.collide_circle)
        if len(queimou) > 0:
            vidas = vidas - 1
            tocar(assets, "dano")
            ninja.voltar_pro_inicio()

        # chegou no gongo? (só vale com todas as estrelas)
        if todas and pygame.sprite.collide_circle(ninja, gongo):
            tocar(assets, "vitoria")
            estado = TEMPLO

        # ----- Tempo e vidas
        restante = TEMPO_FASE1 - (agora - dados["inicio"]) / 1000
        if restante <= 0:
            dados["motivo"] = "O tempo acabou!"
            tocar(assets, "erro")
            estado = GAME_OVER
        if vidas <= 0:
            dados["motivo"] = "As bolas de fogo te pegaram!"
            tocar(assets, "erro")
            estado = GAME_OVER

        # ----- Desenha
        take = (agora // 150) % len(assets["jardim"])       # troca de take a cada 150 ms
        tela.blit(assets["jardim"][take], (0, 0))
        todos.draw(tela)

        # placar da esquerda: nome e vidas
        painel(tela, 20, 15, 300, 95)
        escreve(tela, NOMES[dados["personagem"]], assets["fonte"], DOURADO, 170, 42)
        for i in range(vidas):
            desenha_coracao(tela, 125 + i * 30, 78)

        # placar da direita: tempo e estrelas
        painel(tela, LARGURA - 320, 15, 300, 95)
        if restante < 20:
            cor_tempo = VERMELHO
        else:
            cor_tempo = BRANCO
        escreve(tela, "Tempo: " + str(int(restante)), assets["fonte"], cor_tempo, LARGURA - 170, 42)
        desenha_estrela(tela, LARGURA - 215, 82, 0)
        escreve(tela, str(pegas) + " / " + str(total), assets["fonte"], BRANCO, LARGURA - 155, 82)

        if todas:
            painel(tela, CX - 420, ALTURA - 72, 840, 50)
            escreve(tela, "Todas as estrelas! Corra para o gongo no centro!",
                    assets["fonte"], AMARELO, CX, ALTURA - 47)

        pygame.display.flip()

    return estado





    
