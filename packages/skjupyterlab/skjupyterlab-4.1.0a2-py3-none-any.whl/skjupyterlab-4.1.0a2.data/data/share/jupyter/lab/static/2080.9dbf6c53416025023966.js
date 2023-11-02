"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[2080],{

/***/ 52080:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(65681);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(82545);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(51955);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(40200);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(2116);
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(78254);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(47698);
/* harmony import */ var _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(16564);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(35012);
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(94908);
/* harmony import */ var _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(56916);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(66866);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(89397);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module debugger-extension
 */














function notifyCommands(app) {
    Object.values(_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.CommandIDs).forEach(command => {
        if (app.commands.hasCommand(command)) {
            app.commands.notifyCommandChanged(command);
        }
    });
}
/**
 * A plugin that provides visual debugging support for consoles.
 */
const consoles = {
    // FIXME This should be in @jupyterlab/console-extension
    id: '@jupyterlab/debugger-extension:consoles',
    description: 'Add debugger capability to the consoles.',
    autoStart: true,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger, _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__.IConsoleTracker],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    activate: (app, debug, consoleTracker, labShell) => {
        const handler = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Handler({
            type: 'console',
            shell: app.shell,
            service: debug
        });
        const updateHandlerAndCommands = async (widget) => {
            const { sessionContext } = widget;
            await sessionContext.ready;
            await handler.updateContext(widget, sessionContext);
            notifyCommands(app);
        };
        if (labShell) {
            labShell.currentChanged.connect((_, update) => {
                const widget = update.newValue;
                if (widget instanceof _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__.ConsolePanel) {
                    void updateHandlerAndCommands(widget);
                }
            });
        }
        else {
            consoleTracker.currentChanged.connect((_, consolePanel) => {
                if (consolePanel) {
                    void updateHandlerAndCommands(consolePanel);
                }
            });
        }
    }
};
/**
 * A plugin that provides visual debugging support for file editors.
 */
const files = {
    // FIXME This should be in @jupyterlab/fileeditor-extension
    id: '@jupyterlab/debugger-extension:files',
    description: 'Adds debugger capabilities to files.',
    autoStart: true,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger, _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_8__.IEditorTracker],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    activate: (app, debug, editorTracker, labShell) => {
        const handler = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Handler({
            type: 'file',
            shell: app.shell,
            service: debug
        });
        const activeSessions = {};
        const updateHandlerAndCommands = async (widget) => {
            const sessions = app.serviceManager.sessions;
            try {
                const model = await sessions.findByPath(widget.context.path);
                if (!model) {
                    return;
                }
                let session = activeSessions[model.id];
                if (!session) {
                    // Use `connectTo` only if the session does not exist.
                    // `connectTo` sends a kernel_info_request on the shell
                    // channel, which blocks the debug session restore when waiting
                    // for the kernel to be ready
                    session = sessions.connectTo({ model });
                    activeSessions[model.id] = session;
                }
                await handler.update(widget, session);
                notifyCommands(app);
            }
            catch (_a) {
                return;
            }
        };
        if (labShell) {
            labShell.currentChanged.connect((_, update) => {
                const widget = update.newValue;
                if (widget instanceof _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_7__.DocumentWidget) {
                    const { content } = widget;
                    if (content instanceof _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_8__.FileEditor) {
                        void updateHandlerAndCommands(widget);
                    }
                }
            });
        }
        else {
            editorTracker.currentChanged.connect((_, documentWidget) => {
                if (documentWidget) {
                    void updateHandlerAndCommands(documentWidget);
                }
            });
        }
    }
};
/**
 * A plugin that provides visual debugging support for notebooks.
 */
