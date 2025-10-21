import pygame
import random
import math
import GlobalVar
from BoidsAgent import Boid
from PredatorAgent import Predator

GlobalVar.init()

# --- INITIALIZE ---
pygame.init()
display_screen = pygame.display.set_mode((GlobalVar.WIDTH, GlobalVar.HEIGHT))
clock = pygame.time.Clock()

boids = [Boid((random.uniform(0, GlobalVar.WIDTH), random.uniform(0, GlobalVar.HEIGHT))) for _ in range(GlobalVar.BOID_COUNT)]
preds = [Predator((random.uniform(0, GlobalVar.WIDTH), random.uniform(0, GlobalVar.HEIGHT))) for _ in range(GlobalVar.PREDATOR_COUNT)]

# --- MAIN LOOP ---
running = True
frame = 0
while running:
    clock.tick(60)
    frame += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            boids.append(Boid(pygame.mouse.get_pos()))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f: GlobalVar.show_flocking = not GlobalVar.show_flocking
            if event.key == pygame.K_p: GlobalVar.show_predators = not GlobalVar.show_predators
            if event.key == pygame.K_o: GlobalVar.show_obstacle = not GlobalVar.show_obstacle
            if event.key == pygame.K_a: GlobalVar.show_arrows = not GlobalVar.show_arrows
            if event.key == pygame.K_c: GlobalVar.show_circles = not GlobalVar.show_circles

    # background
    display_screen.fill(GlobalVar.BG)

    mouse_pos = pygame.mouse.get_pos()
    if GlobalVar.show_obstacle:
        pygame.draw.circle(display_screen, (100, 50, 50), mouse_pos, GlobalVar.OBSTACLE_RADIUS, 1)

    # update boids
    for b in boids:
        if GlobalVar.show_predators:
            for p in preds:
                b.repel(p.pos, GlobalVar.OBSTACLE_RADIUS)
        if GlobalVar.show_obstacle:
            b.repel(mouse_pos, GlobalVar.OBSTACLE_RADIUS)
        if GlobalVar.show_flocking:
            b.flock(boids)
        b.update()
        b.draw(display_screen)

    # update predators
    if GlobalVar.show_predators:
        for p in preds:
            if GlobalVar.show_flocking:
                p.flock(boids)
                for other in preds:
                    if other is not p:
                        p.repel(other.pos, 30)
            p.update()
            p.draw(display_screen)

    # draw text
    font = pygame.font.SysFont("comic sans ms", 18)
    help_text = [
        "Flocking: f",
        "Obstacle: o",
        "Predator: p",
        "Arrows: a",
        "Circles: c",
        "Add Boid: click"
    ]
    for i, text in enumerate(help_text):
        display_screen.blit(font.render(text, True, (50, 20, 40)), (10, 670 + i*20))

    display_screen.blit(font.render(f"Number of Boids: {len(boids)}", True, (50, 20, 40)), (10, 10))
    display_screen.blit(font.render(f"Flocking: {'ON' if show_flocking else 'OFF'}", True, (50, 20, 40)), (10, 30))
    display_screen.blit(font.render(f"Obstacle: {'ON' if show_obstacle else 'OFF'}", True, (50, 20, 40)), (10, 50))
    display_screen.blit(font.render(f"Predators: {'ON' if show_predators else 'OFF'}", True, (50, 20, 40)), (10, 70))
    pygame.display.flip()

pygame.quit()
