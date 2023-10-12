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
        #self.fuente = pygame.font.Font('Arial.ttf', 32)
        self.corriendo = True
        
        self.plantilla_jugador = Plantilla_Sprites('img/character.png')
        self.plantilla_terreno = Plantilla_Sprites('img/terrain.png')
        self.plantilla_enemigo = Plantilla_Sprites('img/enemy.png')
        self.plantilla_ataque = Plantilla_Sprites('img/attack.png')
        self.intro_fondo = pygame.image.load('img/introbackground.png')
        self.muerte_fondo = pygame.image.load('img/gameover.png')
        
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

        #Carga de imagenes para game over
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
        
        self.battle_theme.play(-1)
    
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
        boton_menu = Boton(750, 10, self.menu_img, 1)
        
        #Ciclo de juego
        while self.jugando:
            self.eventos() #Contiene configuración de teclas
            self.actualizar() #Actualiza la pantalla de juego
            self.mostrar()
            if boton_menu.dibujar(self.screen):
                self.pausado = True
                self.pausa()
        #self.corriendo = False
    
    def pausa(self):
        
        #Instancia de botones
        boton_resume = Boton(320, 300, self.restart_img, 1.5)
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
            
            if boton_resume.dibujar(self.screen):
                self.pausado = False
            
            if boton_quit_2.dibujar(self.screen):
                self.pausado = False
                self.jugando = False
                self.corriendo = False
            
            self.clock.tick(FPS)
            pygame.display.update()
        
    def game_over(self):
        
        #texto = self.fuente.render('Game Over', True, BLANCO)
        #texto_rect = texto.get_rect(center=(PANTALLA_ANCHO/2, PANTALLA_ALTO/2))
        
        #boton_restart = Boton (10, PANTALLA_ALTO - 60 , 120, 50, BLANCO, NEGRO, 'Restart', 32)

        for sprite in self.todos_sprites:
            sprite.kill()
        
        #Instancia de botones
        boton_resume = Boton(320, 300, self.restart_img, 1.5)
        boton_quit_2 = Boton(320, 500, self.quit_2_img, 1.5)
        
        while self.corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.corriendo = False
            
            self.screen.fill(AZUL)
            #self.screen.blit(game_over_img, [50,50])
            self.screen.blit(pygame.transform.scale(self.game_over_img, (600,80)), [100, 100])
            
            if boton_resume.dibujar(self.screen):
                self.nuevo()
                self.main()
            
            if boton_quit_2.dibujar(self.screen):
                self.corriendo = False
            #mouse_pos = pygame.mouse.get_pos()
            #mouse_presionado = pygame.mouse.get_pressed()
            
            #if boton_restart.es_presionado(mouse_pos, mouse_presionado):
            #    self.nuevo()
            #    self.main()
            
            #self.screen.blit(self.muerte_fondo, (0,0))
            #self.screen.blit(texto, texto_rect)
            #self.screen.blit(boton_restart.image, boton_restart.rect)
            self.clock.tick(FPS)
            pygame.display.update()
            
    def intro_screen(self):
        intro = True
        movimiento_fondo = 0
        
        self.menu_theme.play(-1) #-1 para reproducción infinita
        tema_menu_encendido = True
        
        #Instancia de botones
        boton_play = Boton(300, 250, self.play_img, 1)
        #boton_option = Boton(300, 350, option_img, 1)
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
                #tema_batalla_encendido = True
                #battle_theme.play(-1)
            
            #if boton_option.dibujar(screen):
            #    print('OPTION')
            
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
    #juego.pausa()
    juego.game_over()
pygame.quit()
sys.exit()