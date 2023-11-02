"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[5782],{

/***/ 95782:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "CodeEditor": () => (/* reexport */ CodeEditor),
  "CodeEditorWrapper": () => (/* reexport */ CodeEditorWrapper),
  "CodeViewerWidget": () => (/* reexport */ CodeViewerWidget),
  "IEditorMimeTypeService": () => (/* reexport */ IEditorMimeTypeService),
  "IEditorServices": () => (/* reexport */ IEditorServices),
  "IPositionModel": () => (/* reexport */ IPositionModel),
  "JSONEditor": () => (/* reexport */ JSONEditor),
  "LineCol": () => (/* reexport */ LineCol)
});

// EXTERNAL MODULE: consume shared module (default) @jupyter/ydoc@~1.0.2 (singleton) (fallback: ../node_modules/@jupyter/ydoc/lib/index.js)
var index_js_ = __webpack_require__(69688);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/observables@~5.1.0-alpha.2 (strict) (fallback: ../packages/observables/lib/index.js)
var lib_index_js_ = __webpack_require__(57090);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(30205);
;// CONCATENATED MODULE: ../packages/codeeditor/lib/mimetype.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * A namespace for `IEditorMimeTypeService`.
 */
var IEditorMimeTypeService;
(function (IEditorMimeTypeService) {
    /**
     * The default mime type.
     */
    IEditorMimeTypeService.defaultMimeType = 'text/plain';
})(IEditorMimeTypeService || (IEditorMimeTypeService = {}));

;// CONCATENATED MODULE: ../packages/codeeditor/lib/editor.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * A namespace for code editors.
 *
 * #### Notes
 * - A code editor is a set of common assumptions which hold for all concrete editors.
 * - Changes in implementations of the code editor should only be caused by changes in concrete editors.
 * - Common JLab services which are based on the code editor should belong to `IEditorServices`.
 */
var CodeEditor;
(function (CodeEditor) {
    /**
     * The default implementation of the editor model.
     */
    class Model {
        /**
         * Construct a new Model.
         */
        constructor(options = {}) {
            var _a, _b;
            /**
             * Whether the model should disposed the shared model on disposal or not.
             */
            this.standaloneModel = false;
            this._isDisposed = false;
            this._selections = new lib_index_js_.ObservableMap();
            this._mimeType = IEditorMimeTypeService.defaultMimeType;
            this._mimeTypeChanged = new index_es6_js_.Signal(this);
            // Track if we need to dispose the model or not.
            this.standaloneModel = typeof options.sharedModel === 'undefined';
            this.sharedModel = (_a = options.sharedModel) !== null && _a !== void 0 ? _a : new index_js_.YFile();
            this._mimeType =
                (_b = options.mimeType) !== null && _b !== void 0 ? _b : IEditorMimeTypeService.defaultMimeType;
        }
        /**
         * A signal emitted when a mimetype changes.
         */
        get mimeTypeChanged() {
            return this._mimeTypeChanged;
        }
        /**
         * Get the selections for the model.
         */
        get selections() {
            return this._selections;
        }
        /**
         * A mime type of the model.
         */
        get mimeType() {
            return this._mimeType;
        }
        set mimeType(newValue) {
            const oldValue = this.mimeType;
            if (oldValue === newValue) {
                return;
            }
            this._mimeType = newValue;
            this._mimeTypeChanged.emit({
                name: 'mimeType',
                oldValue: oldValue,
                newValue: newValue
            });
        }
        /**
         * Whether the model is disposed.
         */
        get isDisposed() {
            return this._isDisposed;
        }
        /**
         * Dispose of the resources used by the model.
         */
        dispose() {
            if (this._isDisposed) {
                return;
            }
            this._isDisposed = true;
            this._selections.dispose();
            if (this.standaloneModel) {
                this.sharedModel.dispose();
            }
            index_es6_js_.Signal.clearData(this);
        }
    }
    CodeEditor.Model = Model;
})(CodeEditor || (CodeEditor = {}));

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/codeeditor/lib/jsoneditor.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * The class name added to a JSONEditor instance.
 */
const JSONEDITOR_CLASS = 'jp-JSONEditor';
/**
 * The class name added when the Metadata editor contains invalid JSON.
 */
