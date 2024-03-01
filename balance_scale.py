import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()

WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
gravity = 0.5
bounce_stop = 0.3
wall_thickness = 10
mouse_trajectory = []


class Ball:
    def __init__(self, space, radius, mass, x_pos=300, y_pos=300,GRAVITY = 9.81, AIR_RESISTANCE = 0.01, FRICTION = 0.5, ELASTICITY = 0.8):
        self.mass = mass
        self.GRAVITY = GRAVITY
        self.AIR_RESISTANCE = AIR_RESISTANCE
        self.FRICTION = FRICTION
        self.ELASTICITY = ELASTICITY
        self.selected = False
        self.radius = radius
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_speed = 0
        self.y_speed = 0
        self.friction = 0.5
        self.retention = 0.8
        density = mass / ((4/3) * math.pi * radius**3)
        self.body = pymunk.Body()
        self.body.position = (x_pos, y_pos)
        self.circle = pymunk.Circle(self.body, radius)
        self.circle.mass = mass
        self.circle.density = density
        self.circle.color = (255, 0, 0, 100)
        self.circle.elasticity = 0.8 
        self.circle.friction = 0.5  
        space.add(self.body, self.circle)

    def check_gravity(self, x_push, y_push):
        self.x_speed -= self.x_speed * self.AIR_RESISTANCE
        self.y_speed -= self.y_speed * self.AIR_RESISTANCE
        if not self.selected:
            if self.y_pos < HEIGHT - self.radius - (wall_thickness / 2):
                self.y_speed += gravity
            else:
              if self.y_speed > bounce_stop:
                   self.y_speed = self.y_speed * -1 * self.retention
              else:
                  if abs(self.y_speed) <= bounce_stop:
                    self.y_speed = 0
            if (self.x_pos < self.radius + (wall_thickness/2) and self.x_speed < 0) or \
                 (self.x_pos > WIDTH - self.radius - (wall_thickness/2) and self.x_speed > 0):
                self.x_speed *= -1 * self.retention
                if abs(self.x_speed) < bounce_stop:
                 self.x_speed = 0
            if self.y_speed == 0 and self.x_speed != 0:
                if self.x_speed > 0:
                    self.x_speed -= self.friction
                elif self.x_speed < 0:
                  self.x_speed += self.friction
        else:
            self.x_speed = x_push
            self.y_speed = y_push
        return self.y_speed

    def update_pos(self, mouse):
        if not self.selected:
            self.y_pos += self.y_speed
            self.x_pos += self.x_speed
        else:
            self.x_pos = mouse[0]
            self.y_pos = mouse[1]

    def check_select(self, pos):
        self.selected = False
        if self.circle.collidepoint(pos):
            self.selected = True
        return self.selected

def calc_motion_vector():
    x_speed = 0
    y_speed = 0
    if len(mouse_trajectory) > 10:
        x_speed = (mouse_trajectory[-1][0] - mouse_trajectory[0][0]) / len(mouse_trajectory)
        y_speed = (mouse_trajectory[-1][1] - mouse_trajectory[0][1]) / len(mouse_trajectory)
    return x_speed, y_speed


def update_pos(self, mouse):
        if not self.selected:
            self.y_pos += self.y_speed
            self.x_pos += self.x_speed
        else:
            self.x_pos = mouse[0]
            self.y_pos = mouse[1]

def check_select(self, pos):
        self.selected = False
        if self.circle.collidepoint(pos):
            self.selected = True
        return self.selected


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
    ball_mass = 1
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = (500, 350)

    body = pymunk.Body()
    body.position = (500, 350)
    rect = pymunk.Poly.create_box(body, (500, 40))
    rect.friction = 1
    rect.mass = ball_mass
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
    shape = pymunk.Segment(space.static_body, (0, 0), (width, 0), wall_thickness)
    FRICTION = 0.5
    ELASTICITY = 0.8
    rects = [
        [(width/2, height-10), (width, 20)],
        [(width/2, 10), (width, 20)],
        [(10, height/2), (20, height)],
        [(width-10, height/2), (20, height)],
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape.friction = FRICTION
        shape.elasticity = ELASTICITY
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.8  
        shape.friction = 0.5  
        space.add(body, shape)

def run(window, width, height):
    GRAVITY = 9.81
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    space = pymunk.Space()
    space.gravity = (0, GRAVITY * 100) 
    draw_options = pymunk.pygame_util.DrawOptions(window)

    ball = Ball(space, 30, 1)  # Adjusted mass to 1 kg
    space.gravity = (0, ball.GRAVITY * 100)
    create_boundaries(space, width, height)
    create_scale_base(space, width, height)
    create_scale_body(space)
    dragging = False
    original_gravity = space.gravity
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    if is_point_in_circle(pos, ball):
                        dragging = True
                        space.gravity = 0, 0
                        mouse_coords = pygame.mouse.get_pos()
                        mouse_trajectory.append(mouse_coords)
                        if len(mouse_trajectory) > 20:
                            mouse_trajectory.pop(0)
                        x_push, y_push = calc_motion_vector()
                        ball.check_gravity(x_push, y_push)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    dragging = False
                    space.gravity = original_gravity
                    mouse_coords = pygame.mouse.get_pos()
                    mouse_trajectory.append(mouse_coords)
                    if len(mouse_trajectory) > 20:
                        mouse_trajectory.pop(0)
                    x_push, y_push = calc_motion_vector()
                    ball.check_gravity(x_push, y_push)

        if dragging:
            pos = pygame.mouse.get_pos()
            ball.body.position = pos

        space.step(dt)
        draw(space, window, draw_options)
        clock.tick(fps)

    pygame.quit()

def is_point_in_circle(point, circle):
    circle = circle.circle
    dx = point[0] - circle.body.position.x
    dy = point[1] - circle.body.position.y
    distance_squared = dx ** 2 + dy ** 2
    return distance_squared <= circle.radius ** 2

if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)