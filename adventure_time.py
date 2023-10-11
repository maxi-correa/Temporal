#Paquetes necesarios para la creación del juego
import sys
import pygame
from boton import Boton

pygame.init()

#Definición de colores
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
CYAN =  (  0, 255, 255)
BLUE =  (  0,   0, 255)

#Definición de resolución de pantalla
PANTALLA_ANCHO = 800
PANTALLA_ALTO = 600
movimiento_fondo = 0

#Creación y nombre de ventana
screen = pygame.display.set_mode((PANTALLA_ANCHO, PANTALLA_ALTO))  
pygame.display.set_caption("Adventure Time")

#Carga de imagenes
titulo_img = pygame.image.load('imagenes/adventure_time.png').convert_alpha()
fondo_img = pygame.image.load('imagenes/fondo.png').convert_alpha()
play_img = pygame.image.load('imagenes/play_btn.png').convert_alpha()
option_img = pygame.image.load('imagenes/option_btn.png').convert_alpha()
option_2_img = pygame.image.load('imagenes/option_2_btn.png').convert_alpha()
quit_img = pygame.image.load('imagenes/quit_btn.png').convert_alpha()
quit_2_img = pygame.image.load('imagenes/quit_2_btn.png').convert_alpha()
sound_on_img = pygame.image.load('imagenes/sound_on_btn.png').convert_alpha()
sound_on_2_img = pygame.image.load('imagenes/sound_on_2_btn.png').convert_alpha()
sound_off_img = pygame.image.load('imagenes/sound_off_btn.png').convert_alpha()
sound_off_2_img = pygame.image.load('imagenes/sound_off_2_btn.png').convert_alpha()
menu_img = pygame.image.load('imagenes/menu_btn.png').convert_alpha()
restart_img = pygame.image.load('imagenes/restart_btn.png').convert_alpha()

#Carga de música de fondo
menu_theme = pygame.mixer.Sound('sonidos/menu_theme.ogg')
battle_theme = pygame.mixer.Sound('sonidos/battle_theme.ogg')
menu_theme.play(-1) #-1 para reproducción infinita

#Instancias de botones
boton_play = Boton(300, 250, play_img, 1)
#boton_option = Boton(300, 350, option_img, 1)
boton_sound_on = Boton (520, 350, sound_on_img, 1.4)
boton_sound_off = Boton(620, 350, sound_off_img, 1.4)
boton_quit = Boton(300, 450, quit_img, 1)
boton_menu = Boton(750, 10, menu_img, 1)
boton_resume = Boton(320, 300, restart_img, 1.5)
boton_sound_on_2 = Boton(470, 400, sound_on_2_img, 1.5)
boton_sound_off_2 = Boton(550, 400, sound_off_2_img, 1.5)
#boton_option_2 = Boton(320, 400, option_2_img, 1.5)
boton_quit_2 = Boton(320, 500, quit_2_img, 1.5)

#Marcadores de inicio
tema_menu_encendido = True
juego_corriendo = False
juego_pausado = False
run = True

#loop de ejecución
while run:
    
    #Entrada al menú principal
    if juego_corriendo == False and juego_pausado == False:
        
        #Fondo en movimiento
        movimiento_fondo_relativo = movimiento_fondo % fondo_img.get_rect().width
        screen.blit(fondo_img, (movimiento_fondo_relativo - fondo_img.get_rect().width,0))
        if movimiento_fondo_relativo < PANTALLA_ANCHO:
            screen.blit(fondo_img, (movimiento_fondo_relativo, 0))
        movimiento_fondo -= 1
        
        #Título del juego
        screen.blit(titulo_img, [50, -70])
        screen.blit(option_img, [300, 350])
        
        #Condiciones de los botones del menú
        if boton_play.dibujar(screen):
            juego_corriendo = True
            menu_theme.stop()
            tema_batalla_encendido = True
            battle_theme.play(-1)
        
        #if boton_option.dibujar(screen):
        #    print('OPTION')
        
        if boton_sound_on.dibujar(screen):
            if tema_menu_encendido == False:
                tema_menu_encendido = True
                menu_theme.play(-1)
        
        if boton_sound_off.dibujar(screen):
            tema_menu_encendido = False
            menu_theme.stop()
        
        if boton_quit.dibujar(screen):
            run = False
    
    #Se comienza a ejecutar el juego
    if juego_corriendo:
        
        screen.fill(BLACK)
        
        #CODIGO DE JUEGO
        
        if boton_menu.dibujar(screen):
            juego_corriendo = False
            juego_pausado = True
    
    #El juego está en estado de pausa
    if juego_pausado:
        screen.fill(BLUE)
        screen.blit(titulo_img, [50,-70])
        screen.blit(pygame.transform.scale(option_2_img, (135,55)), [320, 400])
        
        if boton_resume.dibujar(screen):
            juego_pausado = False
            juego_corriendo = True
        
        if boton_sound_on_2.dibujar(screen):
            if tema_batalla_encendido == False:
                tema_batalla_encendido = True
                battle_theme.play(-1)
        
        if boton_sound_off_2.dibujar(screen):
            tema_batalla_encendido = False
            battle_theme.stop()
        
        #if boton_option_2.dibujar(screen):
        #    print('OPTION 2')
        
        if boton_quit_2.dibujar(screen):
            run = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    #Actualiza la pantalla en cada ciclo
    pygame.display.update()

pygame.quit()
sys.exit()