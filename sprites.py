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
    
        self.animaciones_bajar = [self.juego.plantilla_jugador.get_plantilla(3, 2, self.ancho, self.alto),
                        self.juego.plantilla_jugador.get_plantilla(35, 2, self.ancho, self.alto),
                        self.juego.plantilla_jugador.get_plantilla(68, 2, self.ancho, self.alto)]

        self.animaciones_subir = [self.juego.plantilla_jugador.get_plantilla(3, 34, self.ancho, self.alto),
                        self.juego.plantilla_jugador.get_plantilla(35, 34, self.ancho, self.alto),
                        self.juego.plantilla_jugador.get_plantilla(68, 34, self.ancho, self.alto)]

        self.animaciones_izquierda = [self.juego.plantilla_jugador.get_plantilla(3, 98, self.ancho, self.alto),
                        self.juego.plantilla_jugador.get_plantilla(35, 98, self.ancho, self.alto),
                        self.juego.plantilla_jugador.get_plantilla(68, 98, self.ancho, self.alto)]

        self.animaciones_derecha = [self.juego.plantilla_jugador.get_plantilla(3, 66, self.ancho, self.alto),
                            self.juego.plantilla_jugador.get_plantilla(35, 66, self.ancho, self.alto),
                            self.juego.plantilla_jugador.get_plantilla(68, 66, self.ancho, self.alto)]
    
    def movimiento(self):
        teclas = pygame.key.get_pressed()#Lista de todas las teclas que pueden ser apretadas
        if teclas[pygame.K_LEFT]:
            for sprite in self.juego.todos_sprites:
                sprite.rect.x += VELOCIDAD_JUGADOR
            self.x_cambio -= VELOCIDAD_JUGADOR
            self.direccion = 'izquierda'
        if teclas[pygame.K_RIGHT]:
            for sprite in self.juego.todos_sprites:
                sprite.rect.x -= VELOCIDAD_JUGADOR
            self.x_cambio += VELOCIDAD_JUGADOR
            self.direccion = 'derecha'
        if teclas[pygame.K_UP]:
            for sprite in self.juego.todos_sprites:
                sprite.rect.y += VELOCIDAD_JUGADOR
            self.y_cambio -= VELOCIDAD_JUGADOR
            self.direccion = 'arriba'
        if teclas[pygame.K_DOWN]:
            for sprite in self.juego.todos_sprites:
                sprite.rect.y -= VELOCIDAD_JUGADOR
            self.y_cambio += VELOCIDAD_JUGADOR
            self.direccion = 'abajo'
    
    def colision_enemigo(self):
        choque = pygame.sprite.spritecollide(self, self.juego.enemigos, False)
        if choque:
            self.kill() #borra el sprite de Jugador de la pantalla
            self.juego.jugando = False #El juego deja de correr
            #self.juego.corriendo = True
    
    def colision_arboles(self, direccion):
        if direccion == "x":
            choque = pygame.sprite.spritecollide(self, self.juego.arboles, False)
            if choque:
                if self.x_cambio > 0:
                    self.rect.x = choque[0].rect.left - self.rect.width
                    for sprite in self.juego.todos_sprites:
                        sprite.rect.x += VELOCIDAD_JUGADOR
                if self.x_cambio < 0:
                    self.rect.x = choque[0].rect.right
                    for sprite in self.juego.todos_sprites:
                        sprite.rect.x -= VELOCIDAD_JUGADOR
        if direccion == "y":
            choque = pygame.sprite.spritecollide(self, self.juego.arboles, False)
            if choque:
                if self.y_cambio > 0:
                    self.rect.y = choque[0].rect.top - self.rect.height
                    for sprite in self.juego.todos_sprites:
                        sprite.rect.y += VELOCIDAD_JUGADOR
                if self.y_cambio < 0:
                    self.rect.y = choque[0].rect.bottom
                    for sprite in self.juego.todos_sprites:
                        sprite.rect.y -= VELOCIDAD_JUGADOR

    def animacion(self):
        
        if self.direccion == "abajo":
            if self.y_cambio == 0: #Si se queda parado
                self.image = self.juego.plantilla_jugador.get_plantilla(3, 2, self.ancho, self.alto)
            else: #Si se mueve hacia abajo
                self.image = self.animaciones_bajar[math.floor(self.bucle_animacion)]
                self.bucle_animacion += 0.1
                if self.bucle_animacion >= 3:
                    self.bucle_animacion = 1
        
        if self.direccion == "arriba":
            if self.y_cambio == 0: #Si se queda parado
                self.image = self.juego.plantilla_jugador.get_plantilla(3, 34, self.ancho, self.alto)
            else: #Si se mueve hacia abajo
                self.image = self.animaciones_subir[math.floor(self.bucle_animacion)]
                self.bucle_animacion += 0.1
                if self.bucle_animacion >= 3:
                    self.bucle_animacion = 1
        
        if self.direccion == "izquierda":
            if self.x_cambio == 0: #Si se queda parado
                self.image = self.juego.plantilla_jugador.get_plantilla(3, 98, self.ancho, self.alto)
            else: #Si se mueve hacia abajo
                self.image = self.animaciones_izquierda[math.floor(self.bucle_animacion)]
                self.bucle_animacion += 0.1
                if self.bucle_animacion >= 3:
                    self.bucle_animacion = 1
        
        if self.direccion == "derecha":
            if self.x_cambio == 0: #Si se queda parado
                self.image = self.juego.plantilla_jugador.get_plantilla(3, 66, self.ancho, self.alto)
            else: #Si se mueve hacia abajo
                self.image = self.animaciones_derecha[math.floor(self.bucle_animacion)]
                self.bucle_animacion += 0.1
                if self.bucle_animacion >= 3:
                    self.bucle_animacion = 1

