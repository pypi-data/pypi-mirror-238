"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[6011,6573],{

/***/ 26573:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(65681);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(82545);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(2116);
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(79891);
/* harmony import */ var _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(45534);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(56916);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(76351);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module inspector-extension
 */








/**
 * The command IDs used by the inspector plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'inspector:open';
    CommandIDs.close = 'inspector:close';
    CommandIDs.toggle = 'inspector:toggle';
})(CommandIDs || (CommandIDs = {}));
/**
 * A service providing code introspection.
 */
const inspector = {
    id: '@jupyterlab/inspector-extension:inspector',
    description: 'Provides the code introspection widget.',
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__.ILauncher, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    provides: _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.IInspector,
    autoStart: true,
    activate: (app, translator, palette, launcher, restorer) => {
        const trans = translator.load('jupyterlab');
        const { commands, shell } = app;
        const caption = trans.__('Live updating code documentation from the active kernel');
        const openedLabel = trans.__('Contextual Help');
        const namespace = 'inspector';
        const datasetKey = 'jpInspector';
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace
        });
        function isInspectorOpen() {
            return inspector && !inspector.isDisposed;
        }
        let source = null;
        let inspector;
        function openInspector(args) {
            var _a;
            if (!isInspectorOpen()) {
                inspector = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({
                    content: new _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.InspectorPanel({ translator })
                });
                inspector.id = 'jp-inspector';
                inspector.title.label = openedLabel;
                inspector.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.inspectorIcon;
                void tracker.add(inspector);
                source = source && !source.isDisposed ? source : null;
                inspector.content.source = source;
                (_a = inspector.content.source) === null || _a === void 0 ? void 0 : _a.onEditorChange(args);
            }
            if (!inspector.isAttached) {
                shell.add(inspector, 'main', {
                    activate: false,
                    mode: 'split-right',
                    type: 'Inspector'
                });
            }
            shell.activateById(inspector.id);
            document.body.dataset[datasetKey] = 'open';
            return inspector;
        }
        function closeInspector() {
            inspector.dispose();
            delete document.body.dataset[datasetKey];
        }
        // Add inspector:open command to registry.
        const showLabel = trans.__('Show Contextual Help');
        commands.addCommand(CommandIDs.open, {
            caption,
            isEnabled: () => !inspector ||
                inspector.isDisposed ||
                !inspector.isAttached ||
                !inspector.isVisible,
            label: showLabel,
            icon: args => (args.isLauncher ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.inspectorIcon : undefined),
            execute: args => {
                var _a;
                const text = args && args.text;
                const refresh = args && args.refresh;
                // if inspector is open, see if we need a refresh
                if (isInspectorOpen() && refresh)
                    (_a = inspector.content.source) === null || _a === void 0 ? void 0 : _a.onEditorChange(text);
                else
                    openInspector(text);
            }
        });
        // Add inspector:close command to registry.
        const closeLabel = trans.__('Hide Contextual Help');
        commands.addCommand(CommandIDs.close, {
            caption,
            isEnabled: () => isInspectorOpen(),
            label: closeLabel,
            icon: args => (args.isLauncher ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.inspectorIcon : undefined),
            execute: () => closeInspector()
        });
        // Add inspector:toggle command to registry.
        const toggleLabel = trans.__('Show Contextual Help');
        commands.addCommand(CommandIDs.toggle, {
            caption,
            label: toggleLabel,
            isToggled: () => isInspectorOpen(),
            execute: args => {
                if (isInspectorOpen()) {
                    closeInspector();
                }
                else {
                    const text = args && args.text;
                    openInspector(text);
                }
            }
        });
        // Add open command to launcher if possible.
        if (launcher) {
            launcher.add({ command: CommandIDs.open, args: { isLauncher: true } });
        }
        // Add toggle command to command palette if possible.
        if (palette) {
            palette.addItem({ command: CommandIDs.toggle, category: toggleLabel });
        }
        // Handle state restoration.
        if (restorer) {
            void restorer.restore(tracker, {
                command: CommandIDs.toggle,
                name: () => 'inspector'
            });
        }
        // Create a proxy to pass the `source` to the current inspector.
        const proxy = Object.defineProperty({}, 'source', {
            get: () => !inspector || inspector.isDisposed ? null : inspector.content.source,
            set: (src) => {
                source = src && !src.isDisposed ? src : null;
                if (inspector && !inspector.isDisposed) {
                    inspector.content.source = source;
                }
            }
        });
        return proxy;
    }
};
/**
 * An extension that registers consoles for inspection.
 */
