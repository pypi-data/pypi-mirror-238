"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[8097,9386],{

/***/ 18097:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "CellBarExtension": () => (/* reexport */ CellBarExtension),
  "CellToolbarTracker": () => (/* reexport */ CellToolbarTracker)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/observables@~5.1.0-alpha.2 (strict) (fallback: ../packages/observables/lib/index.js)
var lib_index_js_ = __webpack_require__(57090);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(16415);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(30205);
;// CONCATENATED MODULE: ../packages/cell-toolbar/lib/celltoolbartracker.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/





/*
 * Text mime types
 */
const TEXT_MIME_TYPES = [
    'text/plain',
    'application/vnd.jupyter.stdout',
    'application/vnd.jupyter.stderr'
];
/**
 * Widget cell toolbar classes
 */
const CELL_TOOLBAR_CLASS = 'jp-cell-toolbar';
const CELL_MENU_CLASS = 'jp-cell-menu';
/**
 * Class for a cell whose contents overlap with the cell toolbar
 */
const TOOLBAR_OVERLAP_CLASS = 'jp-toolbar-overlap';
/**
 * Watch a notebook so that a cell toolbar appears on the active cell
 */
class CellToolbarTracker {
    constructor(panel, toolbar) {
        var _a;
        this._isDisposed = false;
        this._panel = panel;
        this._previousActiveCell = this._panel.content.activeCell;
        this._toolbar = toolbar;
        this._onToolbarChanged();
        this._toolbar.changed.connect(this._onToolbarChanged, this);
        // Only add the toolbar to the notebook's active cell (if any) once it has fully rendered and been revealed.
        void panel.revealed.then(() => {
            // Wait one frame (at 60 fps) for the panel to render the first cell, then display the cell toolbar on it if possible.
            setTimeout(() => {
                this._onActiveCellChanged(panel.content);
            }, 1000 / 60);
        });
        // Check whether the toolbar should be rendered upon a layout change
        panel.content.renderingLayoutChanged.connect(this._onActiveCellChanged, this);
        // Handle subsequent changes of active cell.
        panel.content.activeCellChanged.connect(this._onActiveCellChanged, this);
        (_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.model.metadataChanged.connect(this._onMetadataChanged, this);
        panel.disposed.connect(() => {
            var _a;
            panel.content.activeCellChanged.disconnect(this._onActiveCellChanged);
            (_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.model.metadataChanged.disconnect(this._onMetadataChanged);
        });
    }
    _onMetadataChanged(model, args) {
        if (args.key === 'jupyter') {
            if (typeof args.newValue === 'object' &&
                args.newValue.source_hidden === true &&
                (args.type === 'add' || args.type === 'change')) {
                // Cell just became hidden; remove toolbar
                this._removeToolbar(model);
            }
            // Check whether input visibility changed
            else if (typeof args.oldValue === 'object' &&
                args.oldValue.source_hidden === true) {
                // Cell just became visible; add toolbar
                this._addToolbar(model);
            }
        }
    }
    _onActiveCellChanged(notebook) {
        if (this._previousActiveCell && !this._previousActiveCell.isDisposed) {
            // Disposed cells do not have a model anymore.
            this._removeToolbar(this._previousActiveCell.model);
            this._previousActiveCell.model.metadataChanged.disconnect(this._onMetadataChanged);
        }
        const activeCell = notebook.activeCell;
        if (activeCell === null || activeCell.inputHidden) {
            return;
        }
        activeCell.model.metadataChanged.connect(this._onMetadataChanged, this);
        this._addToolbar(activeCell.model);
        this._previousActiveCell = activeCell;
    }
    get isDisposed() {
        return this._isDisposed;
    }
    dispose() {
        var _a;
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._toolbar.changed.disconnect(this._onToolbarChanged, this);
        const cells = (_a = this._panel) === null || _a === void 0 ? void 0 : _a.context.model.cells;
        if (cells) {
            for (const model of cells) {
                this._removeToolbar(model);
            }
        }
        this._panel = null;
        dist_index_es6_js_.Signal.clearData(this);
    }
    _addToolbar(model) {
        const cell = this._getCell(model);
        if (cell) {
            const toolbarWidget = new ui_components_lib_index_js_.Toolbar();
            toolbarWidget.addClass(CELL_MENU_CLASS);
            const promises = [];
            for (const { name, widget } of this._toolbar) {
                toolbarWidget.addItem(name, widget);
                if (widget instanceof ui_components_lib_index_js_.ReactWidget &&
                    widget.renderPromise !== undefined) {
                    widget.update();
                    promises.push(widget.renderPromise);
                }
            }
            // Wait for all the buttons to be rendered before attaching the toolbar.
            Promise.all(promises)
                .then(() => {
                toolbarWidget.addClass(CELL_TOOLBAR_CLASS);
                cell.layout.insertWidget(0, toolbarWidget);
                // For rendered markdown, watch for resize events.
                cell.displayChanged.connect(this._resizeEventCallback, this);
                // Watch for changes in the cell's contents.
                cell.model.contentChanged.connect(this._changedEventCallback, this);
                // Hide the cell toolbar if it overlaps with cell contents
                this._updateCellForToolbarOverlap(cell);
            })
                .catch(e => {
                console.error('Error rendering buttons of the cell toolbar: ', e);
            });
        }
    }
    _getCell(model) {
        var _a;
        return (_a = this._panel) === null || _a === void 0 ? void 0 : _a.content.widgets.find(widget => widget.model === model);
    }
    _findToolbarWidgets(cell) {
        const widgets = cell.layout.widgets;
        // Search for header using the CSS class or use the first one if not found.
        return widgets.filter(widget => widget.hasClass(CELL_TOOLBAR_CLASS)) || [];
    }
    _removeToolbar(model) {
        const cell = this._getCell(model);
        if (cell) {
            this._findToolbarWidgets(cell).forEach(widget => {
                widget.dispose();
            });
            // Attempt to remove the resize and changed event handlers.
            cell.displayChanged.disconnect(this._resizeEventCallback, this);
        }
        model.contentChanged.disconnect(this._changedEventCallback, this);
    }
    /**
     * Call back on settings changes
     */
    _onToolbarChanged() {
        var _a;
        // Reset toolbar when settings changes
        const activeCell = (_a = this._panel) === null || _a === void 0 ? void 0 : _a.content.activeCell;
        if (activeCell) {
            this._removeToolbar(activeCell.model);
            this._addToolbar(activeCell.model);
        }
    }
    _changedEventCallback() {
        var _a;
        const activeCell = (_a = this._panel) === null || _a === void 0 ? void 0 : _a.content.activeCell;
        if (activeCell === null || activeCell === undefined) {
            return;
        }
        this._updateCellForToolbarOverlap(activeCell);
    }
    _resizeEventCallback() {
        var _a;
        const activeCell = (_a = this._panel) === null || _a === void 0 ? void 0 : _a.content.activeCell;
        if (activeCell === null || activeCell === undefined) {
            return;
        }
        this._updateCellForToolbarOverlap(activeCell);
    }
    _updateCellForToolbarOverlap(activeCell) {
        // When we do change in cell, If we don't wait the browser might not have
        // completed the layout update, resulting in the previous width being returned
        // using `getBoundingClientRect().width` in later functions.
        requestAnimationFrame(() => {
            // Remove the "toolbar overlap" class from the cell, rendering the cell's toolbar
            const activeCellElement = activeCell.node;
            activeCellElement.classList.remove(TOOLBAR_OVERLAP_CLASS);
            if (this._cellToolbarOverlapsContents(activeCell)) {
                // Add the "toolbar overlap" class to the cell, completely concealing the toolbar,
                // if the first line of the content overlaps with it at all
                activeCellElement.classList.add(TOOLBAR_OVERLAP_CLASS);
            }
        });
    }
    _cellToolbarOverlapsContents(activeCell) {
        var _a;
        const cellType = activeCell.model.type;
        // If the toolbar is too large for the current cell, hide it.
        const cellLeft = this._cellEditorWidgetLeft(activeCell);
        const cellRight = this._cellEditorWidgetRight(activeCell);
        const toolbarLeft = this._cellToolbarLeft(activeCell);
        if (toolbarLeft === null) {
            return false;
        }
        // The toolbar should not take up more than 50% of the cell.
        if ((cellLeft + cellRight) / 2 > toolbarLeft) {
            return true;
        }
        if (cellType === 'markdown' && activeCell.rendered) {
            // Check for overlap in rendered markdown content
            return this._markdownOverlapsToolbar(activeCell);
        }
        // Check for overlap in code content
        if (((_a = this._panel) === null || _a === void 0 ? void 0 : _a.content.renderingLayout) === 'default') {
            return this._codeOverlapsToolbar(activeCell);
        }
        else {
            return this._outputOverlapsToolbar(activeCell);
        }
    }
    /**
     * Check for overlap between rendered Markdown and the cell toolbar
     *
     * @param activeCell A rendered MarkdownCell
     * @returns `true` if the first line of the output overlaps with the cell toolbar, `false` otherwise
     */
    _markdownOverlapsToolbar(activeCell) {
        const markdownOutput = activeCell.inputArea; // Rendered markdown appears in the input area
        if (!markdownOutput) {
            return false;
        }
        // Get the rendered markdown as a widget.
        const markdownOutputWidget = markdownOutput.renderedInput;
        const markdownOutputElement = markdownOutputWidget.node;
        const firstOutputElementChild = markdownOutputElement.firstElementChild;
        if (firstOutputElementChild === null) {
            return false;
        }
        // Temporarily set the element's max width so that the bounding client rectangle only encompasses the content.
        const oldMaxWidth = firstOutputElementChild.style.maxWidth;
        firstOutputElementChild.style.maxWidth = 'max-content';
        const lineRight = firstOutputElementChild.getBoundingClientRect().right;
        // Reinstate the old max width.
        firstOutputElementChild.style.maxWidth = oldMaxWidth;
        const toolbarLeft = this._cellToolbarLeft(activeCell);
        return toolbarLeft === null ? false : lineRight > toolbarLeft;
    }
    _outputOverlapsToolbar(activeCell) {
        const outputArea = activeCell.outputArea.node;
        if (outputArea) {
            const outputs = outputArea.querySelectorAll('[data-mime-type]');
            const toolbarRect = this._cellToolbarRect(activeCell);
            if (toolbarRect) {
                const { left: toolbarLeft, bottom: toolbarBottom } = toolbarRect;
                return (0,index_es6_js_.some)(outputs, output => {
                    const node = output.firstElementChild;
                    if (node) {
                        const range = new Range();
                        if (TEXT_MIME_TYPES.includes(output.getAttribute('data-mime-type') || '')) {
                            // If the node is plain text, it's in a <pre>. To get the true bounding box of the
                            // text, the node contents need to be selected.
                            range.selectNodeContents(node);
                        }
                        else {
                            range.selectNode(node);
                        }
                        const { right: nodeRight, top: nodeTop } = range.getBoundingClientRect();
                        // Note: y-coordinate increases toward the bottom of page
                        return nodeRight > toolbarLeft && nodeTop < toolbarBottom;
                    }
                    return false;
                });
            }
        }
        return false;
    }
    _codeOverlapsToolbar(activeCell) {
        const editorWidget = activeCell.editorWidget;
        const editor = activeCell.editor;
        if (!editorWidget || !editor) {
            return false;
        }
        if (editor.lineCount < 1) {
            return false; // Nothing in the editor
        }
        const codeMirrorLines = editorWidget.node.getElementsByClassName('cm-line');
        if (codeMirrorLines.length < 1) {
            return false; // No lines present
        }
        let lineRight = codeMirrorLines[0].getBoundingClientRect().left;
        const range = document.createRange();
        range.selectNodeContents(codeMirrorLines[0]);
        lineRight += range.getBoundingClientRect().width;
        const toolbarLeft = this._cellToolbarLeft(activeCell);
        return toolbarLeft === null ? false : lineRight > toolbarLeft;
    }
    _cellEditorWidgetLeft(activeCell) {
        var _a, _b;
        return (_b = (_a = activeCell.editorWidget) === null || _a === void 0 ? void 0 : _a.node.getBoundingClientRect().left) !== null && _b !== void 0 ? _b : 0;
    }
    _cellEditorWidgetRight(activeCell) {
        var _a, _b;
        return (_b = (_a = activeCell.editorWidget) === null || _a === void 0 ? void 0 : _a.node.getBoundingClientRect().right) !== null && _b !== void 0 ? _b : 0;
    }
    _cellToolbarRect(activeCell) {
        const toolbarWidgets = this._findToolbarWidgets(activeCell);
        if (toolbarWidgets.length < 1) {
            return null;
        }
        const activeCellToolbar = toolbarWidgets[0].node;
        return activeCellToolbar.getBoundingClientRect();
    }
    _cellToolbarLeft(activeCell) {
        var _a;
        return ((_a = this._cellToolbarRect(activeCell)) === null || _a === void 0 ? void 0 : _a.left) || null;
    }
}
const defaultToolbarItems = [
    {
        command: 'notebook:duplicate-below',
        name: 'duplicate-cell'
    },
    {
        command: 'notebook:move-cell-up',
        name: 'move-cell-up'
    },
    {
        command: 'notebook:move-cell-down',
        name: 'move-cell-down'
    },
    {
        command: 'notebook:insert-cell-above',
        name: 'insert-cell-above'
    },
    {
        command: 'notebook:insert-cell-below',
        name: 'insert-cell-below'
    },
    {
        command: 'notebook:delete-cell',
        name: 'delete-cell'
    }
];
/**
 * Widget extension that creates a CellToolbarTracker each time a notebook is
 * created.
 */
class CellBarExtension {
    constructor(commands, toolbarFactory) {
        this._commands = commands;
        this._toolbarFactory = toolbarFactory !== null && toolbarFactory !== void 0 ? toolbarFactory : this.defaultToolbarFactory;
    }
    get defaultToolbarFactory() {
        const itemFactory = (0,index_js_.createDefaultFactory)(this._commands);
        return (widget) => new lib_index_js_.ObservableList({
            values: defaultToolbarItems.map(item => {
                return {
                    name: item.name,
                    widget: itemFactory(CellBarExtension.FACTORY_NAME, widget, item)
                };
            })
        });
    }
    createNew(panel) {
        return new CellToolbarTracker(panel, this._toolbarFactory(panel));
    }
}
CellBarExtension.FACTORY_NAME = 'Cell';


;// CONCATENATED MODULE: ../packages/cell-toolbar/lib/index.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module cell-toolbar
 */



/***/ })

}]);
//# sourceMappingURL=8097.b19e0bb9266aee22ffaa.js.map?v=b19e0bb9266aee22ffaa