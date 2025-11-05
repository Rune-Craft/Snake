class Snake : 

    def initialize(self, init_body, init_direction) :
        self.body = init_body
        self.direction = init_direction

    def take_step(self) :
        current_head = self.head()
        new_head = current_head
        if self.direction == 'UP':
            new_head = (current_head[0], current_head[1] - 1)
        elif self.direction == 'LEFT':
            new_head = (current_head[0] - 1, current_head[1])
        elif self.direction == 'DOWN':
            new_head = (current_head[0], current_head[1] + 1)
        elif self.direction == 'RIGHT':
            new_head = (current_head[0] + 1, current_head[1])
        self.body = self.body[1:] + [new_head]

    def set_direction(self, direction) :
        if direction == ord('w'):
            self.direction = 'UP'
        elif direction == ord('a'):
            self.direction = 'LEFT'
        elif direction == ord('s'):
            self.direction = 'DOWN'
        elif direction == ord('d'):
            self.direction = 'RIGHT'

    def head(self) :
        return self.body[-1]
    
    def grow(self) :
        self.body = self.body + [self.body[-1]]
        return self.body