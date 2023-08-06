from main import *
import pygame, math

# Collision will be based on previous movement!

running = True
pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("SUCC")
pygame.key.set_repeat(1)
FPSCAP=30
delayFPS=1000/FPSCAP

class ManagerForRealBoxes:
    #private
    allRealBoxes=[]

    #public
    def __init__(self):
        pass
    def addRealBox(self, newRealBox):
        self.allRealBoxes.append(newRealBox)
    def drawAllRealBoxes(self, window):
        for box in self.allRealBoxes:
            box.draw(window)
    def checkAllForCollision(self, box):
        for otherBox in self.allRealBoxes:
                if box != otherBox:
                    shortestT, diagonal = box.checkForCollision(otherBox)
                    if shortestT!=1.0 and diagonal:
                        return True
        return False
    def updateAllBoxesMovements(self):
        for box in self.allRealBoxes:
            box.updateCurrentMovement()
            if self.checkAllForCollision(box):
                print("SecondCheck")
                self.checkAllForCollision(box)
                print("---------------")
            box.updatePosition()

class RealBox:
    #variables
    EdgeLines=None
    AbsoluteEdgeLines=None
    pos=None
    boxSize=None
    rectBuffer = None
    movementDirection = None
    TemporarySpeedScaler = 500/FPSCAP
    color = None
    currentMovement=None
    collisionOffset=0.01

    #public
    def __init__(self, AbsolutePosition, boxSize, color=(255,0,0)):
        self.pos = AbsolutePosition
        self.boxSize = boxSize
        self.movementDirection = [0,0]
        self.color = color
        self.constructArrayOfEdgeLinesRelative()
        self.constructArrayOfEdgeLinesAbsolute()
        self.currentMovement = [0,0,0,0]
    def moveMulti(self, dir):
        self.movementDirection = dir
    def moveHorizontal(self, dir):
        self.movementDirection[0]=dir
    def moveVertical(self, dir):
        self.movementDirection[1]=dir

    def updateCurrentMovement(self):
        self.currentMovement[0] = self.movementDirection[0]*self.TemporarySpeedScaler
        self.currentMovement[1] = self.movementDirection[1]*self.TemporarySpeedScaler

    def updatePosition(self):
        self.pos[0] += self.currentMovement[0]
        self.pos[1] += self.currentMovement[1]

    def updateXPosition(self):
        self.pos[0] += self.currentMovement[0]
    def updateYPosition(self):
        self.pos[1] += self.currentMovement[1]

    def draw(self, window):
        self.rectBuffer = pygame.Rect(self.pos[0], self.pos[1], self.boxSize[0], self.boxSize[1])
        #pygame.draw.rect(window, self.color, self.rectBuffer, 2)

    def isMovingLeft(self):
        if self.movementDirection[0] < 0:
            return True
        return False
    def isMovingRight(self):
        if self.movementDirection[0] > 0:
            return True
        return False
    def isMovingUp(self):
        if self.movementDirection[1] < 0:
            return True
        return False
    def isMovingDown(self):
        if self.movementDirection[1] > 0:
            return True
        return False

    #private
    def constructArrayOfEdgeLinesRelative(self):
        edgeLine1 = [[0, 0],                [self.boxSize[0], 0]]
        edgeLine2 = [[0, 0],                [0, self.boxSize[1]]]
        edgeLine3 = [[self.boxSize[0], 0],  [self.boxSize[0], self.boxSize[1]]]
        edgeLine4 = [[0, self.boxSize[1]],  [self.boxSize[0], self.boxSize[1]]]
        self.EdgeLines = [edgeLine1, edgeLine2, edgeLine3, edgeLine4]

    def constructArrayOfEdgeLinesAbsolute(self):
        edgeLine1 = [[self.pos[0],self.pos[1]],                        [self.boxSize[0]+self.pos[0], self.pos[1]]]
        edgeLine2 = [[self.pos[0],self.pos[1]],                        [self.pos[0], self.boxSize[1]+self.pos[1]]]
        edgeLine3 = [[self.boxSize[0]+self.pos[0], self.boxSize[1]+self.pos[1]],     [self.boxSize[0]+self.pos[0], self.pos[1]]]
        edgeLine4 = [[self.boxSize[0]+self.pos[0], self.boxSize[1]+self.pos[1]],    [self.pos[0], self.boxSize[1]+self.pos[1]]]
        self.AbsoluteEdgeLines = [edgeLine1, edgeLine2, edgeLine3, edgeLine4]

    def ApplyMiddleMovement_HitAVerticalWall(self, shiftedShortestT):
        self.currentMovement[0]*=shiftedShortestT
        self.updateXPosition()
        self.currentMovement[0]=0
        self.pos[1]+=self.currentMovement[1]*shiftedShortestT

    def ApplyMiddleMovement_HitAHorizontalWall(self, shiftedShortestT):
        self.currentMovement[1]*=shiftedShortestT
        self.updateYPosition()
        self.currentMovement[1]=0
        self.pos[0]+=self.currentMovement[0]*shiftedShortestT

    def checkForCollision(self, target, prevShortestT=1.0):
        absoluteCurrentMovement = [self.currentMovement[0]+ self.pos[0], self.currentMovement[1]+self.pos[1]]
        movementPathLine1 = [[self.pos[0],self.pos[1]],                                        [absoluteCurrentMovement[0], absoluteCurrentMovement[1]]]
        movementPathLine2 = [[self.boxSize[0]+self.pos[0], self.pos[1]],                       [absoluteCurrentMovement[0]+self.boxSize[0], absoluteCurrentMovement[1]]]
        movementPathLine3 = [[self.pos[0], self.boxSize[1]+self.pos[1]],                       [absoluteCurrentMovement[0], absoluteCurrentMovement[1]+ self.boxSize[1]]]
        movementPathLine4 = [[self.boxSize[0]+self.pos[0], self.boxSize[1]+self.pos[1]],       [absoluteCurrentMovement[0]+self.boxSize[0], self.boxSize[1]+absoluteCurrentMovement[1]]]
        

        Lines = [movementPathLine1, movementPathLine2, movementPathLine3, movementPathLine4]
        target.constructArrayOfEdgeLinesAbsolute()

        shortestT = prevShortestT
        nearestEdge = []
        for line in Lines:
            for edge in target.AbsoluteEdgeLines:
                pygame.draw.line(screen, (255,255,255), line[0], line[1])
                pygame.draw.line(screen, (255,255,255), edge[0], edge[1])
                isIntersecting, intersectionPnt, t = intersectionVecReturnsT(line, edge)
                if isIntersecting:
                    if t < shortestT:
                        shortestT = t
                        nearestEdge=edge
        if shortestT < 1.0: 
            if self.movementDirection[0]==0 or self.movementDirection[1]==0:
                shiftedShortestT=shortestT-self.collisionOffset
                self.currentMovement[0]*=shiftedShortestT
                self.currentMovement[1]*=shiftedShortestT
                print("FullStop!")
                return shiftedShortestT, False
            else:
                nEdgeRelativePntA = [nearestEdge[0][0]-target.pos[0], nearestEdge[0][1]-target.pos[1]]
                nEdgeRelativePntB = [nearestEdge[1][0]-target.pos[0], nearestEdge[1][1]-target.pos[1]]
                shiftedShortestT=shortestT-self.collisionOffset
                if nEdgeRelativePntA[0]==0:
                    if nEdgeRelativePntB[0]!=0:
                        self.ApplyMiddleMovement_HitAHorizontalWall(shiftedShortestT)
                    else:
                        self.ApplyMiddleMovement_HitAVerticalWall(shiftedShortestT)
                else:
                    if nEdgeRelativePntB[0]!=0:
                        self.ApplyMiddleMovement_HitAVerticalWall(shiftedShortestT)
                    else:
                        self.ApplyMiddleMovement_HitAHorizontalWall(shiftedShortestT)
                print("DiagonalStop")
                return shiftedShortestT, True
        return shortestT, False


        