class Ataque(pygame.sprite.Sprite): #Clase en pygame para manejar sprites mas facilmente
    def __init__(self, juego, x, y): #x, y: coordenadas de lo que aparezca en pantalla
        self.juego = juego
        #self.capa = CAPA_ATAQUE #Las capas permiten dar un orden a los sprites
        self.grupos = self.juego.todos_sprites, self.juego.ataques
        pygame.sprite.Sprite.__init__(self, self.grupos)
        
        self.x = x
        self.y = y
        self.ancho = TAMANIO_MOSAICO
        self.alto = TAMANIO_MOSAICO
        
        self.bucle_animacion = 0
        self.image = self.juego.plantilla_ataque.get_plantilla(0 , 0, self.ancho, self.alto)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.animaciones_derecha = [self.juego.plantilla_ataque.get_plantilla(0, 64, self.ancho, self.alto),
                        self.juego.plantilla_ataque.get_plantilla(32, 64, self.ancho, self.alto),
                        self.juego.plantilla_ataque.get_plantilla(64, 64, self.ancho, self.alto),
                        self.juego.plantilla_ataque.get_plantilla(96, 64, self.ancho, self.alto),
                        self.juego.plantilla_ataque.get_plantilla(128, 64, self.ancho, self.alto)]

        self.animaciones_abajo = [self.juego.plantilla_ataque.get_plantilla(0, 32, self.ancho, self.alto),
                        self.juego.plantilla_ataque.get_plantilla(32, 32, self.ancho, self.alto),
                        self.juego.plantilla_ataque.get_plantilla(64, 32, self.ancho, self.alto),
                        self.juego.plantilla_ataque.get_plantilla(96, 32, self.ancho, self.alto),
                        self.juego.plantilla_ataque.get_plantilla(128, 32, self.ancho, self.alto)]

        self.animaciones_izquierda = [self.juego.plantilla_ataque.get_plantilla(0, 96, self.ancho, self.alto),
                        self.juego.plantilla_ataque.get_plantilla(32, 96, self.ancho, self.alto),
                        self.juego.plantilla_ataque.get_plantilla(64, 96, self.ancho, self.alto),
                        self.juego.plantilla_ataque.get_plantilla(96, 96, self.ancho, self.alto),
                        self.juego.plantilla_ataque.get_plantilla(128, 96, self.ancho, self.alto)]

        self.animaciones_arriba = [self.juego.plantilla_ataque.get_plantilla(0, 0, self.ancho, self.alto),
                        self.juego.plantilla_ataque.get_plantilla(32, 0, self.ancho, self.alto),
                        self.juego.plantilla_ataque.get_plantilla(64, 0, self.ancho, self.alto),
                        self.juego.plantilla_ataque.get_plantilla(96, 0, self.ancho, self.alto),
                        self.juego.plantilla_ataque.get_plantilla(128, 0, self.ancho, self.alto)]
        
    def update(self):
        self.colision()
        self.animacion()
    
    def colision(self):
        #choque = 
        pygame.sprite.spritecollide(self, self.juego.enemigos, True)
    
    def animacion(self):
        
        direccion = self.juego.jugador.direccion
        
        if direccion == 'arriba':
            self.image = self.animaciones_arriba[math.floor(self.bucle_animacion)]
            self.bucle_animacion += 0.5
            if self.bucle_animacion >= 5:
                self.kill()
        
        if direccion == 'abajo':
            self.image = self.animaciones_abajo[math.floor(self.bucle_animacion)]
            self.bucle_animacion += 0.5
            if self.bucle_animacion >= 5:
                self.kill()
        
        if direccion == 'izquierda':
            self.image = self.animaciones_izquierda[math.floor(self.bucle_animacion)]
            self.bucle_animacion += 0.5
            if self.bucle_animacion >= 5:
                self.kill()
        
        if direccion == 'derecha':
            self.image = self.animaciones_derecha[math.floor(self.bucle_animacion)]
            self.bucle_animacion += 0.5
            if self.bucle_animacion >= 5:
                self.kill()
                
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
        
        self.animaciones_izquierda = [self.juego.plantilla_enemigo.get_plantilla(3, 98, self.ancho, self.alto),
                        self.juego.plantilla_enemigo.get_plantilla(35, 98, self.ancho, self.alto),
                        self.juego.plantilla_enemigo.get_plantilla(68, 98, self.ancho, self.alto)]

        self.animaciones_derecha = [self.juego.plantilla_enemigo.get_plantilla(3, 66, self.ancho, self.alto),
                            self.juego.plantilla_enemigo.get_plantilla(35, 66, self.ancho, self.alto),
                            self.juego.plantilla_enemigo.get_plantilla(68, 66, self.ancho, self.alto)]
        
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
        
        if self.direccion == "izquierda":
            if self.x_cambio == 0: #Si se queda parado
                self.image = self.juego.plantilla_jugador.get_plantilla(3, 98, self.ancho, self.alto)
            else: #Si se mueve hacia abajo
                self.image = self.animaciones_izquierda[math.floor(self.bucle_animacion)]
                self.bucle_animacion += 0.1
                if self.bucle_animacion >= 3:
                    self.bucle_animacion = 1
        
        if self.direccion == "derecha":
            if self.x_cambio == 0: #Si se queda parado
                self.image = self.juego.plantilla_jugador.get_plantilla(3, 66, self.ancho, self.alto)
            else: #Si se mueve hacia abajo
                self.image = self.animaciones_derecha[math.floor(self.bucle_animacion)]
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
""""
class Boton:
    def __init__(self, x, y , ancho, alto, color_fuente, color_fondo, contenido, tamaño):
        self.fuente = pygame.font.Font('Arial.ttf', tamaño)
        self.contenido = contenido
        
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        
        self.color_fuente = color_fuente
        self.color_fondo = color_fondo
        
        self.image = pygame.Surface((self.ancho, self.alto))
        self.image.fill(self.color_fondo)
        self.rect = self.image.get_rect()
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.texto = self.fuente.render(self.contenido, True, self.color_fuente)
        self.texto_rect = self.texto.get_rect(center=(self.ancho/2, self.alto/2))
        self.image.blit(self.texto, self.texto_rect)
    
    def es_presionado (self, pos, presionado):
        if self.rect.collidepoint(pos):
            if presionado[0]:
                return True
            return False
        return False
"""