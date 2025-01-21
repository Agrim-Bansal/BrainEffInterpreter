from blessed import Terminal

term = Terminal()
code = ',.,.,,.,,<><[]'
userInput = '12 123'
codePointer = 0
memory = [0]*10
memoryPointer = 6
output = 'hello world'
stateStack = ['start']

codeBoxPos = (term.length('Code :  '), term.height//6)
inputBoxPos = (term.length('Input : '), 2 * term.height//6)
memoryPos = (0, term.height//2 - 1)
outputBoxPos = (term.length('Output : '), 4* term.height//6)

box_chars = {
    'tl': '┌',  # top left corner
    'tr': '┐',  # top right corner
    'bl': '└',  # bottom left corner
    'br': '┘',  # bottom right corner
    'v': '│',   # vertical line
    'h': '─',    # horizontal line
    'pointer' : '▲', 
    'up-joint' : '┬',
    'down-joint' : '┴',

}

def render(): 
    global term, code, memory, memoryPointer, output, codePointer, userInput

    print(term.home + term.clear+ term.bold + f'{"BrainFuck": ^{term.width}}')
    
    print(f'{"-"*11: ^{term.width}}')
    print(term.move_xy(0, term.height//6) + "Code  :")
    print(term.move_xy(0, 2*term.height//6) + "Input :")
    print(term.move_xy(0, 4*term.height//6) + "Output :")
    print(term.move_xy(term.length("Code  :" + code), term.height//6))
    print(term.move_xy(term.length("Input: " + userInput), 2* term.height//6))

    print(term.move_xy(*memoryPos) + box_chars['tl'] + box_chars['h']*3 + (box_chars['up-joint'] + box_chars['h']*3)*9 + box_chars['tr'])
    print(term.move_xy(memoryPos[0], memoryPos[1]+1), *[f"{box_chars['v']}{i:03}" for i in memory], box_chars['v'], sep="")
    print(term.move_xy(memoryPos[0], memoryPos[1]+2) + box_chars['bl'] + box_chars['h']*3 + (box_chars['down-joint'] + box_chars['h']*3)*9 + box_chars['br'])
    print(term.move_xy(memoryPos[0]+4*memoryPointer + 2, memoryPos[1]+2) + term.blue +box_chars['pointer'] + term.normal)

    print(term.move_xy(*codeBoxPos) + code)
    print(term.move_xy(codeBoxPos[0]+codePointer, codeBoxPos[1]) + term.orange + (code[codePointer] if code else '') + term.normal)
    print(term.move_right(8) + box_chars['h']*len(code))

    print(term.move_xy(*inputBoxPos) + userInput)
    print(term.move_right(8) + box_chars['h']*len(userInput))


    print(term.move_xy(*outputBoxPos) + output)
    print(term.move_right(9) + box_chars['h']*len(output))

    if stateStack[-1] == 'code':
        print(term.move_xy(codeBoxPos[0]+term.length(code), codeBoxPos[1]) + term.on_white + ' ' + term.normal)
    elif stateStack[-1] =='input' :
        print(term.move_xy(inputBoxPos[0]+term.length(userInput), inputBoxPos[1]) + term.on_white + ' ' + term.normal)


if __name__ == "__main__":

    render()
    # render_memory_array(0,3)
    # term.hidden_cursor()
    while True:
        with term.cbreak(), term.hidden_cursor():
            inp = term.inkey(timeout=0.1)
            # print(inp)
        if inp == 'q':
            print(term.clear())
            break
        elif inp =='r':
            memory = [0]*10
            memoryPointer = 0
            render()
        elif inp == 'c':
            if stateStack[-1] != 'code':
                stateStack.append('code')
            render()
        elif inp == 'i':
            if stateStack[-1] != 'input':
                stateStack.append('input')
            render()
        elif inp.name == 'KEY_ENTER':
            if stateStack[-1] == 'input':
                userInput += ' '
            if stateStack[-1] == 'code' or stateStack[-1] == 'input':
                stateStack.pop()
            render()
        elif inp == 'p':
            if stateStack[-1] != 'play':
                stateStack = ['start', 'play']
            else:
                stateStack = ['start']
        elif inp == 's':
            pass
        elif inp == '':
            if stateStack[-1] == 'input':
                if userInput:
                    userInput = userInput[:-1]
            if stateStack[-1] == 'code':
                if code:
                    code = code[:-1]
            render()
            # render_code(term.length('Code : ') + memoryPos[0], memoryPos[1])
        elif inp in '+-<>.,[]' and (stateStack[-1] == 'code'):
            code += inp
            render()
            # render_code(term.length('Code : ') + memoryPos[0], memoryPos[1])
        elif inp.isnumeric() and stateStack[-1] == 'input':
            userInput += str(inp)
            render()
            # render_code(term.length('Code : ') + memoryPos[0], memoryPos[1])
        # elif inp:
        #     print(inp.name)
        # render()
        inp = None

        
        



'''
q-quit
p - play-pause
r - reset
s - step
c - code

and ,.<>[]+- are the brainfuck commands

enter takes in the input / code
'''