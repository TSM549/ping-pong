import os
import sys

import pygame


pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60
WIN_SCORE = 5
BACKGROUND = (28, 93, 82)
WHITE = (245, 248, 238)
PADDLE_SPEED = 7

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 28)

assets = os.path.dirname(os.path.abspath(__file__))
left_image = pygame.image.load(
    os.path.join(assets, "009b6b73-8481-4990-84bf-8c761aa167e1-removebg-preview.png")
).convert_alpha()
right_image = pygame.image.load(
    os.path.join(assets, "e37253f1-6889-474b-97ec-49585a9502d1-removebg-preview.png")
).convert_alpha()
ball_image = pygame.image.load(
    os.path.join(assets, "2ef5fe2d-4bb4-47d3-ac13-1285d991fa5d-removebg-preview.png")
).convert_alpha()

paddle_size = (90, 90)
left_image = pygame.transform.smoothscale(left_image, paddle_size)
right_image = pygame.transform.smoothscale(right_image, paddle_size)
ball_image = pygame.transform.smoothscale(ball_image, (32, 32))

left_paddle = pygame.Rect(35, HEIGHT // 2 - 50, 24, 100)
right_paddle = pygame.Rect(WIDTH - 59, HEIGHT // 2 - 50, 24, 100)
ball = pygame.Rect(WIDTH // 2 - 12, HEIGHT // 2 - 12, 24, 24)
ball_speed_x = 5
ball_speed_y = 4
left_score = 0
right_score = 0
game_over = False


def reset_ball(direction):
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = 5 * direction
    ball_speed_y = 4


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_over and event.key == pygame.K_r:
            left_score = 0
            right_score = 0
            game_over = False
            left_paddle.centery = HEIGHT // 2
            right_paddle.centery = HEIGHT // 2
            reset_ball(1)

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_w]:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s]:
            left_paddle.y += PADDLE_SPEED
        if keys[pygame.K_UP]:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN]:
            right_paddle.y += PADDLE_SPEED

        left_paddle.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
        right_paddle.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        if ball.colliderect(left_paddle) and ball_speed_x < 0:
            ball.left = left_paddle.right
            ball_speed_x *= -1
        if ball.colliderect(right_paddle) and ball_speed_x > 0:
            ball.right = right_paddle.left
            ball_speed_x *= -1

        if ball.left <= 0:
            right_score += 1
            game_over = right_score >= WIN_SCORE
            reset_ball(-1)
        elif ball.right >= WIDTH:
            left_score += 1
            game_over = left_score >= WIN_SCORE
            reset_ball(1)

    screen.fill(BACKGROUND)
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
    for y in range(12, HEIGHT, 28):
        pygame.draw.circle(screen, WHITE, (WIDTH // 2, y), 3)

    screen.blit(left_image, (left_paddle.centerx - 45, left_paddle.centery - 45))
    screen.blit(right_image, (right_paddle.centerx - 45, right_paddle.centery - 45))
    screen.blit(ball_image, (ball.centerx - 16, ball.centery - 16))

    left_text = font.render(str(left_score), True, WHITE)
    right_text = font.render(str(right_score), True, WHITE)
    screen.blit(left_text, (WIDTH // 2 - 70, 24))
    screen.blit(right_text, (WIDTH // 2 + 45, 24))

    if game_over:
        winner = "Gauche" if left_score >= WIN_SCORE else "Droite"
        message = font.render(f"{winner} gagne !", True, WHITE)
        restart = small_font.render("Appuyez sur R pour rejouer", True, WHITE)
        screen.blit(message, message.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 18)))
        screen.blit(restart, restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 24)))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
