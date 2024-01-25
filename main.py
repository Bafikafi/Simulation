# Importing necessary modules
import pygame
import objects
import electric_field
import pygame_widgets
from pygame_widgets.button import Button

# Importing sys module
import sys

# Initializing pygame
pygame.init()
clock = pygame.time.Clock()

mouse_clicked = False

# TODO other simulations - currently not implemented

# Creating display
width_of_display = 1280
height_of_display = 720
screen = pygame.display.set_mode((width_of_display, height_of_display))

# Creating buttons for Electric Field simulation and Exit
ef_button = objects.button(screen, width_of_display/2 - 75, height_of_display/2 - 25, 150, 50, text='Electric Field')
exit_button = objects.button(screen, width_of_display/2 - 75, height_of_display/2 + 75, 150, 50, text='Exit')
handled = False
mouse_down = False
mouse_dragged = False

# Creating an instance of the Electric Field simulation
ef = electric_field.electric_field(screen, 1)

# Variable to track whether in the Electric Field simulation
not_in_sim = False
in_efsim = False

# Function to start the Electric Field simulation
def start_sim():
    in_efsim = True

# Running loop
while True:
    screen.fill(pygame.Color('black'))
    mouse_poss = pygame.mouse.get_pos()

    # system prepared for multiple simulations
    if in_efsim:
        not_in_sim = False
    else:
        not_in_sim = True

    # Draw objects based on whether in the Electric Field simulation or not
    if not not_in_sim and in_efsim:
        ef.draw(screen)
        
        # Running Electric Field simulation
        mouses, in_efsim = electric_field.electric_field_simulation(screen, mouse_down, mouse_dragged, mouse_poss, ef)
        mouse_down, mouse_dragged = mouses[0], mouses[1]
    if not_in_sim:
        # Drawing buttons for Electric Field and Exit
        ef_button.draw(ef_button.is_in(mouse_poss[0], mouse_poss[1]))
        exit_button.draw(exit_button.is_in(mouse_poss[0], mouse_poss[1]))

    # Handling events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            print("A key has been pressed")

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handling button clicks
            if not_in_sim and  ef_button.is_in(mouse_poss[0], mouse_poss[1]):
                ef.make_utils()
                in_efsim = True
                not_in_sim = False
                ef.is_running = True
            
            if not_in_sim and exit_button.is_in(mouse_poss[0], mouse_poss[1]):
                pygame.quit()
                sys.exit()
                
            mouse_clicked = True
        else:
            mouse_clicked = False
    
    # Checking if during button press event, the main branch of the condition will happen only once
    if mouse_clicked:
        handled = True
    elif (not mouse_clicked) and handled:
        handled = False

    # Updating UI and display
    pygame_widgets.update(pygame.event.get())
    pygame.display.update()
    dt = clock.tick(60)  # Limits the framerate to 60 fps and creates dt variable for other simulations

    # Update the display
    pygame.display.flip()
    # TODO other simulations - currently not implemented
