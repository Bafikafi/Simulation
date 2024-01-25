import pygame
import math

# assuming we are calculating vector for visual purpouses we can assume the constant k = 1 or k = scale
# this constant is not in any place, what would make this calculation for visual pourpuses invalid.
# we will be using Coulumb's law to calculate the Force, F = k*(q*Q)/r, where k is coulumb's constant
# that we already have given it value of 1, q and Q are electric charges, r is the distance between 
# charges, for vector of F, we will replace r in equasion with vector r
# for visual pourpuses we will assume that in this possition the charge is equal to q = 1 C. Basically,
# we are getting the potencial of the field in this possition
def calculate_electric_field_vector(charges, possition, scale):

    vector_x = 0
    vector_y = 0
    distance = 0

    for charge in charges:
        
        # Here we define the polarity, if it is positive, than the vector should 
        # be pointing away from the electric charge
        polarity = 1
        if charge.positive:
            polarity = -1

        dx = charge.possition[0] - possition[0]
        dy = charge.possition[1] - possition[1]

        # Calculate absolute distance to avoid division by zero
        distance = max(math.sqrt(dx**2 + dy**2), 1)

        # Coulomb's law: F = k * (q1 * q2) / r^2
        # Here, we assume k = 1, and q1 and q2 are both equal to 1.
        # But if the charge is supposed to be bigger, we can easily update it
        # by using scale variable
        magnitude = scale / distance**2

        # Update vector components based on the charge and distance
        vector_x += polarity * magnitude * 500 * dx / distance
        vector_y += polarity * magnitude * 500 * dy / distance
    
    # We will return the vector of the intensity and the length of the vector,
    # so we don't need to calculate it later
    return [vector_x, vector_y], math.sqrt(vector_x**2 + vector_y**2)




# problem we are solving with this, is that when we draw arrows, we need to draw the head of an arrow
# in 45 deg angle. We are solving it by calculating the vector rotated by 45 deg and inverting it, therefore
# we get a vector in the direction we need to draw the head line
def draw_arrow_head(screen, vector, point_position, strength):

    # we got the strength of the force, we can determin the color with it
    color_value = int(255 * strength)
    color = (color_value, color_value, color_value)

    # the cosine function is working with radians
    angle = math.radians(45)

    # we calculate the first vector, this is the x element
    x_vector = -(math.cos(angle) * vector[0] - math.sin(angle) * vector[1])
    
    # here we just calculate the y element of the vector
    y_vector = -(math.sin(angle) * vector[0] + math.cos(angle) * vector[1])

    leng_of_vector = math.sqrt(x_vector**2 + y_vector**2)

    # we are just normalizing vector and making it the size we need for our arrow
    if x_vector != 0:
        x_vector = (x_vector / leng_of_vector) * 5

    if y_vector != 0:
        y_vector = (y_vector / leng_of_vector) * 5
    
    # This is wehere we can determin where to draw the line.
    end_position = [point_position[0] + x_vector, point_position[1] + y_vector]

    pygame.draw.line(screen, color, point_position, end_position)

    # we do the same here for the other line in the arrow head
    angle = math.radians(-45)

    x_vector = -(math.cos(angle) * vector[0] - math.sin(angle) * vector[1])


    y_vector = -(math.sin(angle) * vector[0] + math.cos(angle) * vector[1])

    leng_of_vector = math.sqrt(x_vector**2 + y_vector**2)

    if x_vector != 0:
        x_vector = (x_vector / leng_of_vector) * 5

    if y_vector != 0:
        y_vector = (y_vector / leng_of_vector) * 5

    end_position = [point_position[0] + x_vector, point_position[1] + y_vector]

    pygame.draw.line(screen, color, point_position, end_position)

