import os
import sys
import random
import pygame
import cfg

def isGameOver(board, size):
    num_cells = size * size
    return all(board[i] == i for i in range(num_cells - 1))

def moveR(board, blank_cell_idx, num_cols):
    if blank_cell_idx % num_cols == 0:
        return blank_cell_idx
    board[blank_cell_idx - 1], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx - 1]
    return blank_cell_idx - 1

def moveL(board, blank_cell_idx, num_cols):
    if (blank_cell_idx + 1) % num_cols == 0:
        return blank_cell_idx
    board[blank_cell_idx + 1], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx + 1]
    return blank_cell_idx + 1

def moveD(board, blank_cell_idx, num_cols):
    if blank_cell_idx < num_cols:
        return blank_cell_idx
    board[blank_cell_idx - num_cols], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx - num_cols]
    return blank_cell_idx - num_cols

def moveU(board, blank_cell_idx, num_rows, num_cols):
    if blank_cell_idx >= (num_rows - 1) * num_cols:
        return blank_cell_idx
    board[blank_cell_idx + num_cols], board[blank_cell_idx] = board[blank_cell_idx], board[blank_cell_idx + num_cols]
    return blank_cell_idx + num_cols

def CreateBoard(num_rows, num_cols, num_cells):
    board = list(range(num_cells))
    blank_cell_idx = num_cells - 1
    board[blank_cell_idx] = -1
    for _ in range(cfg.RANDNUM):
        direction = random.randint(0, 3)
        if direction == 0:
            blank_cell_idx = moveL(board, blank_cell_idx, num_cols)
        elif direction == 1:
            blank_cell_idx = moveR(board, blank_cell_idx, num_cols)
        elif direction == 2:
            blank_cell_idx = moveU(board, blank_cell_idx, num_rows, num_cols)
        elif direction == 3:
            blank_cell_idx = moveD(board, blank_cell_idx, num_cols)
    return board, blank_cell_idx

def GetImagePath(rootdir):
    imagenames = os.listdir(rootdir)
    assert imagenames, "No images found in the directory"
    return os.path.join(rootdir, random.choice(imagenames))

def ShowEndInterface(screen, width, height):
    screen.fill(cfg.BACKGROUNDCOLOR)
    font = pygame.font.Font(cfg.FONTPATH, width // 15)
    title = font.render('Good Job! You Won!', True, (233, 150, 122))
    rect = title.get_rect(midtop=(width / 2, height / 2.5))
    screen.blit(title, rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        pygame.display.update()

def ShowStartInterface(screen, width, height):
    screen.fill(cfg.BACKGROUNDCOLOR)
    tfont = pygame.font.Font(cfg.FONTPATH, width // 4)
    cfont = pygame.font.Font(cfg.FONTPATH, width // 20)
    title = tfont.render(' puzzle', True, cfg.RED)
    content1 = cfont.render(' H or M or L to start the game', True, cfg.BLUE)
    content2 = cfont.render('H 5*5 , M  4*4 , L  3*3 ', True, cfg.BLUE)
    trect = title.get_rect(midtop=(width / 2, height / 10))
    crect1 = content1.get_rect(midtop=(width / 2, height / 2.2))
    crect2 = content2.get_rect(midtop=(width / 2, height / 1.8))
    screen.blit(title, trect)
    screen.blit(content1, crect1)
    screen.blit(content2, crect2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == ord('l'):
                    return 3
                elif event.key == ord('m'):
                    return 4
                elif event.key == ord('h'):
                    return 5
        pygame.display.update()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    game_img_used = pygame.image.load(GetImagePath(cfg.PICTURE_ROOT_DIR))
    game_img_used = pygame.transform.scale(game_img_used, cfg.SCREENSIZE)
    game_img_used_rect = game_img_used.get_rect()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('Puzzle')

    size = ShowStartInterface(screen, game_img_used_rect.width, game_img_used_rect.height)
    num_rows, num_cols = size, size
    num_cells = size * size
    cell_width = game_img_used_rect.width // num_cols
    cell_height = game_img_used_rect.height // num_rows

    while True:
        game_board, blank_cell_idx = CreateBoard(num_rows, num_cols, num_cells)
        if not isGameOver(game_board, size):
            break

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    blank_cell_idx = moveL(game_board, blank_cell_idx, num_cols)
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                    blank_cell_idx = moveR(game_board, blank_cell_idx, num_cols)
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    blank_cell_idx = moveU(game_board, blank_cell_idx, num_rows, num_cols)
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    blank_cell_idx = moveD(game_board, blank_cell_idx, num_cols)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                x_pos = x // cell_width
                y_pos = y // cell_height
                idx = x_pos + y_pos * num_cols
                if idx == blank_cell_idx - 1:
                    blank_cell_idx = moveR(game_board, blank_cell_idx, num_cols)
                elif idx == blank_cell_idx + 1:
                    blank_cell_idx = moveL(game_board, blank_cell_idx, num_cols)
                elif idx == blank_cell_idx + num_cols:
                    blank_cell_idx = moveU(game_board, blank_cell_idx, num_rows, num_cols)
                elif idx == blank_cell_idx - num_cols:
                    blank_cell_idx = moveD(game_board, blank_cell_idx, num_cols)

        if isGameOver(game_board, size):
            game_board[blank_cell_idx] = num_cells - 1
            is_running = False

        screen.fill(cfg.BACKGROUNDCOLOR)
        for i in range(num_cells):
            if game_board[i] == -1:
                continue
            x_pos = i // num_cols
            y_pos = i % num_cols
            rect = pygame.Rect(y_pos * cell_width, x_pos * cell_height, cell_width, cell_height)
            img_area = pygame.Rect((game_board[i] % num_cols) * cell_width, (game_board[i] // num_cols) * cell_height,
                                   cell_width, cell_height)
            screen.blit(game_img_used, rect, img_area)
        for i in range(num_cols + 1):
            pygame.draw.line(screen, cfg.BLACK, (i * cell_width, 0), (i * cell_width, game_img_used_rect.height))
        for i in range(num_rows + 1):
            pygame.draw.line(screen, cfg.BLACK, (0, i * cell_height), (game_img_used_rect.width, i * cell_height))
        pygame.display.update()
        clock.tick(cfg.FPS)

    ShowEndInterface(screen, game_img_used_rect.width, game_img_used_rect.height)

if __name__ == '__main__':
    main()