const consoles = {
    // FIXME This should be in @jupyterlab/console-extension
    id: '@jupyterlab/inspector-extension:consoles',
    description: 'Adds code introspection support to consoles.',
    requires: [_jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.IInspector, _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__.IConsoleTracker, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    autoStart: true,
    activate: (app, manager, consoles, labShell, translator) => {
        // Maintain association of new consoles with their respective handlers.
        const handlers = {};
        // Create a handler for each console that is created.
        consoles.widgetAdded.connect((sender, parent) => {
            const sessionContext = parent.console.sessionContext;
            const rendermime = parent.console.rendermime;
            const connector = new _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.KernelConnector({ sessionContext });
            const handler = new _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.InspectionHandler({ connector, rendermime });
            // Associate the handler to the widget.
            handlers[parent.id] = handler;
            // Set the initial editor.
            const cell = parent.console.promptCell;
            handler.editor = cell && cell.editor;
            // Listen for prompt creation.
            parent.console.promptCellCreated.connect((sender, cell) => {
                handler.editor = cell && cell.editor;
            });
            // Listen for parent disposal.
            parent.disposed.connect(() => {
                delete handlers[parent.id];
                handler.dispose();
            });
        });
        // Keep track of console instances and set inspector source.
        const setSource = (widget) => {
            if (widget && consoles.has(widget) && handlers[widget.id]) {
                manager.source = handlers[widget.id];
            }
        };
        labShell.currentChanged.connect((_, args) => setSource(args.newValue));
        void app.restored.then(() => setSource(labShell.currentWidget));
    }
};
/**
 * An extension that registers notebooks for inspection.
 */
const notebooks = {
    // FIXME This should be in @jupyterlab/notebook-extension
    id: '@jupyterlab/inspector-extension:notebooks',
    description: 'Adds code introspection to notebooks.',
    requires: [_jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.IInspector, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__.INotebookTracker, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    autoStart: true,
    activate: (app, manager, notebooks, labShell) => {
        // Maintain association of new notebooks with their respective handlers.
        const handlers = {};
        // Create a handler for each notebook that is created.
        notebooks.widgetAdded.connect((sender, parent) => {
            const sessionContext = parent.sessionContext;
            const rendermime = parent.content.rendermime;
            const connector = new _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.KernelConnector({ sessionContext });
            const handler = new _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.InspectionHandler({ connector, rendermime });
            // Associate the handler to the widget.
            handlers[parent.id] = handler;
            // Set the initial editor.
            const cell = parent.content.activeCell;
            handler.editor = cell && cell.editor;
            // Listen for active cell changes.
            parent.content.activeCellChanged.connect((sender, cell) => {
                void (cell === null || cell === void 0 ? void 0 : cell.ready.then(() => {
                    if (cell === parent.content.activeCell) {
                        handler.editor = cell.editor;
                    }
                }));
            });
            // Listen for parent disposal.
            parent.disposed.connect(() => {
                delete handlers[parent.id];
                handler.dispose();
            });
        });
        // Keep track of notebook instances and set inspector source.
        const setSource = (widget) => {
            if (widget && notebooks.has(widget) && handlers[widget.id]) {
                manager.source = handlers[widget.id];
            }
        };
        labShell.currentChanged.connect((_, args) => setSource(args.newValue));
        void app.restored.then(() => setSource(labShell.currentWidget));
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [inspector, consoles, notebooks];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=6011.d527b08d0d83d6a8dd9c.js.map?v=d527b08d0d83d6a8dd9c