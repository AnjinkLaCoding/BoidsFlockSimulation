import pygame
import random
import math
# import from 

pygame.init()
display_screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

boids = [Boid((random.uniform(0, WIDTH), random.uniform(0, HEIGHT))) for _ in range(BOID_COUNT)
predators = [Predator((random.uniform(0, WIDTH), random.uniform(0,HEIGHT))) for _ in range(PREDATOR_COUNT)

