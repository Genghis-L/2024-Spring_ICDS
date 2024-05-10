import pygame
import sys
import json
from chat_utils import myrecv, mysend
import tkinter
from pygame.locals import QUIT, KEYDOWN
from tkinter import messagebox

# constant declaration
SCREEN_COLOR = WHITE_CHESS = [255, 255, 255]
BLACK_CHESS = [0, 0, 0]
LINE_COLOR = [0, 0, 0, 175]
CURSOR_COLOR = [255, 255, 255, 100]
# BOARD_COLOR = [238, 154, 73]
BOARD_FILL = pygame.image.load('wood_texture_bright.jpg')
BACKGROUND_FILL = pygame.image.load('smooth-wood-texture.jpg')

X_BOARD = Y_BOARD = 20
BOARD_SIZE = 618
GRID_SIZE = 44
SCREEN_SIZE = (720, 658)

BLACK = 0
WHITE = 1
EMPTY = -1

ROUND_TIME = 5


class FiveINARow:
    def __init__(self):
        # key variables declaration
        self.delay_flag = False
        self.delay_accumulator = 0
        # self.turn = 0
        self.time = 0

        # a list of chess objects that have been put onto the board
        self.chess = []

        # bitboards for quick match of patterns
        self.black_bb = self.white_bb = 0

        # winning times for black and white
        self.black_winning = self.white_winning = 0

        self.round_change_flag = True

        # initiate the display
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        frame_rate = pygame.time.Clock()
        frame_rate.tick(60)

    def check_whose_turn(self):
        return BLACK if len(self.chess) % 2 == 0 else WHITE

    def check_occupied(self, x, y):
        for element in self.chess:
            if element[0][0] == x and element[0][1] == y:
                return False
        return True

    @staticmethod
    def report_cursor():
        cursor_x, cursor_y = pygame.mouse.get_pos()
        if cursor_x < X_BOARD or cursor_x > X_BOARD + BOARD_SIZE \
                or cursor_y < Y_BOARD or cursor_y > Y_BOARD + BOARD_SIZE:
            return cursor_x, cursor_y

        x_lower_bound, x_residue = divmod(cursor_x - X_BOARD, GRID_SIZE)
        x0 = x_lower_bound * GRID_SIZE + X_BOARD
        if x_residue >= GRID_SIZE / 2:
            x0 += GRID_SIZE

        y_lower_bound, y_residue = divmod(cursor_y - Y_BOARD, GRID_SIZE)
        y0 = y_lower_bound * GRID_SIZE + Y_BOARD
        if y_residue >= GRID_SIZE / 2:
            y0 += GRID_SIZE

        return x0, y0

    def helper_win_checker(self, bitboard_arg):
        def _result_illustrator(row1, col1, row2, col2):
            x_starting, y_starting = col1 * GRID_SIZE + X_BOARD, row1 * GRID_SIZE + Y_BOARD
            x_end, y_end = col2 * GRID_SIZE + X_BOARD, row2 * GRID_SIZE + Y_BOARD
            pygame.draw.line(self.screen, (255, 0, 0), (x_starting, y_starting), (x_end, y_end), 2)

        def _horizontal_win(bitboard):
            # binary representation of 5 consecutive 1's in row
            win_pattern = 0b11111

            for i in range(15):
                row = bitboard >> (i * 15) & 0b11111_11111_11111  # extract the i-th row
                # print(f'{row:b}')
                for j in range(11):
                    shifted_row = row >> j
                    if shifted_row & win_pattern == win_pattern:
                        # print('yes, yes')
                        # print(i, j)
                        _result_illustrator(i, j, i, j + 4)
                        pygame.display.update()
                        return True
            return False

        def _vertical_win(bitboard):
            # binary representation of 5 consecutive 1's in column
            win_pattern = 0b1000000000000001000000000000001000000000000001000000000000001
            for i in range(150):
                shifted_col = bitboard >> i
                if shifted_col & win_pattern == win_pattern:
                    # print('yes, yes')
                    _result_illustrator(i // 15, i % 15, i // 15 + 4, i % 15)
                    pygame.display.update()
                    return True
            return False

        def _positive_slope_diagonal_win(bitboard):
            # binary representation of 5 consecutive 1's in positive slope
            win_pattern = 0b100000000000001000000000000010000000000000100000000000001
            for i in range(168):
                shifted_col = bitboard >> i
                if shifted_col & win_pattern == win_pattern:
                    # print('yes, yes')
                    _result_illustrator(i // 15, i % 15, i // 15 + 4, i % 15 - 4)
                    pygame.display.update()
                    return True
            return False

        def _negative_slope_diagonal_win(bitboard):
            # binary representation of 5 consecutive 1's in negative slope
            win_pattern = 0b10000000000000001000000000000000100000000000000010000000000000001
            for i in range(168):
                shifted_col = bitboard >> i
                if shifted_col & win_pattern == win_pattern:
                    # print('yes, yes')
                    _result_illustrator(i // 15, i % 15, i // 15 + 4, i % 15 + 4)
                    pygame.display.update()
                    return True
            return False

        return _horizontal_win(bitboard_arg) or _vertical_win(bitboard_arg) \
            or _positive_slope_diagonal_win(bitboard_arg) or _negative_slope_diagonal_win(bitboard_arg)

    def update_bitboard(self, new_chess):
        x = int((new_chess[0][0] - X_BOARD) / GRID_SIZE)
        y = int((new_chess[0][1] - X_BOARD) / GRID_SIZE)
        if new_chess[1] == WHITE_CHESS:
            self.white_bb |= 1 << (y * 15 + x)
        else:
            self.black_bb |= 1 << (y * 15 + x)

    def if_continue(self):
        # display a msg box with the winning msg
        message = "Congratulations, you won! Do you want to continue?"

        root = tkinter.Tk()
        root.withdraw()

        response = tkinter.messagebox.askquestion("Game Over", message)
        if response == "yes":
            self.reset_game()
        else:
            pygame.quit()
            sys.exit()

    def check_win(self):
        if self.helper_win_checker(self.white_bb):
            self.white_winning += 1
            self.if_continue()

        if self.helper_win_checker(self.black_bb):
            self.black_winning += 1
            self.if_continue()

    def make_chess_board(self):
        # pygame.draw.rect(screen, BOARD_COLOR, [X_BOARD, Y_BOARD, BOARD_SIZE, BOARD_SIZE], width=0)
        out_flow_size = 20
        image_surface = pygame.Surface((BOARD_SIZE + 2 * out_flow_size, BOARD_SIZE + 2 * out_flow_size))
        image_surface.blit(
            pygame.transform.scale(BOARD_FILL, (BOARD_SIZE + 2 * out_flow_size, BOARD_SIZE + 2 * out_flow_size)),
            (0, 0))
        self.screen.blit(image_surface, (X_BOARD - out_flow_size, Y_BOARD - out_flow_size))

        board = pygame.Surface((1080, 720), pygame.SRCALPHA)

        # # draw axes
        # font = pygame.font.Font(None, 30)
        # for i in range(15):
        #     letter_text = font.render(chr(65 + i), True, LINE_COLOR)
        #     board.blit(letter_text, (X_BOARD - 5 + GRID_SIZE * i, Y_BOARD - 25))
        #     number_text = font.render(str(i + 1) if i+1 >= 10 else f'0{i+1}', True, LINE_COLOR)
        #     board.blit(number_text, (X_BOARD - 35, Y_BOARD - 5 + GRID_SIZE * i))

        for i in range(X_BOARD, BOARD_SIZE + X_BOARD, 44):
            # print(i)
            if i == Y_BOARD or i == BOARD_SIZE + Y_BOARD - 2:
                pygame.draw.line(self.screen, LINE_COLOR, [i, Y_BOARD], [i, BOARD_SIZE + Y_BOARD], 4)
            else:
                pygame.draw.line(board, LINE_COLOR, [i, Y_BOARD], [i, BOARD_SIZE + Y_BOARD], 1)

            if i == X_BOARD or i == BOARD_SIZE + X_BOARD - 2:
                pygame.draw.line(self.screen, LINE_COLOR, [X_BOARD, i], [BOARD_SIZE + X_BOARD, i], 4)
            else:
                pygame.draw.line(board, LINE_COLOR, [X_BOARD, i], [BOARD_SIZE + X_BOARD, i], 1)

        pygame.draw.circle(self.screen, LINE_COLOR, [X_BOARD + GRID_SIZE * 7 + 0.5, Y_BOARD + GRID_SIZE * 7 + 0.5], 8,
                           0)
        pygame.draw.circle(self.screen, LINE_COLOR, [X_BOARD + GRID_SIZE * 3 + 0.5, Y_BOARD + GRID_SIZE * 3 + 0.5], 6,
                           0)
        pygame.draw.circle(self.screen, LINE_COLOR, [X_BOARD + GRID_SIZE * 11 + 0.5, Y_BOARD + GRID_SIZE * 3 + 0.5], 6,
                           0)
        pygame.draw.circle(self.screen, LINE_COLOR, [X_BOARD + GRID_SIZE * 3 + 0.5, Y_BOARD + GRID_SIZE * 11 + 0.5], 6,
                           0)
        pygame.draw.circle(self.screen, LINE_COLOR, [X_BOARD + GRID_SIZE * 11 + 0.5, Y_BOARD + GRID_SIZE * 11 + 0.5], 6,
                           0)

        self.screen.blit(board, (0, 0))

    def show_chess(self):
        for chess in self.chess:
            pygame.draw.circle(self.screen, chess[1], chess[0], 20, 0)

    def validate_chess_placement_availability(self, x, y):
        return self.check_occupied(x, y) \
            and X_BOARD <= x <= X_BOARD + BOARD_SIZE \
            and Y_BOARD <= y <= Y_BOARD + BOARD_SIZE

    def chess_guider(self, x, y):
        if self.validate_chess_placement_availability(x, y):
            cursor = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
            pygame.draw.circle(cursor, CURSOR_COLOR, [x, y], 25, 0)
            self.screen.blit(cursor, (0, 0))

    def put_down_chess(self, x, y, system_override=False):
        keys_pressed = pygame.mouse.get_pressed()

        if system_override or keys_pressed[0] and self.delay_accumulator == 0:
            self.delay_flag = True
            if not self.validate_chess_placement_availability(x, y):
                return
            # if len(self.chess) % 2 == 0:
            if self.check_whose_turn() == BLACK:
                new_chess = [[x, y], BLACK_CHESS]
            else:
                new_chess = [[x, y], WHITE_CHESS]
            # self.turn += 1
            self.chess.append(new_chess)
            self.update_bitboard(new_chess)
            self.round_change_flag = True

        if self.delay_flag:
            self.delay_accumulator += 1
        if self.delay_accumulator % 25 == 0:
            self.delay_flag = False
            self.delay_accumulator = 0

        pygame.display.update()

    def timer(self):

        if self.round_change_flag:
            self.time = pygame.time.get_ticks()
            self.round_change_flag = False

        time_passed = (pygame.time.get_ticks() - self.time) / 1000
        time_passed_percentage = time_passed / ROUND_TIME
        time_left_percentage = 1 - time_passed_percentage

        BAR_LENGTH = 618
        BAR_THICKNESS = 25

        display = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        pygame.draw.rect(display, (255, 255, 255, 50),
                         (0, 0, SCREEN_SIZE[0] - (X_BOARD + BOARD_SIZE + 20), SCREEN_SIZE[1]))

        if self.check_whose_turn() == BLACK:
            pygame.draw.rect(display, WHITE_CHESS, (15, 20, BAR_THICKNESS, time_left_percentage * BAR_LENGTH),
                             border_radius=25)
            pygame.draw.circle(display, BLACK_CHESS, (27.5, time_left_percentage * BAR_LENGTH + 20), 25, 0)
            font1 = pygame.font.SysFont('TimeNewRoman', size=30)
            text1 = font1.render(f'{ROUND_TIME - time_passed:.0f}s', True, WHITE_CHESS)
            display.blit(text1, (17, time_left_percentage * BAR_LENGTH + 12))
        else:
            pygame.draw.rect(display, BLACK_CHESS, (
            15, 20 + time_passed_percentage * BAR_LENGTH, BAR_THICKNESS, time_left_percentage * BAR_LENGTH),
                             border_radius=25)
            # pygame.draw.rect(screen, WHITE_CHESS, (10, 20, BAR_THICKNESS, BAR_LENGTH), width=1)
            pygame.draw.circle(display, WHITE_CHESS, (27.5, 20 + time_passed_percentage * BAR_LENGTH), 25, 0)
            font1 = pygame.font.SysFont('TimeNewRoman', size=30)
            text1 = font1.render(f'{ROUND_TIME - time_passed:.0f}s', True, BLACK_CHESS)
            display.blit(text1, (17, time_passed_percentage * BAR_LENGTH + 12))

        self.screen.blit(display, (X_BOARD + BOARD_SIZE + 25, Y_BOARD - 20))

    def passive_round_change(self):
        def random_placed():
            x = y = 7
            yield x, y

            x, y = x + 1, y + 1
            for r in range(1, 8):
                yield x, y

                for _ in range(2 * r):
                    x = x - 1
                    yield x, y
                for _ in range(2 * r):
                    y = y - 1
                    yield x, y
                for _ in range(2 * r):
                    x = x + 1
                    yield x, y
                for _ in range(2 * r - 1):
                    y = y + 1
                    yield x, y
                x, y = x + 1, y + 2

        if (pygame.time.get_ticks() - self.time) >= ROUND_TIME * 1000:
            self.round_change_flag = True
            for item in random_placed():
                loc_x, loc_y = X_BOARD + GRID_SIZE * item[0], Y_BOARD + GRID_SIZE * item[1]
                if self.check_occupied(loc_x, loc_y):
                    self.put_down_chess(loc_x, loc_y, system_override=True)
                    return

    def reset_game(self):
        self.time = 0
        self.round_change_flag = True

        self.delay_flag = False
        self.delay_accumulator = 0

        # a list of chess objects that have been put onto the board
        self.chess = []

        # bitboards for quick match of patterns
        self.black_bb = self.white_bb = 0

    def main_game(self):
        while True:
            self.screen.fill(SCREEN_COLOR)
            self.screen.blit(pygame.transform.scale(BACKGROUND_FILL, SCREEN_SIZE), (0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

            self.make_chess_board()
            self.timer()
            self.show_chess()
            self.passive_round_change()

            self.check_win()

            x, y = self.report_cursor()
            self.chess_guider(x, y)
            self.put_down_chess(x, y)


class OnlineFiveInARow(FiveINARow):
    def __init__(self, socket, me, peer, holding):
        super().__init__()
        self.socket = socket
        self.me = me
        self.peer = peer
        self.hold = holding

    def info_exchange(self):
        def _chess_state_synchronize(peer_state_arg):
            if len(peer_state_arg['msg']) > len(self.chess) or len(peer_state_arg['msg']) == 0:
                self.chess = peer_state_arg['msg']
                self.round_change_flag = True
            return

        # send out our chess board
        mysend(self.socket,
               json.dumps({'action': 'chess_state_update', "from": "[" + self.me + "]", "to": self.peer,
                           "msg": self.chess}))

        # receive peer's chess board
        peer_state = myrecv(self.socket)
        if len(peer_state) > 0:
            peer_state = json.loads(peer_state)
            # print(peer_state_arg['msg'])
            if peer_state['action'] == 'chess_state_update':
                _chess_state_synchronize(peer_state)

    def put_down_chess(self, x, y, system_override=False):
        # print(self.hold)
        if self.hold == 'BLACK' and self.check_whose_turn() == BLACK:
            super().put_down_chess(x, y, system_override=system_override)

        if self.hold == 'WHITE' and self.check_whose_turn() == WHITE:
            super().put_down_chess(x, y, system_override=system_override)

        pygame.display.update()

    def main_game(self):
        while True:
            self.screen.fill(SCREEN_COLOR)
            self.screen.blit(pygame.transform.scale(BACKGROUND_FILL, SCREEN_SIZE), (0, 0))
            for event in pygame.event.get():
                if event.type in (QUIT, KEYDOWN):
                    sys.exit()

            self.make_chess_board()
            self.timer()

            self.info_exchange()

            self.show_chess()
            self.passive_round_change()

            self.check_win()

            x, y = self.report_cursor()
            self.chess_guider(x, y)
            self.put_down_chess(x, y)


if __name__ == "__main__":
    game = FiveINARow()
    game.main_game()
