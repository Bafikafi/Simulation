import pygame




# button to press       
class button:
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')

    def __init__(self, screen, x, y, width, height, text) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.font = pygame.font.SysFont(None, 30)
        self.img = self.font.render(text, True, 'black')

    
    def draw(self, is_mouse_on=False):
        if not isinstance(is_mouse_on, bool):
            raise TypeError
        
        if is_mouse_on:
            color = self.COLOR_ACTIVE
        else:
            color = self.COLOR_INACTIVE
        pygame.draw.rect(self.screen, color, [self.x, self.y, self.width, self.height])
        self.screen.blit(self.img, (self.x + self.width / 10, self.y + self.height / 4))

    # detects if the mouse or x, y coordinate is on the button
    def is_in(self, x, y) -> bool:
        return self.x+self.width > x > self.x and self.y + self.height > y > self.y
    
    # changes text of the button
    def change_text(self, text):
        self.img = self.font.render(text, True, 'black')


class checkbox:
    def __init__(self, screen, x, y, bg_color, size=50, checked=False) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        self.size = size
        self.checked = checked
        self.bg_color = bg_color

    # renders the box itself and if it is checked it will also render cross in the middle
    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), [self.x, self.y, self.size, self.size])
        pygame.draw.rect(self.screen, self.bg_color, [self.x+5, self.y+5, self.size-10, self.size-10])
        if self.checked:
            pygame.draw.line(self.screen, pygame.Color('White'), (self.x + 5, self.y + 5), (self.x - 5 + self.size, self.y - 5 + self.size), 3)
            pygame.draw.line(self.screen, pygame.Color('White'), (self.x + 5, self.y + self.size - 5), (self.x + self.size - 5 , self.y + 5), 3)
    
    # this should happen if it is clicked on it
    def click(self):
        self.checked = not self.checked
    
    # will return True, if x, y coords or the possition of click is inside
    def is_in(self, x, y) -> bool:
        return self.x+self.size > x > self.x and self.y + self.size > y > self.y


    def is_checked(self):
        return self.checked
    
def display_text(screen, text: str, font, color: tuple, x: int, y: int):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))