from math import sqrt

DEFAULT_SPEED = 4

class Agent(object):

    def __init__(self,pos = (1,1), vel=(DEFAULT_SPEED,0)):
        self.pos = (pos[0],pos[1])
        self.vel = vel

    def distance_from(self,other_agent):
        return sqrt((other_agent.pos[0] - self.pos[0])**2 + (other_agent.pos[1] - self.pos[1]) **2)

    def update_pos(self):
        self.pos = self.pos[0] + self.vel[0], self.pos[1] + self.vel[1]
