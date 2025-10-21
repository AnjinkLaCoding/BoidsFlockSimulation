import random
import math

def limit_vector(v, max_value):
    mag = math.sqrt(v[0]**2 + v[1]**2)
    if mag > max_value and mag != 0:
        return (v[0] / mag * max_value, v[1] / mag * max_value)
    return v

class Boid:
    def __init__(self, pos):
        self.pos = pos
        self.vel = (random.uniform(-2, 2), random.uniform(-2, 2))
        self.acc = (0, 0)
        self.mass = random.randint(5, 10)
        self.max_force = 6

    def update(self):
        self.vel = self.vel[0]+self.acc[0], self.vel[1]+self.acc[1]
        self.vel = limit_vector(self.vel, 5)
        self.pos = self.pos[0]+self.vel[0], self.pos[1]+self.vel[1]
        self.acc = (0, 0)

        # wrap around screen
        x, y = self.pos
        if x < 0: x = WIDTH
        elif x > WIDTH: x = 0
        if y < 0: y = HEIGHT
        elif y > HEIGHT: y = 0
        self.pos = (x, y)

    def apply_force(self, f):
        self.acc = add(self.acc, div(f, self.mass))

    def avoid(self, boids):
        count = 0
        loc_sum = (0, 0)
        for other in boids:
            d = dist(self.pos, other.pos)
            if 0 < d < self.mass + 20:
                loc_sum = add(loc_sum, other.pos)
                count += 1
        if count > 0:
            loc_sum = div(loc_sum, count)
            avoid_vec = sub(self.pos, loc_sum)
            avoid_vec = limit_vector(avoid_vec, self.max_force * 2.5)
            self.apply_force(avoid_vec)

    def approach(self, boids):
        count = 0
        loc_sum = (0, 0)
        for other in boids:
            d = dist(self.pos, other.pos)
            if 0 < d < self.mass + 60:
                loc_sum = add(loc_sum, other.pos)
                count += 1
        if count > 0:
            loc_sum = div(loc_sum, count)
            approach_vec = sub(loc_sum, self.pos)
            approach_vec = limit_vector(approach_vec, self.max_force)
            self.apply_force(approach_vec)

    def align(self, boids):
        count = 0
        vel_sum = (0, 0)
        for other in boids:
            d = dist(self.pos, other.pos)
            if 0 < d < self.mass + 100:
                vel_sum = add(vel_sum, other.vel)
                count += 1
        if count > 0:
            vel_sum = div(vel_sum, count)
            align_vec = limit_vector(vel_sum, self.max_force)
            self.apply_force(align_vec)

    def repel(self, point, radius):
        future_pos = add(self.pos, self.vel)
        d = dist(point, future_pos)
        if d <= radius and d != 0:
            repel_vec = sub(self.pos, point)
            repel_vec = limit_vector(repel_vec, self.max_force * 7)
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
