import sys, pygame, random
from pygame.locals import *

screenWidth = 900
screenHeight = 600
gridSize = 30
xGrids = screenWidth // gridSize
yGrids = screenHeight // gridSize
game = { "state": "startup" }
headTo = { "direction": "east" }
score = 0
deltaScore = 0
level = 1

def init():
    pygame.init()
    pygame.display.set_caption("Snake")

    global screen, clock, main_img, grass_img, head_img, body_img, nibble_img, dead_img, background_music, eat_audio
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    clock = pygame.time.Clock()

    main_img = pygame.image.load("assets/image/main.png").convert()
    grass_img = pygame.image.load("assets/image/grass.png")
    head_img = pygame.image.load("assets/image/head.png").convert_alpha()
    body_img = pygame.image.load("assets/image/body.png")
    nibble_img = pygame.image.load("assets/image/nibble.png").convert_alpha()
    dead_img = pygame.image.load("assets/image/sadSnake.png")

    background_music = pygame.mixer.Sound("assets/audio/music.ogg")
    eat_audio = pygame.mixer.Sound("assets/audio/eat.ogg")

def drawText(screen, pos, text, size, color, bold=False, italic=False, posCenter=False):
    font = pygame.font.Font(None, size)
    font.set_bold(bold)
    font.set_italic(italic)
    text = font.render(text, True, color)

    if posCenter:
        textBox = text.get_rect()
        textBox.center = pos
        screen.blit(text, textBox)
    else:
        screen.blit(text, pos)

def showWelcomeScreen():
    screen.blit(main_img, (0, 0))
    screenCenter = (screenWidth // 2, screenHeight // 2)

    drawText(screen, (screenCenter[0], screenCenter[1]-50), "Snake", 150, (200, 100, 200), posCenter=True)
    drawText(screen, (screenCenter[0], screenCenter[1]+50), "Press space to start",  60, (10, 10, 10), posCenter=True)

    pygame.display.update()

    while True:
        clock.tick(8)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    game["state"] = "running"
                    return

def placeNibble():
    notOK = True
    while notOK:
        pos = random.randint(0, xGrids-1), random.randint(0, yGrids-1)
        for body in snake:
            if body == pos:
                continue
        notOK = False
    return pos

def resetGame():
    global snake, nibble, score, deltaScore, level
    snake = [(8, 8), (7, 8), (6, 8)]
    nibble = (10, 10)
    headTo["direction"] = "east"
    score = 0
    deltaScore = 0
    level = 1

def startGame():
    global snake, nibble, score, deltaScore, level
    resetGame()

    background_music.play(loops=-1, fade_ms=500)

    while True:
        clock.tick(6 + level)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                turn(snake, event)

        if snake[0] == nibble:
            eat_audio.play()

            score += 5
            deltaScore += 5
            if deltaScore >= 20:
                level += 1
                deltaScore = 0

            nibble = placeNibble()
            move(snake, True)
        else:
            move(snake, False)

        head = snake[0]
        if head[0] < 0 or head[0] >= xGrids or head[1] < 0 or head[1] >= yGrids:
            game["state"] = "died"
            return
        for body in snake[1:]:
            if body == snake[0]:
                game["state"] = "died"
                return

        screen.blit(grass_img, (0, 0))
        screen.blit(nibble_img, (nibble[0]*gridSize, nibble[1]*gridSize))
        drawSnake(snake)
        drawText(screen, (50, 50), "Level: %d   Scores: %d " % (level, score), 60, (0, 88, 88))

        pygame.display.update()

def turnHead():
    h_img = head_img
    direction = headTo["direction"]
    if direction == "north":
        h_img = pygame.transform.rotate(head_img, 270)
    elif direction == "east":
        h_img = pygame.transform.rotate(head_img, 180)
    elif direction == "south":
        h_img = pygame.transform.rotate(head_img, 90)
    return h_img

def drawSnake(snake):
    h_img = turnHead()
    screen.blit(h_img, (snake[0][0]*gridSize, snake[0][1]*gridSize))
    for pos in snake[1:]:
        screen.blit(body_img, (pos[0]*gridSize, pos[1]*gridSize))

def turn(snake, event):
    direction = headTo["direction"]

    if direction == "west" or direction == "east":
        if event.key == K_UP: headTo["direction"] = "north"
        elif event.key == K_DOWN: headTo["direction"] = "south"
    elif direction == "north" or direction == "south":
        if event.key == K_RIGHT: headTo["direction"] = "east"
        elif event.key == K_LEFT: headTo["direction"] = "west"


def move(snake, eat):
    direction = headTo["direction"]
    newHead = ()
    if direction == "east":
        newHead = (snake[0][0] + 1, snake[0][1])
    elif direction == "south":
        newHead = (snake[0][0], snake[0][1] + 1)
    elif direction == "west":
        newHead = (snake[0][0] - 1, snake[0][1])
    elif direction == "north":
        newHead = (snake[0][0], snake[0][1] - 1)

    snake.insert(0, newHead)
    if not eat:
        del snake[-1]

def showDeathScreen():
    screen.fill((100, 100, 100))
    screen.blit(dead_img, (30, 20))

    drawText(screen, (300, 100), "YOU DIED!", 150, (255, 0, 0))
    drawText(screen, (350, 240), "Press space to restart", 60, (0, 0, 0))

    pygame.display.update()

    background_music.stop()

    while True:
        clock.tick(8)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    game["state"] = "running"
                    return

def main():
    init()

    while True:
        state = game["state"]
        if state == "startup":
            showWelcomeScreen()
        elif state == "running":
            startGame()
        elif state == "died":
            showDeathScreen()

if __name__ == "__main__":
    main()
