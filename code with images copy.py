import pygame
import sys
import random
import subprocess

# ---------------- INIT ----------------
pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Fly Feast")

clock = pygame.time.Clock()

# ---------------- LOAD IMAGES ----------------
def load_image(filename):
    """Load image from intro_project/images folder."""
    path = f"images/{filename}"
    try:
        return pygame.image.load(path).convert_alpha()
    except Exception as e:
        print(f"⚠️ Failed to load {path}: {e}")
        return None

bg_img = load_image("view.png")
bee_img = load_image("bee.png")
frog_img = load_image("frog.png")  # Single frog image

# ---------------- GAME VARIABLES ----------------
bees = []
for _ in range(6):
    bees.append({
        "x": random.randint(0, SCREEN_WIDTH),
        "y": random.randint(0, SCREEN_HEIGHT),
        "speed": random.randint(2, 4)
    })

frog_x, frog_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
frog_speed = 5
FRAME_W, FRAME_H = frog_img.get_width(), frog_img.get_height() if frog_img else (64, 64)

# ---------------- GIT PUSH FUNCTION ----------------
def git_push(commit_message="Auto-update from Python"):
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Git push successful!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git push failed: {e}")

# ---------------- MAIN LOOP ----------------
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    keys = pygame.key.get_pressed()

    # FROG MOVEMENT
    if keys[pygame.K_LEFT]:
        frog_x -= frog_speed
    elif keys[pygame.K_RIGHT]:
        frog_x += frog_speed

    # DRAW
    if bg_img:
        screen.blit(bg_img, (0, 0))
    else:
        screen.fill((0, 0, 0))

    for bee in bees:
        bee["x"] += bee["speed"]
        bee["y"] += random.choice([-1, 0, 1])
        if bee["x"] > SCREEN_WIDTH:
            bee["x"] = -40
            bee["y"] = random.randint(0, SCREEN_HEIGHT)
        if bee_img:
            screen.blit(bee_img, (bee["x"], bee["y"]))
        else:
            pygame.draw.rect(screen, (255, 255, 0), (bee["x"], bee["y"], 40, 40))

    if frog_img:
        screen.blit(frog_img, (frog_x, frog_y))
    else:
        pygame.draw.rect(screen, (0, 255, 0), (frog_x, frog_y, FRAME_W, FRAME_H))

    # Keep frog on screen
    frog_x = max(0, min(frog_x, SCREEN_WIDTH - FRAME_W))
    frog_y = max(0, min(frog_y, SCREEN_HEIGHT - FRAME_H))

    pygame.display.flip()

# ---------------- CLEANUP ----------------
git_push("Auto-commit game assets and updates")
pygame.quit()
sys.exit()
