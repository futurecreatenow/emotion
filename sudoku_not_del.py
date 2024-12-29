import pygame

# 画面の設定
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 550  # 数字ボタン分高さを増やす
CELL_SIZE = 50
BUTTON_SIZE = 30
BUTTON_POS = (SCREEN_WIDTH + 50, 50)

# 色の設定
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)  # 選択中のマスをハイライトする色

# フォントの設定
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 36)

# 数独の盤面を格納する2次元配列
board = [[0 for _ in range(9)] for _ in range(9)]
locked_board = [[False for _ in range(9)] for _ in range(9)]  # 各マスのロック状態を管理する配列

# 選択中のマスの座標
selected_row = -1
selected_col = -1

# 数字削除ボタンの座標とサイズ
DELETE_BUTTON_POS = (SCREEN_WIDTH + 50, BUTTON_POS[1] + 9 * BUTTON_SIZE + 20)
DELETE_BUTTON_SIZE = BUTTON_SIZE

# ロックボタンの座標とサイズ
LOCK_BUTTON_POS = (SCREEN_WIDTH + 50, DELETE_BUTTON_POS[1] + BUTTON_SIZE + 20)
LOCK_BUTTON_SIZE = BUTTON_SIZE

# マス目を描画する関数
def draw_board():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        for y in range(0, 9 * CELL_SIZE, CELL_SIZE):  # yの範囲を9行分に変更
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

    # 太い線で3x3のブロックを区切る
    for x in range(0, SCREEN_WIDTH, CELL_SIZE * 3):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT), 3)
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE * 3):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y), 3)

# 数字を描画する関数
def draw_number(row, col, num):
    text = FONT.render(str(num), True, BLACK)
    text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
    screen.blit(text, text_rect)


# 数字ボタンを描画する関数
def draw_number_buttons():
    for i in range(1, 10):
        button_rect = pygame.Rect(BUTTON_POS[0], BUTTON_POS[1] + (i-1) * BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE)
        pygame.draw.rect(screen, BLACK, button_rect, 1)
        text = FONT.render(str(i), True, BLACK)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

# 選択中のマスをハイライトする関数
def draw_selected_cell():
    if selected_row != -1 and selected_col != -1:
        pygame.draw.rect(screen, GRAY, (selected_col * CELL_SIZE, selected_row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)

# 数字削除ボタンを描画する関数
def draw_delete_button():
    button_rect = pygame.Rect(DELETE_BUTTON_POS[0], DELETE_BUTTON_POS[1], DELETE_BUTTON_SIZE, DELETE_BUTTON_SIZE)
    pygame.draw.rect(screen, BLACK, button_rect, 1)
    text = FONT.render("X", True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

# ロックボタンを描画する関数
def draw_lock_button():
    button_rect = pygame.Rect(LOCK_BUTTON_POS[0], LOCK_BUTTON_POS[1], LOCK_BUTTON_SIZE, LOCK_BUTTON_SIZE)
    pygame.draw.rect(screen, BLACK, button_rect, 1)
    text = FONT.render("Lock", True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

# メインループ
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH + 100, 9 * CELL_SIZE + 50))  # 画面の高さを調整
pygame.display.set_caption("数独")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            # マスの選択
            if x < SCREEN_WIDTH and y < SCREEN_HEIGHT:
                selected_row = y // CELL_SIZE
                selected_col = x // CELL_SIZE
            # 数字ボタンのクリック
            elif BUTTON_POS[0] <= x <= BUTTON_POS[0] + BUTTON_SIZE and BUTTON_POS[1] <= y <= BUTTON_POS[1] + 9 * BUTTON_SIZE:
                for i in range(1, 10):
                    button_rect = pygame.Rect(BUTTON_POS[0], BUTTON_POS[1] + (i-1) * BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE)
                    if button_rect.collidepoint(x, y):
                        if not locked_board[selected_row][selected_col]:
                            board[selected_row][selected_col] = i
            # 数字削除ボタンのクリック
            else:
                delete_button_rect = pygame.Rect(DELETE_BUTTON_POS[0], DELETE_BUTTON_POS[1], DELETE_BUTTON_SIZE, DELETE_BUTTON_SIZE)
                if delete_button_rect.collidepoint(x, y):
                    if selected_row != -1 and selected_col != -1:
                        if not locked_board[selected_row][selected_col]:
                            board[selected_row][selected_col] = 0
                # ロックボタンのクリック
                lock_button_rect = pygame.Rect(LOCK_BUTTON_POS[0], LOCK_BUTTON_POS[1], LOCK_BUTTON_SIZE, LOCK_BUTTON_SIZE)
                if lock_button_rect.collidepoint(x, y):
                    if selected_row != -1 and selected_col != -1:
                        locked_board[selected_row][selected_col] = True

    # 画面をクリア
    screen.fill(WHITE)

    # マス目を描画
    draw_board()

    # 数字を描画
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                draw_number(i, j, board[i][j])

    # 選択中のマスをハイライト
    draw_selected_cell()

    # 数字ボタンを描画
    draw_number_buttons()
    draw_delete_button()  # 数字削除ボタンを描画
    draw_lock_button()  # ロックボタンを描画
    pygame.display.update()

pygame.quit()
