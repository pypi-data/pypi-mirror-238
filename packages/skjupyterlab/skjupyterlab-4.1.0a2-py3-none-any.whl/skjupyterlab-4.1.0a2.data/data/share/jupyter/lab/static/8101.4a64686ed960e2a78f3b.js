"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[8101,2074],{

/***/ 22074:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(65681);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(82545);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_extensionmanager__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(55064);
/* harmony import */ var _jupyterlab_extensionmanager__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_extensionmanager__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(89397);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(76351);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module extensionmanager-extension
 */






const PLUGIN_ID = '@jupyterlab/extensionmanager-extension:plugin';
/**
 * IDs of the commands added by this extension.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.showPanel = 'extensionmanager:show-panel';
    CommandIDs.toggle = 'extensionmanager:toggle';
})(CommandIDs || (CommandIDs = {}));
/**
 * The extension manager plugin.
 */
const plugin = {
    id: PLUGIN_ID,
    description: 'Adds the extension manager plugin.',
    autoStart: true,
    requires: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: async (app, registry, translator, restorer, palette) => {
        const { commands, shell, serviceManager } = app;
        translator = translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.nullTranslator;
        const trans = translator.load('jupyterlab');
        const model = new _jupyterlab_extensionmanager__WEBPACK_IMPORTED_MODULE_2__.ListModel(serviceManager, translator);
        const createView = () => {
            const v = new _jupyterlab_extensionmanager__WEBPACK_IMPORTED_MODULE_2__.ExtensionsPanel({ model, translator: translator });
            v.id = 'extensionmanager.main-view';
            v.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.extensionIcon;
            v.title.caption = trans.__('Extension Manager');
            v.node.setAttribute('role', 'region');
            v.node.setAttribute('aria-label', trans.__('Extension Manager section'));
            if (restorer) {
                restorer.add(v, v.id);
            }
            shell.add(v, 'left', { rank: 1000 });
            return v;
        };
        // Create a view by default, so it can be restored when loading the workspace.
        let view = createView();
        // If the extension is enabled or disabled,
        // add or remove it from the left area.
        Promise.all([app.restored, registry.load(PLUGIN_ID)])
            .then(([, settings]) => {
            model.isDisclaimed = settings.get('disclaimed').composite;
            model.isEnabled = settings.get('enabled').composite;
            model.stateChanged.connect(() => {
                if (model.isDisclaimed !==
                    settings.get('disclaimed').composite) {
                    settings.set('disclaimed', model.isDisclaimed).catch(reason => {
                        console.error(`Failed to set setting 'disclaimed'.\n${reason}`);
                    });
                }
                if (model.isEnabled !== settings.get('enabled').composite) {
                    settings.set('enabled', model.isEnabled).catch(reason => {
                        console.error(`Failed to set setting 'enabled'.\n${reason}`);
                    });
                }
            });
            if (model.isEnabled) {
                view = view !== null && view !== void 0 ? view : createView();
            }
            else {
                view === null || view === void 0 ? void 0 : view.dispose();
                view = null;
            }
            settings.changed.connect(async () => {
                model.isDisclaimed = settings.get('disclaimed').composite;
                model.isEnabled = settings.get('enabled').composite;
                app.commands.notifyCommandChanged(CommandIDs.toggle);
                if (model.isEnabled) {
                    if (view === null || !view.isAttached) {
                        const accepted = await Private.showWarning(trans);
                        if (!accepted) {
                            void settings.set('enabled', false);
                            return;
                        }
                    }
                    view = view !== null && view !== void 0 ? view : createView();
                }
                else {
                    view === null || view === void 0 ? void 0 : view.dispose();
                    view = null;
                }
            });
        })
            .catch(reason => {
            console.error(`Something went wrong when reading the settings.\n${reason}`);
        });
        commands.addCommand(CommandIDs.showPanel, {
            label: trans.__('Extension Manager'),
            execute: () => {
                if (view) {
                    shell.activateById(view.id);
                }
            },
            isVisible: () => model.isEnabled
        });
        commands.addCommand(CommandIDs.toggle, {
            label: trans.__('Enable Extension Manager'),
            execute: () => {
                if (registry) {
                    void registry.set(plugin.id, 'enabled', !model.isEnabled);
                }
            },
            isToggled: () => model.isEnabled
        });
        if (palette) {
            palette.addItem({
                command: CommandIDs.toggle,
                category: trans.__('Extension Manager')
            });
        }
    }
};
/**
 * Export the plugin as the default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * A namespace for module-private functions.
 */
var Private;
(function (Private) {
    /**
     * Show a warning dialog about extension security.
     *
     * @returns whether the user accepted the dialog.
     */
    async function showWarning(trans) {
        const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
            title: trans.__('Enable Extension Manager?'),
            body: trans.__(`Thanks for trying out JupyterLab's extension manager.
The JupyterLab development team is excited to have a robust
third-party extension community.
However, we cannot vouch for every extension,
and some may introduce security risks.
Do you want to continue?`),
            buttons: [
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: trans.__('Disable') }),
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: trans.__('Enable') })
            ]
        });
        return result.button.accept;
    }
    Private.showWarning = showWarning;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=8101.4a64686ed960e2a78f3b.js.map?v=4a64686ed960e2a78f3b