mainBoxManager = ManagerForRealBoxes()
PrimaryBox = RealBox([0, 0], (50, 50), (100, 100, 0))
SecondaryBox = RealBox([380, 380], (100, 100))
ThirdBox = RealBox([500, 500], (50, 50))

mainBoxManager.addRealBox(SecondaryBox)
mainBoxManager.addRealBox(ThirdBox)
mainBoxManager.addRealBox(PrimaryBox)

while running:
    currentTicks = pygame.time.get_ticks()

    xMouse, yMouse = get_pos()

    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.MOUSEBUTTONUP:
            pass
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                PrimaryBox.moveVertical(-1)
            if event.key == pygame.K_s:
                PrimaryBox.moveVertical(1)
            if event.key == pygame.K_a:
                PrimaryBox.moveHorizontal(-1)
            if event.key == pygame.K_d:
                PrimaryBox.moveHorizontal(1)

            # Third box
            if event.key == pygame.K_UP:
                ThirdBox.moveVertical(-1)
            if event.key == pygame.K_DOWN:
                ThirdBox.moveVertical(1)
            if event.key == pygame.K_LEFT:
                ThirdBox.moveHorizontal(-1)
            if event.key == pygame.K_RIGHT:
                ThirdBox.moveHorizontal(1)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                print("peepeepoopoo")
            if event.key == pygame.K_w:
                if PrimaryBox.isMovingUp():
                    PrimaryBox.moveVertical(0)
            if event.key == pygame.K_s:
                if PrimaryBox.isMovingDown():
                    PrimaryBox.moveVertical(0)
            if event.key == pygame.K_a:
                if PrimaryBox.isMovingLeft():
                    PrimaryBox.moveHorizontal(0)
            if event.key == pygame.K_d:
                if PrimaryBox.isMovingRight():
                    PrimaryBox.moveHorizontal(0)

            # third box
            if event.key == pygame.K_UP:
                if ThirdBox.isMovingUp():
                    ThirdBox.moveVertical(0)
            if event.key == pygame.K_DOWN:
                if ThirdBox.isMovingDown():
                    ThirdBox.moveVertical(0)
            if event.key == pygame.K_LEFT:
                if ThirdBox.isMovingLeft():
                    ThirdBox.moveHorizontal(0)
            if event.key == pygame.K_RIGHT:
                if ThirdBox.isMovingRight():
                    ThirdBox.moveHorizontal(0)
        if event.type == pygame.QUIT:
            running = False

    mainBoxManager.updateAllBoxesMovements()
    mainBoxManager.drawAllRealBoxes(screen)

    pygame.display.update()
    screen.fill(0)
    endTicks = pygame.time.get_ticks()
    timeElapsed = endTicks-currentTicks
    if(timeElapsed < delayFPS):
        pygame.time.delay(int(delayFPS-timeElapsed)) 