const ERROR_CLASS = 'jp-mod-error';
/**
 * The class name added to the editor host node.
 */
const HOST_CLASS = 'jp-JSONEditor-host';
/**
 * The class name added to the header area.
 */
const HEADER_CLASS = 'jp-JSONEditor-header';
/**
 * A widget for editing observable JSON.
 */
class JSONEditor extends dist_index_es6_js_.Widget {
    /**
     * Construct a new JSON editor.
     */
    constructor(options) {
        super();
        this._dataDirty = false;
        this._inputDirty = false;
        this._source = null;
        this._originalValue = dist_index_js_.JSONExt.emptyObject;
        this._changeGuard = false;
        this.translator = options.translator || translation_lib_index_js_.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this.addClass(JSONEDITOR_CLASS);
        this.headerNode = document.createElement('div');
        this.headerNode.className = HEADER_CLASS;
        this.revertButtonNode = ui_components_lib_index_js_.undoIcon.element({
            tag: 'span',
            title: this._trans.__('Revert changes to data')
        });
        this.commitButtonNode = ui_components_lib_index_js_.checkIcon.element({
            tag: 'span',
            title: this._trans.__('Commit changes to data'),
            marginLeft: '8px'
        });
        this.editorHostNode = document.createElement('div');
        this.editorHostNode.className = HOST_CLASS;
        this.headerNode.appendChild(this.revertButtonNode);
        this.headerNode.appendChild(this.commitButtonNode);
        this.node.appendChild(this.headerNode);
        this.node.appendChild(this.editorHostNode);
        const model = new CodeEditor.Model({ mimeType: 'application/json' });
        model.sharedModel.changed.connect(this._onModelChanged, this);
        this.model = model;
        this.editor = options.editorFactory({
            host: this.editorHostNode,
            model,
            config: {
                readOnly: true
            }
        });
    }
    /**
     * The observable source.
     */
    get source() {
        return this._source;
    }
    set source(value) {
        if (this._source === value) {
            return;
        }
        if (this._source) {
            this._source.changed.disconnect(this._onSourceChanged, this);
        }
        this._source = value;
        this.editor.setOption('readOnly', value === null);
        if (value) {
            value.changed.connect(this._onSourceChanged, this);
        }
        this._setValue();
    }
    /**
     * Get whether the editor is dirty.
     */
    get isDirty() {
        return this._dataDirty || this._inputDirty;
    }
    /**
     * Dispose of the editor.
     */
    dispose() {
        var _a;
        if (this.isDisposed) {
            return;
        }
        (_a = this.source) === null || _a === void 0 ? void 0 : _a.dispose();
        this.model.dispose();
        this.editor.dispose();
        super.dispose();
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the notebook panel's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'blur':
                this._evtBlur(event);
                break;
            case 'click':
                this._evtClick(event);
                break;
            default:
                break;
        }
    }
    /**
     * Handle `after-attach` messages for the widget.
     */
    onAfterAttach(msg) {
        const node = this.editorHostNode;
        node.addEventListener('blur', this, true);
        node.addEventListener('click', this, true);
        this.revertButtonNode.hidden = true;
        this.commitButtonNode.hidden = true;
        this.headerNode.addEventListener('click', this);
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        const node = this.editorHostNode;
        node.removeEventListener('blur', this, true);
        node.removeEventListener('click', this, true);
        this.headerNode.removeEventListener('click', this);
    }
    /**
     * Handle a change to the metadata of the source.
     */
    _onSourceChanged(sender, args) {
        if (this._changeGuard) {
            return;
        }
        if (this._inputDirty || this.editor.hasFocus()) {
            this._dataDirty = true;
            return;
        }
        this._setValue();
    }
    /**
     * Handle change events.
     */
    _onModelChanged(model, change) {
        if (change.sourceChange) {
            let valid = true;
            try {
                const value = JSON.parse(this.editor.model.sharedModel.getSource());
                this.removeClass(ERROR_CLASS);
                this._inputDirty =
                    !this._changeGuard && !dist_index_js_.JSONExt.deepEqual(value, this._originalValue);
            }
            catch (err) {
                this.addClass(ERROR_CLASS);
                this._inputDirty = true;
                valid = false;
            }
            this.revertButtonNode.hidden = !this._inputDirty;
            this.commitButtonNode.hidden = !valid || !this._inputDirty;
        }
    }
    /**
     * Handle blur events for the text area.
     */
    _evtBlur(event) {
        // Update the metadata if necessary.
        if (!this._inputDirty && this._dataDirty) {
            this._setValue();
        }
    }
    /**
     * Handle click events for the buttons.
     */
    _evtClick(event) {
        const target = event.target;
        if (this.revertButtonNode.contains(target)) {
            this._setValue();
        }
        else if (this.commitButtonNode.contains(target)) {
            if (!this.commitButtonNode.hidden && !this.hasClass(ERROR_CLASS)) {
                this._changeGuard = true;
                this._mergeContent();
                this._changeGuard = false;
                this._setValue();
            }
        }
        else if (this.editorHostNode.contains(target)) {
            this.editor.focus();
        }
    }
    /**
     * Merge the user content.
     */
    _mergeContent() {
        const model = this.editor.model;
        const old = this._originalValue;
        const user = JSON.parse(model.sharedModel.getSource());
        const source = this.source;
        if (!source) {
            return;
        }
        // If it is in user and has changed from old, set in new.
        for (const key in user) {
            if (!dist_index_js_.JSONExt.deepEqual(user[key], old[key] || null)) {
                source.set(key, user[key]);
            }
        }
        // If it was in old and is not in user, remove from source.
        for (const key in old) {
            if (!(key in user)) {
                source.delete(key);
            }
        }
    }
    /**
     * Set the value given the owner contents.
     */
    _setValue() {
        this._dataDirty = false;
        this._inputDirty = false;
        this.revertButtonNode.hidden = true;
        this.commitButtonNode.hidden = true;
        this.removeClass(ERROR_CLASS);
        const model = this.editor.model;
        const content = this._source ? this._source.toJSON() : {};
        this._changeGuard = true;
        if (content === void 0) {
            model.sharedModel.setSource(this._trans.__('No data!'));
            this._originalValue = dist_index_js_.JSONExt.emptyObject;
        }
        else {
            const value = JSON.stringify(content, null, 4);
            model.sharedModel.setSource(value);
            this._originalValue = content;
            // Move the cursor to within the brace.
            if (value.length > 1 && value[0] === '{') {
                this.editor.setCursorPosition({ line: 0, column: 1 });
            }
        }
        this._changeGuard = false;
        this.commitButtonNode.hidden = true;
        this.revertButtonNode.hidden = true;
    }
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/statusbar@~4.1.0-alpha.2 (singleton) (fallback: ../packages/statusbar/lib/index.js)
var statusbar_lib_index_js_ = __webpack_require__(34853);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
var react_index_js_default = /*#__PURE__*/__webpack_require__.n(react_index_js_);
;// CONCATENATED MODULE: ../packages/codeeditor/lib/lineCol.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * A component for rendering a "go-to-line" form.
 */
