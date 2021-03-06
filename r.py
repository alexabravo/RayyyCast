#Soy muy mala para esto de los juegos ): por mas que intente e intente no pude

import pygame
import sys
import time
from math import *

clock = pygame.time.Clock()

colors = {
    '1': (146, 60, 63),
    '2': (233, 70, 63),
    '3': (0, 130, 168),
    '4': (0, 0, 0),
    "\n": (0, 0, 0)
}
inicio = pygame.image.load('./personajes/ini.jpg')
ganaste  = pygame.image.load('./personajes/ganaste.png')
perdiste = pygame.image.load('./personajes/perdiste.gif')
pacman = pygame.image.load('./Personajes/pac.jpg')
pacman = pygame.transform.scale(pacman, (50, 50))

textures = {
    '1' : pygame.image.load('./Personajes/fondo.jpg'),
    '2' : pygame.image.load('./Personajes/fondo.jpg'),
    '3' : pygame.image.load('./Personajes/celeste.jpg'),
    '4' : pygame.image.load('./Personajes/rosa.jpg'),
    '5' : pygame.image.load('./Personajes/rojo.jpg'),
    '6' : pygame.image.load('./Personajes/naranja.jpg'),
    '7' : pygame.image.load('./Personajes/meta.jpg')
    }

noir = (0, 0, 0)
blanc = (255, 255, 255)

