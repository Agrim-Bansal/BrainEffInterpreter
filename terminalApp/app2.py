from blessed import Terminal
term = Terminal()
height, width = term.height-6, term.width

box_chars = {
    'tl': '┌',  # top left corner
    'tr': '┐',  # top right corner
    'bl': '└',  # bottom left corner
    'br': '┘',  # bottom right corner
    'v': '│',   # vertical line
    'h': '─'    # horizontal line
}

print(term.clear)

def truncateText(text, w):
    i=0
    while i < len(text):
        if text[i] == '\n':
            text = text[:i] + ' '*(w - i%w) + text[i+1:]
        i+=1
    return [text[w*i:min(w*(i+1), len(text))] for i in range(len(text)//w+1)]

print(term.move_xy(0,0) + box_chars['tl'] + box_chars['h']*(width//3) + box_chars['tr'])

for i in range(1,height):
    print(term.move_xy(0,i) + box_chars['v'] + ' '*(width//3) + box_chars['v'])

print(box_chars['bl'] + box_chars['h']*(width//3) + box_chars['br'])
t = 'BrainFuck'
print(term.move_xy(int((width/3-term.length(t))//2), 1) + t)
print(term.move_xy(0, height))

t=truncateText('Brainfuck is a Turing complete language designed to be extremely minimalistic.\nIt consists of only eight simple commands, a data pointer, and an instruction pointer.\nIt is meant for amusement rather than practical function', term.width//3)
for i in range(len(t)):
    print(term.move_xy(1, i+2) + t[i])




while True:
    with term.cbreak():
        val = term.inkey()
        if val == 'q':
            break
        print(val)
    print(term.move_xy(0, height))