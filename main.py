# Example file showing a circle moving on screen
import constants
import pygame
import math
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode(constants.screen_size)
clock = pygame.time.Clock()
running = True

class Button:
    def __init__(self, location, size):
        self.location = location
        self.size = size
        self.button_pressed = [False, False, False]

    def button_is_pressed(self, type = "l"):
        pygame.event.get()
        mouse = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        if type.lower() == "l":
            num = 0
        elif type.lower() == "m":
            num = 1
        elif type.lower() == "r":
            num = 2
        else:
            print("The mouse button type that you have selected is invalid. Please use either \'l\', \'m\', or \'r\'.")

        # mouse_buttons[0] is the left mouse button. self.location[0] is the top right corner's x value, and self.location[1] is the y value.
        # self.size[0] and self.size[1] are the x and y lengths respectively.
        
        # This following massive if statement just detects if the cursor is within the x and y boundaries of the button and if the left button is being pressed.
        # If all of that is true, then it sets self.button_pressed = True. Upon releasing LMB, the third if statement will activate and it will return True.
        if mouse_buttons[num] == True and mouse[0] >= self.location[0] and mouse[0] <= (self.location[0] + self.size[0]) and mouse[1] >= self.location[1] and mouse[1] <= (self.location[1] + self.size[1]):
            self.button_pressed[num] = True

        # This detects if the cursor leaves the button. If it does, it sets self.button_pressed = False.
        # This enables you to chicken out of pressing the button if you drag your mouse off of the button without releasing left click.
        if mouse[0] <= self.location[0] or mouse[0] >= (self.location[0] + self.size[0]) or mouse[1] <= self.location[1] or mouse[1] >= (self.location[1] + self.size[1]):
            self.button_pressed[num] = False

        # This is what actually returns true. If the first if statement has been activated without the second one, then this one will activate and return true.
        # Mechanistically, this if statement is extremely similar to the first except that it requires the left mouse button to be released AND self.button_pressed == True. If both of those are true, return True.
        if mouse_buttons[num] == False and mouse[0] >= self.location[0] and mouse[0] <= (self.location[0] + self.size[0]) and mouse[1] >= self.location[1] and mouse[1] <= (self.location[1] + self.size[1]) and self.button_pressed[num] == True:
            self.button_pressed[num] = False
            return True
        
class button:
    def __init__(self, type, location, size = (135, 135), rowCol = None, resize = None, exponent = 1.3, multiplier = 2, numFrames = 2):
        self.type = type
        self.location = location
        self.size = size
        self.resize = resize
        self.button = Button(self.location, self.size)
        self.spritesheet = True

        self.rowCol = rowCol
        self.row = 0
        self.column = 0
        self.frame = 1
        self.sleep = 1
        self.animating = False
        self.framesCompleted = True
        self.exponent = exponent
        self.multiplier = multiplier
        self.numFrames = numFrames

        if type == "d4":
            self.image = pygame.image.load("d4_sheet.png")
            self.randMax = 4

        elif type == "d6":
            self.image = pygame.image.load("d6_sheet.png")
            self.randMax = 6

        elif type == "d8":
            self.image = pygame.image.load("d8_sheet.png")
            self.randMax = 8

        elif type == "d10":
            self.image = pygame.image.load("d10_sheet.png")
            self.randMax = 10

        elif type == "d12":
            self.image = pygame.image.load("d12_sheet.png")
            self.randMax = 12

        elif type == "d20":
            self.image = pygame.image.load("d20_sheet.png")
            self.randMax = 20

        else:
            self.image = pygame.image.load(self.type)
            self.spritesheet = False

    # Load a specific image from a specific rectangle
    def image_at(self, location, number = None, colorkey = None):
        # Loads image from x,y,x+offset,y+offset
        sprite_location = pygame.Rect(location[0] * self.size[0], location[1] * self.size[1], self.size[0], self.size[1])
        image = pygame.Surface(self.size, pygame.SRCALPHA)
        image.blit(self.image.subsurface(sprite_location), (0, 0))
        if self.resize:
            image = pygame.transform.scale(image, self.resize)
        if number:
            font = pygame.font.SysFont(constants.font, int(self.resize[0]/2.9))
            # These if statements just modify the positioning of the text for d4s and d20s because they look weird otherwise.
            if self.type == "d20": pygame.Surface.blit(image, font.render(str(self.randomNumber), True, "white"), (self.resize[0]/2 - font.size(str(self.randomNumber))[0]/2, self.resize[1]/2 - font.size(str(self.randomNumber))[1]/2.3))
            elif self.type == "d4": pygame.Surface.blit(image, font.render(str(self.randomNumber), True, "white"), (self.resize[0]/2 - font.size(str(self.randomNumber))[0]/2, self.resize[1]/2 - font.size(str(self.randomNumber))[1]/3))
            else: pygame.Surface.blit(image, font.render(str(self.randomNumber), True, "white"), (self.resize[0]/2 - font.size(str(self.randomNumber))[0]/2, self.resize[1]/2 - font.size(str(self.randomNumber))[1]/2))
        
        if colorkey is None:
            colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey)
        return image

    def roll(self):
        self.animating = True
        self.framesCompleted = False
        self.frame = 1
        self.sleep = 1
        self.randomNumber = random.randint(1, self.randMax)
    
    def draw(self, surface = screen):
        if self.spritesheet:
            # This if statement determines if the required amount of frames has passed. If yes, then set self.framesCompleted == True which enables the loop to stop when you get back to the first sprite in the sheet.
            if self.frame == (self.numFrames * 48 + 1):
                self.framesCompleted = True

            if self.animating == True:
                pygame.Surface.blit(surface, self.image_at((self.row, self.column)), self.location)
            
                # This code controls how fast the dice rolls.
                if self.sleep // self.frame ** self.exponent == 1:
                    self.column += 1
                    if self.column > self.rowCol[1]:
                        self.column = 0
                        self.row +=1
                    if self.row > self.rowCol[0]:
                        self.row = 0
                    self.frame += 1 # Log that another frame has been processed

                # This if statement ensures that the dice doesn't just randomly stop midway through its animation if you click the roll button again
                if self.framesCompleted == True and self.row == 0 and self.column == 0:
                    self.animating = False
                    self.frame = 1

                self.sleep += 1 * self.multiplier # Add one more frame to the sleep timer

            if self.animating == False: # Looks at self.animating is false. If it is, reset self.frame and self.sleep and blit the first object on the spritesheet.
                try: pygame.Surface.blit(screen, self.image_at((0, 0), number = self.randomNumber), self.location) # Blit the top left image onto to surface - this is the still dice
                except: pygame.Surface.blit(screen, self.image_at((0, 0)), self.location) # Blit the top left image onto to surface - this is the still dice
                self.frame = 1 # Reset frames back to 1
                self.sleep = 1 # Reset sleep back to 1
        else:
            if self.resize:
                self.image = pygame.transform.scale(self.image, self.resize)
            pygame.Surface.blit(surface, self.image, self.location)

    def update(self, location = None, size = None):
        if location: self.location = location; self.button.location = location
        if size: self.resize = size; self.button.size = size

