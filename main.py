import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
GRAVITY = 1
PLAYER_SPEED = 5
JUMP_STRENGTH = -15
BULLET_SPEED = 7
SCROLL_THRESHOLD = 300  # Distance from the edge before scrolling starts

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Screen Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer with Shooting")

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.velocity_y = 0
        self.jumping = False
        self.scroll_offset_x = 0  # Track how much the screen has scrolled

    def update(self, keys, platforms):
        self.move(keys)
        self.apply_gravity()
        self.check_collision(platforms)

    def move(self, keys):
        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        # Jumping
        if not self.jumping and keys[pygame.K_UP]:
            self.jumping = True
            self.velocity_y = JUMP_STRENGTH

        # Camera Scrolling Logic
        if self.rect.right > SCREEN_WIDTH - SCROLL_THRESHOLD:
            self.scroll_offset_x -= PLAYER_SPEED
            self.rect.right = SCREEN_WIDTH - SCROLL_THRESHOLD
        if self.rect.left < SCROLL_THRESHOLD:
            self.scroll_offset_x += PLAYER_SPEED
            self.rect.left = SCROLL_THRESHOLD

    def apply_gravity(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

    def check_collision(self, platforms):
        # Move the player by gravity before checking collision
        hits = pygame.sprite.spritecollide(self, platforms, False)

        if hits:
            for platform in hits:
                # We need to ensure that the player only lands on the platform when falling from above
                if self.velocity_y > 0 and self.rect.bottom <= platform.rect.top + 10:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0  # Stop falling
                    self.jumping = False  # Allow jumping again
        else:
            # If no platform is hit, allow the player to keep falling
            self.jumping = True

# Platform Class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Bullet Class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction

    def update(self):
        self.rect.x += BULLET_SPEED * self.direction
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()  # Remove bullet when off-screen

# Game Setup
clock = pygame.time.Clock()

# Create Sprite Groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create Player and Platforms
player = Player()
ground = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH * 2, 40)  # Double the width for scrolling
platform1 = Platform(150, 450, 200, 20)
platform2 = Platform(400, 300, 200, 20)
platform3 = Platform(800, 200, 150, 20)  # Placed further for scrolling

# Add sprites to their respective groups
all_sprites.add(player)
platforms.add(ground, platform1, platform2, platform3)
all_sprites.add(ground, platform1, platform2, platform3)

# Game Loop
running = True
while running:
    clock.tick(FPS)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:  # Fire bullet with 'C' key
                direction = 1 if pygame.key.get_pressed()[pygame.K_RIGHT] else -1
                bullet = Bullet(player.rect.centerx, player.rect.centery, direction)
                all_sprites.add(bullet)
                bullets.add(bullet)

    # Update
    keys = pygame.key.get_pressed()
    player.update(keys, platforms)
    bullets.update()

    # Draw everything with offset based on player's scroll
    screen.fill(WHITE)
    
    # Offset all elements by the player's scroll offset
    for sprite in platforms:
        screen.blit(sprite.image, (sprite.rect.x + player.scroll_offset_x, sprite.rect.y))
    
    for sprite in bullets:
        screen.blit(sprite.image, (sprite.rect.x + player.scroll_offset_x, sprite.rect.y))
    
    # Draw the player at their current position
    screen.blit(player.image, player.rect.topleft)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
