import pygame
from sprites import *
from constantes import *
import sys

class Juego:
    def __init__(self):
        pygame.init() #inicia pygame
        self.screen = pygame.display.set_mode((PANTALLA_ANCHO, PANTALLA_ALTO))
        self.clock = pygame.time.Clock() #Configuracion de FPS
        self.fuente = pygame.font.Font('Arial.ttf', 32)
        self.corriendo = True
        
        self.plantilla_jugador = Plantilla_Sprites('img/character.png')
        self.plantilla_terreno = Plantilla_Sprites('img/terrain.png')
        self.plantilla_enemigo = Plantilla_Sprites('img/enemy.png')
        self.plantilla_ataque = Plantilla_Sprites('img/attack.png')
        self.intro_fondo = pygame.image.load('img/introbackground.png')
        self.muerte_fondo = pygame.image.load('img/gameover.png')
        
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
        #comienza un nuevo juego
        self.jugando = True #Verifica si el usuario esta jugando
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
        self.screen.fill(NEGRO)
        self.todos_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()
    
    def main(self):
        #Ciclo de juego
        while self.jugando:
            self.eventos() #Contiene configuración de teclas
            self.actualizar() #Actualiza la pantalla de juego
            self.mostrar()
        #self.corriendo = False
    
    def game_over(self):
        texto = self.fuente.render('Game Over', True, BLANCO)
        texto_rect = texto.get_rect(center=(PANTALLA_ANCHO/2, PANTALLA_ALTO/2))
        
        boton_restart = Boton (10, PANTALLA_ALTO - 60 , 120, 50, BLANCO, NEGRO, 'Restart', 32)

        for sprite in self.todos_sprites:
            sprite.kill()
        
        while self.corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.corriendo = False
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_presionado = pygame.mouse.get_pressed()
            
            if boton_restart.es_presionado(mouse_pos, mouse_presionado):
                self.nuevo()
                self.main()
            
            self.screen.blit(self.muerte_fondo, (0,0))
            self.screen.blit(texto, texto_rect)
            self.screen.blit(boton_restart.image, boton_restart.rect)
            self.clock.tick(FPS)
            pygame.display.update()
            
    def intro_screen(self):
        intro = True
        titulo = self.fuente.render('Awesome Game', True, NEGRO)
        titulo_rect = titulo.get_rect(x=10, y=10)
        boton_jugar = Boton(10, 50, 100, 50, BLANCO, NEGRO, 'Play', 32)
        while intro:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    intro = False
                    self.corriendo = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_presionado = pygame.mouse.get_pressed()
            
            if boton_jugar.es_presionado(mouse_pos, mouse_presionado):
                intro = False
            
            self.screen.blit(self.intro_fondo, (0,0))
            self.screen.blit(titulo, titulo_rect)
            self.screen.blit(boton_jugar.image, boton_jugar.rect)
            self.clock.tick(FPS)
            pygame.display.update()
                
    
juego = Juego()
juego.intro_screen()
juego.nuevo()
while juego.corriendo:
    juego.main()
    juego.game_over()
pygame.quit()
sys.exit()