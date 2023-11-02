"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[9134],{

/***/ 9134:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "commandEditItem": () => (/* binding */ commandEditItem),
  "default": () => (/* binding */ lib),
  "executionIndicator": () => (/* binding */ executionIndicator),
  "exportPlugin": () => (/* binding */ exportPlugin),
  "notebookTrustItem": () => (/* binding */ notebookTrustItem)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/application@~4.1.0-alpha.2 (singleton) (fallback: ../packages/application/lib/index.js)
var index_js_ = __webpack_require__(65681);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var lib_index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/cells@~4.1.0-alpha.2 (strict) (fallback: ../packages/cells/lib/index.js)
var cells_lib_index_js_ = __webpack_require__(51955);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/codeeditor@~4.1.0-alpha.2 (singleton) (fallback: ../packages/codeeditor/lib/index.js)
var codeeditor_lib_index_js_ = __webpack_require__(40200);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var coreutils_lib_index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/codemirror@~4.1.0-alpha.2 (singleton) (fallback: ../packages/codemirror/lib/index.js)
var codemirror_lib_index_js_ = __webpack_require__(29239);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/completer@~4.1.0-alpha.2 (singleton) (fallback: ../packages/completer/lib/index.js)
var completer_lib_index_js_ = __webpack_require__(4532);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/docmanager@~4.1.0-alpha.2 (singleton) (fallback: ../packages/docmanager/lib/index.js)
var docmanager_lib_index_js_ = __webpack_require__(7280);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/docmanager-extension@~4.1.0-alpha.2 (strict) (fallback: ../packages/docmanager-extension/lib/index.js)
var docmanager_extension_lib_index_js_ = __webpack_require__(68374);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/documentsearch@~4.1.0-alpha.2 (singleton) (fallback: ../packages/documentsearch/lib/index.js)
var documentsearch_lib_index_js_ = __webpack_require__(80599);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/filebrowser@~4.1.0-alpha.2 (singleton) (fallback: ../packages/filebrowser/lib/index.js)
var filebrowser_lib_index_js_ = __webpack_require__(35855);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/launcher@~4.1.0-alpha.2 (singleton) (fallback: ../packages/launcher/lib/index.js)
var launcher_lib_index_js_ = __webpack_require__(45534);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/lsp@~4.1.0-alpha.2 (singleton) (fallback: ../packages/lsp/lib/index.js)
var lsp_lib_index_js_ = __webpack_require__(84144);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/mainmenu@~4.1.0-alpha.2 (singleton) (fallback: ../packages/mainmenu/lib/index.js)
var mainmenu_lib_index_js_ = __webpack_require__(5184);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/metadataform@~4.1.0-alpha.2 (singleton) (fallback: ../packages/metadataform/lib/index.js)
var metadataform_lib_index_js_ = __webpack_require__(20321);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/notebook@~4.1.0-alpha.2 (singleton) (fallback: ../packages/notebook/lib/index.js)
var notebook_lib_index_js_ = __webpack_require__(56916);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/property-inspector@~4.1.0-alpha.2 (strict) (fallback: ../packages/property-inspector/lib/index.js)
var property_inspector_lib_index_js_ = __webpack_require__(28067);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/rendermime@~4.1.0-alpha.2 (singleton) (fallback: ../packages/rendermime/lib/index.js)
var rendermime_lib_index_js_ = __webpack_require__(66866);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/settingregistry@~4.1.0-alpha.2 (singleton) (fallback: ../packages/settingregistry/lib/index.js)
var settingregistry_lib_index_js_ = __webpack_require__(89397);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/statedb@~4.1.0-alpha.2 (singleton) (fallback: ../packages/statedb/lib/index.js)
var statedb_lib_index_js_ = __webpack_require__(1458);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/statusbar@~4.1.0-alpha.2 (singleton) (fallback: ../packages/statusbar/lib/index.js)
var statusbar_lib_index_js_ = __webpack_require__(34853);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/toc@~6.1.0-alpha.2 (singleton) (fallback: ../packages/toc/lib/index.js)
var toc_lib_index_js_ = __webpack_require__(95691);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(16415);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @lumino/disposable@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/disposable/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(78612);
// EXTERNAL MODULE: consume shared module (default) @lumino/messaging@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/messaging/dist/index.es6.js)
var messaging_dist_index_es6_js_ = __webpack_require__(85755);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var widgets_dist_index_es6_js_ = __webpack_require__(72234);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/logconsole@~4.1.0-alpha.2 (singleton) (fallback: ../packages/logconsole/lib/index.js)
var logconsole_lib_index_js_ = __webpack_require__(94908);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/services@~7.1.0-alpha.2 (singleton) (fallback: ../packages/services/lib/index.js)
var services_lib_index_js_ = __webpack_require__(43411);
;// CONCATENATED MODULE: ../packages/notebook-extension/lib/nboutput.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * The Log Console extension.
 */
const logNotebookOutput = {
    activate: activateNBOutput,
    id: '@jupyterlab/notebook-extension:log-output',
    description: 'Adds cell outputs log to the application logger.',
    requires: [notebook_lib_index_js_.INotebookTracker],
    optional: [logconsole_lib_index_js_.ILoggerRegistry],
    autoStart: true
};
function activateNBOutput(app, nbtracker, loggerRegistry) {
    if (!loggerRegistry) {
        // Automatically disable if logconsole is missing
        return;
    }
    function registerNB(nb) {
        function logOutput(msg, levelNormal, levelError) {
            if (services_lib_index_js_.KernelMessage.isDisplayDataMsg(msg) ||
                services_lib_index_js_.KernelMessage.isStreamMsg(msg) ||
                services_lib_index_js_.KernelMessage.isErrorMsg(msg) ||
                services_lib_index_js_.KernelMessage.isExecuteResultMsg(msg)) {
                const logger = loggerRegistry.getLogger(nb.context.path);
                logger.rendermime = nb.content.rendermime;
                const data = {
                    ...msg.content,
                    output_type: msg.header.msg_type
                };
                let level = levelNormal;
                if (services_lib_index_js_.KernelMessage.isErrorMsg(msg) ||
                    (services_lib_index_js_.KernelMessage.isStreamMsg(msg) && msg.content.name === 'stderr')) {
                    level = levelError;
                }
                logger.log({ type: 'output', data, level });
            }
        }
        // There is overlap here since unhandled messages are also emitted in the
        // iopubMessage signal. However, unhandled messages warrant a higher log
        // severity, so we'll accept that they are logged twice.
        nb.context.sessionContext.iopubMessage.connect((_, msg) => logOutput(msg, 'info', 'info'));
        nb.context.sessionContext.unhandledMessage.connect((_, msg) => logOutput(msg, 'warning', 'error'));
    }
    nbtracker.forEach(nb => registerNB(nb));
    nbtracker.widgetAdded.connect((_, nb) => registerNB(nb));
}

// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
var react_index_js_default = /*#__PURE__*/__webpack_require__.n(react_index_js_);
// EXTERNAL MODULE: consume shared module (default) @lumino/polling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/polling/dist/index.es6.js)
var polling_dist_index_es6_js_ = __webpack_require__(81967);
;// CONCATENATED MODULE: ../packages/notebook-extension/lib/tool-widgets/activeCellToolWidget.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */





/**
 * The class name added to the ActiveCellTool.
 */
const ACTIVE_CELL_TOOL_CLASS = 'jp-ActiveCellTool';
/**
 * The class name added to the ActiveCellTool content.
 */
const ACTIVE_CELL_TOOL_CONTENT_CLASS = 'jp-ActiveCellTool-Content';
/**
 * The class name added to the ActiveCellTool cell content.
 */
const ACTIVE_CELL_TOOL_CELL_CONTENT_CLASS = 'jp-ActiveCellTool-CellContent';
/**
 * The active cell field, displaying the first line and execution count of the active cell.
 *
 * ## Note
 * This field does not work as other metadata form fields, as it does not update metadata.
 */
