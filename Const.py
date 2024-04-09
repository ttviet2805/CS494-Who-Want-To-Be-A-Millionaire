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
QUESTION_BUTTON = []
ANSWER_BUTTON = [
    pygame.image.load('Assets/Images/InGame/answerButtonNotHover.png'),
    pygame.image.load('Assets/Images/InGame/answerButtonHover.png'),
    pygame.image.load('Assets/Images/InGame/correctAnswerButton.png'),
    pygame.image.load('Assets/Images/InGame/wrongAnswerButton.png'),
]
NEXT_BUTTON = [
    pygame.image.load('Assets/Images/InGame/nextButtonHover.png'),
    pygame.image.load('Assets/Images/InGame/nextButtonNotHover.png'),
    pygame.image.load('Assets/Images/InGame/nextButtonInvalid.png')
]


# WaitRoom
START_BUTTON = [
    pygame.image.load('Assets/Images/WaitRoom/startButtonNotHover.png'),
    pygame.image.load('Assets/Images/WaitRoom/startButtonHover.png'),
]
NAME_BUTTON = [
    pygame.image.load('Assets/Images/Waitroom/nameButton.png')
]

# EndRoom
HOME_BUTTON = [
    pygame.image.load('Assets/Images/EndRoom/homeButtonNotHover.png'),
    pygame.image.load('Assets/Images/EndRoom/homeButtonHover.png'),
]


