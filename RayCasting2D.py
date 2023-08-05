from main import *
import pygame
print("Hello world!")


running = True
pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("SUCC")
    
starSpikes = construct_star(100, 1415)

# All walls are lines
wall1=[[10, 100], [100, 10]]
wall2=[[150, 300], [500, 40]]
wall3=[[160, 10], [650, 360]]

theWalls = [wall3, 
            wall2, 
            wall1]

def drawTheWalls():
    for wall in theWalls:
        pygame.draw.line(screen, (255,255, 0), wall[0], wall[1])
    
def addWall(wall):
    theWalls.append(wall)

def drawSpikesWithExternalInfluence(LightPosition):
    for spike in starSpikes:
        currentLine = [LightPosition, [spike[0]+LightPosition[0], spike[1]+LightPosition[1]]]
        finalSpike = currentLine
        for wall in theWalls:
            # Checks currently targeted spike() against currently targeted wall
            isIntersecting, intersectionPnt = intersectionVec(finalSpike, wall)

            if isIntersecting:
                finalSpike[1]=intersectionPnt

        # draw final spike
        pygame.draw.line(screen, (255,255, 0), finalSpike[0], finalSpike[1])

WallBuild_pointIndex = False
FirstPointFromClick = []

while running:
    currentTicks = pygame.time.get_ticks()

    xMouse, yMouse = get_pos()

    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.MOUSEBUTTONUP:
            if not WallBuild_pointIndex:
                FirstPointFromClick = [xMouse, yMouse]
                WallBuild_pointIndex=True
            else:
                addWall([[xMouse, yMouse], FirstPointFromClick])
                WallBuild_pointIndex=False

        if event.type == pygame.QUIT:
            running = False

    drawTheWalls()

    pygame.display.update()
    screen.fill(0)

    drawSpikesWithExternalInfluence([xMouse, yMouse])

    endTicks = pygame.time.get_ticks()
    timeElapsed = endTicks-currentTicks
    if(timeElapsed < delayFPS):
        pygame.time.delay(int(delayFPS-timeElapsed)) 