import socket
import pygame
import pickle

# Socket
host, ip = "localhost", 5556
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((host, ip))

# Initialization of the Game
pygame.init()
width = 750
height = 500
screen = pygame.display.set_mode((width, height))  # Width by Height

# Window Stuff
pygame.display.set_caption("Pong")
icon = pygame.image.load("assets/img/icon.png")
pygame.display.set_icon(icon)

winner_font = pygame.font.SysFont("comicsans", 100)

blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)


class PaddleVerical(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 75])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.paddle_speed = 4
        self.points = 0


class PaddleHorizontal(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([75, 10])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.paddle_speed = 4
        self.points = 0


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/img/ball.png")
        self.rect = self.image.get_rect()
        self.speed = 2
        self.dx = 1
        self.dy = 1


def recieve_data():
    data = clientsocket.recv(1024)
    data = pickle.loads(data)
    return data


def init():
    global paddle1, paddle2, paddle3, paddle4, ball, all_sprites

    paddle1 = PaddleVerical()
    paddle1.image.fill(blue)
    paddle1.rect.x = 25
    paddle1.rect.y = 225

    paddle2 = PaddleVerical()
    paddle2.image.fill(red)
    paddle2.rect.x = 715
    paddle2.rect.y = 225

    paddle3 = PaddleHorizontal()
    paddle3.image.fill(yellow)
    paddle3.rect.x = 340
    paddle3.rect.y = 45

    paddle4 = PaddleHorizontal()
    paddle4.image.fill(green)
    paddle4.rect.x = 340
    paddle4.rect.y = 465

    ball = Ball()
    ball.rect.x = 375
    ball.rect.y = 250

    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle1, paddle2, paddle3, paddle4, ball)


