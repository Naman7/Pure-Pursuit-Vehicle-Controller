import pygame
import math

path=[]
e=100

def distance(x1, y1, x2, y2):
    return math.sqrt((y2-y1)**2 + (x2-x1)**2)

def showPath(screen):
    pygame.draw.circle(screen, (0, 0, 100), [path[0][0], path[0][1]], 5)
    for i in range(len(path)-1):
        pygame.draw.line(screen, (150, 150, 150), [path[i][0], path[i][1]], [path[i+1][0], path[i+1][1]])

def setTarget(vehicle):
    while distance(path[0][0], path[0][1], vehicle.pos[0], vehicle.pos[1]) < e:
        if len(path)==1:
            break
        path.pop(0)

def rect(x, y, w, h, angle):
        return [translate(x, y, -w/2, h/2, angle),
               translate(x, y, w/2, h/2, angle),
               translate(x, y, +w/2, -h/2, angle),
               translate(x, y, -w/2, -h/2, angle)]

def translate(x, y, a, b, theta):
    p = x + (a*math.cos(theta) - b*math.sin(theta))
    q = y + (a*math.sin(theta) + b*math.cos(theta))
    return [p,q]
    
def vecMag(a,b):
    a = math.sqrt(a**2 + b**2)
    if a!=0:
        return a
    else:
        return 1

def orientation(p1, p2, p3):
    val = ((p2[1] - p1[1]) * (p3[0] - p2[0])-
           (p2[0] - p1[0]) * (p3[1] - p2[1]))
    if val > 0:
        return 1
    else:
        return 0
            

class Bicycle():
    def __init__(self, screen):
        self.pos = [80,40]
        self.previous = [79, 40]
        self.theta = 0
        self.vel = 0
        self.acc = .03
        self.delta = 0
        self.length = 150
        self.screen = screen
        self.kappa = 0
        self.ld = 0
        self.alpha = 0
        
    def update(self):
        if len(path) <= 1 and self.ld < e:
            self.vel = 0
            self.acc = 0
        else:
            self.acc = .03
            
        self.vel += self.acc
        if self.vel > 15 or self.vel < -15:
            self.vel -= self.acc
        if self.delta > 1:
            self.delta = 1
        elif self.delta < -1:
            self.delta = -1
        
        if((self.vel * math.cos(self.theta)) != 0 or (self.vel * math.sin(self.theta)) != 0):
            self.previous[0] = self.pos[0]
            self.previous[1] = self.pos[1]
        
        self.pos[0] += self.vel * math.cos(self.theta)
        self.pos[1] += self.vel * math.sin(self.theta)
        self.theta += (self.vel * math.tan(self.delta)) / self.length
        self.vel *= 0.95
    
    def control(self):
        pygame.draw.line(self.screen, (100, 0, 0), [path[0][0], path[0][1]], [self.pos[0], self.pos[1]])
        self.ld = distance(path[0][0], path[0][1], self.pos[0], self.pos[1])
        self.alpha = math.acos(((self.pos[0] - self.previous[0]) * (path[0][0]-self.pos[0]) + (self.pos[1] - self.previous[1]) * (path[0][1]-self.pos[1]))/
                              (vecMag(self.pos[0] - self.previous[0], self.pos[1] - self.previous[1]) * vecMag(path[0][0] - self.pos[0], path[0][1] - self.pos[1])))
        
        if orientation([self.pos[0], self.pos[1]], [self.pos[0] + self.length*math.cos(self.theta), self.pos[1] + self.length*math.sin(self.theta)], path[0]):
                       self.alpha = -1*self.alpha
        
        if math.atan2(2*math.sin(self.alpha)*self.length, self.ld) - self.delta > 0.05:
           self.delta += 0.05
        elif self.delta - math.atan2(2*math.sin(self.alpha)*self.length, self.ld) > 0.05:
           self.delta -= 0.05
    
    def display(self):
        x=int(self.pos[0])
        y=int(self.pos[1])
        z=self.length
        pygame.draw.polygon(self.screen, (139, 69, 19), rect(x + z/2*math.cos(self.theta), y + z/2*math.sin(self.theta), z, 5, self.theta))
        pygame.draw.polygon(self.screen, (105, 105, 105), rect(x, y, 30, 15, self.theta))
        pygame.draw.polygon(self.screen, (105, 105, 105), rect(x + z*math.cos(self.theta), y + z*math.sin(self.theta), 30, 15, self.theta + self.delta))
               
def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    done = False
    vehicle = Bicycle(screen)
    while not done:
        screen.fill((0,0,0))
        if pygame.mouse.get_pressed()[0]:
            (Mx, My) = pygame.mouse.get_pos()
            if not len(path):
                path.append((Mx, My))
            if not path[-1][0] == Mx and not path[-1][1] == My:
                path.append((Mx, My))
                
        if len(path):
            showPath(screen)
            setTarget(vehicle)
            vehicle.control()
    
        vehicle.update()
        vehicle.display()
        pygame.display.flip()
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
    pygame.quit()
        
if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
          