import pygame
import sys
import objects
import logic
import math
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button


def exit_sim(ef, ef_sim):
    ef.UI_utils.__del__()


# Here we have all of the important sliders and buttons we will use
class UI_utilities:
    def __init__(self, screen) -> None:
        # Slider for adjusting grid size
        self.grid_slider = Slider(screen, 1050, 200, 150, 50, min=20, max=60, step=10) 

        # Textbox for displaying and adjusting grid size
        self.font = pygame.font.SysFont('Ariel', 20)
        self.grid_text = TextBox(screen, 1100, 130, 50, 50, fontSize=30)
        self.grid_label = TextBox(screen, 1050, 80, 150, 40, fontSize=24)
        self.grid_label.setText('Grid size in px')

        # Textbox for displaying instructions
        text = 'Left click to add charge \n Left click on a charge to change polarity \n Left click and drag to move charge \n Right click to remove charge'
        self.text = text.split(' \n ')

        # Set colors for the slider
        self.grid_slider.colour = (100, 100, 100)
        self.grid_slider.handleColour = (250, 250, 250)

        # Button for exiting simulation
        self.exit_button = objects.button(screen, 1050, 650, 150, 50, text='Back to menu')
        self.screen = screen

    def __del__(self):
        # Destructor (currently empty)
        ...

# Class representing an electric charge
class electric_charge:
    def __init__(self, possition: list, positive=True, coulumb=1) -> None:
        self.positive = positive
        self.coulumb = coulumb
        self.possition = possition

    # Method to change the position of the charge
    def change_poss(self, dx, dy):
        new_x = self.possition[0] + dx
        new_y = self.possition[1] + dy

        # Ensure the charge stays within the screen boundaries
        if not 0 < new_x < 1000:
            new_x = self.possition[0]
        
        if not 0 < new_y < 720:
            new_y = self.possition[1] 

        self.possition[0] = new_x
        self.possition[1] = new_y

    # Method to draw the charge on the screen
    def draw(self, screen):
        if self.positive:
            color = pygame.Color('Blue')
        else:
            color = pygame.Color('Red')
        pygame.draw.circle(screen, color, self.possition, 15)

        # Draw the signs (+ and -) around the charge
        start_poss = [self.possition[0] - 10, self.possition[1]]
        end_poss = [self.possition[0] + 10, self.possition[1]]
        pygame.draw.line(screen, pygame.Color('Black'), start_poss, end_poss)

        if self.positive:
            start_poss = [self.possition[0], self.possition[1] - 10]
            end_poss =  [self.possition[0], self.possition[1] + 10]
            pygame.draw.line(screen, pygame.Color('Black'), start_poss, end_poss)

