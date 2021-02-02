import pygame
import random


pygame.init()

display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Код для копирки')

pygame.mixer.music.load('background.mp3')
pygame.mixer.music.set_volume(0.5)  # громкость звука 1 - 100%

jump_sound = pygame.mixer.Sound('Rrr.wav')
fall_sound = pygame.mixer.Sound('Bdish.wav')
lose_sound = pygame.mixer.Sound('loss.wav')
heart_plus_sound = pygame.mixer.Sound('hp+.wav')


icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

cactus_img = [pygame.image.load('Cactus0.png'), pygame.image.load('Cactus1.png'), pygame.image.load('Cactus2.png')]
cactus_option = [69, 449, 37, 410, 40, 420]


stone_img = [pygame.image.load('Stone0.png'), pygame.image.load('Stone1.png')]
cloud_img = [pygame.image.load('Cloud0.png'), pygame.image.load('Cloud1.png')]

dino_img = [pygame.image.load('Dino0.png'), pygame.image.load('Dino1.png'),
            pygame.image.load('Dino2.png'), pygame.image.load('Dino3.png'), pygame.image.load('Dino4.png')]

health_image = pygame.image.load('heart.png')
health_image = pygame.transform.scale(health_image, (30, 30))

img_counter = 0
health = 2


class Object:
    def __init__(self, x, y, width, speed, image):
        self.x = x
        self.y = y
        self.width = width
        self.speed = speed
        self.image = image

    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            self.x = display_width + 50 + random.randrange(-80, 60)
            return False

    def return_self(self, radius, y, width, image):
        self.y = y
        self.width = width
        self.image = image
        self.x = radius
        display.blit(self.image, (self.x, self.y))


class Button:
    def __init__(self, width, height, inactive_color, active_color):
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color


usr_width = 60
usr_height = 100
usr_x = display_width // 3
usr_y = display_height - usr_height - 100

cactus_width = 20
cactus_height = 70
cactus_x = display_width - 50
cactus_y = display_height - cactus_height - 100

clock = pygame.time.Clock()

make_jump = False
jump_counter = 30

scores = 0


def run_game():
    global make_jump

    pygame.mixer.music.play(-1)  # Если хотим чтобы музыка играла всю игру -1, если 1 раз, то 1

    game = True
    cactus_arr = []
    create_cactus_arr(cactus_arr)
    land = pygame.image.load('Land.jpg')

    stone, cloud = open_random_objects()
    heart = Object(display_width, 280, 30, 4, health_image)

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            make_jump = True

        count_scores(cactus_arr)

        display.blit(land, (0, 0))
        print_text('Scores: ' + str(scores), 600, 10)

        draw_array(cactus_arr)
        move_obects(stone, cloud)

        draw_dino()

        if keys[pygame.K_ESCAPE]:
            pause()

        heart.move()
        hearts_plus(heart)

        if make_jump:
            jump()

        if check_collision(cactus_arr):
            # pygame.mixer.music.stop()
            # pygame.mixer.Sound.play(fall_sound)
            # if not check_health():
            game = False

        show_health()

        pygame.display.update()
        clock.tick(80)

    return game_over()


def jump():
    global usr_y, jump_counter, make_jump
    if jump_counter >= -30:
        if jump_counter == 30:
            pygame.mixer.Sound.play(jump_sound)
        if jump_counter == -30:
            pygame.mixer.Sound.play(fall_sound)

        usr_y -= jump_counter / 2.5
        jump_counter -= 1
    else:
        jump_counter = 30
        make_jump = False


def create_cactus_arr(array):
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_option[choice * 2]
    height = cactus_option[choice * 2 + 1]
    array.append(Object(display_width + 20, height, width, 4, img))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_option[choice * 2]
    height = cactus_option[choice * 2 + 1]
    array.append(Object(display_width + 300, height, width, 4, img))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_option[choice * 2]
    height = cactus_option[choice * 2 + 1]
    array.append(Object(display_width + 600, height, width, 4, img))


def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)

    if maximum < display_width:
        radius = display_width
        if radius - maximum < 50:
            radius += 280
    else:
        radius = maximum

    choise = random.randrange(0, 5)
    if choise == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(250, 400)

    return radius


def draw_array(array):
    for cactus in array:
        check = cactus.move()
        if not check:
            object_return(array, cactus)
            radius = find_radius(array)

            choice = random.randrange(0, 3)
            img = cactus_img[choice]
            width = cactus_option[choice * 2]
            height = cactus_option[choice * 2 + 1]

            cactus.return_self(radius, height, width, img)


def object_return(objects, obj):
    radius = find_radius(objects)

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_option[choice * 2]
    height = cactus_option[choice * 2 + 1]

    obj.return_self(radius, height, width, img)


def open_random_objects():
    choice = random.randrange(0, 2)
    img_of_stone = stone_img[choice]

    choice = random.randrange(0, 2)
    img_of_cloud = cloud_img[choice]

    stone = Object(display_width, display_height - 80, 10, 4, img_of_stone)
    cloud = Object(display_width, 80, 70, 2, img_of_cloud)

    return stone, cloud