class LineFormComponent extends (react_index_js_default()).Component {
    /**
     * Construct a new LineFormComponent.
     */
    constructor(props) {
        super(props);
        /**
         * Handle a change to the value in the input field.
         */
        this._handleChange = (event) => {
            this.setState({ value: event.currentTarget.value });
        };
        /**
         * Handle submission of the input field.
         */
        this._handleSubmit = (event) => {
            event.preventDefault();
            const value = parseInt(this._textInput.value, 10);
            if (!isNaN(value) &&
                isFinite(value) &&
                1 <= value &&
                value <= this.props.maxLine) {
                this.props.handleSubmit(value);
            }
            return false;
        };
        /**
         * Handle focusing of the input field.
         */
        this._handleFocus = () => {
            this.setState({ hasFocus: true });
        };
        /**
         * Handle blurring of the input field.
         */
        this._handleBlur = () => {
            this.setState({ hasFocus: false });
        };
        this._textInput = null;
        this.translator = props.translator || translation_lib_index_js_.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this.state = {
            value: '',
            hasFocus: false
        };
    }
    /**
     * Focus the element on mount.
     */
    componentDidMount() {
        this._textInput.focus();
    }
    /**
     * Render the LineFormComponent.
     */
    render() {
        return (react_index_js_default().createElement("div", { className: "jp-lineFormSearch" },
            react_index_js_default().createElement("form", { name: "lineColumnForm", onSubmit: this._handleSubmit, noValidate: true },
                react_index_js_default().createElement("div", { className: (0,ui_components_lib_index_js_.classes)('jp-lineFormWrapper', 'lm-lineForm-wrapper', this.state.hasFocus ? 'jp-lineFormWrapperFocusWithin' : undefined) },
                    react_index_js_default().createElement("input", { type: "text", className: "jp-lineFormInput", onChange: this._handleChange, onFocus: this._handleFocus, onBlur: this._handleBlur, value: this.state.value, ref: input => {
                            this._textInput = input;
                        } }),
                    react_index_js_default().createElement("div", { className: "jp-baseLineForm jp-lineFormButtonContainer" },
                        react_index_js_default().createElement(ui_components_lib_index_js_.lineFormIcon.react, { className: "jp-baseLineForm jp-lineFormButtonIcon", elementPosition: "center" }),
                        react_index_js_default().createElement("input", { type: "submit", className: "jp-baseLineForm jp-lineFormButton", value: "" }))),
                react_index_js_default().createElement("label", { className: "jp-lineFormCaption" }, this._trans.__('Go to line number between 1 and %1', this.props.maxLine)))));
    }
}
/**
 * A pure functional component for rendering a line/column
 * status item.
 */
