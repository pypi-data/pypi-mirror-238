"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[4942],{

/***/ 34942:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "AttachmentsCell": () => (/* reexport */ AttachmentsCell),
  "AttachmentsCellModel": () => (/* reexport */ AttachmentsCellModel),
  "Cell": () => (/* reexport */ Cell),
  "CellDragUtils": () => (/* reexport */ CellDragUtils),
  "CellFooter": () => (/* reexport */ CellFooter),
  "CellHeader": () => (/* reexport */ CellHeader),
  "CellModel": () => (/* reexport */ CellModel),
  "CellSearchProvider": () => (/* reexport */ CellSearchProvider),
  "CodeCell": () => (/* reexport */ CodeCell),
  "CodeCellLayout": () => (/* reexport */ CodeCellLayout),
  "CodeCellModel": () => (/* reexport */ CodeCellModel),
  "Collapser": () => (/* reexport */ Collapser),
  "InputArea": () => (/* reexport */ InputArea),
  "InputCollapser": () => (/* reexport */ InputCollapser),
  "InputPlaceholder": () => (/* reexport */ InputPlaceholder),
  "InputPrompt": () => (/* reexport */ InputPrompt),
  "MarkdownCell": () => (/* reexport */ MarkdownCell),
  "MarkdownCellModel": () => (/* reexport */ MarkdownCellModel),
  "OutputCollapser": () => (/* reexport */ OutputCollapser),
  "OutputPlaceholder": () => (/* reexport */ OutputPlaceholder),
  "Placeholder": () => (/* reexport */ Placeholder),
  "RawCell": () => (/* reexport */ RawCell),
  "RawCellModel": () => (/* reexport */ RawCellModel),
  "SELECTED_HIGHLIGHT_CLASS": () => (/* reexport */ SELECTED_HIGHLIGHT_CLASS),
  "createCellSearchProvider": () => (/* reexport */ createCellSearchProvider),
  "isCodeCellModel": () => (/* reexport */ isCodeCellModel),
  "isMarkdownCellModel": () => (/* reexport */ isMarkdownCellModel),
  "isRawCellModel": () => (/* reexport */ isRawCellModel)
});

// EXTERNAL MODULE: consume shared module (default) @lumino/virtualdom@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/virtualdom/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(49581);
;// CONCATENATED MODULE: ../packages/cells/lib/celldragutils.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/

/**
 * Constants for drag
 */
/**
 * The threshold in pixels to start a drag event.
 */
const DRAG_THRESHOLD = 5;
/**
 * The class name added to drag images.
 */
const DRAG_IMAGE_CLASS = 'jp-dragImage';
/**
 * The class name added to singular drag images
 */
const SINGLE_DRAG_IMAGE_CLASS = 'jp-dragImage-singlePrompt';
/**
 * The class name added to the drag image cell content.
 */
const CELL_DRAG_CONTENT_CLASS = 'jp-dragImage-content';
/**
 * The class name added to the drag image cell content.
 */
const CELL_DRAG_PROMPT_CLASS = 'jp-dragImage-prompt';
/**
 * The class name added to the drag image cell content.
 */
const CELL_DRAG_MULTIPLE_BACK = 'jp-dragImage-multipleBack';
var CellDragUtils;
(function (CellDragUtils) {
    /**
     * Find the cell index containing the target html element.
     * This function traces up the DOM hierarchy to find the root cell
     * node. Then find the corresponding child and select it.
     *
     * @param node - the cell node or a child of the cell node.
     * @param cells - an iterable of Cells
     * @param isCellNode - a function that takes in a node and checks if
     * it is a cell node.
     *
     * @returns index of the cell we're looking for. Returns -1 if
     * the cell is not founds
     */
    function findCell(node, cells, isCellNode) {
        let cellIndex = -1;
        while (node && node.parentElement) {
            if (isCellNode(node)) {
                let index = -1;
                for (const cell of cells) {
                    if (cell.node === node) {
                        cellIndex = ++index;
                        break;
                    }
                }
                break;
            }
            node = node.parentElement;
        }
        return cellIndex;
    }
    CellDragUtils.findCell = findCell;
    /**
     * Detect which part of the cell triggered the MouseEvent
     *
     * @param cell - The cell which contains the MouseEvent's target
     * @param target - The DOM node which triggered the MouseEvent
     */
    function detectTargetArea(cell, target) {
        var _a, _b;
        let targetArea;
        if (cell) {
            if ((_a = cell.editorWidget) === null || _a === void 0 ? void 0 : _a.node.contains(target)) {
                targetArea = 'input';
            }
            else if ((_b = cell.promptNode) === null || _b === void 0 ? void 0 : _b.contains(target)) {
                targetArea = 'prompt';
            }
            else {
                targetArea = 'cell';
            }
        }
        else {
            targetArea = 'unknown';
        }
        return targetArea;
    }
    CellDragUtils.detectTargetArea = detectTargetArea;
    /**
     * Detect if a drag event should be started. This is down if the
     * mouse is moved beyond a certain distance (DRAG_THRESHOLD).
     *
     * @param prevX - X Coordinate of the mouse pointer during the mousedown event
     * @param prevY - Y Coordinate of the mouse pointer during the mousedown event
     * @param nextX - Current X Coordinate of the mouse pointer
     * @param nextY - Current Y Coordinate of the mouse pointer
     */
    function shouldStartDrag(prevX, prevY, nextX, nextY) {
        const dx = Math.abs(nextX - prevX);
        const dy = Math.abs(nextY - prevY);
        return dx >= DRAG_THRESHOLD || dy >= DRAG_THRESHOLD;
    }
    CellDragUtils.shouldStartDrag = shouldStartDrag;
    /**
     * Create an image for the cell(s) to be dragged
     *
     * @param activeCell - The cell from where the drag event is triggered
     * @param selectedCells - The cells to be dragged
     */
    function createCellDragImage(activeCell, selectedCells) {
        const count = selectedCells.length;
        let promptNumber;
        if (activeCell.model.type === 'code') {
            const executionCount = activeCell.model
                .executionCount;
            promptNumber = ' ';
            if (executionCount) {
                promptNumber = executionCount.toString();
            }
        }
        else {
            promptNumber = '';
        }
        const cellContent = activeCell.model.sharedModel
            .getSource()
            .split('\n')[0]
            .slice(0, 26);
        if (count > 1) {
            if (promptNumber !== '') {
                return index_es6_js_.VirtualDOM.realize(index_es6_js_.h.div(index_es6_js_.h.div({ className: DRAG_IMAGE_CLASS }, index_es6_js_.h.span({ className: CELL_DRAG_PROMPT_CLASS }, '[' + promptNumber + ']:'), index_es6_js_.h.span({ className: CELL_DRAG_CONTENT_CLASS }, cellContent)), index_es6_js_.h.div({ className: CELL_DRAG_MULTIPLE_BACK }, '')));
            }
            else {
                return index_es6_js_.VirtualDOM.realize(index_es6_js_.h.div(index_es6_js_.h.div({ className: DRAG_IMAGE_CLASS }, index_es6_js_.h.span({ className: CELL_DRAG_PROMPT_CLASS }), index_es6_js_.h.span({ className: CELL_DRAG_CONTENT_CLASS }, cellContent)), index_es6_js_.h.div({ className: CELL_DRAG_MULTIPLE_BACK }, '')));
            }
        }
        else {
            if (promptNumber !== '') {
                return index_es6_js_.VirtualDOM.realize(index_es6_js_.h.div(index_es6_js_.h.div({ className: `${DRAG_IMAGE_CLASS} ${SINGLE_DRAG_IMAGE_CLASS}` }, index_es6_js_.h.span({ className: CELL_DRAG_PROMPT_CLASS }, '[' + promptNumber + ']:'), index_es6_js_.h.span({ className: CELL_DRAG_CONTENT_CLASS }, cellContent))));
            }
            else {
                return index_es6_js_.VirtualDOM.realize(index_es6_js_.h.div(index_es6_js_.h.div({ className: `${DRAG_IMAGE_CLASS} ${SINGLE_DRAG_IMAGE_CLASS}` }, index_es6_js_.h.span({ className: CELL_DRAG_PROMPT_CLASS }), index_es6_js_.h.span({ className: CELL_DRAG_CONTENT_CLASS }, cellContent))));
            }
        }
    }
    CellDragUtils.createCellDragImage = createCellDragImage;
})(CellDragUtils || (CellDragUtils = {}));

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/domutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/domutils/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(92654);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
;// CONCATENATED MODULE: ../packages/cells/lib/collapser.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/



/**
 * The CSS class added to all collapsers.
 */
const COLLAPSER_CLASS = 'jp-Collapser';
/**
 * The CSS class added to the collapser child.
 */
const COLLAPSER_CHILD_CLASS = 'jp-Collapser-child';
/**
 * The CSS class added to input collapsers.
 */
const INPUT_COLLAPSER = 'jp-InputCollapser';
/**
 * The CSS class added to output collapsers.
 */
const OUTPUT_COLLAPSER = 'jp-OutputCollapser';
/**
 * Abstract collapser base class.
 *
 * ### Notes
 * A collapser is a visible div to the left of a cell's
 * input/output that a user can click on to collapse the
 * input/output.
 */
class Collapser extends index_js_.ReactWidget {
    /**
     * Construct a new collapser.
     */
    constructor() {
        super();
        this.addClass(COLLAPSER_CLASS);
    }
    /**
     * Is the input/output of the parent collapsed.
     */
    get collapsed() {
        return false;
    }
    /**
     * Render the collapser with the virtual DOM.
     */
    render() {
        const childClass = COLLAPSER_CHILD_CLASS;
        return react_index_js_.createElement("div", { className: childClass, onClick: e => this.handleClick(e) });
    }
}
/**
 * A collapser subclass to collapse a cell's input area.
 */
class InputCollapser extends Collapser {
    /**
     * Construct a new input collapser.
     */
    constructor() {
        super();
        this.addClass(INPUT_COLLAPSER);
    }
    /**
     * Is the cell's input collapsed?
     */
    get collapsed() {
        var _a;
        const cell = (_a = this.parent) === null || _a === void 0 ? void 0 : _a.parent;
        if (cell) {
            return cell.inputHidden;
        }
        else {
            return false;
        }
    }
    /**
     * Handle a click event for the user to collapse the cell's input.
     */
    handleClick(e) {
        var _a;
        const cell = (_a = this.parent) === null || _a === void 0 ? void 0 : _a.parent;
        if (cell) {
            cell.inputHidden = !cell.inputHidden;
        }
        /* We need this until we watch the cell state */
        this.update();
    }
}
/**
 * A collapser subclass to collapse a cell's output area.
 */
class OutputCollapser extends Collapser {
    /**
     * Construct a new output collapser.
     */
    constructor() {
        super();
        this.addClass(OUTPUT_COLLAPSER);
    }
    /**
     * Is the cell's output collapsed?
     */
    get collapsed() {
        var _a;
        const cell = (_a = this.parent) === null || _a === void 0 ? void 0 : _a.parent;
        if (cell) {
            return cell.outputHidden;
        }
        else {
            return false;
        }
    }
    /**
     * Handle a click event for the user to collapse the cell's output.
     */
    handleClick(e) {
        var _a, _b;
        const cell = (_a = this.parent) === null || _a === void 0 ? void 0 : _a.parent;
        if (cell) {
            cell.outputHidden = !cell.outputHidden;
            /* Scroll cell into view after output collapse */
            if (cell.outputHidden) {
                let area = (_b = cell.parent) === null || _b === void 0 ? void 0 : _b.node;
                if (area) {
                    dist_index_es6_js_.ElementExt.scrollIntoViewIfNeeded(area, cell.node);
                }
            }
        }
        /* We need this until we watch the cell state */
        this.update();
    }
}

// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var widgets_dist_index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/cells/lib/headerfooter.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/

/**
 * The CSS class added to the cell header.
 */
const CELL_HEADER_CLASS = 'jp-CellHeader';
/**
 * The CSS class added to the cell footer.
 */
const CELL_FOOTER_CLASS = 'jp-CellFooter';
/**
 * Default implementation of a cell header.
 */
class CellHeader extends widgets_dist_index_es6_js_.Widget {
    /**
     * Construct a new cell header.
     */
    constructor() {
        super();
        this.addClass(CELL_HEADER_CLASS);
    }
}
/**
 * Default implementation of a cell footer.
 */
