def init():
    global boids_array, obstacle_array, WIDTH, HEIGHT, FPS
    #global speed_adjustment

    boids_array = [] #To store the boids object
    obstacle_array = [] #To store the obstacle objects
    #speed_adjustment = 0 #To adjust the speed of the boids (if needed just uncomment)

    WIDTH = 1500 #Width of the simulation display
    HEIGHT = 800 #Height of the simulation display
    FPS = 60 #FPS of the simulation display