const notebooks = {
    // FIXME This should be in @jupyterlab/notebook-extension
    id: '@jupyterlab/debugger-extension:notebooks',
    description: 'Adds debugger capability to notebooks and provides the debugger notebook handler.',
    autoStart: true,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.INotebookTracker],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ISessionContextDialogs, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.ITranslator],
    provides: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerHandler,
    activate: (app, service, notebookTracker, labShell, palette, sessionDialogs_, translator_) => {
        const translator = translator_ !== null && translator_ !== void 0 ? translator_ : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.nullTranslator;
        const sessionDialogs = sessionDialogs_ !== null && sessionDialogs_ !== void 0 ? sessionDialogs_ : new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SessionContextDialogs({ translator });
        const handler = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Handler({
            type: 'notebook',
            shell: app.shell,
            service
        });
        const trans = translator.load('jupyterlab');
        app.commands.addCommand(_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.CommandIDs.restartDebug, {
            label: trans.__('Restart Kernel and Debug…'),
            caption: trans.__('Restart Kernel and Debug…'),
            isEnabled: () => service.isStarted,
            execute: async () => {
                const state = service.getDebuggerState();
                await service.stop();
                const widget = notebookTracker.currentWidget;
                if (!widget) {
                    return;
                }
                const { content, sessionContext } = widget;
                const restarted = await sessionDialogs.restart(sessionContext);
                if (!restarted) {
                    return;
                }
                await service.restoreDebuggerState(state);
                await handler.updateWidget(widget, sessionContext.session);
                await _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.NotebookActions.runAll(content, sessionContext, sessionDialogs, translator);
            }
        });
        const updateHandlerAndCommands = async (widget) => {
            if (widget) {
                const { sessionContext } = widget;
                await sessionContext.ready;
                await handler.updateContext(widget, sessionContext);
            }
            notifyCommands(app);
        };
        if (labShell) {
            labShell.currentChanged.connect((_, update) => {
                const widget = update.newValue;
                if (widget instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.NotebookPanel) {
                    void updateHandlerAndCommands(widget);
                }
            });
        }
        else {
            notebookTracker.currentChanged.connect((_, notebookPanel) => {
                if (notebookPanel) {
                    void updateHandlerAndCommands(notebookPanel);
                }
            });
        }
        if (palette) {
            palette.addItem({
                category: 'Notebook Operations',
                command: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.CommandIDs.restartDebug
            });
        }
        return handler;
    }
};
/**
 * A plugin that provides a debugger service.
 */
const service = {
    id: '@jupyterlab/debugger-extension:service',
    description: 'Provides the debugger service.',
    autoStart: true,
    provides: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerConfig],
    optional: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerSources, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.ITranslator],
    activate: (app, config, debuggerSources, translator) => new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Service({
        config,
        debuggerSources,
        specsManager: app.serviceManager.kernelspecs,
        translator
    })
};
/**
 * A plugin that provides a configuration with hash method.
 */
const configuration = {
    id: '@jupyterlab/debugger-extension:config',
    description: 'Provides the debugger configuration',
    provides: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerConfig,
    autoStart: true,
    activate: () => new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Config()
};
/**
 * A plugin that provides source/editor functionality for debugging.
 */
const sources = {
    id: '@jupyterlab/debugger-extension:sources',
    description: 'Provides the source feature for debugging',
    autoStart: true,
    provides: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerSources,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerConfig, _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__.IEditorServices],
    optional: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.INotebookTracker, _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__.IConsoleTracker, _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_8__.IEditorTracker],
    activate: (app, config, editorServices, notebookTracker, consoleTracker, editorTracker) => {
        return new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Sources({
            config,
            shell: app.shell,
            editorServices,
            notebookTracker,
            consoleTracker,
            editorTracker
        });
    }
};
/*
 * A plugin to open detailed views for variables.
 */