class CellFooter extends widgets_dist_index_es6_js_.Widget {
    /**
     * Construct a new cell footer.
     */
    constructor() {
        super();
        this.addClass(CELL_FOOTER_CLASS);
    }
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/codeeditor@~4.1.0-alpha.2 (singleton) (fallback: ../packages/codeeditor/lib/index.js)
var lib_index_js_ = __webpack_require__(40200);
;// CONCATENATED MODULE: ../packages/cells/lib/inputarea.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/



/**
 * The class name added to input area widgets.
 */
const INPUT_AREA_CLASS = 'jp-InputArea';
/**
 * The class name added to the prompt area of cell.
 */
const INPUT_AREA_PROMPT_CLASS = 'jp-InputArea-prompt';
/**
 * The class name added to OutputPrompt.
 */
const INPUT_PROMPT_CLASS = 'jp-InputPrompt';
/**
 * The class name added to the editor area of the cell.
 */
const INPUT_AREA_EDITOR_CLASS = 'jp-InputArea-editor';
/** ****************************************************************************
 * InputArea
 ******************************************************************************/
/**
 * An input area widget, which hosts a prompt and an editor widget.
 */
class InputArea extends widgets_dist_index_es6_js_.Widget {
    /**
     * Construct an input area widget.
     */
    constructor(options) {
        super();
        this.addClass(INPUT_AREA_CLASS);
        const { contentFactory, editorOptions, model } = options;
        this.model = model;
        this.contentFactory = contentFactory;
        // Prompt
        const prompt = (this._prompt = contentFactory.createInputPrompt());
        prompt.addClass(INPUT_AREA_PROMPT_CLASS);
        // Editor
        const editor = (this._editor = new lib_index_js_.CodeEditorWrapper({
            factory: contentFactory.editorFactory,
            model,
            editorOptions
        }));
        editor.addClass(INPUT_AREA_EDITOR_CLASS);
        const layout = (this.layout = new widgets_dist_index_es6_js_.PanelLayout());
        layout.addWidget(prompt);
        layout.addWidget(editor);
    }
    /**
     * Get the CodeEditorWrapper used by the cell.
     */
    get editorWidget() {
        return this._editor;
    }
    /**
     * Get the CodeEditor used by the cell.
     */
    get editor() {
        return this._editor.editor;
    }
    /**
     * Get the prompt node used by the cell.
     */
    get promptNode() {
        return this._prompt.node;
    }
    /**
     * Get the rendered input area widget, if any.
     */
    get renderedInput() {
        return this._rendered;
    }
    /**
     * Render an input instead of the text editor.
     */
    renderInput(widget) {
        const layout = this.layout;
        if (this._rendered) {
            this._rendered.parent = null;
        }
        this._editor.hide();
        this._rendered = widget;
        layout.addWidget(widget);
    }
    /**
     * Show the text editor.
     */
    showEditor() {
        if (this._rendered) {
            this._rendered.parent = null;
        }
        this._editor.show();
    }
    /**
     * Set the prompt of the input area.
     */
    setPrompt(value) {
        this._prompt.executionCount = value;
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        // Do nothing if already disposed.
        if (this.isDisposed) {
            return;
        }
        this._prompt = null;
        this._editor = null;
        this._rendered = null;
        super.dispose();
    }
}
/**
 * A namespace for `InputArea` statics.
 */
(function (InputArea) {
    /**
     * Default implementation of `IContentFactory`.
     *
     * This defaults to using an `editorFactory` based on CodeMirror.
     */
    class ContentFactory {
        /**
         * Construct a `ContentFactory`.
         */
        constructor(options) {
            this._editor = options.editorFactory;
        }
        /**
         * Return the `CodeEditor.Factory` being used.
         */
        get editorFactory() {
            return this._editor;
        }
        /**
         * Create an input prompt.
         */
        createInputPrompt() {
            return new InputPrompt();
        }
    }
    InputArea.ContentFactory = ContentFactory;
})(InputArea || (InputArea = {}));
/**
 * The default input prompt implementation.
 */
class InputPrompt extends widgets_dist_index_es6_js_.Widget {
    /*
     * Create an output prompt widget.
     */
    constructor() {
        super();
        this._executionCount = null;
        this.addClass(INPUT_PROMPT_CLASS);
    }
    /**
     * The execution count for the prompt.
     */
    get executionCount() {
        return this._executionCount;
    }
    set executionCount(value) {
        this._executionCount = value;
        if (value === null) {
            this.node.textContent = ' ';
        }
        else {
            this.node.textContent = `[${value || ' '}]:`;
        }
    }
}

// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var signaling_dist_index_es6_js_ = __webpack_require__(30205);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/attachments@~4.1.0-alpha.2 (strict) (fallback: ../packages/attachments/lib/index.js)
var attachments_lib_index_js_ = __webpack_require__(1909);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/outputarea@~4.1.0-alpha.2 (strict) (fallback: ../packages/outputarea/lib/index.js)
var outputarea_lib_index_js_ = __webpack_require__(65583);
// EXTERNAL MODULE: consume shared module (default) @jupyter/ydoc@~1.0.2 (singleton) (fallback: ../node_modules/@jupyter/ydoc/lib/index.js)
var ydoc_lib_index_js_ = __webpack_require__(69688);
;// CONCATENATED MODULE: ../packages/cells/lib/model.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/





const globalModelDBMutex = (0,ydoc_lib_index_js_.createMutex)();
function isCodeCellModel(model) {
    return model.type === 'code';
}
function isMarkdownCellModel(model) {
    return model.type === 'markdown';
}
function isRawCellModel(model) {
    return model.type === 'raw';
}
/**
 * An implementation of the cell model.
 */
class CellModel extends lib_index_js_.CodeEditor.Model {
    constructor(options = {}) {
        const { cell_type, sharedModel, ...others } = options;
        super({
            sharedModel: sharedModel !== null && sharedModel !== void 0 ? sharedModel : (0,ydoc_lib_index_js_.createStandaloneCell)({
                cell_type: cell_type !== null && cell_type !== void 0 ? cell_type : 'raw',
                id: options.id
            }),
            ...others
        });
        /**
         * A signal emitted when the state of the model changes.
         */
        this.contentChanged = new signaling_dist_index_es6_js_.Signal(this);
        /**
         * A signal emitted when a model state changes.
         */
        this.stateChanged = new signaling_dist_index_es6_js_.Signal(this);
        this._metadataChanged = new signaling_dist_index_es6_js_.Signal(this);
        this._trusted = false;
        this.standaloneModel = typeof options.sharedModel === 'undefined';
        this.trusted = !!this.getMetadata('trusted') || !!options.trusted;
        this.sharedModel.changed.connect(this.onGenericChange, this);
        this.sharedModel.metadataChanged.connect(this._onMetadataChanged, this);
    }
    /**
     * Signal emitted when cell metadata changes.
     */
    get metadataChanged() {
        return this._metadataChanged;
    }
    /**
     * The id for the cell.
     */
    get id() {
        return this.sharedModel.getId();
    }
    /**
     * The metadata associated with the cell.
     */
    get metadata() {
        return this.sharedModel.metadata;
    }
    /**
     * The trusted state of the model.
     */
    get trusted() {
        return this._trusted;
    }
    set trusted(newValue) {
        const oldValue = this.trusted;
        if (oldValue !== newValue) {
            this._trusted = newValue;
            this.onTrustedChanged(this, { newValue, oldValue });
        }
    }
    /**
     * Dispose of the resources held by the model.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.sharedModel.changed.disconnect(this.onGenericChange, this);
        this.sharedModel.metadataChanged.disconnect(this._onMetadataChanged, this);
        super.dispose();
    }
    /**
     * Handle a change to the trusted state.
     *
     * The default implementation is a no-op.
     */
    onTrustedChanged(trusted, args) {
        /* no-op */
    }
    /**
     * Delete a metadata
     *
     * @param key Metadata key
     */
    deleteMetadata(key) {
        return this.sharedModel.deleteMetadata(key);
    }
    /**
     * Get a metadata
     *
     * ### Notes
     * This returns a copy of the key value.
     *
     * @param key Metadata key
     */
    getMetadata(key) {
        return this.sharedModel.getMetadata(key);
    }
    /**
     * Set a metadata
     *
     * @param key Metadata key
     * @param value Metadata value
     */
    setMetadata(key, value) {
        if (typeof value === 'undefined') {
            this.sharedModel.deleteMetadata(key);
        }
        else {
            this.sharedModel.setMetadata(key, value);
        }
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        return this.sharedModel.toJSON();
    }
    /**
     * Handle a change to the observable value.
     */
    onGenericChange() {
        this.contentChanged.emit(void 0);
    }
    _onMetadataChanged(sender, change) {
        this._metadataChanged.emit(change);
    }
}
/**
 * A base implementation for cell models with attachments.
 */
class AttachmentsCellModel extends CellModel {
    /**
     * Construct a new cell with optional attachments.
     */
    constructor(options) {
        var _a;
        super(options);
        const factory = (_a = options.contentFactory) !== null && _a !== void 0 ? _a : AttachmentsCellModel.defaultContentFactory;
        const values = this.sharedModel.getAttachments();
        this._attachments = factory.createAttachmentsModel({ values });
        this._attachments.stateChanged.connect(this.onGenericChange, this);
        this._attachments.changed.connect(this._onAttachmentsChange, this);
        this.sharedModel.changed.connect(this._onSharedModelChanged, this);
    }
    /**
     * Get the attachments of the model.
     */
    get attachments() {
        return this._attachments;
    }
    /**
     * Dispose of the resources held by the model.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._attachments.stateChanged.disconnect(this.onGenericChange, this);
        this._attachments.changed.disconnect(this._onAttachmentsChange, this);
        this._attachments.dispose();
        this.sharedModel.changed.disconnect(this._onSharedModelChanged, this);
        super.dispose();
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        return super.toJSON();
    }
    /**
     * Handle a change to the cell outputs modelDB and reflect it in the shared model.
     */
    _onAttachmentsChange(sender, event) {
        const cell = this.sharedModel;
        globalModelDBMutex(() => cell.setAttachments(sender.toJSON()));
    }
    /**
     * Handle a change to the code cell value.
     */
    _onSharedModelChanged(slot, change) {
        if (change.attachmentsChange) {
            const cell = this.sharedModel;
            globalModelDBMutex(() => { var _a; return this._attachments.fromJSON((_a = cell.getAttachments()) !== null && _a !== void 0 ? _a : {}); });
        }
    }
}
/**
 * The namespace for `AttachmentsCellModel` statics.
 */
(function (AttachmentsCellModel) {
    /**
     * The default implementation of an `IContentFactory`.
     */
    class ContentFactory {
        /**
         * Create an attachments model.
         */
        createAttachmentsModel(options) {
            return new attachments_lib_index_js_.AttachmentsModel(options);
        }
    }
    AttachmentsCellModel.ContentFactory = ContentFactory;
    /**
     * The shared `ContentFactory` instance.
     */
    AttachmentsCellModel.defaultContentFactory = new ContentFactory();
})(AttachmentsCellModel || (AttachmentsCellModel = {}));
/**
 * An implementation of a raw cell model.
 */
class RawCellModel extends AttachmentsCellModel {
    /**
     * Construct a raw cell model from optional shared model.
     */
    constructor(options = {}) {
        super({
            cell_type: 'raw',
            ...options
        });
    }
    /**
     * The type of the cell.
     */
    get type() {
        return 'raw';
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        return super.toJSON();
    }
}
/**
 * An implementation of a markdown cell model.
 */
class MarkdownCellModel extends AttachmentsCellModel {
    /**
     * Construct a markdown cell model from optional shared model.
     */
    constructor(options = {}) {
        super({
            cell_type: 'markdown',
            ...options
        });
        // Use the Github-flavored markdown mode.
        this.mimeType = 'text/x-ipythongfm';
    }
    /**
     * The type of the cell.
     */
    get type() {
        return 'markdown';
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        return super.toJSON();
    }
}
/**
 * An implementation of a code cell Model.
 */
class CodeCellModel extends CellModel {
    /**
     * Construct a new code cell with optional original cell content.
     */
    constructor(options = {}) {
        var _a;
        super({
            cell_type: 'code',
            ...options
        });
        this._executedCode = '';
        this._isDirty = false;
        const factory = (_a = options === null || options === void 0 ? void 0 : options.contentFactory) !== null && _a !== void 0 ? _a : CodeCellModel.defaultContentFactory;
        const trusted = this.trusted;
        const outputs = this.sharedModel.getOutputs();
        this._outputs = factory.createOutputArea({ trusted, values: outputs });
        this.sharedModel.changed.connect(this._onSharedModelChanged, this);
        this._outputs.changed.connect(this.onGenericChange, this);
        this._outputs.changed.connect(this.onOutputsChange, this);
    }
    /**
     * The type of the cell.
     */
    get type() {
        return 'code';
    }
    /**
     * The execution count of the cell.
     */
    get executionCount() {
        return this.sharedModel.execution_count || null;
    }
    set executionCount(newValue) {
        this.sharedModel.execution_count = newValue || null;
    }
    /**
     * Whether the cell is dirty or not.
     *
     * A cell is dirty if it is output is not empty and does not
     * result of the input code execution.
     */
    get isDirty() {
        // Test could be done dynamically with this._executedCode
        // but for performance reason, the diff status is stored in a boolean.
        return this._isDirty;
    }
    /**
     * The cell outputs.
     */
    get outputs() {
        return this._outputs;
    }
    clearExecution() {
        this.outputs.clear();
        this.executionCount = null;
        this._setDirty(false);
        this.sharedModel.deleteMetadata('execution');
        // We trust this cell as it no longer has any outputs.
        this.trusted = true;
    }
    /**
     * Dispose of the resources held by the model.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.sharedModel.changed.disconnect(this._onSharedModelChanged, this);
        this._outputs.changed.disconnect(this.onGenericChange, this);
        this._outputs.changed.disconnect(this.onOutputsChange, this);
        this._outputs.dispose();
        this._outputs = null;
        super.dispose();
    }
    /**
     * Handle a change to the trusted state.
     */
    onTrustedChanged(trusted, args) {
        const newTrusted = args.newValue;
        if (this._outputs) {
            this._outputs.trusted = newTrusted;
        }
        if (newTrusted) {
            const codeCell = this.sharedModel;
            const metadata = codeCell.getMetadata();
            metadata.trusted = true;
            codeCell.setMetadata(metadata);
        }
        this.stateChanged.emit({
            name: 'trusted',
            oldValue: args.oldValue,
            newValue: newTrusted
        });
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        return super.toJSON();
    }
    /**
     * Handle a change to the cell outputs modelDB and reflect it in the shared model.
     */
    onOutputsChange(sender, event) {
        const codeCell = this.sharedModel;
        globalModelDBMutex(() => {
            switch (event.type) {
                case 'add': {
                    const outputs = event.newValues.map(output => output.toJSON());
                    codeCell.updateOutputs(event.newIndex, event.newIndex, outputs);
                    break;
                }
                case 'set': {
                    const newValues = event.newValues.map(output => output.toJSON());
                    codeCell.updateOutputs(event.oldIndex, event.oldIndex + newValues.length, newValues);
                    break;
                }
                case 'remove':
                    codeCell.updateOutputs(event.oldIndex, event.oldValues.length);
                    break;
                default:
                    throw new Error(`Invalid event type: ${event.type}`);
            }
        });
    }
    /**
     * Handle a change to the code cell value.
     */
    _onSharedModelChanged(slot, change) {
        if (change.outputsChange) {
            globalModelDBMutex(() => {
                this.outputs.clear();
                slot.getOutputs().forEach(output => this._outputs.add(output));
            });
        }
        if (change.executionCountChange) {
            if (change.executionCountChange.newValue &&
                (this.isDirty || !change.executionCountChange.oldValue)) {
                this._setDirty(false);
            }
            this.stateChanged.emit({
                name: 'executionCount',
                oldValue: change.executionCountChange.oldValue,
                newValue: change.executionCountChange.newValue
            });
        }
        if (change.sourceChange && this.executionCount !== null) {
            this._setDirty(this._executedCode !== this.sharedModel.getSource().trim());
        }
    }
    /**
     * Set whether the cell is dirty or not.
     */
    _setDirty(v) {
        if (!v) {
            this._executedCode = this.sharedModel.getSource().trim();
        }
        if (v !== this._isDirty) {
            this._isDirty = v;
            this.stateChanged.emit({
                name: 'isDirty',
                oldValue: !v,
                newValue: v
            });
        }
    }
}
/**
 * The namespace for `CodeCellModel` statics.
 */
(function (CodeCellModel) {
    /**
     * The default implementation of an `IContentFactory`.
     */
    class ContentFactory {
        /**
         * Create an output area.
         */
        createOutputArea(options) {
            return new outputarea_lib_index_js_.OutputAreaModel(options);
        }
    }
    CodeCellModel.ContentFactory = ContentFactory;
    /**
     * The shared `ContentFactory` instance.
     */
    CodeCellModel.defaultContentFactory = new ContentFactory();
})(CodeCellModel || (CodeCellModel = {}));

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
;// CONCATENATED MODULE: ../packages/cells/lib/placeholder.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/



/**
 * The CSS class added to placeholders.
 */
const PLACEHOLDER_CLASS = 'jp-Placeholder';
/**
 * The CSS classes added to input placeholder prompts.
 */
const placeholder_INPUT_PROMPT_CLASS = 'jp-Placeholder-prompt jp-InputPrompt';
/**
 * The CSS classes added to output placeholder prompts.
 */
const OUTPUT_PROMPT_CLASS = 'jp-Placeholder-prompt jp-OutputPrompt';
/**
 * The CSS class added to placeholder content.
 */
const CONTENT_CLASS = 'jp-Placeholder-content';
/**
 * The CSS class added to input placeholders.
 */
const INPUT_PLACEHOLDER_CLASS = 'jp-InputPlaceholder';
/**
 * The CSS class added to output placeholders.
 */
const OUTPUT_PLACEHOLDER_CLASS = 'jp-OutputPlaceholder';
/**
 * An base class for placeholders
 *
 * ### Notes
 * A placeholder is the element that is shown when input/output
 * is hidden.
 */
class Placeholder extends widgets_dist_index_es6_js_.Widget {
    /**
     * Construct a new placeholder.
     */
    constructor(options) {
        var _a, _b, _c;
        const node = document.createElement('div');
        super({ node });
        const trans = ((_a = options.translator) !== null && _a !== void 0 ? _a : translation_lib_index_js_.nullTranslator).load('jupyterlab');
        const innerNode = document.createElement('div');
        innerNode.className = (_b = options.promptClass) !== null && _b !== void 0 ? _b : '';
        node.insertAdjacentHTML('afterbegin', innerNode.outerHTML);
        this._cell = document.createElement('div');
        this._cell.classList.add(CONTENT_CLASS);
        this._cell.title = trans.__('Click to expand');
        const container = this._cell.appendChild(document.createElement('div'));
        container.classList.add('jp-Placeholder-contentContainer');
        this._textContent = container.appendChild(document.createElement('span'));
        this._textContent.className = 'jp-PlaceholderText';
        this._textContent.innerText = (_c = options.text) !== null && _c !== void 0 ? _c : '';
        node.appendChild(this._cell);
        index_js_.ellipsesIcon.element({
            container: container.appendChild(document.createElement('span')),
            className: 'jp-MoreHorizIcon',
            elementPosition: 'center',
            height: 'auto',
            width: '32px'
        });
        this.addClass(PLACEHOLDER_CLASS);
        this._callback = options.callback;
    }
    /**
     * The text displayed in the placeholder.
     */
    set text(t) {
        this._textContent.innerText = t;
    }
    get text() {
        return this._textContent.innerText;
    }
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        this.node.addEventListener('click', this._callback);
    }
    onBeforeDetach(msg) {
        this.node.removeEventListener('click', this._callback);
        super.onBeforeDetach(msg);
    }
}
/**
 * The input placeholder class.
 */
