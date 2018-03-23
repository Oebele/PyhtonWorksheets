import { exec }  from 'child_process';
import { CodeAction } from 'vscode';
const sep = require('path').sep;


export function interpret(code:string): Promise<string> {
    const serverPath: string = constructInterpreterPath();
    let buff = new Buffer(code);  
    let base64data = buff.toString('base64');
    
    let command: string = `python3 "${serverPath}" -b "${base64data}"`;
    return new Promise<string> ((resolve, reject) => {
        exec(command, (error, stdout, stderr) => {
            if (error) {
                reject(error);
                return;
            }
            resolve(escape(stdout.trim()));
        });
    });
}
 

export function constructInterpreterPath(): string {
    return __dirname.split(sep).slice(0, -1).join(sep) +
        '/src/python/source/interpreter.py';
}

function escape(dirtyCode) {
    let newString = new Array(dirtyCode.length);
    let doubleQuotesOpen = false;
    for (let i = 0; i < dirtyCode.length; ++i) {
        let letter = dirtyCode[i];
        if (letter === '"') {
            newString[i] = letter;
            doubleQuotesOpen = !doubleQuotesOpen;
        } else if (letter === "'" && !doubleQuotesOpen) {
            newString[i] = '"';
        } else {
            newString[i] = letter;            
        }         
    }
    return newString.join('');
}
