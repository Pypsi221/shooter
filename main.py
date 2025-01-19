from pygame import*
from random import randint

init()

W, H = 500, 700
FPS = 60

mixer.init()
mixer.music.load('sounds/space.ogg')
mixer.music.set_volume(0.2)
mixer.music.play()

fire_snd = mixer.Sound('sounds/fire.ogg')

font.init()
font1 = font.SysFont('fonts/Bebas_Neue_Cyrillic.ttf',35, bold=True)
font2 = font.SysFont('fonts/Bebas_Neue_Cyrillic.ttf',100, bold=True)

window = display.set_mode((W, H))
display.set_caption("Shooter")

bg = transform.scale(image.load('images/galaxy.jpg'), (W, H))

clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, x, y, width, height, speed, img):
        super().__init__()
        self.width = width
        self.height = height
        self.speed = speed
        self.image = transform.scale(image.load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        # draw.rect(window, (255, 0, 0), self.rect, 2)

class Player(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < W - self.width:
            self.rect.x += self.speed


    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, 15, 20, 20 , 'images/bullet.png')
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global skipped
        self.rect.y += self.speed
        if self.rect.y > H - self.height:
            self.rect.x = randint(0, W - self.width)
            self.rect.y = 0
            skipped += 1

class Asteroid(GameSprite):
    def __init__(self, x, y, width, height, speed, img):
        super().__init__(x, y, width, height, speed, img)
        self.angle = 0
        self.original_image = self.image

    def update(self):
        self.rect.y += self.speed
        self.angle = (self.angle + 2.5) % 360
        self.image = transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.rect.y > H - self.height:
            self.rect.x = randint(0, W - self.width)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

     
player = Player(W / 2, H - 100, 50, 100, 5, 'images/rocket.png')
enemies = sprite.Group()
for i in range(5):
    enemy = Enemy(randint(0, W - 70), randint(-35, 10), 70, 35, randint(1, 3), 'images/ufo.png')
    enemies.add(enemy)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid(randint(0, W - 70), randint(-35, 10), 70, 35, randint(1, 3), 'images/asteroid.png')
    asteroids.add(asteroid)

bullets = sprite.Group()
life = 3
killed = 0
skipped = 0
game = True  
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_snd.play()
                player.fire()


    
    window.blit(bg, (0, 0))
    player.draw()
    player.move()

    enemies.draw(window)
    enemies.update()

    asteroids.draw(window)
    asteroids.update()

    bullets.draw(window)
    bullets.update()

    if sprite.groupcollide(bullets,enemies,True,True):
        killed += 1
        enemy = Enemy(randint(0, W - 70), randint(-35, 10), 70, 35, randint(1, 3), 'images/ufo.png')
        enemies.add(enemy)

    if sprite.groupcollide(bullets, asteroids, True, False):#зіткнення куль з ворогами
       pass

    if sprite.spritecollide(player, asteroids,  True):
        life -= 1
        asteroid = Asteroid(randint(0, W - 70), randint(-35, 10), 70, 35, randint(1, 3), 'images/asteroid.png')
        asteroids.add(asteroid)

    if sprite.spritecollide(player, enemies, True):
        life -= 1
        enemy = Enemy(randint(0, W - 70), randint(-35, 10), 70, 35, randint(1, 3), 'images/ufo.png')
        enemies.add(enemy)

    if life < 0:
        game = False

    skipped_txt = font1.render(f'Пропущено: {skipped}',True, (255,255,255))
    killed_txt = font1.render(f'Збито: {killed}',True, (255,255,255)) 
    life_txt = font2.render(str(life) ,True,(0,255,0)) 

    window.blit(skipped_txt,(10,10))
    window.blit(killed_txt,(10,40))
    window.blit(life_txt,(W - 50,10))


    display.update()
    clock.tick(FPS)