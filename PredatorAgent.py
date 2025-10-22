from random import randint
from BoidsAgent import Boid
import math
import pygame
import GlobalVar

class Predator(Boid):
    def __init__(self, pos):
        super().__init__(pos)
        self.mass = randint(8, 15)
        self.max_force = 10

    #Keeps vectors like steering force or velocity from getting too large (Keep their movement in controlled manner)
    def limit_vector(self, v, max_value):
        mag = math.sqrt(v[0]**2 + v[1]**2)
        if mag > max_value and mag != 0:
            return (v[0] / mag * max_value, v[1] / mag * max_value)
        return v

    #Function to seek nearby boids
    def approach(self, boids):
        count = 0
        loc_sum = (0, 0)
        #Check for potential prey
        for other in boids:
            d = math.sqrt((self.pos[0] - other.pos[0])**2 + (self.pos[1] - other.pos[1])**2)
            #If the boids within the range, it's considered a target
            if 0 < d < self.mass + 260:
                loc_sum = (loc_sum[0] + other.pos[0], loc_sum[1] + other.pos[1])
                count += 1
        #If there are potential preys, the predator will chase them
        if count > 0:
            loc_sum = (loc_sum[0]/count, loc_sum[1]/count) if count != 0 else (loc_sum[0], loc_sum[1])
            approach_vec = (loc_sum[0] - self.pos[0], loc_sum[1] - self.pos[1])
            approach_vec = self.limit_vector(approach_vec, self.max_force)
            self.apply_force(approach_vec)

    #Draw it to the display
    def draw(self, screen):
        pygame.draw.circle(screen, GlobalVar.PRED_COLOR, (int(self.pos[0]), int(self.pos[1])), self.mass)
