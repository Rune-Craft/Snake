import curses
import json
import os


class Settings:
    def __init__(self):
        self.snake_color = curses.COLOR_GREEN
        self.apple_color = curses.COLOR_RED
        self.border_color = curses.COLOR_WHITE

        self.board_height = 10
        self.board_width = 20
        self.game_speed = 200

    def save(self):
        data = {
            'snake_color': self.snake_color,
            'apple_color': self.apple_color,
            'border_color': self.border_color,
            'board_width': self.board_width,
            'board_height': self.board_height,
            'game_speed': self.game_speed
        }
        with open('settings.json', 'w') as file:
            json.dump(data, file, indent=4)

    @classmethod
    def load(cls):
        settings = cls()
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as file:
                data = json.load(file)
                settings.snake_color = data.get('snake_color', settings.snake_color)
                settings.apple_color = data.get('apple_color', settings.apple_color)
                settings.border_color = data.get('border_color', settings.border_color)
                settings.board_width = data.get('board_width', settings.board_width)
                settings.board_height = data.get('board_height', settings.board_height)
                settings.game_speed = data.get('game_speed', settings.game_speed)
        return settings
