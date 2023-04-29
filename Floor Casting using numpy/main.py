import numpy
import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Dimensions of the pygame window
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

# Create pygame window
DISP_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Create the constants
H_RES = 120 # Resolution horizontally
HALF_VRES = 100 # Half of the resolution vertically
H_FOV = 60 # Horizontal field of vision in degrees
SCALE = H_RES // H_FOV # Each angle scales 2 display resolutions

# Defining some common variables
player_x = WINDOW_WIDTH /2
player_y = WINDOW_WIDTH /2
player_angle = math.pi / 2 # In radians

# Create the clock
CLOCK = pygame.time.Clock()
FPS = 60

ROTATION_SPEED = 0.001 * FPS
PLAYER_SPEED = 0.005 * FPS

# The main function of the program
def main():
    # Background sky image
    sky_img = pygame.image.load("Images/bg.jpg")
    sky_array = pygame.surfarray.array3d(pygame.transform.scale(sky_img, (360, HALF_VRES)))

    #Floor image
    floor_img = pygame.image.load("Images/floor.jpg")
    floor_array = pygame.surfarray.array3d(floor_img)

    # Create an array corresponding to the distance of a point from player
    dist_array = HALF_VRES / (HALF_VRES + 0.01 - numpy.linspace(0, HALF_VRES, HALF_VRES))

    # Create an array for the shade of a the flooring
    shade = 0.2 + 0.8 * (numpy.linspace(0, HALF_VRES, HALF_VRES) / HALF_VRES)
    shade_array = numpy.dstack((shade, shade, shade))
    
    # Game loop
    while True:
        # Time difference between the previous call of the function
        time = CLOCK.tick(FPS)

        # Actual FPS
        actual_fps = CLOCK.get_fps()

        # Set the title of the pygame window
        pygame.display.set_caption("FLOOR CASTING fps: " + str(int(actual_fps)))

        # To handle pygame events
        for event in pygame.event.get():
            # Quit condition
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        frame_array = numpy.random.uniform(0, 1, (H_RES, HALF_VRES * 2, 3)) # => returns a random noise like frame array
        frame_array = new_frame(frame_array, sky_array, floor_array, dist_array, shade_array) # => desired frame array is created

        # Convert the array into a surface
        surface = pygame.surfarray.make_surface(frame_array * 255)

        # Transform the surface to fit the display surface
        surface = pygame.transform.scale(surface, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Blit the surface onto the display surface
        DISP_SURF.blit(surface, (0, 0))

        pygame.display.update()

        # Player movement
        movement(time)

def new_frame(frame_array, sky_array, floor_array, dist_array, shade_array):
    # Iterating through the rays
    for nth_ray in range(H_RES):
        ray_angle = player_angle + numpy.deg2rad(nth_ray / SCALE - H_FOV / 2)
        sin = numpy.sin(ray_angle)
        cos = numpy.cos(ray_angle)
        cos2 = numpy.cos(player_angle - ray_angle)
        point_x_array = player_x + cos / cos2 * dist_array
        point_y_array = player_y - sin / cos2 * dist_array
        xx_array = (point_x_array * 100 % 505).astype("int")
        yy_array = (point_y_array * 100 % 505).astype("int")
        
        frame_array[H_RES - nth_ray - 1][:HALF_VRES] = sky_array[int(numpy.rad2deg(ray_angle)) % 360][:HALF_VRES] / 255
        frame_array[H_RES - nth_ray - 1][HALF_VRES:] = shade_array * floor_array[numpy.flip(xx_array), numpy.flip(yy_array)] / 255
        
    return frame_array
    
def movement(time):
    global player_x, player_y, player_angle
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        player_x += numpy.cos(player_angle) * PLAYER_SPEED * time / FPS
        player_y -= numpy.sin(player_angle) * PLAYER_SPEED * time / FPS 

    if keys[pygame.K_DOWN]:
        player_x -= numpy.cos(player_angle) * PLAYER_SPEED * time / FPS
        player_y += numpy.sin(player_angle) * PLAYER_SPEED * time / FPS

    if keys[pygame.K_LEFT]:
        player_x -= numpy.sin(player_angle) * PLAYER_SPEED * time / FPS
        player_y -= numpy.cos(player_angle) * PLAYER_SPEED * time / FPS
    
    if keys[pygame.K_RIGHT]:
        player_x += numpy.sin(player_angle) * PLAYER_SPEED * time / FPS
        player_y += numpy.cos(player_angle) * PLAYER_SPEED * time / FPS
    
    if keys[ord('a')]:
        player_angle += ROTATION_SPEED
    
    if keys[ord('d')]:
        player_angle -= ROTATION_SPEED

if __name__ == "__main__":
    main()
