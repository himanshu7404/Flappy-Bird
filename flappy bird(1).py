import pygame
from pygame import *
import random
pygame.mixer.init()
pygame.font.init()
height = 500
width = 500


def start():
    global alive,x1,x2,bird1,all_sprites,pipes,u1,l1,score
    score = 0
    alive = True
    bird1 = bird()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(bird1)
    u1 = upipe()
    all_sprites.add(u1)
    l1 = lpipe(u1.h)
    all_sprites.add(l1)
    pipes = pygame.sprite.Group()
    pipes.add(l1)
    pipes.add(u1)
    x1 = 0
    x2 = width
pipeimage = pygame.image.load("pipe-green.png")
deathsound = pygame.mixer.Sound("die.wav")
deathsound.set_volume(0.20)
wingflap = pygame.mixer.Sound("wing.wav")
screen = pygame.display.set_mode((500,500),RESIZABLE)
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
bg = pygame.image.load("background-day.png")
bg = pygame.transform.scale(bg,(width,height))
bg_rect = bg.get_rect()
birdimg = []
for i in range(1,4):
    b = pygame.image.load("bird{}.png".format(i))
    birdimg.append(b)
ic = 0
jumpcount =0
font_name = pygame.font.match_font("arial")
def write(string,x,y,size,color=(0,0,0)):
    font = pygame.font.Font(font_name,size)
    sur = font.render(string,True,color)
    rec = sur.get_rect()
    rec.centerx=x
    rec.y=y
    screen.blit(sur,rec)
class upipe(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  
        self.h = random.randint(80,height*3//5)
        self.image = pygame.transform.rotate(pygame.transform.scale(pipeimage,(width//10,self.h)),180)
        self.rect = self.image.get_rect()
        self.rect.x = width+100
        self.rect.y = 0
        
    def update(self):
        if self.rect.x > -100:
            self.rect.x-=5
        else:
            self.kill()
            u1=upipe()
            all_sprites.add(u1)
            l1 = lpipe(u1.h)
            all_sprites.add(l1)
            pipes.add(l1)
            pipes.add(u1)
class lpipe(pygame.sprite.Sprite):
    def __init__(self,h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pipeimage, (width // 10, height-h-150))
        self.rect = self.image.get_rect()
        self.rect.x = width + 100
        self.rect.y = h+150
    def update(self):
        if self.rect.x > -100:
            self.rect.x-=5
        else:
            self.kill()
class bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = birdimg[0]
        self.rect = self.image.get_rect()
        self.rect.x = width//10
        self.rect.y = height//2
        self.lives = 5
    def update(self):
        global jumpcount
        if self.rect.y<height-10:
            self.rect.y+=5
        if jumpcount>0:
            if self.rect.y>10:
                self.rect.y-=(jumpcount*jumpcount)//4
            jumpcount -= 1

run = True

pygame.mixer.music.load("pacman_beginning.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.10)
start()
while run:
    clock.tick(30)
    screen.blit(bg,(x1,0))
    screen.blit(bg,(x2,0))
    if alive:
        score += 0.03

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
        if i.type == pygame.KEYDOWN:
            if not(alive):
                start()
            if i.key == K_SPACE:
                jumpcount = 10
                wingflap.play()
        if i.type== pygame.VIDEORESIZE:
            height = i.h
            width = i.w
            x2 = width
            screen = pygame.display.set_mode((width,height),RESIZABLE)
            bg = pygame.transform.scale(bg, (width, height))
    ic +=1
    hit = pygame.sprite.spritecollide(bird1,pipes,True)
    for i in hit:
        if i:
            bird1.kill()
            u1.kill()
            l1.kill()
            alive = False
    if bird1.rect.y>height-90:
        bird1.kill()
        alive = False
    if alive == False:
        u1.kill()
        l1.kill()
        write("Game Over :(", width // 2, height // 2, 60, (255, 0, 0))
        write("Press any key to restart", width // 2, height // 1.5, 25, (255, 0, 0))
        deathsound.play()
    if x1>-width:
        x1-=1
        x2-=1
    else:
        x1 = 0
        x2 = width 
    if ic%15==0:
        bird1.image = birdimg[ic//30]
    if ic > 30:
        ic = 0
    all_sprites.draw(screen)
    all_sprites.update()
    write("Score:" + str(int(score)), width // 2, 18, 24)

    pygame.display.update()
pygame.quit()
