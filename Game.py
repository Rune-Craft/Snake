import os
import Snake
import Apple
import random
import curses
import json

class Game :

    def initialize(self, height, width) : 
        self.height = height
        self.width = width
        self.snake = Snake.Snake()
        self.snake.initialize([(0, 0), (0, 1), (2, 0), (3, 0)], "RIGHT")
        self.apples = []
        self.applesToMake = 1
        self.score = 0

        while len(self.apples) <= self.applesToMake:
            random_apple_x = random.randint(0, self.width - 1)
            random_apple_y = random.randint(0, self.height - 1)

            if (
                (random_apple_x, random_apple_y) not in self.snake.body 
                and (random_apple_x, random_apple_y) != self.snake.head() 
                and (random_apple_x, random_apple_y) not in self.apples
            ):
                self.apples.append(Apple.Apple(random_apple_x, random_apple_y))

    def render(self, stdscr) : 
        stdscr.clear()
        matrix = self.board_matrix()

        for apple in self.apples:
            if not apple.checkIsEaten(self):
                matrix[apple.y][apple.x] = "A"
            else:
                self.apples.remove(apple)
                self.apples.append(self.make_apple())
                matrix[self.apples[-1].y][self.apples[-1].x] = "A"

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
        if self.apples:
            for apple in self.apples:
                if apple.y == self.snake.head()[1] and apple.x == self.snake.head()[0]:
                    self.snake.grow()
                    self.apples.remove(apple)
                    self.score += 1
                    
                    # Increase apple count every 10 points
                    self.applesToMake = 1 + self.score // 10
                    
                    # Add apples if needed to reach the new target
                    while len(self.apples) < self.applesToMake:
                        self.apples.append(self.make_apple())
                    
                    return True

        return False

    def make_apple(self):
        while True:
            random_apple_x = random.randint(0, self.width - 1)
            random_apple_y = random.randint(0, self.height - 1)

            if (random_apple_x, random_apple_y) not in self.snake.body and (random_apple_x, random_apple_y) != self.snake.head():
                return Apple.Apple(random_apple_x, random_apple_y)
        

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

    def save_game(self, stdscr):
        stdscr.clear()
        stdscr.addstr(0, 0, "Enter your initials (3 letters): ")
        stdscr.addstr(1, 0, "_ _ _")
        stdscr.move(1, 0)
        curses.curs_set(2)
        stdscr.nodelay(False)
        stdscr.refresh()

        initials = ""
        i = 0
        while i < 3:
            char = stdscr.getch()
            if 65 <= char <= 90 or 97 <= char <= 122:
                letter = chr(char).upper()
                initials += letter
                stdscr.addstr(1, i * 2, letter)
                stdscr.refresh()
                i += 1
                if i < 3:
                    stdscr.move(1, i * 2)

        directory = "C:\\Dev Git\\snake\\"
        filename = "leaderboard.json"
        filepath = os.path.join(directory, filename)

        curses.curs_set(0)
        stdscr.nodelay(True)  # Reset nodelay back to True
        initials = initials.upper()
        game_data = {
            "score": f"{self.score}",
            "initials": f"{initials}"
        }

        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            with open(filepath, 'r') as file:
                existing_data = json.load(file)
                # existing_data.sort(key=lambda x: int(x['score']), reverse=True)
                sorted_data = sorted(existing_data, key=lambda x: int(x['score']), reverse=True)
                sorted_data.append(game_data)
                sorted_data = sorted(sorted_data, key=lambda x: int(x['score']), reverse=True)
                top_five_scores = sorted_data[:5]
                existing_data = top_five_scores
                with open(filepath, 'w') as file:
                    file.write(json.dumps(existing_data, indent=4))
        else:
            with open(filepath, 'w') as file:
                file.write(json.dumps([game_data], indent=4))

    def display_leaderboard(self, stdscr):
        stdscr.clear()
        stdscr.addstr(0, 0, "LeaderBoard")
        stdscr.refresh()

        directory = "C:\\Dev Git\\snake\\"
        filename = "leaderboard.json"
        filepath = os.path.join(directory, filename)

        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                leaderboard = json.load(file)
                leaderboard.sort(key=lambda x: int(x['score']), reverse=True)
                for i, entry in enumerate(leaderboard):
                    stdscr.addstr(i + 2, 0, f"{entry['initials']}: {entry['score']}")
        
        stdscr.addstr(12, 0, "Press any key to exit...")
        stdscr.refresh()
        
        stdscr.timeout(-1)
        stdscr.nodelay(False)
        curses.flushinp()
        stdscr.getch()
        
        stdscr.timeout(200)
        stdscr.nodelay(True)
