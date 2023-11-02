"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[712],{

/***/ 58986:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {


// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "q": () => (/* binding */ Debugger)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var index_js_ = __webpack_require__(76351);
;// CONCATENATED MODULE: ../packages/debugger/lib/hash.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
// Most of the implementation below is adapted from the following repository:
// https://github.com/garycourt/murmurhash-js/blob/master/murmurhash2_gc.js
// Which has the following MIT License:
//
// Copyright (c) 2011 Gary Court
// Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
// to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
// and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
// The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
//  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
// The implementation below uses case fallthrough as part of the algorithm.
/* eslint-disable no-fallthrough */
const m = 0x5bd1e995;
const encoder = new TextEncoder();
/**
 * Calculate the murmurhash2 for a given string and seed.
 *
 * @param str The string to calculate the Murmur2 hash for.
 * @param seed The seed.
 *
 * @returns The Murmurhash2 hash.
 */
function murmur2(str, seed) {
    const data = encoder.encode(str);
    let len = data.length;
    let h = seed ^ len;
    let i = 0;
    while (len >= 4) {
        let k = (data[i] & 0xff) |
            ((data[++i] & 0xff) << 8) |
            ((data[++i] & 0xff) << 16) |
            ((data[++i] & 0xff) << 24);
        k = (k & 0xffff) * m + ((((k >>> 16) * m) & 0xffff) << 16);
        k ^= k >>> 24;
        k = (k & 0xffff) * m + ((((k >>> 16) * m) & 0xffff) << 16);
        h = ((h & 0xffff) * m + ((((h >>> 16) * m) & 0xffff) << 16)) ^ k;
        len -= 4;
        ++i;
    }
    switch (len) {
        case 3:
            h ^= (data[i + 2] & 0xff) << 16;
        case 2:
            h ^= (data[i + 1] & 0xff) << 8;
        case 1:
            h ^= data[i] & 0xff;
            h = (h & 0xffff) * m + ((((h >>> 16) * m) & 0xffff) << 16);
    }
    h ^= h >>> 13;
    h = (h & 0xffff) * m + ((((h >>> 16) * m) & 0xffff) << 16);
    h ^= h >>> 15;
    return h >>> 0;
}

;// CONCATENATED MODULE: ../packages/debugger/lib/config.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A class that holds debugger configuration for all kernels.
 */
class DebuggerConfig {
    constructor() {
        this._fileParams = new Map();
        this._hashMethods = new Map();
    }
    /**
     * Returns an id based on the given code.
     *
     * @param code The source code.
     * @param kernel The kernel name from current session.
     */
    getCodeId(code, kernel) {
        const fileParams = this._fileParams.get(kernel);
        if (!fileParams) {
            throw new Error(`Kernel (${kernel}) has no tmp file params.`);
        }
        const hash = this._hashMethods.get(kernel);
        if (!hash) {
            throw new Error(`Kernel (${kernel}) has no hashing params.`);
        }
        const { prefix, suffix } = fileParams;
        return `${prefix}${hash(code)}${suffix}`;
    }
    /**
     * Sets the hash parameters for a kernel.
     *
     * @param params - Hashing parameters for a kernel.
     */
    setHashParams(params) {
        const { kernel, method, seed } = params;
        if (!kernel) {
            throw new TypeError(`Kernel name is not defined.`);
        }
        switch (method) {
            case 'Murmur2':
                this._hashMethods.set(kernel, code => murmur2(code, seed).toString());
                break;
            default:
                throw new Error(`Hash method (${method}) is not supported.`);
        }
    }
    /**
     * Sets the parameters used by the kernel to create temp files (e.g. cells).
     *
     * @param params - Temporary file prefix and suffix for a kernel.
     */
    setTmpFileParams(params) {
        const { kernel, prefix, suffix } = params;
        if (!kernel) {
            throw new TypeError(`Kernel name is not defined.`);
        }
        this._fileParams.set(kernel, { kernel, prefix, suffix });
    }
    /**
     * Gets the parameters used for the temp files (e.e. cells) for a kernel.
     *
     * @param kernel - The kernel name from current session.
     */
    getTmpFileParams(kernel) {
        return this._fileParams.get(kernel);
    }
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var lib_index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/cells@~4.1.0-alpha.2 (strict) (fallback: ../packages/cells/lib/index.js)
var cells_lib_index_js_ = __webpack_require__(51955);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/debugger/lib/dialogs/evaluate.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */



/**
 * A namespace for DebuggerEvaluateDialog statics.
 */
var DebuggerEvaluateDialog;
(function (DebuggerEvaluateDialog) {
    /**
     * Create and show a dialog to prompt user for code.
     *
     * @param options - The dialog setup options.
     *
     * @returns A promise that resolves with whether the dialog was accepted
     */
    function getCode(options) {
        const dialog = new EvaluateDialog({
            ...options,
            body: new EvaluateDialogBody(options),
            buttons: [
                lib_index_js_.Dialog.cancelButton({ label: options.cancelLabel }),
                lib_index_js_.Dialog.okButton({ label: options.okLabel })
            ]
        });
        return dialog.launch();
    }
    DebuggerEvaluateDialog.getCode = getCode;
})(DebuggerEvaluateDialog || (DebuggerEvaluateDialog = {}));
/**
 * A dialog to prompt users for code to evaluate.
 */
class EvaluateDialog extends lib_index_js_.Dialog {
    /**
     * Handle the DOM events for the Evaluate dialog.
     *
     * @param event The DOM event sent to the dialog widget
     */
    handleEvent(event) {
        if (event.type === 'keydown') {
            const keyboardEvent = event;
            const { code, shiftKey } = keyboardEvent;
            if (shiftKey && code === 'Enter') {
                return this.resolve();
            }
            if (code === 'Enter') {
                return;
            }
        }
        super.handleEvent(event);
    }
}
/**
 * Widget body with a code cell prompt in a dialog
 */
class EvaluateDialogBody extends index_es6_js_.Widget {
    /**
     * CodePromptDialog constructor
     *
     * @param options Constructor options
     */
    constructor(options) {
        super();
        const { contentFactory, rendermime, mimeType } = options;
        const model = new cells_lib_index_js_.CodeCellModel();
        model.mimeType = mimeType !== null && mimeType !== void 0 ? mimeType : '';
        this._prompt = new cells_lib_index_js_.CodeCell({
            contentFactory,
            rendermime,
            model,
            placeholder: false
        }).initializeState();
        // explicitly remove the prompt in front of the input area
        this._prompt.inputArea.promptNode.remove();
        this.node.appendChild(this._prompt.node);
    }
    /**
     * Get the text specified by the user
     */
    getValue() {
        return this._prompt.model.sharedModel.getSource();
    }
    /**
     *  A message handler invoked on an `'after-attach'` message.
     */
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        this._prompt.activate();
    }
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/codeeditor@~4.1.0-alpha.2 (singleton) (fallback: ../packages/codeeditor/lib/index.js)
var codeeditor_lib_index_js_ = __webpack_require__(40200);
;// CONCATENATED MODULE: ../packages/debugger/lib/factory.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A widget factory for read only editors.
 */
class factory_ReadOnlyEditorFactory {
    /**
     * Construct a new editor widget factory.
     *
     * @param options The instantiation options for a ReadOnlyEditorFactory.
     */
    constructor(options) {
        this._services = options.editorServices;
    }
    /**
     * Create a new CodeEditorWrapper given a Source.
     *
     * @param source The source to create a new editor for.
     */
    createNewEditor(source) {
        const { content, mimeType, path } = source;
        const factory = this._services.factoryService.newInlineEditor;
        const mimeTypeService = this._services.mimeTypeService;
        const model = new codeeditor_lib_index_js_.CodeEditor.Model({
            mimeType: mimeType || mimeTypeService.getMimeTypeByFilePath(path)
        });
        model.sharedModel.source = content;
        const editor = new codeeditor_lib_index_js_.CodeEditorWrapper({
            editorOptions: {
                config: {
                    readOnly: true,
                    lineNumbers: true
                }
            },
            model,
            factory
        });
        editor.node.setAttribute('data-jp-debugger', 'true');
        editor.disposed.connect(() => {
            model.dispose();
        });
        return editor;
    }
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/observables@~5.1.0-alpha.2 (strict) (fallback: ../packages/observables/lib/index.js)
var observables_lib_index_js_ = __webpack_require__(57090);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(30205);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var coreutils_lib_index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: consume shared module (default) @codemirror/state@^6.2.0 (singleton) (fallback: ../node_modules/@codemirror/state/dist/index.js)
var dist_index_js_ = __webpack_require__(42904);
// EXTERNAL MODULE: consume shared module (default) @codemirror/view@^6.9.6 (singleton) (fallback: ../node_modules/@codemirror/view/dist/index.js)
var view_dist_index_js_ = __webpack_require__(87801);
;// CONCATENATED MODULE: ../packages/debugger/lib/handlers/editor.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * The class name added to the current line.
 */
const LINE_HIGHLIGHT_CLASS = 'jp-DebuggerEditor-highlight';
/**
 * The timeout for listening to editor content changes.
 */
const EDITOR_CHANGED_TIMEOUT = 1000;
/**
 * A handler for a CodeEditor.IEditor.
 */
class editor_EditorHandler {
    /**
     * Instantiate a new EditorHandler.
     *
     * @param options The instantiation options for a EditorHandler.
     */
    constructor(options) {
        var _a, _b, _c, _d;
        this._src = options.src;
        this._id = (_c = (_b = (_a = options.debuggerService.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.id) !== null && _c !== void 0 ? _c : '';
        this._path = (_d = options.path) !== null && _d !== void 0 ? _d : '';
        this._debuggerService = options.debuggerService;
        this._editor = options.getEditor;
        this._editorMonitor = new coreutils_lib_index_js_.ActivityMonitor({
            signal: this._src.changed,
            timeout: EDITOR_CHANGED_TIMEOUT
        });
        this._editorMonitor.activityStopped.connect(() => {
            this._sendEditorBreakpoints();
        }, this);
        this._debuggerService.model.breakpoints.changed.connect(async () => {
            const editor = this.editor;
            if (!editor || editor.isDisposed) {
                return;
            }
            this._addBreakpointsToEditor();
        });
        this._debuggerService.model.breakpoints.restored.connect(async () => {
            const editor = this.editor;
            if (!editor || editor.isDisposed) {
                return;
            }
            this._addBreakpointsToEditor();
        });
        this._debuggerService.model.callstack.currentFrameChanged.connect(() => {
            const editor = this.editor;
            if (editor) {
                editor_EditorHandler.clearHighlight(editor);
            }
        });
        this._breakpointEffect = dist_index_js_.StateEffect.define({
            map: (value, mapping) => ({ pos: value.pos.map(v => mapping.mapPos(v)) })
        });
        this._breakpointState = dist_index_js_.StateField.define({
            create: () => {
                return dist_index_js_.RangeSet.empty;
            },
            update: (breakpoints, transaction) => {
                breakpoints = breakpoints.map(transaction.changes);
                for (let ef of transaction.effects) {
                    if (ef.is(this._breakpointEffect)) {
                        let e = ef;
                        if (e.value.pos.length) {
                            breakpoints = breakpoints.update({
                                add: e.value.pos.map(v => Private.breakpointMarker.range(v)),
                                sort: true
                            });
                        }
                        else {
                            breakpoints = dist_index_js_.RangeSet.empty;
                        }
                    }
                }
                return breakpoints;
            }
        });
        this._gutter = new dist_index_js_.Compartment();
        this._highlightDeco = view_dist_index_js_.Decoration.line({ class: LINE_HIGHLIGHT_CLASS });
        this._highlightState = dist_index_js_.StateField.define({
            create: () => {
                return view_dist_index_js_.Decoration.none;
            },
            update: (highlights, transaction) => {
                highlights = highlights.map(transaction.changes);
                for (let ef of transaction.effects) {
                    if (ef.is(editor_EditorHandler._highlightEffect)) {
                        let e = ef;
                        if (e.value.pos.length) {
                            highlights = highlights.update({
                                add: e.value.pos.map(v => this._highlightDeco.range(v))
                            });
                        }
                        else {
                            highlights = view_dist_index_js_.Decoration.none;
                        }
                    }
                }
                return highlights;
            },
            provide: f => view_dist_index_js_.EditorView.decorations.from(f)
        });
        void options.editorReady().then(() => {
            this._setupEditor();
        });
    }
    /**
     * The editor
     */
    get editor() {
        return this._editor();
    }
    /**
     * Dispose the handler.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._editorMonitor.dispose();
        this._clearEditor();
        this.isDisposed = true;
        dist_index_es6_js_.Signal.clearData(this);
    }
    /**
     * Refresh the breakpoints display
     */
    refreshBreakpoints() {
        this._addBreakpointsToEditor();
    }
    /**
     * Setup the editor.
     */
    _setupEditor() {
        const editor = this.editor;
        if (!editor || editor.isDisposed) {
            return;
        }
        editor.setOption('lineNumbers', true);
        const breakpointGutter = [
            this._breakpointState,
            this._highlightState,
            dist_index_js_.Prec.highest((0,view_dist_index_js_.gutter)({
                class: 'cm-breakpoint-gutter',
                renderEmptyElements: true,
                markers: v => v.state.field(this._breakpointState),
                initialSpacer: () => Private.breakpointMarker,
                domEventHandlers: {
                    mousedown: (view, line) => {
                        this._onGutterClick(view, line.from);
                        return true;
                    }
                }
            }))
        ];
        editor.injectExtension(this._gutter.of(breakpointGutter));
        this._addBreakpointsToEditor();
    }
    /**
     * Clear the editor by removing visual elements and handlers.
     */
    _clearEditor() {
        const editor = this.editor;
        if (!editor || editor.isDisposed) {
            return;
        }
        editor_EditorHandler.clearHighlight(editor);
        this._clearGutter(editor);
        editor.setOption('lineNumbers', false);
        editor.editor.dispatch({
            effects: this._gutter.reconfigure([])
        });
    }
    /**
     * Send the breakpoints from the editor UI via the debug service.
     */
    _sendEditorBreakpoints() {
        var _a;
        if ((_a = this.editor) === null || _a === void 0 ? void 0 : _a.isDisposed) {
            return;
        }
        const breakpoints = this._getBreakpointsFromEditor().map(lineNumber => {
            var _a, _b;
            return Private.createBreakpoint(((_b = (_a = this._debuggerService.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.name) || '', lineNumber);
        });
        void this._debuggerService.updateBreakpoints(this._src.getSource(), breakpoints, this._path);
    }
    /**
     * Handle a click on the gutter.
     *
     * @param editor The editor from where the click originated.
     * @param position The position corresponding to the click event.
     */
    _onGutterClick(editor, position) {
        var _a, _b, _c;
        if (this._id !== ((_b = (_a = this._debuggerService.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.id)) {
            return;
        }
        const lineNumber = editor.state.doc.lineAt(position).number;
        let stateBreakpoints = editor.state.field(this._breakpointState);
        let hasBreakpoint = false;
        stateBreakpoints.between(position, position, () => {
            hasBreakpoint = true;
        });
        let breakpoints = this._getBreakpoints();
        if (hasBreakpoint) {
            breakpoints = breakpoints.filter(ele => ele.line !== lineNumber);
        }
        else {
            breakpoints.push(Private.createBreakpoint((_c = this._path) !== null && _c !== void 0 ? _c : this._debuggerService.session.connection.name, lineNumber));
        }
        breakpoints.sort((a, b) => {
            return a.line - b.line;
        });
        void this._debuggerService.updateBreakpoints(this._src.getSource(), breakpoints, this._path);
    }
    /**
     * Add the breakpoints to the editor.
     */
    _addBreakpointsToEditor() {
        var _a, _b;
        if (this._id !== ((_b = (_a = this._debuggerService.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.id)) {
            return;
        }
        const editor = this.editor;
        const breakpoints = this._getBreakpoints();
        this._clearGutter(editor);
        const breakpointPos = breakpoints.map(b => {
            return editor.state.doc.line(b.line).from;
        });
        editor.editor.dispatch({
            effects: this._breakpointEffect.of({ pos: breakpointPos })
        });
    }
    /**
     * Retrieve the breakpoints from the editor.
     */
    _getBreakpointsFromEditor() {
        const editor = this.editor;
        const breakpoints = editor.editor.state.field(this._breakpointState);
        let lines = [];
        breakpoints.between(0, editor.doc.length, (from) => {
            lines.push(editor.doc.lineAt(from).number);
        });
        return lines;
    }
    _clearGutter(editor) {
        if (!editor) {
            return;
        }
        const view = editor.editor;
        view.dispatch({
            effects: this._breakpointEffect.of({ pos: [] })
        });
    }
    /**
     * Get the breakpoints for the editor using its content (code),
     * or its path (if it exists).
     */
    _getBreakpoints() {
        const code = this._src.getSource();
        return this._debuggerService.model.breakpoints.getBreakpoints(this._path || this._debuggerService.getCodeId(code));
    }
}
/**
 * A namespace for EditorHandler `statics`.
 */
(function (EditorHandler) {
    EditorHandler._highlightEffect = dist_index_js_.StateEffect.define({
        map: (value, mapping) => ({ pos: value.pos.map(v => mapping.mapPos(v)) })
    });
    /**
     * Highlight the current line of the frame in the given editor.
     *
     * @param editor The editor to highlight.
     * @param line The line number.
     */
    function showCurrentLine(editor, line) {
        clearHighlight(editor);
        const cmEditor = editor;
        const linePos = cmEditor.doc.line(line).from;
        cmEditor.editor.dispatch({
            effects: EditorHandler._highlightEffect.of({ pos: [linePos] })
        });
    }
    EditorHandler.showCurrentLine = showCurrentLine;
    /**
     * Remove all line highlighting indicators for the given editor.
     *
     * @param editor The editor to cleanup.
     */
    function clearHighlight(editor) {
        if (!editor || editor.isDisposed) {
            return;
        }
        const cmEditor = editor;
        cmEditor.editor.dispatch({
            effects: EditorHandler._highlightEffect.of({ pos: [] })
        });
    }
    EditorHandler.clearHighlight = clearHighlight;
})(editor_EditorHandler || (editor_EditorHandler = {}));
/**
 * A namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * Create a marker DOM element for a breakpoint.
     */
    Private.breakpointMarker = new (class extends view_dist_index_js_.GutterMarker {
        toDOM() {
            const marker = document.createTextNode('●');
            return marker;
        }
    })();
    /**
     * Create a new breakpoint.
     *
     * @param session The name of the session.
     * @param line The line number of the breakpoint.
     */
    function createBreakpoint(session, line) {
        return {
            line,
            verified: true,
            source: {
                name: session
            }
        };
    }
    Private.createBreakpoint = createBreakpoint;
})(Private || (Private = {}));

;// CONCATENATED MODULE: ../packages/debugger/lib/handlers/console.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * A handler for consoles.
 */
class ConsoleHandler {
    /**
     * Instantiate a new ConsoleHandler.
     *
     * @param options The instantiation options for a ConsoleHandler.
     */
    constructor(options) {
        this._debuggerService = options.debuggerService;
        this._consolePanel = options.widget;
        this._cellMap = new observables_lib_index_js_.ObservableMap();
        const codeConsole = this._consolePanel.console;
        if (codeConsole.promptCell) {
            this._addEditorHandler(codeConsole.promptCell);
        }
        codeConsole.promptCellCreated.connect((_, cell) => {
            this._addEditorHandler(cell);
        });
        const addHandlers = () => {
            for (const cell of codeConsole.cells) {
                this._addEditorHandler(cell);
            }
        };
        addHandlers();
        this._consolePanel.console.cells.changed.connect(addHandlers);
    }
    /**
     * Dispose the handler.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.isDisposed = true;
        this._cellMap.values().forEach(handler => handler.dispose());
        this._cellMap.dispose();
        dist_index_es6_js_.Signal.clearData(this);
    }
    /**
     * Add a new editor handler for the given cell.
     *
     * @param cell The cell to add the handler to.
     */
    _addEditorHandler(cell) {
        const modelId = cell.model.id;
        if (cell.model.type !== 'code' || this._cellMap.has(modelId)) {
            return;
        }
        const codeCell = cell;
        const editorHandler = new editor_EditorHandler({
            debuggerService: this._debuggerService,
            editorReady: async () => {
                await codeCell.ready;
                return codeCell.editor;
            },
            getEditor: () => codeCell.editor,
            src: cell.model.sharedModel
        });
        codeCell.disposed.connect(() => {
            this._cellMap.delete(modelId);
            editorHandler.dispose();
        });
        this._cellMap.set(modelId, editorHandler);
    }
}

;// CONCATENATED MODULE: ../packages/debugger/lib/handlers/file.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * A handler for files.
 */
class FileHandler {
    /**
     * Instantiate a new FileHandler.
     *
     * @param options The instantiation options for a FileHandler.
     */
    constructor(options) {
        var _a;
        this._debuggerService = options.debuggerService;
        this._fileEditor = options.widget.content;
        this._hasLineNumber =
            (_a = this._fileEditor.editor.getOption('lineNumbers')) !== null && _a !== void 0 ? _a : false;
        this._editorHandler = new editor_EditorHandler({
            debuggerService: this._debuggerService,
            editorReady: () => Promise.resolve(this._fileEditor.editor),
            getEditor: () => this._fileEditor.editor,
            src: this._fileEditor.model.sharedModel
        });
    }
    /**
     * Dispose the handler.
     */
    dispose() {
        var _a, _b;
        if (this.isDisposed) {
            return;
        }
        this.isDisposed = true;
        (_a = this._editorHandler) === null || _a === void 0 ? void 0 : _a.dispose();
        // Restore editor options
        (_b = this._editorHandler) === null || _b === void 0 ? void 0 : _b.editor.setOptions({
            lineNumbers: this._hasLineNumber
        });
        dist_index_es6_js_.Signal.clearData(this);
    }
}

;// CONCATENATED MODULE: ../packages/debugger/lib/handlers/notebook.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * A handler for notebooks.
 */
class NotebookHandler {
    /**
     * Instantiate a new NotebookHandler.
     *
     * @param options The instantiation options for a NotebookHandler.
     */
    constructor(options) {
        this._debuggerService = options.debuggerService;
        this._notebookPanel = options.widget;
        this._cellMap = new observables_lib_index_js_.ObservableMap();
        const notebook = this._notebookPanel.content;
        notebook.model.cells.changed.connect(this._onCellsChanged, this);
        this._onCellsChanged();
    }
    /**
     * Dispose the handler.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.isDisposed = true;
        this._cellMap.values().forEach(handler => {
            var _a;
            handler.dispose();
            // Ensure to restore notebook editor settings
            (_a = handler.editor) === null || _a === void 0 ? void 0 : _a.setOptions({
                ...this._notebookPanel.content.editorConfig.code
            });
        });
        this._cellMap.dispose();
        dist_index_es6_js_.Signal.clearData(this);
    }
    /**
     * Handle a notebook cells changed event.
     */
    _onCellsChanged(cells, changes) {
        var _a;
        this._notebookPanel.content.widgets.forEach(cell => this._addEditorHandler(cell));
        if ((changes === null || changes === void 0 ? void 0 : changes.type) === 'move') {
            for (const cell of changes.newValues) {
                (_a = this._cellMap.get(cell.id)) === null || _a === void 0 ? void 0 : _a.refreshBreakpoints();
            }
        }
    }
    /**
     * Add a new editor handler for the given cell.
     *
     * @param cell The cell to add the handler to.
     */
    _addEditorHandler(cell) {
        const modelId = cell.model.id;
        if (cell.model.type !== 'code' || this._cellMap.has(modelId)) {
            return;
        }
        const codeCell = cell;
        const editorHandler = new editor_EditorHandler({
            debuggerService: this._debuggerService,
            editorReady: async () => {
                await codeCell.ready;
                return codeCell.editor;
            },
            getEditor: () => codeCell.editor,
            src: cell.model.sharedModel
        });
        codeCell.disposed.connect(() => {
            this._cellMap.delete(modelId);
            editorHandler.dispose();
        });
        this._cellMap.set(cell.model.id, editorHandler);
    }
}

;// CONCATENATED MODULE: ../packages/debugger/lib/handler.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






const TOOLBAR_DEBUGGER_ITEM = 'debugger-icon';
/**
 * Add a bug icon to the widget toolbar to enable and disable debugging.
 *
 * @param widget The widget to add the debug toolbar button to.
 * @param onClick The callback when the toolbar button is clicked.
 */
function updateIconButton(widget, onClick, enabled, pressed, translator = translation_lib_index_js_.nullTranslator) {
    const trans = translator.load('jupyterlab');
    const icon = new index_js_.ToolbarButton({
        className: 'jp-DebuggerBugButton',
        icon: index_js_.bugIcon,
        tooltip: trans.__('Enable Debugger'),
        pressedIcon: index_js_.bugDotIcon,
        pressedTooltip: trans.__('Disable Debugger'),
        disabledTooltip: trans.__('Select a kernel that supports debugging to enable debugger'),
        enabled,
        pressed,
        onClick
    });
    if (!widget.toolbar.insertBefore('kernelName', TOOLBAR_DEBUGGER_ITEM, icon)) {
        widget.toolbar.addItem(TOOLBAR_DEBUGGER_ITEM, icon);
    }
    return icon;
}
/**
 * Updates button state to on/off,
 * adds/removes css class to update styling
 *
 * @param widget the debug button widget
 * @param pressed true if pressed, false otherwise
 * @param enabled true if widget enabled, false otherwise
 * @param onClick click handler
 */
function updateIconButtonState(widget, pressed, enabled = true, onClick) {
    if (widget) {
        widget.enabled = enabled;
        widget.pressed = pressed;
        if (onClick) {
            widget.onClick = onClick;
        }
    }
}
/**
 * A handler for debugging a widget.
 */
class DebuggerHandler {
    /**
     * Instantiate a new DebuggerHandler.
     *
     * @param options The instantiation options for a DebuggerHandler.
     */
    constructor(options) {
        this._handlers = {};
        this._contextKernelChangedHandlers = {};
        this._kernelChangedHandlers = {};
        this._statusChangedHandlers = {};
        this._iopubMessageHandlers = {};
        this._iconButtons = {};
        this._type = options.type;
        this._shell = options.shell;
        this._service = options.service;
    }
    /**
     * Get the active widget.
     */
    get activeWidget() {
        return this._activeWidget;
    }
    /**
     * Update a debug handler for the given widget, and
     * handle kernel changed events.
     *
     * @param widget The widget to update.
     * @param connection The session connection.
     */
    async update(widget, connection) {
        if (!connection) {
            delete this._kernelChangedHandlers[widget.id];
            delete this._statusChangedHandlers[widget.id];
            delete this._iopubMessageHandlers[widget.id];
            return this.updateWidget(widget, connection);
        }
        const kernelChanged = () => {
            void this.updateWidget(widget, connection);
        };
        const kernelChangedHandler = this._kernelChangedHandlers[widget.id];
        if (kernelChangedHandler) {
            connection.kernelChanged.disconnect(kernelChangedHandler);
        }
        this._kernelChangedHandlers[widget.id] = kernelChanged;
        connection.kernelChanged.connect(kernelChanged);
        const statusChanged = (_, status) => {
            if (status.endsWith('restarting')) {
                void this.updateWidget(widget, connection);
            }
        };
        const statusChangedHandler = this._statusChangedHandlers[widget.id];
        if (statusChangedHandler) {
            connection.statusChanged.disconnect(statusChangedHandler);
        }
        connection.statusChanged.connect(statusChanged);
        this._statusChangedHandlers[widget.id] = statusChanged;
        const iopubMessage = (_, msg) => {
            if (msg.parent_header.msg_type ==
                'execute_request' &&
                this._service.isStarted &&
                !this._service.hasStoppedThreads()) {
                void this._service.displayDefinedVariables();
            }
        };
        const iopubMessageHandler = this._iopubMessageHandlers[widget.id];
        if (iopubMessageHandler) {
            connection.iopubMessage.disconnect(iopubMessageHandler);
        }
        connection.iopubMessage.connect(iopubMessage);
        this._iopubMessageHandlers[widget.id] = iopubMessage;
        this._activeWidget = widget;
        return this.updateWidget(widget, connection);
    }
    /**
     * Update a debug handler for the given widget, and
     * handle connection kernel changed events.
     *
     * @param widget The widget to update.
     * @param sessionContext The session context.
     */
    async updateContext(widget, sessionContext) {
        const connectionChanged = () => {
            const { session: connection } = sessionContext;
            void this.update(widget, connection);
        };
        const contextKernelChangedHandlers = this._contextKernelChangedHandlers[widget.id];
        if (contextKernelChangedHandlers) {
            sessionContext.kernelChanged.disconnect(contextKernelChangedHandlers);
        }
        this._contextKernelChangedHandlers[widget.id] = connectionChanged;
        sessionContext.kernelChanged.connect(connectionChanged);
        return this.update(widget, sessionContext.session);
    }
    /**
     * Update a debug handler for the given widget.
     *
     * @param widget The widget to update.
     * @param connection The session connection.
     */
    async updateWidget(widget, connection) {
        var _a, _b, _c, _d;
        if (!this._service.model || !connection) {
            return;
        }
        const hasFocus = () => {
            return this._shell.currentWidget === widget;
        };
        const updateAttribute = () => {
            if (!this._handlers[widget.id]) {
                widget.node.removeAttribute('data-jp-debugger');
                return;
            }
            widget.node.setAttribute('data-jp-debugger', 'true');
        };
        const createHandler = () => {
            if (this._handlers[widget.id]) {
                return;
            }
            switch (this._type) {
                case 'notebook':
                    this._handlers[widget.id] = new NotebookHandler({
                        debuggerService: this._service,
                        widget: widget
                    });
                    break;
                case 'console':
                    this._handlers[widget.id] = new ConsoleHandler({
                        debuggerService: this._service,
                        widget: widget
                    });
                    break;
                case 'file':
                    this._handlers[widget.id] = new FileHandler({
                        debuggerService: this._service,
                        widget: widget
                    });
                    break;
                default:
                    throw Error(`No handler for the type ${this._type}`);
            }
            updateAttribute();
        };
        const removeHandlers = () => {
            var _a, _b, _c, _d;
            const handler = this._handlers[widget.id];
            if (!handler) {
                return;
            }
            handler.dispose();
            delete this._handlers[widget.id];
            delete this._kernelChangedHandlers[widget.id];
            delete this._statusChangedHandlers[widget.id];
            delete this._iopubMessageHandlers[widget.id];
            delete this._contextKernelChangedHandlers[widget.id];
            // Clear the model if the handler being removed corresponds
            // to the current active debug session, or if the connection
            // does not have a kernel.
            if (((_b = (_a = this._service.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.path) === (connection === null || connection === void 0 ? void 0 : connection.path) ||
                !((_d = (_c = this._service.session) === null || _c === void 0 ? void 0 : _c.connection) === null || _d === void 0 ? void 0 : _d.kernel)) {
                const model = this._service.model;
                model.clear();
            }
            updateAttribute();
        };
        const addToolbarButton = (enabled = true) => {
            const debugButton = this._iconButtons[widget.id];
            if (!debugButton) {
                this._iconButtons[widget.id] = updateIconButton(widget, toggleDebugging, this._service.isStarted, enabled);
            }
            else {
                updateIconButtonState(debugButton, this._service.isStarted, enabled, toggleDebugging);
            }
        };
        const isDebuggerOn = () => {
            var _a;
            return (this._service.isStarted &&
                ((_a = this._previousConnection) === null || _a === void 0 ? void 0 : _a.id) === (connection === null || connection === void 0 ? void 0 : connection.id));
        };
        const stopDebugger = async () => {
            this._service.session.connection = connection;
            await this._service.stop();
        };
        const startDebugger = async () => {
            var _a, _b;
            this._service.session.connection = connection;
            this._previousConnection = connection;
            await this._service.restoreState(true);
            await this._service.displayDefinedVariables();
            if ((_b = (_a = this._service.session) === null || _a === void 0 ? void 0 : _a.capabilities) === null || _b === void 0 ? void 0 : _b.supportsModulesRequest) {
                await this._service.displayModules();
            }
        };
        const toggleDebugging = async () => {
            // bail if the widget doesn't have focus
            if (!hasFocus()) {
                return;
            }
            const debugButton = this._iconButtons[widget.id];
            if (isDebuggerOn()) {
                await stopDebugger();
                removeHandlers();
                updateIconButtonState(debugButton, false);
            }
            else {
                await startDebugger();
                createHandler();
                updateIconButtonState(debugButton, true);
            }
        };
        addToolbarButton(false);
        // listen to the disposed signals
        widget.disposed.connect(async () => {
            if (isDebuggerOn()) {
                await stopDebugger();
            }
            removeHandlers();
            delete this._iconButtons[widget.id];
            delete this._contextKernelChangedHandlers[widget.id];
        });
        const debuggingEnabled = await this._service.isAvailable(connection);
        if (!debuggingEnabled) {
            removeHandlers();
            updateIconButtonState(this._iconButtons[widget.id], false, false);
            return;
        }
        // update the active debug session
        if (!this._service.session) {
            this._service.session = new Debugger.Session({
                connection,
                config: this._service.config
            });
        }
        else {
            this._previousConnection = ((_a = this._service.session.connection) === null || _a === void 0 ? void 0 : _a.kernel)
                ? this._service.session.connection
                : null;
            this._service.session.connection = connection;
        }
        await this._service.restoreState(false);
        if (this._service.isStarted && !this._service.hasStoppedThreads()) {
            await this._service.displayDefinedVariables();
            if ((_c = (_b = this._service.session) === null || _b === void 0 ? void 0 : _b.capabilities) === null || _c === void 0 ? void 0 : _c.supportsModulesRequest) {
                await this._service.displayModules();
            }
        }
        updateIconButtonState(this._iconButtons[widget.id], this._service.isStarted, true);
        // check the state of the debug session
        if (!this._service.isStarted) {
            removeHandlers();
            this._service.session.connection = (_d = this._previousConnection) !== null && _d !== void 0 ? _d : connection;
            await this._service.restoreState(false);
            return;
        }
        // if the debugger is started but there is no handler, create a new one
        createHandler();
        this._previousConnection = connection;
    }
}

;// CONCATENATED MODULE: ../packages/debugger/style/icons/close-all.svg
const close_all_namespaceObject = "<svg width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\">\n  <g class=\"jp-icon3\" fill=\"#616161\">\n    <path d=\"M16.4805 17.2481C16.8158 16.3972 17 15.4701 17 14.5C17 10.3579 13.6421 7.00001 9.5 7.00001C8.36314 7.00001 7.28536 7.25295 6.31986 7.70564C7.60064 6.0592 9.60074 5 11.8482 5C15.7142 5 18.8482 8.13401 18.8482 12C18.8482 14.0897 17.9325 15.9655 16.4805 17.2481Z\" />\n    <path d=\"M19.1607 14.2481C19.496 13.3971 19.6801 12.4701 19.6801 11.5C19.6801 7.35786 16.3223 4 12.1801 4C11.0433 4 9.9655 4.25295 9.00001 4.70563C10.2808 3.05919 12.2809 2 14.5284 2C18.3944 2 21.5284 5.134 21.5284 9C21.5284 11.0897 20.6127 12.9655 19.1607 14.2481Z\" />\n    <path d=\"M16 15C16 18.866 12.866 22 9 22C5.13401 22 2 18.866 2 15C2 11.134 5.13401 8 9 8C12.866 8 16 11.134 16 15ZM11.7914 11L13 12.2086L10.2086 15L13 17.7914L11.7914 19L9 16.2086L6.20857 19L5 17.7914L7.79143 15L5 12.2086L6.20857 11L9 13.7914L11.7914 11Z\" />\n    </g>\n</svg>\n";
;// CONCATENATED MODULE: ../packages/debugger/style/icons/step-into.svg
const step_into_namespaceObject = "<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\">\n\t<g class=\"jp-icon3\" fill=\"#616161\">\n\t\t<path d=\"M7.99998 9.53198H8.54198L12.447 5.62698L11.386 4.56698L8.74898 7.17698L8.74898 0.999985H7.99998H7.25098L7.25098 7.17698L4.61398 4.56698L3.55298 5.62698L7.45798 9.53198H7.99998ZM9.95598 13.013C9.95598 14.1175 9.06055 15.013 7.95598 15.013C6.85141 15.013 5.95598 14.1175 5.95598 13.013C5.95598 11.9084 6.85141 11.013 7.95598 11.013C9.06055 11.013 9.95598 11.9084 9.95598 13.013Z\"/>\n\t</g>\n</svg>\n";
;// CONCATENATED MODULE: ../packages/debugger/style/icons/step-out.svg
const step_out_namespaceObject = "<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\">\n\t<g class=\"jp-icon3\" fill=\"#616161\">\n\t\t<path d=\"M7.99998 1H7.45798L3.55298 4.905L4.61398 5.965L7.25098 3.355V9.532H7.99998H8.74898V3.355L11.386 5.965L12.447 4.905L8.54198 1H7.99998ZM9.95598 13.013C9.95598 14.1176 9.06055 15.013 7.95598 15.013C6.85141 15.013 5.95598 14.1176 5.95598 13.013C5.95598 11.9084 6.85141 11.013 7.95598 11.013C9.06055 11.013 9.95598 11.9084 9.95598 13.013Z\"/>\n\t</g>\n</svg>\n";
;// CONCATENATED MODULE: ../packages/debugger/style/icons/step-over.svg
const step_over_namespaceObject = "<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" xmlns=\"http://www.w3.org/2000/svg\">\n\t<g class=\"jp-icon3\" fill=\"#616161\">\n\t\t<path d=\"M14.25 5.75V1.75H12.75V4.2916C11.605 2.93303 9.83899 2.08334 7.90914 2.08334C4.73316 2.08334 1.98941 4.39036 1.75072 7.48075L1.72992 7.75H3.231L3.25287 7.5241C3.46541 5.32932 5.45509 3.58334 7.90914 3.58334C9.6452 3.58334 11.1528 4.45925 11.9587 5.75H9.12986V7.25H13.292L14.2535 6.27493V5.75H14.25ZM7.99997 14C9.10454 14 9.99997 13.1046 9.99997 12C9.99997 10.8954 9.10454 10 7.99997 10C6.8954 10 5.99997 10.8954 5.99997 12C5.99997 13.1046 6.8954 14 7.99997 14Z\"/>\n\t</g>\n</svg>\n";
;// CONCATENATED MODULE: ../packages/debugger/style/icons/variable.svg
const variable_namespaceObject = "<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M1.5 4L1 4.5V12.5L1.5 13H4V12H2V5H4V4H1.5ZM14.5 13L15 12.5L15 4.5L14.5 4H12V5L14 5L14 12H12V13H14.5ZM8.79693 5L4.29693 7L4 7.45691V9.95691L4.24275 10.3857L6.74275 11.8857L7.20307 11.9138L11.7031 9.91381L12 9.45691V6.95691L11.7572 6.52816L9.25725 5.02816L8.79693 5ZM5 8.34V9.67381L6.5 10.5738V9.24L5 8.34ZM7.5 9.28184V10.6875L11 9.13197V7.72629L7.5 9.28184ZM10.4178 6.89071L8.96559 6.01936L5.58216 7.52311L7.03441 8.39445L10.4178 6.89071Z\" fill=\"#007ACC\"/>\n</svg>\n";
;// CONCATENATED MODULE: ../packages/debugger/style/icons/pause.svg
const pause_namespaceObject = "<svg height=\"24\" viewBox=\"0 0 24 24\" width=\"24\" xmlns=\"http://www.w3.org/2000/svg\">\n    <g class=\"jp-icon3\" fill=\"#616161\">\n        <path d=\"m 7,6 h 4 V 18 H 7 Z\" />\n        <path d=\"m 13,6 h 4 v 12 h -4 z\" />\n    </g>\n</svg>\n";
;// CONCATENATED MODULE: ../packages/debugger/style/icons/view-breakpoint.svg
const view_breakpoint_namespaceObject = "<svg width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\">\n    <g class=\"jp-icon3\" fill=\"#616161\">\n        <path d=\"M5 2H15L20 7V20C20 20.5304 19.7893 21.0391 19.4142 21.4142C19.0391 21.7893 18.5304 22 18 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V14H4V16L8 13L4 10V12H3V4C3 3.46957 3.21071 2.96086 3.58579 2.58579C3.96086 2.21071 4.46957 2 5 2ZM12 18H16V16H12V18ZM12 14H18V12H12V14ZM12 10H18V8H12V10ZM10 14C10.5523 14 11 13.5523 11 13C11 12.4477 10.5523 12 10 12C9.44771 12 9 12.4477 9 13C9 13.5523 9.44771 14 10 14Z\"/>\n        <path d=\"M3 12V14H1V13V12H3Z\"/>\n    </g>\n</svg>\n";
;// CONCATENATED MODULE: ../packages/debugger/style/icons/open-kernel-source.svg
const open_kernel_source_namespaceObject = "<svg width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\">\n    <g class=\"jp-icon3\" fill=\"#616161\">\n        <path d=\"M5 2H15L20 7V20C20 20.5304 19.7893 21.0391 19.4142 21.4142C19.0391 21.7893 18.5304 22 18 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V14H4V16L8 13L4 10V12H3V4C3 3.46957 3.21071 2.96086 3.58579 2.58579C3.96086 2.21071 4.46957 2 5 2ZM12 18H16V16H12V18ZM12 14H18V12H12V14ZM12 10H18V8H12V10ZM10 14C10.5523 14 11 13.5523 11 13C11 12.4477 10.5523 12 10 12C9.44771 12 9 12.4477 9 13C9 13.5523 9.44771 14 10 14Z\"/>\n        <path d=\"M3 12V14H1V13V12H3Z\"/>\n    </g>\n</svg>\n";
;// CONCATENATED MODULE: ../packages/debugger/style/icons/exceptions.svg
const exceptions_namespaceObject = "<svg height=\"24\" width=\"24\" viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\">\n  <g class=\"jp-icon3\" fill=\"#616161\" transform=\"matrix(1.1999396,0,0,1.3858273,-2.3726971,-4.6347192)\">\n    <path\n      d=\"M 12.023438,0.30859375 11.158203,1.8085937 -1.2382812,23.285156 l 26.5292972,-0.002 z m 0.002,3.99999995 9.800781,16.9746093 -19.6015626,0.002 z\"\n      transform=\"matrix(0.72509832,0,0,0.7247701,3.2918397,3.480876)\"\n    />\n    <path d=\"m 11.144475,9.117095 h 1.666751 v 7.215906 h -1.666751 z\" />\n    <path d=\"m 11.144475,17.054592 h 1.666751 v 1.443181 h -1.666751 z\" />\n  </g>\n</svg>\n";
;// CONCATENATED MODULE: ../packages/debugger/lib/icons.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.











const closeAllIcon = new index_js_.LabIcon({
    name: 'debugger:close-all',
    svgstr: close_all_namespaceObject
});
const exceptionIcon = new index_js_.LabIcon({
    name: 'debugger:pause-on-exception',
    svgstr: exceptions_namespaceObject
});
const pauseIcon = new index_js_.LabIcon({
    name: 'debugger:pause',
    svgstr: pause_namespaceObject
});
const stepIntoIcon = new index_js_.LabIcon({
    name: 'debugger:step-into',
    svgstr: step_into_namespaceObject
});
const stepOverIcon = new index_js_.LabIcon({
    name: 'debugger:step-over',
    svgstr: step_over_namespaceObject
});
const stepOutIcon = new index_js_.LabIcon({
    name: 'debugger:step-out',
    svgstr: step_out_namespaceObject
});
const variableIcon = new index_js_.LabIcon({
    name: 'debugger:variable',
    svgstr: variable_namespaceObject
});
const viewBreakpointIcon = new index_js_.LabIcon({
    name: 'debugger:view-breakpoint',
    svgstr: view_breakpoint_namespaceObject
});
const openKernelSourceIcon = new index_js_.LabIcon({
    name: 'debugger:open-kernel-source',
    svgstr: open_kernel_source_namespaceObject
});

;// CONCATENATED MODULE: ../packages/debugger/lib/panels/breakpoints/model.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A model for a list of breakpoints.
 */
class BreakpointsModel {
    constructor() {
        this._breakpoints = new Map();
        this._changed = new dist_index_es6_js_.Signal(this);
        this._restored = new dist_index_es6_js_.Signal(this);
        this._clicked = new dist_index_es6_js_.Signal(this);
    }
    /**
     * Signal emitted when the model changes.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Signal emitted when the breakpoints are restored.
     */
    get restored() {
        return this._restored;
    }
    /**
     * Signal emitted when a breakpoint is clicked.
     */
    get clicked() {
        return this._clicked;
    }
    /**
     * Get all the breakpoints.
     */
    get breakpoints() {
        return this._breakpoints;
    }
    /**
     * Set the breakpoints for a given id (path).
     *
     * @param id The code id (path).
     * @param breakpoints The list of breakpoints.
     */
    setBreakpoints(id, breakpoints) {
        this._breakpoints.set(id, breakpoints);
        this._changed.emit(breakpoints);
    }
    /**
     * Get the breakpoints for a given id (path).
     *
     * @param id The code id (path).
     */
    getBreakpoints(id) {
        var _a;
        return (_a = this._breakpoints.get(id)) !== null && _a !== void 0 ? _a : [];
    }
    /**
     * Restore a map of breakpoints.
     *
     * @param breakpoints The map of breakpoints
     */
    restoreBreakpoints(breakpoints) {
        this._breakpoints = breakpoints;
        this._restored.emit();
    }
}

;// CONCATENATED MODULE: ../packages/debugger/lib/panels/callstack/model.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A model for a callstack.
 */
class CallstackModel {
    constructor() {
        this._state = [];
        this._currentFrame = null;
        this._framesChanged = new dist_index_es6_js_.Signal(this);
        this._currentFrameChanged = new dist_index_es6_js_.Signal(this);
    }
    /**
     * Get all the frames.
     */
    get frames() {
        return this._state;
    }
    /**
     * Set the frames.
     */
    set frames(newFrames) {
        this._state = newFrames;
        const currentFrameId = this.frame !== null ? model_Private.getFrameId(this.frame) : '';
        const frame = newFrames.find(frame => model_Private.getFrameId(frame) === currentFrameId);
        // Default to the first frame if the previous one can't be found.
        // Otherwise keep the current frame selected.
        if (!frame) {
            this.frame = newFrames[0];
        }
        this._framesChanged.emit(newFrames);
    }
    /**
     * Get the current frame.
     */
    get frame() {
        return this._currentFrame;
    }
    /**
     * Set the current frame.
     */
    set frame(frame) {
        this._currentFrame = frame;
        this._currentFrameChanged.emit(frame);
    }
    /**
     * Signal emitted when the frames have changed.
     */
    get framesChanged() {
        return this._framesChanged;
    }
    /**
     * Signal emitted when the current frame has changed.
     */
    get currentFrameChanged() {
        return this._currentFrameChanged;
    }
}
/**
 * A namespace for private data.
 */
var model_Private;
(function (Private) {
    /**
     * Construct an id for the given frame.
     *
     * @param frame The frame.
     */
    function getFrameId(frame) {
        var _a;
        return `${(_a = frame === null || frame === void 0 ? void 0 : frame.source) === null || _a === void 0 ? void 0 : _a.path}-${frame === null || frame === void 0 ? void 0 : frame.id}`;
    }
    Private.getFrameId = getFrameId;
})(model_Private || (model_Private = {}));

;// CONCATENATED MODULE: ../packages/debugger/lib/panels/sources/model.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The model to keep track of the current source being displayed.
 */
class SourcesModel {
    /**
     * Instantiate a new Sources.Model
     *
     * @param options The Sources.Model instantiation options.
     */
    constructor(options) {
        this._currentSourceOpened = new dist_index_es6_js_.Signal(this);
        this._currentSourceChanged = new dist_index_es6_js_.Signal(this);
        this.currentFrameChanged = options.currentFrameChanged;
    }
    /**
     * Signal emitted when a source should be open in the main area.
     */
    get currentSourceOpened() {
        return this._currentSourceOpened;
    }
    /**
     * Signal emitted when the current source changes.
     */
    get currentSourceChanged() {
        return this._currentSourceChanged;
    }
    /**
     * Return the current source.
     */
    get currentSource() {
        return this._currentSource;
    }
    /**
     * Set the current source.
     *
     * @param source The source to set as the current source.
     */
    set currentSource(source) {
        this._currentSource = source;
        this._currentSourceChanged.emit(source);
    }
    /**
     * Open a source in the main area.
     */
    open() {
        this._currentSourceOpened.emit(this._currentSource);
    }
}

// EXTERNAL MODULE: consume shared module (default) @lumino/polling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/polling/dist/index.es6.js)
var polling_dist_index_es6_js_ = __webpack_require__(81967);
;// CONCATENATED MODULE: ../packages/debugger/lib/panels/kernelSources/model.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * The rate limit for the filter debouncer
 */
const DEBOUNCER_RATE_LIMIT_MS = 500;
const compare = (a, b) => {
    if (a.name < b.name) {
        return -1;
    }
    if (a.name > b.name) {
        return 1;
    }
    return 0;
};
/**
 * The model to keep track of the current source being displayed.
 */
class KernelSourcesModel {
    constructor() {
        this._filteredKernelSources = null;
        this._filter = '';
        this._isDisposed = false;
        this._kernelSources = null;
        this._changed = new dist_index_es6_js_.Signal(this);
        this._filterChanged = new dist_index_es6_js_.Signal(this);
        this._kernelSourceOpened = new dist_index_es6_js_.Signal(this);
        this.refresh = this.refresh.bind(this);
        this._refreshDebouncer = new polling_dist_index_es6_js_.Debouncer(this.refresh, DEBOUNCER_RATE_LIMIT_MS);
    }
    /**
     * Get the filter.
     */
    get filter() {
        return this._filter;
    }
    /**
     * Set the filter.
     * The update
     */
    set filter(filter) {
        this._filter = filter;
        this._filterChanged.emit(filter);
        void this._refreshDebouncer.invoke();
    }
    /**
     * Whether the kernel sources model is disposed or not.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Get the kernel sources.
     */
    get kernelSources() {
        return this._kernelSources;
    }
    /**
     * Set the kernel sources and emit a changed signal.
     */
    set kernelSources(kernelSources) {
        this._kernelSources = kernelSources;
        this.refresh();
    }
    /**
     * Signal emitted when the current source changes.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Signal emitted when the current source changes.
     */
    get filterChanged() {
        return this._filterChanged;
    }
    /**
     * Signal emitted when a kernel source should be open in the main area.
     */
    get kernelSourceOpened() {
        return this._kernelSourceOpened;
    }
    /**
     * Dispose the kernel sources model
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._refreshDebouncer.dispose();
        dist_index_es6_js_.Signal.clearData(this);
    }
    /**
     * Open a source in the main area.
     */
    open(kernelSource) {
        this._kernelSourceOpened.emit(kernelSource);
    }
    getFilteredKernelSources() {
        const regexp = new RegExp(this._filter);
        return this._kernelSources.filter(module => regexp.test(module.name));
    }
    refresh() {
        if (this._kernelSources) {
            this._filteredKernelSources = this._filter
                ? this.getFilteredKernelSources()
                : this._kernelSources;
            this._filteredKernelSources.sort(compare);
        }
        else {
            this._kernelSources = new Array();
            this._filteredKernelSources = new Array();
        }
        this._changed.emit(this._filteredKernelSources);
    }
}

;// CONCATENATED MODULE: ../packages/debugger/lib/panels/variables/model.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A model for a variable explorer.
 */
class VariablesModel {
    constructor() {
        this._selectedVariable = null;
        this._state = [];
        this._variableExpanded = new dist_index_es6_js_.Signal(this);
        this._changed = new dist_index_es6_js_.Signal(this);
    }
    /**
     * Get all the scopes.
     */
    get scopes() {
        return this._state;
    }
    /**
     * Set the scopes.
     */
    set scopes(scopes) {
        this._state = scopes;
        this._changed.emit();
    }
    /**
     * Signal emitted when the current variable has changed.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Signal emitted when the current variable has been expanded.
     */
    get variableExpanded() {
        return this._variableExpanded;
    }
    get selectedVariable() {
        return this._selectedVariable;
    }
    set selectedVariable(selection) {
        this._selectedVariable = selection;
    }
    /**
     * Expand a variable.
     *
     * @param variable The variable to expand.
     */
    expandVariable(variable) {
        this._variableExpanded.emit(variable);
    }
}

;// CONCATENATED MODULE: ../packages/debugger/lib/model.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






/**
 * A model for a debugger.
 */
class DebuggerModel {
    /**
     * Instantiate a new DebuggerModel
     */
    constructor() {
        this._disposed = new dist_index_es6_js_.Signal(this);
        this._isDisposed = false;
        this._hasRichVariableRendering = false;
        this._supportCopyToGlobals = false;
        this._stoppedThreads = new Set();
        this._title = '-';
        this._titleChanged = new dist_index_es6_js_.Signal(this);
        this.breakpoints = new BreakpointsModel();
        this.callstack = new CallstackModel();
        this.variables = new VariablesModel();
        this.sources = new SourcesModel({
            currentFrameChanged: this.callstack.currentFrameChanged
        });
        this.kernelSources = new KernelSourcesModel();
    }
    /**
     * A signal emitted when the debugger widget is disposed.
     */
    get disposed() {
        return this._disposed;
    }
    /**
     * Whether the kernel support rich variable rendering based on mime type.
     */
    get hasRichVariableRendering() {
        return this._hasRichVariableRendering;
    }
    set hasRichVariableRendering(v) {
        this._hasRichVariableRendering = v;
    }
    /**
     * Whether the kernel supports the copyToGlobals request.
     */
    get supportCopyToGlobals() {
        return this._supportCopyToGlobals;
    }
    set supportCopyToGlobals(v) {
        this._supportCopyToGlobals = v;
    }
    /**
     * Whether the model is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * The set of threads in stopped state.
     */
    get stoppedThreads() {
        return this._stoppedThreads;
    }
    /**
     * Assigns the parameters to the set of threads in stopped state.
     */
    set stoppedThreads(threads) {
        this._stoppedThreads = threads;
    }
    /**
     * The current debugger title.
     */
    get title() {
        return this._title;
    }
    /**
     * Set the current debugger title.
     */
    set title(title) {
        if (title === this._title) {
            return;
        }
        this._title = title !== null && title !== void 0 ? title : '-';
        this._titleChanged.emit(title);
    }
    /**
     * A signal emitted when the title changes.
     */
    get titleChanged() {
        return this._titleChanged;
    }
    /**
     * Dispose the model.
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        this.kernelSources.dispose();
        this._disposed.emit();
    }
    /**
     * Clear the model.
     */
    clear() {
        this._stoppedThreads.clear();
        const breakpoints = new Map();
        this.breakpoints.restoreBreakpoints(breakpoints);
        this.callstack.frames = [];
        this.variables.scopes = [];
        this.sources.currentSource = null;
        this.kernelSources.kernelSources = null;
        this.title = '-';
    }
}

;// CONCATENATED MODULE: ../packages/debugger/lib/panels/variables/grid.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A data grid that displays variables in a debugger session.
 */
class VariablesBodyGrid extends index_es6_js_.Panel {
    /**
     * Instantiate a new VariablesBodyGrid.
     *
     * @param options The instantiation options for a VariablesBodyGrid.
     */
    constructor(options) {
        super();
        this._filter = new Set();
        this._grid = null;
        this._pending = null;
        this.commands = options.commands;
        this.model = options.model;
        this.themeManager = options.themeManager;
        this.translator = options.translator;
        this.model.changed.connect(() => this.update(), this);
        this.addClass('jp-DebuggerVariables-body');
    }
    /**
     * The variable filter list.
     */
    get filter() {
        return this._filter;
    }
    set filter(filter) {
        this._filter = filter;
        this.update();
    }
    /**
     * The current scope of the variables.
     */
    get scope() {
        return this._scope;
    }
    set scope(scope) {
        this._scope = scope;
        if (scope !== 'Globals') {
            this.addClass('jp-debuggerVariables-local');
        }
        else {
            this.removeClass('jp-debuggerVariables-local');
        }
        this.update();
    }
    /**
     * Load the grid panel implementation and instantiate a grid.
     */
    async initialize() {
        if (this._grid || this._pending) {
            return;
        }
        // Lazily load the datagrid module when the first grid is requested.
        const { Grid } = await (this._pending = Promise.all(/* import() */[__webpack_require__.e(2942), __webpack_require__.e(2107)]).then(__webpack_require__.bind(__webpack_require__, 32107)));
        const { commands, model, themeManager, translator } = this;
        this._grid = new Grid({ commands, model, themeManager, translator });
        this._grid.addClass('jp-DebuggerVariables-grid');
        this._pending = null;
        this.addWidget(this._grid);
        this.update();
    }
    /**
     * Wait until actually displaying the grid to trigger initialization.
     */
    onBeforeShow(msg) {
        if (!this._grid && !this._pending) {
            void this.initialize();
        }
        super.onBeforeShow(msg);
    }
    /**
     * Handle `update-request` messages.
     */
    onUpdateRequest(msg) {
        var _a;
        if (this._grid) {
            const { dataModel } = this._grid;
            dataModel.filter = this._filter;
            dataModel.scope = this._scope;
            dataModel.setData((_a = this.model.scopes) !== null && _a !== void 0 ? _a : []);
        }
        super.onUpdateRequest(msg);
    }
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/rendermime@~4.1.0-alpha.2 (singleton) (fallback: ../packages/rendermime/lib/index.js)
var rendermime_lib_index_js_ = __webpack_require__(66866);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var coreutils_dist_index_js_ = __webpack_require__(22100);
;// CONCATENATED MODULE: ../packages/debugger/lib/panels/variables/mimerenderer.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */






const RENDERER_PANEL_CLASS = 'jp-VariableRendererPanel';
const RENDERER_PANEL_RENDERER_CLASS = 'jp-VariableRendererPanel-renderer';
/**
 * Debugger variable mime type renderer
 */
class VariableMimeRenderer extends lib_index_js_.MainAreaWidget {
    /**
     * Instantiate a new VariableMimeRenderer.
     */
    constructor(options) {
        const { dataLoader, rendermime, translator } = options;
        const content = new index_es6_js_.Panel();
        const loaded = new coreutils_dist_index_js_.PromiseDelegate();
        super({
            content,
            reveal: Promise.all([dataLoader, loaded.promise])
        });
        this.content.addClass(RENDERER_PANEL_CLASS);
        this.trans = (translator !== null && translator !== void 0 ? translator : translation_lib_index_js_.nullTranslator).load('jupyterlab');
        this.dataLoader = dataLoader;
        this.renderMime = rendermime;
        this._dataHash = null;
        this.refresh()
            .then(() => {
            loaded.resolve();
        })
            .catch(reason => loaded.reject(reason));
    }
    /**
     * Refresh the variable view
     */
    async refresh(force = false) {
        let data = await this.dataLoader();
        if (Object.keys(data.data).length === 0) {
            data = {
                data: {
                    'text/plain': this.trans.__('The variable is undefined in the active context.')
                },
                metadata: {}
            };
        }
        if (data.data) {
            const hash = murmur2(JSON.stringify(data), 17);
            if (force || this._dataHash !== hash) {
                if (this.content.layout) {
                    this.content.widgets.forEach(w => {
                        this.content.layout.removeWidget(w);
                    });
                }
                // We trust unconditionally the data as the user is required to
                // execute the code to load a particular variable in memory
                const mimeType = this.renderMime.preferredMimeType(data.data, 'any');
                if (mimeType) {
                    const widget = this.renderMime.createRenderer(mimeType);
                    widget.addClass(RENDERER_PANEL_RENDERER_CLASS);
                    const model = new rendermime_lib_index_js_.MimeModel({ ...data, trusted: true });
                    this._dataHash = hash;
                    await widget.renderModel(model);
                    this.content.addWidget(widget);
                }
                else {
                    this._dataHash = null;
                    return Promise.reject('Unable to determine the preferred mime type.');
                }
            }
        }
        else {
            this._dataHash = null;
            return Promise.reject('Unable to get a view on the variable.');
        }
    }
}

;// CONCATENATED MODULE: ../packages/debugger/lib/service.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * A concrete implementation of the IDebugger interface.
 */
class DebuggerService {
    /**
     * Instantiate a new DebuggerService.
     *
     * @param options The instantiation options for a DebuggerService.
     */
    constructor(options) {
        var _a, _b;
        this._eventMessage = new dist_index_es6_js_.Signal(this);
        this._isDisposed = false;
        this._sessionChanged = new dist_index_es6_js_.Signal(this);
        this._pauseOnExceptionChanged = new dist_index_es6_js_.Signal(this);
        this._config = options.config;
        // Avoids setting session with invalid client
        // session should be set only when a notebook or
        // a console get the focus.
        // TODO: also checks that the notebook or console
        // runs a kernel with debugging ability
        this._session = null;
        this._specsManager = (_a = options.specsManager) !== null && _a !== void 0 ? _a : null;
        this._model = new Debugger.Model();
        this._debuggerSources = (_b = options.debuggerSources) !== null && _b !== void 0 ? _b : null;
        this._trans = (options.translator || translation_lib_index_js_.nullTranslator).load('jupyterlab');
    }
    /**
     * Signal emitted for debug event messages.
     */
    get eventMessage() {
        return this._eventMessage;
    }
    /**
     * Get debugger config.
     */
    get config() {
        return this._config;
    }
    /**
     * Whether the debug service is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Whether the current debugger is started.
     */
    get isStarted() {
        var _a, _b;
        return (_b = (_a = this._session) === null || _a === void 0 ? void 0 : _a.isStarted) !== null && _b !== void 0 ? _b : false;
    }
    /**
     * A signal emitted when the pause on exception filter changes.
     */
    get pauseOnExceptionChanged() {
        return this._pauseOnExceptionChanged;
    }
    /**
     * Returns the debugger service's model.
     */
    get model() {
        return this._model;
    }
    /**
     * Returns the current debug session.
     */
    get session() {
        return this._session;
    }
    /**
     * Sets the current debug session to the given parameter.
     *
     * @param session - the new debugger session.
     */
    set session(session) {
        var _a;
        if (this._session === session) {
            return;
        }
        if (this._session) {
            this._session.dispose();
        }
        this._session = session;
        (_a = this._session) === null || _a === void 0 ? void 0 : _a.eventMessage.connect((_, event) => {
            if (event.event === 'stopped') {
                this._model.stoppedThreads.add(event.body.threadId);
                void this._getAllFrames();
            }
            else if (event.event === 'continued') {
                this._model.stoppedThreads.delete(event.body.threadId);
                this._clearModel();
                this._clearSignals();
            }
            this._eventMessage.emit(event);
        });
        this._sessionChanged.emit(session);
    }
    /**
     * Signal emitted upon session changed.
     */
    get sessionChanged() {
        return this._sessionChanged;
    }
    /**
     * Dispose the debug service.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        dist_index_es6_js_.Signal.clearData(this);
    }
    /**
     * Computes an id based on the given code.
     *
     * @param code The source code.
     */
    getCodeId(code) {
        var _a, _b, _c, _d;
        try {
            return this._config.getCodeId(code, (_d = (_c = (_b = (_a = this.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.name) !== null && _d !== void 0 ? _d : '');
        }
        catch (_e) {
            return '';
        }
    }
    /**
     * Whether there exists a thread in stopped state.
     */
    hasStoppedThreads() {
        var _a, _b;
        return (_b = ((_a = this._model) === null || _a === void 0 ? void 0 : _a.stoppedThreads.size) > 0) !== null && _b !== void 0 ? _b : false;
    }
    /**
     * Request whether debugging is available for the session connection.
     *
     * @param connection The session connection.
     */
    async isAvailable(connection) {
        var _a, _b, _c, _d;
        if (!this._specsManager) {
            return true;
        }
        await this._specsManager.ready;
        const kernel = connection === null || connection === void 0 ? void 0 : connection.kernel;
        if (!kernel) {
            return false;
        }
        const name = kernel.name;
        if (!((_a = this._specsManager.specs) === null || _a === void 0 ? void 0 : _a.kernelspecs[name])) {
            return true;
        }
        return !!((_d = (_c = (_b = this._specsManager.specs.kernelspecs[name]) === null || _b === void 0 ? void 0 : _b.metadata) === null || _c === void 0 ? void 0 : _c['debugger']) !== null && _d !== void 0 ? _d : false);
    }
    /**
     * Clear all the breakpoints for the current session.
     */
    async clearBreakpoints() {
        var _a;
        if (((_a = this.session) === null || _a === void 0 ? void 0 : _a.isStarted) !== true) {
            return;
        }
        this._model.breakpoints.breakpoints.forEach((_, path, map) => {
            void this._setBreakpoints([], path);
        });
        let bpMap = new Map();
        this._model.breakpoints.restoreBreakpoints(bpMap);
    }
    /**
     * Continues the execution of the current thread.
     */
    async continue() {
        try {
            if (!this.session) {
                throw new Error('No active debugger session');
            }
            await this.session.sendRequest('continue', {
                threadId: this._currentThread()
            });
            this._model.stoppedThreads.delete(this._currentThread());
            this._clearModel();
            this._clearSignals();
        }
        catch (err) {
            console.error('Error:', err.message);
        }
    }
    /**
     * Retrieve the content of a source file.
     *
     * @param source The source object containing the path to the file.
     */
    async getSource(source) {
        var _a, _b;
        if (!this.session) {
            throw new Error('No active debugger session');
        }
        const reply = await this.session.sendRequest('source', {
            source,
            sourceReference: (_a = source.sourceReference) !== null && _a !== void 0 ? _a : 0
        });
        return { ...reply.body, path: (_b = source.path) !== null && _b !== void 0 ? _b : '' };
    }
    /**
     * Evaluate an expression.
     *
     * @param expression The expression to evaluate as a string.
     */
    async evaluate(expression) {
        var _a;
        if (!this.session) {
            throw new Error('No active debugger session');
        }
        const frameId = (_a = this.model.callstack.frame) === null || _a === void 0 ? void 0 : _a.id;
        const reply = await this.session.sendRequest('evaluate', {
            context: 'repl',
            expression,
            frameId
        });
        if (!reply.success) {
            return null;
        }
        // get the frames to retrieve the latest state of the variables
        this._clearModel();
        await this._getAllFrames();
        return reply.body;
    }
    /**
     * Makes the current thread run again for one step.
     */
    async next() {
        try {
            if (!this.session) {
                throw new Error('No active debugger session');
            }
            await this.session.sendRequest('next', {
                threadId: this._currentThread()
            });
        }
        catch (err) {
            console.error('Error:', err.message);
        }
    }
    /**
     * Request rich representation of a variable.
     *
     * @param variableName The variable name to request
     * @param frameId The current frame id in which to request the variable
     * @returns The mime renderer data model
     */
    async inspectRichVariable(variableName, frameId) {
        if (!this.session) {
            throw new Error('No active debugger session');
        }
        const reply = await this.session.sendRequest('richInspectVariables', {
            variableName,
            frameId
        });
        if (reply.success) {
            return reply.body;
        }
        else {
            throw new Error(reply.message);
        }
    }
    /**
     * Request variables for a given variable reference.
     *
     * @param variablesReference The variable reference to request.
     */
    async inspectVariable(variablesReference) {
        if (!this.session) {
            throw new Error('No active debugger session');
        }
        const reply = await this.session.sendRequest('variables', {
            variablesReference
        });
        if (reply.success) {
            return reply.body.variables;
        }
        else {
            throw new Error(reply.message);
        }
    }
    /**
     * Request to set a variable in the global scope.
     *
     * @param name The name of the variable.
     */
    async copyToGlobals(name) {
        if (!this.session) {
            throw new Error('No active debugger session');
        }
        if (!this.model.supportCopyToGlobals) {
            throw new Error('The "copyToGlobals" request is not supported by the kernel');
        }
        const frames = this.model.callstack.frames;
        this.session
            .sendRequest('copyToGlobals', {
            srcVariableName: name,
            dstVariableName: name,
            srcFrameId: frames[0].id
        })
            .then(async () => {
            const scopes = await this._getScopes(frames[0]);
            const variables = await Promise.all(scopes.map(scope => this._getVariables(scope)));
            const variableScopes = this._convertScopes(scopes, variables);
            this._model.variables.scopes = variableScopes;
        })
            .catch(reason => {
            console.error(reason);
        });
    }
    /**
     * Requests all the defined variables and display them in the
     * table view.
     */
    async displayDefinedVariables() {
        if (!this.session) {
            throw new Error('No active debugger session');
        }
        const inspectReply = await this.session.sendRequest('inspectVariables', {});
        const variables = inspectReply.body.variables;
        const variableScopes = [
            {
                name: this._trans.__('Globals'),
                variables: variables
            }
        ];
        this._model.variables.scopes = variableScopes;
    }
    async displayModules() {
        if (!this.session) {
            throw new Error('No active debugger session');
        }
        const modules = await this.session.sendRequest('modules', {});
        this._model.kernelSources.kernelSources = modules.body.modules.map(module => {
            return {
                name: module.name,
                path: module.path
            };
        });
    }
    /**
     * Restart the debugger.
     */
    async restart() {
        const { breakpoints } = this._model.breakpoints;
        await this.stop();
        await this.start();
        await this._restoreBreakpoints(breakpoints);
    }
    /**
     * Restore the state of a debug session.
     *
     * @param autoStart - If true, starts the debugger if it has not been started.
     */
    async restoreState(autoStart) {
        var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k;
        if (!this.model || !this.session) {
            return;
        }
        const reply = await this.session.restoreState();
        const { body } = reply;
        const breakpoints = this._mapBreakpoints(body.breakpoints);
        const stoppedThreads = new Set(body.stoppedThreads);
        this._model.hasRichVariableRendering = body.richRendering === true;
        this._model.supportCopyToGlobals = body.copyToGlobals === true;
        this._config.setHashParams({
            kernel: (_d = (_c = (_b = (_a = this.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.name) !== null && _d !== void 0 ? _d : '',
            method: body.hashMethod,
            seed: body.hashSeed
        });
        this._config.setTmpFileParams({
            kernel: (_h = (_g = (_f = (_e = this.session) === null || _e === void 0 ? void 0 : _e.connection) === null || _f === void 0 ? void 0 : _f.kernel) === null || _g === void 0 ? void 0 : _g.name) !== null && _h !== void 0 ? _h : '',
            prefix: body.tmpFilePrefix,
            suffix: body.tmpFileSuffix
        });
        this._model.stoppedThreads = stoppedThreads;
        if (!this.isStarted && (autoStart || stoppedThreads.size !== 0)) {
            await this.start();
        }
        if (this.isStarted || autoStart) {
            this._model.title = this.isStarted
                ? ((_k = (_j = this.session) === null || _j === void 0 ? void 0 : _j.connection) === null || _k === void 0 ? void 0 : _k.name) || '-'
                : '-';
        }
        if (this._debuggerSources) {
            const filtered = this._filterBreakpoints(breakpoints);
            this._model.breakpoints.restoreBreakpoints(filtered);
        }
        else {
            this._model.breakpoints.restoreBreakpoints(breakpoints);
        }
        if (stoppedThreads.size !== 0) {
            await this._getAllFrames();
        }
        else if (this.isStarted) {
            this._clearModel();
            this._clearSignals();
        }
        // Send the currentExceptionFilters to debugger.
        if (this.session.currentExceptionFilters) {
            await this.pauseOnExceptions(this.session.currentExceptionFilters);
        }
    }
    /**
     * Starts a debugger.
     * Precondition: !isStarted
     */
    start() {
        if (!this.session) {
            throw new Error('No active debugger session');
        }
        return this.session.start();
    }
    /**
     * Makes the current thread pause if possible.
     */
    async pause() {
        try {
            if (!this.session) {
                throw new Error('No active debugger session');
            }
            await this.session.sendRequest('pause', {
                threadId: this._currentThread()
            });
        }
        catch (err) {
            console.error('Error:', err.message);
        }
    }
    /**
     * Makes the current thread step in a function / method if possible.
     */
    async stepIn() {
        try {
            if (!this.session) {
                throw new Error('No active debugger session');
            }
            await this.session.sendRequest('stepIn', {
                threadId: this._currentThread()
            });
        }
        catch (err) {
            console.error('Error:', err.message);
        }
    }
    /**
     * Makes the current thread step out a function / method if possible.
     */
    async stepOut() {
        try {
            if (!this.session) {
                throw new Error('No active debugger session');
            }
            await this.session.sendRequest('stepOut', {
                threadId: this._currentThread()
            });
        }
        catch (err) {
            console.error('Error:', err.message);
        }
    }
    /**
     * Stops the debugger.
     * Precondition: isStarted
     */
    async stop() {
        if (!this.session) {
            throw new Error('No active debugger session');
        }
        await this.session.stop();
        if (this._model) {
            this._model.clear();
        }
    }
    /**
     * Update all breakpoints at once.
     *
     * @param code - The code in the cell where the breakpoints are set.
     * @param breakpoints - The list of breakpoints to set.
     * @param path - Optional path to the file where to set the breakpoints.
     */
    async updateBreakpoints(code, breakpoints, path) {
        var _a;
        if (!((_a = this.session) === null || _a === void 0 ? void 0 : _a.isStarted)) {
            return;
        }
        if (!path) {
            path = (await this._dumpCell(code)).body.sourcePath;
        }
        const state = await this.session.restoreState();
        const localBreakpoints = breakpoints
            .filter(({ line }) => typeof line === 'number')
            .map(({ line }) => ({ line: line }));
        const remoteBreakpoints = this._mapBreakpoints(state.body.breakpoints);
        // Set the local copy of breakpoints to reflect only editors that exist.
        if (this._debuggerSources) {
            const filtered = this._filterBreakpoints(remoteBreakpoints);
            this._model.breakpoints.restoreBreakpoints(filtered);
        }
        else {
            this._model.breakpoints.restoreBreakpoints(remoteBreakpoints);
        }
        // Removes duplicated breakpoints. It is better to do it here than
        // in the editor, because the kernel can change the line of a
        // breakpoint (when you attemp to set a breakpoint on an empty
        // line for instance).
        let addedLines = new Set();
        // Set the kernel's breakpoints for this path.
        const reply = await this._setBreakpoints(localBreakpoints, path);
        const updatedBreakpoints = reply.body.breakpoints.filter((val, _, arr) => {
            const cond1 = arr.findIndex(el => el.line === val.line) > -1;
            const cond2 = !addedLines.has(val.line);
            addedLines.add(val.line);
            return cond1 && cond2;
        });
        // Update the local model and finish kernel configuration.
        this._model.breakpoints.setBreakpoints(path, updatedBreakpoints);
        await this.session.sendRequest('configurationDone', {});
    }
    /**
     * Determines if pausing on exceptions is supported by the kernel
     */
    pauseOnExceptionsIsValid() {
        var _a, _b;
        if (this.isStarted) {
            if (((_b = (_a = this.session) === null || _a === void 0 ? void 0 : _a.exceptionBreakpointFilters) === null || _b === void 0 ? void 0 : _b.length) !== 0) {
                return true;
            }
        }
        return false;
    }
    /**
     * Add or remove a filter from the current used filters.
     *
     * @param exceptionFilter - The filter to add or remove from current filters.
     */
    async pauseOnExceptionsFilter(exceptionFilter) {
        var _a;
        if (!((_a = this.session) === null || _a === void 0 ? void 0 : _a.isStarted)) {
            return;
        }
        let exceptionFilters = this.session.currentExceptionFilters;
        if (this.session.isPausingOnException(exceptionFilter)) {
            const index = exceptionFilters.indexOf(exceptionFilter);
            exceptionFilters.splice(index, 1);
        }
        else {
            exceptionFilters === null || exceptionFilters === void 0 ? void 0 : exceptionFilters.push(exceptionFilter);
        }
        await this.pauseOnExceptions(exceptionFilters);
    }
    /**
     * Enable or disable pausing on exceptions.
     *
     * @param exceptionFilters - The filters to use for the current debugging session.
     */
    async pauseOnExceptions(exceptionFilters) {
        var _a, _b;
        if (!((_a = this.session) === null || _a === void 0 ? void 0 : _a.isStarted)) {
            return;
        }
        const exceptionBreakpointFilters = ((_b = this.session.exceptionBreakpointFilters) === null || _b === void 0 ? void 0 : _b.map(e => e.filter)) || [];
        let options = {
            filters: []
        };
        exceptionFilters.forEach(filter => {
            if (exceptionBreakpointFilters.includes(filter)) {
                options.filters.push(filter);
            }
        });
        this.session.currentExceptionFilters = options.filters;
        await this.session.sendRequest('setExceptionBreakpoints', options);
        this._pauseOnExceptionChanged.emit();
    }
    /**
     * Get the debugger state
     *
     * @returns Debugger state
     */
    getDebuggerState() {
        var _a, _b, _c, _d, _e, _f, _g;
        const breakpoints = this._model.breakpoints.breakpoints;
        let cells = [];
        if (this._debuggerSources) {
            for (const id of breakpoints.keys()) {
                const editorList = this._debuggerSources.find({
                    focus: false,
                    kernel: (_d = (_c = (_b = (_a = this.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.name) !== null && _d !== void 0 ? _d : '',
                    path: (_g = (_f = (_e = this._session) === null || _e === void 0 ? void 0 : _e.connection) === null || _f === void 0 ? void 0 : _f.path) !== null && _g !== void 0 ? _g : '',
                    source: id
                });
                const tmpCells = editorList.map(e => e.src.getSource());
                cells = cells.concat(tmpCells);
            }
        }
        return { cells, breakpoints };
    }
    /**
     * Restore the debugger state
     *
     * @param state Debugger state
     * @returns Whether the state has been restored successfully or not
     */
    async restoreDebuggerState(state) {
        var _a, _b, _c, _d;
        await this.start();
        for (const cell of state.cells) {
            await this._dumpCell(cell);
        }
        const breakpoints = new Map();
        const kernel = (_d = (_c = (_b = (_a = this.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.name) !== null && _d !== void 0 ? _d : '';
        const { prefix, suffix } = this._config.getTmpFileParams(kernel);
        for (const item of state.breakpoints) {
            const [id, list] = item;
            const unsuffixedId = id.substr(0, id.length - suffix.length);
            const codeHash = unsuffixedId.substr(unsuffixedId.lastIndexOf('/') + 1);
            const newId = prefix.concat(codeHash).concat(suffix);
            breakpoints.set(newId, list);
        }
        await this._restoreBreakpoints(breakpoints);
        const config = await this.session.sendRequest('configurationDone', {});
        await this.restoreState(false);
        return config.success;
    }
    /**
     * Clear the current model.
     */
    _clearModel() {
        this._model.callstack.frames = [];
        this._model.variables.scopes = [];
    }
    /**
     * Clear the signals set on the model.
     */
    _clearSignals() {
        this._model.callstack.currentFrameChanged.disconnect(this._onCurrentFrameChanged, this);
        this._model.variables.variableExpanded.disconnect(this._onVariableExpanded, this);
    }
    /**
     * Map a list of scopes to a list of variables.
     *
     * @param scopes The list of scopes.
     * @param variables The list of variables.
     */
    _convertScopes(scopes, variables) {
        if (!variables || !scopes) {
            return [];
        }
        return scopes.map((scope, i) => {
            return {
                name: scope.name,
                variables: variables[i].map(variable => {
                    return { ...variable };
                })
            };
        });
    }
    /**
     * Get the current thread from the model.
     */
    _currentThread() {
        // TODO: ask the model for the current thread ID
        return 1;
    }
    /**
     * Dump the content of a cell.
     *
     * @param code The source code to dump.
     */
    async _dumpCell(code) {
        if (!this.session) {
            throw new Error('No active debugger session');
        }
        return this.session.sendRequest('dumpCell', { code });
    }
    /**
     * Filter breakpoints and only return those associated with a known editor.
     *
     * @param breakpoints - Map of breakpoints.
     *
     */
    _filterBreakpoints(breakpoints) {
        if (!this._debuggerSources) {
            return breakpoints;
        }
        let bpMapForRestore = new Map();
        for (const collection of breakpoints) {
            const [id, list] = collection;
            list.forEach(() => {
                var _a, _b, _c, _d, _e, _f, _g;
                this._debuggerSources.find({
                    focus: false,
                    kernel: (_d = (_c = (_b = (_a = this.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.name) !== null && _d !== void 0 ? _d : '',
                    path: (_g = (_f = (_e = this._session) === null || _e === void 0 ? void 0 : _e.connection) === null || _f === void 0 ? void 0 : _f.path) !== null && _g !== void 0 ? _g : '',
                    source: id
                }).forEach(() => {
                    if (list.length > 0) {
                        bpMapForRestore.set(id, list);
                    }
                });
            });
        }
        return bpMapForRestore;
    }
    /**
     * Get all the frames from the kernel.
     */
    async _getAllFrames() {
        this._model.callstack.currentFrameChanged.connect(this._onCurrentFrameChanged, this);
        this._model.variables.variableExpanded.connect(this._onVariableExpanded, this);
        const stackFrames = await this._getFrames(this._currentThread());
        this._model.callstack.frames = stackFrames;
    }
    /**
     * Get all the frames for the given thread id.
     *
     * @param threadId The thread id.
     */
    async _getFrames(threadId) {
        if (!this.session) {
            throw new Error('No active debugger session');
        }
        const reply = await this.session.sendRequest('stackTrace', {
            threadId
        });
        const stackFrames = reply.body.stackFrames;
        return stackFrames;
    }
    /**
     * Get all the scopes for the given frame.
     *
     * @param frame The frame.
     */
    async _getScopes(frame) {
        if (!this.session) {
            throw new Error('No active debugger session');
        }
        if (!frame) {
            return [];
        }
        const reply = await this.session.sendRequest('scopes', {
            frameId: frame.id
        });
        return reply.body.scopes;
    }
    /**
     * Get the variables for a given scope.
     *
     * @param scope The scope to get variables for.
     */
    async _getVariables(scope) {
        if (!this.session) {
            throw new Error('No active debugger session');
        }
        if (!scope) {
            return [];
        }
        const reply = await this.session.sendRequest('variables', {
            variablesReference: scope.variablesReference
        });
        return reply.body.variables;
    }
    /**
     * Process the list of breakpoints from the server and return as a map.
     *
     * @param breakpoints - The list of breakpoints from the kernel.
     *
     */
    _mapBreakpoints(breakpoints) {
        if (!breakpoints.length) {
            return new Map();
        }
        return breakpoints.reduce((map, val) => {
            const { breakpoints, source } = val;
            map.set(source, breakpoints.map(point => ({
                ...point,
                source: { path: source },
                verified: true
            })));
            return map;
        }, new Map());
    }
    /**
     * Handle a change of the current active frame.
     *
     * @param _ The callstack model
     * @param frame The frame.
     */
    async _onCurrentFrameChanged(_, frame) {
        if (!frame) {
            return;
        }
        const scopes = await this._getScopes(frame);
        const variables = await Promise.all(scopes.map(scope => this._getVariables(scope)));
        const variableScopes = this._convertScopes(scopes, variables);
        this._model.variables.scopes = variableScopes;
    }
    /**
     * Handle a variable expanded event and request variables from the kernel.
     *
     * @param _ The variables model.
     * @param variable The expanded variable.
     */
    async _onVariableExpanded(_, variable) {
        if (!this.session) {
            throw new Error('No active debugger session');
        }
        const reply = await this.session.sendRequest('variables', {
            variablesReference: variable.variablesReference
        });
        let newVariable = { ...variable, expanded: true };
        reply.body.variables.forEach((variable) => {
            newVariable = { [variable.name]: variable, ...newVariable };
        });
        const newScopes = this._model.variables.scopes.map(scope => {
            const findIndex = scope.variables.findIndex(ele => ele.variablesReference === variable.variablesReference);
            scope.variables[findIndex] = newVariable;
            return { ...scope };
        });
        this._model.variables.scopes = [...newScopes];
        return reply.body.variables;
    }
    /**
     * Set the breakpoints for a given file.
     *
     * @param breakpoints The list of breakpoints to set.
     * @param path The path to where to set the breakpoints.
     */
    async _setBreakpoints(breakpoints, path) {
        if (!this.session) {
            throw new Error('No active debugger session');
        }
        return await this.session.sendRequest('setBreakpoints', {
            breakpoints: breakpoints,
            source: { path },
            sourceModified: false
        });
    }
    /**
     * Re-send the breakpoints to the kernel and update the model.
     *
     * @param breakpoints The map of breakpoints to send
     */
    async _restoreBreakpoints(breakpoints) {
        for (const [source, points] of breakpoints) {
            await this._setBreakpoints(points
                .filter(({ line }) => typeof line === 'number')
                .map(({ line }) => ({ line: line })), source);
        }
        this._model.breakpoints.restoreBreakpoints(breakpoints);
    }
}

;// CONCATENATED MODULE: ../packages/debugger/lib/session.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * A concrete implementation of IDebugger.ISession.
 */
class DebuggerSession {
    /**
     * Instantiate a new debug session
     *
     * @param options - The debug session instantiation options.
     */
    constructor(options) {
        this._seq = 0;
        this._ready = new coreutils_dist_index_js_.PromiseDelegate();
        this._isDisposed = false;
        this._isStarted = false;
        this._exceptionPaths = [];
        this._exceptionBreakpointFilters = [];
        this._currentExceptionFilters = {};
        this._disposed = new dist_index_es6_js_.Signal(this);
        this._eventMessage = new dist_index_es6_js_.Signal(this);
        this.connection = options.connection;
        this._config = options.config;
        this.translator = options.translator || translation_lib_index_js_.nullTranslator;
    }
    /**
     * Whether the debug session is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Returns the initialize response .
     */
    get capabilities() {
        return this._capabilities;
    }
    /**
     * A signal emitted when the debug session is disposed.
     */
    get disposed() {
        return this._disposed;
    }
    /**
     * Returns the API session connection to connect to a debugger.
     */
    get connection() {
        return this._connection;
    }
    /**
     * Sets the API session connection to connect to a debugger to
     * the given parameter.
     *
     * @param connection - The new API session connection.
     */
    set connection(connection) {
        var _a, _b;
        if (this._connection) {
            this._connection.iopubMessage.disconnect(this._handleEvent, this);
        }
        this._connection = connection;
        if (!this._connection) {
            this._isStarted = false;
            return;
        }
        this._connection.iopubMessage.connect(this._handleEvent, this);
        this._ready = new coreutils_dist_index_js_.PromiseDelegate();
        const future = (_b = (_a = this.connection) === null || _a === void 0 ? void 0 : _a.kernel) === null || _b === void 0 ? void 0 : _b.requestDebug({
            type: 'request',
            seq: 0,
            command: 'debugInfo'
        });
        if (future) {
            future.onReply = (msg) => {
                this._ready.resolve();
                future.dispose();
            };
        }
    }
    /**
     * Whether the debug session is started.
     */
    get isStarted() {
        return this._isStarted;
    }
    /**
     * Exception paths defined by the debugger
     */
    get exceptionPaths() {
        return this._exceptionPaths;
    }
    /**
     * Exception breakpoint filters defined by the debugger
     */
    get exceptionBreakpointFilters() {
        return this._exceptionBreakpointFilters;
    }
    /**
     * Get current exception filters.
     */
    get currentExceptionFilters() {
        var _a, _b, _c;
        const kernel = (_c = (_b = (_a = this.connection) === null || _a === void 0 ? void 0 : _a.kernel) === null || _b === void 0 ? void 0 : _b.name) !== null && _c !== void 0 ? _c : '';
        if (!kernel) {
            return [];
        }
        const tmpFileParams = this._config.getTmpFileParams(kernel);
        if (!tmpFileParams) {
            return [];
        }
        let prefix = tmpFileParams.prefix;
        if (Object.keys(this._currentExceptionFilters).includes(prefix)) {
            return this._currentExceptionFilters[prefix];
        }
        return [];
    }
    /**
     * Set current exception filters.
     */
    set currentExceptionFilters(exceptionFilters) {
        var _a, _b, _c;
        const kernel = (_c = (_b = (_a = this.connection) === null || _a === void 0 ? void 0 : _a.kernel) === null || _b === void 0 ? void 0 : _b.name) !== null && _c !== void 0 ? _c : '';
        if (!kernel) {
            return;
        }
        const tmpFileParams = this._config.getTmpFileParams(kernel);
        if (!tmpFileParams) {
            return;
        }
        let prefix = tmpFileParams.prefix;
        if (exceptionFilters === null) {
            if (Object.keys(this._currentExceptionFilters).includes(prefix)) {
                delete this._currentExceptionFilters[prefix];
            }
        }
        else {
            this._currentExceptionFilters[prefix] = exceptionFilters;
        }
    }
    /**
     * Signal emitted for debug event messages.
     */
    get eventMessage() {
        return this._eventMessage;
    }
    /**
     * Dispose the debug session.
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._disposed.emit();
        dist_index_es6_js_.Signal.clearData(this);
    }
    /**
     * Start a new debug session
     */
    async start() {
        var _a, _b, _c, _d;
        const initializeResponse = await this.sendRequest('initialize', {
            clientID: 'jupyterlab',
            clientName: 'JupyterLab',
            adapterID: (_c = (_b = (_a = this.connection) === null || _a === void 0 ? void 0 : _a.kernel) === null || _b === void 0 ? void 0 : _b.name) !== null && _c !== void 0 ? _c : '',
            pathFormat: 'path',
            linesStartAt1: true,
            columnsStartAt1: true,
            supportsVariableType: true,
            supportsVariablePaging: true,
            supportsRunInTerminalRequest: true,
            locale: document.documentElement.lang
        });
        if (!initializeResponse.success) {
            throw new Error(`Could not start the debugger: ${initializeResponse.message}`);
        }
        this._capabilities = initializeResponse.body;
        this._isStarted = true;
        this._exceptionBreakpointFilters =
            (_d = initializeResponse.body) === null || _d === void 0 ? void 0 : _d.exceptionBreakpointFilters;
        await this.sendRequest('attach', {});
    }
    /**
     * Stop the running debug session.
     */
    async stop() {
        this._isStarted = false;
        await this.sendRequest('disconnect', {
            restart: false,
            terminateDebuggee: false
        });
    }
    /**
     * Restore the state of a debug session.
     */
    async restoreState() {
        var _a;
        const message = await this.sendRequest('debugInfo', {});
        this._isStarted = message.body.isStarted;
        this._exceptionPaths = (_a = message.body) === null || _a === void 0 ? void 0 : _a.exceptionPaths;
        return message;
    }
    /**
     * Whether the debugger is pausing on exception.
     *
     * @param filter - Specify a filter
     */
    isPausingOnException(filter) {
        var _a, _b;
        if (filter) {
            return (_b = (_a = this.currentExceptionFilters) === null || _a === void 0 ? void 0 : _a.includes(filter)) !== null && _b !== void 0 ? _b : false;
        }
        else {
            return this.currentExceptionFilters.length > 0;
        }
    }
    /**
     * Send a custom debug request to the kernel.
     *
     * @param command debug command.
     * @param args arguments for the debug command.
     */
    async sendRequest(command, args) {
        await this._ready.promise;
        const message = await this._sendDebugMessage({
            type: 'request',
            seq: this._seq++,
            command,
            arguments: args
        });
        return message.content;
    }
    /**
     * Handle debug events sent on the 'iopub' channel.
     *
     * @param sender - the emitter of the event.
     * @param message - the event message.
     */
    _handleEvent(sender, message) {
        const msgType = message.header.msg_type;
        if (msgType !== 'debug_event') {
            return;
        }
        const event = message.content;
        this._eventMessage.emit(event);
    }
    /**
     * Send a debug request message to the kernel.
     *
     * @param msg debug request message to send to the kernel.
     */
    async _sendDebugMessage(msg) {
        var _a;
        const kernel = (_a = this.connection) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel) {
            return Promise.reject(new Error('A kernel is required to send debug messages.'));
        }
        const reply = new coreutils_dist_index_js_.PromiseDelegate();
        const future = kernel.requestDebug(msg);
        future.onReply = (msg) => {
            reply.resolve(msg);
        };
        await future.done;
        return reply.promise;
    }
}

// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
var react_index_js_default = /*#__PURE__*/__webpack_require__.n(react_index_js_);
;// CONCATENATED MODULE: ../packages/debugger/lib/panels/breakpoints/body.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * The body for a Breakpoints Panel.
 */
class BreakpointsBody extends index_js_.ReactWidget {
    /**
     * Instantiate a new Body for the Breakpoints Panel.
     *
     * @param model The model for the breakpoints.
     */
    constructor(model) {
        super();
        this._model = model;
        this.addClass('jp-DebuggerBreakpoints-body');
    }
    /**
     * Render the BreakpointsComponent.
     */
    render() {
        return react_index_js_default().createElement(BreakpointsComponent, { model: this._model });
    }
}
/**
 * A React component to display a list of breakpoints.
 *
 * @param {object} props The component props.
 * @param props.model The model for the breakpoints.
 */
const BreakpointsComponent = ({ model }) => {
    const [breakpoints, setBreakpoints] = (0,react_index_js_.useState)(Array.from(model.breakpoints.entries()));
    (0,react_index_js_.useEffect)(() => {
        const updateBreakpoints = (_, updates) => {
            setBreakpoints(Array.from(model.breakpoints.entries()));
        };
        const restoreBreakpoints = (_) => {
            setBreakpoints(Array.from(model.breakpoints.entries()));
        };
        model.changed.connect(updateBreakpoints);
        model.restored.connect(restoreBreakpoints);
        return () => {
            model.changed.disconnect(updateBreakpoints);
            model.restored.disconnect(restoreBreakpoints);
        };
    });
    return (react_index_js_default().createElement((react_index_js_default()).Fragment, null, breakpoints.map(entry => (react_index_js_default().createElement(BreakpointCellComponent, { key: entry[0], breakpoints: entry[1], model: model })))));
};
/**
 * A React Component to display breakpoints grouped by source file.
 *
 * @param {object} props The component props.
 * @param props.breakpoints The list of breakpoints.
 * @param props.model The model for the breakpoints.
 */
const BreakpointCellComponent = ({ breakpoints, model }) => {
    return (react_index_js_default().createElement((react_index_js_default()).Fragment, null, breakpoints
        .sort((a, b) => {
        var _a, _b;
        return ((_a = a.line) !== null && _a !== void 0 ? _a : 0) - ((_b = b.line) !== null && _b !== void 0 ? _b : 0);
    })
        .map((breakpoint, index) => {
        var _a, _b;
        return (react_index_js_default().createElement(BreakpointComponent, { key: ((_b = (_a = breakpoint.source) === null || _a === void 0 ? void 0 : _a.path) !== null && _b !== void 0 ? _b : '') + index, breakpoint: breakpoint, model: model }));
    })));
};
/**
 * A React Component to display a single breakpoint.
 *
 * @param {object} props The component props.
 * @param props.breakpoint The breakpoint.
 * @param props.model The model for the breakpoints.
 */
const BreakpointComponent = ({ breakpoint, model }) => {
    var _a, _b, _c;
    const moveToEndFirstCharIfSlash = (breakpointSourcePath) => {
        return breakpointSourcePath[0] === '/'
            ? breakpointSourcePath.slice(1) + '/'
            : breakpointSourcePath;
    };
    return (react_index_js_default().createElement("div", { className: 'jp-DebuggerBreakpoint', onClick: () => model.clicked.emit(breakpoint), title: (_a = breakpoint.source) === null || _a === void 0 ? void 0 : _a.path },
        react_index_js_default().createElement("span", { className: 'jp-DebuggerBreakpoint-marker' }, "\u25CF"),
        react_index_js_default().createElement("span", { className: 'jp-DebuggerBreakpoint-source jp-left-truncated' }, moveToEndFirstCharIfSlash((_c = (_b = breakpoint.source) === null || _b === void 0 ? void 0 : _b.path) !== null && _c !== void 0 ? _c : '')),
        react_index_js_default().createElement("span", { className: 'jp-DebuggerBreakpoint-line' }, breakpoint.line)));
};

;// CONCATENATED MODULE: ../packages/debugger/lib/panels/breakpoints/pauseonexceptions.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


const PAUSE_ON_EXCEPTION_CLASS = 'jp-debugger-pauseOnExceptions';
const PAUSE_ON_EXCEPTION_BUTTON_CLASS = 'jp-PauseOnExceptions';
const PAUSE_ON_EXCEPTION_MENU_CLASS = 'jp-PauseOnExceptions-menu';
/**
 * A button which display a menu on click, to select the filter.
 */
class PauseOnExceptionsWidget extends index_js_.ToolbarButton {
    /**
     * Constructor of the button.
     */
    constructor(props) {
        super();
        /**
         * open menu on click.
         */
        this.onclick = () => {
            this._menu.open(this.node.getBoundingClientRect().left, this.node.getBoundingClientRect().bottom);
        };
        this._menu = new PauseOnExceptionsMenu({
            service: props.service,
            commands: {
                registry: props.commands.registry,
                pauseOnExceptions: props.commands.pauseOnExceptions
            }
        });
        this.node.className = PAUSE_ON_EXCEPTION_CLASS;
        this._props = props;
        this._props.className = PAUSE_ON_EXCEPTION_BUTTON_CLASS;
        this._props.service.eventMessage.connect((_, event) => {
            if (event.event === 'initialized' || event.event === 'terminated') {
                this.onChange();
            }
        }, this);
        this._props.enabled = this._props.service.pauseOnExceptionsIsValid();
        this._props.service.pauseOnExceptionChanged.connect(this.onChange, this);
    }
    /**
     * Called when the debugger is initialized or the filter changed.
     */
    onChange() {
        var _a;
        const session = this._props.service.session;
        const exceptionBreakpointFilters = session === null || session === void 0 ? void 0 : session.exceptionBreakpointFilters;
        this._props.className = PAUSE_ON_EXCEPTION_BUTTON_CLASS;
        if (((_a = this._props.service.session) === null || _a === void 0 ? void 0 : _a.isStarted) && exceptionBreakpointFilters) {
            if (session.isPausingOnException()) {
                this._props.className += ' lm-mod-toggled';
            }
            this._props.enabled = true;
        }
        else {
            this._props.enabled = false;
        }
        this.update();
    }
    render() {
        return react_index_js_.createElement(index_js_.ToolbarButtonComponent, { ...this._props, onClick: this.onclick });
    }
}
/**
 * A menu with all the available filter from the debugger as entries.
 */
class PauseOnExceptionsMenu extends index_js_.MenuSvg {
    /**
     * The constructor of the menu.
     */
    constructor(props) {
        super({ commands: props.commands.registry });
        this._service = props.service;
        this._command = props.commands.pauseOnExceptions;
        props.service.eventMessage.connect((_, event) => {
            if (event.event === 'initialized') {
                this._build();
            }
        }, this);
        this._build();
        this.addClass(PAUSE_ON_EXCEPTION_MENU_CLASS);
    }
    _build() {
        var _a, _b;
        this.clearItems();
        const exceptionsBreakpointFilters = (_b = (_a = this._service.session) === null || _a === void 0 ? void 0 : _a.exceptionBreakpointFilters) !== null && _b !== void 0 ? _b : [];
        exceptionsBreakpointFilters.map((filter, _) => {
            this.addItem({
                command: this._command,
                args: {
                    filter: filter.filter,
                    description: filter.description
                }
            });
        });
    }
}

;// CONCATENATED MODULE: ../packages/debugger/lib/panels/breakpoints/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/**
 * A Panel to show a list of breakpoints.
 */
class Breakpoints extends index_js_.PanelWithToolbar {
    /**
     * Instantiate a new Breakpoints Panel.
     *
     * @param options The instantiation options for a Breakpoints Panel.
     */
    constructor(options) {
        var _a;
        super(options);
        this.clicked = new dist_index_es6_js_.Signal(this);
        const { model, service, commands } = options;
        const trans = ((_a = options.translator) !== null && _a !== void 0 ? _a : translation_lib_index_js_.nullTranslator).load('jupyterlab');
        this.title.label = trans.__('Breakpoints');
        const body = new BreakpointsBody(model);
        this.toolbar.addItem('pauseOnException', new PauseOnExceptionsWidget({
            service: service,
            commands: commands,
            icon: exceptionIcon,
            tooltip: trans.__('Pause on exception filter')
        }));
        this.toolbar.addItem('closeAll', new index_js_.ToolbarButton({
            icon: closeAllIcon,
            onClick: async () => {
                if (model.breakpoints.size === 0) {
                    return;
                }
                const result = await (0,lib_index_js_.showDialog)({
                    title: trans.__('Remove All Breakpoints'),
                    body: trans.__('Are you sure you want to remove all breakpoints?'),
                    buttons: [
                        lib_index_js_.Dialog.okButton({ label: trans.__('Remove breakpoints') }),
                        lib_index_js_.Dialog.cancelButton()
                    ],
                    hasClose: true
                });
                if (result.button.accept) {
                    return service.clearBreakpoints();
                }
            },
            tooltip: trans.__('Remove All Breakpoints')
        }));
        this.addWidget(body);
        this.addClass('jp-DebuggerBreakpoints');
    }
}

;// CONCATENATED MODULE: ../packages/debugger/lib/panels/callstack/body.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * The body for a Callstack Panel.
 */
class CallstackBody extends index_js_.ReactWidget {
    /**
     * Instantiate a new Body for the Callstack Panel.
     *
     * @param model The model for the callstack.
     */
    constructor(model) {
        super();
        this._model = model;
        this.addClass('jp-DebuggerCallstack-body');
    }
    /**
     * Render the FramesComponent.
     */
    render() {
        return react_index_js_default().createElement(FramesComponent, { model: this._model });
    }
}
/**
 * A React component to display a list of frames in a callstack.
 *
 * @param {object} props The component props.
 * @param props.model The model for the callstack.
 */
const FramesComponent = ({ model }) => {
    const [frames, setFrames] = (0,react_index_js_.useState)(model.frames);
    const [selected, setSelected] = (0,react_index_js_.useState)(model.frame);
    const onSelected = (frame) => {
        setSelected(frame);
        model.frame = frame;
    };
    (0,react_index_js_.useEffect)(() => {
        const updateFrames = () => {
            setSelected(model.frame);
            setFrames(model.frames);
        };
        model.framesChanged.connect(updateFrames);
        return () => {
            model.framesChanged.disconnect(updateFrames);
        };
    }, [model]);
    const toShortLocation = (el) => {
        var _a;
        const path = ((_a = el.source) === null || _a === void 0 ? void 0 : _a.path) || '';
        const base = coreutils_lib_index_js_.PathExt.basename(coreutils_lib_index_js_.PathExt.dirname(path));
        const filename = coreutils_lib_index_js_.PathExt.basename(path);
        const shortname = coreutils_lib_index_js_.PathExt.join(base, filename);
        return `${shortname}:${el.line}`;
    };
    return (react_index_js_default().createElement("ul", null, frames.map(ele => {
        var _a;
        return (react_index_js_default().createElement("li", { key: ele.id, onClick: () => onSelected(ele), className: (selected === null || selected === void 0 ? void 0 : selected.id) === ele.id
                ? 'selected jp-DebuggerCallstackFrame'
                : 'jp-DebuggerCallstackFrame' },
            react_index_js_default().createElement("span", { className: 'jp-DebuggerCallstackFrame-name' }, ele.name),
            react_index_js_default().createElement("span", { className: 'jp-DebuggerCallstackFrame-location', title: (_a = ele.source) === null || _a === void 0 ? void 0 : _a.path }, toShortLocation(ele))));
    })));
};

;// CONCATENATED MODULE: ../packages/debugger/lib/panels/callstack/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * A Panel to show a callstack.
 */
class Callstack extends index_js_.PanelWithToolbar {
    /**
     * Instantiate a new Callstack Panel.
     *
     * @param options The instantiation options for a Callstack Panel.
     */
    constructor(options) {
        var _a;
        super(options);
        const { commands, model } = options;
        const trans = ((_a = options.translator) !== null && _a !== void 0 ? _a : translation_lib_index_js_.nullTranslator).load('jupyterlab');
        this.title.label = trans.__('Callstack');
        const body = new CallstackBody(model);
        this.toolbar.addItem('continue', new index_js_.CommandToolbarButton({
            commands: commands.registry,
            id: commands.continue,
            label: ''
        }));
        this.toolbar.addItem('terminate', new index_js_.CommandToolbarButton({
            commands: commands.registry,
            id: commands.terminate,
            label: ''
        }));
        this.toolbar.addItem('step-over', new index_js_.CommandToolbarButton({
            commands: commands.registry,
            id: commands.next,
            label: ''
        }));
        this.toolbar.addItem('step-in', new index_js_.CommandToolbarButton({
            commands: commands.registry,
            id: commands.stepIn,
            label: ''
        }));
        this.toolbar.addItem('step-out', new index_js_.CommandToolbarButton({
            commands: commands.registry,
            id: commands.stepOut,
            label: ''
        }));
        this.toolbar.addItem('evaluate', new index_js_.CommandToolbarButton({
            commands: commands.registry,
            id: commands.evaluate,
            label: ''
        }));
        this.addWidget(body);
        this.addClass('jp-DebuggerCallstack');
    }
}

;// CONCATENATED MODULE: ../packages/debugger/lib/panels/sources/sourcepath.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * A React component to display the path to a source.
 *
 * @param {object} props The component props.
 * @param props.model The model for the sources.
 */
const SourcePathComponent = ({ model }) => {
    return (react_index_js_default().createElement(index_js_.UseSignal, { signal: model.currentSourceChanged, initialSender: model }, (model) => {
        var _a, _b;
        return (react_index_js_default().createElement("span", { onClick: () => model === null || model === void 0 ? void 0 : model.open(), className: "jp-DebuggerSources-header-path" }, (_b = (_a = model === null || model === void 0 ? void 0 : model.currentSource) === null || _a === void 0 ? void 0 : _a.path) !== null && _b !== void 0 ? _b : ''));
    }));
};

;// CONCATENATED MODULE: ../packages/debugger/lib/panels/sources/body.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * The body for a Sources Panel.
 */
class SourcesBody extends index_es6_js_.Widget {
    /**
     * Instantiate a new Body for the SourcesBody widget.
     *
     * @param options The instantiation options for a SourcesBody.
     */
    constructor(options) {
        super();
        this._model = options.model;
        this._debuggerService = options.service;
        this._mimeTypeService = options.editorServices.mimeTypeService;
        const factory = new Debugger.ReadOnlyEditorFactory({
            editorServices: options.editorServices
        });
        this._editor = factory.createNewEditor({
            content: '',
            mimeType: '',
            path: ''
        });
        this._editor.hide();
        this._model.currentFrameChanged.connect(async (_, frame) => {
            if (!frame) {
                this._clearEditor();
                return;
            }
            void this._showSource(frame);
        });
        const layout = new index_es6_js_.PanelLayout();
        layout.addWidget(this._editor);
        this.layout = layout;
        this.addClass('jp-DebuggerSources-body');
    }
    /**
     * Dispose the sources body widget.
     */
    dispose() {
        var _a;
        if (this.isDisposed) {
            return;
        }
        (_a = this._editorHandler) === null || _a === void 0 ? void 0 : _a.dispose();
        dist_index_es6_js_.Signal.clearData(this);
        super.dispose();
    }
    /**
     * Clear the content of the source read-only editor.
     */
    _clearEditor() {
        this._model.currentSource = null;
        this._editor.hide();
    }
    /**
     * Show the content of the source for the given frame.
     *
     * @param frame The current frame.
     */
    async _showSource(frame) {
        var _a;
        const path = (_a = frame.source) === null || _a === void 0 ? void 0 : _a.path;
        const source = await this._debuggerService.getSource({
            sourceReference: 0,
            path
        });
        if (!(source === null || source === void 0 ? void 0 : source.content)) {
            this._clearEditor();
            return;
        }
        if (this._editorHandler) {
            this._editorHandler.dispose();
        }
        const { content, mimeType } = source;
        const editorMimeType = mimeType || this._mimeTypeService.getMimeTypeByFilePath(path !== null && path !== void 0 ? path : '');
        this._editor.model.sharedModel.setSource(content);
        this._editor.model.mimeType = editorMimeType;
        this._editorHandler = new editor_EditorHandler({
            debuggerService: this._debuggerService,
            editorReady: () => Promise.resolve(this._editor.editor),
            getEditor: () => this._editor.editor,
            path,
            src: this._editor.model.sharedModel
        });
        this._model.currentSource = {
            content,
            mimeType: editorMimeType,
            path: path !== null && path !== void 0 ? path : ''
        };
        requestAnimationFrame(() => {
            editor_EditorHandler.showCurrentLine(this._editor.editor, frame.line);
        });
        this._editor.show();
    }
}

;// CONCATENATED MODULE: ../packages/debugger/lib/panels/sources/index.js
/*-----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/







/**
 * A Panel that shows a preview of the source code while debugging.
 */
class Sources extends index_js_.PanelWithToolbar {
    /**
     * Instantiate a new Sources preview Panel.
     *
     * @param options The Sources instantiation options.
     */
    constructor(options) {
        var _a;
        super();
        const { model, service, editorServices } = options;
        const trans = ((_a = options.translator) !== null && _a !== void 0 ? _a : translation_lib_index_js_.nullTranslator).load('jupyterlab');
        this.title.label = trans.__('Source');
        this.toolbar.addClass('jp-DebuggerSources-header');
        const body = new SourcesBody({
            service,
            model,
            editorServices
        });
        this.toolbar.addItem('open', new index_js_.ToolbarButton({
            icon: viewBreakpointIcon,
            onClick: () => model.open(),
            tooltip: trans.__('Open in the Main Area')
        }));
        const sourcePath = index_js_.ReactWidget.create(react_index_js_default().createElement(SourcePathComponent, { model: model }));
        this.toolbar.addItem('sourcePath', sourcePath);
        this.addClass('jp-DebuggerSources-header');
        this.addWidget(body);
        this.addClass('jp-DebuggerSources');
    }
}

;// CONCATENATED MODULE: ../packages/debugger/lib/panels/kernelSources/filter.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


const FilterBox = (props) => {
    const onFilterChange = (e) => {
        const filter = e.target.value;
        props.model.filter = filter;
    };
    return (react_index_js_default().createElement(index_js_.InputGroup, { type: "text", onChange: onFilterChange, placeholder: "Filter the kernel sources", value: props.model.filter }));
};
/**
 * A widget which hosts a input textbox to filter on file names.
 */
const KernelSourcesFilter = (props) => {
    return (react_index_js_default().createElement(index_js_.UseSignal, { signal: props.model.filterChanged, initialArgs: props.model.filter }, model => react_index_js_default().createElement(FilterBox, { model: props.model })));
};

;// CONCATENATED MODULE: ../packages/debugger/lib/panels/kernelSources/body.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/**
 * The class name added to the filterbox node.
 */
const FILTERBOX_CLASS = 'jp-DebuggerKernelSource-filterBox';
/**
 * The class name added to hide the filterbox node.
 */
const FILTERBOX_HIDDEN_CLASS = 'jp-DebuggerKernelSource-filterBox-hidden';
/**
 * The body for a Sources Panel.
 */
class KernelSourcesBody extends index_js_.ReactWidget {
    /**
     * Instantiate a new Body for the KernelSourcesBody widget.
     *
     * @param options The instantiation options for a KernelSourcesBody.
     */
    constructor(options) {
        var _a;
        super();
        this._showFilter = false;
        this._model = options.model;
        this._debuggerService = options.service;
        this._trans = ((_a = options.translator) !== null && _a !== void 0 ? _a : translation_lib_index_js_.nullTranslator).load('jupyterlab');
        this.addClass('jp-DebuggerKernelSources-body');
    }
    render() {
        let filterClass = FILTERBOX_CLASS;
        if (!this._showFilter) {
            filterClass += ' ' + FILTERBOX_HIDDEN_CLASS;
        }
        return (react_index_js_default().createElement((react_index_js_default()).Fragment, null,
            react_index_js_default().createElement("div", { className: filterClass, key: 'filter' },
                react_index_js_default().createElement(KernelSourcesFilter, { model: this._model })),
            react_index_js_default().createElement(index_js_.UseSignal, { signal: this._model.changed }, (_, kernelSources) => {
                const keymap = {};
                return (kernelSources !== null && kernelSources !== void 0 ? kernelSources : []).map(module => {
                    var _a;
                    const name = module.name;
                    const path = module.path;
                    const key = name + (keymap[name] = ((_a = keymap[name]) !== null && _a !== void 0 ? _a : 0) + 1).toString();
                    const button = (react_index_js_default().createElement(index_js_.ToolbarButtonComponent, { key: key, icon: openKernelSourceIcon, label: name, tooltip: path, onClick: () => {
                            this._debuggerService
                                .getSource({
                                sourceReference: 0,
                                path: path
                            })
                                .then(source => {
                                this._model.open(source);
                            })
                                .catch(reason => {
                                void (0,lib_index_js_.showErrorMessage)(this._trans.__('Fail to get source'), this._trans.__("Fail to get '%1' source:\n%2", path, reason));
                            });
                        } }));
                    return button;
                });
            })));
    }
    /**
     * Show or hide the filter box.
     */
    toggleFilterbox() {
        this._showFilter = !this._showFilter;
        this.update();
    }
}

;// CONCATENATED MODULE: ../packages/debugger/lib/panels/kernelSources/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * A Panel that shows a preview of the source code while debugging.
 */
class KernelSources extends index_js_.PanelWithToolbar {
    /**
     * Instantiate a new Sources preview Panel.
     *
     * @param options The Sources instantiation options.
     */
    constructor(options) {
        var _a;
        super();
        const { model, service } = options;
        this._model = model;
        const trans = ((_a = options.translator) !== null && _a !== void 0 ? _a : translation_lib_index_js_.nullTranslator).load('jupyterlab');
        this.title.label = trans.__('Kernel Sources');
        this.toolbar.addClass('jp-DebuggerKernelSources-header');
        this._body = new KernelSourcesBody({
            service,
            model,
            translator: options.translator
        });
        this.toolbar.addItem('open-filter', new index_js_.ToolbarButton({
            icon: index_js_.searchIcon,
            onClick: async () => {
                this._body.toggleFilterbox();
            },
            tooltip: trans.__('Toggle search filter')
        }));
        this.toolbar.addItem('refresh', new index_js_.ToolbarButton({
            icon: index_js_.refreshIcon,
            onClick: () => {
                this._model.kernelSources = [];
                void service.displayModules().catch(reason => {
                    void (0,lib_index_js_.showErrorMessage)(trans.__('Fail to get kernel sources'), trans.__('Fail to get kernel sources:\n%2', reason));
                });
            },
            tooltip: trans.__('Refresh kernel sources')
        }));
        this.addClass('jp-DebuggerKernelSources-header');
        this.addWidget(this._body);
        this.addClass('jp-DebuggerKenelSources');
    }
    set filter(filter) {
        this._model.filter = filter;
    }
}

;// CONCATENATED MODULE: ../packages/debugger/lib/panels/variables/scope.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */



/**
 * A React component to handle scope changes.
 *
 * @param {object} props The component props.
 * @param props.model The variables model.
 * @param props.tree The variables tree widget.
 * @param props.grid The variables grid widget.
 * @param props.trans The translation bundle.
 */
const ScopeSwitcherComponent = ({ model, tree, grid, trans }) => {
    const [value, setValue] = (0,react_index_js_.useState)('-');
    const scopes = model.scopes;
    const onChange = (event) => {
        const value = event.target.value;
        setValue(value);
        tree.scope = value;
        grid.scope = value;
    };
    return (react_index_js_default().createElement(index_js_.HTMLSelect, { onChange: onChange, value: value, "aria-label": trans.__('Scope') }, scopes.map(scope => (react_index_js_default().createElement("option", { key: scope.name, value: scope.name }, trans.__(scope.name))))));
};
/**
 * A widget to switch between scopes.
 */
class ScopeSwitcher extends index_js_.ReactWidget {
    /**
     * Instantiate a new scope switcher.
     *
     * @param options The instantiation options for a ScopeSwitcher
     */
    constructor(options) {
        super();
        const { translator, model, tree, grid } = options;
        this._model = model;
        this._tree = tree;
        this._grid = grid;
        this._trans = (translator || translation_lib_index_js_.nullTranslator).load('jupyterlab');
    }
    /**
     * Render the scope switcher.
     */
    render() {
        return (react_index_js_default().createElement(index_js_.UseSignal, { signal: this._model.changed, initialSender: this._model }, () => (react_index_js_default().createElement(ScopeSwitcherComponent, { model: this._model, trans: this._trans, tree: this._tree, grid: this._grid }))));
    }
}

// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var algorithm_dist_index_es6_js_ = __webpack_require__(16415);
;// CONCATENATED MODULE: ../packages/debugger/lib/panels/variables/tree.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







const BUTTONS_CLASS = 'jp-DebuggerVariables-buttons';
/**
 * The body for tree of variables.
 */
class VariablesBodyTree extends index_js_.ReactWidget {
    /**
     * Instantiate a new Body for the tree of variables.
     *
     * @param options The instantiation options for a VariablesBodyTree.
     */
    constructor(options) {
        super();
        this._scope = '';
        this._scopes = [];
        this._filter = new Set();
        this._commands = options.commands;
        this._service = options.service;
        this._translator = options.translator;
        this._hoverChanged = new dist_index_es6_js_.Signal(this);
        const model = (this.model = options.model);
        model.changed.connect(this._updateScopes, this);
        this.addClass('jp-DebuggerVariables-body');
    }
    /**
     * Render the VariablesBodyTree.
     */
    render() {
        var _a;
        const scope = (_a = this._scopes.find(scope => scope.name === this._scope)) !== null && _a !== void 0 ? _a : this._scopes[0];
        const handleSelectVariable = (variable) => {
            this.model.selectedVariable = variable;
        };
        const collapserIcon = (react_index_js_default().createElement(index_js_.caretDownEmptyIcon.react, { stylesheet: "menuItem", tag: "span" }));
        if ((scope === null || scope === void 0 ? void 0 : scope.name) !== 'Globals') {
            this.addClass('jp-debuggerVariables-local');
        }
        else {
            this.removeClass('jp-debuggerVariables-local');
        }
        return scope ? (react_index_js_default().createElement((react_index_js_default()).Fragment, null,
            react_index_js_default().createElement(VariablesBranch, { key: scope.name, commands: this._commands, service: this._service, data: scope.variables, filter: this._filter, translator: this._translator, handleSelectVariable: handleSelectVariable, onHoverChanged: (data) => {
                    this._hoverChanged.emit(data);
                }, collapserIcon: collapserIcon }),
            react_index_js_default().createElement(TreeButtons, { commands: this._commands, service: this._service, hoverChanged: this._hoverChanged, handleSelectVariable: handleSelectVariable }))) : (react_index_js_default().createElement("div", null));
    }
    /**
     * Set the variable filter list.
     */
    set filter(filter) {
        this._filter = filter;
        this.update();
    }
    /**
     * Set the current scope
     */
    set scope(scope) {
        this._scope = scope;
        this.update();
    }
    /**
     * Update the scopes and the tree of variables.
     *
     * @param model The variables model.
     */
    _updateScopes(model) {
        if (algorithm_dist_index_es6_js_.ArrayExt.shallowEqual(this._scopes, model.scopes)) {
            return;
        }
        this._scopes = model.scopes;
        this.update();
    }
}
/**
 * The singleton buttons bar shown by the variables.
 */
const TreeButtons = (props) => {
    var _a;
    const { commands, service, translator, handleSelectVariable } = props;
    const trans = (translator !== null && translator !== void 0 ? translator : translation_lib_index_js_.nullTranslator).load('jupyterlab');
    const [buttonsTop, setButtonsTop] = (0,react_index_js_.useState)(0);
    const [variable, setVariable] = (0,react_index_js_.useState)(null);
    let stateRefreshLock = 0;
    // Empty dependency array is to only register once per lifetime.
    const handleHover = (0,react_index_js_.useCallback)((_, data) => {
        const current = ++stateRefreshLock;
        if (!data.variable) {
            // Handle mouse leave.
            if (current !== stateRefreshLock) {
                return;
            }
            const target = data.target;
            if (target &&
                // Note: Element, not HTMLElement to permit entering <svg> icon.
                target instanceof Element &&
                target.closest(`.${BUTTONS_CLASS}`)) {
                // Allow to enter the buttons.
                return;
            }
            setVariable(null);
        }
        else {
            // Handle mouse over.
            setVariable(data.variable);
            requestAnimationFrame(() => {
                if (current !== stateRefreshLock || !data.target) {
                    return;
                }
                setButtonsTop(data.target.offsetTop);
            });
        }
    }, []);
    (0,react_index_js_.useEffect)(() => {
        props.hoverChanged.connect(handleHover);
        return () => {
            props.hoverChanged.disconnect(handleHover);
        };
    }, [handleHover]);
    return (react_index_js_default().createElement("div", { className: BUTTONS_CLASS, style: 
        // Positioning and hiding is implemented using compositor-only
        // properties (transform and opacity) for performance.
        {
            transform: `translateY(${buttonsTop}px)`,
            opacity: !variable ||
                // Do not show buttons display for special entries, defined in debugpy:
                // https://github.com/microsoft/debugpy/blob/cf0d684566edc339545b161da7c3dfc48af7c7d5/src/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_utils.py#L359
                [
                    'special variables',
                    'protected variables',
                    'function variables',
                    'class variables'
                ].includes(variable.name)
                ? 0
                : 1
        } },
        react_index_js_default().createElement("button", { className: "jp-DebuggerVariables-renderVariable", disabled: !variable ||
                !service.model.hasRichVariableRendering ||
                !commands.isEnabled(Debugger.CommandIDs.renderMimeVariable, {
                    name: variable.name,
                    frameID: (_a = service.model.callstack.frame) === null || _a === void 0 ? void 0 : _a.id
                }), onClick: e => {
                var _a;
                if (!variable || !handleSelectVariable) {
                    return;
                }
                e.stopPropagation();
                handleSelectVariable(variable);
                commands
                    .execute(Debugger.CommandIDs.renderMimeVariable, {
                    name: variable.name,
                    frameID: (_a = service.model.callstack.frame) === null || _a === void 0 ? void 0 : _a.id
                })
                    .catch(reason => {
                    console.error(`Failed to render variable ${variable === null || variable === void 0 ? void 0 : variable.name}`, reason);
                });
            }, title: trans.__('Render variable: %1', variable === null || variable === void 0 ? void 0 : variable.name) },
            react_index_js_default().createElement(index_js_.searchIcon.react, { stylesheet: "menuItem", tag: "span" }))));
};
/**
 * A React component to display a list of variables.
 *
 * @param {object} props The component props.
 * @param props.data An array of variables.
 * @param props.service The debugger service.
 * @param props.filter Optional variable filter list.
 */
const VariablesBranch = (props) => {
    const { commands, data, service, filter, translator, handleSelectVariable, onHoverChanged, collapserIcon } = props;
    const [variables, setVariables] = (0,react_index_js_.useState)(data);
    (0,react_index_js_.useEffect)(() => {
        setVariables(data);
    }, [data]);
    return (react_index_js_default().createElement("ul", { className: "jp-DebuggerVariables-branch" }, variables
        .filter(variable => !(filter || new Set()).has(variable.evaluateName || ''))
        .map(variable => {
        const key = `${variable.name}-${variable.evaluateName}-${variable.type}-${variable.value}-${variable.variablesReference}`;
        return (react_index_js_default().createElement(VariableComponent, { key: key, commands: commands, data: variable, service: service, filter: filter, translator: translator, onSelect: handleSelectVariable, onHoverChanged: onHoverChanged, collapserIcon: collapserIcon }));
    })));
};
function _prepareDetail(variable) {
    const detail = convertType(variable);
    if (variable.type === 'float' && isNaN(detail)) {
        // silence React warning:
        // `Received NaN for the `children` attribute. If this is expected, cast the value to a string`
        return 'NaN';
    }
    return detail;
}
/**
 * A React component to display one node variable in tree.
 *
 * @param {object} props The component props.
 * @param props.data An array of variables.
 * @param props.service The debugger service.
 * @param props.filter Optional variable filter list.
 */
const VariableComponent = (props) => {
    const { commands, data, service, filter, translator, onSelect, onHoverChanged, collapserIcon } = props;
    const [variable] = (0,react_index_js_.useState)(data);
    const [expanded, setExpanded] = (0,react_index_js_.useState)();
    const [variables, setVariables] = (0,react_index_js_.useState)();
    const onSelection = onSelect !== null && onSelect !== void 0 ? onSelect : (() => void 0);
    const expandable = variable.variablesReference !== 0 || variable.type === 'function';
    const onVariableClicked = async (e) => {
        if (!expandable) {
            return;
        }
        e.stopPropagation();
        const variables = await service.inspectVariable(variable.variablesReference);
        setExpanded(!expanded);
        setVariables(variables);
    };
    return (react_index_js_default().createElement("li", { onClick: (e) => onVariableClicked(e), onMouseDown: e => {
            e.stopPropagation();
            onSelection(variable);
        }, onMouseOver: (event) => {
            if (onHoverChanged) {
                onHoverChanged({ target: event.currentTarget, variable });
                event.stopPropagation();
            }
        }, onMouseLeave: (event) => {
            if (onHoverChanged) {
                onHoverChanged({
                    target: event.relatedTarget,
                    variable: null
                });
                event.stopPropagation();
            }
        } },
        react_index_js_default().createElement("span", { className: 'jp-DebuggerVariables-collapser' +
                (expanded ? ' jp-mod-expanded' : '') }, 
        // note: using React.cloneElement due to high typestyle cost
        expandable ? react_index_js_default().cloneElement(collapserIcon) : null),
        react_index_js_default().createElement("span", { className: "jp-DebuggerVariables-name" }, variable.name),
        react_index_js_default().createElement("span", { className: "jp-DebuggerVariables-detail" }, _prepareDetail(variable)),
        expanded && variables && (react_index_js_default().createElement(VariablesBranch, { key: variable.name, commands: commands, data: variables, service: service, filter: filter, translator: translator, handleSelectVariable: onSelect, onHoverChanged: onHoverChanged, collapserIcon: collapserIcon }))));
};

;// CONCATENATED MODULE: ../packages/debugger/lib/panels/variables/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * A Panel to show a variable explorer.
 */
class Variables extends index_js_.PanelWithToolbar {
    /**
     * Instantiate a new Variables Panel.
     *
     * @param options The instantiation options for a Variables Panel.
     */
    constructor(options) {
        super(options);
        const { model, service, commands, themeManager } = options;
        const translator = options.translator || translation_lib_index_js_.nullTranslator;
        const trans = translator.load('jupyterlab');
        this.title.label = trans.__('Variables');
        this.toolbar.addClass('jp-DebuggerVariables-toolbar');
        this._tree = new VariablesBodyTree({
            model,
            service,
            commands,
            translator
        });
        this._table = new VariablesBodyGrid({
            model,
            commands,
            themeManager,
            translator
        });
        this._table.hide();
        this.toolbar.addItem('scope-switcher', new ScopeSwitcher({
            translator,
            model,
            tree: this._tree,
            grid: this._table
        }));
        const onViewChange = () => {
            if (this._table.isHidden) {
                this._tree.hide();
                this._table.show();
                this.node.setAttribute('data-jp-table', 'true');
                markViewButtonSelection('table');
            }
            else {
                this._tree.show();
                this._table.hide();
                this.node.removeAttribute('data-jp-table');
                markViewButtonSelection('tree');
            }
            this.update();
        };
        const treeViewButton = new index_js_.ToolbarButton({
            icon: index_js_.treeViewIcon,
            className: 'jp-TreeView',
            onClick: onViewChange,
            tooltip: trans.__('Tree View')
        });
        const tableViewButton = new index_js_.ToolbarButton({
            icon: index_js_.tableRowsIcon,
            className: 'jp-TableView',
            onClick: onViewChange,
            tooltip: trans.__('Table View')
        });
        const markViewButtonSelection = (selectedView) => {
            const viewModeClassName = 'jp-ViewModeSelected';
            if (selectedView === 'tree') {
                tableViewButton.removeClass(viewModeClassName);
                treeViewButton.addClass(viewModeClassName);
            }
            else {
                treeViewButton.removeClass(viewModeClassName);
                tableViewButton.addClass(viewModeClassName);
            }
        };
        markViewButtonSelection(this._table.isHidden ? 'tree' : 'table');
        this.toolbar.addItem('view-VariableTreeView', treeViewButton);
        this.toolbar.addItem('view-VariableTableView', tableViewButton);
        this.addWidget(this._tree);
        this.addWidget(this._table);
        this.addClass('jp-DebuggerVariables');
    }
    /**
     * Set the variable filter for both the tree and table views.
     */
    set filter(filter) {
        this._tree.filter = filter;
        this._table.filter = filter;
    }
    /**
     * A message handler invoked on a `'resize'` message.
     *
     * @param msg The Lumino message to process.
     */
    onResize(msg) {
        super.onResize(msg);
        this._resizeBody(msg);
    }
    /**
     * Resize the body.
     *
     * @param msg The resize message.
     */
    _resizeBody(msg) {
        const height = msg.height - this.toolbar.node.offsetHeight;
        this._tree.node.style.height = `${height}px`;
    }
}
/**
 * Convert a variable to a primitive type.
 *
 * @param variable The variable.
 */
const convertType = (variable) => {
    var _a, _b;
    const { type, value } = variable;
    switch (type) {
        case 'int':
            return parseInt(value, 10);
        case 'float':
            return parseFloat(value);
        case 'bool':
            return value;
        case 'str':
            if ((_b = (_a = variable.presentationHint) === null || _a === void 0 ? void 0 : _a.attributes) === null || _b === void 0 ? void 0 : _b.includes('rawString')) {
                return value.slice(1, value.length - 1);
            }
            else {
                return value;
            }
        default:
            return type !== null && type !== void 0 ? type : value;
    }
};

;// CONCATENATED MODULE: ../packages/debugger/lib/sidebar.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








/**
 * A debugger sidebar.
 */
class DebuggerSidebar extends index_js_.SidePanel {
    /**
     * Instantiate a new Debugger.Sidebar
     *
     * @param options The instantiation options for a Debugger.Sidebar
     */
    constructor(options) {
        const translator = options.translator || translation_lib_index_js_.nullTranslator;
        super({ translator });
        this.id = 'jp-debugger-sidebar';
        this.title.icon = index_js_.bugIcon;
        this.addClass('jp-DebuggerSidebar');
        const { callstackCommands, breakpointsCommands, editorServices, service, themeManager } = options;
        const model = service.model;
        this.variables = new Variables({
            model: model.variables,
            commands: callstackCommands.registry,
            service,
            themeManager,
            translator
        });
        this.callstack = new Callstack({
            commands: callstackCommands,
            model: model.callstack,
            translator
        });
        this.breakpoints = new Breakpoints({
            service,
            commands: breakpointsCommands,
            model: model.breakpoints,
            translator
        });
        this.sources = new Sources({
            model: model.sources,
            service,
            editorServices,
            translator
        });
        this.kernelSources = new KernelSources({
            model: model.kernelSources,
            service,
            translator
        });
        const header = new DebuggerSidebar.Header();
        this.header.addWidget(header);
        model.titleChanged.connect((_, title) => {
            header.title.label = title;
        });
        this.content.addClass('jp-DebuggerSidebar-body');
        this.addWidget(this.variables);
        this.addWidget(this.callstack);
        this.addWidget(this.breakpoints);
        this.addWidget(this.sources);
        this.addWidget(this.kernelSources);
    }
}
/**
 * A namespace for DebuggerSidebar statics
 */
(function (DebuggerSidebar) {
    /**
     * The header for a debugger sidebar.
     */
    class Header extends index_es6_js_.Widget {
        /**
         * Instantiate a new sidebar header.
         */
        constructor() {
            super({ node: sidebar_Private.createHeader() });
            this.title.changed.connect(_ => {
                this.node.textContent = this.title.label;
            });
        }
    }
    DebuggerSidebar.Header = Header;
})(DebuggerSidebar || (DebuggerSidebar = {}));
/**
 * A namespace for private module data.
 */
var sidebar_Private;
(function (Private) {
    /**
     * Create a sidebar header node.
     */
    function createHeader() {
        const title = document.createElement('h2');
        title.textContent = '-';
        title.classList.add('jp-text-truncated');
        return title;
    }
    Private.createHeader = createHeader;
})(sidebar_Private || (sidebar_Private = {}));

;// CONCATENATED MODULE: ../packages/debugger/lib/sources.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * The source and editor manager for a debugger instance.
 */
class DebuggerSources {
    /**
     * Create a new DebuggerSources instance.
     *
     * @param options The instantiation options for a DebuggerSources instance.
     */
    constructor(options) {
        var _a, _b, _c;
        this._config = options.config;
        this._shell = options.shell;
        this._notebookTracker = (_a = options.notebookTracker) !== null && _a !== void 0 ? _a : null;
        this._consoleTracker = (_b = options.consoleTracker) !== null && _b !== void 0 ? _b : null;
        this._editorTracker = (_c = options.editorTracker) !== null && _c !== void 0 ? _c : null;
        this._readOnlyEditorTracker = new lib_index_js_.WidgetTracker({ namespace: '@jupyterlab/debugger' });
    }
    /**
     * Returns an array of editors for a source matching the current debug
     * session by iterating through all the widgets in each of the supported
     * debugger types (i.e., consoles, files, notebooks).
     *
     * @param params - The editor search parameters.
     */
    find(params) {
        return [
            ...this._findInConsoles(params),
            ...this._findInEditors(params),
            ...this._findInNotebooks(params),
            ...this._findInReadOnlyEditors(params)
        ];
    }
    /**
     * Open a read-only editor in the main area.
     *
     * @param params The editor open parameters.
     */
    open(params) {
        const { editorWrapper, label, caption } = params;
        const widget = new lib_index_js_.MainAreaWidget({
            content: editorWrapper
        });
        widget.id = lib_index_js_.DOMUtils.createDomID();
        widget.title.label = label;
        widget.title.closable = true;
        widget.title.caption = caption;
        widget.title.icon = index_js_.textEditorIcon;
        this._shell.add(widget, 'main', { type: 'Debugger Sources' });
        void this._readOnlyEditorTracker.add(widget);
    }
    /**
     * Find relevant editors matching the search params in the notebook tracker.
     *
     * @param params - The editor search parameters.
     */
    _findInNotebooks(params) {
        if (!this._notebookTracker) {
            return [];
        }
        const { focus, kernel, path, source } = params;
        const editors = [];
        this._notebookTracker.forEach(notebookPanel => {
            const sessionContext = notebookPanel.sessionContext;
            if (path !== sessionContext.path) {
                return;
            }
            const notebook = notebookPanel.content;
            if (focus) {
                notebook.mode = 'command';
            }
            const cells = notebookPanel.content.widgets;
            cells.forEach((cell, i) => {
                // check the event is for the correct cell
                const code = cell.model.sharedModel.getSource();
                const codeId = this._getCodeId(code, kernel);
                if (!codeId) {
                    return;
                }
                if (source !== codeId) {
                    return;
                }
                if (focus) {
                    notebook.activeCellIndex = i;
                    if (notebook.activeCell) {
                        notebook.scrollToItem(notebook.activeCellIndex).catch(reason => {
                            // no-op
                        });
                    }
                    this._shell.activateById(notebookPanel.id);
                }
                editors.push(Object.freeze({
                    get: () => cell.editor,
                    reveal: () => notebook.scrollToItem(i),
                    src: cell.model.sharedModel
                }));
            });
        });
        return editors;
    }
    /**
     * Find relevant editors matching the search params in the console tracker.
     *
     * @param params - The editor search parameters.
     */
    _findInConsoles(params) {
        if (!this._consoleTracker) {
            return [];
        }
        const { focus, kernel, path, source } = params;
        const editors = [];
        this._consoleTracker.forEach(consoleWidget => {
            const sessionContext = consoleWidget.sessionContext;
            if (path !== sessionContext.path) {
                return;
            }
            const cells = consoleWidget.console.cells;
            for (const cell of cells) {
                const code = cell.model.sharedModel.getSource();
                const codeId = this._getCodeId(code, kernel);
                if (!codeId) {
                    break;
                }
                if (source !== codeId) {
                    break;
                }
                editors.push(Object.freeze({
                    get: () => cell.editor,
                    reveal: () => Promise.resolve(this._shell.activateById(consoleWidget.id)),
                    src: cell.model.sharedModel
                }));
                if (focus) {
                    this._shell.activateById(consoleWidget.id);
                }
            }
        });
        return editors;
    }
    /**
     * Find relevant editors matching the search params in the editor tracker.
     *
     * @param params - The editor search parameters.
     */
    _findInEditors(params) {
        if (!this._editorTracker) {
            return [];
        }
        const { focus, kernel, path, source } = params;
        const editors = [];
        this._editorTracker.forEach(doc => {
            const fileEditor = doc.content;
            if (path !== fileEditor.context.path) {
                return;
            }
            const editor = fileEditor.editor;
            if (!editor) {
                return;
            }
            const code = editor.model.sharedModel.getSource();
            const codeId = this._getCodeId(code, kernel);
            if (!codeId) {
                return;
            }
            if (source !== codeId) {
                return;
            }
            editors.push(Object.freeze({
                get: () => editor,
                reveal: () => Promise.resolve(this._shell.activateById(doc.id)),
                src: fileEditor.model.sharedModel
            }));
            if (focus) {
                this._shell.activateById(doc.id);
            }
        });
        return editors;
    }
    /**
     * Find relevant editors matching the search params in the read-only tracker.
     *
     * @param params - The editor search parameters.
     */
    _findInReadOnlyEditors(params) {
        const { focus, kernel, source } = params;
        const editors = [];
        this._readOnlyEditorTracker.forEach(widget => {
            var _a;
            const editor = (_a = widget.content) === null || _a === void 0 ? void 0 : _a.editor;
            if (!editor) {
                return;
            }
            const code = editor.model.sharedModel.getSource();
            const codeId = this._getCodeId(code, kernel);
            if (!codeId) {
                return;
            }
            if (widget.title.caption !== source && source !== codeId) {
                return;
            }
            editors.push(Object.freeze({
                get: () => editor,
                reveal: () => Promise.resolve(this._shell.activateById(widget.id)),
                src: editor.model.sharedModel
            }));
            if (focus) {
                this._shell.activateById(widget.id);
            }
        });
        return editors;
    }
    /**
     * Get the code id for a given source and kernel,
     * and handle the case of a kernel without parameters.
     *
     * @param code The source code.
     * @param kernel The name of the kernel.
     */
    _getCodeId(code, kernel) {
        try {
            return this._config.getCodeId(code, kernel);
        }
        catch (_a) {
            return '';
        }
    }
}

;// CONCATENATED MODULE: ../packages/debugger/lib/debugger.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.














/**
 * A namespace for `Debugger` statics.
 */
var Debugger;
(function (Debugger) {
    /**
     * Debugger configuration for all kernels.
     */
    class Config extends DebuggerConfig {
    }
    Debugger.Config = Config;
    /**
     * A handler for a CodeEditor.IEditor.
     */
    class EditorHandler extends editor_EditorHandler {
    }
    Debugger.EditorHandler = EditorHandler;
    /**
     * A handler for debugging a widget.
     */
    class Handler extends DebuggerHandler {
    }
    Debugger.Handler = Handler;
    /**
     * A model for a debugger.
     */
    class Model extends DebuggerModel {
    }
    Debugger.Model = Model;
    /**
     * A widget factory for read only editors.
     */
    class ReadOnlyEditorFactory extends factory_ReadOnlyEditorFactory {
    }
    Debugger.ReadOnlyEditorFactory = ReadOnlyEditorFactory;
    /**
     * The main IDebugger implementation.
     */
    class Service extends DebuggerService {
    }
    Debugger.Service = Service;
    /**
     * A concrete implementation of IDebugger.ISession.
     */
    class Session extends DebuggerSession {
    }
    Debugger.Session = Session;
    /**
     * The debugger sidebar UI.
     */
    class Sidebar extends DebuggerSidebar {
    }
    Debugger.Sidebar = Sidebar;
    /**
     * The source and editor manager for a debugger instance.
     */
    class Sources extends DebuggerSources {
    }
    Debugger.Sources = Sources;
    /**
     * A data grid that displays variables in a debugger session.
     */
    class VariablesGrid extends VariablesBodyGrid {
    }
    Debugger.VariablesGrid = VariablesGrid;
    /**
     * A widget to display data according to its mime type
     */
    class VariableRenderer extends VariableMimeRenderer {
    }
    Debugger.VariableRenderer = VariableRenderer;
    /**
     * The command IDs used by the debugger plugin.
     */
    let CommandIDs;
    (function (CommandIDs) {
        CommandIDs.debugContinue = 'debugger:continue';
        CommandIDs.terminate = 'debugger:terminate';
        CommandIDs.next = 'debugger:next';
        CommandIDs.showPanel = 'debugger:show-panel';
        CommandIDs.stepIn = 'debugger:stepIn';
        CommandIDs.stepOut = 'debugger:stepOut';
        CommandIDs.inspectVariable = 'debugger:inspect-variable';
        CommandIDs.renderMimeVariable = 'debugger:render-mime-variable';
        CommandIDs.evaluate = 'debugger:evaluate';
        CommandIDs.restartDebug = 'debugger:restart-debug';
        CommandIDs.pauseOnExceptions = 'debugger:pause-on-exceptions';
        CommandIDs.copyToClipboard = 'debugger:copy-to-clipboard';
        CommandIDs.copyToGlobals = 'debugger:copy-to-globals';
    })(CommandIDs = Debugger.CommandIDs || (Debugger.CommandIDs = {}));
    /**
     * The debugger user interface icons.
     */
    let Icons;
    (function (Icons) {
        Icons.closeAllIcon = closeAllIcon;
        Icons.evaluateIcon = index_js_.codeIcon;
        Icons.continueIcon = index_js_.runIcon;
        Icons.pauseIcon = pauseIcon;
        Icons.stepIntoIcon = stepIntoIcon;
        Icons.stepOutIcon = stepOutIcon;
        Icons.stepOverIcon = stepOverIcon;
        Icons.terminateIcon = index_js_.stopIcon;
        Icons.variableIcon = variableIcon;
        Icons.viewBreakpointIcon = viewBreakpointIcon;
        Icons.pauseOnExceptionsIcon = pauseIcon;
    })(Icons = Debugger.Icons || (Debugger.Icons = {}));
    /**
     * The debugger dialog helpers.
     */
    let Dialogs;
    (function (Dialogs) {
        /**
         * Open a code prompt in a dialog.
         */
        Dialogs.getCode = DebuggerEvaluateDialog.getCode;
    })(Dialogs = Debugger.Dialogs || (Debugger.Dialogs = {}));
})(Debugger || (Debugger = {}));


/***/ }),

/***/ 50712:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "Debugger": () => (/* reexport */ lib_debugger/* Debugger */.q),
  "IDebugger": () => (/* reexport */ IDebugger),
  "IDebuggerConfig": () => (/* reexport */ IDebuggerConfig),
  "IDebuggerHandler": () => (/* reexport */ IDebuggerHandler),
  "IDebuggerSidebar": () => (/* reexport */ IDebuggerSidebar),
  "IDebuggerSources": () => (/* reexport */ IDebuggerSources)
});

// EXTERNAL MODULE: ../packages/debugger/lib/debugger.js + 45 modules
var lib_debugger = __webpack_require__(58986);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var index_js_ = __webpack_require__(22100);
;// CONCATENATED MODULE: ../packages/debugger/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The visual debugger token.
 */
const IDebugger = new index_js_.Token('@jupyterlab/debugger:IDebugger', 'A debugger user interface.');
/**
 * The debugger configuration token.
 */
const IDebuggerConfig = new index_js_.Token('@jupyterlab/debugger:IDebuggerConfig', 'A service to handle the debugger configuration.');
/**
 * The debugger sources utility token.
 */
const IDebuggerSources = new index_js_.Token('@jupyterlab/debugger:IDebuggerSources', 'A service to display sources in debug mode.');
/**
 * The debugger sidebar token.
 */
const IDebuggerSidebar = new index_js_.Token('@jupyterlab/debugger:IDebuggerSidebar', 'A service for the debugger sidebar.');
/**
 * The debugger handler token.
 */
const IDebuggerHandler = new index_js_.Token('@jupyterlab/debugger:IDebuggerHandler', 'A service for handling notebook debugger.');

;// CONCATENATED MODULE: ../packages/debugger/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module debugger
 */




/***/ })

}]);
//# sourceMappingURL=712.8c2711efcb6e2633985a.js.map?v=8c2711efcb6e2633985a