class InputPlaceholder extends Placeholder {
    /**
     * Construct a new input placeholder.
     */
    constructor(options) {
        super({ ...options, promptClass: placeholder_INPUT_PROMPT_CLASS });
        this.addClass(INPUT_PLACEHOLDER_CLASS);
    }
}
/**
 * The output placeholder class.
 */
class OutputPlaceholder extends Placeholder {
    /**
     * Construct a new output placeholder.
     */
    constructor(options) {
        super({ ...options, promptClass: OUTPUT_PROMPT_CLASS });
        this.addClass(OUTPUT_PLACEHOLDER_CLASS);
    }
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/codemirror@~4.1.0-alpha.2 (singleton) (fallback: ../packages/codemirror/lib/index.js)
var codemirror_lib_index_js_ = __webpack_require__(29239);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var coreutils_lib_index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/documentsearch@~4.1.0-alpha.2 (singleton) (fallback: ../packages/documentsearch/lib/index.js)
var documentsearch_lib_index_js_ = __webpack_require__(80599);
;// CONCATENATED MODULE: ../packages/cells/lib/searchprovider.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * Class applied on highlighted search matches
 */
const SELECTED_HIGHLIGHT_CLASS = 'jp-mod-selected';
/**
 * Search provider for cells.
 */
class CellSearchProvider extends codemirror_lib_index_js_.EditorSearchProvider {
    constructor(cell) {
        super();
        this.cell = cell;
        if (!this.cell.inViewport && !this.cell.editor) {
            void (0,coreutils_lib_index_js_.signalToPromise)(cell.inViewportChanged).then(([, inViewport]) => {
                if (inViewport) {
                    this.cmHandler.setEditor(this.editor);
                }
            });
        }
    }
    /**
     * Text editor
     */
    get editor() {
        return this.cell.editor;
    }
    /**
     * Editor content model
     */
    get model() {
        return this.cell.model;
    }
}
/**
 * Code cell search provider
 */
class CodeCellSearchProvider extends CellSearchProvider {
    /**
     * Constructor
     *
     * @param cell Cell widget
     */
    constructor(cell) {
        super(cell);
        this.currentProviderIndex = -1;
        this.outputsProvider = [];
        const outputs = this.cell.outputArea;
        this._onOutputsChanged(outputs, outputs.widgets.length).catch(reason => {
            console.error(`Failed to initialize search on cell outputs.`, reason);
        });
        outputs.outputLengthChanged.connect(this._onOutputsChanged, this);
        outputs.disposed.connect(() => {
            outputs.outputLengthChanged.disconnect(this._onOutputsChanged);
        }, this);
    }
    /**
     * Number of matches in the cell.
     */
    get matchesCount() {
        if (!this.isActive) {
            return 0;
        }
        return (super.matchesCount +
            this.outputsProvider.reduce((sum, provider) => { var _a; return sum + ((_a = provider.matchesCount) !== null && _a !== void 0 ? _a : 0); }, 0));
    }
    /**
     * Clear currently highlighted match.
     */
    async clearHighlight() {
        await super.clearHighlight();
        await Promise.all(this.outputsProvider.map(provider => provider.clearHighlight()));
    }
    /**
     * Dispose the search provider
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        super.dispose();
        this.outputsProvider.map(provider => {
            provider.dispose();
        });
        this.outputsProvider.length = 0;
    }
    /**
     * Highlight the next match.
     *
     * @returns The next match if there is one.
     */
    async highlightNext(loop, options) {
        if (this.matchesCount === 0 || !this.isActive) {
            this.currentIndex = null;
        }
        else {
            if (this.currentProviderIndex === -1) {
                const match = await super.highlightNext(true, options);
                if (match) {
                    this.currentIndex = this.cmHandler.currentIndex;
                    return match;
                }
                else {
                    this.currentProviderIndex = 0;
                }
            }
            while (this.currentProviderIndex < this.outputsProvider.length) {
                const provider = this.outputsProvider[this.currentProviderIndex];
                const match = await provider.highlightNext(false);
                if (match) {
                    this.currentIndex =
                        super.matchesCount +
                            this.outputsProvider
                                .slice(0, this.currentProviderIndex)
                                .reduce((sum, provider) => { var _a; return (sum += (_a = provider.matchesCount) !== null && _a !== void 0 ? _a : 0); }, 0) +
                            provider.currentMatchIndex;
                    return match;
                }
                else {
                    this.currentProviderIndex += 1;
                }
            }
            this.currentProviderIndex = -1;
            this.currentIndex = null;
            return undefined;
        }
    }
    /**
     * Highlight the previous match.
     *
     * @returns The previous match if there is one.
     */
    async highlightPrevious() {
        if (this.matchesCount === 0 || !this.isActive) {
            this.currentIndex = null;
        }
        else {
            if (this.currentIndex === null) {
                this.currentProviderIndex = this.outputsProvider.length - 1;
            }
            while (this.currentProviderIndex >= 0) {
                const provider = this.outputsProvider[this.currentProviderIndex];
                const match = await provider.highlightPrevious(false);
                if (match) {
                    this.currentIndex =
                        super.matchesCount +
                            this.outputsProvider
                                .slice(0, this.currentProviderIndex)
                                .reduce((sum, provider) => { var _a; return (sum += (_a = provider.matchesCount) !== null && _a !== void 0 ? _a : 0); }, 0) +
                            provider.currentMatchIndex;
                    return match;
                }
                else {
                    this.currentProviderIndex -= 1;
                }
            }
            const match = await super.highlightPrevious();
            if (match) {
                this.currentIndex = this.cmHandler.currentIndex;
                return match;
            }
            else {
                this.currentIndex = null;
                return undefined;
            }
        }
    }
    /**
     * Initialize the search using the provided options. Should update the UI to highlight
     * all matches and "select" the first match.
     *
     * @param query A RegExp to be use to perform the search
     * @param filters Filter parameters to pass to provider
     */
    async startQuery(query, filters) {
        await super.startQuery(query, filters);
        // Search outputs
        if ((filters === null || filters === void 0 ? void 0 : filters.output) !== false && this.isActive) {
            await Promise.all(this.outputsProvider.map(provider => provider.startQuery(query)));
        }
    }
    async endQuery() {
        var _a;
        await super.endQuery();
        if (((_a = this.filters) === null || _a === void 0 ? void 0 : _a.output) !== false && this.isActive) {
            await Promise.all(this.outputsProvider.map(provider => provider.endQuery()));
        }
    }
    async _onOutputsChanged(outputArea, changes) {
        var _a;
        this.outputsProvider.forEach(provider => {
            provider.dispose();
        });
        this.outputsProvider.length = 0;
        this.currentProviderIndex = -1;
        this.outputsProvider = this.cell.outputArea.widgets.map(output => new documentsearch_lib_index_js_.GenericSearchProvider(output));
        if (this.isActive && this.query && ((_a = this.filters) === null || _a === void 0 ? void 0 : _a.output) !== false) {
            await Promise.all([
                this.outputsProvider.map(provider => {
                    void provider.startQuery(this.query);
                })
            ]);
        }
        this._stateChanged.emit();
    }
}
/**
 * Markdown cell search provider
 */
class MarkdownCellSearchProvider extends CellSearchProvider {
    /**
     * Constructor
     *
     * @param cell Cell widget
     */
    constructor(cell) {
        super(cell);
        this._unrenderedByHighligh = false;
        this.renderedProvider = new documentsearch_lib_index_js_.GenericSearchProvider(cell.renderer);
    }
    /**
     * Clear currently highlighted match
     */
    async clearHighlight() {
        await super.clearHighlight();
        await this.renderedProvider.clearHighlight();
    }
    /**
     * Dispose the search provider
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        super.dispose();
        this.renderedProvider.dispose();
    }
    /**
     * Stop the search and clean any UI elements.
     */
    async endQuery() {
        await super.endQuery();
        await this.renderedProvider.endQuery();
    }
    /**
     * Highlight the next match.
     *
     * @returns The next match if there is one.
     */
    async highlightNext() {
        let match = undefined;
        if (!this.isActive) {
            return match;
        }
        const cell = this.cell;
        if (cell.rendered && this.matchesCount > 0) {
            // Unrender the cell
            this._unrenderedByHighligh = true;
            const waitForRendered = (0,coreutils_lib_index_js_.signalToPromise)(cell.renderedChanged);
            cell.rendered = false;
            await waitForRendered;
        }
        match = await super.highlightNext();
        return match;
    }
    /**
     * Highlight the previous match.
     *
     * @returns The previous match if there is one.
     */
    async highlightPrevious() {
        let match = undefined;
        const cell = this.cell;
        if (cell.rendered && this.matchesCount > 0) {
            // Unrender the cell if there are matches within the cell
            this._unrenderedByHighligh = true;
            const waitForRendered = (0,coreutils_lib_index_js_.signalToPromise)(cell.renderedChanged);
            cell.rendered = false;
            await waitForRendered;
        }
        match = await super.highlightPrevious();
        return match;
    }
    /**
     * Initialize the search using the provided options. Should update the UI
     * to highlight all matches and "select" the first match.
     *
     * @param query A RegExp to be use to perform the search
     * @param filters Filter parameters to pass to provider
     */
    async startQuery(query, filters) {
        await super.startQuery(query, filters);
        const cell = this.cell;
        if (cell.rendered) {
            this.onRenderedChanged(cell, cell.rendered);
        }
        cell.renderedChanged.connect(this.onRenderedChanged, this);
    }
    /**
     * Replace all matches in the cell source with the provided text
     *
     * @param newText The replacement text.
     * @returns Whether a replace occurred.
     */
    async replaceAllMatches(newText) {
        const result = await super.replaceAllMatches(newText);
        // if the cell is rendered force update
        if (this.cell.rendered) {
            this.cell.update();
        }
        return result;
    }
    /**
     * Callback on rendered state change
     *
     * @param cell Cell that emitted the change
     * @param rendered New rendered value
     */
    onRenderedChanged(cell, rendered) {
        var _a;
        if (!this._unrenderedByHighligh) {
            this.currentIndex = null;
        }
        this._unrenderedByHighligh = false;
        if (this.isActive) {
            if (rendered) {
                void this.renderedProvider.startQuery(this.query);
            }
            else {
                // Force cursor position to ensure reverse search is working as expected
                (_a = cell.editor) === null || _a === void 0 ? void 0 : _a.setCursorPosition({ column: 0, line: 0 });
                void this.renderedProvider.endQuery();
            }
        }
    }
}
/**
 * Factory to create a cell search provider
 *
 * @param cell Cell widget
 * @returns Cell search provider
 */
function createCellSearchProvider(cell) {
    if (cell.isPlaceholder()) {
        return new CellSearchProvider(cell);
    }
    switch (cell.model.type) {
        case 'code':
            return new CodeCellSearchProvider(cell);
        case 'markdown':
            return new MarkdownCellSearchProvider(cell);
        default:
            return new CellSearchProvider(cell);
    }
}

// EXTERNAL MODULE: consume shared module (default) @codemirror/view@^6.9.6 (singleton) (fallback: ../node_modules/@codemirror/view/dist/index.js)
var dist_index_js_ = __webpack_require__(87801);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var apputils_lib_index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/rendermime@~4.1.0-alpha.2 (singleton) (fallback: ../packages/rendermime/lib/index.js)
var rendermime_lib_index_js_ = __webpack_require__(66866);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/toc@~6.1.0-alpha.2 (singleton) (fallback: ../packages/toc/lib/index.js)
var toc_lib_index_js_ = __webpack_require__(95691);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var coreutils_dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var algorithm_dist_index_es6_js_ = __webpack_require__(16415);
// EXTERNAL MODULE: consume shared module (default) @lumino/messaging@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/messaging/dist/index.es6.js)
var messaging_dist_index_es6_js_ = __webpack_require__(85755);
// EXTERNAL MODULE: consume shared module (default) @lumino/polling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/polling/dist/index.es6.js)
var polling_dist_index_es6_js_ = __webpack_require__(81967);
;// CONCATENATED MODULE: ../packages/cells/lib/resizeHandle.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */


const RESIZE_HANDLE_CLASS = 'jp-CellResizeHandle';
const CELL_RESIZED_CLASS = 'jp-mod-resizedCell';
/**
 * A handle that allows to change input/output proportions in side-by-side mode.
 */
class ResizeHandle extends widgets_dist_index_es6_js_.Widget {
    constructor(targetNode) {
        super();
        this.targetNode = targetNode;
        this._isActive = false;
        this._isDragging = false;
        this.addClass(RESIZE_HANDLE_CLASS);
        this._resizer = new polling_dist_index_es6_js_.Throttler(event => this._resize(event), 50);
    }
    /**
     * Dispose the resizer handle.
     */
    dispose() {
        this._resizer.dispose();
        super.dispose();
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     */
    handleEvent(event) {
        var _a, _b;
        switch (event.type) {
            case 'dblclick':
                (_a = this.targetNode.parentNode) === null || _a === void 0 ? void 0 : _a.childNodes.forEach(node => {
                    node.classList.remove(CELL_RESIZED_CLASS);
                });
                document.documentElement.style.setProperty('--jp-side-by-side-output-size', `1fr`);
                this._isActive = false;
                break;
            case 'mousedown':
                this._isDragging = true;
                if (!this._isActive) {
                    (_b = this.targetNode.parentNode) === null || _b === void 0 ? void 0 : _b.childNodes.forEach(node => {
                        node.classList.add(CELL_RESIZED_CLASS);
                    });
                    this._isActive = true;
                }
                window.addEventListener('mousemove', this);
                window.addEventListener('mouseup', this);
                break;
            case 'mousemove': {
                if (this._isActive && this._isDragging) {
                    void this._resizer.invoke(event);
                }
                break;
            }
            case 'mouseup':
                this._isDragging = false;
                window.removeEventListener('mousemove', this);
                window.removeEventListener('mouseup', this);
                break;
            default:
                break;
        }
    }
    /**
     * Handle `after-attach` messages.
     */
    onAfterAttach(msg) {
        this.node.addEventListener('dblclick', this);
        this.node.addEventListener('mousedown', this);
        super.onAfterAttach(msg);
    }
    /**
     * Handle `before-detach` messages.
     */
    onBeforeDetach(msg) {
        this.node.removeEventListener('dblclick', this);
        this.node.removeEventListener('mousedown', this);
        super.onBeforeDetach(msg);
    }
    _resize(event) {
        // Gate the output size ratio between {0.05, 50} as sensible defaults.
        const { width, x } = this.targetNode.getBoundingClientRect();
        const position = event.clientX - x;
        const ratio = width / position - 1;
        if (0 < ratio) {
            const normalized = Math.max(Math.min(Math.abs(ratio), 50), 0.05);
            document.documentElement.style.setProperty('--jp-side-by-side-output-size', `${normalized}fr`);
        }
    }
}

;// CONCATENATED MODULE: ../packages/cells/lib/widget.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/




















/**
 * The CSS class added to cell widgets.
 */
const CELL_CLASS = 'jp-Cell';
/**
 * The CSS class added to the cell header.
 */
const widget_CELL_HEADER_CLASS = 'jp-Cell-header';
/**
 * The CSS class added to the cell footer.
 */
const widget_CELL_FOOTER_CLASS = 'jp-Cell-footer';
/**
 * The CSS class added to the cell input wrapper.
 */
const CELL_INPUT_WRAPPER_CLASS = 'jp-Cell-inputWrapper';
/**
 * The CSS class added to the cell output wrapper.
 */
const CELL_OUTPUT_WRAPPER_CLASS = 'jp-Cell-outputWrapper';
/**
 * The CSS class added to the cell input area.
 */
const CELL_INPUT_AREA_CLASS = 'jp-Cell-inputArea';
/**
 * The CSS class added to the cell output area.
 */
const CELL_OUTPUT_AREA_CLASS = 'jp-Cell-outputArea';
/**
 * The CSS class added to the cell input collapser.
 */
const CELL_INPUT_COLLAPSER_CLASS = 'jp-Cell-inputCollapser';
/**
 * The CSS class added to the cell output collapser.
 */
const CELL_OUTPUT_COLLAPSER_CLASS = 'jp-Cell-outputCollapser';
/**
 * The class name added to the cell when dirty.
 */
const DIRTY_CLASS = 'jp-mod-dirty';
/**
 * The class name added to code cells.
 */
const CODE_CELL_CLASS = 'jp-CodeCell';
/**
 * The class name added to markdown cells.
 */
const MARKDOWN_CELL_CLASS = 'jp-MarkdownCell';
/**
 * The class name added to rendered markdown output widgets.
 */
const MARKDOWN_OUTPUT_CLASS = 'jp-MarkdownOutput';
const MARKDOWN_HEADING_COLLAPSED = 'jp-MarkdownHeadingCollapsed';
const HEADING_COLLAPSER_CLASS = 'jp-collapseHeadingButton';
const SHOW_HIDDEN_CELLS_CLASS = 'jp-showHiddenCellsButton';
/**
 * The class name added to raw cells.
 */
const RAW_CELL_CLASS = 'jp-RawCell';
/**
 * The class name added to a rendered input area.
 */
const RENDERED_CLASS = 'jp-mod-rendered';
const NO_OUTPUTS_CLASS = 'jp-mod-noOutputs';
/**
 * The text applied to an empty markdown cell.
 */
const DEFAULT_MARKDOWN_TEXT = 'Type Markdown and LaTeX: $ α^2 $';
/**
 * The timeout to wait for change activity to have ceased before rendering.
 */
const RENDER_TIMEOUT = 1000;
/**
 * The mime type for a rich contents drag object.
 */
const CONTENTS_MIME_RICH = 'application/x-jupyter-icontentsrich';
/** ****************************************************************************
 * Cell
 ******************************************************************************/
/**
 * A base cell widget.
 */
class Cell extends widgets_dist_index_es6_js_.Widget {
    /**
     * Construct a new base cell widget.
     */
    constructor(options) {
        var _a, _b, _c, _d;
        super();
        this.prompt = '';
        this._displayChanged = new signaling_dist_index_es6_js_.Signal(this);
        this._editorConfig = {};
        this._inputHidden = false;
        this._inViewportChanged = new signaling_dist_index_es6_js_.Signal(this);
        this._readOnly = false;
        this._ready = new coreutils_dist_index_js_.PromiseDelegate();
        this._resizeDebouncer = new polling_dist_index_es6_js_.Debouncer(() => {
            this._displayChanged.emit();
        }, 0);
        this._syncCollapse = false;
        this._syncEditable = false;
        this.addClass(CELL_CLASS);
        const model = (this._model = options.model);
        this.contentFactory = options.contentFactory;
        this.layout = (_a = options.layout) !== null && _a !== void 0 ? _a : new widgets_dist_index_es6_js_.PanelLayout();
        // Set up translator for aria labels
        this.translator = (_b = options.translator) !== null && _b !== void 0 ? _b : translation_lib_index_js_.nullTranslator;
        this._editorConfig = (_c = options.editorConfig) !== null && _c !== void 0 ? _c : {};
        this._placeholder = true;
        this._inViewport = false;
        this.placeholder = (_d = options.placeholder) !== null && _d !== void 0 ? _d : true;
        model.metadataChanged.connect(this.onMetadataChanged, this);
    }
    /**
     * Initialize view state from model.
     *
     * #### Notes
     * Should be called after construction. For convenience, returns this, so it
     * can be chained in the construction, like `new Foo().initializeState();`
     */
    initializeState() {
        this.loadCollapseState();
        this.loadEditableState();
        return this;
    }
    /**
     * Signal to indicate that widget has changed visibly (in size, in type, etc)
     */
    get displayChanged() {
        return this._displayChanged;
    }
    /**
     * Whether the cell is in viewport or not.
     */
    get inViewport() {
        return this._inViewport;
    }
    set inViewport(v) {
        if (this._inViewport !== v) {
            this._inViewport = v;
            this._inViewportChanged.emit(this._inViewport);
        }
    }
    /**
     * Will emit true just after the node is attached to the DOM
     * Will emit false just before the node is detached of the DOM
     */
    get inViewportChanged() {
        return this._inViewportChanged;
    }
    /**
     * Whether the cell is a placeholder not yet fully rendered or not.
     */
    get placeholder() {
        return this._placeholder;
    }
    set placeholder(v) {
        if (this._placeholder !== v && v === false) {
            this.initializeDOM();
            this._placeholder = v;
            this._ready.resolve();
        }
    }
    /**
     * Get the prompt node used by the cell.
     */
    get promptNode() {
        if (this.placeholder) {
            return null;
        }
        if (!this._inputHidden) {
            return this._input.promptNode;
        }
        else {
            return this._inputPlaceholder.node
                .firstElementChild;
        }
    }
    /**
     * Get the CodeEditorWrapper used by the cell.
     */
    get editorWidget() {
        var _a, _b;
        return (_b = (_a = this._input) === null || _a === void 0 ? void 0 : _a.editorWidget) !== null && _b !== void 0 ? _b : null;
    }
    /**
     * Get the CodeEditor used by the cell.
     */
    get editor() {
        var _a, _b;
        return (_b = (_a = this._input) === null || _a === void 0 ? void 0 : _a.editor) !== null && _b !== void 0 ? _b : null;
    }
    /**
     * Editor configuration
     */
    get editorConfig() {
        return this._editorConfig;
    }
    /**
     * Cell headings
     */
    get headings() {
        return new Array();
    }
    /**
     * Get the model used by the cell.
     */
    get model() {
        return this._model;
    }
    /**
     * Get the input area for the cell.
     */
    get inputArea() {
        return this._input;
    }
    /**
     * The read only state of the cell.
     */
    get readOnly() {
        return this._readOnly;
    }
    set readOnly(value) {
        if (value === this._readOnly) {
            return;
        }
        this._readOnly = value;
        if (this.syncEditable) {
            this.saveEditableState();
        }
        this.update();
    }
    /**
     * Whether the cell is a placeholder that defer rendering
     *
     * #### Notes
     * You can wait for the promise `Cell.ready` to wait for the
     * cell to be rendered.
     */
    isPlaceholder() {
        return this.placeholder;
    }
    /**
     * Save view editable state to model
     */
    saveEditableState() {
        const { sharedModel } = this.model;
        const current = sharedModel.getMetadata('editable');
        if ((this.readOnly && current === false) ||
            (!this.readOnly && current === undefined)) {
            return;
        }
        if (this.readOnly) {
            sharedModel.setMetadata('editable', false);
        }
        else {
            sharedModel.deleteMetadata('editable');
        }
    }
    /**
     * Load view editable state from model.
     */
    loadEditableState() {
        this.readOnly =
            this.model.sharedModel.getMetadata('editable') ===
                false;
    }
    /**
     * A promise that resolves when the widget renders for the first time.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * Set the prompt for the widget.
     */
    setPrompt(value) {
        var _a;
        this.prompt = value;
        (_a = this._input) === null || _a === void 0 ? void 0 : _a.setPrompt(value);
    }
    /**
     * The view state of input being hidden.
     */
    get inputHidden() {
        return this._inputHidden;
    }
    set inputHidden(value) {
        var _a;
        if (this._inputHidden === value) {
            return;
        }
        if (!this.placeholder) {
            const layout = this._inputWrapper.layout;
            if (value) {
                this._input.parent = null;
                if (this._inputPlaceholder) {
                    this._inputPlaceholder.text = (_a = this.model.sharedModel
                        .getSource()
                        .split('\n')) === null || _a === void 0 ? void 0 : _a[0];
                }
                layout.addWidget(this._inputPlaceholder);
            }
            else {
                this._inputPlaceholder.parent = null;
                layout.addWidget(this._input);
            }
        }
        this._inputHidden = value;
        if (this.syncCollapse) {
            this.saveCollapseState();
        }
        this.handleInputHidden(value);
    }
    /**
     * Save view collapse state to model
     */
    saveCollapseState() {
        const jupyter = { ...this.model.getMetadata('jupyter') };
        if ((this.inputHidden && jupyter.source_hidden === true) ||
            (!this.inputHidden && jupyter.source_hidden === undefined)) {
            return;
        }
        if (this.inputHidden) {
            jupyter.source_hidden = true;
        }
        else {
            delete jupyter.source_hidden;
        }
        if (Object.keys(jupyter).length === 0) {
            this.model.deleteMetadata('jupyter');
        }
        else {
            this.model.setMetadata('jupyter', jupyter);
        }
    }
    /**
     * Revert view collapse state from model.
     */
    loadCollapseState() {
        var _a;
        const jupyter = (_a = this.model.getMetadata('jupyter')) !== null && _a !== void 0 ? _a : {};
        this.inputHidden = !!jupyter.source_hidden;
    }
    /**
     * Handle the input being hidden.
     *
     * #### Notes
     * This is called by the `inputHidden` setter so that subclasses
     * can perform actions upon the input being hidden without accessing
     * private state.
     */
    handleInputHidden(value) {
        return;
    }
    /**
     * Whether to sync the collapse state to the cell model.
     */
    get syncCollapse() {
        return this._syncCollapse;
    }
    set syncCollapse(value) {
        if (this._syncCollapse === value) {
            return;
        }
        this._syncCollapse = value;
        if (value) {
            this.loadCollapseState();
        }
    }
    /**
     * Whether to sync the editable state to the cell model.
     */
    get syncEditable() {
        return this._syncEditable;
    }
    set syncEditable(value) {
        if (this._syncEditable === value) {
            return;
        }
        this._syncEditable = value;
        if (value) {
            this.loadEditableState();
        }
    }
    /**
     * Clone the cell, using the same model.
     */
    clone() {
        const constructor = this.constructor;
        return new constructor({
            model: this.model,
            contentFactory: this.contentFactory,
            placeholder: false,
            translator: this.translator
        });
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        // Do nothing if already disposed.
        if (this.isDisposed) {
            return;
        }
        this._resizeDebouncer.dispose();
        this._input = null;
        this._model = null;
        this._inputWrapper = null;
        this._inputPlaceholder = null;
        super.dispose();
    }
    /**
     * Update the editor configuration with the partial provided dictionary.
     *
     * @param v Partial editor configuration
     */
    updateEditorConfig(v) {
        this._editorConfig = { ...this._editorConfig, ...v };
        if (this.editor) {
            this.editor.setOptions(this._editorConfig);
        }
    }
    /**
     * Create children widgets.
     */
    initializeDOM() {
        if (!this.placeholder) {
            return;
        }
        const contentFactory = this.contentFactory;
        const model = this._model;
        // Header
        const header = contentFactory.createCellHeader();
        header.addClass(widget_CELL_HEADER_CLASS);
        this.layout.addWidget(header);
        // Input
        const inputWrapper = (this._inputWrapper = new widgets_dist_index_es6_js_.Panel());
        inputWrapper.addClass(CELL_INPUT_WRAPPER_CLASS);
        const inputCollapser = new InputCollapser();
        inputCollapser.addClass(CELL_INPUT_COLLAPSER_CLASS);
        const input = (this._input = new InputArea({
            model,
            contentFactory,
            editorOptions: this.getEditorOptions()
        }));
        input.addClass(CELL_INPUT_AREA_CLASS);
        inputWrapper.addWidget(inputCollapser);
        inputWrapper.addWidget(input);
        this.layout.addWidget(inputWrapper);
        this._inputPlaceholder = new InputPlaceholder({
            callback: () => {
                this.inputHidden = !this.inputHidden;
            },
            text: input.model.sharedModel.getSource().split('\n')[0],
            translator: this.translator
        });
        input.model.contentChanged.connect((sender, args) => {
            var _a;
            if (this._inputPlaceholder && this.inputHidden) {
                this._inputPlaceholder.text = (_a = sender.sharedModel
                    .getSource()
                    .split('\n')) === null || _a === void 0 ? void 0 : _a[0];
            }
        });
        if (this.inputHidden) {
            input.parent = null;
            inputWrapper.layout.addWidget(this._inputPlaceholder);
        }
        // Footer
        const footer = this.contentFactory.createCellFooter();
        footer.addClass(widget_CELL_FOOTER_CLASS);
        this.layout.addWidget(footer);
    }
    /**
     * Get the editor options at initialization.
     *
     * @returns Editor options
     */
    getEditorOptions() {
        return { config: this.editorConfig };
    }
    /**
     * Handle `before-attach` messages.
     */
    onBeforeAttach(msg) {
        if (this.placeholder) {
            this.placeholder = false;
        }
    }
    /**
     * Handle `after-attach` messages.
     */
    onAfterAttach(msg) {
        this.update();
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        var _a;
        (_a = this.editor) === null || _a === void 0 ? void 0 : _a.focus();
    }
    /**
     * Handle `resize` messages.
     */
    onResize(msg) {
        void this._resizeDebouncer.invoke();
    }
    /**
     * Handle `update-request` messages.
     */
    onUpdateRequest(msg) {
        var _a, _b;
        if (!this._model) {
            return;
        }
        // Handle read only state.
        if (((_a = this.editor) === null || _a === void 0 ? void 0 : _a.getOption('readOnly')) !== this._readOnly) {
            (_b = this.editor) === null || _b === void 0 ? void 0 : _b.setOption('readOnly', this._readOnly);
        }
    }
    onContentChanged() {
        var _a;
        if (this.inputHidden && this._inputPlaceholder) {
            this._inputPlaceholder.text = (_a = this.model.sharedModel
                .getSource()
                .split('\n')) === null || _a === void 0 ? void 0 : _a[0];
        }
    }
    /**
     * Handle changes in the metadata.
     */
    onMetadataChanged(model, args) {
        switch (args.key) {
            case 'jupyter':
                if (this.syncCollapse) {
                    this.loadCollapseState();
                }
                break;
            case 'editable':
                if (this.syncEditable) {
                    this.loadEditableState();
                }
                break;
            default:
                break;
        }
    }
}
/**
 * The namespace for the `Cell` class statics.
 */
(function (Cell) {
    /**
     * Type of headings
     */
    let HeadingType;
    (function (HeadingType) {
        /**
         * Heading from HTML output
         */
        HeadingType[HeadingType["HTML"] = 0] = "HTML";
        /**
         * Heading from Markdown cell or Markdown output
         */
        HeadingType[HeadingType["Markdown"] = 1] = "Markdown";
    })(HeadingType = Cell.HeadingType || (Cell.HeadingType = {}));
    /**
     * The default implementation of an `IContentFactory`.
     *
     * This includes a CodeMirror editor factory to make it easy to use out of the box.
     */
    class ContentFactory {
        /**
         * Create a content factory for a cell.
         */
        constructor(options) {
            this._editorFactory = options.editorFactory;
        }
        /**
         * The readonly editor factory that create code editors
         */
        get editorFactory() {
            return this._editorFactory;
        }
        /**
         * Create a new cell header for the parent widget.
         */
        createCellHeader() {
            return new CellHeader();
        }
        /**
         * Create a new cell footer for the parent widget.
         */
        createCellFooter() {
            return new CellFooter();
        }
        /**
         * Create an input prompt.
         */
        createInputPrompt() {
            return new InputPrompt();
        }
        /**
         * Create the output prompt for the widget.
         */
        createOutputPrompt() {
            return new outputarea_lib_index_js_.OutputPrompt();
        }
        /**
         * Create an stdin widget.
         */
        createStdin(options) {
            return new outputarea_lib_index_js_.Stdin(options);
        }
    }
    Cell.ContentFactory = ContentFactory;
})(Cell || (Cell = {}));
/** ****************************************************************************
 * CodeCell
 ******************************************************************************/
/**
 * Code cell layout
 *
 * It will not detached the output area when the cell is detached.
 */
class CodeCellLayout extends widgets_dist_index_es6_js_.PanelLayout {
    /**
     * A message handler invoked on a `'before-attach'` message.
     *
     * #### Notes
     * The default implementation of this method forwards the message
     * to all widgets. It assumes all widget nodes are attached to the
     * parent widget node.
     *
     * This may be reimplemented by subclasses as needed.
     */
    onBeforeAttach(msg) {
        let beforeOutputArea = true;
        const outputAreaWrapper = this.parent.node.firstElementChild;
        for (const widget of this) {
            if (outputAreaWrapper) {
                if (widget.node === outputAreaWrapper) {
                    beforeOutputArea = false;
                }
                else {
                    messaging_dist_index_es6_js_.MessageLoop.sendMessage(widget, msg);
                    if (beforeOutputArea) {
                        this.parent.node.insertBefore(widget.node, outputAreaWrapper);
                    }
                    else {
                        this.parent.node.appendChild(widget.node);
                    }
                    // Force setting isVisible to true as it requires the parent widget to be
                    // visible. But that flag will be set only during the `onAfterAttach` call.
                    if (!this.parent.isHidden) {
                        widget.setFlag(widgets_dist_index_es6_js_.Widget.Flag.IsVisible);
                    }
                    // Not called in NotebookWindowedLayout to avoid outputArea
                    // widgets unwanted update or reset.
                    messaging_dist_index_es6_js_.MessageLoop.sendMessage(widget, widgets_dist_index_es6_js_.Widget.Msg.AfterAttach);
                }
            }
        }
    }
    /**
     * A message handler invoked on an `'after-detach'` message.
     *
     * #### Notes
     * The default implementation of this method forwards the message
     * to all widgets. It assumes all widget nodes are attached to the
     * parent widget node.
     *
     * This may be reimplemented by subclasses as needed.
     */
    onAfterDetach(msg) {
        for (const widget of this) {
            // TODO we could improve this further by removing outputs based
            // on their mime type (for example plain/text or markdown could safely be detached)
            // If the cell is out of the view port, its children are already detached -> skip detaching
            if (!widget.hasClass(CELL_OUTPUT_WRAPPER_CLASS) &&
                widget.node.isConnected) {
                // Not called in NotebookWindowedLayout for windowed notebook
                messaging_dist_index_es6_js_.MessageLoop.sendMessage(widget, widgets_dist_index_es6_js_.Widget.Msg.BeforeDetach);
                this.parent.node.removeChild(widget.node);
                messaging_dist_index_es6_js_.MessageLoop.sendMessage(widget, msg);
            }
        }
    }
}
/**
 * A widget for a code cell.
 */
class CodeCell extends Cell {
    /**
     * Construct a code cell widget.
     */
    constructor(options) {
        var _a;
        super({ layout: new CodeCellLayout(), ...options, placeholder: true });
        this._headingsCache = null;
        this._outputHidden = false;
        this._outputWrapper = null;
        this._outputPlaceholder = null;
        this._syncScrolled = false;
        this.addClass(CODE_CELL_CLASS);
        const trans = this.translator.load('jupyterlab');
        // Only save options not handled by parent constructor.
        const rendermime = (this._rendermime = options.rendermime);
        const contentFactory = this.contentFactory;
        const model = this.model;
        this.maxNumberOutputs = options.maxNumberOutputs;
        // Note that modifying the below label warrants one to also modify
        // the same in this._outputLengthHandler. Ideally, this label must
        // have been a constant and used in both places but it is not done
        // so because of limitations in the translation manager.
        const ariaLabel = model.outputs.length === 0
            ? trans.__('Code Cell Content')
            : trans.__('Code Cell Content with Output');
        this.node.setAttribute('aria-label', ariaLabel);
        const output = (this._output = new outputarea_lib_index_js_.OutputArea({
            model: this.model.outputs,
            rendermime,
            contentFactory: contentFactory,
            maxNumberOutputs: this.maxNumberOutputs,
            translator: this.translator,
            promptOverlay: true,
            inputHistoryScope: options.inputHistoryScope
        }));
        output.addClass(CELL_OUTPUT_AREA_CLASS);
        output.toggleScrolling.connect(() => {
            this.outputsScrolled = !this.outputsScrolled;
        });
        output.initialize.connect(() => {
            this.updatePromptOverlayIcon();
        });
        // Defer setting placeholder as OutputArea must be instantiated before initializing the DOM
        this.placeholder = (_a = options.placeholder) !== null && _a !== void 0 ? _a : true;
        model.outputs.changed.connect(this.onOutputChanged, this);
        model.outputs.stateChanged.connect(this.onOutputChanged, this);
        model.stateChanged.connect(this.onStateChanged, this);
    }
    /**
     * Create children widgets.
     */
    initializeDOM() {
        if (!this.placeholder) {
            return;
        }
        super.initializeDOM();
        this.setPrompt(this.prompt);
        // Insert the output before the cell footer.
        const outputWrapper = (this._outputWrapper = new widgets_dist_index_es6_js_.Panel());
        outputWrapper.addClass(CELL_OUTPUT_WRAPPER_CLASS);
        const outputCollapser = new OutputCollapser();
        outputCollapser.addClass(CELL_OUTPUT_COLLAPSER_CLASS);
        outputWrapper.addWidget(outputCollapser);
        // Set a CSS if there are no outputs, and connect a signal for future
        // changes to the number of outputs. This is for conditional styling
        // if there are no outputs.
        if (this.model.outputs.length === 0) {
            this.addClass(NO_OUTPUTS_CLASS);
        }
        this._output.outputLengthChanged.connect(this._outputLengthHandler, this);
        outputWrapper.addWidget(this._output);
        const layout = this.layout;
        layout.insertWidget(layout.widgets.length - 1, new ResizeHandle(this.node));
        layout.insertWidget(layout.widgets.length - 1, outputWrapper);
        if (this.model.isDirty) {
            this.addClass(DIRTY_CLASS);
        }
        this._outputPlaceholder = new OutputPlaceholder({
            callback: () => {
                this.outputHidden = !this.outputHidden;
            },
            text: this.getOutputPlaceholderText(),
            translator: this.translator
        });
        const layoutWrapper = outputWrapper.layout;
        if (this.outputHidden) {
            layoutWrapper.removeWidget(this._output);
            layoutWrapper.addWidget(this._outputPlaceholder);
            if (this.inputHidden && !outputWrapper.isHidden) {
                this._outputWrapper.hide();
            }
        }
        const trans = this.translator.load('jupyterlab');
        const ariaLabel = this.model.outputs.length === 0
            ? trans.__('Code Cell Content')
            : trans.__('Code Cell Content with Output');
        this.node.setAttribute('aria-label', ariaLabel);
    }
    getOutputPlaceholderText() {
        var _a;
        const firstOutput = this.model.outputs.get(0);
        const outputData = firstOutput === null || firstOutput === void 0 ? void 0 : firstOutput.data;
        if (!outputData) {
            return undefined;
        }
        const supportedOutputTypes = [
            'text/html',
            'image/svg+xml',
            'application/pdf',
            'text/markdown',
            'text/plain',
            'application/vnd.jupyter.stderr',
            'application/vnd.jupyter.stdout',
            'text'
        ];
        const preferredOutput = supportedOutputTypes.find(mt => {
            const data = firstOutput.data[mt];
            return (Array.isArray(data) ? typeof data[0] : typeof data) === 'string';
        });
        const dataToDisplay = firstOutput.data[preferredOutput !== null && preferredOutput !== void 0 ? preferredOutput : ''];
        if (dataToDisplay !== undefined) {
            return (_a = (Array.isArray(dataToDisplay)
                ? dataToDisplay
                : dataToDisplay === null || dataToDisplay === void 0 ? void 0 : dataToDisplay.split('\n'))) === null || _a === void 0 ? void 0 : _a.find(part => part !== '');
        }
        return undefined;
    }
    /**
     * Initialize view state from model.
     *
     * #### Notes
     * Should be called after construction. For convenience, returns this, so it
     * can be chained in the construction, like `new Foo().initializeState();`
     */
    initializeState() {
        super.initializeState();
        this.loadScrolledState();
        this.setPrompt(`${this.model.executionCount || ''}`);
        return this;
    }
    get headings() {
        if (!this._headingsCache) {
            const headings = [];
            // Iterate over the code cell outputs to check for Markdown or HTML from which we can generate ToC headings...
            const outputs = this.model.outputs;
            for (let j = 0; j < outputs.length; j++) {
                const m = outputs.get(j);
                let htmlType = null;
                let mdType = null;
                Object.keys(m.data).forEach(t => {
                    if (!mdType && toc_lib_index_js_.TableOfContentsUtils.Markdown.isMarkdown(t)) {
                        mdType = t;
                    }
                    else if (!htmlType && toc_lib_index_js_.TableOfContentsUtils.isHTML(t)) {
                        htmlType = t;
                    }
                });
                // Parse HTML output
                if (htmlType) {
                    headings.push(...toc_lib_index_js_.TableOfContentsUtils.getHTMLHeadings(this._rendermime.sanitizer.sanitize(m.data[htmlType])).map(heading => {
                        return {
                            ...heading,
                            outputIndex: j,
                            type: Cell.HeadingType.HTML
                        };
                    }));
                }
                else if (mdType) {
                    headings.push(...toc_lib_index_js_.TableOfContentsUtils.Markdown.getHeadings(m.data[mdType]).map(heading => {
                        return {
                            ...heading,
                            outputIndex: j,
                            type: Cell.HeadingType.Markdown
                        };
                    }));
                }
            }
            this._headingsCache = headings;
        }
        return [...this._headingsCache];
    }
    /**
     * Get the output area for the cell.
     */
    get outputArea() {
        return this._output;
    }
    /**
     * The view state of output being collapsed.
     */
    get outputHidden() {
        return this._outputHidden;
    }
    set outputHidden(value) {
        var _a;
        if (this._outputHidden === value) {
            return;
        }
        if (!this.placeholder) {
            const layout = this._outputWrapper.layout;
            if (value) {
                layout.removeWidget(this._output);
                layout.addWidget(this._outputPlaceholder);
                if (this.inputHidden && !this._outputWrapper.isHidden) {
                    this._outputWrapper.hide();
                }
                if (this._outputPlaceholder) {
                    this._outputPlaceholder.text = (_a = this.getOutputPlaceholderText()) !== null && _a !== void 0 ? _a : '';
                }
            }
            else {
                if (this._outputWrapper.isHidden) {
                    this._outputWrapper.show();
                }
                layout.removeWidget(this._outputPlaceholder);
                layout.addWidget(this._output);
            }
        }
        this._outputHidden = value;
        if (this.syncCollapse) {
            this.saveCollapseState();
        }
    }
    /**
     * Save view collapse state to model
     */
    saveCollapseState() {
        // Because collapse state for a code cell involves two different pieces of
        // metadata (the `collapsed` and `jupyter` metadata keys), we block reacting
        // to changes in metadata until we have fully committed our changes.
        // Otherwise setting one key can trigger a write to the other key to
        // maintain the synced consistency.
        this.model.sharedModel.transact(() => {
            super.saveCollapseState();
            const collapsed = this.model.getMetadata('collapsed');
            if ((this.outputHidden && collapsed === true) ||
                (!this.outputHidden && collapsed === undefined)) {
                return;
            }
            // Do not set jupyter.outputs_hidden since it is redundant. See
            // and https://github.com/jupyter/nbformat/issues/137
            if (this.outputHidden) {
                this.model.setMetadata('collapsed', true);
            }
            else {
                this.model.deleteMetadata('collapsed');
            }
        }, false);
    }
    /**
     * Revert view collapse state from model.
     *
     * We consider the `collapsed` metadata key as the source of truth for outputs
     * being hidden.
     */
    loadCollapseState() {
        super.loadCollapseState();
        this.outputHidden = !!this.model.getMetadata('collapsed');
    }
    /**
     * Whether the output is in a scrolled state?
     */
    get outputsScrolled() {
        return this._outputsScrolled;
    }
    set outputsScrolled(value) {
        this.toggleClass('jp-mod-outputsScrolled', value);
        this._outputsScrolled = value;
        if (this.syncScrolled) {
            this.saveScrolledState();
        }
        this.updatePromptOverlayIcon();
    }
    /**
     * Update the Prompt Overlay Icon
     */
    updatePromptOverlayIcon() {
        var _a;
        const overlay = apputils_lib_index_js_.DOMUtils.findElement(this.node, 'jp-OutputArea-promptOverlay');
        if (!overlay) {
            return;
        }
        // If you are changing this, don't forget about svg.
        const ICON_HEIGHT = 16 + 4 + 4; // 4px for padding
        if (overlay.clientHeight <= ICON_HEIGHT) {
            (_a = overlay.firstChild) === null || _a === void 0 ? void 0 : _a.remove();
            return;
        }
        let overlayTitle;
        if (this._outputsScrolled) {
            index_js_.expandIcon.element({
                container: overlay
            });
            overlayTitle = 'Expand Output';
        }
        else {
            index_js_.collapseIcon.element({
                container: overlay
            });
            overlayTitle = 'Collapse Output';
        }
        const trans = this.translator.load('jupyterlab');
        overlay.title = trans.__(overlayTitle);
    }
    /**
     * Save view collapse state to model
     */
    saveScrolledState() {
        const current = this.model.getMetadata('scrolled');
        if ((this.outputsScrolled && current === true) ||
            (!this.outputsScrolled && current === undefined)) {
            return;
        }
        if (this.outputsScrolled) {
            this.model.setMetadata('scrolled', true);
        }
        else {
            this.model.deleteMetadata('scrolled');
        }
    }
    /**
     * Revert view collapse state from model.
     */
    loadScrolledState() {
        // We don't have the notion of 'auto' scrolled, so we make it false.
        if (this.model.getMetadata('scrolled') === 'auto') {
            this.outputsScrolled = false;
        }
        else {
            this.outputsScrolled = !!this.model.getMetadata('scrolled');
        }
    }
    /**
     * Whether to sync the scrolled state to the cell model.
     */
    get syncScrolled() {
        return this._syncScrolled;
    }
    set syncScrolled(value) {
        if (this._syncScrolled === value) {
            return;
        }
        this._syncScrolled = value;
        if (value) {
            this.loadScrolledState();
        }
    }
    /**
     * Handle the input being hidden.
     *
     * #### Notes
     * This method is called by the case cell implementation and is
     * subclasses here so the code cell can watch to see when input
     * is hidden without accessing private state.
     */
    handleInputHidden(value) {
        if (this.placeholder) {
            return;
        }
        if (!value && this._outputWrapper.isHidden) {
            this._outputWrapper.show();
        }
        else if (value && !this._outputWrapper.isHidden && this._outputHidden) {
            this._outputWrapper.hide();
        }
    }
    /**
     * Clone the cell, using the same model.
     */
    clone() {
        const constructor = this.constructor;
        return new constructor({
            model: this.model,
            contentFactory: this.contentFactory,
            rendermime: this._rendermime,
            placeholder: false,
            translator: this.translator
        });
    }
    /**
     * Clone the OutputArea alone, returning a simplified output area, using the same model.
     */
    cloneOutputArea() {
        return new outputarea_lib_index_js_.SimplifiedOutputArea({
            model: this.model.outputs,
            contentFactory: this.contentFactory,
            rendermime: this._rendermime
        });
    }
    /**
     * Dispose of the resources used by the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._output.outputLengthChanged.disconnect(this._outputLengthHandler, this);
        this._rendermime = null;
        this._output = null;
        this._outputWrapper = null;
        this._outputPlaceholder = null;
        super.dispose();
    }
    /**
     * Handle changes in the model.
     */
    onStateChanged(model, args) {
        switch (args.name) {
            case 'executionCount':
                this.setPrompt(`${model.executionCount || ''}`);
                break;
            case 'isDirty':
                if (model.isDirty) {
                    this.addClass(DIRTY_CLASS);
                }
                else {
                    this.removeClass(DIRTY_CLASS);
                }
                break;
            default:
                break;
        }
    }
    /**
     * Callback on output changes
     */
    onOutputChanged() {
        var _a;
        this._headingsCache = null;
        if (this._outputPlaceholder && this.outputHidden) {
            this._outputPlaceholder.text = (_a = this.getOutputPlaceholderText()) !== null && _a !== void 0 ? _a : '';
        }
        // This is to hide/show icon on single line output.
        this.updatePromptOverlayIcon();
    }
    /**
     * Handle changes in the metadata.
     */
    onMetadataChanged(model, args) {
        switch (args.key) {
            case 'scrolled':
                if (this.syncScrolled) {
                    this.loadScrolledState();
                }
                break;
            case 'collapsed':
                if (this.syncCollapse) {
                    this.loadCollapseState();
                }
                break;
            default:
                break;
        }
        super.onMetadataChanged(model, args);
    }
    /**
     * Handle changes in the number of outputs in the output area.
     */
    _outputLengthHandler(sender, args) {
        const force = args === 0 ? true : false;
        this.toggleClass(NO_OUTPUTS_CLASS, force);
        const trans = this.translator.load('jupyterlab');
        const ariaLabel = force
            ? trans.__('Code Cell Content')
            : trans.__('Code Cell Content with Output');
        this.node.setAttribute('aria-label', ariaLabel);
    }
}
/**
 * The namespace for the `CodeCell` class statics.
 */
(function (CodeCell) {
    /**
     * Execute a cell given a client session.
     */
    async function execute(cell, sessionContext, metadata) {
        var _a;
        const model = cell.model;
        const code = model.sharedModel.getSource();
        if (!code.trim() || !((_a = sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel)) {
            model.sharedModel.transact(() => {
                model.clearExecution();
            }, false);
            return;
        }
        const cellId = { cellId: model.sharedModel.getId() };
        metadata = {
            ...model.metadata,
            ...metadata,
            ...cellId
        };
        const { recordTiming } = metadata;
        model.sharedModel.transact(() => {
            model.clearExecution();
            cell.outputHidden = false;
        }, false);
        cell.setPrompt('*');
        model.trusted = true;
        let future;
        try {
            const msgPromise = outputarea_lib_index_js_.OutputArea.execute(code, cell.outputArea, sessionContext, metadata);
            // cell.outputArea.future assigned synchronously in `execute`
            if (recordTiming) {
                const recordTimingHook = (msg) => {
                    let label;
                    switch (msg.header.msg_type) {
                        case 'status':
                            label = `status.${msg.content.execution_state}`;
                            break;
                        case 'execute_input':
                            label = 'execute_input';
                            break;
                        default:
                            return true;
                    }
                    // If the data is missing, estimate it to now
                    // Date was added in 5.1: https://jupyter-client.readthedocs.io/en/stable/messaging.html#message-header
                    const value = msg.header.date || new Date().toISOString();
                    const timingInfo = Object.assign({}, model.getMetadata('execution'));
                    timingInfo[`iopub.${label}`] = value;
                    model.setMetadata('execution', timingInfo);
                    return true;
                };
                cell.outputArea.future.registerMessageHook(recordTimingHook);
            }
            else {
                model.deleteMetadata('execution');
            }
            // Save this execution's future so we can compare in the catch below.
            future = cell.outputArea.future;
            const msg = (await msgPromise);
            model.executionCount = msg.content.execution_count;
            if (recordTiming) {
                const timingInfo = Object.assign({}, model.getMetadata('execution'));
                const started = msg.metadata.started;
                // Started is not in the API, but metadata IPyKernel sends
                if (started) {
                    timingInfo['shell.execute_reply.started'] = started;
                }
                // Per above, the 5.0 spec does not assume date, so we estimate is required
                const finished = msg.header.date;
                timingInfo['shell.execute_reply'] =
                    finished || new Date().toISOString();
                model.setMetadata('execution', timingInfo);
            }
            return msg;
        }
        catch (e) {
            // If we started executing, and the cell is still indicating this
            // execution, clear the prompt.
            if (future && !cell.isDisposed && cell.outputArea.future === future) {
                cell.setPrompt('');
            }
            throw e;
        }
    }
    CodeCell.execute = execute;
})(CodeCell || (CodeCell = {}));
/**
 * `AttachmentsCell` - A base class for a cell widget that allows
 *  attachments to be drag/drop'd or pasted onto it
 */
class AttachmentsCell extends Cell {
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
     * Get the editor options at initialization.
     *
     * @returns Editor options
     */
    getEditorOptions() {
        var _a, _b;
        const base = (_a = super.getEditorOptions()) !== null && _a !== void 0 ? _a : {};
        base.extensions = [
            ...((_b = base.extensions) !== null && _b !== void 0 ? _b : []),
            dist_index_js_.EditorView.domEventHandlers({
                dragenter: (event) => {
                    event.preventDefault();
                },
                dragover: (event) => {
                    event.preventDefault();
                },
                drop: (event) => {
                    this._evtNativeDrop(event);
                },
                paste: (event) => {
                    this._evtPaste(event);
                }
            })
        ];
        return base;
    }
    /**
     * Handle `after-attach` messages for the widget.
     */
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        const node = this.node;
        node.addEventListener('lm-dragover', this);
        node.addEventListener('lm-drop', this);
    }
    /**
     * A message handler invoked on a `'before-detach'`
     * message
     */
    onBeforeDetach(msg) {
        const node = this.node;
        node.removeEventListener('lm-dragover', this);
        node.removeEventListener('lm-drop', this);
        super.onBeforeDetach(msg);
    }
    _evtDragOver(event) {
        const supportedMimeType = (0,algorithm_dist_index_es6_js_.some)(rendermime_lib_index_js_.imageRendererFactory.mimeTypes, mimeType => {
            if (!event.mimeData.hasData(CONTENTS_MIME_RICH)) {
                return false;
            }
            const data = event.mimeData.getData(CONTENTS_MIME_RICH);
            return data.model.mimetype === mimeType;
        });
        if (!supportedMimeType) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
        event.dropAction = event.proposedAction;
    }
    /**
     * Handle the `paste` event for the widget
     */
    _evtPaste(event) {
        if (event.clipboardData) {
            const items = event.clipboardData.items;
            for (let i = 0; i < items.length; i++) {
                if (items[i].type === 'text/plain') {
                    // Skip if this text is the path to a file
                    if (i < items.length - 1 && items[i + 1].kind === 'file') {
                        continue;
                    }
                    items[i].getAsString(text => {
                        var _a, _b;
                        (_b = (_a = this.editor).replaceSelection) === null || _b === void 0 ? void 0 : _b.call(_a, text);
                    });
                }
                this._attachFiles(event.clipboardData.items);
            }
        }
        event.preventDefault();
    }
    /**
     * Handle the `drop` event for the widget
     */
    _evtNativeDrop(event) {
        if (event.dataTransfer) {
            this._attachFiles(event.dataTransfer.items);
        }
        event.preventDefault();
    }
    /**
     * Handle the `'lm-drop'` event for the widget.
     */
    _evtDrop(event) {
        const supportedMimeTypes = event.mimeData.types().filter(mimeType => {
            if (mimeType === CONTENTS_MIME_RICH) {
                const data = event.mimeData.getData(CONTENTS_MIME_RICH);
                return (rendermime_lib_index_js_.imageRendererFactory.mimeTypes.indexOf(data.model.mimetype) !== -1);
            }
            return rendermime_lib_index_js_.imageRendererFactory.mimeTypes.indexOf(mimeType) !== -1;
        });
        if (supportedMimeTypes.length === 0) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
        if (event.proposedAction === 'none') {
            event.dropAction = 'none';
            return;
        }
        event.dropAction = 'copy';
        for (const mimeType of supportedMimeTypes) {
            if (mimeType === CONTENTS_MIME_RICH) {
                const { model, withContent } = event.mimeData.getData(CONTENTS_MIME_RICH);
                if (model.type === 'file') {
                    const URI = this._generateURI(model.name);
                    this.updateCellSourceWithAttachment(model.name, URI);
                    void withContent().then(fullModel => {
                        this.model.attachments.set(URI, {
                            [fullModel.mimetype]: fullModel.content
                        });
                    });
                }
            }
            else {
                // Pure mimetype, no useful name to infer
                const URI = this._generateURI();
                this.model.attachments.set(URI, {
                    [mimeType]: event.mimeData.getData(mimeType)
                });
                this.updateCellSourceWithAttachment(URI, URI);
            }
        }
    }
    /**
     * Attaches all DataTransferItems (obtained from
     * clipboard or native drop events) to the cell
     */
    _attachFiles(items) {
        for (let i = 0; i < items.length; i++) {
            const item = items[i];
            if (item.kind === 'file') {
                const blob = item.getAsFile();
                if (blob) {
                    this._attachFile(blob);
                }
            }
        }
    }
    /**
     * Takes in a file object and adds it to
     * the cell attachments
     */
    _attachFile(blob) {
        const reader = new FileReader();
        reader.onload = evt => {
            const { href, protocol } = coreutils_lib_index_js_.URLExt.parse(reader.result);
            if (protocol !== 'data:') {
                return;
            }
            const dataURIRegex = /([\w+\/\+]+)?(?:;(charset=[\w\d-]*|base64))?,(.*)/;
            const matches = dataURIRegex.exec(href);
            if (!matches || matches.length !== 4) {
                return;
            }
            const mimeType = matches[1];
            const encodedData = matches[3];
            const bundle = { [mimeType]: encodedData };
            const URI = this._generateURI(blob.name);
            if (mimeType.startsWith('image/')) {
                this.model.attachments.set(URI, bundle);
                this.updateCellSourceWithAttachment(blob.name, URI);
            }
        };
        reader.onerror = evt => {
            console.error(`Failed to attach ${blob.name}` + evt);
        };
        reader.readAsDataURL(blob);
    }
    /**
     * Generates a unique URI for a file
     * while preserving the file extension.
     */
    _generateURI(name = '') {
        const lastIndex = name.lastIndexOf('.');
        return lastIndex !== -1
            ? coreutils_dist_index_js_.UUID.uuid4().concat(name.substring(lastIndex))
            : coreutils_dist_index_js_.UUID.uuid4();
    }
}
/** ****************************************************************************
 * MarkdownCell
 ******************************************************************************/
/**
 * A widget for a Markdown cell.
 *
 * #### Notes
 * Things get complicated if we want the rendered text to update
 * any time the text changes, the text editor model changes,
 * or the input area model changes.  We don't support automatically
 * updating the rendered text in all of these cases.
 */
class MarkdownCell extends AttachmentsCell {
    /**
     * Construct a Markdown cell widget.
     */
    constructor(options) {
        var _a, _b, _c, _d;
        super({ ...options, placeholder: true });
        this._headingsCache = null;
        this._headingCollapsedChanged = new signaling_dist_index_es6_js_.Signal(this);
        this._prevText = '';
        this._rendered = true;
        this._renderedChanged = new signaling_dist_index_es6_js_.Signal(this);
        this._showEditorForReadOnlyMarkdown = true;
        this.addClass(MARKDOWN_CELL_CLASS);
        this.model.contentChanged.connect(this.onContentChanged, this);
        const trans = this.translator.load('jupyterlab');
        this.node.setAttribute('aria-label', trans.__('Markdown Cell Content'));
        // Ensure we can resolve attachments:
        this._rendermime = options.rendermime.clone({
            resolver: new attachments_lib_index_js_.AttachmentsResolver({
                parent: (_a = options.rendermime.resolver) !== null && _a !== void 0 ? _a : undefined,
                model: this.model.attachments
            })
        });
        this._renderer = this._rendermime.createRenderer('text/markdown');
        this._renderer.addClass(MARKDOWN_OUTPUT_CLASS);
        // Check if heading cell is set to be collapsed
        this._headingCollapsed = ((_b = this.model.getMetadata(MARKDOWN_HEADING_COLLAPSED)) !== null && _b !== void 0 ? _b : false);
        this._showEditorForReadOnlyMarkdown =
            (_c = options.showEditorForReadOnlyMarkdown) !== null && _c !== void 0 ? _c : MarkdownCell.defaultShowEditorForReadOnlyMarkdown;
        // Defer setting placeholder as the renderer must be instantiated before initializing the DOM
        this.placeholder = (_d = options.placeholder) !== null && _d !== void 0 ? _d : true;
        this._monitor = new coreutils_lib_index_js_.ActivityMonitor({
            signal: this.model.contentChanged,
            timeout: RENDER_TIMEOUT
        });
        // Throttle the rendering rate of the widget.
        this.ready
            .then(() => {
            if (this.isDisposed) {
                // Bail early
                return;
            }
            this._monitor.activityStopped.connect(() => {
                if (this._rendered) {
                    this.update();
                }
            }, this);
        })
            .catch(reason => {
            console.error('Failed to be ready', reason);
        });
    }
    /**
     * Text that represents the highest heading (i.e. lowest level) if cell is a heading.
     * Returns empty string if not a heading.
     */
    get headingInfo() {
        // Use table of content algorithm for consistency
        const headings = this.headings;
        if (headings.length > 0) {
            // Return the highest level
            const { text, level } = headings.reduce((prev, curr) => (prev.level <= curr.level ? prev : curr), headings[0]);
            return { text, level };
        }
        else {
            return { text: '', level: -1 };
        }
    }
    get headings() {
        if (!this._headingsCache) {
            // Use table of content algorithm for consistency
            const headings = toc_lib_index_js_.TableOfContentsUtils.Markdown.getHeadings(this.model.sharedModel.getSource());
            this._headingsCache = headings.map(h => {
                return { ...h, type: Cell.HeadingType.Markdown };
            });
        }
        return [...this._headingsCache];
    }
    /**
     * Whether the heading is collapsed or not.
     */
    get headingCollapsed() {
        return this._headingCollapsed;
    }
    set headingCollapsed(value) {
        var _a;
        if (this._headingCollapsed !== value) {
            this._headingCollapsed = value;
            if (value) {
                this.model.setMetadata(MARKDOWN_HEADING_COLLAPSED, value);
            }
            else if (this.model.getMetadata(MARKDOWN_HEADING_COLLAPSED) !== 'undefined') {
                this.model.deleteMetadata(MARKDOWN_HEADING_COLLAPSED);
            }
            const collapseButton = (_a = this.inputArea) === null || _a === void 0 ? void 0 : _a.promptNode.getElementsByClassName(HEADING_COLLAPSER_CLASS)[0];
            if (collapseButton) {
                if (value) {
                    collapseButton.classList.add('jp-mod-collapsed');
                }
                else {
                    collapseButton.classList.remove('jp-mod-collapsed');
                }
            }
            this.renderCollapseButtons(this._renderer);
            this._headingCollapsedChanged.emit(this._headingCollapsed);
        }
    }
    /**
     * Number of collapsed sub cells.
     */
    get numberChildNodes() {
        return this._numberChildNodes;
    }
    set numberChildNodes(value) {
        this._numberChildNodes = value;
        this.renderCollapseButtons(this._renderer);
    }
    /**
     * Signal emitted when the cell collapsed state changes.
     */
    get headingCollapsedChanged() {
        return this._headingCollapsedChanged;
    }
    /**
     * Whether the cell is rendered.
     */
    get rendered() {
        return this._rendered;
    }
    set rendered(value) {
        // Show cell as rendered when cell is not editable
        if (this.readOnly && this._showEditorForReadOnlyMarkdown === false) {
            value = true;
        }
        if (value === this._rendered) {
            return;
        }
        this._rendered = value;
        this._handleRendered()
            .then(() => {
            // If the rendered state changed, raise an event.
            this._displayChanged.emit();
            this._renderedChanged.emit(this._rendered);
        })
            .catch(reason => {
            console.error('Failed to render', reason);
        });
    }
    /**
     * Signal emitted when the markdown cell rendered state changes
     */
    get renderedChanged() {
        return this._renderedChanged;
    }
    /*
     * Whether the Markdown editor is visible in read-only mode.
     */
    get showEditorForReadOnly() {
        return this._showEditorForReadOnlyMarkdown;
    }
    set showEditorForReadOnly(value) {
        this._showEditorForReadOnlyMarkdown = value;
        if (value === false) {
            this.rendered = true;
        }
    }
    /**
     * Renderer
     */
    get renderer() {
        return this._renderer;
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._monitor.dispose();
        super.dispose();
    }
    /**
     * Create children widgets.
     */
    initializeDOM() {
        if (!this.placeholder) {
            return;
        }
        super.initializeDOM();
        this.renderCollapseButtons(this._renderer);
        this._handleRendered().catch(reason => {
            console.error('Failed to render', reason);
        });
    }
    maybeCreateCollapseButton() {
        var _a;
        const { level } = this.headingInfo;
        if (level > 0 &&
            ((_a = this.inputArea) === null || _a === void 0 ? void 0 : _a.promptNode.getElementsByClassName(HEADING_COLLAPSER_CLASS).length) == 0) {
            let collapseButton = this.inputArea.promptNode.appendChild(document.createElement('button'));
            collapseButton.className = `jp-Button ${HEADING_COLLAPSER_CLASS}`;
            collapseButton.setAttribute('data-heading-level', level.toString());
            if (this._headingCollapsed) {
                collapseButton.classList.add('jp-mod-collapsed');
            }
            else {
                collapseButton.classList.remove('jp-mod-collapsed');
            }
            collapseButton.onclick = (event) => {
                this.headingCollapsed = !this.headingCollapsed;
            };
        }
    }
    /**
     * Create, update or remove the hidden cells button.
     * Note that the actual visibility is controlled in Static Notebook by toggling jp-mod-showHiddenCellsButton class.
     */
    maybeCreateOrUpdateExpandButton() {
        const showHiddenCellsButtonList = this.node.getElementsByClassName(SHOW_HIDDEN_CELLS_CLASS);
        let trans = this.translator.load('jupyterlab');
        let buttonText = trans._n('%1 cell hidden', '%1 cells hidden', this._numberChildNodes);
        let needToCreateButton = this.headingCollapsed &&
            this._numberChildNodes > 0 &&
            showHiddenCellsButtonList.length == 0;
        if (needToCreateButton) {
            const newShowHiddenCellsButton = document.createElement('button');
            newShowHiddenCellsButton.className = `jp-mod-minimal jp-Button ${SHOW_HIDDEN_CELLS_CLASS}`;
            index_js_.addIcon.render(newShowHiddenCellsButton);
            const buttonTextElement = document.createElement('div');
            buttonTextElement.textContent = buttonText;
            newShowHiddenCellsButton.appendChild(buttonTextElement);
            newShowHiddenCellsButton.onclick = () => {
                this.headingCollapsed = false;
            };
            this.node.appendChild(newShowHiddenCellsButton);
        }
        let needToUpdateButtonText = this.headingCollapsed &&
            this._numberChildNodes > 0 &&
            showHiddenCellsButtonList.length == 1;
        if (needToUpdateButtonText) {
            showHiddenCellsButtonList[0].childNodes[1].textContent = buttonText;
        }
        let needToRemoveButton = !(this.headingCollapsed && this._numberChildNodes > 0);
        if (needToRemoveButton) {
            for (const button of showHiddenCellsButtonList) {
                this.node.removeChild(button);
            }
        }
    }
    /**
     * Callback on content changed
     */
    onContentChanged() {
        super.onContentChanged();
        this._headingsCache = null;
    }
    /**
     * Render the collapse button for heading cells,
     * and for collapsed heading cells render the "expand hidden cells"
     * button.
     */
    renderCollapseButtons(widget) {
        this.node.classList.toggle(MARKDOWN_HEADING_COLLAPSED, this._headingCollapsed);
        this.maybeCreateCollapseButton();
        this.maybeCreateOrUpdateExpandButton();
    }
    /**
     * Render an input instead of the text editor.
     */
    renderInput(widget) {
        this.addClass(RENDERED_CLASS);
        if (!this.placeholder && !this.isDisposed) {
            this.renderCollapseButtons(widget);
            this.inputArea.renderInput(widget);
        }
    }
    /**
     * Show the text editor instead of rendered input.
     */
    showEditor() {
        this.removeClass(RENDERED_CLASS);
        if (!this.placeholder && !this.isDisposed) {
            this.inputArea.showEditor();
            // if this is going to be a heading, place the cursor accordingly
            let numHashAtStart = (this.model.sharedModel
                .getSource()
                .match(/^#+/g) || [''])[0].length;
            if (numHashAtStart > 0) {
                this.inputArea.editor.setCursorPosition({
                    column: numHashAtStart + 1,
                    line: 0
                });
            }
        }
    }
    /*
     * Handle `update-request` messages.
     */
    onUpdateRequest(msg) {
        // Make sure we are properly rendered.
        this._handleRendered().catch(reason => {
            console.error('Failed to render', reason);
        });
        super.onUpdateRequest(msg);
    }
    /**
     * Modify the cell source to include a reference to the attachment.
     */
    updateCellSourceWithAttachment(attachmentName, URI) {
        var _a, _b;
        const textToBeAppended = `![${attachmentName}](attachment:${URI !== null && URI !== void 0 ? URI : attachmentName})`;
        // TODO this should be done on the model...
        (_b = (_a = this.editor) === null || _a === void 0 ? void 0 : _a.replaceSelection) === null || _b === void 0 ? void 0 : _b.call(_a, textToBeAppended);
    }
    /**
     * Handle the rendered state.
     */
    async _handleRendered() {
        if (!this._rendered) {
            this.showEditor();
        }
        else {
            // TODO: It would be nice for the cell to provide a way for
            // its consumers to hook into when the rendering is done.
            await this._updateRenderedInput();
            if (this._rendered) {
                // The rendered flag may be updated in the mean time
                this.renderInput(this._renderer);
            }
        }
    }
    /**
     * Update the rendered input.
     */
    _updateRenderedInput() {
        if (this.placeholder) {
            return Promise.resolve();
        }
        const model = this.model;
        const text = (model && model.sharedModel.getSource()) || DEFAULT_MARKDOWN_TEXT;
        // Do not re-render if the text has not changed.
        if (text !== this._prevText) {
            const mimeModel = new rendermime_lib_index_js_.MimeModel({ data: { 'text/markdown': text } });
            this._prevText = text;
            return this._renderer.renderModel(mimeModel);
        }
        return Promise.resolve();
    }
    /**
     * Clone the cell, using the same model.
     */
    clone() {
        const constructor = this.constructor;
        return new constructor({
            model: this.model,
            contentFactory: this.contentFactory,
            rendermime: this._rendermime,
            placeholder: false,
            translator: this.translator
        });
    }
}
/**
 * The namespace for the `CodeCell` class statics.
 */
(function (MarkdownCell) {
    /**
     * Default value for showEditorForReadOnlyMarkdown.
     */
    MarkdownCell.defaultShowEditorForReadOnlyMarkdown = true;
})(MarkdownCell || (MarkdownCell = {}));
/** ****************************************************************************
 * RawCell
 ******************************************************************************/
/**
 * A widget for a raw cell.
 */
class RawCell extends Cell {
    /**
     * Construct a raw cell widget.
     */
    constructor(options) {
        super(options);
        this.addClass(RAW_CELL_CLASS);
        const trans = this.translator.load('jupyterlab');
        this.node.setAttribute('aria-label', trans.__('Raw Cell Content'));
    }
    /**
     * Clone the cell, using the same model.
     */
    clone() {
        const constructor = this.constructor;
        return new constructor({
            model: this.model,
            contentFactory: this.contentFactory,
            placeholder: false,
            translator: this.translator
        });
    }
}

;// CONCATENATED MODULE: ../packages/cells/lib/index.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module cells
 */










/***/ })

}]);
//# sourceMappingURL=4942.2d4e6b2470b95226c5db.js.map?v=2d4e6b2470b95226c5db