import pygame
import random
from GlobalVar import WIDTH, HEIGHT, BOID_COUNT, PREDATOR_COUNT
from Domain import OBSTACLE_RADIUS
from Boids_Agent import Boid
from Predator import Predator

BG = (200, 220, 255)
BOID_COLOR = (30, 30, 30)
PRED_COLOR = (255, 120, 100)

def main():
    pygame.init()
    display_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    boids = [Boid((random.uniform(0, WIDTH), random.uniform(0, HEIGHT))) for _ in range(BOID_COUNT)]
    predators = [Predator((random.uniform(0, WIDTH), random.uniform(0, HEIGHT))) for _ in range(PREDATOR_COUNT)]

    processing = 0
    frame = 0

    while processing == 0:
        clock.tick(60)
        frame += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                processing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                boids.append(Boid(pygame.mouse.get_pos()))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f: show_flocking = not show_flocking
                if event.key == pygame.K_p: show_predators = not show_predators
                if event.key == pygame.K_o: show_obstacle = not show_obstacle
                if event.key == pygame.K_a: show_arrows = not show_arrows
                if event.key == pygame.K_c: show_circles = not show_circles

        # background
        display_screen.fill(BG)

        # draw obstacle(i think this part should be in obstacle.py file?)

        mouse_pos = pygame.mouse.get_pos()
        if show_obstacle:
            pygame.draw.circle(display_screen, (100, 50, 50), mouse_pos, OBSTACLE_RADIUS, 1)
        
        # update boids
        for b in boids:
            if show_predators:
                for p in predators:
                    b.repel(p.pos, OBSTACLE_RADIUS)
            if show_obstacle:
                b.repel(mouse_pos, OBSTACLE_RADIUS)
            if show_flocking:
                b.flock(boids)
            b.update()
            b.draw(display_screen)

        # update predators
        if show_predators:
            for p in predators:
                if show_flocking:
                    p.flock(boids)
                    for other in predators:
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



if __name__ == "__main__":
    main()