function LineColComponent(props) {
    const translator = props.translator || translation_lib_index_js_.nullTranslator;
    const trans = translator.load('jupyterlab');
    return (react_index_js_default().createElement(statusbar_lib_index_js_.TextItem, { onClick: props.handleClick, source: trans.__('Ln %1, Col %2', props.line, props.column), title: trans.__('Go to line number…') }));
}
/**
 * A widget implementing a line/column status item.
 */
class LineCol extends ui_components_lib_index_js_.VDomRenderer {
    /**
     * Construct a new LineCol status item.
     */
    constructor(translator) {
        super(new LineCol.Model());
        this._popup = null;
        this.addClass('jp-mod-highlighted');
        this.translator = translator || translation_lib_index_js_.nullTranslator;
    }
    /**
     * Render the status item.
     */
    render() {
        if (this.model === null) {
            return null;
        }
        else {
            return (react_index_js_default().createElement(LineColComponent, { line: this.model.line, column: this.model.column, translator: this.translator, handleClick: () => this._handleClick() }));
        }
    }
    /**
     * A click handler for the widget.
     */
    _handleClick() {
        if (this._popup) {
            this._popup.dispose();
        }
        const body = ui_components_lib_index_js_.ReactWidget.create(react_index_js_default().createElement(LineFormComponent, { handleSubmit: val => this._handleSubmit(val), currentLine: this.model.line, maxLine: this.model.editor.lineCount, translator: this.translator }));
        this._popup = (0,statusbar_lib_index_js_.showPopup)({
            body: body,
            anchor: this,
            align: 'right'
        });
    }
    /**
     * Handle submission for the widget.
     */
    _handleSubmit(value) {
        this.model.editor.setCursorPosition({ line: value - 1, column: 0 });
        this._popup.dispose();
        this.model.editor.focus();
    }
}
/**
 * A namespace for LineCol statics.
 */
