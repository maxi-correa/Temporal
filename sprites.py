import pygame
from constantes import *
import math
import random

class Plantilla_Sprites:
    def __init__(self, archivo):
        self.plantilla = pygame.image.load(archivo).convert()
    
    def get_plantilla(self, x, y, ancho, alto):
        plantilla = pygame.Surface([ancho, alto])
        plantilla.blit(self.plantilla, (0,0), (x, y, ancho, alto))
        plantilla.set_colorkey(NEGRO)
        return plantilla

class Jugador(pygame.sprite.Sprite): #Clase en pygame para manejar sprites mas facilmente
    def __init__(self, juego, x, y): #x, y: coordenadas de lo que aparezca en pantalla
        self.juego = juego
        #self.capa = CAPA_JUGADOR #Las capas permiten dar un orden a los sprites
        self.grupos = self.juego.todos_sprites
        pygame.sprite.Sprite.__init__(self, self.grupos)
        
        self.x = x * TAMANIO_MOSAICO
        self.y = y * TAMANIO_MOSAICO
        self.ancho = TAMANIO_MOSAICO
        self.alto = TAMANIO_MOSAICO
        
        self.x_cambio = 0 #Variables temporales que guardan el cambio de movimiento durante el loop
        self.y_cambio = 0
        
        self.direccion = 'abajo' #Sirve para saber en que direccion mira el personaje
        
        self.image = self.juego.plantilla_jugador.get_plantilla(3, 2, self.ancho, self.alto)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self):
        self.movimiento()
        
        self.rect.x += self.x_cambio
        self.rect.y += self.y_cambio
        
        self.x_cambio = 0
        self.y_cambio = 0
    
    def movimiento(self):
        teclas = pygame.key.get_pressed()#Lista de todas las teclas que pueden ser apretadas
        if teclas[pygame.K_LEFT]:
            self.x_cambio -= VELOCIDAD_JUGADOR
            self.direccion = 'izquierda'
        if teclas[pygame.K_RIGHT]:
            self.x_cambio += VELOCIDAD_JUGADOR
            self.direccion = 'derecha'
        if teclas[pygame.K_UP]:
            self.y_cambio -= VELOCIDAD_JUGADOR
            self.direccion = 'arriba'
        if teclas[pygame.K_DOWN]:
            self.y_cambio += VELOCIDAD_JUGADOR
            self.direccion = 'abajo'
            
class Arbol(pygame.sprite.Sprite):
    def __init__(self, juego, x, y):
        self.juego = juego
        #self.capa = CAPA_ARBOL
        self.grupos = self.juego.todos_sprites, self.juego.arboles
        pygame.sprite.Sprite.__init__(self, self.grupos)
        
        self.x = x * TAMANIO_MOSAICO
        self.y = y * TAMANIO_MOSAICO
        self.ancho = TAMANIO_MOSAICO
        self.alto = TAMANIO_MOSAICO
        
        self.image = self.juego.plantilla_terreno.get_plantilla(960, 448, self.ancho, self.alto)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Piso(pygame.sprite.Sprite):
    def __init__(self, juego, x, y):
        self.juego = juego
        #self.capa = CAPA_PISO
        self.grupos = self.juego.todos_sprites
        pygame.sprite.Sprite.__init__(self, self.grupos)
        
        self.x = x * TAMANIO_MOSAICO
        self.y = y * TAMANIO_MOSAICO
        self.ancho = TAMANIO_MOSAICO
        self.alto = TAMANIO_MOSAICO
        
        self.image = self.juego.plantilla_terreno.get_plantilla(64, 352, self.ancho, self.alto)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y