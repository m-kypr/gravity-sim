from __future__ import annotations
import sys
import pygame
import time
import random


class Body:
    def __init__(self, x, y, mass, radius, v) -> None:
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
        if r2 <= (self.r + body.r) ** 2:
            self.v[0] *= -1
            self.v[1] *= -1
        else:
            a = G * body.m / r2
            # self.a = [a * dx, a * dy]
            self.v[0] += a * dx
            self.v[1] += a * dy
        self.x += self.v[0]
        self.y += self.v[1]

    def __repr__(self) -> str:
        return f'{self.x} {self.y} {self.m} {self.r}'


def init_bodies():
    bodyidx = None
    if selected and bodies:
        bodyidx = bodies.index(selected[1])
    bdis = [
        Body(width / 3, height / 4, 1000000, 6, [-.3, .3]),
        Body(width / 1.8, height / 4, 1000000, 5, [.3, .3]),
        Body(width / 3, height / 1.8, 1000000, 5, [.3, -.3]),
        Body(width / 1.5, height / 1.5, 10000, 5, [-.1, -.3]),
        Body(width / 1.93, height / 4, 1000, 1, [.1, .1]),
        Body(width / 1.95, height / 4, 1000, 1, [.1, .1]),
        Body(width / 1.97, height / 4, 1000, 1, [.1, .1]),
        Body(width / 1.99, height / 4, 1000, 1, [.1, .1]),
        Body(width / 2, height / 2, 10000000000, 10, [0, 0])
    ]
    if bodyidx:
        selected[0] = time.time()
        selected[1] = bodies[bodyidx]
    return bdis


def init_font(font=None):
    if not font:
        font = random.choice(pygame.font.get_fonts())
    return pygame.font.SysFont(font, 48), pygame.font.SysFont(font, 16), font


def process_textin():
    global G, bodies, status
    if len(textin) == 1:
        if textin[0][1].lower() == 'c':
            for body in bodies:
                body.color = random.choice(colors)
        if textin[0][1].lower() == 't':
            global show_trails
            show_trails = not show_trails
        elif textin[0][1].lower() == 'h':
            print(help)
        else:
            status = [time.time(), red, 'ValueError1']
    elif len(textin) > 1:
        if textin[0][1].lower() == 't':
            try:
                global trail_size
                ts = int(''.join([x[1] for x in textin[1:]]))
                if ts > trail_size:
                    bodies = init_bodies()
                trail_size = ts
            except ValueError as e:
                status = [time.time(), red, str(e)]
        elif textin[0][1].lower() == 'g':
            try:
                G = G_ORIG * float(''.join([x[1] for x in textin[1:]]))
                bodies = init_bodies()
            except ValueError as e:
                status = [time.time(), red, str(e)]
        elif textin[0][1].lower() == 'i':
            try:
                n = int(''.join([x[1] for x in textin[1:]]))
                if n < 0:
                    raise ValueError('i cant travel back in time')
                global ITERATIONS
                ITERATIONS = n
            except ValueError as e:
                status = [time.time(), red, str(e)]
        elif textin[0][1].lower() == 'm':
            if selected:
                try:
                    n = int(''.join([x[1] for x in textin[1:]]))
                    if n < 0:
                        raise ValueError('negative mass')
                    selected[1].m = n
                except ValueError as e:
                    status = [time.time(), red, str(e)]
            else:
                status = [time.time(), red, 'no body selected']
        elif textin[0][1].lower() == 'r':
            if selected:
                try:
                    n = int(''.join([x[1] for x in textin[1:]]))
                    if n < 0:
                        raise ValueError('negative radius')
                    selected[1].r = n
                    print(bodies)
                except ValueError as e:
                    status = [time.time(), red, str(e)]
            else:
                status = [time.time(), red, 'no body selected']
        else:
            status = [time.time(), red, 'ValueError2']
    if not status:
        status = [time.time(), white, f">{''.join([x[1] for x in textin])}"]

    textin.clear()


