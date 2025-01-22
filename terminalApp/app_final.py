from blessed import Terminal

term = Terminal()
code = ',>,<[->+<]>.'
code = ''
userInput = ''
codePointer = 0
memory = [0]*10
memoryPointer = 0
output = ''
stateStack = ['State 0']

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
    if stateStack[-1] != 'code':
        print(term.move_xy(codeBoxPos[0]+codePointer, codeBoxPos[1]) + term.black_on_khaki + (code[codePointer] if code else '') + term.normal)
    
    print(term.move_right(8) + box_chars['h']*len(code))

    print(term.move_xy(*inputBoxPos) + userInput)
    print(term.move_right(8) + box_chars['h']*len(userInput))

    print(term.move_xy(*outputBoxPos) + output)
    print(term.move_right(9) + box_chars['h']*len(output))

    if stateStack[-1] == 'code':
        print(term.move_xy(codeBoxPos[0]+term.length(code), codeBoxPos[1]) + term.on_white + ' ' + term.normal)
    elif stateStack[-1] =='input' :
        print(term.move_xy(inputBoxPos[0]+term.length(userInput), inputBoxPos[1]) + term.on_white + ' ' + term.normal)

    print(term.move_xy(0, term.height-5) + term.blue + 'Status : ' + stateStack[-1] + term.normal)
    print(term.move_xy(0, term.height-3) + term.black_on_white + 'Press p to play/pause, s to enter step mode, c to enter code mode, r to reset, q to quit.' + term.normal)


def runCode():
    global codePointer, memory, memoryPointer, output, code, userInput, stateStack

    codePointer = codePointer
    command = code[codePointer]
    if command == '>':
        memoryPointer = (memoryPointer + 1) % 10
    elif command == '<':
        memoryPointer = (memoryPointer + 10 - 1) % 10
    elif command == '+':
        memory[memoryPointer] = (memory[memoryPointer] + 1) % 256
    elif command == '-':
        memory[memoryPointer] = (memory[memoryPointer] + 256 - 1) % 256
    elif command == '.':
        output += ' ' + str(memory[memoryPointer])
    elif command == ',':
        if stateStack[-1] == 'input':
            memory[memoryPointer] = int(userInput.split()[-1]) % 256
            stateStack.pop()
        else:
            stateStack.append('input')
            return
    elif command == '[':
        openCount = 1
        closeCount = 0
        if memory[memoryPointer] == 0:
            while closeCount != openCount:
                codePointer += 1
                if code[codePointer] == ']':
                    closeCount += 1
                elif code[codePointer] == '[':
                    openCount += 1
        else:
            codePointer += 1
        codePointer -= 1
    elif command == ']':
        openCount = 0
        closeCount = 1
        while closeCount != openCount:
            if memory[memoryPointer] == 0:
                codePointer+=1
                return
            codePointer -= 1
            if code[codePointer] == ']':
                closeCount += 1
            elif code[codePointer] == '[':
                openCount += 1
        codePointer -= 1 # TO change the last additive increment
    else:
        pass
    if codePointer == len(code)-1:
        stateStack = ['State 0']
        codePointer = 0
        return
    if not (codePointer >= len(code)-1) :
        codePointer += 1



if __name__ == "__main__":

    render()

    while True:
        with term.cbreak(), term.hidden_cursor():
            if stateStack[-1] == 'play':
                inp = term.inkey(timeout=0.1)
            else:
                inp = term.inkey(timeout=None)
        if inp == 'q':
            print(term.clear())
            break
        elif inp =='r':
            memory = [0]*10
            memoryPointer = 0
            output = ''
            codePointer = 0
            userInput = ''
        elif inp == 'c':
            if stateStack[-1] != 'code':
                stateStack.append('code')
        elif inp.name == 'KEY_ENTER':
            if stateStack[-1] == 'input':
                userInput += ' '
                runCode()
            if stateStack[-1] == 'code' :
                stateStack.pop()
            if stateStack[-1] == 'step':
                runCode()
        elif inp == 'p':
            if stateStack[-1] != 'play':
                stateStack = ['State 0', 'play']
            else:
                stateStack = ['State 0']
        elif inp == 's':
            if stateStack[-1] != 'step':
                stateStack.append('step')
        elif inp == '':
            if stateStack[-1] == 'input':
                if userInput:
                    userInput = userInput[:-1]
            if stateStack[-1] == 'code':
                if code:
                    codePointer = min(codePointer, len(code)-1)
                    code = code[:-1]
        elif inp in '+-<>.,[]' and (stateStack[-1] == 'code'):
            code += inp
        elif inp.isnumeric() and stateStack[-1] == 'input':
            userInput += str(inp)
        
        if stateStack[-1] == 'play':
            runCode()
            render()
        if inp:
            render()
        

        

        
        



'''
q-quit
p - play-pause
r - reset
s - step
c - code

and ,.<>[]+- are the brainfuck commands

enter takes in the input / code
'''