import pygame
import pymunk
import pymunk.pygame_util
import math
import random

pygame.init()

WIDTH, HEIGHT = 1200, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
gravity = 0.5
bounce_stop = 0.3
wall_thickness = 10
mouse_trajectory = [] # ตำแหน่งของเมาส์
background = pygame.image.load("backgroud_for_display.png")
file = open('log.txt', 'w')
file = open('log.txt', 'a')
file.write('start simulation\n')

          
class Ball:
    def __init__(self, space, radius, mass, color, text_color=(0, 0, 0,255), x_pos=300, y_pos=300,GRAVITY = 9.81, AIR_RESISTANCE = 0.01, FRICTION = 0.5, ELASTICITY = 0.8):
        
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
        self.circle.elasticity = 0.8  # Bounciness
        self.circle.friction = 0.5  # Surface friction
        space.add(self.body, self.circle)


    def draw_text(self, surface, text):
        text_object = self.font.render(str(text), True, self.text_color)
        text_rect = text_object.get_rect(center=self.body.position)
        surface.blit(text_object, text_rect)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.body.position, self.radius)
        self.draw_text(surface, self.body.mass)
        
    def check_gravity(self, x_push, y_push): # ตรวจสอบแรงโน้มถ่วง
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
    # Add background image
    window.blit(background, (0, 0))
    space.debug_draw(draw_option)

def create_scale_base(space, width, height):
    GOLD = (255, 215, 0, 0)

    # Rectangle (base)
    rects = [
        [(500, height - 135), (20, 565), GOLD, 100]
    ]
    for pos, size, color, mass in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)  # Make body static
        body.position = pos
        shape = pymunk.Poly.create_box(body, size, radius=2)
        shape.color = color
        shape.mass = mass
        shape.sensor = False # Disable collision
        space.add(body, shape)

    return space


