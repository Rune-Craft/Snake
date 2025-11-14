import os
import Snake
import Apple
import random
import curses
import json
import Settings

class Game :

    def __init__(self):
        self.settings = Settings.Settings.load()

    def initialize(self, height, width) : 
        self.height = height
        self.width = width
        self.snake = Snake.Snake()
        self.snake.initialize([(2, 3), (3, 3), (4, 3), (5, 3)], "RIGHT")
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
        stdscr.addstr("+" + "-" * border_width + "+", curses.color_pair(3))

        row_num = 1
        for row in matrix:
            stdscr.addstr(row_num, 0, "|", curses.color_pair(3)) # + ' '.join(cell if cell else ' ' for cell in row) + "|")
            col_pos = 1
            for cell in row:
                if cell in ["X", "O"]:
                    stdscr.addstr(row_num, col_pos, cell if cell else ' ', curses.color_pair(1))
                elif cell in ["A"]:
                    stdscr.addstr(row_num, col_pos, cell if cell else ' ', curses.color_pair(2))
                else: 
                    stdscr.addstr(row_num, col_pos, cell if cell else ' ')
                col_pos += 2
            stdscr.addstr(row_num, col_pos, "|", curses.color_pair(3))
            row_num += 1

        stdscr.addstr(row_num, 0, "+" + "-" * border_width + "+", curses.color_pair(3))
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
        directory = "C:\\Dev Git\\snake\\"
        filename = "leaderboard.json"
        filepath = os.path.join(directory, filename)

        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            with open(filepath, 'r') as file:
                saved_data = json.load(file)
                top_five_scores = sorted(saved_data, key=lambda x: int(x['score']), reverse=True)[:5]
                if len(top_five_scores) < 5 or self.score > int(top_five_scores[-1]['score']):
                    stdscr.clear()
                    stdscr.addstr(0, 0, "Congratulations! You've placed on the Leaderboard!")
                    stdscr.addstr(1, 0, f"You scored: {self.score}!")
                    stdscr.addstr(2, 0, "Enter your initials (3 letters): ")
                    stdscr.addstr(3, 0, "_ _ _")
                    stdscr.move(3, 0)
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
                            stdscr.addstr(3, i * 2, letter)
                            stdscr.refresh()
                            i += 1
                            if i < 3:
                                stdscr.move(3, i * 2)

                    curses.curs_set(0)
                    stdscr.nodelay(True)  # Reset nodelay back to True
                    initials = initials.upper()
                    game_data = {
                        "score": f"{self.score}",
                        "initials": f"{initials}"
                    }

                    top_five_scores.append(game_data)
                    top_five_scores = sorted(top_five_scores, key=lambda x: int(x['score']), reverse=True)[:5]
                    with open(filepath, 'w') as file:
                        file.write(json.dumps(top_five_scores, indent=4))

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

    def continue_or_quit_game(self, stdscr):
        options = [
            "Main Menu",
            "Restart",
            "Quit"
        ]
        current_selection = 0

        while True:
            stdscr.addstr(12, 0, "Game Over! What would you like to do?")
            
            for idx, option in enumerate(options):
                if idx == current_selection:
                    stdscr.addstr(14 + idx, 0, f"> {option}", curses.A_REVERSE)
                else:
                    stdscr.addstr(14 + idx, 0, f"  {option}")
            
            stdscr.timeout(-1)
            stdscr.nodelay(False)
            key = stdscr.getch()
            
            if key == curses.KEY_UP:
                current_selection = (current_selection - 1) % len(options)
            elif key == curses.KEY_DOWN:
                current_selection = (current_selection + 1) % len(options)
            elif key == ord('\n'):
                if current_selection == 0:  # Main Menu
                    stdscr.timeout(self.settings.game_speed)
                    stdscr.nodelay(True)
                    return "menu"
                elif current_selection == 1:  # Restart
                    self.score = 0
                    self.snake.initialize([(2, 3), (3, 3), (4, 3), (5, 3)], "RIGHT")
                    stdscr.timeout(self.settings.game_speed)
                    stdscr.nodelay(True)
                    return False
                elif current_selection == 2:  # Quit
                    stdscr.timeout(self.settings.game_speed)
                    stdscr.nodelay(True)
                    return True

    def display_menu(self, stdscr):
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Snake Game")
            stdscr.addstr(4, 0, "(Enter) New Game")
            stdscr.addstr(5, 0, "(S) Settings")
            stdscr.timeout(-1)
            stdscr.nodelay(False)
            key = stdscr.getch() 
            if key == ord('\n'):
                self.settings = Settings.Settings.load()
                return False
            elif key == ord('s'):
                self.display_settings(stdscr, self.settings)

    def display_settings(self, stdscr, settings):
        options = [
            "Snake Color",
            "Apple Color",
            "Border Color",
            "Board Width",
            "Board Height",
            "Game Speed",
            "Back to Main Menu"
        ]
        current_selection = 0

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "====== SETTINGS ======")

            for idx, option in enumerate(options):
                if idx == current_selection:
                    stdscr.addstr(idx + 2, 0, f"> {option}", curses.A_REVERSE)
                else:
                    stdscr.addstr(idx + 2, 0, f"  {option}")
            
            key = stdscr.getch()

            if key == curses.KEY_UP:
                current_selection = (current_selection - 1) % len(options)
            if key == curses.KEY_DOWN:
                current_selection = (current_selection + 1) % len(options)
            elif key == ord('\n'):
                if current_selection == 0:
                    self.select_snake_color(stdscr, settings)
                elif current_selection == 1:
                    self.select_apple_color(stdscr, settings)
                elif current_selection == 2:
                    self.select_border_color(stdscr, settings)
                elif current_selection == 3:
                    self.select_border_width(stdscr, settings)
                elif current_selection == 4:
                    self.select_border_height(stdscr, settings)
                elif current_selection == 5:
                    self.select_game_speed(stdscr, settings)
                elif current_selection == 6:
                    break

    def select_snake_color(self, stdscr, settings): 
        color_options = [
            ("Green", curses.COLOR_GREEN),
            ("Blue", curses.COLOR_BLUE),
            ("Yellow", curses.COLOR_YELLOW),
            ("Magenta", curses.COLOR_MAGENTA),
            ("Cyan", curses.COLOR_CYAN),
            ("White", curses.COLOR_WHITE)
        ]

        current = 0
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Select Snake Color:")

            for idx, (name, color) in enumerate(color_options):
                if idx == current:
                    stdscr.addstr(idx + 2, 0, f"> {name}", curses.A_REVERSE)
                else:
                    stdscr.addstr(idx + 2, 0, f"  {name}")
            
            key = stdscr.getch()
            if key == curses.KEY_UP:
                current = (current - 1) % len(color_options)
            elif key == curses.KEY_DOWN:
                current = (current + 1) % len(color_options)
            elif key == ord('\n'):
                self.settings.snake_color = color_options[current][1]
                self.settings.save()
                curses.init_pair(1, self.settings.snake_color, curses.COLOR_BLACK)
                break
            elif key == ord('q'):
                break

    def select_apple_color(self, stdscr, settings):
        color_options = [
            ("Green", curses.COLOR_GREEN),
            ("Blue", curses.COLOR_BLUE),
            ("Yellow", curses.COLOR_YELLOW),
            ("Magenta", curses.COLOR_MAGENTA),
            ("Cyan", curses.COLOR_CYAN),
            ("White", curses.COLOR_WHITE)
        ]

        current = 0
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Select Apple Color:")

            for idx, (name, color) in enumerate(color_options):
                if idx == current:
                    stdscr.addstr(idx + 2, 0, f"> {name}", curses.A_REVERSE)
                else:
                    stdscr.addstr(idx + 2, 0, f"  {name}")
            
            key = stdscr.getch()
            if key == curses.KEY_UP:
                current = (current - 1) % len(color_options)
            elif key == curses.KEY_DOWN:
                current = (current + 1) % len(color_options)
            elif key == ord('\n'):
                self.settings.apple_color = color_options[current][1]
                self.settings.save()
                curses.init_pair(2, self.settings.apple_color, curses.COLOR_BLACK)
                break
            elif key == ord('q'):
                break

    def select_border_color(self, stdscr, settings):
        color_options = [
            ("Green", curses.COLOR_GREEN),
            ("Blue", curses.COLOR_BLUE),
            ("Yellow", curses.COLOR_YELLOW),
            ("Magenta", curses.COLOR_MAGENTA),
            ("Cyan", curses.COLOR_CYAN),
            ("White", curses.COLOR_WHITE)
        ]

        current = 0
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Select Border Color:")

            for idx, (name, color) in enumerate(color_options):
                if idx == current:
                    stdscr.addstr(idx + 2, 0, f"> {name}", curses.A_REVERSE)
                else:
                    stdscr.addstr(idx + 2, 0, f"  {name}")
            
            key = stdscr.getch()
            if key == curses.KEY_UP:
                current = (current - 1) % len(color_options)
            elif key == curses.KEY_DOWN:
                current = (current + 1) % len(color_options)
            elif key == ord('\n'):
                self.settings.border_color = color_options[current][1]
                self.settings.save()
                curses.init_pair(3, self.settings.border_color, curses.COLOR_BLACK)
                break
            elif key == ord('q'):
                break

    def select_border_width(self, stdscr, settings):
        size_options = [
            10,
            20,
            30,
            40,
            50,
        ]

        current = 0
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Select Border Width:")

            for idx, size in enumerate(size_options):
                if idx == current:
                    stdscr.addstr(idx + 2, 0, f"> {size}", curses.A_REVERSE)
                else:
                    stdscr.addstr(idx + 2, 0, f"  {size}")
            
            key = stdscr.getch()
            if key == curses.KEY_UP:
                current = (current - 1) % len(size_options)
            elif key == curses.KEY_DOWN:
                current = (current + 1) % len(size_options)
            elif key == ord('\n'):
                self.settings.board_width = size_options[current]
                self.settings.save()
                self.width = self.settings.board_width
                break
            elif key == ord('q'):
                break

    def select_border_height(self, stdscr, settings):
        size_options = [
            10,
            20,
            30,
            40,
            50,
        ]

        current = 0
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Select Border Height:")

            for idx, size in enumerate(size_options):
                if idx == current:
                    stdscr.addstr(idx + 2, 0, f"> {size}", curses.A_REVERSE)
                else:
                    stdscr.addstr(idx + 2, 0, f"  {size}")
            
            key = stdscr.getch()
            if key == curses.KEY_UP:
                current = (current - 1) % len(size_options)
            elif key == curses.KEY_DOWN:
                current = (current + 1) % len(size_options)
            elif key == ord('\n'):
                self.settings.board_height = size_options[current]
                self.settings.save()
                self.height = self.settings.board_height
                break
            elif key == ord('q'):
                break

    def select_game_speed(self, stdscr, settings):
        speed_options = [
            50,
            75,
            100,
            150,
            200,
            250
        ]

        current = 0
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Select Game Speed:")

            for idx, speed in enumerate(speed_options):
                if idx == current:
                    stdscr.addstr(idx + 2, 0, f"> {speed}", curses.A_REVERSE)
                else:
                    stdscr.addstr(idx + 2, 0, f"  {speed}")
            
            key = stdscr.getch()
            if key == curses.KEY_UP:
                current = (current - 1) % len(speed_options)
            elif key == curses.KEY_DOWN:
                current = (current + 1) % len(speed_options)
            elif key == ord('\n'):
                self.settings.game_speed = speed_options[current]
                self.settings.save()
                stdscr.timeout(self.settings.game_speed)
                break
            elif key == ord('q'):
                break

