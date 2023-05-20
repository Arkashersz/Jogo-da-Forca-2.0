import pygame as pg
from pygame import mixer
import random
import sys
import time
from pygame.locals import *

pg.init()

palavras = ["banana", "melancia", "morango", "cachorro", "porteira", "hotel", "chuveiro", "python", "cascavel", "elefante", "geladeira", "aparelho", "papelaria", "lab", 
            "grelha", "voto", "estacionamento", "dinamite", "jovem", "cura", "real", "sogra", "passagem", "abaixar", "abrir", "achar", "agir", "ajudar", "amar", "andar", 
            "anotar", "apagar", "aparecer", "aprender", "aproveitar", "apurar", "arranjar", "arrumar", "aspirar", "assar", "assistir", "atender", "atualizar", "aumentar", 
            "avisar", "beber", "buscar", "caber", "calar", "calcular", "caçar", "chegar", "chutar", "cozinhar", "correr", "cortar", "criar", "cuspir", "dançar", "dar", 
            "decidir", "deitar", "desenhar", "desejar", "desistir", "dirigir", "dividir", "dobrar", "doer", "dormir", "duvidar", "embarcar", "emergir", "emitir", "encontrar", 
            "entender", "entrar", "entregar", "enviar", "escalar", "escapar", "escolher", "esconder", "escrever", "esperar", "esquecer", "estudar", "exercer", "explicar", 
            "explodir", "falar", "fechar", "ferir", "fiar", "ficar", "fingir", "flutuar", "foder", "fornecer", "gastar", "gritar", "guardar", "guiar", "haver", "ignorar", 
            "imaginar", "imprimir", "inaugurar", "indicar", "iniciar", "inovar", "inserir", "insistir", "interferir", "ir", "jogar", "juntar", "jurar", "lavar", "ligar", 
            "limpar", "localizar", "lograr", "matar", "mexer", "modificar", "morrer", "nascer", "navegar", "notar", "obedecer", "obter", "ocorrer", "oferecer", "olhar", 
            "opinar", "organizar", "pagar", "passear", "passar", "pensar", "perder", "pesquisar", "pintar", "pisar", "planejar", "plantar", "poder", "preencher", "preparar", 
            "preservar", "procurar", "prometer", "proteger", "quebrar", "querer", "questionar", "rasgar", "receber", "reconhecer", "recusar", "refletir", "registrar", "reparar", 
            "repetir", "resolver", "responder", "retirar", "rezar", "rir", "saber", "sair", "saltar", "seguir", "sentar", "soltar", "sofrer", "sorrir", "subir", "sugerir", "sumir", 
            "surpreender", "teclar", "temer", "ter", "testar", "tocar", "tomar", "trabalhar", "traduzir", "trocar", "usar", "valer", "ver", "vestir", "visitar", "viver", "voltar", 
            "xeretar"]
# Cor
cinza = (128,128,128)
preto = (0,0,0)
branco = (255,255,255)
vermelho = (255,0,0)

# Som
musica_jogo = pg.mixer.music.load('Musica tema do jogo.mp3')
musica_vitoria = pg.mixer.Sound('win.mp3')  # carrega a música de vitória
musica_derrota = pg.mixer.Sound('lose.mp3') # carrega a música de derrota

pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.1)
musica_vitoria.set_volume(0.1)
musica_derrota.set_volume(0.03)

# Start da font do jogo
pg.font.init()
 
# Fonte do jogo
font_principal = pg.font.SysFont('Courier New', 60)
font_botao = pg.font.SysFont('Courier New', 20)
alert_font = pg.font.SysFont("Courier New", 20)
texto = pg.font.SysFont("comicsansms", 20)

# Tela do jogo
tela = pg.display.set_mode((1000, 600))
pg.display.set_caption("Jogo da Forca - Feito por Douglas")

# Variáveis
tentativas = [' ', '-']
palavra_secreta = ''
palavra_escondida = ''
fim_jogo = True
chance = 0
letra = ''
click_botao = False
vitoria = False  # adiciona uma variável para verificar se o jogador venceu o jogo
derrota = False
musica_tocada_vitoria = False

# Desenho da forca
derrota = False
musica_tocada_vitoria = False
musica_tocada_derrota = False
def desenho(tela, chance, musica_tocada_derrota):
    pg.draw.rect(tela, cinza, (0, 0, 1000, 600))
    pg.draw.line(tela, preto, (100, 500), (100, 100), 10)
    pg.draw.line(tela, preto, (50, 500), (150, 500), 10)
    pg.draw.line(tela, preto, (100, 100), (300, 100), 10)
    pg.draw.line(tela, preto, (300, 100), (300, 150), 10)
    if chance >= 1:
        pg.draw.circle(tela, preto, (300, 200), 50, 7)
    if chance >= 2:
        pg.draw.line(tela, preto, (300, 250), (300, 350), 7)
    if chance >= 3:
        pg.draw.line(tela, preto, (300, 260), (225, 350), 7)
    if chance >= 4:
        pg.draw.line(tela, preto, (300, 260), (375, 350), 7)
    if chance >= 5:
        pg.draw.line(tela, preto, (300, 350), (375, 450), 7)
    if chance >= 6:
        pg.draw.line(tela, preto, (300, 350), (225, 450), 7)
        texto = alert_font.render(f'Você perdeu! Tente novamente, a palavra era {palavra_secreta}', True, preto)
        tela.blit(texto, (180, 560))
        pg.mixer.music.stop()
        if not musica_tocada_derrota:
            musica_derrota.play()
            musica_tocada_derrota = True      
     

