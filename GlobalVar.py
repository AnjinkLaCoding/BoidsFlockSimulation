def init():
    global agent_array, obstacle_array, speed_adjustment, WIDTH, HEIGHT, BOID_COUNT, PREDATOR_COUNT, OBSTACLE_RADIUS
    global show_arrows, show_flocking, show_circles, show_predators, show_obstacle, obstacle_pos
    global BG, BOID_COLOR, PRED_COLOR

    #Storing agents
    agent_array = []
    #To store obstacles
    obstacle_array = []
    #To adjust the speed of the biods (if needed)
    speed_adjustment = 0

    #Width and height of the display
    WIDTH, HEIGHT = 1000, 800
    #Default boids
    BOID_COUNT = 10
    #Default predators
    PREDATOR_COUNT = 2
    #Obstacles radius
    OBSTACLE_RADIUS = 150

    #Flag for the features
    show_flocking = True
    show_arrows = True
    show_circles = False
    show_predators = True
    show_obstacle = False
    obstacle_pos = None

    #Background Configuration
    BG = (200, 220, 255)
    BOID_COLOR = (30, 30, 30)
    PRED_COLOR = (255, 120, 100)