# Class representing an electric field
class electric_field:
    def __init__(self, screen, scale: float, grid_size=40) -> None:
        self.scale = scale
        self.electric_charges = []
        self.grid_size = grid_size
        self.screen = screen
        self.is_running = True
        self.has_utils = False

    # Method to change the polarity of a charge at a specific position
    def change_charge(self, x, y):
        for charge in self.electric_charges:
            if abs(charge.possition[0] - x) <= 15 and abs(charge.possition[1] - y) <= 15:
                charge.positive = not charge.positive
                return

    # Method to create UI utilities
    def make_utils(self):
        self.UI_utils = UI_utilities(self.screen)
        self.has_utils = True

    # Method to delete UI utilities
    def del_utils(self):
        del(self.UI_utils)
        self.has_utils = False

    # Method to add a charge at a specific position
    def add_charge(self, x, y, possitive=True, coulumb=1):
        if 0 < x < 1000 and 0 < y < 720:
            self.electric_charges.append(electric_charge([x, y], possitive, coulumb))

    # Method to remove a charge at a specific position
    def remove_charge(self, x, y):
        for charge in self.electric_charges:
            if abs(charge.possition[0] - x) <= 15 and abs(charge.possition[1] - y) <= 15:
                self.electric_charges.remove(charge)
                del(charge)
                return

    # Method to move a charge by a certain displacement
    def move_charge(self, poss, rel_poss):
        x, y = poss[0], poss[1]
        dx, dy = rel_poss[0], rel_poss[1]
        for charge in self.electric_charges:
            if abs(charge.possition[0] - x) <= 15 and abs(charge.possition[1] - y) <= 15:
                charge.change_poss(dx, dy)
                break

    # Method to check if a position is inside a charge
    def inside_charge(self, poss: list) -> bool:
        for charge in self.electric_charges:
            if abs(charge.possition[0] - poss[0]) <= 15 and abs(charge.possition[1] - poss[1]) <= 15:
                return True
        return False

    # Method to draw an arrow representing the electric field vector at a position
    def draw_arrow(self, screen, possition: list, vector):
        arrow_length = self.grid_size / 2 - self.grid_size/10
        vector_len = math.sqrt(vector[0]**2 + vector[1]**2)
        if vector_len == 0:
            vector_len = 1
        vector = [component/vector_len for component in vector]
        end_position = [possition[0] + vector[0] * arrow_length, possition[1] + vector[1] * arrow_length]
        strength = vector_len/0.3
        if strength > 1:
            strength = 1
        color_value = int(255 * strength)
        color = (color_value, color_value, color_value)
        pygame.draw.line(screen, color, possition, end_position)
        logic.draw_arrow_head(screen, vector, end_position, strength)

    # Method to draw electric field vectors on the screen
    def draw_vectors(self, screen):
        width = 1000//self.grid_size
        height = 720//self.grid_size
        max_length = 5

        for i in range(width):
            for j in range(height):
                poss = [i * self.grid_size, j * self.grid_size]
                vector, length = logic.calculate_electric_field_vector(self.electric_charges, poss, self.scale)
                normalized_vector = [component / length if length > 0 else 0 for component in vector]
                self.draw_arrow(screen, poss, vector)
        return True

    # Method to draw charges, vectors, and UI elements on the screen
    def draw(self, screen):
        for charge in self.electric_charges:
            charge.draw(screen)
        self.draw_vectors(screen)
        self.UI_utils.grid_text.setText(str(self.grid_size))
        self.grid_size = self.UI_utils.grid_slider.getValue()
        self.UI_utils.exit_button.draw()
        for i, text in enumerate(self.UI_utils.text):
            objects.display_text(screen, text, self.UI_utils.font, (255, 255, 255), 1000, 350 + i*50)

    # Method to exit the simulation
    def exit(self):
        self.is_running = False
        self.del_utils()
        for charge in self.electric_charges:
            del(charge)
        self.grid_size = 40
        self.electric_charges = []

# Function representing the main loop of the electric field simulation
def electric_field_simulation(screen, mouse_down, mouse_dragged, poss_mouse, ef):
    ef.scale = 6
    mouse1 = pygame.mouse.get_pressed()[0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True          
            
            # Right-click to remove charge
            if pygame.mouse.get_pressed()[2]:
                ef.remove_charge(poss_mouse[0], poss_mouse[1])
            
            # Click on the exit button to end the simulation
            if ef.UI_utils.exit_button.is_in(poss_mouse[0], poss_mouse[1]):
                ef.is_running = False
            
            mouse_clicked = True
        
        else:
            mouse_clicked = False
        
        if mouse_down and event.type == pygame.MOUSEMOTION:
                ef.move_charge(poss_mouse, event.rel)
                mouse_dragged = True
            
        if event.type == pygame.MOUSEBUTTONUP:
            # Left-click without dragging to change charge polarity
            if mouse1 and not mouse_dragged:
                ef.change_charge(poss_mouse[0], poss_mouse[1])
            
            # Left-click without charge at the position to add a new charge
            if not ef.inside_charge(poss_mouse) and mouse1:
                ef.add_charge(poss_mouse[0], poss_mouse[1])
            
            mouse_dragged = False
            mouse_down = False

    if not ef.is_running:
        ef.exit()
        return [mouse_down, mouse_dragged], False

    return [mouse_down, mouse_dragged], True



if __name__ == '__main__':
    import sys

    # initialising pygame
    pygame.init()
    clock = pygame.time.Clock()

    mouse_clicked = False

    width = 1280
    height = 720

    

    # creating display
    screen = pygame.display.set_mode((1280, 720))
    handled = False
    mouse_down = False
    mouse_dragged = False
    # objects.UI.__init__(pygame)
    ef = electric_field(screen, 1)

    # creating a running loop
    while True:
        screen.fill(pygame.Color('black'))

        ef.draw(screen)

        poss_mouse = pygame.mouse.get_pos()


        mouses = electric_field_simulation(screen, mouse_down, mouse_dragged, ef)
        mouse_down, mouse_dragged = mouses[0], mouses[1]
        pygame_widgets.update(pygame.event.get())
        # Update the display
        pygame.display.flip()

        dt = clock.tick(60)  # limits the framerate to 60 fps
