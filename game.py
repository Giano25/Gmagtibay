import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ping Pong Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 15

# Paddle Positions
player1 = pygame.Rect(30, (SCREEN_HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(SCREEN_WIDTH - 50, (SCREEN_HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS, BALL_RADIUS)

# Speed
ball_speed_x, ball_speed_y = 5, 5
player_speed = 7
ai_speed = 5

# Clock
clock = pygame.time.Clock()

# Score
player1_score, player2_score = 0, 0
font = pygame.font.SysFont(None, 50)


# Draw Text
def draw_text(text, x, y):
    render = font.render(text, True, RED)
    screen.blit(render, (x, y))


# AI for Computer Player
def ai_move():
    if ball.centery > player2.centery:
        player2.y += ai_speed
    if ball.centery < player2.centery:
        player2.y -= ai_speed


# Difficulty Selection
def select_difficulty():
    global ai_speed
    selecting = True
    while selecting:
        screen.fill(BLACK)
        draw_text("Select Difficulty Level", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 4)
        draw_text("1 - Easy", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
        draw_text("2 - Medium", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
        draw_text("3 - Hard", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    ai_speed = 3
                    selecting = False
                elif event.key == pygame.K_2:
                    ai_speed = 5
                    selecting = False
                elif event.key == pygame.K_3:
                    ai_speed = 7
                    selecting = False


# Main Loop
def main():
    global ball_speed_x, ball_speed_y, player1_score, player2_score

    running = True
    play_with_computer = None

    while play_with_computer is None:
        screen.fill(BLACK)
        draw_text("Press 1 to Play with Human", SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 3)
        draw_text("Press 2 to Play with Computer", SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    play_with_computer = False
                if event.key == pygame.K_2:
                    play_with_computer = True
                    select_difficulty()

    while running:
        screen.fill(BLACK)
        draw_text(f"{player1_score} - {player2_score}", SCREEN_WIDTH // 2 - 50, 20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= player_speed
        if keys[pygame.K_s] and player1.bottom < SCREEN_HEIGHT:
            player1.y += player_speed

        if not play_with_computer:
            if keys[pygame.K_UP] and player2.top > 0:
                player2.y -= player_speed
            if keys[pygame.K_DOWN] and player2.bottom < SCREEN_HEIGHT:
                player2.y += player_speed
        else:
            ai_move()

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
            ball_speed_y *= -1

        if ball.colliderect(player1) or ball.colliderect(player2):
            ball_speed_x *= -1

        if ball.left <= 0:
            player2_score += 1
            ball.x, ball.y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
            ball_speed_x *= -1
        if ball.right >= SCREEN_WIDTH:
            player1_score += 1
            ball.x, ball.y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
            ball_speed_x *= -1

        if player1_score == 15 or player2_score == 15:
            running = False
            winner = "Player 1" if player1_score == 15 else "Player 2"
            draw_text(f"{winner} Wins!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(3000)

        pygame.draw.rect(screen, WHITE, player1)
        pygame.draw.rect(screen, WHITE, player2)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
