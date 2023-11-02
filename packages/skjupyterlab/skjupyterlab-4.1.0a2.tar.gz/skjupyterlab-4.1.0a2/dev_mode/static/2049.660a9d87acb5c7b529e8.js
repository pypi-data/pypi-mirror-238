"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[2049,3284],{

/***/ 82049:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(65681);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(82545);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(5184);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(89397);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__);
/* ----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module translation-extension
 */





/**
 * Translation plugins
 */
const PLUGIN_ID = '@jupyterlab/translation-extension:plugin';
const translator = {
    id: '@jupyterlab/translation:translator',
    description: 'Provides the application translation object.',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    provides: _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator,
    activate: async (app, paths, settings, labShell) => {
        const setting = await settings.load(PLUGIN_ID);
        const currentLocale = setting.get('locale').composite;
        let stringsPrefix = setting.get('stringsPrefix')
            .composite;
        const displayStringsPrefix = setting.get('displayStringsPrefix')
            .composite;
        stringsPrefix = displayStringsPrefix ? stringsPrefix : '';
        const serverSettings = app.serviceManager.serverSettings;
        const translationManager = new _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.TranslationManager(paths.urls.translations, stringsPrefix, serverSettings);
        await translationManager.fetch(currentLocale);
        // Set translator to UI
        if (labShell) {
            labShell.translator = translationManager;
        }
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.translator = translationManager;
        return translationManager;
    }
};
/**
 * Initialization data for the extension.
 */
const langMenu = {
    id: PLUGIN_ID,
    description: 'Adds translation commands and settings.',
    requires: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    optional: [_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__.IMainMenu, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    autoStart: true,
    activate: (app, settings, translator, mainMenu, palette) => {
        const trans = translator.load('jupyterlab');
        const { commands } = app;
        let currentLocale;
        /**
         * Load the settings for this extension
         *
         * @param setting Extension settings
         */
        function loadSetting(setting) {
            // Read the settings and convert to the correct type
            currentLocale = setting.get('locale').composite;
        }
        settings
            .load(PLUGIN_ID)
            .then(setting => {
            var _a;
            // Read the settings
            loadSetting(setting);
            // Ensure currentLocale is not 'default' which is not a valid language code
            if (currentLocale !== 'default') {
                document.documentElement.lang = (currentLocale !== null && currentLocale !== void 0 ? currentLocale : '').replace('_', '-');
            }
            else {
                document.documentElement.lang = 'en-US';
            }
            // Listen for your plugin setting changes using Signal
            setting.changed.connect(loadSetting);
            // Create a languages menu
            const languagesMenu = mainMenu
                ? (_a = mainMenu.settingsMenu.items.find(item => {
                    var _a;
                    return item.type === 'submenu' &&
                        ((_a = item.submenu) === null || _a === void 0 ? void 0 : _a.id) === 'jp-mainmenu-settings-language';
                })) === null || _a === void 0 ? void 0 : _a.submenu
                : null;
            let command;
            const serverSettings = app.serviceManager.serverSettings;
            // Get list of available locales
            (0,_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.requestTranslationsAPI)('', '', {}, serverSettings)
                .then(data => {
                for (const locale in data['data']) {
                    const value = data['data'][locale];
                    const displayName = value.displayName;
                    const nativeName = value.nativeName;
                    const toggled = displayName === nativeName;
                    const label = toggled
                        ? `${displayName}`
                        : `${displayName} - ${nativeName}`;
                    // Add a command per language
                    command = `jupyterlab-translation:${locale}`;
                    commands.addCommand(command, {
                        label: label,
                        caption: label,
                        isEnabled: () => !toggled,
                        isVisible: () => true,
                        isToggled: () => toggled,
                        execute: () => {
                            return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                                title: trans.__('Change interface language?'),
                                body: trans.__('After changing the interface language to %1, you will need to reload JupyterLab to see the changes.', label),
                                buttons: [
                                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: trans.__('Cancel') }),
                                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Change and reload') })
                                ]
                            }).then(result => {
                                if (result.button.accept) {
                                    setting
                                        .set('locale', locale)
                                        .then(() => {
                                        window.location.reload();
                                    })
                                        .catch(reason => {
                                        console.error(reason);
                                    });
                                }
                            });
                        }
                    });
                    // Add the language command to the menu
                    if (languagesMenu) {
                        languagesMenu.addItem({
                            command,
                            args: {}
                        });
                    }
                    if (palette) {
                        palette.addItem({
                            category: trans.__('Display Languages'),
                            command
                        });
                    }
                }
            })
                .catch(reason => {
                console.error(`Available locales errored!\n${reason}`);
            });
        })
            .catch(reason => {
            console.error(`The jupyterlab translation extension appears to be missing.\n${reason}`);
        });
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [translator, langMenu];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=2049.660a9d87acb5c7b529e8.js.map?v=660a9d87acb5c7b529e8