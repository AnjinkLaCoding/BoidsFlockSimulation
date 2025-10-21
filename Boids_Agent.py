from math import sqrt

DEFAULT_SPEED = 4

class Boids(object):

    #Boids initialization
    def __init__(self,pos = (1,1), vel=(DEFAULT_SPEED,0)):
        self.pos = (pos[0],pos[1])
        self.vel = vel

    #Function to calculate the distance between 2 boids
    def boids_dist(self,other_boids):
        return sqrt((other_boids.pos[0] - self.pos[0])**2 + (other_boids.pos[1] - self.pos[1]) **2)
    
    #Update the position of each boids
    def update_pos(self):
        self.pos = self.pos[0] + self.vel[0], self.pos[1] + self.vel[1]
