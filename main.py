import pygame
from sprites import *
from constantes import *
import sys

class Juego:
    def __init__(self):
        pygame.init() #inicia pygame
        self.screen = pygame.display.set_mode((PANTALLA_ANCHO, PANTALLA_ALTO))
        self.clock = pygame.time.Clock() #Configuracion de FPS
        #self.fuente = pygame.font.Font('Arial', 32)
        self.corriendo = True
        
        self.plantilla_jugador = Plantilla_Sprites('img/character.png')
        self.plantilla_terreno = Plantilla_Sprites('img/terrain.png')
    
    def crear_mapa(self):
        for z in CAPA:
            for i, fila in enumerate(MAPA): #i es la posición y fila es el valor
                for j, columna in enumerate(fila):
                    if z == 1:
                        Piso(self, j, i)
                    if columna == "A" and z == 2:
                        Arbol(self, j, i)
                    if columna == "J" and z == 3:
                        Jugador(self, j, i)
    
    def nuevo(self):
        #comienza un nuevo juego
        self.jugando = True #Verifica si el usuario esta jugando
        self.todos_sprites = pygame.sprite.LayeredUpdates() #contiene todos los sprites
        self.arboles = pygame.sprite.LayeredUpdates()
        self.enemigos = pygame.sprite.LayeredUpdates()
        self.ataques = pygame.sprite.LayeredUpdates()
        
        self.crear_mapa()
    
    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.jugando = False
                self.corriendo = False
                
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
        self.corriendo = False
    
    def game_over(self):
        pass
    
    def intro_screen(self):
        pass
    
juego = Juego()
juego.intro_screen()
juego.nuevo()
while juego.corriendo:
    juego.main()
    juego.game_over()
pygame.quit()
sys.exit()