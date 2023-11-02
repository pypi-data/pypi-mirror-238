"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[3766,2070],{

/***/ 43766:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommandIDs": () => (/* binding */ CommandIDs),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(65681);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(82545);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(78254);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module hub-extension
 */




/**
 * The command IDs used by the plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.controlPanel = 'hub:control-panel';
    CommandIDs.logout = 'hub:logout';
    CommandIDs.restart = 'hub:restart';
})(CommandIDs || (CommandIDs = {}));
/**
 * Activate the jupyterhub extension.
 */
function activateHubExtension(app, paths, translator, palette) {
    const trans = translator.load('jupyterlab');
    const hubHost = paths.urls.hubHost || '';
    const hubPrefix = paths.urls.hubPrefix || '';
    const hubUser = paths.urls.hubUser || '';
    const hubServerName = paths.urls.hubServerName || '';
    const baseUrl = paths.urls.base;
    // Bail if not running on JupyterHub.
    if (!hubPrefix) {
        return;
    }
    console.debug('hub-extension: Found configuration ', {
        hubHost: hubHost,
        hubPrefix: hubPrefix
    });
    // If hubServerName is set, use JupyterHub 1.0 URL.
    const restartUrl = hubServerName
        ? hubHost + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(hubPrefix, 'spawn', hubUser, hubServerName)
        : hubHost + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(hubPrefix, 'spawn');
    const { commands } = app;
    commands.addCommand(CommandIDs.restart, {
        label: trans.__('Restart Server'),
        caption: trans.__('Request that the Hub restart this server'),
        execute: () => {
            window.open(restartUrl, '_blank');
        }
    });
    commands.addCommand(CommandIDs.controlPanel, {
        label: trans.__('Hub Control Panel'),
        caption: trans.__('Open the Hub control panel in a new browser tab'),
        execute: () => {
            window.open(hubHost + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(hubPrefix, 'home'), '_blank');
        }
    });
    commands.addCommand(CommandIDs.logout, {
        label: trans.__('Log Out'),
        caption: trans.__('Log out of the Hub'),
        execute: () => {
            window.location.href = hubHost + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(baseUrl, 'logout');
        }
    });
    // Add palette items.
    if (palette) {
        const category = trans.__('Hub');
        palette.addItem({ category, command: CommandIDs.controlPanel });
        palette.addItem({ category, command: CommandIDs.logout });
    }
}
/**
 * Initialization data for the hub-extension.
 */
const hubExtension = {
    activate: activateHubExtension,
    id: '@jupyterlab/hub-extension:plugin',
    description: 'Registers commands related to the hub server',
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    autoStart: true
};
/**
 * Plugin to load menu description based on settings file
 */
const hubExtensionMenu = {
    activate: () => void 0,
    id: '@jupyterlab/hub-extension:menu',
    description: 'Adds hub related commands to the menu.',
    autoStart: true
};
/**
 * The default JupyterLab connection lost provider. This may be overridden
 * to provide custom behavior when a connection to the server is lost.
 *
 * If the application is being deployed within a JupyterHub context,
 * this will provide a dialog that prompts the user to restart the server.
 * Otherwise, it shows an error dialog.
 */
const connectionlost = {
    id: '@jupyterlab/hub-extension:connectionlost',
    description: 'Provides a service to be notified when the connection to the hub server is lost.',
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterLab.IInfo],
    activate: (app, paths, translator, info) => {
        const trans = translator.load('jupyterlab');
        const hubPrefix = paths.urls.hubPrefix || '';
        const baseUrl = paths.urls.base;
        // Return the default error message if not running on JupyterHub.
        if (!hubPrefix) {
            return _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ConnectionLost;
        }
        // If we are running on JupyterHub, return a dialog
        // that prompts the user to restart their server.
        let showingError = false;
        const onConnectionLost = async (manager, err) => {
            if (showingError) {
                return;
            }
            showingError = true;
            if (info) {
                info.isConnected = false;
            }
            const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: trans.__('Server unavailable or unreachable'),
                body: trans.__('Your server at %1 is not running.\nWould you like to restart it?', baseUrl),
                buttons: [
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Restart') }),
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: trans.__('Dismiss') })
                ]
            });
            if (info) {
                info.isConnected = true;
            }
            showingError = false;
            if (result.button.accept) {
                await app.commands.execute(CommandIDs.restart);
            }
        };
        return onConnectionLost;
    },
    autoStart: true,
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IConnectionLost
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([
    hubExtension,
    hubExtensionMenu,
    connectionlost
]);


/***/ })

}]);
//# sourceMappingURL=3766.f013762d71984ba94462.js.map?v=f013762d71984ba94462