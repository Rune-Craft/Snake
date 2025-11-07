import Snake
import Apple
import random
import curses

class Game :

    def initialize(self, height, width) : 
        self.height = height
        self.width = width
        self.snake = Snake.Snake()
        self.snake.initialize([(0, 0), (0, 1), (2, 0), (3, 0)], "RIGHT")
        self.apple = None
        self.score = 0

        while self.apple is None:
            random_apple_x = random.randint(0, self.width - 1)
            random_apple_y = random.randint(0, self.height - 1)

            if (random_apple_x, random_apple_y) not in self.snake.body and (random_apple_x, random_apple_y) != self.snake.head():
                self.apple = Apple.Apple(random_apple_x, random_apple_y)
    
    def render(self, stdscr) : 
        stdscr.clear()
        matrix = self.board_matrix()

        if self.apple is not None and not self.apple.checkIsEaten():
            matrix[self.apple.y][self.apple.x] = "A"
        else :
            self.apple = self.make_apple()
            matrix[self.apple.y][self.apple.x] = "A"

        border_width = self.width * 2 - 1
        stdscr.addstr("+" + "-" * border_width + "+")

        row_num = 1
        for row in matrix:
            stdscr.addstr(row_num, 0, "|") # + ' '.join(cell if cell else ' ' for cell in row) + "|")
            col_pos = 1
            for cell in row:
                if cell in ["X", "O"]:
                    stdscr.addstr(row_num, col_pos, cell if cell else ' ', curses.color_pair(1))
                elif cell in ["A"]:
                    stdscr.addstr(row_num, col_pos, cell if cell else ' ', curses.color_pair(2))
                else: 
                    stdscr.addstr(row_num, col_pos, cell if cell else ' ')
                col_pos += 2
            stdscr.addstr(row_num, col_pos, "|")
            row_num += 1

        stdscr.addstr(row_num, 0, "+" + "-" * border_width + "+")
        stdscr.addstr(row_num + 1, 0, f"Score: {self.score}")
        stdscr.refresh()

    def board_matrix(self) :
        matrix = []
        for y in range(self.height) :
            row = []
            for x in range(self.width) :
                if (x, y) == self.snake.head() :
                    row.append("X")
                elif (x, y) in self.snake.body :
                    row.append("O")
                else :
                    row.append(" ")
            matrix.append(row)
        return matrix
    
    def check_wall_collision(self, stdscr) :
        head_x, head_y = self.snake.head()
        if head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height:
            stdscr.clear()
            stdscr.addstr(0, 0, "Game Over! You collided with the wall.")
            stdscr.addstr(1, 0, f"Your score: {self.score}")
            stdscr.refresh()
            curses.napms(3000)
            stdscr.nodelay(False)
            stdscr.getch()
            return True  # Collision with wall
        
        return False  # No collision

    def check_self_collision(self, stdscr) :
        head = self.snake.head()
        if head in self.snake.body[:-1]:
            stdscr.clear()
            stdscr.addstr(0, 0, "Game Over! You collided with yourself.")
            stdscr.addstr(1, 0, f"Your score: {self.score}")
            stdscr.refresh()
            curses.napms(3000)
            stdscr.nodelay(False)
            stdscr.getch()
            return True  # Collision with self
        
        return False  # No collision
    
    def check_if_apple_eaten(self) :
        if self.apple is not None and self.apple.y == self.snake.head()[1] and self.apple.x == self.snake.head()[0]:
            self.snake.grow()
            self.apple = None
            self.score += 1
            return True

        return False

    def make_apple(self):
        while self.apple is None:
            random_apple_x = random.randint(0, self.width - 1)
            random_apple_y = random.randint(0, self.height - 1)

            if (random_apple_x, random_apple_y) not in self.snake.body and (random_apple_x, random_apple_y) != self.snake.head():
                self.apple = Apple.Apple(random_apple_x, random_apple_y)
        
        return self.apple
    
    def display_quit_message(self, stdscr) :
        stdscr.clear()
        stdscr.addstr(0, 0, "Thanks for playing!")
        stdscr.addstr(1, 0, f"Your score: {self.score}")
        stdscr.refresh()
        curses.napms(3000)
        stdscr.nodelay(False)
        stdscr.getch()
        return
    
    def pause_game(self, stdscr):
        stdscr.nodelay(False)
        stdscr.getch()
        stdscr.nodelay(True)