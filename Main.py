import Game
import curses
import Settings

def main(stdscr) :
    curses.cbreak()
    curses.start_color()

    settings = Settings.Settings.load()
    curses.init_pair(1, settings.snake_color, curses.COLOR_BLACK)
    curses.init_pair(2, settings.apple_color, curses.COLOR_BLACK)
    curses.init_pair(3, settings.border_color, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    snakeGame = Game.Game()
    snakeGame.initialize(settings.board_height, settings.board_width)
    snakeGame.render(stdscr)
    quit = snakeGame.display_menu(stdscr)
    settings = Settings.Settings.load()

    stdscr.keypad(True)
    stdscr.nodelay(True)
    stdscr.timeout(settings.game_speed)
    
    while not quit:
        user_input = stdscr.getch()

        if user_input in [ord('w'), ord('a'), ord('s'), ord('d'), curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            snakeGame.snake.set_direction(user_input)
        

        elif user_input == ord('q'):
            snakeGame.display_quit_message(stdscr)
            snakeGame.save_game(stdscr)
            snakeGame.display_leaderboard(stdscr)
            result = snakeGame.continue_or_quit_game(stdscr)
            if result == "menu":
                quit = snakeGame.display_menu(stdscr)
                settings = Settings.Settings.load()
                snakeGame.initialize(settings.board_height, settings.board_width)
                stdscr.timeout(settings.game_speed)
            else:
                quit = result

        elif user_input == ord('p'):
            snakeGame.pause_game(stdscr)
            snakeGame.display_leaderboard(stdscr)
            stdscr.addstr(10, 0, "Game Paused. Press 'p' to resume.")
            stdscr.refresh()
            while True:
                if stdscr.getch() == ord('p'):
                    break

        if not quit:
            snakeGame.snake.take_step()

            if snakeGame.check_self_collision(stdscr):
                snakeGame.save_game(stdscr)
                snakeGame.display_leaderboard(stdscr)
                result = snakeGame.continue_or_quit_game(stdscr)
                if result == "menu":
                    quit = snakeGame.display_menu(stdscr)
                    settings = Settings.Settings.load()
                    snakeGame.initialize(settings.board_height, settings.board_width)
                    stdscr.timeout(settings.game_speed)
                else:
                    quit = result

            if snakeGame.check_wall_collision(stdscr):
                snakeGame.save_game(stdscr)
                snakeGame.display_leaderboard(stdscr)
                result = snakeGame.continue_or_quit_game(stdscr)
                if result == "menu":
                    quit = snakeGame.display_menu(stdscr)
                    settings = Settings.Settings.load()
                    snakeGame.initialize(settings.board_height, settings.board_width)
                    stdscr.timeout(settings.game_speed)
                else:
                    quit = result

            snakeGame.check_if_apple_eaten()
            snakeGame.render(stdscr)

    stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