(function (LineCol) {
    /**
     * A VDom model for a status item tracking the line/column of an editor.
     */
    class Model extends ui_components_lib_index_js_.VDomModel {
        constructor() {
            super(...arguments);
            /**
             * React to a change in the cursors of the current editor.
             */
            this._onSelectionChanged = () => {
                const oldState = this._getAllState();
                const pos = this.editor.getCursorPosition();
                this._line = pos.line + 1;
                this._column = pos.column + 1;
                this._triggerChange(oldState, this._getAllState());
            };
            this._line = 1;
            this._column = 1;
            this._editor = null;
        }
        /**
         * The current editor of the model.
         */
        get editor() {
            return this._editor;
        }
        set editor(editor) {
            var _a;
            const oldEditor = this._editor;
            if ((_a = oldEditor === null || oldEditor === void 0 ? void 0 : oldEditor.model) === null || _a === void 0 ? void 0 : _a.selections) {
                oldEditor.model.selections.changed.disconnect(this._onSelectionChanged);
            }
            const oldState = this._getAllState();
            this._editor = editor;
            if (!this._editor) {
                this._column = 1;
                this._line = 1;
            }
            else {
                this._editor.model.selections.changed.connect(this._onSelectionChanged);
                const pos = this._editor.getCursorPosition();
                this._column = pos.column + 1;
                this._line = pos.line + 1;
            }
            this._triggerChange(oldState, this._getAllState());
        }
        /**
         * The current line of the model.
         */
        get line() {
            return this._line;
        }
        /**
         * The current column of the model.
         */
        get column() {
            return this._column;
        }
        _getAllState() {
            return [this._line, this._column];
        }
        _triggerChange(oldState, newState) {
            if (oldState[0] !== newState[0] || oldState[1] !== newState[1]) {
                this.stateChanged.emit(void 0);
            }
        }
    }
    LineCol.Model = Model;
})(LineCol || (LineCol = {}));

;// CONCATENATED MODULE: ../packages/codeeditor/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * Code editor services token.
 */
const IEditorServices = new dist_index_js_.Token('@jupyterlab/codeeditor:IEditorServices', `A service for the text editor provider
  for the application. Use this to create new text editors and host them in your
  UI elements.`);
/**
 * Code editor cursor position token.
 */
const IPositionModel = new dist_index_js_.Token('@jupyterlab/codeeditor:IPositionModel', `A service to handle an code editor cursor position.`);

;// CONCATENATED MODULE: ../packages/codeeditor/lib/widget.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The class name added to an editor widget that has a primary selection.
 */
const HAS_SELECTION_CLASS = 'jp-mod-has-primary-selection';
/**
 * The class name added to an editor widget that has a cursor/selection
 * within the whitespace at the beginning of a line
 */
const HAS_IN_LEADING_WHITESPACE_CLASS = 'jp-mod-in-leading-whitespace';
/**
 * A class used to indicate a drop target.
 */
const DROP_TARGET_CLASS = 'jp-mod-dropTarget';
/**
 * RegExp to test for leading whitespace
 */
const leadingWhitespaceRe = /^\s+$/;
/**
 * A widget which hosts a code editor.
 */
