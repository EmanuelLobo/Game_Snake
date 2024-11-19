import pygame
import random

pygame.init()
pygame.display.set_caption("Jogo Snake Python")
largura, altura = 1200, 800
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# Cores RGB
preta = (0, 0, 0)
branca = (255, 255, 255)
vermelha = (255, 0, 0)
verde = (0, 255, 0)

# Parâmetros da cobra
tamanho_quadrado = 20
velocidade_jogo = 15

imagem = pygame.image.load("background/fundo_snake.png")

def Background(image):
    size = pygame.transform.scale(image, (1200, 800))
    tela.blit(size, (0, 0))

# Tentar carregar a imagem da fruta
try:
    fruta_img = pygame.image.load("Fruta/Maca_verde.png")
    fruta_img = pygame.transform.scale(fruta_img, (tamanho_quadrado, tamanho_quadrado))  # Ajuste o tamanho da fruta
except pygame.error as e:
    pygame.quit()
    exit()


def gerar_comida():
    comida_x = round(random.randrange(0, largura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    comida_y = round(random.randrange(0, altura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    return comida_x, comida_y

def desenhar_comida(comida_x, comida_y):
    tela.blit(fruta_img, (comida_x, comida_y))  # Desenha a imagem da fruta

def desenha_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branca, [pixel[0], pixel[1], tamanho, tamanho])

def desenha_pontuacao(pontuacao):
    fonte = pygame.font.SysFont("poppins", 30)
    texto = fonte.render(f"Pontos: {pontuacao}", True, vermelha) 
    tela.blit(texto, [10, 10])  # Exibe a pontuação no canto superior esquerdo

def selecionar_velocidade(tecla, velocidade_x, velocidade_y):
    if tecla == pygame.K_DOWN and velocidade_y == 0:  # Previne movimento oposto
        velocidade_x = 0
        velocidade_y = tamanho_quadrado
    elif tecla == pygame.K_UP and velocidade_y == 0:
        velocidade_x = 0
        velocidade_y = -tamanho_quadrado
    elif tecla == pygame.K_RIGHT and velocidade_x == 0:
        velocidade_x = tamanho_quadrado
        velocidade_y = 0
    elif tecla == pygame.K_LEFT and velocidade_x == 0:
        velocidade_x = -tamanho_quadrado
        velocidade_y = 0
    return velocidade_x, velocidade_y

def exibir_game_over(pontuacao):
    fonte = pygame.font.SysFont("poppins", 50)
    texto = fonte.render("GAME OVER", True, vermelha)
    tela.blit(texto, [largura / 4, altura / 3])
    texto_pontos = fonte.render(f"Pontuação Final: {pontuacao}", True, branca)
    tela.blit(texto_pontos, [largura / 4, altura / 2])
    pygame.display.update()
    pygame.time.delay(2000)

def roda_jogo():
    fim_jogo = False
    x = largura / 2 
    y = altura / 2

    velocidade_x = 0
    velocidade_y = 0

    tamanho_cobra = 1
    pixels = []

    comida_x, comida_y = gerar_comida()

    pontuacao = 0  # Inicializa a pontuação

    while not fim_jogo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key, velocidade_x, velocidade_y)

        # Movimento da cobra
        x += velocidade_x
        y += velocidade_y

        # Verifica colisão com o próprio corpo
        if [x, y] in pixels[:-1]:  # Colisão com o corpo da cobra
            fim_jogo = True

        # Verifica colisão com as bordas da tela
        if x >= largura or x < 0 or y >= altura or y < 0:
            fim_jogo = True

        # Atualiza a lista de pixels (posições da cobra)
        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]

        # Desenha tudo
        tela.fill(preta)  # Limpa a tela a cada frame
        Background(imagem)  # Coloca o fundo
        desenhar_comida(comida_x, comida_y)
        desenha_cobra(tamanho_quadrado, pixels)
        desenha_pontuacao(pontuacao)  # Exibe a pontuação

        # Atualiza a tela
        pygame.display.update()

        # Verifica se a cobra comeu a comida
        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            pontuacao += 1
            comida_x, comida_y = gerar_comida()

        # Atualiza a velocidade do jogo
        relogio.tick(velocidade_jogo)

    exibir_game_over(pontuacao)  # Exibe a tela de Game Over com pontuação final

# Inicia o jogo
roda_jogo()
