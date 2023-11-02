"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[9297,3460],{

/***/ 93460:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(2116);
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(78254);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(35012);
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(56916);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(66866);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(915);
/* harmony import */ var _jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(16415);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(72234);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_8__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module tooltip-extension
 */









/**
 * The command IDs used by the tooltip plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.dismiss = 'tooltip:dismiss';
    CommandIDs.launchConsole = 'tooltip:launch-console';
    CommandIDs.launchNotebook = 'tooltip:launch-notebook';
    CommandIDs.launchFile = 'tooltip:launch-file';
})(CommandIDs || (CommandIDs = {}));
/**
 * The main tooltip manager plugin.
 */
const manager = {
    id: '@jupyterlab/tooltip-extension:manager',
    description: 'Provides the tooltip manager.',
    autoStart: true,
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    provides: _jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__.ITooltipManager,
    activate: (app, translator) => {
        const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator).load('jupyterlab');
        let tooltip = null;
        // Add tooltip dismiss command.
        app.commands.addCommand(CommandIDs.dismiss, {
            label: trans.__('Dismiss the tooltip'),
            execute: () => {
                if (tooltip) {
                    tooltip.dispose();
                    tooltip = null;
                }
            }
        });
        return {
            invoke(options) {
                const detail = 0;
                const { anchor, editor, kernel, rendermime } = options;
                if (tooltip) {
                    tooltip.dispose();
                    tooltip = null;
                }
                return Private.fetch({ detail, editor, kernel })
                    .then(bundle => {
                    tooltip = new _jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__.Tooltip({ anchor, bundle, editor, rendermime });
                    _lumino_widgets__WEBPACK_IMPORTED_MODULE_8__.Widget.attach(tooltip, document.body);
                })
                    .catch(() => {
                    /* Fails silently. */
                });
            }
        };
    }
};
/**
 * The console tooltip plugin.
 */
const consoles = {
    // FIXME This should be in @jupyterlab/console-extension
    id: '@jupyterlab/tooltip-extension:consoles',
    description: 'Adds the tooltip capability to consoles.',
    autoStart: true,
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    requires: [_jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__.ITooltipManager, _jupyterlab_console__WEBPACK_IMPORTED_MODULE_0__.IConsoleTracker],
    activate: (app, manager, consoles, translator) => {
        const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator).load('jupyterlab');
        // Add tooltip launch command.
        app.commands.addCommand(CommandIDs.launchConsole, {
            label: trans.__('Open the tooltip'),
            execute: () => {
                var _a, _b;
                const parent = consoles.currentWidget;
                if (!parent) {
                    return;
                }
                const anchor = parent.console;
                const editor = (_a = anchor.promptCell) === null || _a === void 0 ? void 0 : _a.editor;
                const kernel = (_b = anchor.sessionContext.session) === null || _b === void 0 ? void 0 : _b.kernel;
                const rendermime = anchor.rendermime;
                // If all components necessary for rendering exist, create a tooltip.
                if (!!editor && !!kernel && !!rendermime) {
                    return manager.invoke({ anchor, editor, kernel, rendermime });
                }
            }
        });
    }
};
/**
 * The notebook tooltip plugin.
 */
const notebooks = {
    // FIXME This should be in @jupyterlab/notebook-extension
    id: '@jupyterlab/tooltip-extension:notebooks',
    description: 'Adds the tooltip capability to notebooks.',
    autoStart: true,
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    requires: [_jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__.ITooltipManager, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.INotebookTracker],
    activate: (app, manager, notebooks, translator) => {
        const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator).load('jupyterlab');
        // Add tooltip launch command.
        app.commands.addCommand(CommandIDs.launchNotebook, {
            label: trans.__('Open the tooltip'),
            execute: () => {
                var _a, _b;
                const parent = notebooks.currentWidget;
                if (!parent) {
                    return;
                }
                const anchor = parent.content;
                const editor = (_a = anchor.activeCell) === null || _a === void 0 ? void 0 : _a.editor;
                const kernel = (_b = parent.sessionContext.session) === null || _b === void 0 ? void 0 : _b.kernel;
                const rendermime = anchor.rendermime;
                // If all components necessary for rendering exist, create a tooltip.
                if (!!editor && !!kernel && !!rendermime) {
                    return manager.invoke({ anchor, editor, kernel, rendermime });
                }
            }
        });
    }
};
/**
 * The file editor tooltip plugin.
 */
