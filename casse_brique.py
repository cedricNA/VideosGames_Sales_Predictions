import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définition des constantes
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
BRICK_WIDTH = 91
BRICK_HEIGHT = 30
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BACKGROUND_COLOR = (30, 30, 30)
LIVES = 1

# Initialisation de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Casse-Briques")

# Charger la police
font_path = "PressStart2P-Regular.ttf"
try:
    font = pygame.font.Font(font_path, 15)
except FileNotFoundError:
    print(f"Police {font_path} introuvable.")
    sys.exit()


# Classe pour la brique
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        pygame.draw.rect(surface, self.image, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)


# Classe pour la raquette
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
        self.rect.y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - PADDLE_WIDTH:
            self.rect.x += 5


# Classe pour la balle
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed_x = 3
        self.speed_y = -3

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y
        if self.rect.bottom >= SCREEN_HEIGHT:
            global lives
            lives -= 1
            self.rect.x = SCREEN_WIDTH // 2
            self.rect.y = SCREEN_HEIGHT // 2
            if lives < 0:
                show_game_over()
            else:
                pygame.time.wait(1000)

        if pygame.sprite.collide_rect(self, paddle):
            self.speed_y = -self.speed_y

        hit_list = pygame.sprite.spritecollide(self, bricks, True)
        if hit_list:
            self.speed_y = -self.speed_y
            if len(bricks) == 0:
                show_you_win()


# Fonction pour afficher le texte
def draw_text(surface, text, font, color, rect, aa=False, bkg=None):
    font_surface = font.render(text, aa, color, bkg)
    font_rect = font_surface.get_rect(center=rect.center)
    surface.blit(font_surface, font_rect.topleft)


# Fonction pour afficher la page d'instructions
def show_instructions():
    screen.fill(BACKGROUND_COLOR)
    instructions = [
        "Instructions du jeu Casse-Briques",
        "Utilisez les flèches gauche et droite pour déplacer la raquette.",
        "Le but du jeu est de détruire toutes les briques avec la balle.",
        "Vous avez 2 vies.",
        "Appuyez sur le bouton Commencer pour débuter le jeu.",
    ]
    for i, line in enumerate(instructions):
        draw_text(screen, line, font, WHITE, screen.get_rect().move(0, i * 40 + 50))
    pygame.draw.rect(screen, WHITE, start_button)
    draw_text(screen, "Commencer", font, BACKGROUND_COLOR, start_button)
    pygame.display.flip()


# Fonction pour afficher la page de Game Over
def show_game_over():
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(font_path, 25)
    draw_text(screen, "Game Over", font, RED, screen.get_rect().move(0, -50))

    # Ajuster la taille du rectangle pour "Quitter"
    pygame.draw.rect(screen, WHITE, quit_button)
    draw_text(screen, "Quitter", font, BACKGROUND_COLOR, quit_button)

    # Ajuster la taille du rectangle pour "Recommencer"
    restart_button.width = (
        350  # Ajuster la largeur pour s'assurer que tout le texte rentre
    )
    pygame.draw.rect(screen, WHITE, restart_button)
    draw_text(screen, "Recommencer", font, BACKGROUND_COLOR, restart_button)

    pygame.display.flip()
    wait_for_input()


# Fonction pour afficher la page de You Win
def show_you_win():
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(font_path, 36)
    draw_text(screen, "You Win Perfect", font, RED, screen.get_rect().move(0, -50))
    restart_button.width = (
        400  # Ajuster la largeur pour s'assurer que tout le texte rentre
    )
    pygame.draw.rect(screen, WHITE, quit_button)
    draw_text(screen, "Quitter", font, BACKGROUND_COLOR, quit_button)

    pygame.draw.rect(screen, WHITE, restart_button)
    draw_text(screen, "Recommencer", font, BACKGROUND_COLOR, restart_button)
    pygame.display.flip()
    wait_for_input()


# Fonction pour attendre l'entrée de l'utilisateur
def wait_for_input():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if restart_button.collidepoint(event.pos):
                    main()


# Création des groupes de sprites
def create_bricks():
    bricks = pygame.sprite.Group()
    colors = [RED, GREEN, BLUE]
    for i in range(9):  # Augmenter le nombre de colonnes
        for j in range(5):
            brick = Brick(
                i * (BRICK_WIDTH + 13) + 35,
                j * (BRICK_HEIGHT + 10) + 35,
                colors[j % len(colors)],
            )
            bricks.add(brick)
    return bricks


def main():
    global bricks, paddle, ball, all_sprites, lives
    lives = LIVES

    bricks = create_bricks()
    paddle = Paddle()
    ball = Ball()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(bricks)
    all_sprites.add(paddle)
    all_sprites.add(ball)

    # Définition des boutons
    global start_button, quit_button, restart_button
    start_button = pygame.Rect(
        (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50)
    )
    quit_button = pygame.Rect(
        (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
    )
    restart_button = pygame.Rect(
        (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 50)
    )

    # Boucle principale
    clock = pygame.time.Clock()
    game_started = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
                if start_button.collidepoint(event.pos):
                    game_started = True

        if game_started:
            all_sprites.update()

            screen.fill(BACKGROUND_COLOR)
            all_sprites.draw(screen)
            pygame.display.flip()

            clock.tick(60)
        else:
            show_instructions()


if __name__ == "__main__":
    main()
