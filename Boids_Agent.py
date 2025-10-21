import random
import math

class Boid:
    def __init__(self, pos):
        self.pos = pos
        self.vel = (random.uniform(-2, 2), random.uniform(-2, 2)) #Velocity
        self.acc = (0, 0) #Acceleration
        self.mass = random.randint(5, 10) #Boid's mass
        self.max_force = 6
        
    def limit_vector(v, max_value):
        mag = math.sqrt(v[0]**2 + v[1]**2)
        if mag > max_value and mag != 0:
            return (v[0] / mag * max_value, v[1] / mag * max_value)
        return v
    
    def update(self):
        self.vel = (self.vel[0]+self.acc[0], self.vel[1]+self.acc[1])
        self.vel = limit_vector(self.vel, 5)
        self.pos = (self.pos[0]+self.vel[0], self.pos[1]+self.vel[1])
        self.acc = (0, 0)

        # wrap around screen
        x, y = self.pos
        if x < 0: x = WIDTH
        elif x > WIDTH: x = 0
        if y < 0: y = HEIGHT
        elif y > HEIGHT: y = 0
        self.pos = (x, y)
        
    def apply_force(self, f):
        temp = (f[0]/self.mass, f[1]/self.mass) if self.mass != 0 else (f[0], f[1])
        self.acc = (self.acc[0]+temp[0], self.acc[1]+temp[1])

    def avoid(self, boids):
        count = 0
        loc_sum = (0, 0)
        for other in boids:
            d = math.sqrt((self.pos[0]-other.pos[0])**2 + (self.pos[1]-other.pos[1])**2)
            if 0 < d < self.mass + 20:
                loc_sum = (loc_sum[0]+other.pos[0], loc_sum[1]+other.pos[1])
                count += 1
        if count > 0:
            loc_sum = (loc_sum[0]/count, loc_sum[1]/count) if count != 0 else (loc_sum[0], loc_sum[1])
            avoid_vec = (self.pos[0]-loc_sum[0], self.pos[1]-loc_sum[1])
            avoid_vec = self.limit_vector(avoid_vec, self.max_force * 2.5)
            self.apply_force(avoid_vec)

    def approach(self, boids):
        count = 0
        loc_sum = (0, 0)
        for other in boids:
            d = math.sqrt((self.pos[0]-other.pos[0])**2 + (self.pos[1]-other.pos[1])**2)
            if 0 < d < self.mass + 60:
                loc_sum = (loc_sum[0]+other.pos[0], loc_sum[1]+other.pos[1])
                count += 1
        if count > 0:
            loc_sum = (loc_sum[0]/count, loc_sum[1]/count) if count != 0 else (loc_sum[0], loc_sum[1])
            approach_vec = (loc_sum[0]-self.pos[0], loc_sum[1]-self.pos[1])
            approach_vec = self.limit_vector(approach_vec, self.max_force)
            self.apply_force(approach_vec)

    def align(self, boids):
        count = 0
        vel_sum = (0, 0)
        for other in boids:
            d = math.sqrt((self.pos[0]-other.pos[0])**2 + (self.pos[1]-other.pos[1])**2)
            if 0 < d < self.mass + 100:
                vel_sum = (vel_sum[0]+other.vel[0], vel_sum[1]+other.vel[1])
                count += 1
        if count > 0:
            vel_sum = (vel_sum[0]/count, vel_sum[1]/count) if count != 0 else (vel_sum[0], vel_sum[1])
            align_vec = self.limit_vector(vel_sum, self.max_force)
            self.apply_force(align_vec)

    def repel(self, point, radius):
        future_pos = (self.pos[0]+self.vel[0], self.pos[1]+self.vel[1])
        d = math.sqrt((point[0]-future_pos[0])**2 + (point[1]-future_pos[1])**2)
        if d <= radius and d != 0:
            repel_vec = (self.pos[0]-point[0], self.pos[1]-point[1])
            repel_vec = self.limit_vector(repel_vec, self.max_force * 7)
            self.apply_force(repel_vec)

    def flock(self, boids):
        self.avoid(boids)
        self.approach(boids)
        self.align(boids)

    def draw(self, screen):
        if show_circles:
            pygame.draw.circle(screen, BOID_COLOR, (int(self.pos[0]), int(self.pos[1])), self.mass, 1)
        if show_arrows:
            end = (self.pos[0] + self.vel[0]*3, self.pos[1] + self.vel[1]*3)
            pygame.draw.line(screen, BOID_COLOR, self.pos, end, 1)
