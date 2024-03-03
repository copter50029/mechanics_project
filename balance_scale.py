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
    def __init__(self, space, radius, mass,color, text_color=(0, 0, 0,255), x_pos=300, y_pos=300,GRAVITY = 9.81, AIR_RESISTANCE = 0.01, FRICTION = 0.5, ELASTICITY = 0.8):
        
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
        self.text_color = text_color
        self.font = pygame.font.Font(None, 24)
        self.friction = 0.5
        self.retention = 0.8
        density = mass / ((4/3) * math.pi * radius**3)
        self.body = pymunk.Body()
        self.body.position = (x_pos, y_pos)
        self.circle = pymunk.Circle(self.body, radius)
        self.circle.mass = mass
        self.circle.density = density
        self.circle.color = color
        self.circle.elasticity = 0.8 
        self.circle.friction = 0.5  
        space.add(self.body, self.circle)

    def draw_text(self, surface, text):
        text_object = self.font.render(str(text), True, self.text_color)
        text_rect = text_object.get_rect(center=self.body.position)
        surface.blit(text_object, text_rect)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.body.position, self.radius)
        self.draw_text(surface, self.body.mass)
        
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

    # Rectangle (base)
    rects = [
        [(500, height - 150), (20, 565), GOLD, 100]
    ]
    for pos, size, color, mass in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)  # Make body static
        body.position = pos
        shape = pymunk.Poly.create_box(body, size, radius=2)
        shape.color = color
        shape.mass = mass
        shape.sensor = False
        space.add(body, shape)

    return space




def create_scale_body(space):
    ball_mass = 1

    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = (500, 350)

    body = pymunk.Body()
    body.position = (500, 350)
    rect = pymunk.Poly.create_box(body, (500, 10))  
    rect.friction = 1
    rect.mass = ball_mass
    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, -100))
    block_rotation = pymunk.PinJoint(body, rotation_center_body, (0,-100), (100, 20))
    block_rotation1 = pymunk.PinJoint(body, rotation_center_body, (0,-100), (-100, 20))
    
    
    
    
     # Adding box 
    body1 = pymunk.Body(mass=10, moment=1000)
    body2 = pymunk.Body(mass=10, moment=1000)
    
    body1.position = (685, 280)
    body2.position = (315, 280)
    body1.apply_impulse_at_local_point((0, 0), (0, 0))
    body2.apply_impulse_at_local_point((0, 0), (0, 0))

    s1 = pymunk.Segment(body1, (60, 60), (-60, 60), 4)
    s2 = pymunk.Segment(body1, (-60, -60), (-60, 60), 4)
    s3 = pymunk.Segment(body1, (60, -60), (60, 60), 4)

    s11 = pymunk.Segment(body2, (60, 60), (-60, 60), 4)
    s22 = pymunk.Segment(body2, (-60, -60), (-60, 60), 4)
    s33 = pymunk.Segment(body2, (60, -60), (60, 60), 4)

    s1.elasticity = 0.01
    s2.elasticity = 0.01
    s3.elasticity = 0.01
    s11.elasticity = 0.01
    s22.elasticity = 0.01
    s33.elasticity = 0.01
    space.add(body, rect, rotation_center_joint,block_rotation,block_rotation1)
    space.add(body1,s1, s2, s3)
    space.add(body2, s11, s22, s33)

    # Add PivotJoint to connect the two boxes-
    pivot_joint = pymunk.PivotJoint(body,body1,(400,300))
    space.add(pivot_joint)
    pivot_joint1 = pymunk.PivotJoint(body,body2,(600,300) )
    space.add(pivot_joint1)
    return body1, body2


