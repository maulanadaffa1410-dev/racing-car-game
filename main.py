import random
import pygame

pygame.init()
pygame.font.init()

TRUCK_IMAGE_PATH = r"C:\Users\user\OneDrive\Pictures\Screenshots\Image20260910190209.png"
truck_image = None
try:
    truck_image = pygame.image.load(TRUCK_IMAGE_PATH).convert_alpha()
except pygame.error:
    truck_image = None

WIDTH, HEIGHT = 480, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Car")
clock = pygame.time.Clock()
FPS = 60

font = pygame.font.SysFont(None, 32)
large_font = pygame.font.SysFont(None, 64)
small_font = pygame.font.SysFont(None, 24)

ROAD_X = 80
ROAD_WIDTH = 320
LANE_WIDTH = ROAD_WIDTH / 3
PLAYER_W = 50
PLAYER_H = 90
PLAYER_Y = HEIGHT - 120
PLAYER_SPEED = 360

state = "menu"
level = 1
score = 0
spawn_timer = 0.0
road_scroll = 0.0
shoot_cooldown = 0.0
player_x = ROAD_X + (ROAD_WIDTH / 2) - (PLAYER_W / 2)
obstacles = []
projectiles = []


def reset_game():
    global level, score, spawn_timer, road_scroll, shoot_cooldown, player_x, obstacles, projectiles
    level = 1
    score = 0
    spawn_timer = 0.8
    road_scroll = 0.0
    shoot_cooldown = 0.0
    player_x = ROAD_X + (ROAD_WIDTH / 2) - (PLAYER_W / 2)
    obstacles = []
    projectiles = []


def start_game():
    global state
    reset_game()
    state = "playing"


def add_obstacle():
    global obstacles
    lane = random.randint(0, 2)
    is_truck = random.random() < 0.28
    obstacle_w = 72 if is_truck else 52
    obstacle_h = 120 if is_truck else 90
    obstacle_x = ROAD_X + (lane * LANE_WIDTH) + ((LANE_WIDTH - obstacle_w) / 2)
    obstacle_speed = 200 + (level * 30) + random.randint(0, 60)
    direction = random.choice([-1, 1])
    color = random.choice([
        (255, 80, 80),
        (80, 180, 255),
        (255, 200, 80),
        (120, 220, 120),
        (255, 128, 191),
    ])
    obstacles.append({
        "x": obstacle_x,
        "y": -obstacle_h,
        "w": obstacle_w,
        "h": obstacle_h,
        "speed": obstacle_speed,
        "color": color,
        "direction": direction,
        "lane_shift_speed": random.uniform(30, 70),
        "is_truck": is_truck,
    })


def add_police_car():
    global obstacles
    lane = random.randint(0, 2)
    obstacle_w = 52
    obstacle_h = 90
    obstacle_x = ROAD_X + (lane * LANE_WIDTH) + ((LANE_WIDTH - obstacle_w) / 2)
    obstacle_speed = 250 + (level * 40)
    obstacles.append({
        "x": obstacle_x,
        "y": -obstacle_h,
        "w": obstacle_w,
        "h": obstacle_h,
        "speed": obstacle_speed,
        "color": (0, 100, 255),
        "direction": 0,
        "lane_shift_speed": random.uniform(80, 120),
        "is_truck": False,
        "is_police": True,
    })


