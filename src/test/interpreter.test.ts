//
// Note: This example test is leveraging the Mocha test framework.
// Please refer to their documentation on https://mochajs.org/ for help.
//

// The module 'assert' provides assertion methods from node
import * as assert from 'assert';

// You can import and use all API from the 'vscode' module
// as well as import your extension to test it
import * as vscode from 'vscode';
import { interpret, constructInterpreterPath} from '../interpreter';

const sep = require('path').sep;


// Defines a Mocha test suite to group tests of similar kind together
suite("Interpreter Tests", () => {

    // Defines a Mocha unit test
    test("Construct path for interpreter", () => {
        const result = constructInterpreterPath()
        const expected = __dirname.split(sep).slice(0, -2).join(sep) + '/src/python/source/interpreter.py';
        assert.equal(result, expected);
    });

    test("run interpreter with simple code 12", async () => {
        const code = '12';
        const expected = [{ 'begin': 0, 'end': 1, 'error_string': '', 'output_string': '', 'return_value': '12'}];
        const resultString = await interpret(code); 
        const result = JSON.parse(resultString);
        assert.deepEqual(result, expected);
    });

    test("run interpreter with with empty string", async () => {
        const code = '';
        const expected = [];
        const resultString = await interpret(code); 
        const result = JSON.parse(resultString);
        assert.deepEqual(result, expected);
    });

    test("run interpreter with long code", async () => {
        const code = `print('hello')

a = 12 + 11

def henk(piet):
    return 'henk en {}.'.format(piet)

henk('piet')

[(i,j) for j in range(2)
        for i in range(2)]

def long(alf, trump):
    assert(alf != trump)
    a = len(alf) - len(trump)
    if a == 0:
        return 'peanuts'
    elif a > 0:
        return 'alf is the real Trump'
    return 'Trump is the biggest alien'

a`;
        const expected =[
            {
                'begin': 0,
                'end': 1,
                'error_string': '',
                'output_string': 'hello',
                'return_value': ''
            },
            {
                'begin': 2,
                'end': 3,
                'error_string': '',
                'output_string': '',
                'return_value': ''
            },
            {
                'begin': 4,
                'end': 6,
                'error_string': '',
                'output_string': '',
                'return_value': ''
            },
            {
                'begin': 7,
                'end': 8,
                'error_string': '',
                'output_string': '',
                'return_value': 'henk en piet.'
            },
            {
                'begin': 9,
                'end': 11,
                'error_string': '',
                'output_string': '',
                'return_value': '[(0, 0), (1, 0), (0, 1), (1, 1)]'
            },
            {
                'begin': 12,
                'end': 20,
                'error_string': '',
                'output_string': '',
                'return_value': ''
            },
            {
                'begin': 21,
                'end': 22,
                'error_string': '',
                'output_string': '',
                'return_value': '23'
            },
        ];
        const resultString = await interpret(code); 
        const result = JSON.parse(resultString);
        assert.deepEqual(result, expected);
    });

    test("run interpreter with with empty string", async () => {
        const code = 'de';
        const expected = [
            {
                'begin': 0,
                'end': 1,
                'error_string': "name 'de' is not defined",
                'output_string': '',
                'return_value': ''
            },
        ];
        const resultString = await interpret(code); 
        const result = JSON.parse(resultString);
        assert.deepEqual(result, expected);
    });

    test("run interpreter with with empty string", async () => {
        const code = ` `;
        const expected = [];
        const resultString = await interpret(code); 
        const result = JSON.parse(resultString);
        assert.deepEqual(result, expected);
    });


});

