import pygame
import sys 
import random
import math

pygame.init()

# Οι λίστες για τις μικρές μπάλες
small_balls = []
small_ball_width = 10
small_ball_height = 10

# Διαστάσεις
# Ανάκτηση των διαστάσεων της οθόνης

window_width = 680
window_height = 650


# background image
background_img = pygame.image.load("images/galaxy.jpg")

# Διαστάσεις της εικόνας του rocket
ball_width = 80
ball_height = 120

# Χρώματα
gray = (150, 150, 150)
white = (255, 255, 255)
black = (0, 0, 0)

# Αρχικοποίηση του σκορ
score = 0
level = 1

show_level2_screen = False
level2_screen_duration = 4  # 4 δευτερόλεπτα

def move_small_balls(small_balls):
    new_small_balls = []
    for x, y, speed in small_balls:
        y -= speed
        x += speed * math.cos(math.radians(30))  # Κίνηση στην γωνία 30 μοιρών από την κατακόρυφη
        new_small_balls.append((x, y, speed))
    return new_small_balls

def nea_small_balls(small_balls):
    new_small_balls = []
    for x, y, speed in small_balls:
        y -= speed
        x += speed * math.cos(math.radians(270))  # Κίνηση στην γωνία -30 μοιρών από την κατακόρυφη
        new_small_balls.append((x, y, speed))
    return new_small_balls


# Αρχική θέση της εικόνας του rocket
ball_x = window_width // 2 - ball_width // 2
ball_y = window_height - ball_height - 35  # Λίγο πάνω από το κάτω όριο της οθόνης

# Ταχύτητα κίνησης της εικόνας του κόμητη
ball_speed = 10

# Κατεύθυνση κίνησης της εικόνας του κόμητη στον άξονα x
ball_direction = 0

# Εμπόδια
obstacles = []
obstacle_width = 100
obstacle_height = 100

# Ufos
ufos = []
ufo_width = 100
ufo_height = 100

# background image
background_img = pygame.image.load("images/galaxy.jpg")

# Φόρτωση της εικόνας του κόμητη
rocket_img = pygame.image.load("images/rocket1.png")
rocket_img = pygame.transform.scale(rocket_img, (ball_width, ball_height))

# Φόρτωση της εικόνας για τα εμπόδια
obstacle_img = pygame.image.load("images/stone.png")
obstacle_img = pygame.transform.scale(obstacle_img, (obstacle_width, obstacle_height))

# Φόρτωση της εικόνας για τα ufo
ufo_img = pygame.image.load("images/ufo.png")
ufo_img = pygame.transform.scale(ufo_img, (ufo_width, ufo_height))

def draw_obstacles():
    for obstacle in obstacles:
        screen.blit(obstacle_img, (obstacle.x, obstacle.y))

def generate_obstacle():
    x = random.randint(0, window_width - obstacle_width)
    y = 0 - obstacle_height
    obstacle = pygame.Rect(x, y, obstacle_width, obstacle_height)
    obstacles.append(obstacle)

# Δημιουργία του παραθύρου παιχνιδιού
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Rocket Game")


# Κώδικας που προσθέτει το γκρι παράθυρο
def draw_modal():
    modal_surface = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    modal_surface.fill((128, 128, 128, 128))
    screen.blit(modal_surface, (0, 0))


clock = pygame.time.Clock()


