import pygame
import sys
import random
import math

pygame.init()
screen = pygame.display.set_mode((500, 540))
pygame.display.set_caption("Minesweeper")

clock = pygame.time.Clock()

in_game = True

blocks = []

choices = []

bombs = []

flags_left = 10

over = False
win = False

my_font = pygame.font.SysFont('Comic Sans MS', 40)
my_font2 = pygame.font.SysFont('Comic Sans MS', 30)
my_font3 = pygame.font.SysFont('Comic Sans MS', 35)

class Block:
  def __init__(self, size, color, x, y, hidden, bomb, count, flag):
    self.size = size
    self.color = color
    self.x = x
    self.y = y
    self.hidden = hidden
    self.bomb = bomb
    self.count = count
    self.flag = flag

  def draw(self):
    if self.hidden == False:
      pygame.draw.rect(screen, self.color, [self.x * 50, self.y * 50 + 43, self.size, self.size])
      if self.bomb == False and self.count > 0:
        display_text(str(self.count), self.x * 50 + 18, self.y * 50 + 43 + 10, (0, 0, 0), my_font)

  def blocks_to_check(self):
    for w in [[self.x+1, self.y], [self.x, self.y+1], [self.x-1, self.y], [self.x, self.y-1], [self.x+1, self.y+1], [self.x-1, self.y-1], [self.x-1, self.y+1], [self.x+1, self.y-1]]:
      for block in blocks:
        if w[0] == block.x and w[1] == block.y:
          if block.bomb == True and self.bomb == False:
            self.count += 1
    

def set_grid():
  for i in range(10):
    for j in range(10):
      blocks.append(Block(50, (47, 88, 222), i, j, True, False, 0, False))
      choices.append([i, j])

def choose_bombs():
  global option, bombs, choices, blocks
  for i in range(10):
    option = random.choice(choices)
    bombs.append(option)
    choices.remove(option)
  for bomb in bombs:
    for block in blocks:
      if bomb[0] == block.x and bomb[1] == block.y:
        block.color = (252, 194, 3)
        block.hidden = True
        block.bomb = True
      
def check_game_over():
  global over, win
  count = 0
  bomb_count = 0
  for block in blocks:
    if block.hidden == False:
      count += 1
    if block.bomb == True and block.flag == True:
      bomb_count += 1
  if count == 100 and bomb_count == 10:
    over = True
    win = True
  return [over, win]

def display_text(text, x, y, color, font):
  text = font.render(text, False, color)
  screen.blit(text, (x, y))

def check_block(mouse_position):
  global over
  block_pos = [math.floor(mouse_position[0]/50), math.floor((mouse_position[1] - 40) / 50)]
  for block in blocks:
    if block_pos[0] == block.x and block_pos[1] == block.y:
      reveal(block)
      if block.bomb == True:
        over = True
        win = False
      if block.count == 0 and block.bomb == False:
        flood_fill(block)

def reveal(block):
  if block.hidden == True:
    block.hidden = False
    block.blocks_to_check()

def flag_block(mouse_position):
  global flags_left
  block_pos = [math.floor(mouse_position[0]/50), math.floor((mouse_position[1] - 40) / 50)]
  for block in blocks:
    if block_pos[0] == block.x and block_pos[1] == block.y:
      if block.flag == False and block.hidden == True and flags_left > 0:
        block.color = (0, 204, 0)
        block.hidden = False
        block.flag = True
        flags_left -= 1
      elif block.flag == True:
        if block.bomb == True:
          block.color = (252, 194, 3)
          block.hidden = True
          block.flag = False
        else:
          block.color = (47, 88, 222)
          block.hidden = True
          block.flag = False
        flags_left += 1

def draw_grid():
  start_pos = [49, 43]
  end_pos = [49, 540]
  for i in range(9):
    pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 2)
    start_pos[0] += 50
    end_pos[0] += 50
    
  start_pos2 = [0, 92]
  end_pos2 = [500, 92]
  for i in range(9):
    pygame.draw.line(screen, (0, 0, 0), start_pos2, end_pos2, 2)
    start_pos2[1] += 50
    end_pos2[1] += 50

def flood_fill(block):
  check_places = [[block.x+1, block.y], [block.x, block.y+1], [block.x-1, block.y], [block.x, block.y-1], [block.x+1, block.y+1], [block.x-1, block.y-1], [block.x+1, block.y-1], [block.x-1, block.y+1]]
  reveal(block)
  for place in check_places:
    if place[0] >= 0 and place[0] <= 9 and place[1] >= 0 and place[1] <= 9:
      for blocked in blocks:
        if place[0] == blocked.x and place[1] == blocked.y:
          if blocked.bomb == False and blocked.hidden == True:
            reveal(blocked)
            if blocked.count == 0 and blocked.bomb == False:
              flood_fill(blocked)

def game_over(text):
  for block in blocks:
    reveal(block)
  display_text(text, 25, 250, (255, 255, 255), my_font3)

def clear_board():
  blocks.clear()
  bombs.clear()
  choices.clear()

def start():
  clear_board()
  set_grid()
  choose_bombs()
  
start()

timer = 0
time = 60     

while in_game:
  screen.fill((9, 28, 87))

  if over == False and win == False:
    time -= 1
    if time <= 0:
      timer += 1
      time = 60

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      in_game = False
    if event.type == pygame.MOUSEBUTTONDOWN:
      if pygame.mouse.get_pressed() == (1, 0, 0):
        mouse_pos = pygame.mouse.get_pos()
        check_block(mouse_pos)
      if pygame.mouse.get_pressed() == (0, 0, 1):
        mouse_pos = pygame.mouse.get_pos()
        flag_block(mouse_pos)
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_r:
        over = False
        win = False
        timer = 0
        flags_left = 10
        start()

  for block in blocks:
    if block.hidden == False:
      block.draw()

  display_text('MINESWEEPER', 155, 10, (0, 204, 0), my_font)
  display_text('Flags left: ' + str(flags_left), 5, 15, (252, 194, 3), my_font2)
  display_text('Time: ' + str(timer), 400, 15, (47, 88, 222), my_font2)
  
  draw_grid()
  
  pygame.draw.line(screen, (0, 0, 255), [0, 42], [500, 42], 2)
  
  game = check_game_over()
  if game[0] == True and game[1] == False:
    game_over("Game Over, final time was " + str(timer) + " seconds.")
  if game[1] == True and game[0] == True:
    game_over("You Win, final time was " + str(timer) + " seconds.")
  
  pygame.display.update()

  clock.tick(60)

pygame.quit()
quit()