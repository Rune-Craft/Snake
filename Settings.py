import curses
import json
import os
import sqlite3
import socket


class Settings:
    def __init__(self):
        self.snake_color = curses.COLOR_GREEN
        self.apple_color = curses.COLOR_RED
        self.border_color = curses.COLOR_WHITE

        self.board_height = 10
        self.board_width = 20
        self.game_speed = 200

    def save(self):
        conn = sqlite3.connect('snake_game.db')
        cursor = conn.cursor()
        
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Settings (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_machine TEXT NOT NULL,
                            snake_color INTEGER NOT NULL,
                            apple_color INTEGER NOT NULL,
                            border_color INTEGER NOT NULL,
                            board_width INTEGER NOT NULL,
                            board_height INTEGER NOT NULL,
                            game_speed INTEGER NOT NULL
                        )
                        ''')
        
        machine_name = socket.gethostname()
        
        cursor.execute("INSERT INTO Settings ( " +
                        " user_machine, snake_color, apple_color, border_color, board_width, board_height, game_speed " +
                        " ) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (machine_name, self.snake_color, self.apple_color, self.border_color, self.board_width, self.board_height, self.game_speed))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def load(cls):
        settings = cls()
        conn = sqlite3.connect('snake_game.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Settings (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_machine TEXT NOT NULL,
                    snake_color INTEGER NOT NULL,
                    apple_color INTEGER NOT NULL,
                    border_color INTEGER NOT NULL,
                    board_width INTEGER NOT NULL,
                    board_height INTEGER NOT NULL,
                    game_speed INTEGER NOT NULL
                )
                ''')
        
        saved_settings = cursor.execute("SELECT * FROM Settings WHERE user_machine = ?", (socket.gethostname(),)).fetchone()
        
        if saved_settings:    
            settings.snake_color = saved_settings['snake_color']
            settings.apple_color = saved_settings['apple_color']
            settings.border_color = saved_settings['border_color']
            settings.board_width = saved_settings['board_width']
            settings.board_height = saved_settings['board_height']
            settings.game_speed = saved_settings['game_speed']
        return settings