def move_obects(stone, cloud):
    check = stone.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_stone = stone_img[choice]
        stone.return_self(display_width, 500 + random.randrange(10, 80), stone.width, img_of_stone)

    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]
        cloud.return_self(display_width, random.randrange(10, 200), cloud.width, img_of_cloud)


def draw_dino():
    global img_counter
    if img_counter == 25:
        img_counter = 0

    display.blit(dino_img[img_counter // 5], (usr_x, usr_y))
    img_counter += 1


def print_text(message, x, y, font_color=(0, 0, 0), font_type='PingPong.ttf', font_size = 30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
    paused = True

    pygame.mixer.music.pause()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Paused. Press enter to continue.', 160, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(15)

    pygame.mixer.music.unpause()


def check_collision(barriers):  # проверка на то, персонаж ли игрок с кактусом, или нет
    for barrier in barriers:  # проходимся по всем препятствиям, через которые должен перепрыгнуть игрок
        if barrier.y == 449:  # маленький кактус
            if not make_jump:  # если не делаем прыжок
                if barrier.x <= usr_x + usr_width - 22 <= barrier.x + barrier.width:  # если выполняется это условие
                    if check_health():
                        object_return(barriers, barrier)
                    else:
                        return True

            elif jump_counter >= 0:  # если прыжок начинает возрастать. 1 часть параболы
                if usr_y + usr_height - 5 >= barrier.y:  # проверяем координаты по у
                    if barrier.x <= usr_x + usr_width - 22 <= barrier.x + barrier.width:  # проверка правой координаты
                        if check_health():
                            object_return(barriers, barrier)
                        else:
                            return True
            else:  # если же вторая часть прыжка
                if usr_y + usr_height - 10 >= barrier.y:  # проверяем координаты по у
                    if barrier.x <= usr_x <= barrier.x + barrier.width:  # проверка правой координаты
                        if check_health():
                            object_return(barriers, barrier)
                        else:
                            return True
        else:  # если не маленький кактус
            if not make_jump:  # если не делаем прыжок
                if barrier.x <= usr_x + usr_width + 5 <= barrier.x + barrier.width:  # если выполняется это условие
                    if check_health():
                        object_return(barriers, barrier)
                        return False
                    else:
                        return True
            elif jump_counter == 10:  # начало прыжка
                if usr_y + usr_height - 2 >= barrier.y:  # если есть столкновение по координате y
                    if barrier.x <= usr_x + 13 <= barrier.x + barrier.width:  # Если столкнулись
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
            elif jump_counter <= 1:  # до того момента, как динозавр начнет падать вниз
                if usr_y + usr_height - 2 >= barrier.y:  # столкновение по у
                    if barrier.x <= usr_x + usr_width + 13 <= barrier.x + barrier.width:  # по х координате
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
            elif jump_counter >= 1: # игрок совершает 2 часть прыжка
                if usr_y + usr_height - 2 >= barrier.y: # столкновение по у
                    if barrier.x <= usr_x + usr_width - 22 <= barrier.x + barrier.width:  # по х координате
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
            else:
                if usr_y + usr_height - 3 >= barrier.y:  # проверяем координаты по у
                    if barrier.x <= usr_x + usr_width + 5 <= barrier.x + barrier.width:  # проверка правой координаты
                        if check_health():
                            object_return(barriers, barrier)
                            return False
                        else:
                            return True
    return False  # если же ничего не произошло, то возвращаем false, т.е ничего не было


def count_scores(cactus_arr):
    global scores
    for cactus in cactus_arr:
        if cactus.x - 2 <= usr_x <= cactus.x + 1:
            scores += 1



def game_over():
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Game over. Press enter to play again, Esc to exit.', 40, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True

        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        clock.tick(15)


def show_health():
    global health
    show = 0
    x = 20
    while show != health:
        display.blit(health_image, (x, 20))
        x += 40
        show += 1


def check_health():
    global health
    health -= 1
    if health == 0:
        pygame.mixer.Sound.play(lose_sound)
        return False
    else:
        pygame.mixer.Sound.play(fall_sound)
        return True


def hearts_plus(heart):
    global health, usr_x, usr_y, usr_width, usr_height

    if heart.x <= -heart.width:
        radius = display_width + random.randrange(1000, 3000)
        heart.return_self(radius, heart.y, heart.width, heart.image)

    if usr_x <= heart.x <= usr_x + usr_width:
        if usr_y <= heart.y <= usr_y + usr_height:
            pygame.mixer.Sound.play(heart_plus_sound)
            if health < 5:
                health += 1

            radius = display_width + random.randrange(1000, 3000)
            heart.return_self(radius, heart.y, heart.width, heart.image)


while run_game():
    scores = 0
    make_jump = False
    jump_counter = 30
    usr_y = display_height - usr_height - 100
    health = 2
pygame.quit()
quit()

print('фиг его')
