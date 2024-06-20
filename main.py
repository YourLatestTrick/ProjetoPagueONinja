import os, random, pygame
from tkinter import simpledialog

pygame.init()

relogio = pygame.time.Clock()
icone  = pygame.image.load("assets/icone.png")
ninja = pygame.image.load("assets/ninja.png")
fundo = pygame.image.load("assets/fundo.png")
fundoStart = pygame.image.load("assets/fundoStart.jpg")
fundoDead = pygame.image.load("assets/fundoDead.png")

moeda = pygame.image.load("assets/moeda.png")
tamanho = (800,600)
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("PAGUE O NINJA")
pygame.display.set_icon(icone)
moedaSound = pygame.mixer.Sound("assets/moeda.mp3")
morteSound = pygame.mixer.Sound("assets/morte.mp3")
fonte = pygame.font.SysFont("comicsans",28)
fonteStart = pygame.font.SysFont("comicsans",55)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("assets/musica.mp3")

branco = (255,255,255)
preto = (0, 0 ,0 )
vermelho = (160,0,0)

def jogar(nome):
    pygame.mixer.Sound.play(moedaSound)
    pygame.mixer.music.play(-1)
    posicaoXNinja = 400
    posicaoYNinja = 300
    movimentoXNinja  = 0
    movimentoYNinja  = 0
    posicaoXMoeda = 400
    posicaoYMoeda = -240
    velocidadeMoeda = 1
    pontos = 0
    larguraNinja = 137
    alturaNinja = 158
    larguaMoeda  = 87
    alturaMoeda  = 87
    dificuldade  = 20

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXNinja = 10
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXNinja = -10
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXNinja = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXNinja = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP:
                movimentoYNinja = -10
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN:
                movimentoYNinja = 10
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_UP:
                movimentoYNinja = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_DOWN:
                movimentoYNinja = 0
                
        posicaoXNinja = posicaoXNinja + movimentoXNinja            
        posicaoYNinja = posicaoYNinja + movimentoYNinja            
        
        if posicaoXNinja < 0 :
            posicaoXNinja = 10
        elif posicaoXNinja >550:
            posicaoXNinja = 540
            
        if posicaoYNinja < 0 :
            posicaoYNinja = 10
        elif posicaoYNinja > 473:
            posicaoYNinja = 463
        
            
        tela.fill(branco)
        tela.blit(fundo, (0,0) )
        #pygame.draw.circle(tela, preto, (posicaoXNinja,posicaoYNinja), 40, 0 )
        tela.blit( ninja, (posicaoXNinja, posicaoYNinja) )
        
        posicaoYMoeda = posicaoYMoeda + velocidadeMoeda
        if posicaoYMoeda > 600:
            posicaoYMoeda = -240
            pontos = pontos + 1
            velocidadeMoeda = velocidadeMoeda + 1
            posicaoXMoeda = random.randint(0,800)
            pygame.mixer.Sound.play(moedaSound)
            
            
        tela.blit( moeda, (posicaoXMoeda, posicaoYMoeda) )
        
        texto = fonte.render(nome+"- Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (10,10))
        
        pixelsNinjaX = list(range(posicaoXNinja, posicaoXNinja+larguraNinja))
        pixelsNinjaY = list(range(posicaoYNinja, posicaoYNinja+alturaNinja))
        pixelsMoedaX = list(range(posicaoXMoeda, posicaoXMoeda + larguaMoeda))
        pixelsMoedaY = list(range(posicaoYMoeda, posicaoYMoeda + alturaMoeda))
        
        #print( len( list( set(pixelsMoedaX).intersection(set(pixelsNinjaX))   ) )   )
        if  len( list( set(pixelsMoedaY).intersection(set(pixelsNinjaY))) ) > dificuldade:
            if len( list( set(pixelsMoedaX).intersection(set(pixelsNinjaX))   ) )  > dificuldade:
                dead(nome, pontos)
        
    
        
        pygame.display.update()
        relogio.tick(60)


def dead(nome, pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(morteSound)
    
    jogadas  = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8")
        jogadas = eval(arquivo.read())
        arquivo.close()
    except:
        arquivo = open("historico.txt","w",encoding="utf-8")
        arquivo.close()
 
    jogadas[nome] = pontos   
    arquivo = open("historico.txt","w",encoding="utf-8") 
    arquivo.write(str(jogadas))
    arquivo.close()
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                jogar(nome)

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
        tela.fill(branco)
        tela.blit(fundoDead, (0,0))
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        textoStart = fonteStart.render("", True, branco)
        tela.blit(textoStart, (400,482))
        textoEnter = fonte.render("Pressione ENTER para buscar vingança...", True, vermelho)
        tela.blit(textoEnter, (60,482))
        pygame.display.update()
        relogio.tick(60)


def ranking():
    estrelas = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8" )
        estrelas = eval(arquivo.read())
        arquivo.close()
    except:
        pass
    
    nomes = sorted(estrelas, key=estrelas.get,reverse=True)
    print(estrelas)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    start()

        tela.fill(preto)
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        textoStart = fonteStart.render("BACK TO START", True, branco)
        tela.blit(textoStart, (330,482))
        
        
        posicaoY = 50
        for key,nome in enumerate(nomes):
            if key == 13:
                break
            textoJogador = fonte.render(nome + " - "+str(estrelas[nome]), True, branco)
            tela.blit(textoJogador, (300,posicaoY))
            posicaoY = posicaoY + 30

            
        
        pygame.display.update()
        relogio.tick(60)


def start():
    nome = simpledialog.askstring("PAGUE O NINJA","CPF:")
    
    
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
                elif buttonRanking.collidepoint(evento.pos):
                    ranking()

        tela.fill(branco)
        tela.blit(fundoStart, (0,0))
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        buttonRanking = pygame.draw.rect(tela, preto, (35,50,200,50),0,30)
        textoRanking = fonte.render("Ranking", True, branco)
        tela.blit(textoRanking, (90,50))
        textoStart = fonteStart.render("JOGAR", True, branco)
        tela.blit(textoStart, (330,482))

        
        
        pygame.display.update()
        relogio.tick(60)

start()