const variables = {
    id: '@jupyterlab/debugger-extension:variables',
    description: 'Adds variables renderer and inspection in the debugger variable panel.',
    autoStart: true,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger, _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerHandler, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IThemeManager, _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_11__.IRenderMimeRegistry],
    activate: (app, service, handler, translator, themeManager, rendermime) => {
        const trans = translator.load('jupyterlab');
        const { commands, shell } = app;
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: 'debugger/inspect-variable'
        });
        const trackerMime = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: 'debugger/render-variable'
        });
        const CommandIDs = _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.CommandIDs;
        // Add commands
        commands.addCommand(CommandIDs.inspectVariable, {
            label: trans.__('Inspect Variable'),
            caption: trans.__('Inspect Variable'),
            isEnabled: args => {
                var _a, _b, _c, _d;
                return !!((_a = service.session) === null || _a === void 0 ? void 0 : _a.isStarted) &&
                    Number((_d = (_b = args.variableReference) !== null && _b !== void 0 ? _b : (_c = service.model.variables.selectedVariable) === null || _c === void 0 ? void 0 : _c.variablesReference) !== null && _d !== void 0 ? _d : 0) > 0;
            },
            execute: async (args) => {
                var _a, _b, _c, _d;
                let { variableReference, name } = args;
                if (!variableReference) {
                    variableReference =
                        (_a = service.model.variables.selectedVariable) === null || _a === void 0 ? void 0 : _a.variablesReference;
                }
                if (!name) {
                    name = (_b = service.model.variables.selectedVariable) === null || _b === void 0 ? void 0 : _b.name;
                }
                const id = `jp-debugger-variable-${name}`;
                if (!name ||
                    !variableReference ||
                    tracker.find(widget => widget.id === id)) {
                    return;
                }
                const variables = await service.inspectVariable(variableReference);
                if (!variables || variables.length === 0) {
                    return;
                }
                const model = service.model.variables;
                const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({
                    content: new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.VariablesGrid({
                        model,
                        commands,
                        scopes: [{ name, variables }],
                        themeManager
                    })
                });
                widget.addClass('jp-DebuggerVariables');
                widget.id = id;
                widget.title.icon = _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.variableIcon;
                widget.title.label = `${(_d = (_c = service.session) === null || _c === void 0 ? void 0 : _c.connection) === null || _d === void 0 ? void 0 : _d.name} - ${name}`;
                void tracker.add(widget);
                const disposeWidget = () => {
                    widget.dispose();
                    model.changed.disconnect(disposeWidget);
                };
                model.changed.connect(disposeWidget);
                shell.add(widget, 'main', {
                    mode: tracker.currentWidget ? 'split-right' : 'split-bottom',
                    activate: false,
                    type: 'Debugger Variables'
                });
            }
        });
        commands.addCommand(CommandIDs.renderMimeVariable, {
            label: trans.__('Render Variable'),
            caption: trans.__('Render variable according to its mime type'),
            isEnabled: () => { var _a; return !!((_a = service.session) === null || _a === void 0 ? void 0 : _a.isStarted); },
            isVisible: () => service.model.hasRichVariableRendering &&
                (rendermime !== null || handler.activeWidget instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.NotebookPanel),
            execute: args => {
                var _a, _b, _c, _d, _e, _f, _g, _h;
                let { name, frameId } = args;
                if (!name) {
                    name = (_a = service.model.variables.selectedVariable) === null || _a === void 0 ? void 0 : _a.name;
                }
                if (!frameId) {
                    frameId = (_b = service.model.callstack.frame) === null || _b === void 0 ? void 0 : _b.id;
                }
                const activeWidget = handler.activeWidget;
                let activeRendermime = activeWidget instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.NotebookPanel
                    ? activeWidget.content.rendermime
                    : rendermime;
                if (!activeRendermime) {
                    return;
                }
                const id = `jp-debugger-variable-mime-${name}-${(_d = (_c = service.session) === null || _c === void 0 ? void 0 : _c.connection) === null || _d === void 0 ? void 0 : _d.path.replace('/', '-')}`;
                if (!name || // Name is mandatory
                    trackerMime.find(widget => widget.id === id) || // Widget already exists
                    (!frameId && service.hasStoppedThreads()) // frame id missing on breakpoint
                ) {
                    return;
                }
                const variablesModel = service.model.variables;
                const widget = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.VariableRenderer({
                    dataLoader: () => service.inspectRichVariable(name, frameId),
                    rendermime: activeRendermime,
                    translator
                });
                widget.addClass('jp-DebuggerRichVariable');
                widget.id = id;
                widget.title.icon = _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.variableIcon;
                widget.title.label = `${name} - ${(_f = (_e = service.session) === null || _e === void 0 ? void 0 : _e.connection) === null || _f === void 0 ? void 0 : _f.name}`;
                widget.title.caption = `${name} - ${(_h = (_g = service.session) === null || _g === void 0 ? void 0 : _g.connection) === null || _h === void 0 ? void 0 : _h.path}`;
                void trackerMime.add(widget);
                const disposeWidget = () => {
                    widget.dispose();
                    variablesModel.changed.disconnect(refreshWidget);
                    activeWidget === null || activeWidget === void 0 ? void 0 : activeWidget.disposed.disconnect(disposeWidget);
                };
                const refreshWidget = () => {
                    // Refresh the widget only if the active element is the same.
                    if (handler.activeWidget === activeWidget) {
                        void widget.refresh();
                    }
                };
                widget.disposed.connect(disposeWidget);
                variablesModel.changed.connect(refreshWidget);
                activeWidget === null || activeWidget === void 0 ? void 0 : activeWidget.disposed.connect(disposeWidget);
                shell.add(widget, 'main', {
                    mode: trackerMime.currentWidget ? 'split-right' : 'split-bottom',
                    activate: false,
                    type: 'Debugger Variables'
                });
            }
        });
        commands.addCommand(CommandIDs.copyToClipboard, {
            label: trans.__('Copy to Clipboard'),
            caption: trans.__('Copy text representation of the value to clipboard'),
            isEnabled: () => {
                var _a, _b;
                return (!!((_a = service.session) === null || _a === void 0 ? void 0 : _a.isStarted) &&
                    !!((_b = service.model.variables.selectedVariable) === null || _b === void 0 ? void 0 : _b.value));
            },
            isVisible: () => handler.activeWidget instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.NotebookPanel,
            execute: async () => {
                const value = service.model.variables.selectedVariable.value;
                if (value) {
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Clipboard.copyToSystem(value);
                }
            }
        });
        commands.addCommand(CommandIDs.copyToGlobals, {
            label: trans.__('Copy Variable to Globals'),
            caption: trans.__('Copy variable to globals scope'),
            isEnabled: () => { var _a; return !!((_a = service.session) === null || _a === void 0 ? void 0 : _a.isStarted); },
            isVisible: () => handler.activeWidget instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.NotebookPanel &&
                service.model.supportCopyToGlobals,
            execute: async (args) => {
                const name = service.model.variables.selectedVariable.name;
                await service.copyToGlobals(name);
            }
        });
    }
};
/**
 * Debugger sidebar provider plugin.
 */
