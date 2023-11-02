"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[3376,6656],{

/***/ 73376:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(65681);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(82545);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(35855);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(45534);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(76351);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(16415);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_6__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module launcher-extension
 */







/**
 * The command IDs used by the launcher plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.create = 'launcher:create';
})(CommandIDs || (CommandIDs = {}));
/**
 * A service providing an interface to the the launcher.
 */
const plugin = {
    activate,
    id: '@jupyterlab/launcher-extension:plugin',
    description: 'Provides the launcher tab service.',
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    optional: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__.IDefaultFileBrowser,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__.IFileBrowserFactory
    ],
    provides: _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__.ILauncher,
    autoStart: true
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * Activate the launcher.
 */
function activate(app, translator, labShell, palette, defaultBrowser, factory) {
    const { commands, shell } = app;
    const trans = translator.load('jupyterlab');
    const model = new _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__.LauncherModel();
    commands.addCommand(CommandIDs.create, {
        label: trans.__('New Launcher'),
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.addIcon : undefined),
        execute: (args) => {
            var _a, _b;
            const cwd = (_b = (_a = args['cwd']) !== null && _a !== void 0 ? _a : defaultBrowser === null || defaultBrowser === void 0 ? void 0 : defaultBrowser.model.path) !== null && _b !== void 0 ? _b : '';
            const id = `launcher-${Private.id++}`;
            const callback = (item) => {
                // If widget is attached to the main area replace the launcher
                if ((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_6__.find)(shell.widgets('main'), w => w === item)) {
                    shell.add(item, 'main', { ref: id });
                    launcher.dispose();
                }
            };
            const launcher = new _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__.Launcher({
                model,
                cwd,
                callback,
                commands,
                translator
            });
            launcher.model = model;
            launcher.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.launcherIcon;
            launcher.title.label = trans.__('Launcher');
            const main = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content: launcher });
            // If there are any other widgets open, remove the launcher close icon.
            main.title.closable = !!Array.from(shell.widgets('main')).length;
            main.id = id;
            shell.add(main, 'main', {
                activate: args['activate'],
                ref: args['ref']
            });
            if (labShell) {
                labShell.layoutModified.connect(() => {
                    // If there is only a launcher open, remove the close icon.
                    main.title.closable = Array.from(labShell.widgets('main')).length > 1;
                }, main);
            }
            if (defaultBrowser) {
                const onPathChanged = (model) => {
                    launcher.cwd = model.path;
                };
                defaultBrowser.model.pathChanged.connect(onPathChanged);
                launcher.disposed.connect(() => {
                    defaultBrowser.model.pathChanged.disconnect(onPathChanged);
                });
            }
            return main;
        }
    });
    if (labShell) {
        void Promise.all([app.restored, defaultBrowser === null || defaultBrowser === void 0 ? void 0 : defaultBrowser.model.restored]).then(() => {
            function maybeCreate() {
                // Create a launcher if there are no open items.
                if (labShell.isEmpty('main')) {
                    void commands.execute(CommandIDs.create);
                }
            }
            // When layout is modified, create a launcher if there are no open items.
            labShell.layoutModified.connect(() => {
                maybeCreate();
            });
        });
    }
    if (palette) {
        palette.addItem({
            command: CommandIDs.create,
            category: trans.__('Launcher')
        });
    }
    if (labShell) {
        labShell.addButtonEnabled = true;
        labShell.addRequested.connect((sender, arg) => {
            var _a;
            // Get the ref for the current tab of the tabbar which the add button was clicked
            const ref = ((_a = arg.currentTitle) === null || _a === void 0 ? void 0 : _a.owner.id) ||
                arg.titles[arg.titles.length - 1].owner.id;
            return commands.execute(CommandIDs.create, { ref });
        });
    }
    return model;
}
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * The incrementing id used for launcher widgets.
     */
    Private.id = 0;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=3376.b6038914879ad6435f3b.js.map?v=b6038914879ad6435f3b