import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()

WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

def draw(space, window, draw_option):
    window.fill("white")
    space.debug_draw(draw_option)
    pygame.display.update()

def create_scale_base(space, width, height):
    GOLD = (255, 215, 0, 0)
    rects = [
        [(500, height - 120), (35, 400), GOLD, 100]
    ]
    
    for pos, size, color, mass in rects:
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Poly.create_box(body, size, radius=2)
        shape.color = GOLD
        shape.mass = mass
        shape.elasticity = 0
        shape.friction = 0.4
        space.add(body, shape)

def create_scale_body(space):
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = (500, 350)

    body = pymunk.Body()
    body.position = (500, 350)
    rect = pymunk.Poly.create_box(body, (500, 40))
    rect.friction = 1
    rect.mass = 8
    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))
    space.add(rect, body, rotation_center_joint)

def create_ball(space, radius, mass):
    density = mass / ((4/3) * math.pi * radius**3)
    body = pymunk.Body()
    body.position = (300, 300)
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.density = density
    shape.color = (255, 0, 0, 100)
    shape.elasticity = 0.8 
    shape.friction = 0.5  
    space.add(body, shape)
    return shape

def create_boundaries(space, width, height):
    rects = [
        [(width/2, height-10), (width, 20)],
        [(width/2, 10), (width, 20)],
        [(10, height/2), (20, height)],
        [(width-10, height/2), (20, height)],
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.8  
        shape.friction = 0.5  
        space.add(body, shape)

def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    space = pymunk.Space()
    space.gravity = (0, 981)  

    draw_options = pymunk.pygame_util.DrawOptions(window)

    ball = create_ball(space, 30, 1)  # Adjusted mass to 1 kg
    create_boundaries(space, width, height)

    dragging = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    if is_point_in_circle(pos, ball):
                        dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    dragging = False

        if dragging:
            pos = pygame.mouse.get_pos()
            ball.body.position = pos

        space.step(dt)
        draw(space, window, draw_options)
        clock.tick(fps)

    pygame.quit()

def is_point_in_circle(point, circle):
    dx = point[0] - circle.body.position.x
    dy = point[1] - circle.body.position.y
    distance_squared = dx ** 2 + dy ** 2
    return distance_squared <= circle.radius ** 2

if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)
