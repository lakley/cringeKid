# x1+t(x2-x1)=x3+(x4-x3)u
# y1+t(y2-y1)=y3+(y4-y3)u
#
#      (x4-x3)(y1-y3)-(y4-y3)(x1-x3)    = top
# t = -------------------------------
#      (y4-y3)(x2-x1)-(x4-x3)(y2-y1)    = bot
#

import pygame, math

x1 = 256
x2 = 450
x3 = 120
x4 = 70

y1 = 16
y2 = 450
y3 = 50
y4 = 450

# Lines
L1 = [[x1, y1],[x2, y2]]
L2 = [[x3, y3],[x4, y4]]

ObstacleLines = [L1, L2]

def get_pos():
    pos = pygame.mouse.get_pos()
    return (pos)

def draw_circle():
    pos=get_pos()
    pygame.draw.circle(screen, (255, 0 ,0), pos, 20)

def construct_star(amount_of_spikes, StarSpikeLengthscaler=100):

    # buffer coords
    x=1
    y=0

    lines = [[x*StarSpikeLengthscaler,y*StarSpikeLengthscaler]]
    if int(amount_of_spikes) >=1 and type(amount_of_spikes) == int:
        angle = 6.28/amount_of_spikes

    for i in range(amount_of_spikes-1):
        a = (i+1)*angle
        lines.append([math.cos(a)*StarSpikeLengthscaler,math.sin(a)*StarSpikeLengthscaler])
    return lines

def draw_starlines(mouse_pos, lines):
    for line in lines:
        pygame.draw.line(
            screen, (0,150, 100), 
            (mouse_pos[0], mouse_pos[1]), 
            (mouse_pos[0]+(line[0]), mouse_pos[1]+(line[1]))
             )

starLines = construct_star(10)

def intersectionVec(L1, L2):
    x1 = L1[0][0] 
    x2 = L1[1][0]
    x3 = L2[0][0] 
    x4 = L2[1][0]
    y1 = L1[0][1]
    y2 = L1[1][1]
    y3 = L2[0][1]
    y4 = L2[1][1]
    t = 0
    u = 0

    top = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3))

    top2  = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3))

    bot =((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))


    if bot!=0 :
        t = top/bot
        u = top2/bot
        if t < 0 or t > 1 or u < 0 or u > 1:
          return False, (0, 0)
        
        return True, (x1+t*(x2-x1), y1+t*(y2-y1))
    
    return False, (0, 0)

def intersectionVecReturnsT(L1, L2):
    x1 = L1[0][0] 
    x2 = L1[1][0]
    x3 = L2[0][0] 
    x4 = L2[1][0]
    y1 = L1[0][1]
    y2 = L1[1][1]
    y3 = L2[0][1]
    y4 = L2[1][1]
    t = 0
    u = 0

    top = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3))

    top2  = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3))

    bot =((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))


    if bot!=0 :
        t = top/bot
        u = top2/bot
        if t < 0 or t > 1 or u < 0 or u > 1:
          return False, (0, 0), t
        return True, (x1+t*(x2-x1), y1+t*(y2-y1)), t
    
    return False, (0, 0), t
    
def Collision_Check(mousePos, lines1, lines2): # specific for starlines
    for line1 in lines1:
        for line2 in lines2:
            collision, pnt = intersectionVec([mousePos, [line1[0]+mousePos[0], line1[1]+mousePos[1]]], line2)
            if collision:
                pygame.draw.circle(screen, (150,100,0), pnt, 5)

delayFPS=1000/10



def main():

    running = True
    global screen
    pygame.init()
    screen = pygame.display.set_mode((700, 600))
    pygame.display.set_caption("SUCC")
    
    
    while running:
        currentTicks = pygame.time.get_ticks()
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                draw_circle()
                pygame.display.update()

            if event.type == pygame.QUIT:
                running = False
            
        xMouse, yMouse = get_pos()
        pygame.draw.line(screen, (255,255, 0), L1[0], L1[1])
        pygame.draw.line(screen, (255,255, 0), L2[0], L2[1])
        draw_starlines([xMouse, yMouse], starLines)
        Collision_Check([xMouse, yMouse], starLines, ObstacleLines)
        pygame.display.update()
        screen.fill(0)

        endTicks = pygame.time.get_ticks()
        timeElapsed = endTicks-currentTicks
        if(timeElapsed < delayFPS):
            pygame.time.delay(int(delayFPS-timeElapsed)) 


#main()

print("end")





""""
def intersection(x1, x2, x3, x4, y1, y2, y3, y4):
    t = 0
    u = 0
    top = (x4-x3)*(y1-y3)-(y4-y3)*(x1-x3)
    top2  = (y3-y1)*(x1-x2)-(x3-x1)*(y1-y2)
    bot = (y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)
    if bot!=0 :
        t = top/bot
        u = top2/bot
        if t < 0 or t > 1 or u < 0 or u > 1:
          return False, (x1+t*(x2-x1), y1+t*(y2-y1))
        return True, (x1+t*(x2-x1), y1+t*(y2-y1))
    return False, (0, 0)

def intersectionVecVersion2(L1, L2):
    x1 = L1[0][0] 
    x2 = L1[1][0]
    x3 = L2[0][0] 
    x4 = L2[1][0]
    y1 = L1[0][1]
    y2 = L1[1][1]
    y3 = L2[0][1]
    y4 = L2[1][1]
    t = 0
    u = 0
    top = (x4-x3)*(y1-y3)-(y4-y3)*(x1-x3)
    top2  = (y3-y1)*(x1-x2)-(x3-x1)*(y1-y2)
    bot = (y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)
    if bot!=0 :
        t = top/bot
        u = top2/bot
        if t < 0 or t > 1 or u < 0 or u > 1:
          return False, (x1+t*(x2-x1), y1+t*(y2-y1))
        return True, (x1+t*(x2-x1), y1+t*(y2-y1))
    return False, (0, 0)


    x1+t(x2-x1)=x3+u(x4-x3)
    y1+t(y2-y1)=y3+u(y4-y3)

    (x1-x3)+t(x2-x1)=u(x4-x3)
    (y1-y3)(x4-x3)-(y4-y3)(x1-x3)=t(x2-x1)(y4-y3)-t(y2-y1)(x4-x3)
    t= (y1-y3)(x4-x3)-(y4-y3)(x1-x3)
       -----------------------------
        (x2-x1)(y4-y3)-(y2-y1)(x4-x3)

    top = (y1-y3)*(x4-x3)-(y4-y3)*(x1-x3)
    top2  = (y3-y1)*(x1-x2)-(x3-x1)*(y1-y2)
    bot =(x2-x1)(y4-y3)-(y2-y1)(x4-x3)

"""