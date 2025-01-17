from blessed import Terminal
from time import sleep

term = Terminal()

print

box_chars = {
    'tl': '┌',  # top left corner
    'tr': '┐',  # top right corner
    'bl': '└',  # bottom left corner
    'br': '┘',  # bottom right corner
    'v': '│',   # vertical line
    'h': '─'    # horizontal line
}

print(term.clear)

print(term.move, end='')
term.center(box_chars['tl'] + 'Welcome to the terminal app!' + box_chars['tr'])


class Colors:
    global term
    FontPrimary = term.black
    FontSecondary = term.black
    BackgroundPrimary = term.on_deepskyblue
    BackgroundSecondary = term.on_deepskyblue4

    RED = term.red
    GREEN = term.green
    BLUE = term.blue
    YELLOW = term.yellow
    MAGENTA = term.magenta
    CYAN = term.cyan
    WHITE = term.white
    BLACK = term.black
    ORANGE = term.orange
    PURPLE = term.purple
    GRAY = term.gray
    BRIGHT_RED = term.bright_red
    BRIGHT_GREEN = term.bright_green
    BRIGHT_BLUE = term.bright_blue
    BRIGHT_YELLOW = term.bright_yellow
    BRIGHT_MAGENTA = term.bright_magenta
    BRIGHT_CYAN = term.bright_cyan
    BRIGHT_WHITE = term.bright_white
    BRIGHT_BLACK = term.bright_black
    BRIGHT_ORANGE = term.bright_orange
    BRIGHT_PURPLE = term.bright_purple
    BRIGHT_GRAY = term.bright_gray




class text_box():
    def __init__(self, text, x, y, w, h, border={'top':True, 'bottom':True, 'left':True, 'right':True}, color=Colors.FontPrimary, bg=Colors.BackgroundPrimary):
        self.box_chars = {
            'tl': '┌',  # top left corner
            'tr': '┐',  # top right corner
            'bl': '└',  # bottom left corner
            'br': '┘',  # bottom right corner
            'v': '│',   # vertical line
            'h': '─'    # horizontal line
        }
        self.x = x
        self.y = y
        self.wt = w-2
        self.ht = h-2
        self.truncated_text = self.truncateText(text)
        self.setBorder(border)
        self.border = border
        self.color = color
        self.bg = bg

    def setBorder(self, borders):
        self.box_chars = {
            'tl': '┌' if borders['top'] and borders['left'] else '-' if borders['top'] else '|' if borders['left'] else ' ',
            'tr': '┐' if borders['top'] and borders['right'] else '-' if borders['top'] else '|' if borders['right'] else ' ',
            'bl': '└' if borders['bottom'] and borders['left'] else '-' if borders['bottom'] else '|' if borders['left'] else ' ',
            'br': '┘' if borders['bottom'] and borders['right'] else '-' if borders['bottom'] else '|' if borders['right'] else ' ',
            'l' : '│' if borders['left'] else ' ',
            'r' : '│' if borders['right'] else ' ',
            'v' : '│',
            'h': '─', 
        }


    def truncateText(self, text):
        i=0
        while i < len(text):
            if text[i] == '\n':
                text = text[:i] + ' '*(self.wt - i%self.wt) + text[i+1:]
            i+=1
        return [text[self.wt*i:min(self.wt*(i+1), len(text))] for i in range(len(text)//self.wt+1)]



    def addText(self, text):
        self.truncated_text = [*self.truncated_text[:-1], *self.truncateText(self.truncated_text[-1] + text)]

    def __str__(self):
        print(self.color + self.bg)

        if self.border['top']:
            print(term.move_xy(self.x,self.y) + self.box_chars['tl'] + self.box_chars['h']*self.wt + self.box_chars['tr'])

        if len(self.truncated_text) > self.ht:
            for i in range(self.ht):
                if len(self.truncated_text[i]) == self.wt:
                    print(term.move_xy(self.x,self.y+i+1) + self.box_chars['l'] + self.truncated_text[i] + self.box_chars['r'])
                else :
                    print(term.move_xy(self.x,self.y+i+1) + self.box_chars['l'] + self.truncated_text[i] + ' '*(self.wt - len(self.truncated_text[i])) + self.box_chars['r'])

            print(term.move_xy(self.x,self.y+self.ht+1) + self.box_chars['l'] + term.orangered + '.'*self.wt + term.normal + self.box_chars['r'])  
        else:
            for i in range(len(self.truncated_text)):
                if len(self.truncated_text[i]) == self.wt:
                    print(term.move_xy(self.x,self.y+i+1) + self.box_chars['l'] + self.truncated_text[i] + self.box_chars['r'])
                else :
                    print(term.move_xy(self.x,self.y+i+1) + self.box_chars['l'] + self.truncated_text[i] + ' '*(self.wt - len(self.truncated_text[i])) + self.box_chars['r'])

            for i in range(len(self.truncated_text), self.ht):
                print(term.move_xy(self.x,self.y+i+1) + self.box_chars['l'] + ' ' * self.wt + self.box_chars['r'])
            if self.border['bottom']:
                print(term.move_xy(self.x,self.y+self.ht+1) + self.box_chars['bl'] + self.box_chars['h']*self.wt + self.box_chars['br'])
        print(term.normal + term.on_normal)

        return ''
    
    def render(self):
        print(self)

layout = []

layout += [
    text_box('', 0, 0, term.width//3 + 1, term.height-2),
    text_box('BrainFuck', int((term.width/3 - term.length('BrainFuck'))/2), 0, term.length('BrainFuck')+3, 3, border={'top':False, 'bottom':False, 'left':False, 'right':False}),
    text_box('Brainfuck is a Turing complete language designed to be extremely minimalistic.\nIt consists of only eight simple commands, a data pointer, and an instruction pointer.\nIt is meant for amusement rather than practical function', 1, 2, term.width//3-1, 20, {'top':False, 'bottom':False, 'left':False, 'right':False}),
]


def refresh():
    global layout
    print(term.clear)

    for e in layout:
        print(e)
    # print(te)

refresh()

while True:
    with term.cbreak():
        inp = term.inkey(timeout=0.1)
    if inp == 'q':
        print(term.move_xy(term.width//16, term.height) + term.center('Goodbye!'))
        sleep(1)
        exit(0)
    if inp=='r':
        refresh()

    # else:
    #     term.clear
    # print(inp)
    # if inp == '\n':
    #     print('Enter pressed')
    # with open('logs', 'w+') as f:
    #     f.write(f.read() + inp)