def redraw(info):
    screen.fill(black)
    font = pygame.font.SysFont("Consolas", 24)
    text = font.render("", 1, black)
    text_rect = text.get_rect()
    text_rect.center = (width // 2, 25)
    screen.blit(text, text_rect)

    # Score text
    score_text = font.render("Score:", 1, white)
    score_text_rect = text.get_rect()
    score_text_rect.center = (20, 25)
    screen.blit(score_text, score_text_rect)

    # Player 1 score
    p1_score = font.render(str([info["points"]["player1"]]), 1, blue)
    p1_rect = p1_score.get_rect()
    p1_rect.center = (120, 25)
    screen.blit(p1_score, p1_rect)

    # Player 2 score
    p2_score = font.render(str([info["points"]["player2"]]), 1, red)
    p2_rect = p2_score.get_rect()
    p2_rect.center = (160, 25)
    screen.blit(p2_score, p2_rect)

    # Player 3 score
    p3_score = font.render(str([info["points"]["player3"]]), 1, yellow)
    p3_rect = p3_score.get_rect()
    p3_rect.center = (200, 25)
    screen.blit(p3_score, p3_rect)

    # Player 4 score
    p4_score = font.render(str([info["points"]["player4"]]), 1, green)
    p4_rect = p4_score.get_rect()
    p4_rect.center = (240, 25)
    screen.blit(p4_score, p4_rect)

    all_sprites.draw(screen)
    pygame.display.update()


def draw_winner(text):
    draw_text = winner_font.render(text, 1, white)
    screen.blit(
        draw_text,
        (
            width // 2 - draw_text.get_width() / 2,
            height // 2 - draw_text.get_height() / 2,
        ),
    )
    pygame.display.update()


def run():
    init()

    winner_text = ""
    restart_time = 0
    game_over = False

    last_touch = None
    touch = False

    clock = pygame.time.Clock()
    run = True
    while run:
        info = recieve_data()
        game_over = info["game_over"]
        paddle1.rect.y = info["paddle1_rect_y"]
        paddle2.rect.y = info["paddle2_rect_y"]
        paddle3.rect.x = info["paddle3_rect_x"]
        paddle4.rect.x = info["paddle4_rect_x"]

        clock.tick(100)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if not game_over:
            if paddle1.points >= 10:
                winner_text = "Blue Wins!"
                restart_time = current_time + 5000
                game_over = True

            if paddle2.points >= 10:
                winner_text = "Red Wins!"
                restart_time = current_time + 5000
                game_over = True

            if paddle3.points >= 10:
                winner_text = "Yellow Wins!"
                restart_time = current_time + 5000
                game_over = True

            if paddle4.points >= 10:
                winner_text = "Green Wins!"
                restart_time = current_time + 5000
                game_over = True

        if game_over:
            draw_winner(winner_text)
            if current_time > restart_time:
                init()
                game_over = False
            else:
                continue

        # Paddle movement
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            paddle1.rect.y -= paddle1.paddle_speed
        if key[pygame.K_s]:
            paddle1.rect.y += paddle1.paddle_speed
        if key[pygame.K_UP]:
            paddle2.rect.y -= paddle2.paddle_speed
        if key[pygame.K_DOWN]:
            paddle2.rect.y += paddle2.paddle_speed
        if key[pygame.K_a]:
            paddle3.rect.x -= paddle3.paddle_speed
        if key[pygame.K_d]:
            paddle3.rect.x += paddle3.paddle_speed
        if key[pygame.K_LEFT]:
            paddle4.rect.x -= paddle4.paddle_speed
        if key[pygame.K_RIGHT]:
            paddle4.rect.x += paddle4.paddle_speed

        # Ensures paddles never move off the screen
        if paddle1.rect.y < 0:
            paddle1.rect.y = 0

        if paddle1.rect.y > 425:
            paddle1.rect.y = 425

        if paddle2.rect.y < 0:
            paddle2.rect.y = 0

        if paddle2.rect.y > 425:
            paddle2.rect.y = 425

        if paddle3.rect.x < 0:
            paddle3.rect.x = 0

        if paddle3.rect.x > 680:
            paddle3.rect.x = 680

        if paddle4.rect.x < 0:
            paddle4.rect.x = 0

        if paddle4.rect.x > 680:
            paddle4.rect.x = 680

        # Ball movement
        ball.rect.x += ball.speed * ball.dx
        ball.rect.y += ball.speed * ball.dy

        # Setting up collision detection with the walls by changing ball's direction
        if ball.rect.y > 490:
            ball.rect.x, ball.rect.y = 375, 250
            touch = True

        if ball.rect.x > 740:
            ball.rect.x, ball.rect.y = 375, 250
            touch = True

        if ball.rect.y < 10:
            ball.rect.x, ball.rect.y = 375, 250
            touch = True

        if ball.rect.x < 10:
            ball.rect.x, ball.rect.y = 375, 250
            touch = True

        # Setting up collision detection with the paddles
        if paddle1.rect.colliderect(ball.rect):
            ball.dx = 1
            last_touch = "blue"

        if paddle2.rect.colliderect(ball.rect):
            ball.dx = -1
            last_touch = "red"

        if paddle3.rect.colliderect(ball.rect):
            ball.dy = 1
            last_touch = "yellow"

        if paddle4.rect.colliderect(ball.rect):
            ball.dy = -1
            last_touch = "green"

        # Set score
        if touch:
            if last_touch == "blue":
                paddle1.points += 1

            if last_touch == "red":
                paddle2.points += 1

            if last_touch == "yellow":
                paddle3.points += 1

            if last_touch == "green":
                paddle4.points += 1

            touch = False

        # Send data over socket
        data = dict()
        points = dict()
        points["player1"] = paddle1.points
        points["player2"] = paddle2.points
        points["player3"] = paddle3.points
        points["player4"] = paddle4.points
        data["points"] = points

        data["paddle1_rect_y"] = paddle1.rect.y
        data["paddle2_rect_y"] = paddle2.rect.y
        data["paddle3_rect_x"] = paddle3.rect.x
        data["paddle4_rect_x"] = paddle4.rect.x

        data["game_over"] = game_over
        data["winner_text"] = winner_text

        _data = pickle.dumps(data)
        clientsocket.send(_data)

        redraw(info)


if __name__ == "__main__":
    run()