def iterations(n=1):
    for _ in range(n):
        for body1 in bodies:
            for body2 in bodies:
                body2.update(body1)
        for body in bodies:
            body.trail.append([body.x, body.y])
    for body in bodies:
        body.trail = body.trail[-trail_size:]


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
init_size = size
speed = [2, 2]
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
screen = pygame.display.set_mode(size, pygame.NOFRAME)
selected = []
bodies = init_bodies()
textin = []
status = []
help = '\n    '.join(['commands:', 'global:', *('\n    '.join(['', 'h - help', 'g{number} - multiply gravitational constant G by number', 't{number} - set length of trail', 'i{number} - set number of iterations per tick',
                                                               't - toggle trails', 'c - change color', 'f - change font', 'q / [Esc] - quit', 'f11 - fullscreen'])).split('\n')[1:], 'body:', *('\n    '.join(['', 'm{number} - set mass', 'r{number} - set radius', '[left click] - select body', '[right click] - move body'])).split('\n')[1:]])
mousex, mousey = 0, 0
leftheld, rightheld = False, False
show_trails = True
trail_size = 1000
fullscreen = False

print(help)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_RETURN:
                process_textin()
            elif event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode(
                        (0, 0), pygame.FULLSCREEN)
                    info = pygame.display.Info()
                    size = width, height = info.current_w, info.current_h
                else:
                    screen = pygame.display.set_mode(init_size, pygame.NOFRAME)
                    size = width, height = init_size
                bodies = init_bodies()
            elif event.key == pygame.K_BACKSPACE:
                if textin:
                    textin = textin[:-1]
                    if textin:
                        textin[-1][0] = time.time()
            elif event.key in [pygame.K_TAB, pygame.K_LALT, pygame.K_RALT]:
                pass
            else:
                textin.append([time.time(), event.unicode])
        if event.type == pygame.QUIT:
            sys.exit()

    mousex, mousey = pygame.mouse.get_pos()
    left, middle, right = pygame.mouse.get_pressed(3)
    if left:
        if not leftheld:
            for body in bodies:
                if mousex > body.x - body.r and mousex < body.x + body.r:
                    if mousey > body.y - body.r and mousey < body.y + body.r:
                        selected = [time.time(), body]
                        break
            else:
                selected.clear()
        leftheld = True
    else:
        leftheld = False
    if right:
        if rightheld:
            if selected:
                selected[1].x = mousex
                selected[1].y = mousey
        rightheld = True
    else:
        rightheld = False

    clock.tick(60)

    iterations(ITERATIONS)

    screen.fill(black)

    for body in bodies:
        pygame.draw.circle(screen, body.color, (body.x, body.y), body.r)
        if selected:
            if body == selected[1]:
                pygame.draw.circle(screen, body.color,
                                   (body.x, body.y), body.r + 3, 1)
        if show_trails:
            for point in body.trail:
                pygame.draw.circle(screen, body.color,
                                   (point[0], point[1]), 1)

    if selected:
        body: Body = selected[1]
        x, y = body.x + body.r, body.y + body.r
        texts = [f'x: {round(body.x, 2)}  y: {round(body.y, 2)}',
                 f'mass: {body.m}', f'radius: {body.r}']
        textsizes = [myfontsmall.size(x) for x in texts]
        boxwidth, boxheight = max([x[0] for x in textsizes]), sum(
            [x[1] for x in textsizes])
        pygame.draw.rect(screen, (125, 125, 125),
                         (x, y, boxwidth, boxheight), 0)
        j = 0
        for text in texts:
            text1 = myfontsmall.render(
                text, True, white)
            screen.blit(text1, (x, y + textsizes[j][1] * j))
            j += 1

    if textin:
        if time.time() - textin[-1][0] > 4:
            process_textin()
        textsurface = myfont.render(
            ''.join([x[1] for x in textin]), True, white)
        screen.blit(textsurface, (0, 0))

    if status:
        if time.time() - status[0] < 1.5:
            errortext = myfontsmall.render(status[2], True, status[1])
            screen.blit(errortext, (0, myfont.get_height()))
        else:
            status.clear()

    fpstext = myfontsmall.render(
        f'{round(clock.get_fps(), 2)}', True, white)
    screen.blit(fpstext, (width - myfontsmall.get_height() * 3, 0))
    pygame.display.flip()
