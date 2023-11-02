"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[1883,7267],{

/***/ 47267:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(65681);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(82545);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(89397);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(34853);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module statusbar-extension
 */





const STATUSBAR_PLUGIN_ID = '@jupyterlab/statusbar-extension:plugin';
/**
 * Initialization data for the statusbar extension.
 */
const statusBar = {
    id: STATUSBAR_PLUGIN_ID,
    description: 'Provides the application status bar.',
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    provides: _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_3__.IStatusBar,
    autoStart: true,
    activate: (app, translator, labShell, settingRegistry, palette) => {
        const trans = translator.load('jupyterlab');
        const statusBar = new _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_3__.StatusBar();
        statusBar.id = 'jp-main-statusbar';
        app.shell.add(statusBar, 'bottom');
        // If available, connect to the shell's layout modified signal.
        if (labShell) {
            labShell.layoutModified.connect(() => {
                statusBar.update();
            });
        }
        const category = trans.__('Main Area');
        const command = 'statusbar:toggle';
        app.commands.addCommand(command, {
            label: trans.__('Show Status Bar'),
            execute: () => {
                statusBar.setHidden(statusBar.isVisible);
                if (settingRegistry) {
                    void settingRegistry.set(STATUSBAR_PLUGIN_ID, 'visible', statusBar.isVisible);
                }
            },
            isToggled: () => statusBar.isVisible
        });
        app.commands.commandExecuted.connect((registry, executed) => {
            if (executed.id === 'application:reset-layout' && !statusBar.isVisible) {
                app.commands.execute(command).catch(reason => {
                    console.error('Failed to show the status bar.', reason);
                });
            }
        });
        if (palette) {
            palette.addItem({ command, category });
        }
        if (settingRegistry) {
            const loadSettings = settingRegistry.load(STATUSBAR_PLUGIN_ID);
            const updateSettings = (settings) => {
                const visible = settings.get('visible').composite;
                statusBar.setHidden(!visible);
            };
            Promise.all([loadSettings, app.restored])
                .then(([settings]) => {
                updateSettings(settings);
                settings.changed.connect(settings => {
                    updateSettings(settings);
                });
            })
                .catch((reason) => {
                console.error(reason.message);
            });
        }
        return statusBar;
    },
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette]
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (statusBar);


/***/ })

}]);
//# sourceMappingURL=1883.346e72b82d877b338f9e.js.map?v=346e72b82d877b338f9e