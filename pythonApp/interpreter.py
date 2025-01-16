import sys

def interpret(code):
    
    memory_array = [0] * 10
    pointer_location = 0
    code = cleanup(code)
    l = len(code)

    if not syntax_check(code):
        return 'Syntax error'
    i = 0
    while i < l:
        command = code[i]
        if command == '>':
            pointer_location = (pointer_location + 1) % 10
        elif command == '<':
            pointer_location = (pointer_location + 10 - 1) % 10
        elif command == '+':
            memory_array[pointer_location] = (memory_array[pointer_location] + 1) % 256
        elif command == '-':
            memory_array[pointer_location] = (memory_array[pointer_location] + 256 - 1) % 256
        elif command == '.':
            print(memory_array[pointer_location])
        elif command == ',':
            memory_array[pointer_location] = int(input()) % 256
        elif command == '[':
            pass
        elif command == ']':
            openCount = 0
            closeCount = 1
            while closeCount != openCount:
                if memory_array[pointer_location] == 0:
                    i+=1
                    break
                i -= 1
                if code[i] == ']':
                    closeCount += 1
                elif code[i] == '[':
                    openCount += 1
            i -= 1
        else:
            pass
        i += 1
        print(*memory_array[:pointer_location], str(memory_array[pointer_location]) + '*', *memory_array[pointer_location+1:], sep="|")
    print()


def cleanup(code):
    code = code.replace('\n', '')
    allowed = '[]><,.+-'
    code = ''.join([c for c in code if c in allowed])
    return code

def syntax_check(code):
    firstClosing = code.find(']')

    if firstClosing == -1:
        lastOpening = code.rfind('[')
        if lastOpening == -1:
            return True
        return False
    else:
        lastOpening = code[:firstClosing].rfind('[')
        if lastOpening == -1:
            return False
        if lastOpening > firstClosing:
            return False
    return syntax_check(code[:lastOpening] + code[firstClosing+1:])

if __name__ == '__main__':
    if len(sys.argv) == 3:
        if(sys.argv[1] == '-f'):
            with open(sys.argv[2], 'r') as f:
                code = f.read()
    else:
        code = input('Enter the code to be executed :') 
    
    (interpret(code))