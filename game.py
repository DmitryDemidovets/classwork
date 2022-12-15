import pygame
import time
import random
 
# инициализация модулей pygame
pygame.init()
 
# настройки окна игры
display_width = 800
display_height = 600
# окно игры
game_display = pygame.display.set_mode((display_width, display_height))
# имя игры сверху в окошке
pygame.display.set_caption("Ride game") 
 
# цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
 
# мониторинг времени
clock = pygame.time.Clock()
 
# авария да/нет
crashed = False 
# машина
carImg = pygame.image.load('imgs/car.png')
# размер картинки, если очень большая
carImg = pygame.transform.scale(carImg, (90, 100))
 
# машина (картинка + ось вверх, ось вбок)
def car(x, y):
    game_display.blit(carImg, (x, y))
 
# падающие предметы
def things(thing_x, thing_y, thing_w, thing_h, color):
    pygame.draw.rect(game_display, color, [thing_x, thing_y, thing_w, thing_h])
 
# счетчик падающих предметов, которые мы проехали
def things_dodget(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " + str(count), True, black)
    game_display.blit(text, (0, 0))
 
# функция вывода текста
def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()
 
# украшение текста
def message_display(text):
    # шрифт
    large_text = pygame.font.Font('freesansbold.ttf', 40)
    # текст и его блок
    text_surf, text_rect = text_objects(text, large_text)
    # позиция
    text_rect.center = ((display_width / 2), (display_height / 2))
    # рисуем на экране текст
    game_display.blit(text_surf, text_rect)
    # обновление экрана
    pygame.display.update()
    # спим 2 секунды, чтобы успеть прочитать надпись
    time.sleep(2)
    # запускаем игру с нуля
    game_loop()
 
# функция сработает при аварии, на экране будет текст
def crash():
    message_display('CRASHED! TRY AGAIN?')
 
# параметры машины
car_speed = 0
car_width = 73
 
# игровой цикл (условия игры, обработчики нажатий)
def game_loop():
    # оси для размещения машины
    x = (display_width * 0.45)
    y = (display_height * 0.8)
 
    # смещение по оси X
    x_change = 0 
    # стартовое значение пропущенных падающих предметов
    dodged = 0
 
    game_exit = False
 
    # настройки падающих предметов
    # стартовая позиция падающего предмета по оси икс
    thing_start_x = random.randrange(0, display_width)
    # стартовая по оси y
    thing_start_y = -600
    # скорость
    thing_speed = 5
    # высота
    thing_width = 100
    # ширина
    thing_height = 100
 
 
 
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
                pygame.quit()
                quit()
 
            # управление 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
 
        # изменяемая позиция по x
        x += x_change
 
        # фон игры
        game_display.fill(white)
 
        # создаем падающие предметы
        things(thing_start_x, thing_start_y, thing_width, thing_height, black)
        # ускорение падающих предметов
        thing_start_y += thing_speed
        # создаем машину и наполняем данными
        car(x,y)
        # счетчик
        things_dodget(dodged)
 
        # обработчики условий для конца игры
        # если заехали за края - конец игры
 
        if x > display_width - car_width or x < 0:
            crash()
            game_loop()
 
        # если влетел в предмет - конец игры
        if y < thing_start_y + thing_height:
            if x > thing_start_x and x < thing_start_x + thing_width or x + car_width > thing_start_x and x + car_width < thing_start_x + thing_width:
                crash()
                game_loop()
        
        # предметы в пределах экрана
        if thing_start_y > display_height:
            thing_start_y = 0 - thing_height
            thing_start_x = random.randrange(0, display_width)
            dodged += 1
            thing_speed += 0.5
            thing_width += (dodged * 2)
 
        pygame.display.update()
        clock.tick(60)
 
game_loop()
pygame.quit()
quit()
