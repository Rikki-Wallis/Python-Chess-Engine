class Stack:
    def __init__(self):
        self.stack = []
        self.len = 0
    
    def is_empty(self):
        return self.len == 0
    
    def push(self, item):
        self.stack.append(item)
        self.len += 1
    
    def pop(self):
        if not self.is_empty():
            self.len -= 1
            return self.stack.pop()
    
    def peek(self):
        if not self.is_empty():
            return self.stack[-1]

class Node:
    def __init__(self, piece, colour, location):
        self.piece = piece
        self.colour = colour
        self.location = location