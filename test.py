import pygame
import random

# 初始化
pygame.init()

# 设置游戏窗口尺寸
screen_width = 1300
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("飞机大战")

# 颜色定义
WHITE = (255, 255, 255)

# 加载图片资源
player_img = pygame.image.load("player_daoli.png")
enemy_img = pygame.image.load("xuangou.png")
bullet_img = pygame.image.load("bullet.png")
enemy_dead_img = pygame.image.load("boom.png")
player_dead_img = pygame.image.load("player_dead2.png")

# 加载字体
font = pygame.font.Font(None, 36)

# 渲染文字函数
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# 玩家飞机类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 50)
        self.speed = 5
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250  # 射击延迟（毫秒）
        self.is_dead = False  # 是否处于死亡状态
        self.dead_timer = 0  # 死亡特效显示计时器

    def update(self):
        if not self.is_dead:
            # 控制玩家飞机移动和射击逻辑
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed

            # 限制飞机移动范围
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > screen_width:
                self.rect.right = screen_width
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height

            # 射击
            now = pygame.time.get_ticks()
            if keys[pygame.K_SPACE] and now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
        else:
            # 如果处于死亡状态，显示死亡动画并控制显示时间
            self.image = player_dead_img
            self.dead_timer += 1
            if self.dead_timer > 600:
                self.kill()

    def draw(self):
        screen.blit(self.image, self.rect)

    def hit(self):
        self.is_dead = True  # 标记为死亡状态

# 敌机类
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 3)
        self.is_dead = False  # 是否处于死亡状态
        self.dead_timer = 0  # 死亡特效显示计时器

    def update(self):
        if not self.is_dead:
            self.rect.y += self.speed_y
            if self.rect.top > screen_height + 10:
                self.reset_position()
        else:
            # 如果处于死亡状态，使用死亡特效图片，并控制显示时间
            self.image = enemy_dead_img
            self.dead_timer += 1
            if self.dead_timer > 8:
                self.kill()  # 销毁对象

    def reset_position(self):
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(5, 10)
        self.is_dead = False  # 重置死亡状态
        self.dead_timer = 0  # 重置计时器

    def hit(self):
        self.is_dead = True  # 标记为死亡状态

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        # 如果子弹超出屏幕，销毁子弹
        if self.rect.bottom < 0:
            self.kill()

# 创建精灵组
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# 创建玩家飞机
player = Player()
all_sprites.add(player)

# 游戏主循环
running = True
clock = pygame.time.Clock()
game_over = False
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # 更新
        all_sprites.update()

        # 生成敌机
        if random.randrange(100) < 2:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # 碰撞检测：子弹与敌机
        hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
        for enemy in hits:
            enemy.hit()
            score += 10

        # 碰撞检测：玩家飞机与敌机
        if not player.is_dead:
            hits = pygame.sprite.spritecollide(player, enemies, False)
            if hits:
                player.hit()
                game_over = True

    # 绘制
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # 显示得分
    draw_text(f"Score: {score}", font, (255, 0, 0), screen, screen_width - 100, 50)

    if game_over:
        player.update()
        player.draw()  # 绘制死亡动画
        draw_text("I explain your dream", font, (255, 0, 0), screen, screen_width // 2, screen_height // 2)

    pygame.display.flip()

    # 控制帧率
    clock.tick(60)

pygame.quit()