def create_scale_body(space):
    global limit_joint
    scg = 1

    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = (500, 350)

    body = pymunk.Body(body_type=pymunk.Body.DYNAMIC) # Make body dynamic (affected by gravity)
    body.position = (500, 350)
    body.angle = math.radians(0)
    rect = pymunk.Poly.create_box(body, (500, 10))  
    rect.friction = 1
    rect.mass = scg
    

    s2 = pymunk.Segment(body, (-250, 120), (-250, 0), 4)
    s3 = pymunk.Segment(body, (-250, 120), (-200, 200), 4)
    s4 = pymunk.Segment(body, (-200, 200), (-200, 350), 4)
    s5 = pymunk.Segment(body, (-200, 350), (-300, 350), 4)
    s6 = pymunk.Segment(body, (-300, 350), (-300, 200), 4)
    s7 = pymunk.Segment(body, (-300, 200), (-250, 120), 4)
    s6.color = (255, 0, 0, 255)
    s5.color = (255, 0, 0, 255)
    s4.color = (255, 0, 0, 255)
    
    
    
   
    circle = pymunk.Circle(body, 30, (0, 0))
    s11 = pymunk.Segment(body, (250, 120), (250, 0), 4)
    s12 = pymunk.Segment(body, (250, 120), (200, 200), 4)
    s13 = pymunk.Segment(body, (200, 200), (200, 350), 4)
    s14 = pymunk.Segment(body, (200, 350), (300, 350), 4)
    s15 = pymunk.Segment(body, (300, 350), (300, 200), 4)
    s16 = pymunk.Segment(body, (300, 200), (250, 120), 4)
    s15.color = (0, 255, 0, 255)
    s14.color = (0, 255, 0, 255)
    s13.color = (0, 255, 0, 255)
    
    pivot_joint = pymunk.PivotJoint(rotation_center_body, body, (500, 350)) # Create pivot joint to keep the body in place
    space.add(pivot_joint)
    # Add a rotary limit joint to limit rotation to 10 degrees
    limit_joint = pymunk.RotaryLimitJoint(rotation_center_body, body, -math.radians(10), math.radians(10))
    space.add(limit_joint)
    
    space.add(body, rect)
    space.add(s2, s3, s11,circle,s4,s5,s6,s7,s12,s13,s14,s15,s16)



  
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
        body = pymunk.Body(body_type=pymunk.Body.STATIC) # Make body static (not affected by gravity)
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
    dt = 1 / fps # Time step
    

    handler = space.add_collision_handler(1, 2)
    handler.begin = lambda a, b, arbiter, space: False # Disable collision between balls
    space = pymunk.Space()
    space.gravity = (0, GRAVITY * 100)
    draw_options = pymunk.pygame_util.DrawOptions(window)

    #Explain the weight of each ball
    #sball1 = Ball(space, 15, 0.5/2, (0, 0, 0,255),200,100) #black  # Adjusted mass to 0.5 kg
    #sball2 = Ball(space, 15, 1/2, (0, 0, 255,255),200,100) #blue  # Adjusted mass to 1kg
    #sball3 = Ball(space, 15, 1.5/2, (0, 255, 255,255),200,100) #cyan  # Adjusted mass to 1.5kg
    #sball4 = Ball(space, 15, 2/2, (255, 215, 0,255),200,100) #gold   # Adjusted mass to 2kg
    #sball5 = Ball(space, 15, 2.5/2, (190, 190, 190,255),200,100)#gray   # Adjusted mass to 2.5kg

    Rightside_weight = [] # สร้าง list ของน้ำหนักของลูกบอลที่อยู่ทางขวา
    Rball_params = [
    (30, 3, (0, 255, 0, 255), 300, 1000),  # green mass 3kg
    (30, 5, (255, 165, 0, 255), 300, 1000),  # orange mass 5kg
    (30, 7, (160, 32, 240, 255), 300, 1000),  # purple mass 7kg
    (30, 11, (255, 0, 0, 255), 300, 1000),  # red mass 11kg
    (30, 18, (255, 255, 0, 255), 300, 1000)  # yellow mass 18kg
    ]
    #สุ่มลูกบอลซ้ำลูกที่เหลือ  
    Rparams = random.choice(Rball_params)
    Bball = Ball(space, *Rparams)
    Rightside_weight.append(Bball)
    if Rball_params == [0]:
        weight_Bball = 3 # Adjusted mass to 3 kg
        Rightside_weight.append(weight_Bball)
    elif Rball_params == [1]:
        weight_Bball = 5  # Adjusted mass to 5 kg
        Rightside_weight.append(weight_Bball)
    elif Rball_params == [2]:
        weight_Bball = 7 # Adjusted mass to 7 kg
        Rightside_weight.append(weight_Bball)  
    elif Rball_params == [3]:
        weight_Bball = 11 # Adjusted mass to 11 kg
        Rightside_weight.append(weight_Bball)
    elif Rball_params == [4]:
        weight_Bball = 18 # Adjusted mass to 18 kg
        Rightside_weight.append(weight_Bball)
    
    file.write('insert Bigball in right side\n')
    
    create_boundaries(space, width, height)
    create_scale_base(space, width, height)
    create_scale_body(space)
    
    
    sball1 = None 
    sball2 = None
    sball3 = None
    sball4 = None
    sball5 = None



    # Separate drag states for each ball
    original_gravity = space.gravity
    Leftside = []
    Leftside_weight = [] # สร้าง list ของน้ำหนักของลูกบอลที่อยู่ทางซ้าย
    dragging_Leftside = [] 
    dragging_Rightside = False
    weight_Bball = None

    while run:

        
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:  # New event check for key press
                if event.key == pygame.K_1:  # If '1' key is pressed
                    sball1 = Ball(space, 15, 0.5/2, (0, 0, 0,255),200,100)  # Spawn sball1
                    weight_sball1 = 0.5 # Adjusted mass to 0.5 kg
                    Leftside.append(sball1)
                    Leftside_weight.append(weight_sball1)
                    dragging_Leftside.append(False)
                    file.write('insert 0.5kg smallball in left side\n')
                elif event.key == pygame.K_2:  # If '2' key is pressed
                    sball2 = Ball(space, 15, 1/2, (0, 0, 255,255),200,100)  # Spawn sball2
                    weight_sball2 = 1 # Adjusted mass to 1kg
                    Leftside.append(sball2)
                    Leftside_weight.append(weight_sball2)
                    dragging_Leftside.append(False)
                    file.write('insert 1kg smallball in left side\n')
                elif event.key == pygame.K_3:  # If '3' key is pressed
                    sball3 = Ball(space, 15, 1.5/2, (0, 255, 255,255),200,100)  # Spawn sball3
                    weight_sball3 = 1.5 # Adjusted mass to 1.5kg
                    Leftside.append(sball3)
                    Leftside_weight.append(weight_sball3)
                    dragging_Leftside.append(False)
                    file.write('insert 1.5kg smallball in left side\n')
                elif event.key == pygame.K_4:  # If '4' key is pressed
                    sball4 = Ball(space, 15, 2/2, (255, 215, 0,255),200,100)  # Spawn sball4
                    weight_sball4 = 2 # Adjusted mass to 2kg
                    Leftside.append(sball4)
                    Leftside_weight.append(weight_sball4)
                    dragging_Leftside.append(False)
                    file.write('insert 2kg smallball in left side\n')
                elif event.key == pygame.K_5:  # If '5' key is pressed
                    sball5 = Ball(space, 15, 2.5/2, (190, 190, 190,255),200,100)  # Spawn sball5
                    weight_sball5 = 2.5 # Adjusted mass to 2.5kg
                    Leftside.append(sball5)
                    Leftside_weight.append(weight_sball5)
                    dragging_Leftside.append(False)
                    file.write('insert 2.5kg smallball in left side\n')
                elif event.key == pygame.K_r: # If 'r' key is pressed
                    for ball in Leftside:
                        if ball.body in space.bodies:  # Check if the body is in the space
                            space.remove(ball.body, ball.circle)
                            
                    Leftside_weight.clear()  # Clear the list
                    if Bball.body in space.bodies:  # Check if the body is in the space
                        space.remove(Bball.body, Bball.circle)
                    Rightside_weight.clear()
                    Rparamss = random.choice(Rball_params)
                    Bball = Ball(space, *Rparamss)
                    if Rball_params == [0]:
                        weight_Bball = 3 # Adjusted mass to 3 kg
                        Rightside_weight.append(weight_Bball)
                    elif Rball_params == [1]:
                        weight_Bball = 5  # Adjusted mass to 5 kg
                        Rightside_weight.append(weight_Bball)
                    elif Rball_params == [2]:
                        weight_Bball = 7 # Adjusted mass to 7 kg
                        Rightside_weight.append(weight_Bball)
                    elif Rball_params == [3]:
                        weight_Bball = 11 # Adjusted mass to 11 kg
                        Rightside_weight.append(weight_Bball)
                    elif Rball_params == [4]:
                        weight_Bball = 18 # Adjusted mass to 18 kg
                        Rightside_weight.append(weight_Bball)
                    Rightside_weight.append(Bball)
                    file.write('insert Bigball in right side\n')
                    file.write('reset simulation\n')
                    file.write('----------------------------------------\n')
    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        pos = pygame.mouse.get_pos()
                    if Bball is not None and is_point_in_circle(pos, Bball):
                        dragging_Rightside = True
                        Bball.body.force = 0, 0
                        space.gravity = 0, 981
                    for i, ball in enumerate(Leftside):
                        if ball is not None and is_point_in_circle(pos, ball):
                            dragging_Leftside[i] = True
                            ball.body.force = 0, 0
                            space.gravity = 0, 981
        
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    if dragging_Rightside:
                        Bball.body.force = 0, -Bball.body.mass * GRAVITY * 100
                        dragging_Rightside = False
                    for i, ball in enumerate(Leftside):
                        if dragging_Leftside[i]:
                            ball.body.force = 0, -ball.body.mass * GRAVITY * 100
                            dragging_Leftside[i] = False
                    space.gravity = original_gravity
    
        # Handle dragging independently for each ball
        if dragging_Rightside:
            pos = pygame.mouse.get_pos()
            Bball.body.position = pos
            Bball.body.velocity = 0, 0
        for i, ball in enumerate(Leftside):#make loop for each ball
            if dragging_Leftside[i]:
                pos = pygame.mouse.get_pos()
                ball.body.position = pos
                ball.body.velocity = 0, 0
        
        left_weight = sum(Leftside_weight)
        right_weight = sum(ball.mass for ball in Rightside_weight)
        weight_difference = right_weight - left_weight
        

        font = pygame.font.SysFont(None, 36, bold = True)
        left_text = font.render("Left Weight: {:.2f} kg".format(left_weight), True, (255, 0, 0))
        right_text = font.render("Right Weight: {:.2f} kg".format(right_weight), True, (0, 128, 0))
        middle_text = font.render("Weight Difference: {:.2f} kg".format(abs(weight_difference)), True, (128, 0, 128))
        insert_Rball = font.render("please insert Bigball in right side", True, (0, 0, 0))
        insert_sball = font.render("please insert smallball in left side", True, (0, 0, 0))
        
        if weight_difference == 0:
            balance_text = font.render("Balance", True, (0, 128, 0))
        else:
            balance_text = font.render("Unbalance", True, (255, 0, 0))
        if weight_difference == 0:
            limit_joint.max = math.radians(0)
            limit_joint.min = math.radians(0)
        elif weight_difference > 0:
            limit_joint.max = math.radians(10)
            limit_joint.min = math.radians(0)
        elif weight_difference < 0:
            limit_joint.max = math.radians(0)
            limit_joint.min = math.radians(-10)

        window.blit(balance_text, (500, 175))
        window.blit(left_text, (20, 20))
        window.blit(right_text, (width - right_text.get_width() - 20, 20))
        window.blit(middle_text, (width/3, 20))
        window.blit(insert_Rball, (600, 750))
        window.blit(insert_sball, (50, 750))

        pygame.display.update()
        clock.tick(fps)
        space.step(dt)
        draw(space, window, draw_options)



    
    pygame.quit()
    file.write('end simulation\n')
    file.write('----------------------------------------\n')
    file.close()



def is_point_in_circle(point, circles): # ตรวจสอบว่าจุดอยู่ในวงกลมหรือไม่ #check cirle
    if not isinstance(circles, list):
        circles = [circles]

    for circle in circles:
        dx = point[0] - circle.body.position.x
        dy = point[1] - circle.body.position.y
        distance_squared = dx ** 2 + dy ** 2
        if distance_squared <= circle.radius ** 2:
            return True
    return False

if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)