import Game
import curses

def main(stdscr) :
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)
    stdscr.timeout(200)
    curses.start_color()

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    snakeGame = Game.Game()
    snakeGame.initialize(10, 20)
    snakeGame.render(stdscr)
    quit = False
    
    while not quit:
        user_input = stdscr.getch()

        if user_input in [ord('w'), ord('a'), ord('s'), ord('d'), curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            snakeGame.snake.set_direction(user_input)
        

        elif user_input == ord('q'):
            snakeGame.display_quit_message(stdscr)
            snakeGame.save_game(stdscr)
            snakeGame.display_leaderboard(stdscr)
            quit = snakeGame.continue_or_quit_game(stdscr)

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
                quit = snakeGame.continue_or_quit_game(stdscr)

            if snakeGame.check_wall_collision(stdscr):
                snakeGame.save_game(stdscr)
                snakeGame.display_leaderboard(stdscr)
                quit = snakeGame.continue_or_quit_game(stdscr)

            snakeGame.check_if_apple_eaten()
            snakeGame.render(stdscr)

    stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
