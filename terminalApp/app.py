from blessed import Terminal
from time import sleep

term = Terminal()

# term.home + term.clear + term.move_y(term.height // 2)
a = (term.home + term.clear + term.move_y(term.height // 2))

print(a)

print(term.black_on_darkkhaki(term.center('press any key to continue.')))


with term.cbreak(), term.hidden_cursor():
    inp = term.inkey()

print(term.move_down(2) + 'You pressed ' + term.bold(repr(inp)))

print(term.move_down(2) + term.center('Goodbye!'))
sleep(1)
print(term.clear)