def create_ball(space, radius, mass):
    density = mass / ((4/3) * math.pi * radius**3)
    body = pymunk.Body()
    body.position = (300, 300)
    shape.collision_type = 1
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
    space = pymunk.Space()
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    handler = space.add_collision_handler(1, 2)
    handler.begin = lambda a, b, arbiter, space: False
    space = pymunk.Space()
    space.gravity = (0, GRAVITY * 100)
    draw_options = pymunk.pygame_util.DrawOptions(window)

    sball1 = Ball(space, 15, 0.5, (0, 0, 0,255)) #black  # Adjusted mass to 0.5 kg
    sball2 = Ball(space, 15, 1, (0, 0, 255,255)) #blue  # Adjusted mass to 1kg
    sball3 = Ball(space, 15, 1.5, (0, 255, 255,255)) #cyan  # Adjusted mass to 1.5kg
    sball4 = Ball(space, 15, 2, (255, 215, 0,255)) #gold   # Adjusted mass to 2kg
    sball5 = Ball(space, 15, 2.5, (190, 190, 190,255))#gray   # Adjusted mass to 2.5kg
    Bball1 =Ball(space, 30, 3, (0, 255, 0, 255))#green   # Adjusted mass to 3kg
    Bball2 =Ball(space, 30, 5, (255, 165, 0, 255))#orange  # Adjusted mass to 5kg
    Bball3 =Ball(space, 30, 7, (160, 32, 240, 255))#purple   # Adjusted mass to 7kg
    Bball4 =Ball(space, 30, 11, (255, 0, 0, 255))#red  # Adjusted mass to 11kg
    Bball5 =Ball(space, 30, 18, (255, 255, 0, 255))#yellow   # Adjusted mass to 18kg
    

    create_boundaries(space, width, height)
    create_scale_base(space, width, height)
    create_scale_body(space)
    

    dragging = [False, False,False,False,False,False, False,False,False,False]  # Separate drag states for each ball
    original_gravity = space.gravity

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    if is_point_in_circle(pos, sball1):
                        dragging[0] = True
                        sball1.body.force = 0, 0
                        space.gravity = 0, 0
                    elif is_point_in_circle(pos, sball2):
                        dragging[1] = True
                        sball2.body.force = 0, 0
                        space.gravity = 0, 0
                    elif is_point_in_circle(pos, sball3):
                        dragging[2] = True
                        sball3.body.force = 0, 0
                        space.gravity = 0, 0
                    elif is_point_in_circle(pos, sball4):
                        dragging[3] = True
                        sball4.body.force = 0, 0
                        space.gravity = 0, 0
                    elif is_point_in_circle(pos, sball5):
                        dragging[4] = True
                        sball5.body.force = 0, 0
                        space.gravity = 0, 0
                    elif is_point_in_circle(pos, Bball1):
                        dragging[5] = True
                        Bball1.body.force = 0, 0
                        space.gravity = 0, 0
                    elif is_point_in_circle(pos, Bball2):
                        dragging[6] = True
                        Bball2.body.force = 0, 0
                        space.gravity = 0, 0
                    elif is_point_in_circle(pos, Bball3):
                        dragging[7] = True
                        Bball3.body.force = 0, 0
                        space.gravity = 0, 0
                    elif is_point_in_circle(pos, Bball4):
                        dragging[8] = True
                        Bball4.body.force = 0, 0
                        space.gravity = 0, 0
                    elif is_point_in_circle(pos, Bball5):
                        dragging[9] = True
                        Bball5.body.force = 0, 0
                        space.gravity = 0, 0
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    if dragging[0]:
                        sball1.body.force = 0, -sball1.body.mass * GRAVITY * 100
                    if dragging[1]:
                        sball2.body.force = 0, -sball2.body.mass * GRAVITY * 100
                    if dragging[2]:
                        sball3.body.force = 0, -sball3.body.mass * GRAVITY * 100
                    if dragging[3]:
                        sball4.body.force = 0, -sball4.body.mass * GRAVITY * 100
                    if dragging[4]:
                        sball5.body.force = 0, -sball5.body.mass * GRAVITY * 100
                    if dragging[5]:
                        Bball1.body.force = 0, -Bball1.body.mass * GRAVITY * 100
                    if dragging[6]:
                        Bball2.body.force = 0, -Bball2.body.mass * GRAVITY * 100
                    if dragging[7]:
                        Bball3.body.force = 0, -Bball3.body.mass * GRAVITY * 100
                    if dragging[8]:
                        Bball4.body.force = 0, -Bball4.body.mass * GRAVITY * 100
                    if dragging[9]:
                        Bball5.body.force = 0, -Bball5.body.mass * GRAVITY * 100
                    space.gravity = original_gravity
                    dragging = [False] * 10
        # Handle dragging independently for each ball
        if dragging[0]:
            pos = pygame.mouse.get_pos()
            sball1.body.position = pos
            sball1.body.velocity = 0, 0
        if dragging[1]:
            pos2 = pygame.mouse.get_pos()
            sball2.body.position = pos2
            sball2.body.velocity = 0, 0
        if dragging[2]:
            pos3 = pygame.mouse.get_pos()
            sball3.body.position = pos3
            sball3.body.velocity = 0, 0
        if dragging[3]:
            pos4 = pygame.mouse.get_pos()
            sball4.body.position = pos4
            sball4.body.velocity = 0, 0
        if dragging[4]:
            pos5 = pygame.mouse.get_pos()
            sball5.body.position = pos5
            sball5.body.velocity = 0, 0
        if dragging[5]:
            pos6 = pygame.mouse.get_pos()
            Bball1.body.position = pos6
            Bball1.body.velocity = 0, 0
        if dragging[6]:
            pos7 = pygame.mouse.get_pos()
            Bball2.body.position = pos7
            Bball2.body.velocity = 0, 0
        if dragging[7]:
            pos8 = pygame.mouse.get_pos()
            Bball3.body.position = pos8
            Bball3.body.velocity = 0, 0
        if dragging[8]:
            pos9 = pygame.mouse.get_pos()
            Bball4.body.position = pos9
            Bball4.body.velocity = 0, 0
        if dragging[9]:
            pos10 = pygame.mouse.get_pos()
            Bball5.body.position = pos10
            Bball5.body.velocity = 0, 0


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