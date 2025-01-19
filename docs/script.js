let codeRunning = false;
inputs = [];
let memory_pointer = 0;
let code_pointer = 0;
let speed = 100 - document.getElementById('speed').value;

const examples = [
    '',
    '+>++>+++>++++',
    ',>,<[->+<]>.',
    ',[->[>],[<]<] >+ [[>]<-[<]>+>]<-.',
]


document.getElementById('run').addEventListener('click', ()=>{
    codeCleanup();
    codeRunning =true;
    document.getElementById('input').readOnly = true;
    document.getElementById('code').readOnly = true;
    inputs = document.getElementById('input').value.split(' ');
});

document.getElementById('stop').addEventListener('click', ()=>{
    if (codeRunning){
        codeRunning = false;
    }else{
        codeRunning = true;
    }
});

document.getElementById('step').addEventListener('click', runCode);

document.getElementById('reset').addEventListener('click', ()=>{
    code_pointer = 0;
    memory_pointer = 0;
    codeRunning = false;
    document.getElementById('input').readOnly = false;
    document.getElementById('code').readOnly = false;
    document.getElementById('output').innerHTML = '';
    document.getElementById('input').value = '';
    inputs = [];
    memory_container = document.getElementsByClassName('memory-container')[0];
    for (let i = 0; i < memory_container.children.length; i++){
        memory_container.children[i].innerHTML = 0;
    }
});

setInterval(()=>{
    memory_container = document.getElementsByClassName('memory-container')[0];

    for (let i = 0; i < memory_container.children.length; i++){
        memory_container.children[i].classList.remove('active');
    }
    memory_container.children[memory_pointer].classList.add('active');

}, 10);


function codeCleanup(){
    console.log('Cleaning up')
    const code = document.getElementById('code');
    const allowedChars = '[],.<>+-';
    const codeText = code.value;
    let cleanCode = '';

    for (let i =0; i < codeText.length; i++){
        char = codeText[i];
        if (allowedChars.includes(char)){
            cleanCode += char;
        }
    }
    code.value = cleanCode;
}

function runCode(){
    var code = document.getElementById('code');
    var char = code.value[code_pointer];

    var memory = document.getElementsByClassName('memory-container')[0].children[memory_pointer];
    console.log('run' + code_pointer + ' ' + char);

    switch (char){
        case '>':
            memory_pointer = (memory_pointer + 1)%16;
            break;
        case '<':
            memory_pointer = (memory_pointer + 16 -1 )%16;
            break;
        case '+':
            memory.innerHTML = (parseInt(memory.innerHTML) + 1)%256;
            break;
        case '-':
            memory.innerHTML = (parseInt(memory.innerHTML) - 1)%256;
            break;
        case '.':
            document.getElementById('output').innerHTML +=  " " + memory.innerHTML;
            break;
        case ',':
            memory.innerHTML = inputs.shift();
            break;
        case '[':
            if (memory.innerHTML == 0){
                open_brackets = 1;
                while (open_brackets != 0){
                    code_pointer++;
                    if (code.value[code_pointer] == '['){
                        open_brackets++;
                    }else if (code.value[code_pointer] == ']'){
                        open_brackets--;
                    }
                }
            }
            break;   
        case ']':
            if (memory.innerHTML != 0){
                close_brackets = 1;
                while (close_brackets != 0){
                    code_pointer--;
                    if (code.value[code_pointer] == ']'){
                        close_brackets++;
                    }else if (code.value[code_pointer] == '['){
                        close_brackets--;
                    }
                }
            }
            break; 
    }
    if (code_pointer >= code.value.length-1){
        codeRunning = false;
        code_pointer = 0;
        document.getElementById('input').readOnly = false;
        document.getElementById('code').readOnly = false;
    }else{
        code_pointer++;
    }
}

var running = setInterval(()=>{
    if (codeRunning){
        runCode();
    }
}, speed*10);


document.getElementById('speed').addEventListener('change', ()=>{
    clearInterval(running);
    speed = 100 - document.getElementById('speed').value;
    running = setInterval(()=>{
        if (codeRunning){
            runCode();
        }
    }, speed*10);
});


document.getElementById('examples').addEventListener('change', (e)=>{
    const example = e.target.value;
    document.getElementById('reset').click();
    console.log(example);
    document.getElementById('code').value = examples[example];
});


document.getElementById('close').addEventListener('click', ()=>{
    if (document.getElementById('dialog')){
        const dialog = document.getElementById('dialog');
        dialog.classList.add('fade-out');
        setTimeout(()=>document.getElementById('dialog').remove(), 500);
    }
});