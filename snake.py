import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Définition des constantes
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
CELL_SIZE = 20
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (30, 30, 30)

# Initialisation de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Charger la police
font_path = "PressStart2P-Regular.ttf"
try:
    font = pygame.font.Font(font_path, 25)
except FileNotFoundError:
    print(f"Police {font_path} introuvable.")
    sys.exit()


# Classe pour la pomme
class Apple:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
            random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE,
        )

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            RED,
            pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE),
        )


# Classe pour le serpent
class Snake:
    def __init__(self):
        self.positions = [(100, 100)]
        self.direction = (0, 0)
        self.grow = False

    def set_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def move(self):
        head_x, head_y = self.positions[0]
        new_head_x = head_x + self.direction[0] * CELL_SIZE
        new_head_y = head_y + self.direction[1] * CELL_SIZE

        # Faire traverser les bords à la tête du serpent
        new_head_x = new_head_x % SCREEN_WIDTH
        new_head_y = new_head_y % SCREEN_HEIGHT

        new_head = (new_head_x, new_head_y)

        if self.grow:
            self.positions = [new_head] + self.positions
            self.grow = False
        else:
            self.positions = [new_head] + self.positions[:-1]

    def grow_snake(self):
        self.grow = True

    def draw(self, surface):
        for position in self.positions:
            pygame.draw.rect(
                surface,
                GREEN,
                pygame.Rect(position[0], position[1], CELL_SIZE, CELL_SIZE),
            )

    def collides_with_self(self):
        head = self.positions[0]
        return head in self.positions[1:]


# Fonction pour afficher le texte
def draw_text(surface, text, font, color, position):
    font_surface = font.render(text, True, color)
    surface.blit(font_surface, position)


# Fonction pour afficher la page de Game Over
def show_game_over():
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(font_path, 25)
    draw_text(
        screen,
        "Game Over",
        font,
        RED,
        (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50),
    )

    # Ajuster la taille du rectangle pour "Quitter"
    pygame.draw.rect(screen, WHITE, quit_button)
    draw_text(
        screen,
        "Quitter",
        font,
        BACKGROUND_COLOR,
        (quit_button.x + 60, quit_button.y + 10),
    )

    # Ajuster la taille du rectangle pour "Recommencer"
    restart_button.width = (
        350  # Ajuster la largeur pour s'assurer que tout le texte rentre
    )
    pygame.draw.rect(screen, WHITE, restart_button)
    draw_text(
        screen,
        "Recommencer",
        font,
        BACKGROUND_COLOR,
        (restart_button.x + 60, restart_button.y + 10),
    )

    pygame.display.flip()
    wait_for_input()


# Fonction pour afficher la page d'instructions
def show_instructions():
    screen.fill(BACKGROUND_COLOR)
    instructions = [
        "Instructions du jeu Snake:",
        "Utilisez les flèches directionnelles pour déplacer le serpent.",
        "Le but du jeu est de manger les pommes rouges pour grandir.",
        "Le jeu se termine si le serpent se mord lui-même.",
        "Appuyez sur le bouton Commencer pour débuter le jeu.",
    ]
    for i, line in enumerate(instructions):
        draw_text(
            screen, line, pygame.font.Font(font_path, 15), WHITE, (100, 60 + i * 40)
        )
    pygame.draw.rect(screen, WHITE, start_button)
    start_button.width = 350
    draw_text(
        screen,
        "Commencer",
        font,
        (30, 30, 30),
        (start_button.x + 60, start_button.y + 10),
    )
    pygame.display.flip()


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
                if start_button.collidepoint(event.pos):
                    return  # Sortir de la boucle pour démarrer le jeu


# Fonction principale
def main():
    snake = Snake()
    apple = Apple()
    clock = pygame.time.Clock()
    score = 0

    # Définition des boutons
    global quit_button, restart_button, start_button
    quit_button = pygame.Rect(
        (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
    )
    restart_button = pygame.Rect(
        (SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 + 150, 350, 50)
    )
    start_button = pygame.Rect(
        (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)
    )

    show_instructions()
    wait_for_input()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.set_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.set_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.set_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.set_direction((1, 0))

        snake.move()

        if snake.positions[0] == apple.position:
            snake.grow_snake()
            apple.randomize_position()
            score += 1

        if snake.collides_with_self():
            show_game_over()
            break

        screen.fill(BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        draw_text(
            screen, f"Score: {score}", font, WHITE, (100, 30)
        )  # Ajuster la position du texte "Score"
        pygame.display.flip()

        # Ajuster la vitesse proportionnellement à la longueur du serpent
        speed = min(30, 5 + len(snake.positions) // 2)
        clock.tick(speed)


if __name__ == "__main__":
    main()
