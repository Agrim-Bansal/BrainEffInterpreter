let codeRunning = false;
document.getElementById

let memory_pointer = 0;
let code_pointer = 0;

document.getElementById('run').addEventListener('click', ()=>codeRunning = true);
document.getElementById('stop').addEventListener('click', ()=>codeRunning = false);

setInterval(()=>{
    if (codeRunning){
        document.getElementById('code').readOnly = true;
    }else{
        document.getElementById('code').readOnly = false;
    }
}, 10);




function codeCleanup(){
    console.log('Cleaning up')
    const code = document.getElementById('code');
    const allowedChars = '[],.<>+_';
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

document.getElementById('code').addEventListener('change', (e)=>{
    e.target.innerHTML = e.target.value;
});

function toggleCodeStatic(){
    console.log('Toggling code static');
    const code = document.getElementById('code');
    console.log(code.readOnly);
    if (code.readOnly){
        code.readOnly = false;
        return;
    }else{
        code.readOnly = true;
        return;
    }
}

function runCode(){
    codeCleanup();
    const codeElement = document.getElementById('code');
    const code = codeElement.value;
    char = code[code_pointer];
    memory = document.getElementsByClassName('memory-container')[0].children[i];

    switch (char){
        case '>':
            memory_pointer += 1;
            break;
        case '<':
            memory_pointer -= 1;
            break;
        case '+':
            memory.innerHTML = parseInt(memory.innerHTML) + 1;
            break;
        case '-':
            memory.innerHTML = parseInt(memory.innerHTML) - 1;
            break;
        case '.':
            document.getElementById('output').innerHTML += String.fromCharCode(parseInt(memory.innerHTML));
            break;
    }
    code_pointer++;
}