const sidebar = {
    id: '@jupyterlab/debugger-extension:sidebar',
    description: 'Provides the debugger sidebar.',
    provides: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerSidebar,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger, _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__.IEditorServices, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IThemeManager, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12__.ISettingRegistry],
    autoStart: true,
    activate: async (app, service, editorServices, translator, themeManager, settingRegistry) => {
        const { commands } = app;
        const CommandIDs = _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.CommandIDs;
        const callstackCommands = {
            registry: commands,
            continue: CommandIDs.debugContinue,
            terminate: CommandIDs.terminate,
            next: CommandIDs.next,
            stepIn: CommandIDs.stepIn,
            stepOut: CommandIDs.stepOut,
            evaluate: CommandIDs.evaluate
        };
        const breakpointsCommands = {
            registry: commands,
            pauseOnExceptions: CommandIDs.pauseOnExceptions
        };
        const sidebar = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Sidebar({
            service,
            callstackCommands,
            breakpointsCommands,
            editorServices,
            themeManager,
            translator
        });
        if (settingRegistry) {
            const setting = await settingRegistry.load(main.id);
            const updateSettings = () => {
                var _a, _b, _c, _d;
                const filters = setting.get('variableFilters').composite;
                const kernel = (_d = (_c = (_b = (_a = service.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.name) !== null && _d !== void 0 ? _d : '';
                if (kernel && filters[kernel]) {
                    sidebar.variables.filter = new Set(filters[kernel]);
                }
                const kernelSourcesFilter = setting.get('defaultKernelSourcesFilter')
                    .composite;
                sidebar.kernelSources.filter = kernelSourcesFilter;
            };
            updateSettings();
            setting.changed.connect(updateSettings);
            service.sessionChanged.connect(updateSettings);
        }
        return sidebar;
    }
};
/**
 * The main debugger UI plugin.
 */
const main = {
    id: '@jupyterlab/debugger-extension:main',
    description: 'Initialize the debugger user interface.',
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger, _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerSidebar, _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__.IEditorServices, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.ITranslator],
    optional: [
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerSources,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_9__.ILoggerRegistry,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12__.ISettingRegistry
    ],
    autoStart: true,
    activate: async (app, service, sidebar, editorServices, translator, palette, debuggerSources, labShell, restorer, loggerRegistry, settingRegistry) => {
        var _a;
        const trans = translator.load('jupyterlab');
        const { commands, shell, serviceManager } = app;
        const { kernelspecs } = serviceManager;
        const CommandIDs = _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.CommandIDs;
        // First check if there is a PageConfig override for the extension visibility
        const alwaysShowDebuggerExtension = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__.PageConfig.getOption('alwaysShowDebuggerExtension').toLowerCase() ===
            'true';
        if (!alwaysShowDebuggerExtension) {
            // hide the debugger sidebar if no kernel with support for debugging is available
            await kernelspecs.ready;
            const specs = (_a = kernelspecs.specs) === null || _a === void 0 ? void 0 : _a.kernelspecs;
            if (!specs) {
                return;
            }
            const enabled = Object.keys(specs).some(name => { var _a, _b, _c; return !!((_c = (_b = (_a = specs[name]) === null || _a === void 0 ? void 0 : _a.metadata) === null || _b === void 0 ? void 0 : _b['debugger']) !== null && _c !== void 0 ? _c : false); });
            if (!enabled) {
                return;
            }
        }
        // get the mime type of the kernel language for the current debug session
        const getMimeType = async () => {
            var _a, _b, _c;
            const kernel = (_b = (_a = service.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.kernel;
            if (!kernel) {
                return '';
            }
            const info = (await kernel.info).language_info;
            const name = info.name;
            const mimeType = (_c = editorServices.mimeTypeService.getMimeTypeByLanguage({ name })) !== null && _c !== void 0 ? _c : '';
            return mimeType;
        };
        const rendermime = new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_11__.RenderMimeRegistry({ initialFactories: _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_11__.standardRendererFactories });
        commands.addCommand(CommandIDs.evaluate, {
            label: trans.__('Evaluate Code'),
            caption: trans.__('Evaluate Code'),
            icon: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.evaluateIcon,
            isEnabled: () => service.hasStoppedThreads(),
            execute: async () => {
                var _a, _b, _c;
                const mimeType = await getMimeType();
                const result = await _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Dialogs.getCode({
                    title: trans.__('Evaluate Code'),
                    okLabel: trans.__('Evaluate'),
                    cancelLabel: trans.__('Cancel'),
                    mimeType,
                    contentFactory: new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__.CodeCell.ContentFactory({
                        editorFactory: options => editorServices.factoryService.newInlineEditor(options)
                    }),
                    rendermime
                });
                const code = result.value;
                if (!result.button.accept || !code) {
                    return;
                }
                const reply = await service.evaluate(code);
                if (reply) {
                    const data = reply.result;
                    const path = (_b = (_a = service === null || service === void 0 ? void 0 : service.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.path;
                    const logger = path ? (_c = loggerRegistry === null || loggerRegistry === void 0 ? void 0 : loggerRegistry.getLogger) === null || _c === void 0 ? void 0 : _c.call(loggerRegistry, path) : undefined;
                    if (logger) {
                        // print to log console of the notebook currently being debugged
                        logger.log({ type: 'text', data, level: logger.level });
                    }
                    else {
                        // fallback to printing to devtools console
                        console.debug(data);
                    }
                }
            }
        });
        commands.addCommand(CommandIDs.debugContinue, {
            label: () => {
                return service.hasStoppedThreads()
                    ? trans.__('Continue')
                    : trans.__('Pause');
            },
            caption: () => {
                return service.hasStoppedThreads()
                    ? trans.__('Continue')
                    : trans.__('Pause');
            },
            icon: () => {
                return service.hasStoppedThreads()
                    ? _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.continueIcon
                    : _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.pauseIcon;
            },
            isEnabled: () => { var _a, _b; return (_b = (_a = service.session) === null || _a === void 0 ? void 0 : _a.isStarted) !== null && _b !== void 0 ? _b : false; },
            execute: async () => {
                if (service.hasStoppedThreads()) {
                    await service.continue();
                }
                else {
                    await service.pause();
                }
                commands.notifyCommandChanged(CommandIDs.debugContinue);
            }
        });
        commands.addCommand(CommandIDs.terminate, {
            label: trans.__('Terminate'),
            caption: trans.__('Terminate'),
            icon: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.terminateIcon,
            isEnabled: () => service.hasStoppedThreads(),
            execute: async () => {
                await service.restart();
                notifyCommands(app);
            }
        });
        commands.addCommand(CommandIDs.next, {
            label: trans.__('Next'),
            caption: trans.__('Next'),
            icon: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.stepOverIcon,
            isEnabled: () => service.hasStoppedThreads(),
            execute: async () => {
                await service.next();
            }
        });
        commands.addCommand(CommandIDs.stepIn, {
            label: trans.__('Step In'),
            caption: trans.__('Step In'),
            icon: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.stepIntoIcon,
            isEnabled: () => service.hasStoppedThreads(),
            execute: async () => {
                await service.stepIn();
            }
        });
        commands.addCommand(CommandIDs.stepOut, {
            label: trans.__('Step Out'),
            caption: trans.__('Step Out'),
            icon: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.stepOutIcon,
            isEnabled: () => service.hasStoppedThreads(),
            execute: async () => {
                await service.stepOut();
            }
        });
        commands.addCommand(CommandIDs.pauseOnExceptions, {
            label: args => args.filter || 'Breakpoints on exception',
            caption: args => args.description,
            isToggled: args => { var _a; return ((_a = service.session) === null || _a === void 0 ? void 0 : _a.isPausingOnException(args.filter)) || false; },
            isEnabled: () => service.pauseOnExceptionsIsValid(),
            execute: async (args) => {
                var _a, _b, _c;
                if (args === null || args === void 0 ? void 0 : args.filter) {
                    let filter = args.filter;
                    await service.pauseOnExceptionsFilter(filter);
                }
                else {
                    let items = [];
                    (_b = (_a = service.session) === null || _a === void 0 ? void 0 : _a.exceptionBreakpointFilters) === null || _b === void 0 ? void 0 : _b.forEach(availableFilter => {
                        items.push(availableFilter.filter);
                    });
                    const result = await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getMultipleItems({
                        title: trans.__('Select a filter for breakpoints on exception'),
                        items: items,
                        defaults: ((_c = service.session) === null || _c === void 0 ? void 0 : _c.currentExceptionFilters) || []
                    });
                    let filters = result.button.accept ? result.value : null;
                    if (filters !== null) {
                        await service.pauseOnExceptions(filters);
                    }
                }
            }
        });
        let autoCollapseSidebar = false;
        if (settingRegistry) {
            const setting = await settingRegistry.load(main.id);
            const updateSettings = () => {
                autoCollapseSidebar = setting.get('autoCollapseDebuggerSidebar')
                    .composite;
            };
            updateSettings();
            setting.changed.connect(updateSettings);
        }
        service.eventMessage.connect((_, event) => {
            notifyCommands(app);
            if (labShell && event.event === 'initialized') {
                labShell.activateById(sidebar.id);
            }
            else if (labShell &&
                sidebar.isVisible &&
                event.event === 'terminated' &&
                autoCollapseSidebar) {
                labShell.collapseRight();
            }
        });
        service.sessionChanged.connect(_ => {
            notifyCommands(app);
        });
        if (restorer) {
            restorer.add(sidebar, 'debugger-sidebar');
        }
        sidebar.node.setAttribute('role', 'region');
        sidebar.node.setAttribute('aria-label', trans.__('Debugger section'));
        sidebar.title.caption = trans.__('Debugger');
        shell.add(sidebar, 'right', { type: 'Debugger' });
        commands.addCommand(CommandIDs.showPanel, {
            label: trans.__('Debugger Panel'),
            execute: () => {
                shell.activateById(sidebar.id);
            }
        });
        if (palette) {
            const category = trans.__('Debugger');
            [
                CommandIDs.debugContinue,
                CommandIDs.terminate,
                CommandIDs.next,
                CommandIDs.stepIn,
                CommandIDs.stepOut,
                CommandIDs.evaluate,
                CommandIDs.pauseOnExceptions
            ].forEach(command => {
                palette.addItem({ command, category });
            });
        }
        if (debuggerSources) {
            const { model } = service;
            const readOnlyEditorFactory = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.ReadOnlyEditorFactory({
                editorServices
            });
            const onCurrentFrameChanged = (_, frame) => {
                var _a, _b, _c, _d, _e, _f, _g, _h, _j;
                debuggerSources
                    .find({
                    focus: true,
                    kernel: (_d = (_c = (_b = (_a = service.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.name) !== null && _d !== void 0 ? _d : '',
                    path: (_g = (_f = (_e = service.session) === null || _e === void 0 ? void 0 : _e.connection) === null || _f === void 0 ? void 0 : _f.path) !== null && _g !== void 0 ? _g : '',
                    source: (_j = (_h = frame === null || frame === void 0 ? void 0 : frame.source) === null || _h === void 0 ? void 0 : _h.path) !== null && _j !== void 0 ? _j : ''
                })
                    .forEach(editor => {
                    requestAnimationFrame(() => {
                        void editor.reveal().then(() => {
                            const edit = editor.get();
                            if (edit) {
                                _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.EditorHandler.showCurrentLine(edit, frame.line);
                            }
                        });
                    });
                });
            };
            const onSourceOpened = (_, source, breakpoint) => {
                var _a, _b, _c, _d, _e, _f, _g;
                if (!source) {
                    return;
                }
                const { content, mimeType, path } = source;
                const results = debuggerSources.find({
                    focus: true,
                    kernel: (_d = (_c = (_b = (_a = service.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.name) !== null && _d !== void 0 ? _d : '',
                    path: (_g = (_f = (_e = service.session) === null || _e === void 0 ? void 0 : _e.connection) === null || _f === void 0 ? void 0 : _f.path) !== null && _g !== void 0 ? _g : '',
                    source: path
                });
                if (results.length > 0) {
                    if (breakpoint && typeof breakpoint.line !== 'undefined') {
                        results.forEach(editor => {
                            void editor.reveal().then(() => {
                                var _a;
                                (_a = editor.get()) === null || _a === void 0 ? void 0 : _a.revealPosition({
                                    line: breakpoint.line - 1,
                                    column: breakpoint.column || 0
                                });
                            });
                        });
                    }
                    return;
                }
                const editorWrapper = readOnlyEditorFactory.createNewEditor({
                    content,
                    mimeType,
                    path
                });
                const editor = editorWrapper.editor;
                const editorHandler = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.EditorHandler({
                    debuggerService: service,
                    editorReady: () => Promise.resolve(editor),
                    getEditor: () => editor,
                    path,
                    src: editor.model.sharedModel
                });
                editorWrapper.disposed.connect(() => editorHandler.dispose());
                debuggerSources.open({
                    label: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__.PathExt.basename(path),
                    caption: path,
                    editorWrapper
                });
                const frame = service.model.callstack.frame;
                if (frame) {
                    _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.EditorHandler.showCurrentLine(editor, frame.line);
                }
            };
            const onKernelSourceOpened = (_, source, breakpoint) => {
                if (!source) {
                    return;
                }
                onSourceOpened(null, source, breakpoint);
            };
            model.callstack.currentFrameChanged.connect(onCurrentFrameChanged);
            model.sources.currentSourceOpened.connect(onSourceOpened);
            model.kernelSources.kernelSourceOpened.connect(onKernelSourceOpened);
            model.breakpoints.clicked.connect(async (_, breakpoint) => {
                var _a;
                const path = (_a = breakpoint.source) === null || _a === void 0 ? void 0 : _a.path;
                const source = await service.getSource({
                    sourceReference: 0,
                    path
                });
                onSourceOpened(null, source, breakpoint);
            });
        }
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [
    service,
    consoles,
    files,
    notebooks,
    variables,
    sidebar,
    main,
    sources,
    configuration
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=2080.9dbf6c53416025023966.js.map?v=9dbf6c53416025023966