def makeNewDice(type, location = None, size = (135, 135), resize = None):
    DICE.append(button(type, location, size, (7, 5), resize))

def calculateCoords(dice_number):
    # For the record, this is the only bit that ChatGPT did, and I have no idea how it works nor could I replicate it.
    usable_y_size = constants.screen_size[1] - (round((constants.screen_size[0] - 100) / 6) * 1.2)
    aspect_ratio = 1 / 2 # Change these numbers to set how you want the dice to be arranged. Currently, there are two columns per rows.
    num_dice = len(DICE)
    max_cols = min(num_dice, math.ceil(math.sqrt(num_dice / aspect_ratio)))
    max_rows = math.ceil(num_dice / max_cols)
    dice_width = constants.screen_size[0] // max_cols
    dice_height = usable_y_size // max_rows
    # Constrain dice_width and dice_height to the smaller of the two values
    dice_size = min(dice_width, dice_height)
    margin_x = (constants.screen_size[0] - dice_size * max_cols) // 2
    margin_y = (usable_y_size - dice_size * max_rows) // 2
    row = (dice_number - 1) // max_cols
    col = (dice_number - 1) % max_cols
    x = margin_x + col * dice_size
    y = margin_y + row * dice_size
    return (x, y), (dice_size, dice_size)


def initializeTheThings():

    global DICE, rollButton, makeD4, makeD6, makeD8, makeD8, makeD10, makeD12, makeD20, buttonSize, yValue

    DICE = []

    xFactor = round((constants.screen_size[0]-225-80)/6)
    buttonSize = math.floor(xFactor)
    yValue = constants.screen_size[1]-(buttonSize*1.2)

    rollButton = button("roll button.png", (constants.screen_size[0]-225, constants.screen_size[1]-buttonSize), (200, 100))
    makeD4 = button("d4.png", (10, (yValue)), resize = (buttonSize, buttonSize))
    makeD6 = button("d6.png", ((10 * 2 + xFactor + 8), (yValue+6)), resize = (buttonSize-16, buttonSize-16))
    makeD8 = button("d8.png", ((10 * 3 + xFactor * 2), (yValue)), resize = (buttonSize, buttonSize))
    makeD10 = button("d10.png", ((10 * 4 + xFactor * 3), (yValue)), resize = (buttonSize, buttonSize))
    makeD12 = button("d12.png", ((10 * 5 + xFactor * 4), (yValue)), resize = (buttonSize, buttonSize))
    makeD20 = button("d20.png", ((10 * 6 + xFactor * 5), (yValue)), resize = (buttonSize, buttonSize))
    
def makeGUI():
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("azure2")
    pygame.draw.rect(screen, "grey23", (0, constants.screen_size[1]-buttonSize*1.4, constants.screen_size[0], (buttonSize*1.4)))
    rollButton.draw()
    makeD4.draw()
    makeD6.draw()
    makeD8.draw()
    makeD10.draw()
    makeD12.draw()
    makeD20.draw()

def doThingsContinuously():

    diceNum = 1
    for i in DICE:
        location, size = calculateCoords(diceNum)
        i.update(location = location, size = size)
        i.draw()
        if i.button.button_is_pressed() == True: DICE.remove(i)
        if i.button.button_is_pressed("r") == True: i.roll()
        diceNum += 1

    if makeD4.button.button_is_pressed():
        makeNewDice("d4")

    if makeD6.button.button_is_pressed():
        makeNewDice("d6")

    if makeD8.button.button_is_pressed():
        makeNewDice("d8")

    if makeD10.button.button_is_pressed():
        makeNewDice("d10")

    if makeD12.button.button_is_pressed():
        makeNewDice("d12")

    if makeD20.button.button_is_pressed():
        makeNewDice("d20")

    if rollButton.button.button_is_pressed():
        for i in DICE:
            i.roll()


initializeTheThings()

while running:

    makeGUI()

    # poll for events
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]: # pygame.QUIT event means the user clicked X to close the window
            running = False

    pygame.event.get()
    
    if keys[pygame.K_ESCAPE]:
        running = False
    
    doThingsContinuously()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    clock.tick(60)

pygame.quit()