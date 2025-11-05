import Game
import curses

def main(stdscr) :
    curses.cbreak()
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

        if user_input in [ord('w'), ord('a'), ord('s'), ord('d')]:
            snakeGame.snake.set_direction(user_input)
        

        elif user_input == ord('Q'):
            snakeGame.display_quit_message(stdscr)
            quit = True
    
        if not quit:
            snakeGame.snake.take_step()

            if snakeGame.check_self_collision(stdscr):
                quit = True

            if snakeGame.check_wall_collision(stdscr):
                quit = True

            snakeGame.check_if_apple_eaten()
            snakeGame.render(stdscr)

    stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
