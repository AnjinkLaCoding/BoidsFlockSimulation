from random import randrange
import math
from Boids_Agent import Boids, DEFAULT_SPEED
import GlobalVar
from operator import add, sub

ALIGNMENT_WEIGHT = [10,4]
COHESION_WEIGHT = [5,3]
SEPERATION_WEIGHT = [5,8]
OBSTACLE_DODGE_WEIGHT = 180

ALIGNMENT_RADIUS = 200
COHESION_RADIUS = 170
SEPERATION_RADIUS = 30
OBSTACLE_DODGE_RADIUS = 70

MAX_SPEED = 25
MIN_SPEED = 1


# Additional mathematical functions
def convert_unit_to_vector(vel, desired_v_length = 1):
    x, y = vel
    mag = math.sqrt(x**2 + y**2)
    if mag == 0:
        return 0, 0
    return (x / mag * desired_v_length, y / mag * desired_v_length)

def limit(vel, limit):
    x, y = vel
    mag = math.sqrt(x**2 + y**2)
    if mag > limit:
        return (x / mag * limit, y / mag * limit)
    else:
        return (x, y)

# Compute functions
def compute_alignment(myBoids, t):
    compute_vel = (0,0)
    neighbors_cnt = 0
    for i in range(len(GlobalVar.boids_array)):
        boids = GlobalVar.boids_array[i]
        if boids != myBoids and myBoids.boids_dist(boids) < ALIGNMENT_RADIUS and t == i % 2:
            compute_vel = (compute_vel[0] + boids.vel[0], compute_vel[1] + boids.vel[1])
            neighbors_cnt += 1
    
    if neighbors_cnt == 0:
        return compute_vel
    
    compute_vel = (compute_vel[0] / neighbors_cnt, compute_vel[1] / neighbors_cnt)

    return limit(compute_vel, 0.05)

def compute_cohesion(myBoids, t):
    compute_vel = (0,0)
    neighbors_cnt = 0
    for i in range(len(GlobalVar.boids_array)):
        boids = GlobalVar.boids_array[i]
        if boids != myBoids and myBoids.boids_dist(boids) < COHESION_RADIUS and t == i % 2:
            compute_vel = (boids.pos[0] - myBoids.pos[0], boids.pos[1] + myBoids.pos[1])
            neighbors_cnt += 1
    
    if neighbors_cnt == 0:
        return compute_vel
    
    compute_vel = (compute_vel[0] / neighbors_cnt, compute_vel[1] / neighbors_cnt)

    return limit(compute_vel, 0.05)

def compute_seperation(myBoids, t):
    compute_vel = (0,0)
    neighbors_cnt = 0
    for i in range(len(GlobalVar.boids_array)):
        boids = GlobalVar.boids_array[i]
        if boids != myBoids and myBoids.boids_dist(boids) < SEPERATION_RADIUS and t == i % 2:
            temp_vel = (myBoids.pos[0] - boids.pos[0], myBoids.pos[1] - boids.pos[1])
            temp_vel = convert_unit_to_vector(temp_vel)
            compute_vel = (compute_vel[0] + (temp_vel[0] / myBoids.boids_dist(boids)), compute_vel[1] + (temp_vel[1] / myBoids.boids_dist(boids)))
            neighbors_cnt += 1
    
    if neighbors_cnt == 0:
        return compute_vel
    
    return (compute_vel[0] / neighbors_cnt, compute_vel[1] / neighbors_cnt)

def compute_obstacle_dodge(myBoids):
    compute_vel = (0,0)
    neighbors_cnt = 0
    for obs in GlobalVar.obstacle_array:
        if obs.boids_dist(myBoids) < OBSTACLE_DODGE_RADIUS:
            temp_vel = (myBoids.pos[0] - obs.pos[0], myBoids.pos[1] - obs.pos[1])
            temp_vel = convert_unit_to_vector(temp_vel)
            compute_vel = (compute_vel[0] + (temp_vel[0] / myBoids.boids_dist(obs)), compute_vel[1] + (temp_vel[1] / myBoids.boids_dist(obs)))    
            neighbors_cnt += 1

    if neighbors_cnt == 0:
        return compute_vel

    return (compute_vel[0] / neighbors_cnt, compute_vel[1] / neighbors_cnt)

def check_agent_inbound():
    for boids in GlobalVar.boids_array:
        if boids.pos[0] > GlobalVar.WIDTH:
            boids.pos = (0, boids.pos[1])
        if boids.pos[0] < 0:
            boids.pos = (GlobalVar.WIDTH, boids.pos[1])
        if boids.pos[1] > GlobalVar.HEIGHT:
            boids.pos = (boids.pos[0], 0)
        if boids.pos[1] < 0:
            boids.pos = (boids.pos[0], GlobalVar.HEIGHT)

def agent_update():
    temp_boids_array = []
    for i in range(len(GlobalVar.boids_array)):
        boids = GlobalVar.boids_array[i]
        temp_vel = (0,0)
        cohesion_v = compute_cohesion(boids, i % 2)
        alignment_v = compute_alignment(boids, i % 2)
        seperation_v = compute_seperation(boids, i % 2)
        obstacle_dodge_v = compute_obstacle_dodge(boids)
        v_array = [boids.vel,
                   (cohesion_v[0] * COHESION_WEIGHT[i % 2], cohesion_v[1] * COHESION_WEIGHT[i % 2]),
                   (alignment_v[0] * ALIGNMENT_WEIGHT[i % 2], alignment_v[1] * ALIGNMENT_WEIGHT[i % 2]),
                   (seperation_v[0] * SEPERATION_WEIGHT[i % 2], seperation_v[1] * SEPERATION_WEIGHT[i % 2]),
                   (obstacle_dodge_v[0] * OBSTACLE_DODGE_WEIGHT, obstacle_dodge_v[1] * OBSTACLE_DODGE_WEIGHT)
                    ]
        sum_x, sum_y = 0, 0
        for v in v_array:
            sum_x += v[0]
            sum_y += v[1]
        temp_vel = (sum_x, sum_y)
        temp_vel = (temp_vel[0] * GlobalVar.FPS, temp_vel[1] * GlobalVar.FPS)

        a = Boids(boids.pos, temp_vel)
        if i % 2:
            a.vel = limit(temp_vel, DEFAULT_SPEED + 6 + GlobalVar.speed_adjustment)
        else:
            a.vel = limit(temp_vel, DEFAULT_SPEED + GlobalVar.speed_adjustment)
        a.update_pos()
        temp_boids_array.append(a)

    GlobalVar.boids_array = temp_boids_array

def randomize_position():
    for boids in GlobalVar.boids_array:
        boids.pos = randrange(0, GlobalVar.WIDTH, 1), randrange(0, GlobalVar.HEIGHT, 1)

def clear_all_items():
    GlobalVar.boids_array = []
    GlobalVar.obstacle_array = []

def adjust_speed(type):
    if type:
        GlobalVar.speed_adjustment += 1
    else:
        GlobalVar.speed_adjustment -= 1

    if GlobalVar.speed_adjustment > MAX_SPEED:
        GlobalVar.speed_adjustment = MAX_SPEED
    elif GlobalVar.speed_adjustment < MIN_SPEED:
        GlobalVar.speed_adjustmment = MIN_SPEED