class CodeEditorWrapper extends dist_index_es6_js_.Widget {
    /**
     * Construct a new code editor widget.
     */
    constructor(options) {
        super();
        const { factory, model, editorOptions } = options;
        const editor = (this.editor = factory({
            host: this.node,
            model,
            ...editorOptions
        }));
        editor.model.selections.changed.connect(this._onSelectionsChanged, this);
    }
    /**
     * Get the model used by the widget.
     */
    get model() {
        return this.editor.model;
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.editor.dispose();
        super.dispose();
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the notebook panel's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'lm-dragenter':
                this._evtDragEnter(event);
                break;
            case 'lm-dragleave':
                this._evtDragLeave(event);
                break;
            case 'lm-dragover':
                this._evtDragOver(event);
                break;
            case 'lm-drop':
                this._evtDrop(event);
                break;
            default:
                break;
        }
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        this.editor.focus();
    }
    /**
     * A message handler invoked on an `'after-attach'` message.
     */
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        const node = this.node;
        node.addEventListener('lm-dragenter', this);
        node.addEventListener('lm-dragleave', this);
        node.addEventListener('lm-dragover', this);
        node.addEventListener('lm-drop', this);
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        const node = this.node;
        node.removeEventListener('lm-dragenter', this);
        node.removeEventListener('lm-dragleave', this);
        node.removeEventListener('lm-dragover', this);
        node.removeEventListener('lm-drop', this);
    }
    /**
     * Handle a change in model selections.
     */
    _onSelectionsChanged() {
        const { start, end } = this.editor.getSelection();
        if (start.column !== end.column || start.line !== end.line) {
            // a selection was made
            this.addClass(HAS_SELECTION_CLASS);
            this.removeClass(HAS_IN_LEADING_WHITESPACE_CLASS);
        }
        else {
            // the cursor was placed
            this.removeClass(HAS_SELECTION_CLASS);
            if (this.editor
                .getLine(end.line)
                .slice(0, end.column)
                .match(leadingWhitespaceRe)) {
                this.addClass(HAS_IN_LEADING_WHITESPACE_CLASS);
            }
            else {
                this.removeClass(HAS_IN_LEADING_WHITESPACE_CLASS);
            }
        }
    }
    /**
     * Handle the `'lm-dragenter'` event for the widget.
     */
    _evtDragEnter(event) {
        if (this.editor.getOption('readOnly') === true) {
            return;
        }
        const data = Private.findTextData(event.mimeData);
        if (data === undefined) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
        this.addClass('jp-mod-dropTarget');
    }
    /**
     * Handle the `'lm-dragleave'` event for the widget.
     */
    _evtDragLeave(event) {
        this.removeClass(DROP_TARGET_CLASS);
        if (this.editor.getOption('readOnly') === true) {
            return;
        }
        const data = Private.findTextData(event.mimeData);
        if (data === undefined) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
    }
    /**
     * Handle the `'lm-dragover'` event for the widget.
     */
    _evtDragOver(event) {
        this.removeClass(DROP_TARGET_CLASS);
        if (this.editor.getOption('readOnly') === true) {
            return;
        }
        const data = Private.findTextData(event.mimeData);
        if (data === undefined) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
        event.dropAction = 'copy';
        this.addClass(DROP_TARGET_CLASS);
    }
    /**
     * Handle the `'lm-drop'` event for the widget.
     */
    _evtDrop(event) {
        if (this.editor.getOption('readOnly') === true) {
            return;
        }
        const data = Private.findTextData(event.mimeData);
        if (data === undefined) {
            return;
        }
        const coordinate = {
            top: event.y,
            bottom: event.y,
            left: event.x,
            right: event.x,
            x: event.x,
            y: event.y,
            width: 0,
            height: 0
        };
        const position = this.editor.getPositionForCoordinate(coordinate);
        if (position === null) {
            return;
        }
        this.removeClass(DROP_TARGET_CLASS);
        event.preventDefault();
        event.stopPropagation();
        if (event.proposedAction === 'none') {
            event.dropAction = 'none';
            return;
        }
        const offset = this.editor.getOffsetAt(position);
        this.model.sharedModel.updateSource(offset, offset, data);
    }
}
/**
 * A namespace for private functionality.
 */
var Private;
(function (Private) {
    /**
     * Given a MimeData instance, extract the first text data, if any.
     */
    function findTextData(mime) {
        const types = mime.types();
        const textType = types.find(t => t.indexOf('text') === 0);
        if (textType === undefined) {
            return undefined;
        }
        return mime.getData(textType);
    }
    Private.findTextData = findTextData;
})(Private || (Private = {}));

;// CONCATENATED MODULE: ../packages/codeeditor/lib/viewer.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



class CodeViewerWidget extends dist_index_es6_js_.Widget {
    /**
     * Construct a new code viewer widget.
     */
    constructor(options) {
        var _a;
        super();
        this.model = options.model;
        const editorWidget = new CodeEditorWrapper({
            factory: options.factory,
            model: this.model,
            editorOptions: {
                ...options.editorOptions,
                config: { ...(_a = options.editorOptions) === null || _a === void 0 ? void 0 : _a.config, readOnly: true }
            }
        });
        this.editor = editorWidget.editor;
        const layout = (this.layout = new dist_index_es6_js_.StackedLayout());
        layout.addWidget(editorWidget);
    }
    static createCodeViewer(options) {
        const { content, mimeType, ...others } = options;
        const model = new CodeEditor.Model({
            mimeType
        });
        model.sharedModel.setSource(content);
        const widget = new CodeViewerWidget({ ...others, model });
        widget.disposed.connect(() => {
            model.dispose();
        });
        return widget;
    }
    get content() {
        return this.model.sharedModel.getSource();
    }
    get mimeType() {
        return this.model.mimeType;
    }
}

;// CONCATENATED MODULE: ../packages/codeeditor/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module codeeditor
 */










/***/ })

}]);
//# sourceMappingURL=5782.ed0828bf885e8086e797.js.map?v=ed0828bf885e8086e797