class ActiveCellTool extends notebook_lib_index_js_.NotebookTools.Tool {
    constructor(options) {
        super();
        const { languages } = options;
        this._tracker = options.tracker;
        this.addClass(ACTIVE_CELL_TOOL_CLASS);
        this.layout = new widgets_dist_index_es6_js_.PanelLayout();
        this._inputPrompt = new cells_lib_index_js_.InputPrompt();
        this.layout.addWidget(this._inputPrompt);
        // First code line container
        const node = document.createElement('div');
        node.classList.add(ACTIVE_CELL_TOOL_CONTENT_CLASS);
        const container = node.appendChild(document.createElement('div'));
        const editor = container.appendChild(document.createElement('pre'));
        container.className = ACTIVE_CELL_TOOL_CELL_CONTENT_CLASS;
        this._editorEl = editor;
        this.layout.addWidget(new widgets_dist_index_es6_js_.Widget({ node }));
        const update = async () => {
            var _a, _b;
            this._editorEl.innerHTML = '';
            if (((_a = this._cellModel) === null || _a === void 0 ? void 0 : _a.type) === 'code') {
                this._inputPrompt.executionCount = `${(_b = this._cellModel.executionCount) !== null && _b !== void 0 ? _b : ''}`;
                this._inputPrompt.show();
            }
            else {
                this._inputPrompt.executionCount = null;
                this._inputPrompt.hide();
            }
            if (this._cellModel) {
                await languages.highlight(this._cellModel.sharedModel.getSource().split('\n')[0], languages.findByMIME(this._cellModel.mimeType), this._editorEl);
            }
        };
        this._refreshDebouncer = new polling_dist_index_es6_js_.Debouncer(update, 150);
    }
    render(props) {
        var _a, _b;
        const activeCell = this._tracker.activeCell;
        if (activeCell)
            this._cellModel = (activeCell === null || activeCell === void 0 ? void 0 : activeCell.model) || null;
        ((_a = this._cellModel) === null || _a === void 0 ? void 0 : _a.sharedModel).changed.connect(this.refresh, this);
        (_b = this._cellModel) === null || _b === void 0 ? void 0 : _b.mimeTypeChanged.connect(this.refresh, this);
        this.refresh()
            .then(() => undefined)
            .catch(() => undefined);
        return react_index_js_default().createElement("div", { ref: ref => ref === null || ref === void 0 ? void 0 : ref.appendChild(this.node) });
    }
    async refresh() {
        await this._refreshDebouncer.invoke();
    }
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/observables@~5.1.0-alpha.2 (strict) (fallback: ../packages/observables/lib/index.js)
var observables_lib_index_js_ = __webpack_require__(57090);
;// CONCATENATED MODULE: ../packages/notebook-extension/lib/tool-widgets/metadataEditorFields.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */



const CELL_METADATA_EDITOR_CLASS = 'jp-CellMetadataEditor';
const NOTEBOOK_METADATA_EDITOR_CLASS = 'jp-NotebookMetadataEditor';
/**
 * The cell metadata field.
 *
 * ## Note
 * This field does not work as other metadata form fields, as it does not use RJSF to update metadata.
 * It extends the MetadataEditorTool which updates itself the metadata.
 * It only renders the node of MetadataEditorTool in a React element instead of displaying a RJSF field.
 */
class CellMetadataField extends notebook_lib_index_js_.NotebookTools.MetadataEditorTool {
    constructor(options) {
        super(options);
        this._tracker = options.tracker;
        this.editor.editorHostNode.addEventListener('blur', this.editor, true);
        this.editor.editorHostNode.addEventListener('click', this.editor, true);
        this.editor.headerNode.addEventListener('click', this.editor);
    }
    _onSourceChanged() {
        var _a;
        if (this.editor.source) {
            (_a = this._tracker.activeCell) === null || _a === void 0 ? void 0 : _a.model.sharedModel.setMetadata(this.editor.source.toJSON());
        }
    }
    render(props) {
        var _a;
        const cell = this._tracker.activeCell;
        this.editor.source = cell
            ? new observables_lib_index_js_.ObservableJSON({ values: cell.model.metadata })
            : null;
        (_a = this.editor.source) === null || _a === void 0 ? void 0 : _a.changed.connect(this._onSourceChanged, this);
        return (react_index_js_default().createElement("div", { className: CELL_METADATA_EDITOR_CLASS },
            react_index_js_default().createElement("div", { ref: ref => ref === null || ref === void 0 ? void 0 : ref.appendChild(this.node) })));
    }
}
/**
 * The notebook metadata field.
 *
 * ## Note
 * This field does not work as other metadata form fields, as it does not use RJSF to update metadata.
 * It extends the MetadataEditorTool which updates itself the metadata.
 * It only renders the node of MetadataEditorTool in a React element instead of displaying a RJSF field.
 */
class NotebookMetadataField extends notebook_lib_index_js_.NotebookTools.MetadataEditorTool {
    constructor(options) {
        super(options);
        this._tracker = options.tracker;
        this.editor.editorHostNode.addEventListener('blur', this.editor, true);
        this.editor.editorHostNode.addEventListener('click', this.editor, true);
        this.editor.headerNode.addEventListener('click', this.editor);
    }
    _onSourceChanged() {
        var _a, _b;
        if (this.editor.source) {
            (_b = (_a = this._tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.sharedModel.setMetadata(this.editor.source.toJSON());
        }
    }
    render(props) {
        var _a, _b;
        const notebook = this._tracker.currentWidget;
        this.editor.source = notebook
            ? new observables_lib_index_js_.ObservableJSON({ values: (_a = notebook.model) === null || _a === void 0 ? void 0 : _a.metadata })
            : null;
        (_b = this.editor.source) === null || _b === void 0 ? void 0 : _b.changed.connect(this._onSourceChanged, this);
        return (react_index_js_default().createElement("div", { className: NOTEBOOK_METADATA_EDITOR_CLASS },
            react_index_js_default().createElement("div", { ref: ref => ref === null || ref === void 0 ? void 0 : ref.appendChild(this.node) })));
    }
}

;// CONCATENATED MODULE: ../packages/notebook-extension/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module notebook-extension
 */
































/**
 * The command IDs used by the notebook plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.createNew = 'notebook:create-new';
    CommandIDs.interrupt = 'notebook:interrupt-kernel';
    CommandIDs.restart = 'notebook:restart-kernel';
    CommandIDs.restartClear = 'notebook:restart-clear-output';
    CommandIDs.restartAndRunToSelected = 'notebook:restart-and-run-to-selected';
    CommandIDs.restartRunAll = 'notebook:restart-run-all';
    CommandIDs.reconnectToKernel = 'notebook:reconnect-to-kernel';
    CommandIDs.changeKernel = 'notebook:change-kernel';
    CommandIDs.getKernel = 'notebook:get-kernel';
    CommandIDs.createConsole = 'notebook:create-console';
    CommandIDs.createOutputView = 'notebook:create-output-view';
    CommandIDs.clearAllOutputs = 'notebook:clear-all-cell-outputs';
    CommandIDs.shutdown = 'notebook:shutdown-kernel';
    CommandIDs.closeAndShutdown = 'notebook:close-and-shutdown';
    CommandIDs.trust = 'notebook:trust';
    CommandIDs.exportToFormat = 'notebook:export-to-format';
    CommandIDs.run = 'notebook:run-cell';
    CommandIDs.runAndAdvance = 'notebook:run-cell-and-select-next';
    CommandIDs.runAndInsert = 'notebook:run-cell-and-insert-below';
    CommandIDs.runInConsole = 'notebook:run-in-console';
    CommandIDs.runAll = 'notebook:run-all-cells';
    CommandIDs.runAllAbove = 'notebook:run-all-above';
    CommandIDs.runAllBelow = 'notebook:run-all-below';
    CommandIDs.renderAllMarkdown = 'notebook:render-all-markdown';
    CommandIDs.toCode = 'notebook:change-cell-to-code';
    CommandIDs.toMarkdown = 'notebook:change-cell-to-markdown';
    CommandIDs.toRaw = 'notebook:change-cell-to-raw';
    CommandIDs.cut = 'notebook:cut-cell';
    CommandIDs.copy = 'notebook:copy-cell';
    CommandIDs.pasteAbove = 'notebook:paste-cell-above';
    CommandIDs.pasteBelow = 'notebook:paste-cell-below';
    CommandIDs.duplicateBelow = 'notebook:duplicate-below';
    CommandIDs.pasteAndReplace = 'notebook:paste-and-replace-cell';
    CommandIDs.moveUp = 'notebook:move-cell-up';
    CommandIDs.moveDown = 'notebook:move-cell-down';
    CommandIDs.clearOutputs = 'notebook:clear-cell-output';
    CommandIDs.deleteCell = 'notebook:delete-cell';
    CommandIDs.insertAbove = 'notebook:insert-cell-above';
    CommandIDs.insertBelow = 'notebook:insert-cell-below';
    CommandIDs.selectAbove = 'notebook:move-cursor-up';
    CommandIDs.selectBelow = 'notebook:move-cursor-down';
    CommandIDs.selectHeadingAboveOrCollapse = 'notebook:move-cursor-heading-above-or-collapse';
    CommandIDs.selectHeadingBelowOrExpand = 'notebook:move-cursor-heading-below-or-expand';
    CommandIDs.insertHeadingAbove = 'notebook:insert-heading-above';
    CommandIDs.insertHeadingBelow = 'notebook:insert-heading-below';
    CommandIDs.extendAbove = 'notebook:extend-marked-cells-above';
    CommandIDs.extendTop = 'notebook:extend-marked-cells-top';
    CommandIDs.extendBelow = 'notebook:extend-marked-cells-below';
    CommandIDs.extendBottom = 'notebook:extend-marked-cells-bottom';
    CommandIDs.selectAll = 'notebook:select-all';
    CommandIDs.deselectAll = 'notebook:deselect-all';
    CommandIDs.editMode = 'notebook:enter-edit-mode';
    CommandIDs.merge = 'notebook:merge-cells';
    CommandIDs.mergeAbove = 'notebook:merge-cell-above';
    CommandIDs.mergeBelow = 'notebook:merge-cell-below';
    CommandIDs.split = 'notebook:split-cell-at-cursor';
    CommandIDs.commandMode = 'notebook:enter-command-mode';
    CommandIDs.toggleAllLines = 'notebook:toggle-all-cell-line-numbers';
    CommandIDs.undoCellAction = 'notebook:undo-cell-action';
    CommandIDs.redoCellAction = 'notebook:redo-cell-action';
    CommandIDs.redo = 'notebook:redo';
    CommandIDs.undo = 'notebook:undo';
    CommandIDs.markdown1 = 'notebook:change-cell-to-heading-1';
    CommandIDs.markdown2 = 'notebook:change-cell-to-heading-2';
    CommandIDs.markdown3 = 'notebook:change-cell-to-heading-3';
    CommandIDs.markdown4 = 'notebook:change-cell-to-heading-4';
    CommandIDs.markdown5 = 'notebook:change-cell-to-heading-5';
    CommandIDs.markdown6 = 'notebook:change-cell-to-heading-6';
    CommandIDs.hideCode = 'notebook:hide-cell-code';
    CommandIDs.showCode = 'notebook:show-cell-code';
    CommandIDs.hideAllCode = 'notebook:hide-all-cell-code';
    CommandIDs.showAllCode = 'notebook:show-all-cell-code';
    CommandIDs.hideOutput = 'notebook:hide-cell-outputs';
    CommandIDs.showOutput = 'notebook:show-cell-outputs';
    CommandIDs.hideAllOutputs = 'notebook:hide-all-cell-outputs';
    CommandIDs.showAllOutputs = 'notebook:show-all-cell-outputs';
    CommandIDs.toggleRenderSideBySideCurrentNotebook = 'notebook:toggle-render-side-by-side-current';
    CommandIDs.setSideBySideRatio = 'notebook:set-side-by-side-ratio';
    CommandIDs.enableOutputScrolling = 'notebook:enable-output-scrolling';
    CommandIDs.disableOutputScrolling = 'notebook:disable-output-scrolling';
    CommandIDs.selectLastRunCell = 'notebook:select-last-run-cell';
    CommandIDs.replaceSelection = 'notebook:replace-selection';
    CommandIDs.autoClosingBrackets = 'notebook:toggle-autoclosing-brackets';
    CommandIDs.toggleCollapseCmd = 'notebook:toggle-heading-collapse';
    CommandIDs.collapseAllCmd = 'notebook:collapse-all-headings';
    CommandIDs.expandAllCmd = 'notebook:expand-all-headings';
    CommandIDs.copyToClipboard = 'notebook:copy-to-clipboard';
    CommandIDs.invokeCompleter = 'completer:invoke-notebook';
    CommandIDs.selectCompleter = 'completer:select-notebook';
    CommandIDs.tocRunCells = 'toc:run-cells';
})(CommandIDs || (CommandIDs = {}));
/**
 * The name of the factory that creates notebooks.
 */
const FACTORY = 'Notebook';
/**
 * The excluded Export To ...
 * (returned from nbconvert's export list)
 */
const FORMAT_EXCLUDE = ['notebook', 'python', 'custom'];
/**
 * Setting Id storing the customized toolbar definition.
 */
const PANEL_SETTINGS = '@jupyterlab/notebook-extension:panel';
/**
 * The id to use on the style tag for the side by side margins.
 */
const SIDE_BY_SIDE_STYLE_ID = 'jp-NotebookExtension-sideBySideMargins';
/**
 * The notebook widget tracker provider.
 */
const trackerPlugin = {
    id: '@jupyterlab/notebook-extension:tracker',
    description: 'Provides the notebook widget tracker.',
    provides: notebook_lib_index_js_.INotebookTracker,
    requires: [notebook_lib_index_js_.INotebookWidgetFactory, codemirror_lib_index_js_.IEditorExtensionRegistry],
    optional: [
        lib_index_js_.ICommandPalette,
        filebrowser_lib_index_js_.IDefaultFileBrowser,
        launcher_lib_index_js_.ILauncher,
        index_js_.ILayoutRestorer,
        mainmenu_lib_index_js_.IMainMenu,
        index_js_.IRouter,
        settingregistry_lib_index_js_.ISettingRegistry,
        lib_index_js_.ISessionContextDialogs,
        translation_lib_index_js_.ITranslator,
        ui_components_lib_index_js_.IFormRendererRegistry
    ],
    activate: activateNotebookHandler,
    autoStart: true
};
/**
 * The notebook cell factory provider.
 */
const factory = {
    id: '@jupyterlab/notebook-extension:factory',
    description: 'Provides the notebook cell factory.',
    provides: notebook_lib_index_js_.NotebookPanel.IContentFactory,
    requires: [codeeditor_lib_index_js_.IEditorServices],
    autoStart: true,
    activate: (app, editorServices) => {
        const editorFactory = editorServices.factoryService.newInlineEditor;
        return new notebook_lib_index_js_.NotebookPanel.ContentFactory({ editorFactory });
    }
};
/**
 * The notebook tools extension.
 */
const tools = {
    activate: activateNotebookTools,
    provides: notebook_lib_index_js_.INotebookTools,
    id: '@jupyterlab/notebook-extension:tools',
    description: 'Provides the notebook tools.',
    autoStart: true,
    requires: [
        notebook_lib_index_js_.INotebookTracker,
        codeeditor_lib_index_js_.IEditorServices,
        codemirror_lib_index_js_.IEditorLanguageRegistry,
        statedb_lib_index_js_.IStateDB,
        translation_lib_index_js_.ITranslator
    ],
    optional: [property_inspector_lib_index_js_.IPropertyInspectorProvider]
};
/**
 * A plugin providing a CommandEdit status item.
 */
const commandEditItem = {
    id: '@jupyterlab/notebook-extension:mode-status',
    description: 'Adds a notebook mode status widget.',
    autoStart: true,
    requires: [notebook_lib_index_js_.INotebookTracker, translation_lib_index_js_.ITranslator],
    optional: [statusbar_lib_index_js_.IStatusBar],
    activate: (app, tracker, translator, statusBar) => {
        if (!statusBar) {
            // Automatically disable if statusbar missing
            return;
        }
        const { shell } = app;
        const item = new notebook_lib_index_js_.CommandEditStatus(translator);
        // Keep the status item up-to-date with the current notebook.
        tracker.currentChanged.connect(() => {
            const current = tracker.currentWidget;
            item.model.notebook = current && current.content;
        });
        statusBar.registerStatusItem('@jupyterlab/notebook-extension:mode-status', {
            item,
            align: 'right',
            rank: 4,
            isActive: () => !!shell.currentWidget &&
                !!tracker.currentWidget &&
                shell.currentWidget === tracker.currentWidget
        });
    }
};
/**
 * A plugin that provides a execution indicator item to the status bar.
 */
const executionIndicator = {
    id: '@jupyterlab/notebook-extension:execution-indicator',
    description: 'Adds a notebook execution status widget.',
    autoStart: true,
    requires: [notebook_lib_index_js_.INotebookTracker, index_js_.ILabShell, translation_lib_index_js_.ITranslator],
    optional: [statusbar_lib_index_js_.IStatusBar, settingregistry_lib_index_js_.ISettingRegistry],
    activate: (app, notebookTracker, labShell, translator, statusBar, settingRegistry) => {
        let statusbarItem;
        let labShellCurrentChanged;
        let statusBarDisposable;
        const updateSettings = (settings) => {
            var _a, _b;
            let { showOnToolBar, showProgress } = settings;
            if (!showOnToolBar) {
                // Status bar mode, only one `ExecutionIndicator` is needed.
                if (!statusBar) {
                    // Automatically disable if statusbar missing
                    return;
                }
                if (!(statusbarItem === null || statusbarItem === void 0 ? void 0 : statusbarItem.model)) {
                    statusbarItem = new notebook_lib_index_js_.ExecutionIndicator(translator);
                    labShellCurrentChanged = (_, change) => {
                        const { newValue } = change;
                        if (newValue && notebookTracker.has(newValue)) {
                            const panel = newValue;
                            statusbarItem.model.attachNotebook({
                                content: panel.content,
                                context: panel.sessionContext
                            });
                        }
                    };
                    statusBarDisposable = statusBar.registerStatusItem('@jupyterlab/notebook-extension:execution-indicator', {
                        item: statusbarItem,
                        align: 'left',
                        rank: 3,
                        isActive: () => {
                            const current = labShell.currentWidget;
                            return !!current && notebookTracker.has(current);
                        }
                    });
                    statusbarItem.model.attachNotebook({
                        content: (_a = notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content,
                        context: (_b = notebookTracker.currentWidget) === null || _b === void 0 ? void 0 : _b.sessionContext
                    });
                    labShell.currentChanged.connect(labShellCurrentChanged);
                    statusbarItem.disposed.connect(() => {
                        labShell.currentChanged.disconnect(labShellCurrentChanged);
                    });
                }
                statusbarItem.model.displayOption = {
                    showOnToolBar,
                    showProgress
                };
            }
            else {
                //Remove old indicator widget on status bar
                if (statusBarDisposable) {
                    labShell.currentChanged.disconnect(labShellCurrentChanged);
                    statusBarDisposable.dispose();
                }
            }
        };
        if (settingRegistry) {
            // Indicator is default in tool bar, user needs to specify its
            // position in settings in order to have indicator on status bar.
            const loadSettings = settingRegistry.load(trackerPlugin.id);
            Promise.all([loadSettings, app.restored])
                .then(([settings]) => {
                updateSettings(notebook_lib_index_js_.ExecutionIndicator.getSettingValue(settings));
                settings.changed.connect(sender => updateSettings(notebook_lib_index_js_.ExecutionIndicator.getSettingValue(sender)));
            })
                .catch((reason) => {
                console.error(reason.message);
            });
        }
    }
};
/**
 * A plugin providing export commands in the main menu and command palette
 */
const exportPlugin = {
    id: '@jupyterlab/notebook-extension:export',
    description: 'Adds the export notebook commands.',
    autoStart: true,
    requires: [translation_lib_index_js_.ITranslator, notebook_lib_index_js_.INotebookTracker],
    optional: [mainmenu_lib_index_js_.IMainMenu, lib_index_js_.ICommandPalette],
    activate: (app, translator, tracker, mainMenu, palette) => {
        var _a;
        const trans = translator.load('jupyterlab');
        const { commands, shell } = app;
        const services = app.serviceManager;
        const isEnabled = () => {
            return Private.isEnabled(shell, tracker);
        };
        commands.addCommand(CommandIDs.exportToFormat, {
            label: args => {
                if (args.label === undefined) {
                    return trans.__('Save and Export Notebook to the given `format`.');
                }
                const formatLabel = args['label'];
                return args['isPalette']
                    ? trans.__('Save and Export Notebook: %1', formatLabel)
                    : formatLabel;
            },
            execute: args => {
                const current = getCurrent(tracker, shell, args);
                if (!current) {
                    return;
                }
                const url = coreutils_lib_index_js_.PageConfig.getNBConvertURL({
                    format: args['format'],
                    download: true,
                    path: current.context.path
                });
                const { context } = current;
                if (context.model.dirty && !context.model.readOnly) {
                    return context.save().then(() => {
                        window.open(url, '_blank', 'noopener');
                    });
                }
                return new Promise(resolve => {
                    window.open(url, '_blank', 'noopener');
                    resolve(undefined);
                });
            },
            isEnabled
        });
        // Add a notebook group to the File menu.
        let exportTo;
        if (mainMenu) {
            exportTo = (_a = mainMenu.fileMenu.items.find(item => {
                var _a;
                return item.type === 'submenu' &&
                    ((_a = item.submenu) === null || _a === void 0 ? void 0 : _a.id) === 'jp-mainmenu-file-notebookexport';
            })) === null || _a === void 0 ? void 0 : _a.submenu;
        }
        let formatsInitialized = false;
        /** Request formats only when a notebook might use them. */
        const maybeInitializeFormats = async () => {
            if (formatsInitialized) {
                return;
            }
            tracker.widgetAdded.disconnect(maybeInitializeFormats);
            formatsInitialized = true;
            const response = await services.nbconvert.getExportFormats(false);
            if (!response) {
                return;
            }
            const formatLabels = Private.getFormatLabels(translator);
            // Convert export list to palette and menu items.
            const formatList = Object.keys(response);
            formatList.forEach(function (key) {
                const capCaseKey = trans.__(key[0].toUpperCase() + key.substr(1));
                const labelStr = formatLabels[key] ? formatLabels[key] : capCaseKey;
                let args = {
                    format: key,
                    label: labelStr,
                    isPalette: false
                };
                if (FORMAT_EXCLUDE.indexOf(key) === -1) {
                    if (exportTo) {
                        exportTo.addItem({
                            command: CommandIDs.exportToFormat,
                            args: args
                        });
                    }
                    if (palette) {
                        args = {
                            format: key,
                            label: labelStr,
                            isPalette: true
                        };
                        const category = trans.__('Notebook Operations');
                        palette.addItem({
                            command: CommandIDs.exportToFormat,
                            category,
                            args
                        });
                    }
                }
            });
        };
        tracker.widgetAdded.connect(maybeInitializeFormats);
    }
};
/**
 * A plugin that adds a notebook trust status item to the status bar.
 */
const notebookTrustItem = {
    id: '@jupyterlab/notebook-extension:trust-status',
    description: 'Adds the notebook trusted status widget.',
    autoStart: true,
    requires: [notebook_lib_index_js_.INotebookTracker, translation_lib_index_js_.ITranslator],
    optional: [statusbar_lib_index_js_.IStatusBar],
    activate: (app, tracker, tranlator, statusBar) => {
        if (!statusBar) {
            // Automatically disable if statusbar missing
            return;
        }
        const { shell } = app;
        const item = new notebook_lib_index_js_.NotebookTrustStatus(tranlator);
        // Keep the status item up-to-date with the current notebook.
        tracker.currentChanged.connect(() => {
            const current = tracker.currentWidget;
            item.model.notebook = current && current.content;
        });
        statusBar.registerStatusItem('@jupyterlab/notebook-extension:trust-status', {
            item,
            align: 'right',
            rank: 3,
            isActive: () => !!shell.currentWidget &&
                !!tracker.currentWidget &&
                shell.currentWidget === tracker.currentWidget
        });
    }
};
/**
 * The notebook widget factory provider.
 */
const widgetFactoryPlugin = {
    id: '@jupyterlab/notebook-extension:widget-factory',
    description: 'Provides the notebook widget factory.',
    provides: notebook_lib_index_js_.INotebookWidgetFactory,
    requires: [
        notebook_lib_index_js_.NotebookPanel.IContentFactory,
        codeeditor_lib_index_js_.IEditorServices,
        rendermime_lib_index_js_.IRenderMimeRegistry,
        lib_index_js_.IToolbarWidgetRegistry
    ],
    optional: [settingregistry_lib_index_js_.ISettingRegistry, lib_index_js_.ISessionContextDialogs, translation_lib_index_js_.ITranslator],
    activate: activateWidgetFactory,
    autoStart: true
};
/**
 * The cloned output provider.
 */
const clonedOutputsPlugin = {
    id: '@jupyterlab/notebook-extension:cloned-outputs',
    description: 'Adds the clone output feature.',
    requires: [docmanager_lib_index_js_.IDocumentManager, notebook_lib_index_js_.INotebookTracker, translation_lib_index_js_.ITranslator],
    optional: [index_js_.ILayoutRestorer],
    activate: activateClonedOutputs,
    autoStart: true
};
/**
 * A plugin for code consoles functionalities.
 */
const codeConsolePlugin = {
    id: '@jupyterlab/notebook-extension:code-console',
    description: 'Adds the notebook code consoles features.',
    requires: [notebook_lib_index_js_.INotebookTracker, translation_lib_index_js_.ITranslator],
    activate: activateCodeConsole,
    autoStart: true
};
/**
 * A plugin to copy CodeCell outputs.
 */
const copyOutputPlugin = {
    id: '@jupyterlab/notebook-extension:copy-output',
    description: 'Adds the copy cell outputs feature.',
    activate: activateCopyOutput,
    requires: [translation_lib_index_js_.ITranslator, notebook_lib_index_js_.INotebookTracker],
    autoStart: true
};
/**
 * Kernel status indicator.
 */
const kernelStatus = {
    id: '@jupyterlab/notebook-extension:kernel-status',
    description: 'Adds the notebook kernel status.',
    activate: (app, tracker, kernelStatus) => {
        const provider = (widget) => {
            let session = null;
            if (widget && tracker.has(widget)) {
                return widget.sessionContext;
            }
            return session;
        };
        kernelStatus.addSessionProvider(provider);
    },
    requires: [notebook_lib_index_js_.INotebookTracker, lib_index_js_.IKernelStatusModel],
    autoStart: true
};
/**
 * Cursor position.
 */
const lineColStatus = {
    id: '@jupyterlab/notebook-extension:cursor-position',
    description: 'Adds the notebook cursor position status.',
    activate: (app, tracker, positionModel) => {
        let previousWidget = null;
        const provider = async (widget) => {
            let editor = null;
            if (widget !== previousWidget) {
                previousWidget === null || previousWidget === void 0 ? void 0 : previousWidget.content.activeCellChanged.disconnect(positionModel.update);
                previousWidget = null;
                if (widget && tracker.has(widget)) {
                    widget.content.activeCellChanged.connect(positionModel.update);
                    const activeCell = widget.content.activeCell;
                    editor = null;
                    if (activeCell) {
                        await activeCell.ready;
                        editor = activeCell.editor;
                    }
                    previousWidget = widget;
                }
            }
            else if (widget) {
                const activeCell = widget.content.activeCell;
                editor = null;
                if (activeCell) {
                    await activeCell.ready;
                    editor = activeCell.editor;
                }
            }
            return editor;
        };
        positionModel.addEditorProvider(provider);
    },
    requires: [notebook_lib_index_js_.INotebookTracker, codeeditor_lib_index_js_.IPositionModel],
    autoStart: true
};
const completerPlugin = {
    id: '@jupyterlab/notebook-extension:completer',
    description: 'Adds the code completion capability to notebooks.',
    requires: [notebook_lib_index_js_.INotebookTracker],
    optional: [completer_lib_index_js_.ICompletionProviderManager, translation_lib_index_js_.ITranslator, lib_index_js_.ISanitizer],
    activate: activateNotebookCompleterService,
    autoStart: true
};
/**
 * A plugin to search notebook documents
 */
const searchProvider = {
    id: '@jupyterlab/notebook-extension:search',
    description: 'Adds search capability to notebooks.',
    requires: [documentsearch_lib_index_js_.ISearchProviderRegistry],
    autoStart: true,
    activate: (app, registry) => {
        registry.add('jp-notebookSearchProvider', notebook_lib_index_js_.NotebookSearchProvider);
    }
};
const tocPlugin = {
    id: '@jupyterlab/notebook-extension:toc',
    description: 'Adds table of content capability to the notebooks',
    requires: [notebook_lib_index_js_.INotebookTracker, toc_lib_index_js_.ITableOfContentsRegistry, lib_index_js_.ISanitizer],
    optional: [rendermime_lib_index_js_.IMarkdownParser],
    autoStart: true,
    activate: (app, tracker, tocRegistry, sanitizer, mdParser) => {
        tocRegistry.add(new notebook_lib_index_js_.NotebookToCFactory(tracker, mdParser, sanitizer));
    }
};
const languageServerPlugin = {
    id: '@jupyterlab/notebook-extension:language-server',
    description: 'Adds language server capability to the notebooks.',
    requires: [
        notebook_lib_index_js_.INotebookTracker,
        lsp_lib_index_js_.ILSPDocumentConnectionManager,
        lsp_lib_index_js_.ILSPFeatureManager,
        lsp_lib_index_js_.ILSPCodeExtractorsManager,
        lsp_lib_index_js_.IWidgetLSPAdapterTracker
    ],
    activate: activateNotebookLanguageServer,
    autoStart: true
};
/**
 * Metadata editor for the raw cell mimetype.
 */
const updateRawMimetype = {
    id: '@jupyterlab/notebook-extension:update-raw-mimetype',
    description: 'Adds metadata form editor for raw cell mimetype.',
    autoStart: true,
    requires: [notebook_lib_index_js_.INotebookTracker, metadataform_lib_index_js_.IMetadataFormProvider, translation_lib_index_js_.ITranslator],
    activate: (app, tracker, metadataForms, translator) => {
        const trans = translator.load('jupyterlab');
        let formatsInitialized = false;
        async function maybeInitializeFormats() {
            if (formatsInitialized) {
                return;
            }
            if (!metadataForms.get('commonToolsSection')) {
                return;
            }
            const properties = metadataForms
                .get('commonToolsSection')
                .getProperties('/raw_mimetype');
            if (!properties) {
                return;
            }
            tracker.widgetAdded.disconnect(maybeInitializeFormats);
            formatsInitialized = true;
            const services = app.serviceManager;
            const response = await services.nbconvert.getExportFormats(false);
            if (!response) {
                return;
            }
            // convert exportList to palette and menu items
            const formatList = Object.keys(response);
            const formatLabels = Private.getFormatLabels(translator);
            formatList.forEach(function (key) {
                var _a;
                const mimetypeExists = ((_a = properties.oneOf) === null || _a === void 0 ? void 0 : _a.filter(value => value.const === key).length) > 0;
                if (!mimetypeExists) {
                    const altOption = trans.__(key[0].toUpperCase() + key.substr(1));
                    const option = formatLabels[key] ? formatLabels[key] : altOption;
                    const mimeTypeValue = response[key].output_mimetype;
                    properties.oneOf.push({
                        const: mimeTypeValue,
                        title: option
                    });
                }
            });
            metadataForms
                .get('commonToolsSection')
                .setProperties('/raw_mimetype', properties);
        }
        tracker.widgetAdded.connect(maybeInitializeFormats);
    }
};
/**
 * Registering metadata editor fields.
 */
const customMetadataEditorFields = {
    id: '@jupyterlab/notebook-extension:metadata-editor',
    description: 'Adds metadata form for full metadata editor.',
    autoStart: true,
    requires: [notebook_lib_index_js_.INotebookTracker, codeeditor_lib_index_js_.IEditorServices, ui_components_lib_index_js_.IFormRendererRegistry],
    optional: [translation_lib_index_js_.ITranslator],
    activate: (app, tracker, editorServices, formRegistry, translator) => {
        const editorFactory = options => editorServices.factoryService.newInlineEditor(options);
        // Register the custom fields.
        const cellComponent = {
            fieldRenderer: (props) => {
                return new CellMetadataField({
                    editorFactory,
                    tracker,
                    label: 'Cell metadata',
                    translator: translator
                }).render(props);
            }
        };
        formRegistry.addRenderer('@jupyterlab/notebook-extension:metadata-editor.cell-metadata', cellComponent);
        const notebookComponent = {
            fieldRenderer: (props) => {
                return new NotebookMetadataField({
                    editorFactory,
                    tracker,
                    label: 'Notebook metadata',
                    translator: translator
                }).render(props);
            }
        };
        formRegistry.addRenderer('@jupyterlab/notebook-extension:metadata-editor.notebook-metadata', notebookComponent);
    }
};
/**
 * Registering active cell field.
 */
const activeCellTool = {
    id: '@jupyterlab/notebook-extension:active-cell-tool',
    description: 'Adds active cell field in the metadata editor tab.',
    autoStart: true,
    requires: [notebook_lib_index_js_.INotebookTracker, ui_components_lib_index_js_.IFormRendererRegistry, codemirror_lib_index_js_.IEditorLanguageRegistry],
    activate: (
    // Register the custom field.
    app, tracker, formRegistry, languages) => {
        const component = {
            fieldRenderer: (props) => {
                return new ActiveCellTool({
                    tracker,
                    languages
                }).render(props);
            }
        };
        formRegistry.addRenderer('@jupyterlab/notebook-extension:active-cell-tool.renderer', component);
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [
    factory,
    trackerPlugin,
    executionIndicator,
    exportPlugin,
    tools,
    commandEditItem,
    notebookTrustItem,
    widgetFactoryPlugin,
    logNotebookOutput,
    clonedOutputsPlugin,
    codeConsolePlugin,
    copyOutputPlugin,
    kernelStatus,
    lineColStatus,
    completerPlugin,
    searchProvider,
    tocPlugin,
    languageServerPlugin,
    updateRawMimetype,
    customMetadataEditorFields,
    activeCellTool
];
/* harmony default export */ const lib = (plugins);
/**
 * Activate the notebook tools extension.
 */
function activateNotebookTools(app, tracker, editorServices, languages, state, translator, inspectorProvider) {
    const trans = translator.load('jupyterlab');
    const id = 'notebook-tools';
    const notebookTools = new notebook_lib_index_js_.NotebookTools({ tracker, translator });
    // Create message hook for triggers to save to the database.
    const hook = (sender, message) => {
        switch (message.type) {
            case 'activate-request':
                void state.save(id, { open: true });
                break;
            case 'after-hide':
            case 'close-request':
                void state.remove(id);
                break;
            default:
                break;
        }
        return true;
    };
    notebookTools.title.icon = ui_components_lib_index_js_.buildIcon;
    notebookTools.title.caption = trans.__('Notebook Tools');
    notebookTools.id = id;
    messaging_dist_index_es6_js_.MessageLoop.installMessageHook(notebookTools, hook);
    if (inspectorProvider) {
        tracker.widgetAdded.connect((sender, panel) => {
            const inspector = inspectorProvider.register(panel);
            inspector.render(notebookTools);
        });
    }
    return notebookTools;
}
/**
 * Activate the notebook widget factory.
 */
function activateWidgetFactory(app, contentFactory, editorServices, rendermime, toolbarRegistry, settingRegistry, sessionContextDialogs_, translator_) {
    const translator = translator_ !== null && translator_ !== void 0 ? translator_ : translation_lib_index_js_.nullTranslator;
    const sessionContextDialogs = sessionContextDialogs_ !== null && sessionContextDialogs_ !== void 0 ? sessionContextDialogs_ : new lib_index_js_.SessionContextDialogs({ translator });
    const preferKernelOption = coreutils_lib_index_js_.PageConfig.getOption('notebookStartsKernel');
    // If the option is not set, assume `true`
    const preferKernelValue = preferKernelOption === '' || preferKernelOption.toLowerCase() === 'true';
    const { commands } = app;
    let toolbarFactory;
    // Register notebook toolbar widgets
    toolbarRegistry.addFactory(FACTORY, 'save', panel => docmanager_extension_lib_index_js_.ToolbarItems.createSaveButton(commands, panel.context.fileChanged));
    toolbarRegistry.addFactory(FACTORY, 'cellType', panel => notebook_lib_index_js_.ToolbarItems.createCellTypeItem(panel, translator));
    toolbarRegistry.addFactory(FACTORY, 'kernelName', panel => lib_index_js_.Toolbar.createKernelNameItem(panel.sessionContext, sessionContextDialogs, translator));
    toolbarRegistry.addFactory(FACTORY, 'executionProgress', panel => {
        const loadingSettings = settingRegistry === null || settingRegistry === void 0 ? void 0 : settingRegistry.load(trackerPlugin.id);
        const indicator = notebook_lib_index_js_.ExecutionIndicator.createExecutionIndicatorItem(panel, translator, loadingSettings);
        void (loadingSettings === null || loadingSettings === void 0 ? void 0 : loadingSettings.then(settings => {
            panel.disposed.connect(() => {
                settings.dispose();
            });
        }));
        return indicator;
    });
    if (settingRegistry) {
        // Create the factory
        toolbarFactory = (0,lib_index_js_.createToolbarFactory)(toolbarRegistry, settingRegistry, FACTORY, PANEL_SETTINGS, translator);
    }
    const trans = translator.load('jupyterlab');
    const factory = new notebook_lib_index_js_.NotebookWidgetFactory({
        name: FACTORY,
        label: trans.__('Notebook'),
        fileTypes: ['notebook'],
        modelName: 'notebook',
        defaultFor: ['notebook'],
        preferKernel: preferKernelValue,
        canStartKernel: true,
        rendermime,
        contentFactory,
        editorConfig: notebook_lib_index_js_.StaticNotebook.defaultEditorConfig,
        notebookConfig: notebook_lib_index_js_.StaticNotebook.defaultNotebookConfig,
        mimeTypeService: editorServices.mimeTypeService,
        toolbarFactory,
        translator
    });
    app.docRegistry.addWidgetFactory(factory);
    return factory;
}
/**
 * Activate the plugin to create and track cloned outputs.
 */
function activateClonedOutputs(app, docManager, notebookTracker, translator, restorer) {
    const trans = translator.load('jupyterlab');
    const clonedOutputs = new lib_index_js_.WidgetTracker({
        namespace: 'cloned-outputs'
    });
    if (restorer) {
        void restorer.restore(clonedOutputs, {
            command: CommandIDs.createOutputView,
            args: widget => ({
                path: widget.content.path,
                index: widget.content.index
            }),
            name: widget => `${widget.content.path}:${widget.content.index}`,
            when: notebookTracker.restored // After the notebook widgets (but not contents).
        });
    }
    const { commands, shell } = app;
    const isEnabledAndSingleSelected = () => {
        return Private.isEnabledAndSingleSelected(shell, notebookTracker);
    };
    commands.addCommand(CommandIDs.createOutputView, {
        label: trans.__('Create New View for Cell Output'),
        execute: async (args) => {
            var _a;
            let cell;
            let current;
            // If we are given a notebook path and cell index, then
            // use that, otherwise use the current active cell.
            const path = args.path;
            let index = args.index;
            if (path && index !== undefined && index !== null) {
                current = docManager.findWidget(path, FACTORY);
                if (!current) {
                    return;
                }
            }
            else {
                current = notebookTracker.currentWidget;
                if (!current) {
                    return;
                }
                cell = current.content.activeCell;
                index = current.content.activeCellIndex;
            }
            // Create a MainAreaWidget
            const content = new Private.ClonedOutputArea({
                notebook: current,
                cell,
                index,
                translator
            });
            const widget = new lib_index_js_.MainAreaWidget({ content });
            current.context.addSibling(widget, {
                ref: current.id,
                mode: 'split-bottom',
                type: 'Cloned Output'
            });
            const updateCloned = () => {
                void clonedOutputs.save(widget);
            };
            current.context.pathChanged.connect(updateCloned);
            (_a = current.context.model) === null || _a === void 0 ? void 0 : _a.cells.changed.connect(updateCloned);
            // Add the cloned output to the output widget tracker.
            void clonedOutputs.add(widget);
            // Remove the output view if the parent notebook is closed.
            current.content.disposed.connect(() => {
                var _a;
                current.context.pathChanged.disconnect(updateCloned);
                (_a = current.context.model) === null || _a === void 0 ? void 0 : _a.cells.changed.disconnect(updateCloned);
                widget.dispose();
            });
        },
        isEnabled: isEnabledAndSingleSelected
    });
}
/**
 * Activate the plugin to add code console functionalities
 */
function activateCodeConsole(app, tracker, translator) {
    const trans = translator.load('jupyterlab');
    const { commands, shell } = app;
    const isEnabled = () => Private.isEnabled(shell, tracker);
    commands.addCommand(CommandIDs.createConsole, {
        label: trans.__('New Console for Notebook'),
        execute: args => {
            const current = tracker.currentWidget;
            if (!current) {
                return;
            }
            return Private.createConsole(commands, current, args['activate']);
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.runInConsole, {
        label: trans.__('Run Selected Text or Current Line in Console'),
        execute: async (args) => {
            var _a, _b;
            // Default to not activating the notebook (thereby putting the notebook
            // into command mode)
            const current = tracker.currentWidget;
            if (!current) {
                return;
            }
            const { context, content } = current;
            const cell = content.activeCell;
            const metadata = cell === null || cell === void 0 ? void 0 : cell.model.metadata;
            const path = context.path;
            // ignore action in non-code cell
            if (!cell || cell.model.type !== 'code') {
                return;
            }
            let code;
            const editor = cell.editor;
            if (!editor) {
                return;
            }
            const selection = editor.getSelection();
            const { start, end } = selection;
            const selected = start.column !== end.column || start.line !== end.line;
            if (selected) {
                // Get the selected code from the editor.
                const start = editor.getOffsetAt(selection.start);
                const end = editor.getOffsetAt(selection.end);
                code = editor.model.sharedModel.getSource().substring(start, end);
            }
            else {
                // no selection, find the complete statement around the current line
                const cursor = editor.getCursorPosition();
                const srcLines = editor.model.sharedModel.getSource().split('\n');
                let curLine = selection.start.line;
                while (curLine < editor.lineCount &&
                    !srcLines[curLine].replace(/\s/g, '').length) {
                    curLine += 1;
                }
                // if curLine > 0, we first do a search from beginning
                let fromFirst = curLine > 0;
                let firstLine = 0;
                let lastLine = firstLine + 1;
                // eslint-disable-next-line
                while (true) {
                    code = srcLines.slice(firstLine, lastLine).join('\n');
                    const reply = await ((_b = (_a = current.context.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel) === null || _b === void 0 ? void 0 : _b.requestIsComplete({
                        // ipython needs an empty line at the end to correctly identify completeness of indented code
                        code: code + '\n\n'
                    }));
                    if ((reply === null || reply === void 0 ? void 0 : reply.content.status) === 'complete') {
                        if (curLine < lastLine) {
                            // we find a block of complete statement containing the current line, great!
                            while (lastLine < editor.lineCount &&
                                !srcLines[lastLine].replace(/\s/g, '').length) {
                                lastLine += 1;
                            }
                            editor.setCursorPosition({
                                line: lastLine,
                                column: cursor.column
                            });
                            break;
                        }
                        else {
                            // discard the complete statement before the current line and continue
                            firstLine = lastLine;
                            lastLine = firstLine + 1;
                        }
                    }
                    else if (lastLine < editor.lineCount) {
                        // if incomplete and there are more lines, add the line and check again
                        lastLine += 1;
                    }
                    else if (fromFirst) {
                        // we search from the first line and failed, we search again from current line
                        firstLine = curLine;
                        lastLine = curLine + 1;
                        fromFirst = false;
                    }
                    else {
                        // if we have searched both from first line and from current line and we
                        // cannot find anything, we submit the current line.
                        code = srcLines[curLine];
                        while (curLine + 1 < editor.lineCount &&
                            !srcLines[curLine + 1].replace(/\s/g, '').length) {
                            curLine += 1;
                        }
                        editor.setCursorPosition({
                            line: curLine + 1,
                            column: cursor.column
                        });
                        break;
                    }
                }
            }
            if (!code) {
                return;
            }
            await commands.execute('console:open', {
                activate: false,
                insertMode: 'split-bottom',
                path
            });
            await commands.execute('console:inject', {
                activate: false,
                code,
                path,
                metadata
            });
        },
        isEnabled
    });
}
/**
 * Activate the output copying extension
 */
function activateCopyOutput(app, translator, tracker) {
    const trans = translator.load('jupyterlab');
    /**
     * Copy the contents of an HTMLElement to the system clipboard
     */
    function copyElement(e) {
        const sel = window.getSelection();
        if (sel == null) {
            return;
        }
        // Save the current selection.
        const savedRanges = [];
        for (let i = 0; i < sel.rangeCount; ++i) {
            savedRanges[i] = sel.getRangeAt(i).cloneRange();
        }
        const range = document.createRange();
        range.selectNodeContents(e);
        sel.removeAllRanges();
        sel.addRange(range);
        document.execCommand('copy');
        // Restore the saved selection.
        sel.removeAllRanges();
        savedRanges.forEach(r => sel.addRange(r));
    }
    app.commands.addCommand(CommandIDs.copyToClipboard, {
        label: trans.__('Copy Output to Clipboard'),
        execute: args => {
            var _a;
            const cell = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.activeCell;
            if (cell == null) {
                return;
            }
            const output = cell.outputArea.outputTracker.currentWidget;
            if (output == null) {
                return;
            }
            const outputAreaAreas = output.node.getElementsByClassName('jp-OutputArea-output');
            if (outputAreaAreas.length > 0) {
                const area = outputAreaAreas[0];
                copyElement(area);
            }
        }
    });
    app.contextMenu.addItem({
        command: CommandIDs.copyToClipboard,
        selector: '.jp-OutputArea-child',
        rank: 0
    });
}
/**
 * Activate the notebook handler extension.
 */
function activateNotebookHandler(app, factory, extensions, palette, defaultBrowser, launcher, restorer, mainMenu, router, settingRegistry, sessionDialogs_, translator_, formRegistry) {
    const translator = translator_ !== null && translator_ !== void 0 ? translator_ : translation_lib_index_js_.nullTranslator;
    const sessionDialogs = sessionDialogs_ !== null && sessionDialogs_ !== void 0 ? sessionDialogs_ : new lib_index_js_.SessionContextDialogs({ translator });
    const trans = translator.load('jupyterlab');
    const services = app.serviceManager;
    const { commands, shell } = app;
    const tracker = new notebook_lib_index_js_.NotebookTracker({ namespace: 'notebook' });
    // Use the router to deal with hash navigation
    function onRouted(router, location) {
        if (location.hash && tracker.currentWidget) {
            tracker.currentWidget.setFragment(location.hash);
        }
    }
    router === null || router === void 0 ? void 0 : router.routed.connect(onRouted);
    const isEnabled = () => {
        return Private.isEnabled(shell, tracker);
    };
    const setSideBySideOutputRatio = (sideBySideOutputRatio) => document.documentElement.style.setProperty('--jp-side-by-side-output-size', `${sideBySideOutputRatio}fr`);
    // Fetch settings if possible.
    const fetchSettings = settingRegistry
        ? settingRegistry.load(trackerPlugin.id)
        : Promise.reject(new Error(`No setting registry for ${trackerPlugin.id}`));
    fetchSettings
        .then(settings => {
        updateConfig(settings);
        settings.changed.connect(() => {
            updateConfig(settings);
        });
        const updateSessionSettings = (session, changes) => {
            const { newValue, oldValue } = changes;
            const autoStartDefault = newValue.autoStartDefault;
            if (typeof autoStartDefault === 'boolean' &&
                autoStartDefault !== oldValue.autoStartDefault) {
                // Ensure we break the cycle
                if (autoStartDefault !==
                    settings.get('autoStartDefaultKernel').composite)
                    // Once the settings is changed `updateConfig` will take care
                    // of the propagation to existing session context.
                    settings
                        .set('autoStartDefaultKernel', autoStartDefault)
                        .catch(reason => {
                        console.error(`Failed to set ${settings.id}.autoStartDefaultKernel`);
                    });
            }
        };
        const sessionContexts = new WeakSet();
        const listenToKernelPreference = (panel) => {
            const session = panel.context.sessionContext;
            if (!session.isDisposed && !sessionContexts.has(session)) {
                sessionContexts.add(session);
                session.kernelPreferenceChanged.connect(updateSessionSettings);
                session.disposed.connect(() => {
                    session.kernelPreferenceChanged.disconnect(updateSessionSettings);
                });
            }
        };
        tracker.forEach(listenToKernelPreference);
        tracker.widgetAdded.connect((tracker, panel) => {
            listenToKernelPreference(panel);
        });
        commands.addCommand(CommandIDs.autoClosingBrackets, {
            execute: args => {
                var _a;
                const codeConfig = settings.get('codeCellConfig')
                    .composite;
                const markdownConfig = settings.get('markdownCellConfig')
                    .composite;
                const rawConfig = settings.get('rawCellConfig')
                    .composite;
                const anyToggled = codeConfig.autoClosingBrackets ||
                    markdownConfig.autoClosingBrackets ||
                    rawConfig.autoClosingBrackets;
                const toggled = !!((_a = args['force']) !== null && _a !== void 0 ? _a : !anyToggled);
                [
                    codeConfig.autoClosingBrackets,
                    markdownConfig.autoClosingBrackets,
                    rawConfig.autoClosingBrackets
                ] = [toggled, toggled, toggled];
                void settings.set('codeCellConfig', codeConfig);
                void settings.set('markdownCellConfig', markdownConfig);
                void settings.set('rawCellConfig', rawConfig);
            },
            label: trans.__('Auto Close Brackets for All Notebook Cell Types'),
            isToggled: () => ['codeCellConfig', 'markdownCellConfig', 'rawCellConfig'].some(x => {
                var _a;
                return ((_a = settings.get(x).composite.autoClosingBrackets) !== null && _a !== void 0 ? _a : extensions.baseConfiguration['autoClosingBrackets']) === true;
            })
        });
        commands.addCommand(CommandIDs.setSideBySideRatio, {
            label: trans.__('Set side-by-side ratio'),
            execute: args => {
                lib_index_js_.InputDialog.getNumber({
                    title: trans.__('Width of the output in side-by-side mode'),
                    value: settings.get('sideBySideOutputRatio').composite
                })
                    .then(result => {
                    setSideBySideOutputRatio(result.value);
                    if (result.value) {
                        void settings.set('sideBySideOutputRatio', result.value);
                    }
                })
                    .catch(console.error);
            }
        });
    })
        .catch((reason) => {
        console.warn(reason.message);
        updateTracker({
            editorConfig: factory.editorConfig,
            notebookConfig: factory.notebookConfig,
            kernelShutdown: factory.shutdownOnClose,
            autoStartDefault: factory.autoStartDefault
        });
    });
    if (formRegistry) {
        const CMRenderer = formRegistry.getRenderer('@jupyterlab/codemirror-extension:plugin.defaultConfig');
        if (CMRenderer) {
            formRegistry.addRenderer('@jupyterlab/notebook-extension:tracker.codeCellConfig', CMRenderer);
            formRegistry.addRenderer('@jupyterlab/notebook-extension:tracker.markdownCellConfig', CMRenderer);
            formRegistry.addRenderer('@jupyterlab/notebook-extension:tracker.rawCellConfig', CMRenderer);
        }
    }
    // Handle state restoration.
    if (restorer) {
        void restorer.restore(tracker, {
            command: 'docmanager:open',
            args: panel => ({ path: panel.context.path, factory: FACTORY }),
            name: panel => panel.context.path,
            when: services.ready
        });
    }
    const registry = app.docRegistry;
    const modelFactory = new notebook_lib_index_js_.NotebookModelFactory({
        disableDocumentWideUndoRedo: factory.notebookConfig.disableDocumentWideUndoRedo,
        collaborative: true
    });
    registry.addModelFactory(modelFactory);
    addCommands(app, tracker, translator, sessionDialogs, isEnabled);
    if (palette) {
        populatePalette(palette, translator);
    }
    let id = 0; // The ID counter for notebook panels.
    const ft = app.docRegistry.getFileType('notebook');
    factory.widgetCreated.connect((sender, widget) => {
        var _a, _b;
        // If the notebook panel does not have an ID, assign it one.
        widget.id = widget.id || `notebook-${++id}`;
        // Set up the title icon
        widget.title.icon = ft === null || ft === void 0 ? void 0 : ft.icon;
        widget.title.iconClass = (_a = ft === null || ft === void 0 ? void 0 : ft.iconClass) !== null && _a !== void 0 ? _a : '';
        widget.title.iconLabel = (_b = ft === null || ft === void 0 ? void 0 : ft.iconLabel) !== null && _b !== void 0 ? _b : '';
        // Notify the widget tracker if restore data needs to update.
        widget.context.pathChanged.connect(() => {
            void tracker.save(widget);
        });
        // Add the notebook panel to the tracker.
        void tracker.add(widget);
    });
    /**
     * Update the settings of the current tracker.
     */
    function updateTracker(options) {
        tracker.forEach(widget => {
            widget.setConfig(options);
        });
    }
    /**
     * Update the setting values.
     */
    function updateConfig(settings) {
        const code = {
            ...notebook_lib_index_js_.StaticNotebook.defaultEditorConfig.code,
            ...settings.get('codeCellConfig').composite
        };
        const markdown = {
            ...notebook_lib_index_js_.StaticNotebook.defaultEditorConfig.markdown,
            ...settings.get('markdownCellConfig').composite
        };
        const raw = {
            ...notebook_lib_index_js_.StaticNotebook.defaultEditorConfig.raw,
            ...settings.get('rawCellConfig').composite
        };
        factory.editorConfig = { code, markdown, raw };
        factory.notebookConfig = {
            showHiddenCellsButton: settings.get('showHiddenCellsButton')
                .composite,
            scrollPastEnd: settings.get('scrollPastEnd').composite,
            defaultCell: settings.get('defaultCell').composite,
            recordTiming: settings.get('recordTiming').composite,
            overscanCount: settings.get('overscanCount').composite,
            inputHistoryScope: settings.get('inputHistoryScope').composite,
            maxNumberOutputs: settings.get('maxNumberOutputs').composite,
            showEditorForReadOnlyMarkdown: settings.get('showEditorForReadOnlyMarkdown').composite,
            disableDocumentWideUndoRedo: !settings.get('documentWideUndoRedo')
                .composite,
            renderingLayout: settings.get('renderingLayout').composite,
            sideBySideLeftMarginOverride: settings.get('sideBySideLeftMarginOverride')
                .composite,
            sideBySideRightMarginOverride: settings.get('sideBySideRightMarginOverride').composite,
            sideBySideOutputRatio: settings.get('sideBySideOutputRatio')
                .composite,
            windowingMode: settings.get('windowingMode').composite
        };
        setSideBySideOutputRatio(factory.notebookConfig.sideBySideOutputRatio);
        const sideBySideMarginStyle = `.jp-mod-sideBySide.jp-Notebook .jp-Notebook-cell {
      margin-left: ${factory.notebookConfig.sideBySideLeftMarginOverride} !important;
      margin-right: ${factory.notebookConfig.sideBySideRightMarginOverride} !important;`;
        const sideBySideMarginTag = document.getElementById(SIDE_BY_SIDE_STYLE_ID);
        if (sideBySideMarginTag) {
            sideBySideMarginTag.innerText = sideBySideMarginStyle;
        }
        else {
            document.head.insertAdjacentHTML('beforeend', `<style id="${SIDE_BY_SIDE_STYLE_ID}">${sideBySideMarginStyle}}</style>`);
        }
        factory.autoStartDefault = settings.get('autoStartDefaultKernel')
            .composite;
        factory.shutdownOnClose = settings.get('kernelShutdown')
            .composite;
        modelFactory.disableDocumentWideUndoRedo = !settings.get('documentWideUndoRedo').composite;
        updateTracker({
            editorConfig: factory.editorConfig,
            notebookConfig: factory.notebookConfig,
            kernelShutdown: factory.shutdownOnClose,
            autoStartDefault: factory.autoStartDefault
        });
    }
    // Add main menu notebook menu.
    if (mainMenu) {
        populateMenus(mainMenu, isEnabled);
    }
    // Utility function to create a new notebook.
    const createNew = async (cwd, kernelId, kernelName) => {
        const model = await commands.execute('docmanager:new-untitled', {
            path: cwd,
            type: 'notebook'
        });
        if (model !== undefined) {
            const widget = (await commands.execute('docmanager:open', {
                path: model.path,
                factory: FACTORY,
                kernel: { id: kernelId, name: kernelName }
            }));
            widget.isUntitled = true;
            return widget;
        }
    };
    // Add a command for creating a new notebook.
    commands.addCommand(CommandIDs.createNew, {
        label: args => {
            var _a, _b, _c;
            const kernelName = args['kernelName'] || '';
            if (args['isLauncher'] && args['kernelName'] && services.kernelspecs) {
                return ((_c = (_b = (_a = services.kernelspecs.specs) === null || _a === void 0 ? void 0 : _a.kernelspecs[kernelName]) === null || _b === void 0 ? void 0 : _b.display_name) !== null && _c !== void 0 ? _c : '');
            }
            if (args['isPalette'] || args['isContextMenu']) {
                return trans.__('New Notebook');
            }
            return trans.__('Notebook');
        },
        caption: trans.__('Create a new notebook'),
        icon: args => (args['isPalette'] ? undefined : ui_components_lib_index_js_.notebookIcon),
        execute: args => {
            var _a;
            const cwd = args['cwd'] || ((_a = defaultBrowser === null || defaultBrowser === void 0 ? void 0 : defaultBrowser.model.path) !== null && _a !== void 0 ? _a : '');
            const kernelId = args['kernelId'] || '';
            const kernelName = args['kernelName'] || '';
            return createNew(cwd, kernelId, kernelName);
        }
    });
    // Add a launcher item if the launcher is available.
    if (launcher) {
        void services.ready.then(() => {
            let disposables = null;
            const onSpecsChanged = () => {
                if (disposables) {
                    disposables.dispose();
                    disposables = null;
                }
                const specs = services.kernelspecs.specs;
                if (!specs) {
                    return;
                }
                disposables = new dist_index_es6_js_.DisposableSet();
                for (const name in specs.kernelspecs) {
                    const rank = name === specs.default ? 0 : Infinity;
                    const spec = specs.kernelspecs[name];
                    const kernelIconUrl = spec.resources['logo-svg'] || spec.resources['logo-64x64'];
                    disposables.add(launcher.add({
                        command: CommandIDs.createNew,
                        args: { isLauncher: true, kernelName: name },
                        category: trans.__('Notebook'),
                        rank,
                        kernelIconUrl,
                        metadata: {
                            kernel: dist_index_js_.JSONExt.deepCopy(spec.metadata || {})
                        }
                    }));
                }
            };
            onSpecsChanged();
            services.kernelspecs.specsChanged.connect(onSpecsChanged);
        });
    }
    return tracker;
}
/**
 * Activate the completer service for notebook.
 */
function activateNotebookCompleterService(app, notebooks, manager, translator, appSanitizer) {
    if (!manager) {
        return;
    }
    const trans = (translator !== null && translator !== void 0 ? translator : translation_lib_index_js_.nullTranslator).load('jupyterlab');
    const sanitizer = appSanitizer !== null && appSanitizer !== void 0 ? appSanitizer : new lib_index_js_.Sanitizer();
    app.commands.addCommand(CommandIDs.invokeCompleter, {
        label: trans.__('Display the completion helper.'),
        execute: args => {
            var _a;
            const panel = notebooks.currentWidget;
            if (panel && ((_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.model.type) === 'code') {
                manager.invoke(panel.id);
            }
        }
    });
    app.commands.addCommand(CommandIDs.selectCompleter, {
        label: trans.__('Select the completion suggestion.'),
        execute: () => {
            const id = notebooks.currentWidget && notebooks.currentWidget.id;
            if (id) {
                return manager.select(id);
            }
        }
    });
    app.commands.addKeyBinding({
        command: CommandIDs.selectCompleter,
        keys: ['Enter'],
        selector: '.jp-Notebook .jp-mod-completer-active'
    });
    const updateCompleter = async (_, notebook) => {
        var _a, _b;
        const completerContext = {
            editor: (_b = (_a = notebook.content.activeCell) === null || _a === void 0 ? void 0 : _a.editor) !== null && _b !== void 0 ? _b : null,
            session: notebook.sessionContext.session,
            widget: notebook,
            sanitizer: sanitizer
        };
        await manager.updateCompleter(completerContext);
        notebook.content.activeCellChanged.connect((_, cell) => {
            // Ensure the editor will exist on the cell before adding the completer
            cell === null || cell === void 0 ? void 0 : cell.ready.then(() => {
                const newCompleterContext = {
                    editor: cell.editor,
                    session: notebook.sessionContext.session,
                    widget: notebook,
                    sanitizer: sanitizer
                };
                return manager.updateCompleter(newCompleterContext);
            }).catch(console.error);
        });
        notebook.sessionContext.sessionChanged.connect(() => {
            var _a;
            // Ensure the editor will exist on the cell before adding the completer
            (_a = notebook.content.activeCell) === null || _a === void 0 ? void 0 : _a.ready.then(() => {
                var _a, _b;
                const newCompleterContext = {
                    editor: (_b = (_a = notebook.content.activeCell) === null || _a === void 0 ? void 0 : _a.editor) !== null && _b !== void 0 ? _b : null,
                    session: notebook.sessionContext.session,
                    widget: notebook
                };
                return manager.updateCompleter(newCompleterContext);
            }).catch(console.error);
        });
    };
    notebooks.widgetAdded.connect(updateCompleter);
    manager.activeProvidersChanged.connect(() => {
        notebooks.forEach(panel => {
            updateCompleter(undefined, panel).catch(e => console.error(e));
        });
    });
}
/**
 * Activate the language server for notebook.
 */
function activateNotebookLanguageServer(app, notebooks, connectionManager, featureManager, codeExtractorManager, adapterTracker) {
    notebooks.widgetAdded.connect(async (_, notebook) => {
        const adapter = new notebook_lib_index_js_.NotebookAdapter(notebook, {
            connectionManager,
            featureManager,
            foreignCodeExtractorsManager: codeExtractorManager
        });
        adapterTracker.add(adapter);
    });
}
// Get the current widget and activate unless the args specify otherwise.
function getCurrent(tracker, shell, args) {
    const widget = tracker.currentWidget;
    const activate = args['activate'] !== false;
    if (activate && widget) {
        shell.activateById(widget.id);
    }
    return widget;
}
/**
 * Add the notebook commands to the application's command registry.
 */
function addCommands(app, tracker, translator, sessionDialogs, isEnabled) {
    const trans = translator.load('jupyterlab');
    const { commands, shell } = app;
    const isEnabledAndSingleSelected = () => {
        return Private.isEnabledAndSingleSelected(shell, tracker);
    };
    const refreshCellCollapsed = (notebook) => {
        var _a, _b;
        for (const cell of notebook.widgets) {
            if (cell instanceof cells_lib_index_js_.MarkdownCell && cell.headingCollapsed) {
                notebook_lib_index_js_.NotebookActions.setHeadingCollapse(cell, true, notebook);
            }
            if (cell.model.id === ((_b = (_a = notebook.activeCell) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.id)) {
                notebook_lib_index_js_.NotebookActions.expandParent(cell, notebook);
            }
        }
    };
    const isEnabledAndHeadingSelected = () => {
        return Private.isEnabledAndHeadingSelected(shell, tracker);
    };
    // Set up signal handler to keep the collapse state consistent
    tracker.currentChanged.connect((sender, panel) => {
        var _a, _b;
        if (!((_b = (_a = panel === null || panel === void 0 ? void 0 : panel.content) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.cells)) {
            return;
        }
        panel.content.model.cells.changed.connect((list, args) => {
            // Might be overkill to refresh this every time, but
            // it helps to keep the collapse state consistent.
            refreshCellCollapsed(panel.content);
        });
        panel.content.activeCellChanged.connect((notebook, cell) => {
            notebook_lib_index_js_.NotebookActions.expandParent(cell, notebook);
        });
    });
    tracker.selectionChanged.connect(() => {
        commands.notifyCommandChanged(CommandIDs.duplicateBelow);
        commands.notifyCommandChanged(CommandIDs.deleteCell);
        commands.notifyCommandChanged(CommandIDs.copy);
        commands.notifyCommandChanged(CommandIDs.cut);
        commands.notifyCommandChanged(CommandIDs.pasteBelow);
        commands.notifyCommandChanged(CommandIDs.pasteAbove);
        commands.notifyCommandChanged(CommandIDs.pasteAndReplace);
        commands.notifyCommandChanged(CommandIDs.moveUp);
        commands.notifyCommandChanged(CommandIDs.moveDown);
        commands.notifyCommandChanged(CommandIDs.run);
        commands.notifyCommandChanged(CommandIDs.runAll);
        commands.notifyCommandChanged(CommandIDs.runAndAdvance);
        commands.notifyCommandChanged(CommandIDs.runAndInsert);
    });
    tracker.activeCellChanged.connect(() => {
        commands.notifyCommandChanged(CommandIDs.moveUp);
        commands.notifyCommandChanged(CommandIDs.moveDown);
    });
    commands.addCommand(CommandIDs.runAndAdvance, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Run Selected Cell', 'Run Selected Cells', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        caption: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Run this cell and advance', 'Run these %1 cells and advance', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                return notebook_lib_index_js_.NotebookActions.runAndAdvance(content, context.sessionContext, sessionDialogs, translator);
            }
        },
        isEnabled: args => (args.toolbar ? true : isEnabled()),
        icon: args => (args.toolbar ? ui_components_lib_index_js_.runIcon : undefined)
    });
    commands.addCommand(CommandIDs.run, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Run Selected Cell and Do not Advance', 'Run Selected Cells and Do not Advance', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                return notebook_lib_index_js_.NotebookActions.run(content, context.sessionContext, sessionDialogs, translator);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.runAndInsert, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Run Selected Cell and Insert Below', 'Run Selected Cells and Insert Below', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                return notebook_lib_index_js_.NotebookActions.runAndInsert(content, context.sessionContext, sessionDialogs, translator);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.runAll, {
        label: trans.__('Run All Cells'),
        caption: trans.__('Run all cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                return notebook_lib_index_js_.NotebookActions.runAll(content, context.sessionContext, sessionDialogs, translator);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.runAllAbove, {
        label: trans.__('Run All Above Selected Cell'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                return notebook_lib_index_js_.NotebookActions.runAllAbove(content, context.sessionContext, sessionDialogs, translator);
            }
        },
        isEnabled: () => {
            // Can't run above if there are multiple cells selected,
            // or if we are at the top of the notebook.
            return (isEnabledAndSingleSelected() &&
                tracker.currentWidget.content.activeCellIndex !== 0);
        }
    });
    commands.addCommand(CommandIDs.runAllBelow, {
        label: trans.__('Run Selected Cell and All Below'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                return notebook_lib_index_js_.NotebookActions.runAllBelow(content, context.sessionContext, sessionDialogs, translator);
            }
        },
        isEnabled: () => {
            // Can't run below if there are multiple cells selected,
            // or if we are at the bottom of the notebook.
            return (isEnabledAndSingleSelected() &&
                tracker.currentWidget.content.activeCellIndex !==
                    tracker.currentWidget.content.widgets.length - 1);
        }
    });
    commands.addCommand(CommandIDs.renderAllMarkdown, {
        label: trans.__('Render All Markdown Cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { content } = current;
                return notebook_lib_index_js_.NotebookActions.renderAllMarkdown(content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.restart, {
        label: trans.__('Restart Kernel…'),
        caption: trans.__('Restart the kernel'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return sessionDialogs.restart(current.sessionContext);
            }
        },
        isEnabled: args => (args.toolbar ? true : isEnabled()),
        icon: args => (args.toolbar ? ui_components_lib_index_js_.refreshIcon : undefined)
    });
    commands.addCommand(CommandIDs.shutdown, {
        label: trans.__('Shut Down Kernel'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (!current) {
                return;
            }
            return current.context.sessionContext.shutdown();
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.closeAndShutdown, {
        label: trans.__('Close and Shut Down Notebook'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (!current) {
                return;
            }
            const fileName = current.title.label;
            return (0,lib_index_js_.showDialog)({
                title: trans.__('Shut down the notebook?'),
                body: trans.__('Are you sure you want to close "%1"?', fileName),
                buttons: [lib_index_js_.Dialog.cancelButton(), lib_index_js_.Dialog.warnButton()]
            }).then(result => {
                if (result.button.accept) {
                    return commands
                        .execute(CommandIDs.shutdown, { activate: false })
                        .then(() => {
                        current.dispose();
                    });
                }
            });
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.trust, {
        label: () => trans.__('Trust Notebook'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const { context, content } = current;
                return notebook_lib_index_js_.NotebookActions.trust(content).then(() => context.save());
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.restartClear, {
        label: trans.__('Restart Kernel and Clear Outputs of All Cells…'),
        caption: trans.__('Restart the kernel and clear all outputs of all cells'),
        execute: async () => {
            const restarted = await commands.execute(CommandIDs.restart, {
                activate: false
            });
            if (restarted) {
                await commands.execute(CommandIDs.clearAllOutputs);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.restartAndRunToSelected, {
        label: trans.__('Restart Kernel and Run up to Selected Cell…'),
        execute: async () => {
            const restarted = await commands.execute(CommandIDs.restart, {
                activate: false
            });
            if (restarted) {
                const executed = await commands.execute(CommandIDs.runAllAbove, { activate: false });
                if (executed) {
                    return commands.execute(CommandIDs.run);
                }
            }
        },
        isEnabled: isEnabledAndSingleSelected
    });
    commands.addCommand(CommandIDs.restartRunAll, {
        label: trans.__('Restart Kernel and Run All Cells…'),
        caption: trans.__('Restart the kernel and run all cells'),
        execute: async () => {
            const restarted = await commands.execute(CommandIDs.restart, {
                activate: false
            });
            if (restarted) {
                await commands.execute(CommandIDs.runAll);
            }
        },
        isEnabled: args => (args.toolbar ? true : isEnabled()),
        icon: args => (args.toolbar ? ui_components_lib_index_js_.fastForwardIcon : undefined)
    });
    commands.addCommand(CommandIDs.clearAllOutputs, {
        label: trans.__('Clear Outputs of All Cells'),
        caption: trans.__('Clear all outputs of all cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.clearAllOutputs(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.clearOutputs, {
        label: trans.__('Clear Cell Output'),
        caption: trans.__('Clear outputs for the selected cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.clearOutputs(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.interrupt, {
        label: trans.__('Interrupt Kernel'),
        caption: trans.__('Interrupt the kernel'),
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, args);
            if (!current) {
                return;
            }
            const kernel = (_a = current.context.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
            if (kernel) {
                return kernel.interrupt();
            }
        },
        isEnabled: args => (args.toolbar ? true : isEnabled()),
        icon: args => (args.toolbar ? ui_components_lib_index_js_.stopIcon : undefined)
    });
    commands.addCommand(CommandIDs.toCode, {
        label: trans.__('Change to Code Cell Type'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.changeCellType(current.content, 'code');
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.toMarkdown, {
        label: trans.__('Change to Markdown Cell Type'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.changeCellType(current.content, 'markdown');
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.toRaw, {
        label: trans.__('Change to Raw Cell Type'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.changeCellType(current.content, 'raw');
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.cut, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Cut Cell', 'Cut Cells', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        caption: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Cut this cell', 'Cut these %1 cells', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.cut(current.content);
            }
        },
        icon: args => (args.toolbar ? ui_components_lib_index_js_.cutIcon : undefined),
        isEnabled: args => (args.toolbar ? true : isEnabled())
    });
    commands.addCommand(CommandIDs.copy, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Copy Cell', 'Copy Cells', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        caption: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Copy this cell', 'Copy these %1 cells', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.copy(current.content);
            }
        },
        icon: args => (args.toolbar ? ui_components_lib_index_js_.copyIcon : undefined),
        isEnabled: args => (args.toolbar ? true : isEnabled())
    });
    commands.addCommand(CommandIDs.pasteBelow, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Paste Cell Below', 'Paste Cells Below', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        caption: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Paste this cell from the clipboard', 'Paste these %1 cells from the clipboard', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.paste(current.content, 'below');
            }
        },
        icon: args => (args.toolbar ? ui_components_lib_index_js_.pasteIcon : undefined),
        isEnabled: args => (args.toolbar ? true : isEnabled())
    });
    commands.addCommand(CommandIDs.pasteAbove, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Paste Cell Above', 'Paste Cells Above', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        caption: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Paste this cell from the clipboard', 'Paste these %1 cells from the clipboard', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.paste(current.content, 'above');
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.duplicateBelow, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Duplicate Cell Below', 'Duplicate Cells Below', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        caption: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Create a duplicate of this cell below', 'Create duplicates of %1 cells below', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                notebook_lib_index_js_.NotebookActions.duplicate(current.content, 'belowSelected');
            }
        },
        icon: args => (args.toolbar ? ui_components_lib_index_js_.duplicateIcon : undefined),
        isEnabled: args => (args.toolbar ? true : isEnabled())
    });
    commands.addCommand(CommandIDs.pasteAndReplace, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Paste Cell and Replace', 'Paste Cells and Replace', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.paste(current.content, 'replace');
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.deleteCell, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Delete Cell', 'Delete Cells', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        caption: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Delete this cell', 'Delete these %1 cells', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.deleteCells(current.content);
            }
        },
        isEnabled: args => (args.toolbar ? true : isEnabled())
    });
    commands.addCommand(CommandIDs.split, {
        label: trans.__('Split Cell'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.splitCell(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.merge, {
        label: trans.__('Merge Selected Cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.mergeCells(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.mergeAbove, {
        label: trans.__('Merge Cell Above'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.mergeCells(current.content, true);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.mergeBelow, {
        label: trans.__('Merge Cell Below'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.mergeCells(current.content, false);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.insertAbove, {
        label: trans.__('Insert Cell Above'),
        caption: trans.__('Insert a cell above'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.insertAbove(current.content);
            }
        },
        icon: args => (args.toolbar ? ui_components_lib_index_js_.addAboveIcon : undefined),
        isEnabled: args => (args.toolbar ? true : isEnabled())
    });
    commands.addCommand(CommandIDs.insertBelow, {
        label: trans.__('Insert Cell Below'),
        caption: trans.__('Insert a cell below'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.insertBelow(current.content);
            }
        },
        icon: args => (args.toolbar ? ui_components_lib_index_js_.addBelowIcon : undefined),
        isEnabled: args => (args.toolbar ? true : isEnabled())
    });
    commands.addCommand(CommandIDs.selectAbove, {
        label: trans.__('Select Cell Above'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.selectAbove(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.selectBelow, {
        label: trans.__('Select Cell Below'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.selectBelow(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.insertHeadingAbove, {
        label: trans.__('Insert Heading Above Current Heading'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.insertSameLevelHeadingAbove(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.insertHeadingBelow, {
        label: trans.__('Insert Heading Below Current Heading'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.insertSameLevelHeadingBelow(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.selectHeadingAboveOrCollapse, {
        label: trans.__('Select Heading Above or Collapse Heading'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.selectHeadingAboveOrCollapseHeading(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.selectHeadingBelowOrExpand, {
        label: trans.__('Select Heading Below or Expand Heading'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.selectHeadingBelowOrExpandHeading(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.extendAbove, {
        label: trans.__('Extend Selection Above'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.extendSelectionAbove(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.extendTop, {
        label: trans.__('Extend Selection to Top'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.extendSelectionAbove(current.content, true);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.extendBelow, {
        label: trans.__('Extend Selection Below'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.extendSelectionBelow(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.extendBottom, {
        label: trans.__('Extend Selection to Bottom'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.extendSelectionBelow(current.content, true);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.selectAll, {
        label: trans.__('Select All Cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.selectAll(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.deselectAll, {
        label: trans.__('Deselect All Cells'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.deselectAll(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.moveUp, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Move Cell Up', 'Move Cells Up', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        caption: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Move this cell up', 'Move these %1 cells up', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                notebook_lib_index_js_.NotebookActions.moveUp(current.content);
                Private.raiseSilentNotification(trans.__('Notebook cell shifted up successfully'), current.node);
            }
        },
        isEnabled: args => {
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            if (!current) {
                return false;
            }
            return current.content.activeCellIndex >= 1;
        },
        icon: args => (args.toolbar ? ui_components_lib_index_js_.moveUpIcon : undefined)
    });
    commands.addCommand(CommandIDs.moveDown, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Move Cell Down', 'Move Cells Down', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        caption: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return trans._n('Move this cell down', 'Move these %1 cells down', (_a = current === null || current === void 0 ? void 0 : current.content.selectedCells.length) !== null && _a !== void 0 ? _a : 1);
        },
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                notebook_lib_index_js_.NotebookActions.moveDown(current.content);
                Private.raiseSilentNotification(trans.__('Notebook cell shifted down successfully'), current.node);
            }
        },
        isEnabled: args => {
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            if (!current || !current.content.model) {
                return false;
            }
            const length = current.content.model.cells.length;
            return current.content.activeCellIndex < length - 1;
        },
        icon: args => (args.toolbar ? ui_components_lib_index_js_.moveDownIcon : undefined)
    });
    commands.addCommand(CommandIDs.toggleAllLines, {
        label: trans.__('Show Line Numbers'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.toggleAllLineNumbers(current.content);
            }
        },
        isEnabled,
        isToggled: args => {
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            if (current) {
                const config = current.content.editorConfig;
                return !!(config.code.lineNumbers &&
                    config.markdown.lineNumbers &&
                    config.raw.lineNumbers);
            }
            else {
                return false;
            }
        }
    });
    commands.addCommand(CommandIDs.commandMode, {
        label: trans.__('Enter Command Mode'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                current.content.mode = 'command';
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.editMode, {
        label: trans.__('Enter Edit Mode'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                current.content.mode = 'edit';
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.undoCellAction, {
        label: trans.__('Undo Cell Operation'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.undo(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.redoCellAction, {
        label: trans.__('Redo Cell Operation'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.redo(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.redo, {
        label: trans.__('Redo'),
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const cell = current.content.activeCell;
                if (cell) {
                    cell.inputHidden = false;
                    return (_a = cell.editor) === null || _a === void 0 ? void 0 : _a.redo();
                }
            }
        }
    });
    commands.addCommand(CommandIDs.undo, {
        label: trans.__('Undo'),
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, args);
            if (current) {
                const cell = current.content.activeCell;
                if (cell) {
                    cell.inputHidden = false;
                    return (_a = cell.editor) === null || _a === void 0 ? void 0 : _a.undo();
                }
            }
        }
    });
    commands.addCommand(CommandIDs.changeKernel, {
        label: trans.__('Change Kernel…'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return sessionDialogs.selectKernel(current.context.sessionContext);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.getKernel, {
        label: trans.__('Get Kernel'),
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, { activate: false, ...args });
            if (current) {
                return (_a = current.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.reconnectToKernel, {
        label: trans.__('Reconnect to Kernel'),
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, args);
            if (!current) {
                return;
            }
            const kernel = (_a = current.context.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
            if (kernel) {
                return kernel.reconnect();
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.markdown1, {
        label: trans.__('Change to Heading 1'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.setMarkdownHeader(current.content, 1);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.markdown2, {
        label: trans.__('Change to Heading 2'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.setMarkdownHeader(current.content, 2);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.markdown3, {
        label: trans.__('Change to Heading 3'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.setMarkdownHeader(current.content, 3);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.markdown4, {
        label: trans.__('Change to Heading 4'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.setMarkdownHeader(current.content, 4);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.markdown5, {
        label: trans.__('Change to Heading 5'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.setMarkdownHeader(current.content, 5);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.markdown6, {
        label: trans.__('Change to Heading 6'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.setMarkdownHeader(current.content, 6);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.hideCode, {
        label: trans.__('Collapse Selected Code'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.hideCode(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.showCode, {
        label: trans.__('Expand Selected Code'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.showCode(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.hideAllCode, {
        label: trans.__('Collapse All Code'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.hideAllCode(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.showAllCode, {
        label: trans.__('Expand All Code'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.showAllCode(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.hideOutput, {
        label: trans.__('Collapse Selected Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.hideOutput(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.showOutput, {
        label: trans.__('Expand Selected Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.showOutput(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.hideAllOutputs, {
        label: trans.__('Collapse All Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.hideAllOutputs(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.toggleRenderSideBySideCurrentNotebook, {
        label: trans.__('Render Side-by-Side'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                if (current.content.renderingLayout === 'side-by-side') {
                    return notebook_lib_index_js_.NotebookActions.renderDefault(current.content);
                }
                return notebook_lib_index_js_.NotebookActions.renderSideBySide(current.content);
            }
        },
        isEnabled,
        isToggled: args => {
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            if (current) {
                return current.content.renderingLayout === 'side-by-side';
            }
            else {
                return false;
            }
        }
    });
    commands.addCommand(CommandIDs.showAllOutputs, {
        label: trans.__('Expand All Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.showAllOutputs(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.enableOutputScrolling, {
        label: trans.__('Enable Scrolling for Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.enableOutputScrolling(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.disableOutputScrolling, {
        label: trans.__('Disable Scrolling for Outputs'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.disableOutputScrolling(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.selectLastRunCell, {
        label: trans.__('Select current running or last run cell'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.selectLastRunCell(current.content);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.replaceSelection, {
        label: trans.__('Replace Selection in Notebook Cell'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            const text = args['text'] || '';
            if (current) {
                return notebook_lib_index_js_.NotebookActions.replaceSelection(current.content, text);
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.toggleCollapseCmd, {
        label: trans.__('Toggle Collapse Notebook Heading'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.toggleCurrentHeadingCollapse(current.content);
            }
        },
        isEnabled: isEnabledAndHeadingSelected
    });
    commands.addCommand(CommandIDs.collapseAllCmd, {
        label: trans.__('Collapse All Headings'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.collapseAllHeadings(current.content);
            }
        }
    });
    commands.addCommand(CommandIDs.expandAllCmd, {
        label: trans.__('Expand All Headings'),
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return notebook_lib_index_js_.NotebookActions.expandAllHeadings(current.content);
            }
        }
    });
    commands.addCommand(CommandIDs.tocRunCells, {
        label: trans.__('Select and Run Cell(s) for this Heading'),
        execute: args => {
            const current = getCurrent(tracker, shell, { activate: false, ...args });
            if (current === null) {
                return;
            }
            const activeCell = current.content.activeCell;
            let lastIndex = current.content.activeCellIndex;
            if (activeCell instanceof cells_lib_index_js_.MarkdownCell) {
                const cells = current.content.widgets;
                const level = activeCell.headingInfo.level;
                for (let i = current.content.activeCellIndex + 1; i < cells.length; i++) {
                    const cell = cells[i];
                    if (cell instanceof cells_lib_index_js_.MarkdownCell &&
                        // cell.headingInfo.level === -1 if no heading
                        cell.headingInfo.level >= 0 &&
                        cell.headingInfo.level <= level) {
                        break;
                    }
                    lastIndex = i;
                }
            }
            current.content.extendContiguousSelectionTo(lastIndex);
            void notebook_lib_index_js_.NotebookActions.run(current.content, current.sessionContext, sessionDialogs, translator);
        }
    });
}
/**
 * Populate the application's command palette with notebook commands.
 */
function populatePalette(palette, translator) {
    const trans = translator.load('jupyterlab');
    let category = trans.__('Notebook Operations');
    [
        CommandIDs.interrupt,
        CommandIDs.restart,
        CommandIDs.restartClear,
        CommandIDs.restartRunAll,
        CommandIDs.runAll,
        CommandIDs.renderAllMarkdown,
        CommandIDs.runAllAbove,
        CommandIDs.runAllBelow,
        CommandIDs.restartAndRunToSelected,
        CommandIDs.selectAll,
        CommandIDs.deselectAll,
        CommandIDs.clearAllOutputs,
        CommandIDs.toggleAllLines,
        CommandIDs.editMode,
        CommandIDs.commandMode,
        CommandIDs.changeKernel,
        CommandIDs.reconnectToKernel,
        CommandIDs.createConsole,
        CommandIDs.closeAndShutdown,
        CommandIDs.trust,
        CommandIDs.toggleCollapseCmd,
        CommandIDs.collapseAllCmd,
        CommandIDs.expandAllCmd
    ].forEach(command => {
        palette.addItem({ command, category });
    });
    palette.addItem({
        command: CommandIDs.createNew,
        category,
        args: { isPalette: true }
    });
    category = trans.__('Notebook Cell Operations');
    [
        CommandIDs.run,
        CommandIDs.runAndAdvance,
        CommandIDs.runAndInsert,
        CommandIDs.runInConsole,
        CommandIDs.clearOutputs,
        CommandIDs.toCode,
        CommandIDs.toMarkdown,
        CommandIDs.toRaw,
        CommandIDs.cut,
        CommandIDs.copy,
        CommandIDs.pasteBelow,
        CommandIDs.pasteAbove,
        CommandIDs.pasteAndReplace,
        CommandIDs.deleteCell,
        CommandIDs.split,
        CommandIDs.merge,
        CommandIDs.mergeAbove,
        CommandIDs.mergeBelow,
        CommandIDs.insertAbove,
        CommandIDs.insertBelow,
        CommandIDs.selectAbove,
        CommandIDs.selectBelow,
        CommandIDs.selectHeadingAboveOrCollapse,
        CommandIDs.selectHeadingBelowOrExpand,
        CommandIDs.insertHeadingAbove,
        CommandIDs.insertHeadingBelow,
        CommandIDs.extendAbove,
        CommandIDs.extendTop,
        CommandIDs.extendBelow,
        CommandIDs.extendBottom,
        CommandIDs.moveDown,
        CommandIDs.moveUp,
        CommandIDs.undoCellAction,
        CommandIDs.redoCellAction,
        CommandIDs.markdown1,
        CommandIDs.markdown2,
        CommandIDs.markdown3,
        CommandIDs.markdown4,
        CommandIDs.markdown5,
        CommandIDs.markdown6,
        CommandIDs.hideCode,
        CommandIDs.showCode,
        CommandIDs.hideAllCode,
        CommandIDs.showAllCode,
        CommandIDs.hideOutput,
        CommandIDs.showOutput,
        CommandIDs.hideAllOutputs,
        CommandIDs.showAllOutputs,
        CommandIDs.toggleRenderSideBySideCurrentNotebook,
        CommandIDs.setSideBySideRatio,
        CommandIDs.enableOutputScrolling,
        CommandIDs.disableOutputScrolling
    ].forEach(command => {
        palette.addItem({ command, category });
    });
}
/**
 * Populates the application menus for the notebook.
 */
function populateMenus(mainMenu, isEnabled) {
    // Add undo/redo hooks to the edit menu.
    mainMenu.editMenu.undoers.redo.add({
        id: CommandIDs.redo,
        isEnabled
    });
    mainMenu.editMenu.undoers.undo.add({
        id: CommandIDs.undo,
        isEnabled
    });
    // Add a clearer to the edit menu
    mainMenu.editMenu.clearers.clearAll.add({
        id: CommandIDs.clearAllOutputs,
        isEnabled
    });
    mainMenu.editMenu.clearers.clearCurrent.add({
        id: CommandIDs.clearOutputs,
        isEnabled
    });
    // Add a console creator the the Kernel menu
    mainMenu.fileMenu.consoleCreators.add({
        id: CommandIDs.createConsole,
        isEnabled
    });
    // Add a close and shutdown command to the file menu.
    mainMenu.fileMenu.closeAndCleaners.add({
        id: CommandIDs.closeAndShutdown,
        isEnabled
    });
    // Add a kernel user to the Kernel menu
    mainMenu.kernelMenu.kernelUsers.changeKernel.add({
        id: CommandIDs.changeKernel,
        isEnabled
    });
    mainMenu.kernelMenu.kernelUsers.clearWidget.add({
        id: CommandIDs.clearAllOutputs,
        isEnabled
    });
    mainMenu.kernelMenu.kernelUsers.interruptKernel.add({
        id: CommandIDs.interrupt,
        isEnabled
    });
    mainMenu.kernelMenu.kernelUsers.reconnectToKernel.add({
        id: CommandIDs.reconnectToKernel,
        isEnabled
    });
    mainMenu.kernelMenu.kernelUsers.restartKernel.add({
        id: CommandIDs.restart,
        isEnabled
    });
    mainMenu.kernelMenu.kernelUsers.shutdownKernel.add({
        id: CommandIDs.shutdown,
        isEnabled
    });
    // Add an IEditorViewer to the application view menu
    mainMenu.viewMenu.editorViewers.toggleLineNumbers.add({
        id: CommandIDs.toggleAllLines,
        isEnabled
    });
    // Add an ICodeRunner to the application run menu
    mainMenu.runMenu.codeRunners.restart.add({
        id: CommandIDs.restart,
        isEnabled
    });
    mainMenu.runMenu.codeRunners.run.add({
        id: CommandIDs.runAndAdvance,
        isEnabled
    });
    mainMenu.runMenu.codeRunners.runAll.add({ id: CommandIDs.runAll, isEnabled });
    // Add kernel information to the application help menu.
    mainMenu.helpMenu.getKernel.add({
        id: CommandIDs.getKernel,
        isEnabled
    });
}
/**
 * A namespace for module private functionality.
 */
var Private;
(function (Private) {
    /**
     * Create a console connected with a notebook kernel
     *
     * @param commands Commands registry
     * @param widget Notebook panel
     * @param activate Should the console be activated
     */
    function createConsole(commands, widget, activate) {
        const options = {
            path: widget.context.path,
            preferredLanguage: widget.context.model.defaultKernelLanguage,
            activate: activate,
            ref: widget.id,
            insertMode: 'split-bottom',
            type: 'Linked Console'
        };
        return commands.execute('console:create', options);
    }
    Private.createConsole = createConsole;
    /**
     * Whether there is an active notebook.
     */
    function isEnabled(shell, tracker) {
        return (tracker.currentWidget !== null &&
            tracker.currentWidget === shell.currentWidget);
    }
    Private.isEnabled = isEnabled;
    /**
     * Whether there is an notebook active, with a single selected cell.
     */
    function isEnabledAndSingleSelected(shell, tracker) {
        if (!Private.isEnabled(shell, tracker)) {
            return false;
        }
        const { content } = tracker.currentWidget;
        const index = content.activeCellIndex;
        // If there are selections that are not the active cell,
        // this command is confusing, so disable it.
        for (let i = 0; i < content.widgets.length; ++i) {
            if (content.isSelected(content.widgets[i]) && i !== index) {
                return false;
            }
        }
        return true;
    }
    Private.isEnabledAndSingleSelected = isEnabledAndSingleSelected;
    /**
     * Whether there is an notebook active, with a single selected cell.
     */
    function isEnabledAndHeadingSelected(shell, tracker) {
        if (!Private.isEnabled(shell, tracker)) {
            return false;
        }
        const { content } = tracker.currentWidget;
        const index = content.activeCellIndex;
        if (!(content.activeCell instanceof cells_lib_index_js_.MarkdownCell)) {
            return false;
        }
        // If there are selections that are not the active cell,
        // this command is confusing, so disable it.
        for (let i = 0; i < content.widgets.length; ++i) {
            if (content.isSelected(content.widgets[i]) && i !== index) {
                return false;
            }
        }
        return true;
    }
    Private.isEnabledAndHeadingSelected = isEnabledAndHeadingSelected;
    /**
     * The default Export To ... formats and their human readable labels.
     */
    function getFormatLabels(translator) {
        translator = translator || translation_lib_index_js_.nullTranslator;
        const trans = translator.load('jupyterlab');
        return {
            html: trans.__('HTML'),
            latex: trans.__('LaTeX'),
            markdown: trans.__('Markdown'),
            pdf: trans.__('PDF'),
            rst: trans.__('ReStructured Text'),
            script: trans.__('Executable Script'),
            slides: trans.__('Reveal.js Slides')
        };
    }
    Private.getFormatLabels = getFormatLabels;
    /**
     * Raises a silent notification that is read by screen readers
     *
     * FIXME: Once a notificatiom API is introduced (https://github.com/jupyterlab/jupyterlab/issues/689),
     * this can be refactored to use the same.
     *
     * More discussion at https://github.com/jupyterlab/jupyterlab/pull/9031#issuecomment-773541469
     *
     *
     * @param message Message to be relayed to screen readers
     * @param notebookNode DOM node to which the notification container is attached
     */
    function raiseSilentNotification(message, notebookNode) {
        const hiddenAlertContainerId = `sr-message-container-${notebookNode.id}`;
        const hiddenAlertContainer = document.getElementById(hiddenAlertContainerId) ||
            document.createElement('div');
        // If the container is not available, append the newly created container
        // to the current notebook panel and set related properties
        if (hiddenAlertContainer.getAttribute('id') !== hiddenAlertContainerId) {
            hiddenAlertContainer.classList.add('sr-only');
            hiddenAlertContainer.setAttribute('id', hiddenAlertContainerId);
            hiddenAlertContainer.setAttribute('role', 'alert');
            hiddenAlertContainer.hidden = true;
            notebookNode.appendChild(hiddenAlertContainer);
        }
        // Insert/Update alert container with the notification message
        hiddenAlertContainer.innerText = message;
    }
    Private.raiseSilentNotification = raiseSilentNotification;
    /**
     * A widget hosting a cloned output area.
     */
    class ClonedOutputArea extends widgets_dist_index_es6_js_.Panel {
        constructor(options) {
            super();
            this._cell = null;
            const trans = (options.translator || translation_lib_index_js_.nullTranslator).load('jupyterlab');
            this._notebook = options.notebook;
            this._index = options.index !== undefined ? options.index : -1;
            this._cell = options.cell || null;
            this.id = `LinkedOutputView-${dist_index_js_.UUID.uuid4()}`;
            this.title.label = 'Output View';
            this.title.icon = ui_components_lib_index_js_.notebookIcon;
            this.title.caption = this._notebook.title.label
                ? trans.__('For Notebook: %1', this._notebook.title.label)
                : trans.__('For Notebook:');
            this.addClass('jp-LinkedOutputView');
            // Wait for the notebook to be loaded before
            // cloning the output area.
            void this._notebook.context.ready.then(() => {
                if (!this._cell) {
                    this._cell = this._notebook.content.widgets[this._index];
                }
                if (!this._cell || this._cell.model.type !== 'code') {
                    this.dispose();
                    return;
                }
                const clone = this._cell.cloneOutputArea();
                this.addWidget(clone);
            });
        }
        /**
         * The index of the cell in the notebook.
         */
        get index() {
            return this._cell
                ? index_es6_js_.ArrayExt.findFirstIndex(this._notebook.content.widgets, c => c === this._cell)
                : this._index;
        }
        /**
         * The path of the notebook for the cloned output area.
         */
        get path() {
            return this._notebook.context.path;
        }
    }
    Private.ClonedOutputArea = ClonedOutputArea;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=9134.351c679c44d97ca75330.js.map?v=351c679c44d97ca75330