# Πιθανότητα δημιουργίας εμποδίου ανά κύκλο (αύξηση της τιμής για πιο συχνή δημιουργία)
obstacle_spawn_chance = 3  # Αυτό θέτει την πιθανότητα σε 3%

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

         # Έλεγχος των πλήκτρων που πατιούνται
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_a, pygame.K_LEFT]:
                ball_direction = -1
            elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                ball_direction = 1
            elif event.key in [pygame.K_w, pygame.K_UP]:
                # Προσθήκη μικρών μπαλών πάνω από τη μεγάλη μπάλα
                small_ball_x = ball_x + ball_width // 2 - small_ball_width // 2
                small_ball_y = ball_y
                small_ball_speed = random.randint(3, 5)
                small_balls.append((small_ball_x, small_ball_y, small_ball_speed))

        # Έλεγχος του πλήκτρου που αφήνεται
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_a, pygame.K_d, pygame.K_LEFT, pygame.K_RIGHT]:
                ball_direction = 0

    # Κίνηση της εικόνας του κόμητη μόνο στον άξονα x
    ball_x += ball_speed * ball_direction

     # Κίνηση των μικρών μπαλών προς τα πάνω και αφαίρεσή τους αν φτάσουν στο πάνω μέρος της οθόνης
    small_balls = [(x, y - speed, speed) for x, y, speed in small_balls if y > 0]

    # Έλεγχος για όρια της εικόνας του κόμητη
    if ball_x <= 0:
        ball_x = 0
    elif ball_x + ball_width >= window_width:
        ball_x = window_width - ball_width

   # Δημιουργία εμποδίων με πιθανότητα `obstacle_spawn_chance`
    if random.randint(1, 100) <= obstacle_spawn_chance:
        generate_obstacle()
    
    # Κίνηση των εμποδίων
    for obstacle in obstacles:
        obstacle.y += 5

    # Αφαίρεση εμποδίων που έχουν φτάσει στο κάτω μέρος της οθόνης
    obstacles = [obstacle for obstacle in obstacles if obstacle.y + obstacle_height <= window_height]


    # Έλεγχος αν η εικόνα του Rocket χτυπήσει εμπόδιο
    for obstacle in obstacles:
        if obstacle.colliderect(pygame.Rect(ball_x, ball_y, ball_width, ball_height)):
            # Εμφάνιση του γκρι παραθύρου (modal)
            draw_modal()

            # Δημιουργία επιφάνειας για το γκραντιέντ
            gradient_surface = pygame.Surface((window_width, window_height // 2), pygame.SRCALPHA)
            for x in range(window_width):
                color = (max(0, 255 - x), 0, 255)
                pygame.draw.line(gradient_surface, color, (x, 0), (x, window_height // 2))

            # Εφαρμογή του γκραντιέντ στο κείμενο "Game Over"
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("Game Over", True, (255, 255, 255))
            game_over_text.blit(gradient_surface, (0, 0), special_flags=pygame.BLEND_MULT)
            game_over_rect = game_over_text.get_rect(center=(window_width // 2, window_height // 2))
            screen.blit(game_over_text, game_over_rect)

            font = pygame.font.Font(None, 36)
            rematch_text = font.render("Click:", True, black)
            rematch_rect = rematch_text.get_rect(center=(window_width // 2, window_height // 2 + 50))
            screen.blit(rematch_text, rematch_rect)

            # Εμφάνιση κειμένων "Click space for rematch" και "Click enter to close the game" κάτω από το "Game Over"
            font = pygame.font.Font(None, 36)
            rematch_text = font.render("Space: to play again!", True, black)
            rematch_rect = rematch_text.get_rect(center=(window_width // 2, window_height // 2 + 80))
            screen.blit(rematch_text, rematch_rect)

            close_game_text = font.render("Enter: to end the game!", True, black)
            close_game_rect = close_game_text.get_rect(center=(window_width // 2, window_height // 2 + 110))
            screen.blit(close_game_text, close_game_rect)

            # Ενημέρωση της οθόνης
            pygame.display.update()

            # Αναμονή μέχρι ο παίκτης πατήσει το πλήκτρο space ή enter
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            # Αν ο παίκτης πατήσει space, κάνουμε reset το παιχνίδι
                            ball_x = window_width // 2 - ball_width // 2
                            ball_y = window_height - ball_height - 35
                            obstacles = []
                            small_balls = []
                            waiting_for_input = False
                        elif event.key == pygame.K_RETURN:
                            # Αν ο παίκτης πατήσει enter, τερματίζουμε το παιχνίδι
                            pygame.quit()
                            sys.exit()

    # Έλεγχος αν κάποια μικρή μπάλα χτυπήσει εμπόδιο
    for small_ball_x, small_ball_y, _ in small_balls:
        for obstacle in obstacles:
            if obstacle.colliderect(pygame.Rect(small_ball_x, small_ball_y, small_ball_width, small_ball_height)):
                # Εξαφάνιση του εμποδίου από τη λίστα των εμποδίων
                obstacles.remove(obstacle)
                # Εξαφάνιση της μικρής μπάλας από τη λίστα των μικρών μπαλών
                small_balls.remove((small_ball_x, small_ball_y, _))
                # Αύξηση του σκορ κατά 1
                score += 1
                  

    panel_width = 170
    panel_height = 90
    panel_surface = pygame.Surface((panel_width, panel_height))
    panel_surface.fill(gray)

    # Σχεδίασε μαύρα borders γύρω από τον πίνακα
    border_thickness = 5
    pygame.draw.rect(panel_surface, black, (0, 0, panel_width, border_thickness))
    pygame.draw.rect(panel_surface, black, (0, 0, border_thickness, panel_height))
    pygame.draw.rect(panel_surface, black, (0, panel_height - border_thickness, panel_width, border_thickness))
    pygame.draw.rect(panel_surface, black, (panel_width - border_thickness, 0, border_thickness, panel_height))

    # Εφαρμόστε το κείμενο score_text και level_text στον γκρι πίνακα
    font = pygame.font.Font(None, 17)  # Ορισμός του font και μεγέθους
    score_text = font.render("Score: " + str(score), True, black)

    if score <= 50:
        task1_text = font.render("1st task: Destroy 50 comets", True, black)
        # Κίνηση των μικρών μπαλών προς τα πάνω και αφαίρεσή τους αν φτάσουν στο πάνω μέρος της οθόνης
        small_balls = [(x, y - speed, speed) for x, y, speed in small_balls if y > 0]

    level_text = font.render("Level: " + str(level), True, black)
    author_text = font.render("© Klajdi Cami", True, black)
    score_rect = score_text.get_rect(topleft=(10, 10))
    task1_rect = level_text.get_rect(topleft=(10, 30))
    level_rect = level_text.get_rect(topleft=(10, 50))
    author_rect = author_text.get_rect(topleft=(10, 70))

    if 50 < score <= 100:
        level = 2
        small_ball_speed = 50
        obstacle_spawn_chance = 4  # Αυτό θέτει την πιθανότητα σε 4%
        task1_text = font.render("2st task: Destroy 50 ufo", True, black)
        small_balls = move_small_balls(small_balls)
        background_img = pygame.image.load("images/moon.jpg")
        obstacle_img = pygame.image.load("images/ufo.png")
        obstacle_width = 120
        obstacle_height = 120
        obstacle_img = pygame.transform.scale(obstacle_img, (obstacle_width, obstacle_height))
        ball_speed = 30

    if score > 100:
        level = 3
        small_ball_speed = 50
        obstacle_spawn_chance = 4  # Αυτό θέτει την πιθανότητα σε 4%
        task1_text = font.render("3st task: Destroy Robots", True, black)
        small_balls = nea_small_balls(small_balls)
        background_img = pygame.image.load("images/mars.png")
        obstacle_img = pygame.image.load("images/robots.png")
        obstacle_width = 120
        obstacle_height = 120
        obstacle_img = pygame.transform.scale(obstacle_img, (obstacle_width, obstacle_height))
        ball_speed = 30
        


    # Τοποθετήστε το κείμενο score_text και level_text στον πίνακα
    panel_surface.blit(score_text, score_rect)
    panel_surface.blit(task1_text, task1_rect)
    panel_surface.blit(level_text, level_rect)
    panel_surface.blit(author_text, author_rect)


    # Εμφάνιση των στοιχείων στην οθόνη
    screen.fill(white)
    screen.blit(background_img, (0, 0))  # Προσθέστε αυτήν τη γραμμή
    screen.blit(rocket_img, (ball_x, ball_y))
    draw_obstacles()
    for small_ball_x, small_ball_y, _ in small_balls:
        pygame.draw.rect(screen, white, (small_ball_x, small_ball_y, small_ball_width, small_ball_height))
    
    # Εμφάνιση του σκορ στην οθόνη
    screen.blit(score_text, score_rect)
    screen.blit(level_text, level_rect)
    screen.blit(panel_surface, (10, 10))

    # Ενημέρωση της οθόνης
    pygame.display.update()

    # Περιορισμός του ρυθμού ανανέωσης των καρέ
    clock.tick(60)
