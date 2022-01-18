from __future__ import annotations
import sys
import pygame
import time
import random


class Body:
    def __init__(self, x, y, mass, radius, v=[0, 0]) -> None:
        self.x = x
        self.y = y
        self.v = v
        self.m = mass
        self.r = radius
        self.color = random.choice(colors)
        self.trail = []

    def update(self, body: Body):
        if body == self:
            return
        dx = body.x - self.x
        dy = body.y - self.y
        r2 = dx * dx + dy * dy
        if r2 <= self.r * body.r:
            self.v[0] *= -1
            self.v[1] *= -1
        else:
            a = G * body.m / r2
            self.a = [a * dx, a * dy]
            self.v[0] += self.a[0]
            self.v[1] += self.a[1]
        self.x += self.v[0]
        self.y += self.v[1]


def init_bodies():
    return [
        Body(width / 3, height / 4, 1000000, 5, [-.3, .3]),
        Body(width / 1.8, height / 4, 1000000, 5, [.3, .3]),
        Body(width / 3, height / 1.8, 1000000, 5, [.3, -.3]),
        Body(width / 1.5, height / 1.5, 10000, 5, [-.1, -.3]),
        Body(width / 2, height / 2, 10000000000, 10)
    ]


def init_font(font=None):
    if not font:
        font = random.choice(pygame.font.get_fonts())
    return pygame.font.SysFont(font, 48), pygame.font.SysFont(font, 16), font


def process_textin():
    global G, bodies, error
    if len(textin) == 1:
        if textin[0][1].lower() == 'c':
            for body in bodies:
                body.color = random.choice(colors)
        elif textin[0][1].lower() == 'f':
            global myfont, myfontsmall
            myfont, myfontsmall, fname = init_font()
            print('new font:', fname)
        elif textin[0][1].lower() == 'h':
            print(help)
        else:
            error = [time.time(), 'ValueError1']
    if len(textin) > 1:
        if textin[0][1].lower() == 'g':
            try:
                G = G_ORIG * float(''.join([x[1] for x in textin[1:]]))
                bodies = init_bodies()
            except ValueError as e:
                error = [time.time(), str(e)]
        elif textin[0][1].lower() == 'i':
            try:
                n = int(''.join([x[1] for x in textin[1:]]))
                if n < 0:
                    raise ValueError('i cant travel back in time')
                global ITERATIONS
                ITERATIONS = n
            except ValueError as e:
                error = [time.time(), str(e)]
        else:
            error = [time.time(), 'ValueError2']
    textin.clear()


def iterations(n=1):
    for _ in range(n):
        for body1 in bodies:
            for body2 in bodies:
                body2.update(body1)
        for body in bodies:
            body.trail.append([body.x, body.y])
    for body in bodies:
        body.trail = body.trail[-1000:]


ITERATIONS = 10
G_ORIG = 6.67430 * 10 ** -11
G = G_ORIG
colors = [(255, 0, 0), (0, 255, 0),
          (255, 0, 255), (0, 255, 255), (255, 255, 0), (255, 255, 255)]
colors += [(x[0] // 2, x[1] // 2, x[2] // 2) for x in colors]

pygame.init()
pygame.font.init()
myfont, myfontsmall, _ = init_font('sourcecodepro')
clock = pygame.time.Clock()
size = width, height = 1280, 840
speed = [2, 2]
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
screen = pygame.display.set_mode(size, pygame.NOFRAME)
bodies = init_bodies()
textin = []
error = []
help = 'commands: \nh - help\ng{number} - multiply gravitational constant G by number and restart simulation\ni{number} - set number of iterations per tick\nc - change color\nf - change font'


print(help)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()
            elif event.key == pygame.K_RETURN:
                process_textin()
            elif event.key == pygame.K_BACKSPACE:
                if textin:
                    textin = textin[:-1]
                    if textin:
                        textin[-1][0] = time.time()
            else:
                textin.append([time.time(), event.unicode])
        if event.type == pygame.QUIT:
            sys.exit()

    clock.tick(60)

    iterations(ITERATIONS)

    screen.fill(black)

    for body in bodies:
        pygame.draw.circle(screen, body.color, (body.x, body.y), body.r)
        for point in body.trail:
            pygame.draw.circle(screen, body.color,
                               (point[0], point[1]), 1)

    if textin:
        if time.time() - textin[-1][0] > 3:
            process_textin()
        textsurface = myfont.render(
            ''.join([x[1] for x in textin]), True, white)
        screen.blit(textsurface, (0, 0))

    if error:
        if time.time() - error[0] < 1.5:
            errortext = myfontsmall.render(error[1], True, red)
            screen.blit(errortext, (0, myfont.get_height()))
        else:
            error.clear()

    fpstext = myfontsmall.render(
        f'{round(clock.get_fps(), 2)}', True, white)
    screen.blit(fpstext, (width - myfontsmall.get_height() * 3, 0))
    pygame.display.flip()
