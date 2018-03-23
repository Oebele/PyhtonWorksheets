'use strict';
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import { interpret } from './interpreter';

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('Congratulations, your extension "open-editor-and-add-extension" is now active!');
    // The command has been defined in the package.json file
    // Now provide the implementation of the command with  registerCommand
    // The commandId parameter must match the command field in package.json
    let disposable = vscode.commands.registerCommand('extension.pythonWorkSheet', () => {
        // The code you place here will be executed every time your command is executed

        let options: Object = {
            content: "'Welcome to python worksheet'",
            language: "python"
        };

        vscode.workspace.openTextDocument(options).then(doc => {
            vscode.window.showTextDocument(doc, vscode.ViewColumn.One);
            // create a new word counter
            let worksheet = new WorkSheet();
            let controller = new WorkSheetController(worksheet, doc);

            // add to a list of disposables which are disposed when this extension
            // is deactivated again.
        }, err => {
            vscode.window.showErrorMessage(err);
        });
    });

    context.subscriptions.push(disposable);
}

// this method is called when your extension is deactivated
export function deactivate() {
}

export class WorkSheet {

    private statusBarItem: vscode.StatusBarItem;
    private ErrorDecorationType: vscode.TextEditorDecorationType;
    private OutputDecorationType: vscode.TextEditorDecorationType;
    private ResultDecorationType: vscode.TextEditorDecorationType;
    private errorCodeWithLineNumber: RegExp;
    private errorCodesLineNumber: RegExp;

    public constructor() {
        this.ErrorDecorationType = vscode.window.createTextEditorDecorationType({
            before: { color: 'red', margin: '0 0 0 1em', },
            rangeBehavior: vscode.DecorationRangeBehavior.ClosedClosed
        });
        this.OutputDecorationType = vscode.window.createTextEditorDecorationType({
            before: { color: 'Silver', margin: '0 0 0 1em', },
            rangeBehavior: vscode.DecorationRangeBehavior.ClosedClosed
        });
        this.ResultDecorationType = vscode.window.createTextEditorDecorationType({
            after: { color: 'green', margin: '0 0 0 1em', },
            rangeBehavior: vscode.DecorationRangeBehavior.ClosedClosed
        });
        this.errorCodeWithLineNumber = new RegExp('line [0-9]+', 'g');
        this.errorCodesLineNumber = new RegExp('[0-9]+', 'g');
    }

    public updateWordCount(document: vscode.TextDocument) {

        // Create as needed
        if (!this.statusBarItem) {
            this.statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left);
        }

        // Get the current text editor
        this.parse(document)
            .catch(e => console.error(e));

    }

    public async parse(document: vscode.TextDocument): Promise<void> {
        const errorTexts: vscode.DecorationOptions[] = [];
        const outputTexts: vscode.DecorationOptions[] = [];
        const resultTexts: vscode.DecorationOptions[] = [];

        let docContent = document.getText();
        // Parse out unwanted whitespace so the split is accurate
        const resultString = await interpret(docContent);
        let results;
        try {
            results = JSON.parse(resultString);
        } catch(e) {
            console.error(resultString, ' ==> ' ,e);
        }

        for (const result of results) {
            let beginLine: vscode.TextLine = document.lineAt(result.end-1);
            let startPos = new vscode.Position(beginLine.range.end.line, beginLine.range.end.character);
            let endPos = new vscode.Position(beginLine.range.end.line, beginLine.range.end.character);

            this.createResultDecorations(result, startPos, endPos, resultTexts);
            this.createOutputDecorations(result, startPos, endPos, outputTexts);
            this.createErrorDecorations(result, beginLine, document, startPos, endPos, errorTexts);

            vscode.window.activeTextEditor.setDecorations(this.ErrorDecorationType, errorTexts);
            vscode.window.activeTextEditor.setDecorations(this.OutputDecorationType, outputTexts);
            vscode.window.activeTextEditor.setDecorations(this.ResultDecorationType, resultTexts);
        }
    }

    private createErrorDecorations(result: any, beginLine: vscode.TextLine, document: vscode.TextDocument, startPos: vscode.Position, endPos: vscode.Position, errorTexts: vscode.DecorationOptions[]) {
        if (result['error_string']) {
            let message: string = result['error_string'].replace(/\s+/g, ' ').trim();
            let array = message.match(this.errorCodeWithLineNumber);
            if (array !== null && array.length > 0) {
                const messageLine = parseInt(array[0].match(this.errorCodesLineNumber)[0]) - 1;
                beginLine = document.lineAt(messageLine);
                startPos = new vscode.Position(beginLine.range.end.line, beginLine.range.end.character);
                endPos = new vscode.Position(beginLine.range.end.line, beginLine.range.end.character);
            }
            message = message.replace(/\s+/g, ' ').trim();
            const decoration = { range: new vscode.Range(startPos, endPos), renderOptions: { before: { contentText: message } } };
            errorTexts.push(decoration);
        }
    }

    private createOutputDecorations(result: any, startPos: vscode.Position, endPos: vscode.Position, outputTexts: vscode.DecorationOptions[]) {
        if (result['output_string']) {
            let message: string = result['output_string'].replace(/\s+/g, ' ').trim();
            const decoration = { range: new vscode.Range(startPos, endPos), renderOptions: { before: { contentText: message } } };
            outputTexts.push(decoration);
        }
    }

    private createResultDecorations(result: any, startPos: vscode.Position, endPos: vscode.Position, resultTexts: vscode.DecorationOptions[]) {
        if (result['return_value']) {
            let message: string = result['return_value'].replace(/\s+/g, ' ').trim();
            const decoration = { range: new vscode.Range(startPos, endPos), renderOptions: { after: { contentText: message } } };
            resultTexts.push(decoration);
        }
    }

    public hideIcon() {
        this.statusBarItem.hide();
    }

    public dispose() {
        this.statusBarItem.dispose();
    }

}

class WorkSheetController {

    private _worksheet: WorkSheet;
    private _disposable: vscode.Disposable;
    private _document: vscode.TextDocument;

    constructor(worksheet: WorkSheet, document: vscode.TextDocument) {
        this._worksheet = worksheet;
        this._worksheet.updateWordCount(document);
        this._document = document;

        // subscribe to selection change and editor activation events
        let subscriptions: vscode.Disposable[] = [];
        vscode.workspace.onDidChangeTextDocument(this._onEvent, this, subscriptions);

        // create a combined disposable from both event subscriptions
        this._disposable = vscode.Disposable.from(...subscriptions);
    }

    private _onEvent() {
        let editor = vscode.window.activeTextEditor;
        if (editor && editor.document === this._document) {
            this._worksheet.updateWordCount(this._document);
        } else {
            this._worksheet.hideIcon();
        }
    }

    public dispose() {
        let editor = vscode.window.activeTextEditor;
        if (editor && editor.document === this._document) {
            this._disposable.dispose();
        }
    }
}

