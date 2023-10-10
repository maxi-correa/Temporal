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
        self.bucle_animacion = 1
        
        self.image = self.juego.plantilla_jugador.get_plantilla(3, 2, self.ancho, self.alto)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self):
        self.movimiento()
        self.animacion()
        self.colision_enemigo()
        
        self.rect.x += self.x_cambio
        self.colision_arboles('x')
        self.rect.y += self.y_cambio
        self.colision_arboles('y')
        
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
    
    def colision_enemigo(self):
        choque = pygame.sprite.spritecollide(self, self.juego.enemigos, False)
        if choque:
            self.muerte()
            self.juego.corriendo = False
    
    def colision_arboles(self, direccion):
        if direccion == "x":
            choque = pygame.sprite.spritecollide(self, self.juego.arboles, False)
            if choque:
                if self.x_cambio > 0:
                    self.rect.x = choque[0].rect.left - self.rect.width
                if self.x_cambio < 0:
                    self.rect.x = choque[0].rect.right
        if direccion == "y":
            choque = pygame.sprite.spritecollide(self, self.juego.arboles, False)
            if choque:
                    if self.y_cambio > 0:
                        self.rect.y = choque[0].rect.top - self.rect.height
                    if self.y_cambio < 0:
                        self.rect.y = choque[0].rect.bottom
    
    def animacion(self):
        
        animaciones_bajar = [self.juego.plantilla_jugador.get_plantilla(3, 2, self.ancho, self.alto),
                        self.juego.plantilla_jugador.get_plantilla(35, 2, self.ancho, self.alto),
                        self.juego.plantilla_jugador.get_plantilla(68, 2, self.ancho, self.alto)]

        animaciones_subir = [self.juego.plantilla_jugador.get_plantilla(3, 34, self.ancho, self.alto),
                        self.juego.plantilla_jugador.get_plantilla(35, 34, self.ancho, self.alto),
                        self.juego.plantilla_jugador.get_plantilla(68, 34, self.ancho, self.alto)]

        animaciones_izquierda = [self.juego.plantilla_jugador.get_plantilla(3, 98, self.ancho, self.alto),
                        self.juego.plantilla_jugador.get_plantilla(35, 98, self.ancho, self.alto),
                        self.juego.plantilla_jugador.get_plantilla(68, 98, self.ancho, self.alto)]

        animaciones_derecha = [self.juego.plantilla_jugador.get_plantilla(3, 66, self.ancho, self.alto),
                            self.juego.plantilla_jugador.get_plantilla(35, 66, self.ancho, self.alto),
                            self.juego.plantilla_jugador.get_plantilla(68, 66, self.ancho, self.alto)]
        
        if self.direccion == "abajo":
            if self.y_cambio == 0: #Si se queda parado
                self.image = self.juego.plantilla_jugador.get_plantilla(3, 2, self.ancho, self.alto)
            else: #Si se mueve hacia abajo
                self.image = animaciones_bajar[math.floor(self.bucle_animacion)]
                self.bucle_animacion += 0.1
                if self.bucle_animacion >= 3:
                    self.bucle_animacion = 1
        
        if self.direccion == "arriba":
            if self.y_cambio == 0: #Si se queda parado
                self.image = self.juego.plantilla_jugador.get_plantilla(3, 34, self.ancho, self.alto)
            else: #Si se mueve hacia abajo
                self.image = animaciones_subir[math.floor(self.bucle_animacion)]
                self.bucle_animacion += 0.1
                if self.bucle_animacion >= 3:
                    self.bucle_animacion = 1
        
        if self.direccion == "izquierda":
            if self.x_cambio == 0: #Si se queda parado
                self.image = self.juego.plantilla_jugador.get_plantilla(3, 98, self.ancho, self.alto)
            else: #Si se mueve hacia abajo
                self.image = animaciones_izquierda[math.floor(self.bucle_animacion)]
                self.bucle_animacion += 0.1
                if self.bucle_animacion >= 3:
                    self.bucle_animacion = 1
        
        if self.direccion == "derecha":
            if self.x_cambio == 0: #Si se queda parado
                self.image = self.juego.plantilla_jugador.get_plantilla(3, 66, self.ancho, self.alto)
            else: #Si se mueve hacia abajo
                self.image = animaciones_derecha[math.floor(self.bucle_animacion)]
                self.bucle_animacion += 0.1
                if self.bucle_animacion >= 3:
                    self.bucle_animacion = 1
                    
