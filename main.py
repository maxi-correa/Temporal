import pygame
from sprites import *
from constantes import *
from boton import *
import sys

class Juego:
    def __init__(self):
        pygame.init() #inicia pygame
        self.screen = pygame.display.set_mode((PANTALLA_ANCHO, PANTALLA_ALTO))
        pygame.display.set_caption("Adventure Time")
        self.clock = pygame.time.Clock() #Configuracion de FPS
        self.corriendo = True
        self.tema_batalla_encendido = False
        
        self.plantilla_jugador = Plantilla_Sprites('imagenes/character.png')
        self.plantilla_terreno = Plantilla_Sprites('imagenes/terrain.png')
        self.plantilla_enemigo = Plantilla_Sprites('imagenes/enemy.png')
        self.plantilla_ataque = Plantilla_Sprites('imagenes/attack.png')
        self.intro_fondo = pygame.image.load('imagenes/introbackground.png')
        self.muerte_fondo = pygame.image.load('imagenes/gameover.png')
        
        #Carga de imagenes para menú
        self.titulo_img = pygame.image.load('imagenes/adventure_time.png').convert_alpha()
        self.fondo_img = pygame.image.load('imagenes/fondo.png').convert_alpha()
        self.play_img = pygame.image.load('imagenes/play_btn.png').convert_alpha()
        self.quit_img = pygame.image.load('imagenes/quit_btn.png').convert_alpha()
        self.option_img = pygame.image.load('imagenes/option_btn.png').convert_alpha()
        self.sound_on_img = pygame.image.load('imagenes/sound_on_btn.png').convert_alpha()
        self.sound_off_img = pygame.image.load('imagenes/sound_off_btn.png').convert_alpha()
        
        #Carga de imagen de opción en main
        self.menu_img = pygame.image.load('imagenes/menu_btn.png').convert_alpha()
        
        #Carga de imagenes de pausa
        self.back_img = pygame.image.load('imagenes/back_btn.png').convert_alpha()
        self.option_2_img = pygame.image.load('imagenes/option_2_btn.png').convert_alpha()
        self.sound_on_2_img = pygame.image.load('imagenes/sound_on_2_btn.png').convert_alpha()
        self.sound_off_2_img = pygame.image.load('imagenes/sound_off_2_btn.png').convert_alpha()
        
        #Carga de imagenes para game over
        self.fondo_game_over_img = pygame.image.load('imagenes/fondo_game_over.png').convert_alpha()
        self.game_over_img = pygame.image.load('imagenes/game_over.png').convert_alpha()
        self.restart_img = pygame.image.load('imagenes/restart_btn.png').convert_alpha()
        self.quit_2_img = pygame.image.load('imagenes/quit_2_btn.png').convert_alpha()

        #Carga de sonido de menú y de batalla
        self.menu_theme = pygame.mixer.Sound('sonidos/menu_theme.ogg')
        self.battle_theme = pygame.mixer.Sound('sonidos/battle_theme.ogg')
        
    def crear_mapa(self):
        for z in CAPA:
            for i, fila in enumerate(MAPA): #i es la posición y fila es el valor
                for j, columna in enumerate(fila):
                    if z == 1:
                        Piso(self, j, i)
                    if columna == "A" and z == 2:
                        Arbol(self, j, i)
                    if columna == "E" and z == 3:
                        Enemigo(self, j, i)
                    if columna == "J" and z == 3:
                        self.jugador = Jugador(self, j, i)
    
    def nuevo(self):
        #Comienza un nuevo juego
        self.jugando = True #Verifica si el usuario esta jugando
        self.pausado = False
        self.todos_sprites = pygame.sprite.LayeredUpdates() #contiene todos los sprites
        self.arboles = pygame.sprite.LayeredUpdates()
        self.enemigos = pygame.sprite.LayeredUpdates()
        self.ataques = pygame.sprite.LayeredUpdates()
        
        self.crear_mapa()
    
    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.jugando = False
                self.corriendo = False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if self.jugador.direccion == 'arriba':
                        Ataque(self, self.jugador.rect.x, self.jugador.rect.y - TAMANIO_MOSAICO)
                    if self.jugador.direccion == 'abajo':
                        Ataque(self, self.jugador.rect.x, self.jugador.rect.y + TAMANIO_MOSAICO)
                    if self.jugador.direccion == 'izquierda':
                        Ataque(self, self.jugador.rect.x - TAMANIO_MOSAICO, self.jugador.rect.y)
                    if self.jugador.direccion == 'derecha':
                        Ataque(self, self.jugador.rect.x + TAMANIO_MOSAICO, self.jugador.rect.y)
    
    def actualizar(self):
        self.todos_sprites.update()
    
    def mostrar(self):
        boton_menu = Boton(750, 10, self.menu_img, 1)          
        
        self.screen.fill(NEGRO)
        self.todos_sprites.draw(self.screen)
        if boton_menu.dibujar(self.screen):
            pass
        self.clock.tick(FPS)
        pygame.display.update()
    
    def main(self):
        
        if self.tema_batalla_encendido == False:
            self.battle_theme.play(-1)
            self.tema_batalla_encendido = True
        
        boton_menu = Boton(750, 10, self.menu_img, 1)
        
        #Ciclo de juego
        while self.jugando:
            self.eventos() #Contiene configuración de teclas
            self.actualizar() #Actualiza la pantalla de juego
            self.mostrar() #Muestra los Sprites para el juego
            if boton_menu.dibujar(self.screen):
                self.pausado = True
                self.pausa()
    
    def pausa(self):
        
        #Instancia de botones
        boton_back = Boton(320, 300, self.back_img, 1.5)
        boton_sound_on_2 = Boton(470, 400, self.sound_on_2_img, 1.5)
        boton_sound_off_2 = Boton(550, 400, self.sound_off_2_img, 1.5)
        boton_quit_2 = Boton(320, 500, self.quit_2_img, 1.5)
        
        #Ciclo de pausa
        while self.pausado:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.pausado = False
                    self.jugando = False
                    self.corriendo = False
            
            self.screen.fill(AZUL)
            self.screen.blit(self.titulo_img, [50,-70])
            self.screen.blit(pygame.transform.scale(self.option_2_img, (135,55)), [320, 400])
            
            if boton_back.dibujar(self.screen):
                self.pausado = False
            
            if boton_sound_on_2.dibujar(self.screen):
                if self.tema_batalla_encendido == False:
                    self.battle_theme.play(-1)
                    self.tema_batalla_encendido = True
            
            if boton_sound_off_2.dibujar(self.screen):
                self.battle_theme.stop()
                self.tema_batalla_encendido = False
                
            if boton_quit_2.dibujar(self.screen):
                self.pausado = False
                self.jugando = False
                self.corriendo = False
            
            self.clock.tick(FPS)
            pygame.display.update()
        
    def game_over(self):

        for sprite in self.todos_sprites:
            sprite.kill() #.kill() es un recurso que elimina todos los sprites de la pantalla
        
        #Instancia de botones
        boton_resume = Boton(100, 320, self.restart_img, 1.5)
        boton_quit_2 = Boton(350, 320, self.quit_2_img, 1.5)
        
        while self.corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.corriendo = False
            
            if self.tema_batalla_encendido:
                self.battle_theme.stop()
                self.tema_batalla_encendido = False
            
            self.screen.blit(pygame.transform.scale(self.fondo_game_over_img, (960,600)), [-100,0])
            self.screen.blit(pygame.transform.scale(self.game_over_img, (600,80)), [0, 100])
            
            if boton_resume.dibujar(self.screen):
                self.nuevo()
                self.main()
            
            if boton_quit_2.dibujar(self.screen):
                self.corriendo = False
            
            self.clock.tick(FPS)
            pygame.display.update()
            
    def intro_screen(self):
        intro = True
        movimiento_fondo = 0
        
        self.menu_theme.play(-1) #-1 para reproducción infinita
        tema_menu_encendido = True
        
        #Instancia de botones
        boton_play = Boton(300, 250, self.play_img, 1)
        boton_quit = Boton(300, 450, self.quit_img, 1)
        boton_sound_on = Boton (520, 350, self.sound_on_img, 1.4)
        boton_sound_off = Boton(620, 350, self.sound_off_img, 1.4)
        boton_quit = Boton(300, 450, self.quit_img, 1)
        
        while intro:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    intro = False
                    self.corriendo = False
            
            #Fondo en movimiento
            movimiento_fondo_relativo = movimiento_fondo % self.fondo_img.get_rect().width
            self.screen.blit(self.fondo_img, (movimiento_fondo_relativo - self.fondo_img.get_rect().width,0))
            if movimiento_fondo_relativo < PANTALLA_ANCHO:
                self.screen.blit(self.fondo_img, (movimiento_fondo_relativo, 0))
            movimiento_fondo -= 1.5
            
            #Título del juego
            self.screen.blit(self.titulo_img, [50, -70])
            self.screen.blit(self.option_img, [300, 350])
            
            #Condiciones de los botones del menú
            if boton_play.dibujar(self.screen):
                intro = False
                self.menu_theme.stop()
            
            if boton_sound_on.dibujar(self.screen):
                if tema_menu_encendido == False:
                    tema_menu_encendido = True
                    self.menu_theme.play(-1)
            
            if boton_sound_off.dibujar(self.screen):
                tema_menu_encendido = False
                self.menu_theme.stop()
            
            if boton_quit.dibujar(self.screen):
                intro = False
                self.corriendo = False
                
            pygame.display.update()
            
    
juego = Juego()
juego.intro_screen()
juego.nuevo()
while juego.corriendo:
    juego.main()
    juego.game_over()
pygame.quit()
sys.exit()