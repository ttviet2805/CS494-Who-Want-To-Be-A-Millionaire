import pygame

# Color
WHITE = (255, 255, 255)
BROWN = (128,0,0)
BLACK = (0, 0, 0)
RED = (255,0,0)
S_COLOR = (255, 117, 117)
B_COLOR = (139, 236, 242)

# Text Font
FONT = 'Assets/Fonts/VarelaRound-Regular.ttf'


# Background
BACKGROUND = pygame.image.load('Assets/Images/Menu/menuBackground.png')

# Menu
REGISTER_BUTTON = [
    pygame.image.load('Assets/Images/Menu/registerNotHover.png'),
    pygame.image.load('Assets/Images/Menu/registerHover.png')
]
TEXT_BOX = [
    pygame.image.load('Assets/Images/Menu/textBox.png'),
    pygame.image.load('Assets/Images/Menu/textBoxClicked.png')
]

# Ingame
ANSWER_BUTTON_HOVER = pygame.image.load('Assets/Images/InGame/answerButtonHover.png')
ANSWER_BUTTON_NOT_HOVER = pygame.image.load('Assets/Images/InGame/answerButtonNotHover.png')
NEXT_BUTTON_HOVER = pygame.image.load('Assets/Images/InGame/nextButtonHover.png')
NEXT_BUTTON_NOT_HOVER = pygame.image.load('Assets/Images/InGame/nextButtonNotHover.png')
NEXT_BUTTON_INVALID = pygame.image.load('Assets/Images/InGame/nextButtonInvalid.png')