class Enemigo(pygame.sprite.Sprite): #Clase en pygame para manejar sprites mas facilmente
    def __init__(self, juego, x, y): #x, y: coordenadas de lo que aparezca en pantalla
        self.juego = juego
        #self.capa = CAPA_ENEMIGO #Las capas permiten dar un orden a los sprites
        self.grupos = self.juego.todos_sprites, self.juego.enemigos
        pygame.sprite.Sprite.__init__(self, self.grupos)
        
        self.x = x * TAMANIO_MOSAICO
        self.y = y * TAMANIO_MOSAICO
        self.ancho = TAMANIO_MOSAICO
        self.alto = TAMANIO_MOSAICO
        
        self.x_cambio = 0 #Variables temporales que guardan el cambio de movimiento durante el loop
        self.y_cambio = 0
        
        
        self.image = self.juego.plantilla_enemigo.get_plantilla(3, 2, self.ancho, self.alto)
        self.image.set_colorkey(NEGRO)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
        self.direccion = random.choice(['izquierda', 'derecha']) #Sirve para saber en que direccion mira el personaje
        self.bucle_animacion = 1
        self.bucle_movimiento = 0
        self.viaje_maximo = random.randint(30, 50)
        
    def update(self):
        self.movimiento()
        self.animacion()
        
        self.rect.x += self.x_cambio
        self.rect.y += self.y_cambio
        
        self.x_cambio = 0
        self.y_cambio = 0
    
    def movimiento(self):
        if self.direccion == 'izquierda':
            self.x_cambio -= VELOCIDAD_ENEMIGO
            self.bucle_movimiento -= 1
            if self.bucle_movimiento <= -self.viaje_maximo:
                self.direccion = 'derecha'
        if self.direccion == 'derecha':
            self.x_cambio += VELOCIDAD_ENEMIGO
            self.bucle_movimiento += 1
            if self.bucle_movimiento >= self.viaje_maximo:
                self.direccion = 'izquierda'
    
    def animacion(self):
        
        animaciones_izquierda = [self.juego.plantilla_enemigo.get_plantilla(3, 98, self.ancho, self.alto),
                        self.juego.plantilla_enemigo.get_plantilla(35, 98, self.ancho, self.alto),
                        self.juego.plantilla_enemigo.get_plantilla(68, 98, self.ancho, self.alto)]

        animaciones_derecha = [self.juego.plantilla_enemigo.get_plantilla(3, 66, self.ancho, self.alto),
                            self.juego.plantilla_enemigo.get_plantilla(35, 66, self.ancho, self.alto),
                            self.juego.plantilla_enemigo.get_plantilla(68, 66, self.ancho, self.alto)]
        
        if self.direccion == "izquierda":
            if self.x_cambio == 0: #Si se queda parado
                self.image = self.juego.plantilla_jugador.get_plantilla(3, 98, self.ancho, self.alto)
            else: #Si se mueve hacia abajo
                self.image = animaciones_izquierda[math.floor(self.bucle_animacion)]
                self.bucle_animacion += 0.1
                if self.bucle_animacion >= 3:
                    self.bucle_animacion = 1
        
        if self.direccion == "derecha":
            if self.x_cambio == 0: #Si se queda parado
                self.image = self.juego.plantilla_jugador.get_plantilla(3, 66, self.ancho, self.alto)
            else: #Si se mueve hacia abajo
                self.image = animaciones_derecha[math.floor(self.bucle_animacion)]
                self.bucle_animacion += 0.1
                if self.bucle_animacion >= 3:
                    self.bucle_animacion = 1

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