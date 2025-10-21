def init():
    # --- CONFIG ---
    WIDTH, HEIGHT = 800, 400
    BOID_COUNT = 10
    PREDATOR_COUNT = 2
    OBSTACLE_RADIUS = 60

    # --- FLAGS ---
    show_flocking = True
    show_arrows = True
    show_circles = False
    show_predators = True
    show_obstacle = False

    # --- COLORS ---
    BG = (255, 249, 240)
    BOID_COLOR = (30, 30, 30)
    PRED_COLOR = (255, 120, 100)