class Raycaster:
    def __init__(self, screen):
        _, _, self.width, self.height = screen.get_rect()
        self.zbuffer = [-float('inf') for z in range(0, 500)]
        self.screen = screen
        self.blocksize = 50
        self.map = []

        self.player = {
            "x": self.blocksize + 20,
            "y": self.blocksize + 20,
            "a": 0,
            "fov": pi/3
        }
        
    def point(self, x, y, c):
        screen.set_at((x, y), c)

    def draw_rectangle(self, x, y, texture):
        for cx in range(x, x + 50):
            for cy in range(y, y + 50):
                tx = int((cx - x) * 128 / 50)
                ty = int((cy - y) * 128 / 50)
                c = texture.get_at((tx, ty))
                self.point(cx, cy, c)

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def draw_player(self, xi, yi, w=256, h=256):
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * 32 / w)
                ty = int((y - yi) * 32 / h)
                c = pacman.get_at((tx, ty))
                if c != (152, 0, 136, 255):
                    self.point(x, y, c)

    def cast_ray(self, a):
        d = 0
        while True:
            x = int(self.player["x"] + d * cos(a))
            y = int(self.player["y"] + d * sin(a))

            i = int(x / self.blocksize)
            j = int(y / self.blocksize)

            if self.map[j][i] != ' ':
                hitx = x - i * 50
                hity = y - j * 50
                if 1 < hitx < 49:
                    maxhit = hitx
                else:
                    maxhit = hity
                tx = int(maxhit * 128 / 50)
                return d, self.map[j][i], tx
            self.point(x, y, blanc)
            d += 1

    def draw_stake(self, x, h, tx, texture):
        start = int(250 - h / 2)
        end = int(250 + h / 2)
        for y in range(start, end):
            ty = int((y - start) * (128 / (end - start)))
            c = texture.get_at((tx, ty))
            self.point(x, y, c)

    def draw_sprite(self, sprite):
        sprite_a = atan2((sprite["y"] - self.player["y"]), (sprite["x"] - self.player["x"]))
        sprite_d = ((self.player["x"] - sprite["x"]) ** 2 + \
                    (self.player["y"] - sprite["y"]) ** 2) ** 0.5
        sprite_size = int(500 / sprite_d * 70)
        sprite_x = int(500 + (sprite_a - self.player["a"]) * 500 / self.player["fov"] + \
                       250 - sprite_size / 2)
        sprite_y = int(250 - sprite_size / 2)

        for x in range(sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                if 500 < x < 1000 and self.zbuffer[x - 500] >= sprite_d:
                    tx = int((x - sprite_x) * 128 / sprite_size)
                    ty = int((y - sprite_y) * 128 / sprite_size)
                    c = sprite["texture"].get_at((tx, ty))
                    if c != (152, 0, 136, 255):
                        self.point(x, y, c)
                        self.zbuffer[x - 500] = sprite_d


#Referencia https://pythonprogramming.net/pygame-start-menu-tutorial/
    def inicio(self):
        while True:
            screen.fill((0, 0, 0))
            d = 10
            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    exit(0)
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_a:
                        r.player["a"] -= pi / 20

                    if e.key == pygame.K_d:
                        r.player["a"] += pi / 20

                    if e.key == pygame.K_w:
                        r.player["x"] += int(d * cos(r.player["a"]))
                        r.player["y"] += int(d * sin(r.player["a"]))

                    if e.key == pygame.K_s:
                        r.player["x"] -= int(d * cos(r.player["a"]))
                        r.player["y"] -= int(d * sin(r.player["a"]))

                    if (r.player["x"] > 394) and (r.player["y"] > 70):
                        self.campeon()

            r.render()
            screen.blit(self.update_fps(), (850, 455))
            pygame.display.flip()

    def text_objects(self, text, font):
        textSurface = font.render(text, True, blanc)
        return textSurface, textSurface.get_rect()
    
    def musicaGanadora(self):
        pygame.mixer.music.load('./Musica/ganar.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        
    def musicaPerdedora(self):
        pygame.mixer.music.load('./Musica/muerto.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        
    def musica(self):
        pygame.mixer.music.load('./Musica/panmaan.wav')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        
    def menu(self):
        self.musica()
        m = True
        while m:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.K_3:
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.inicio()
                    if event.type == pygame.KEYDOWN:
                        if event.type == pygame.K_3:
                            exit(0)

            texto = pygame.font.SysFont('comicsansms', 25, True)
            TextSurf, TextRect = self.text_objects("Presione 1 para iniciar", texto)
            TextRect.center = (int(self.width / 2), int(self.height / 2))
            screen.blit(TextSurf, TextRect)
    
            pygame.display.update()
            clock.tick(15)
            screen.blit(inicio, (0, 0))
            
    def campeon(self):
        self.musicaGanadora
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    exit(0)
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_0:
                        intro = False
                        self.menu()

            felicitaciones = pygame.font.SysFont('comicsansms', 50, False)
            TextSurf, TextRect = self.text_objects("Felicidades Ganaste", felicitaciones)
            TextRect.center = (int(self.width / 1.25), int(self.height / 3))
            screen.blit(TextSurf, TextRect)

            pygame.display.update()
            clock.tick(15)
            screen.blit(ganaste, (0, 0))

    def perdedpr(self):
        self.musicaPerdedora
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    exit(0)
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_0:
                        intro = False
                        self.menu()

            felicitaciones = pygame.font.SysFont('comicsansms', 50, False)
            TextSurf, TextRect = self.text_objects("Game Over", felicitaciones)
            TextRect.center = (int(self.width / 1.25), int(self.height / 3))
            screen.blit(TextSurf, TextRect)

            pygame.display.update()
            clock.tick(15)
            screen.blit(ganaste, (0, 0))
            
    def render(self):
        for x in range(0, int(self.width / 2), self.blocksize):
            for y in range(0, self.height, self.blocksize):
                i = int(x / self.blocksize)
                j = int(y / self.blocksize)
                if self.map[j][i] != ' ':
                    self.draw_rectangle(x, y, textures[self.map[j][i]])

        self.point(self.player["x"], self.player["y"], blanc)

        for i in range(0, 500):
            a = self.player["a"] - self.player["fov"] / 2 + (i * self.player["fov"] / 500)
            d, m, tx = self.cast_ray(a)
            self.zbuffer[i] = d
            x = 500 + i
            h = (500 / (d * cos(a - self.player["a"]))) * 50
            self.draw_stake(x, h, tx, textures[m])

        for i in range(0, 500):
            self.point(499, i, (0, 0, 0))
            self.point(500, i, (0, 0, 0))
            self.point(501, i, (0, 0, 0))

        self.draw_player(1000 - 256 - 128, 500 - 256)

    def update_fps(self):
        font = pygame.font.SysFont("comicsansms", 25)
        fps = "FPS: " + str(int(clock.get_fps()))
        fps_text = font.render(fps, 1, pygame.Color(blanc))
        return fps_text

    
pygame.init()
screen = pygame.display.set_mode((1000, 500))
screen.set_alpha(None)
r = Raycaster(screen)
r.load_map('./mapa.txt')
clock = pygame.time.Clock()
r.menu()