def draw_car(x, y, w, h, color, is_truck=False, is_police=False):
    if is_police:
        # Draw police car with blue and white
        pygame.draw.rect(screen, (0, 100, 255), (x, y, w, h), border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), (x + 8, y + 14, w - 16, h // 2 - 10), border_radius=8)
        pygame.draw.rect(screen, (30, 30, 30), (x + 6, y + 8, 8, 18))
        pygame.draw.rect(screen, (30, 30, 30), (x + w - 14, y + 8, 8, 18))
        pygame.draw.rect(screen, (30, 30, 30), (x + 6, y + h - 26, 8, 18))
        pygame.draw.rect(screen, (30, 30, 30), (x + w - 14, y + h - 26, 8, 18))
        # Police light on top
        pygame.draw.circle(screen, (255, 0, 0), (int(x + w // 2), int(y + 8)), 5)
        pygame.draw.circle(screen, (255, 255, 255), (int(x + w // 2), int(y + 8)), 4)
        return
    
    if is_truck:
        if truck_image is not None:
            scaled_truck = pygame.transform.smoothscale(truck_image, (w, h))
            screen.blit(scaled_truck, (x, y))
            return
        pygame.draw.rect(screen, color, (x, y, w, h), border_radius=16)
        pygame.draw.rect(screen, (230, 230, 230), (x + 10, y + 18, w - 20, h // 2 - 18), border_radius=8)
        pygame.draw.rect(screen, (35, 35, 35), (x + 8, y + 8, 10, 24))
        pygame.draw.rect(screen, (35, 35, 35), (x + w - 18, y + 8, 10, 24))
        pygame.draw.rect(screen, (35, 35, 35), (x + 8, y + h - 32, 10, 24))
        pygame.draw.rect(screen, (35, 35, 35), (x + w - 18, y + h - 32, 10, 24))
        pygame.draw.rect(screen, (90, 90, 90), (x + 20, y + h - 8, w - 40, 8), border_radius=4)
        return

    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=12)
    pygame.draw.rect(screen, (220, 220, 220), (x + 8, y + 14, w - 16, h // 2 - 10), border_radius=8)
    pygame.draw.rect(screen, (30, 30, 30), (x + 6, y + 8, 8, 18))
    pygame.draw.rect(screen, (30, 30, 30), (x + w - 14, y + 8, 8, 18))
    pygame.draw.rect(screen, (30, 30, 30), (x + 6, y + h - 26, 8, 18))
    pygame.draw.rect(screen, (30, 30, 30), (x + w - 14, y + h - 26, 8, 18))


def draw_road():
    screen.fill((40, 120, 40))
    pygame.draw.rect(screen, (45, 45, 45), (ROAD_X, 0, ROAD_WIDTH, HEIGHT))
    pygame.draw.rect(screen, (65, 65, 65), (ROAD_X + 8, 0, ROAD_WIDTH - 16, HEIGHT))

    for lane in range(1, 3):
        line_x = ROAD_X + lane * LANE_WIDTH
        for y in range(-30 + int(road_scroll), HEIGHT + 30, 40):
            pygame.draw.rect(screen, (255, 255, 255), (line_x - 4, y, 8, 24), border_radius=4)


def draw_ui():
    score_text = font.render(f"Score: {int(score)}", True, (255, 255, 255))
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(score_text, (18, 18))
    screen.blit(level_text, (WIDTH - 120, 18))


def draw_start_screen():
    draw_road()
    draw_car(player_x, PLAYER_Y, PLAYER_W, PLAYER_H, (80, 120, 255))

    title = large_font.render("RACING CAR", True, (255, 255, 255))
    title_rect = title.get_rect(center=(WIDTH // 2, 150))
    screen.blit(title, title_rect)

    prompt = font.render("Tekan R untuk mulai", True, (255, 255, 255))
    prompt_rect = prompt.get_rect(center=(WIDTH // 2, 240))
    screen.blit(prompt, prompt_rect)

    controls = small_font.render("Gunakan <- -> atau A/D untuk bergerak, Spasi untuk menembak", True, (230, 230, 230))
    controls_rect = controls.get_rect(center=(WIDTH // 2, 290))
    screen.blit(controls, controls_rect)


def draw_game_over_screen():
    draw_road()
    for obstacle in obstacles:
        draw_car(obstacle["x"], obstacle["y"], obstacle["w"], obstacle["h"], obstacle["color"], obstacle.get("is_truck", False), obstacle.get("is_police", False))
    draw_car(player_x, PLAYER_Y, PLAYER_W, PLAYER_H, (80, 120, 255))

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    game_over = large_font.render("Game Over", True, (255, 90, 90))
    game_over_rect = game_over.get_rect(center=(WIDTH // 2, 180))
    screen.blit(game_over, game_over_rect)

    score_text = font.render(f"Score: {int(score)}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WIDTH // 2, 250))
    screen.blit(score_text, score_rect)

    restart = font.render("Tekan R untuk memulai lagi", True, (255, 255, 255))
    restart_rect = restart.get_rect(center=(WIDTH // 2, 300))
    screen.blit(restart, restart_rect)


def draw_projectiles():
    for bullet in projectiles:
        pygame.draw.rect(screen, (255, 220, 80), (bullet["x"], bullet["y"], bullet["w"], bullet["h"]), border_radius=4)
        pygame.draw.rect(screen, (255, 140, 40), (bullet["x"] + 2, bullet["y"], bullet["w"] - 4, bullet["h"] // 2), border_radius=3)


def update_game(delta_time):
    global level, score, spawn_timer, state, player_x, road_scroll, shoot_cooldown, projectiles

    road_scroll += (220 + level * 45) * delta_time
    if road_scroll > 40:
        road_scroll -= 40

    if shoot_cooldown > 0:
        shoot_cooldown -= delta_time

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= PLAYER_SPEED * delta_time
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += PLAYER_SPEED * delta_time
    if keys[pygame.K_SPACE] and shoot_cooldown <= 0:
        projectiles.append({
            "x": player_x + PLAYER_W / 2 - 4,
            "y": PLAYER_Y - 18,
            "w": 8,
            "h": 18,
            "speed": 520,
        })
        add_police_car()
        shoot_cooldown = 0.28

    player_x = max(ROAD_X + 12, min(ROAD_X + ROAD_WIDTH - PLAYER_W - 12, player_x))

    for bullet in projectiles:
        bullet["y"] -= bullet["speed"] * delta_time

    projectiles[:] = [bullet for bullet in projectiles if bullet["y"] + bullet["h"] > -20]

    spawn_timer -= delta_time
    if spawn_timer <= 0:
        add_obstacle()
        spawn_timer = max(0.45, 1.2 - (level * 0.12)) + random.uniform(0.05, 0.5)

    for obstacle in obstacles:
        if obstacle.get("is_police"):
            # Police car chases the player
            player_center = player_x + PLAYER_W / 2
            police_center = obstacle["x"] + obstacle["w"] / 2
            
            if player_center > police_center + 5:
                obstacle["x"] += obstacle["lane_shift_speed"] * delta_time
            elif player_center < police_center - 5:
                obstacle["x"] -= obstacle["lane_shift_speed"] * delta_time
        else:
            # Regular obstacle movement
            obstacle["x"] += obstacle["direction"] * obstacle["lane_shift_speed"] * delta_time
            
            if obstacle["x"] <= ROAD_X + 10:
                obstacle["x"] = ROAD_X + 10
                obstacle["direction"] = 1
            elif obstacle["x"] + obstacle["w"] >= ROAD_X + ROAD_WIDTH - 10:
                obstacle["x"] = ROAD_X + ROAD_WIDTH - obstacle["w"] - 10
                obstacle["direction"] = -1

            if random.random() < 0.008:
                obstacle["direction"] *= -1
        
        # All obstacles move down
        obstacle["y"] += obstacle["speed"] * delta_time
        
        # Keep within road boundaries
        if obstacle["x"] <= ROAD_X + 10:
            obstacle["x"] = ROAD_X + 10
        elif obstacle["x"] + obstacle["w"] >= ROAD_X + ROAD_WIDTH - 10:
            obstacle["x"] = ROAD_X + ROAD_WIDTH - obstacle["w"] - 10

    for bullet in projectiles[:]:
        bullet_rect = pygame.Rect(bullet["x"], bullet["y"], bullet["w"], bullet["h"])
        for obstacle in obstacles[:]:
            obstacle_rect = pygame.Rect(obstacle["x"], obstacle["y"], obstacle["w"], obstacle["h"])
            if bullet_rect.colliderect(obstacle_rect):
                if obstacle.get("is_truck"):
                    if random.random() < 0.5:
                        obstacles.remove(obstacle)
                        projectiles.remove(bullet)
                        score += 250
                        break
                    else:
                        projectiles.remove(bullet)
                        break
                obstacles.remove(obstacle)
                projectiles.remove(bullet)
                score += 150
                break

    obstacles[:] = [obs for obs in obstacles if obs["y"] < HEIGHT + obs["h"]]

    player_rect = pygame.Rect(player_x, PLAYER_Y, PLAYER_W, PLAYER_H)
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle["x"], obstacle["y"], obstacle["w"], obstacle["h"])
        if player_rect.colliderect(obstacle_rect):
            state = "game_over"
            break

    score += delta_time * 38 * level
    if score >= 1200 and level == 1:
        level = 2
    elif score >= 3000 and level == 2:
        level = 3


running = True
while running:
    delta_time = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if state in ("menu", "game_over"):
                    start_game()

    if state == "playing":
        update_game(delta_time)

    screen.fill((0, 0, 0))

    if state == "menu":
        draw_start_screen()
    elif state == "playing":
        draw_road()
        for obstacle in obstacles:
            draw_car(obstacle["x"], obstacle["y"], obstacle["w"], obstacle["h"], obstacle["color"], obstacle.get("is_truck", False), obstacle.get("is_police", False))
        draw_projectiles()
        draw_car(player_x, PLAYER_Y, PLAYER_W, PLAYER_H, (80, 120, 255))
        draw_ui()
    elif state == "game_over":
        draw_game_over_screen()

    pygame.display.flip()

pygame.quit()
quit()