# Desenho do botão Restart
def desenho_restart(tela):
    pg.draw.rect(tela, preto, (695, 100, 200, 65))
    texto = font_botao.render('Recomeçar', True, branco)
    tela.blit(texto, (740, 120))

# Uso da biblioteca Random para definiri de forma aleatória a palvra secreta
def escolhendo_palavra(palavras, palavra_secreta, fim_jogo):
    if fim_jogo == True:        
        palavra_secreta = random.choice(palavras)
        fim_jogo = False
    return palavra_secreta, fim_jogo

# Esconde a palavra secreta, notifica que ganhou o jogo se acertar a palavra
# Trava a digitação quando acertar a palavra completa e toca uma música de win
def escondendo_palavra(palavra_secreta, palavra_escondida, tentativas, musica_tocada_vitoria):
    palavra_escondida = palavra_secreta
    for opcao in range(len(palavra_escondida)):
        if palavra_escondida[opcao:opcao + 1] not in tentativas:
            palavra_escondida = palavra_escondida.replace(palavra_escondida[opcao], '#')
    # Verifica se a palavra está escondida, caso não esteja retorna a vitória do jogo e bloqueia a digitação
    if "#" not in palavra_escondida:
        vitoria = True
        pg.event.set_blocked(KEYDOWN)
        pg.event.set_blocked(KEYUP)
        # Parar a música do jogo e tocar a música de vitória
        pg.mixer.music.stop()
        if not musica_tocada_vitoria:
            musica_vitoria.play()
            musica_tocada_vitoria = True
    else:
        vitoria = False
    return palavra_escondida, vitoria, musica_tocada_vitoria

# Função para verificar se a letra está dentro da palavra secreta
def tentativa_letra(tentativas, palavra_secreta, letra, chance):
    if letra not in tentativas:
        tentativas.append(letra)
        if letra not in palavra_secreta:
            chance += 1
    elif letra in tentativas:
        pass
    return tentativas, chance

# Função para definir a fonte e tamanho da palavra visivel na forca
def palavra_forca(tela, palavra_escondida):
    palavra = font_principal.render(palavra_escondida, True, preto)
    tela.blit(palavra, (200, 450))

# Função que reseta o jogo para uma nova tentativa ser realizada
def botao_restart(fim_jogo, chance, letra, tentativas, click_botao, click, x, y, musica_tocada_vitoria, musica_tocada_derrota):
    if click_botao == True and click[0] == True:
        if x >= 700 and x <= 900 and y >= 100 and y <= 165:
            tentativas = [' ', '-']
            fim_jogo = True
            chance = 0
            letra = ' '
            musica_tocada_vitoria = False
            musica_tocada_derrota = False
            pg.mixer.music.play()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pg.event.set_allowed(KEYDOWN)
                    pg.event.set_allowed(KEYUP)            
    return fim_jogo, chance, tentativas, letra, musica_tocada_vitoria, musica_tocada_derrota

# Função da mensagem de vitória
def ganhou(tela):
    texto = alert_font.render('Parabéns! Você ganhou o jogo.', True, preto)
    tela.blit(texto, (300, 560))


vitoria = False
derrota = False
musica_tocada_vitoria = False
rodando = True
musica_derrota_tocada = False
while rodando:

    # Posição do mouse
    mouse = pg.mouse.get_pos()
    posicao_x = mouse[0]
    posicao_y = mouse[1]

    # Variavel do click
    click = pg.mouse.get_pressed()

    # Click do botão
    if click[0] == True:
        click_botao = True
    else:
        click_botao = False
    # Define que o jogo fecha apenas no "X"
    for event in pg.event.get():
        if event.type == pg.QUIT:
            rodando = False
        # Se a letra estiver certa irá ser mostrada na tela
        if event.type == pg.KEYDOWN:
            letra = str(pg.key.name(event.key)).lower()
            print(letra)
    # Condição que trava a digitação no jogo e para a núsica tema
    if chance >= 6:
        pg.event.set_blocked(KEYDOWN)
        pg.event.set_blocked(KEYUP)
        pg.mixer.music.stop()
        # Condição que destrava o jogo com o clique do botão esquerdo do mouse quando clicar em "Recomeçar"
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                pg.event.set_allowed(KEYDOWN)
                pg.event.set_allowed(KEYUP)
        # Condição para tocar a música derrota quando o desenho for completo
        if not musica_tocada_derrota:
            musica_derrota.play()
            musica_tocada_derrota = True             

    # Conteúdo do jogo
    desenho(tela, chance, musica_tocada_derrota)
    desenho_restart(tela)
    palavra_secreta, fim_jogo = escolhendo_palavra(palavras, palavra_secreta, fim_jogo)
    palavra_escondida, vitoria, musica_tocada_vitoria = escondendo_palavra(palavra_secreta, palavra_escondida, tentativas, musica_tocada_vitoria)
    tentativas, chance = tentativa_letra(tentativas, palavra_secreta, letra, chance)
    palavra_forca(tela, palavra_escondida)    
    fim_jogo, chance, tentativas, letra, musica_tocada_vitoria, musica_tocada_derrota = botao_restart(fim_jogo, chance, letra, tentativas, click_botao, click, posicao_x, posicao_y, musica_tocada_vitoria, musica_tocada_derrota)


    if vitoria:
        ganhou(tela)

    pg.display.update()
