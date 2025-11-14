import pygame
import random
import math
import sys
#Initialize
pygame.init()
SCREEN=pygame.display.set_mode((500,600))
clock=pygame.time.Clock()
FPS=60
FONT=pygame.font.SysFont("comicsans",20)
pygame.display.set_caption("Fruit Catcher")
#Load assets
BASKET=pygame.image.load(r"C:\Users\shaji\OneDrive\Desktop\Afri\Python\PyGame\basket.jpg")
CLOUD=pygame.image.load(r"C:\Users\shaji\OneDrive\Desktop\Afri\Python\PyGame\cloud.jpg")
FRUIT_TYPES=[
    ("apple",pygame.image.load(r"C:\Users\shaji\OneDrive\Desktop\Afri\Python\PyGame\apple.jpg"),1),
    ("banana",pygame.image.load(r"C:\Users\shaji\OneDrive\Desktop\Afri\Python\PyGame\banana.jpg"),3),
    ("lemon",pygame.image.load(r"C:\Users\shaji\OneDrive\Desktop\Afri\Python\PyGame\lemon.jpg"),-1),
    ("grape",pygame.image.load(r"C:\Users\shaji\OneDrive\Desktop\Afri\Python\PyGame\grape.jpg"),5),
    ("strawberry",pygame.image.load(r"C:\Users\shaji\OneDrive\Desktop\Afri\Python\PyGame\strawberry.jpg"),7),
    ("watermelon",pygame.image.load(r"C:\Users\shaji\OneDrive\Desktop\Afri\Python\PyGame\watermelon.jpg"),10)
]
#Rarity weights
RARITY_WEIGHTS={
    "apple":40,
    "banana":25,
    "lemon":15,
    "grape":10,
    "strawberry":7,
    "watermelon":3
}
def weighted_random_fruit():
    fruits=[f[0] for f in FRUIT_TYPES]
    weights=[RARITY_WEIGHTS[f[0]] for f in FRUIT_TYPES]
    selected_name=random.choices(fruits,weights=weights,k=1)[0]
    for name,img,points in FRUIT_TYPES:
        if name == selected_name:
            return name,img,points
#Cloud positions
def generate_clouds():
    CLOUD_TOP=40
    CLOUD_BOTTOM=500-10
    return [(random.randint(0,500),random.randint(CLOUD_TOP,CLOUD_BOTTOM)) for _ in range(100)]
class Fruit:
    def __init__(self):
        self.reset()
    def reset(self):
        self.name,self.image,self.points=weighted_random_fruit()
        self.x=random.randint(0,450)
        self.y=random.randint(-600,-50)
        self.speed=random.uniform(2,4)
    def fall(self):
        self.y+=self.speed
        if self.y > 600:
            self.reset()
    def draw(self):
        SCREEN.blit(self.image,(self.x,self.y))
    def check_collision(self,basket_x,basket_y):
        distance=math.hypot((self.x - basket_x),(self.y - basket_y))
        return distance < 50
def game_loop():
    BASKETX,BASKETY=200,500
    score=0
    watermelon_count=0
    cloud_positions=generate_clouds()
    fruits=[Fruit() for _ in range(7)]
    running=True
    game_over_reason=""
    while running:
        SCREEN.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if watermelon_count>=5:
            game_over_reason="Caught 5 watermelons!"
            break
        #Draw clouds
        for pos in cloud_positions:
            SCREEN.blit(CLOUD,pos)
        #Basket movement
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and BASKETX>0:
            BASKETX-=5
        if keys[pygame.K_RIGHT] and BASKETX < 450:
            BASKETX+=5
        #Draw basket
        SCREEN.blit(BASKET,(BASKETX,BASKETY))
        #Update fruits
        for fruit in fruits:
            fruit.fall()
            fruit.draw()
            if fruit.check_collision(BASKETX+25,BASKETY+25):
                score+=fruit.points
                if fruit.name=="watermelon":
                    watermelon_count+=1
                fruit.reset()
        #Score
        #Display Score and Watermelon Count
        score_render=FONT.render(f"Score: {score}",True,(0,0,0))
        watermelon_render=FONT.render(f"Watermelons: {watermelon_count}/5",True,(255,0,0))
        SCREEN.blit(score_render,(10,10))
        SCREEN.blit(watermelon_render,(330,10))
        pygame.display.update()
        clock.tick(FPS)
    return score,game_over_reason
def show_game_over(score,reason):
    while True:
        SCREEN.fill((255,255,255))
        msg1=FONT.render(f"Game Over: {reason}",True,(255,0,0))
        msg2=FONT.render(f"Final Score: {score}",True,(0,0,0))
        restart_text=FONT.render("Click to Restart",True,(0,100,255))
        SCREEN.blit(msg1,(150,250))
        SCREEN.blit(msg2,(180,280))
        SCREEN.blit(restart_text,(165,320))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return  #Restart
#Main game cycle
while True:
    final_score,reason=game_loop()
    show_game_over(final_score,reason)