const files = {
    // FIXME This should be in @jupyterlab/fileeditor-extension
    id: '@jupyterlab/tooltip-extension:files',
    description: 'Adds the tooltip capability to file editors.',
    autoStart: true,
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    requires: [_jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__.ITooltipManager, _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2__.IEditorTracker, _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__.IRenderMimeRegistry],
    activate: (app, manager, editorTracker, rendermime, translator) => {
        const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator).load('jupyterlab');
        // Keep a list of active ISessions so that we can
        // clean them up when they are no longer needed.
        const activeSessions = {};
        const sessions = app.serviceManager.sessions;
        // When the list of running sessions changes,
        // check to see if there are any kernels with a
        // matching path for the file editors.
        const onRunningChanged = (sender, models) => {
            editorTracker.forEach(file => {
                const model = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_7__.find)(models, m => file.context.path === m.path);
                if (model) {
                    const oldSession = activeSessions[file.id];
                    // If there is a matching path, but it is the same
                    // session as we previously had, do nothing.
                    if (oldSession && oldSession.id === model.id) {
                        return;
                    }
                    // Otherwise, dispose of the old session and reset to
                    // a new CompletionConnector.
                    if (oldSession) {
                        delete activeSessions[file.id];
                        oldSession.dispose();
                    }
                    const session = sessions.connectTo({ model });
                    activeSessions[file.id] = session;
                }
                else {
                    const session = activeSessions[file.id];
                    if (session) {
                        session.dispose();
                        delete activeSessions[file.id];
                    }
                }
            });
        };
        onRunningChanged(sessions, sessions.running());
        sessions.runningChanged.connect(onRunningChanged);
        // Clean up after a widget when it is disposed
        editorTracker.widgetAdded.connect((sender, widget) => {
            widget.disposed.connect(w => {
                const session = activeSessions[w.id];
                if (session) {
                    session.dispose();
                    delete activeSessions[w.id];
                }
            });
        });
        // Add tooltip launch command.
        app.commands.addCommand(CommandIDs.launchFile, {
            label: trans.__('Open the tooltip'),
            execute: async () => {
                const parent = editorTracker.currentWidget;
                const kernel = parent &&
                    activeSessions[parent.id] &&
                    activeSessions[parent.id].kernel;
                if (!kernel) {
                    return;
                }
                const anchor = parent.content;
                const editor = anchor === null || anchor === void 0 ? void 0 : anchor.editor;
                // If all components necessary for rendering exist, create a tooltip.
                if (!!editor && !!kernel && !!rendermime) {
                    return manager.invoke({ anchor, editor, kernel, rendermime });
                }
            }
        });
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [
    manager,
    consoles,
    notebooks,
    files
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * A counter for outstanding requests.
     */
    let pending = 0;
    /**
     * Fetch a tooltip's content from the API server.
     */
    function fetch(options) {
        const { detail, editor, kernel } = options;
        const code = editor.model.sharedModel.getSource();
        const position = editor.getCursorPosition();
        const offset = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.Text.jsIndexToCharIndex(editor.getOffsetAt(position), code);
        // Clear hints if the new text value is empty or kernel is unavailable.
        if (!code || !kernel) {
            return Promise.reject(void 0);
        }
        const contents = {
            code,
            cursor_pos: offset,
            detail_level: detail || 0
        };
        const current = ++pending;
        return kernel.requestInspect(contents).then(msg => {
            const value = msg.content;
            // If a newer request is pending, bail.
            if (current !== pending) {
                return Promise.reject(void 0);
            }
            // If request fails or returns negative results, bail.
            if (value.status !== 'ok' || !value.found) {
                return Promise.reject(void 0);
            }
            return Promise.resolve(value.data);
        });
    }
    Private.fetch = fetch;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=9297.d0875ea00530db198d37.js.map?v=d0875ea00530db198d37