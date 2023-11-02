"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[8321,5104,7967],{

/***/ 8321:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(65681);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(82545);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(40200);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(76351);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(66866);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_settingeditor_lib_tokens__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(45104);
/* harmony import */ var _jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(42819);
/* harmony import */ var _jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(89397);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(1458);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module settingeditor-extension
 */











/**
 * The command IDs used by the setting editor.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'settingeditor:open';
    CommandIDs.openJSON = 'settingeditor:open-json';
    CommandIDs.revert = 'settingeditor:revert';
    CommandIDs.save = 'settingeditor:save';
})(CommandIDs || (CommandIDs = {}));
/**
 * The default setting editor extension.
 */
const plugin = {
    id: '@jupyterlab/settingeditor-extension:form-ui',
    description: 'Adds the interactive settings editor and provides its tracker.',
    requires: [
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__.ISettingRegistry,
        _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_7__.IStateDB,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator,
        _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.IFormRendererRegistry,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabStatus
    ],
    optional: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_settingeditor_lib_tokens__WEBPACK_IMPORTED_MODULE_9__/* .IJSONSettingEditorTracker */ .g,
        _jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_5__.IPluginManager
    ],
    autoStart: true,
    provides: _jupyterlab_settingeditor_lib_tokens__WEBPACK_IMPORTED_MODULE_9__/* .ISettingEditorTracker */ .O,
    activate
};
/**
 * Activate the setting editor extension.
 */
function activate(app, registry, state, translator, editorRegistry, status, restorer, palette, jsonEditor, pluginManager) {
    const trans = translator.load('jupyterlab');
    const { commands, shell } = app;
    const namespace = 'setting-editor';
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace
    });
    // Handle state restoration.
    if (restorer) {
        void restorer.restore(tracker, {
            command: CommandIDs.open,
            args: widget => ({}),
            name: widget => namespace
        });
    }
    const openUi = async (args) => {
        if (tracker.currentWidget && !tracker.currentWidget.isDisposed) {
            if (!tracker.currentWidget.isAttached) {
                shell.add(tracker.currentWidget, 'main', { type: 'Settings' });
            }
            shell.activateById(tracker.currentWidget.id);
            return;
        }
        const key = plugin.id;
        const { SettingsEditor } = await __webpack_require__.e(/* import() */ 5365).then(__webpack_require__.t.bind(__webpack_require__, 15365, 23));
        const editor = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({
            content: new SettingsEditor({
                editorRegistry,
                key,
                registry,
                state,
                commands,
                toSkip: [
                    '@jupyterlab/application-extension:context-menu',
                    '@jupyterlab/mainmenu-extension:plugin'
                ],
                translator,
                status,
                query: args.query
            })
        });
        editor.toolbar.addItem('spacer', _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.Toolbar.createSpacerItem());
        if (pluginManager) {
            editor.toolbar.addItem('open-plugin-manager', new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.ToolbarButton({
                onClick: async () => {
                    await pluginManager.open();
                },
                icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.launchIcon,
                label: trans.__('Plugin Manager')
            }));
        }
        if (jsonEditor) {
            editor.toolbar.addItem('open-json-editor', new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.CommandToolbarButton({
                commands,
                id: CommandIDs.openJSON,
                icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.launchIcon,
                label: trans.__('JSON Settings Editor')
            }));
        }
        editor.id = namespace;
        editor.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.settingsIcon;
        editor.title.label = trans.__('Settings');
        editor.title.closable = true;
        void tracker.add(editor);
        shell.add(editor, 'main', { type: 'Settings' });
    };
    commands.addCommand(CommandIDs.open, {
        execute: async (args) => {
            var _a;
            if (args.settingEditorType === 'ui') {
                void commands.execute(CommandIDs.open, { query: (_a = args.query) !== null && _a !== void 0 ? _a : '' });
            }
            else if (args.settingEditorType === 'json') {
                void commands.execute(CommandIDs.openJSON);
            }
            else {
                void registry.load(plugin.id).then(settings => {
                    var _a;
                    settings.get('settingEditorType').composite ===
                        'json'
                        ? void commands.execute(CommandIDs.openJSON)
                        : void openUi({ query: (_a = args.query) !== null && _a !== void 0 ? _a : '' });
                });
            }
        },
        label: args => {
            if (args.label) {
                return args.label;
            }
            return trans.__('Settings Editor');
        }
    });
    if (palette) {
        palette.addItem({
            category: trans.__('Settings'),
            command: CommandIDs.open,
            args: { settingEditorType: 'ui' }
        });
    }
    return tracker;
}
/**
 * The default setting editor extension.
 */
const jsonPlugin = {
    id: '@jupyterlab/settingeditor-extension:plugin',
    description: 'Adds the JSON settings editor and provides its tracker.',
    requires: [
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__.ISettingRegistry,
        _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__.IEditorServices,
        _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_7__.IStateDB,
        _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__.IRenderMimeRegistry,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabStatus,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator
    ],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    autoStart: true,
    provides: _jupyterlab_settingeditor_lib_tokens__WEBPACK_IMPORTED_MODULE_9__/* .IJSONSettingEditorTracker */ .g,
    activate: activateJSON
};
/**
 * Activate the setting editor extension.
 */
function activateJSON(app, registry, editorServices, state, rendermime, status, translator, restorer, palette) {
    const trans = translator.load('jupyterlab');
    const { commands, shell } = app;
    const namespace = 'json-setting-editor';
    const factoryService = editorServices.factoryService;
    const editorFactory = factoryService.newInlineEditor;
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace
    });
    // Handle state restoration.
    if (restorer) {
        void restorer.restore(tracker, {
            command: CommandIDs.openJSON,
            args: widget => ({}),
            name: widget => namespace
        });
    }
    commands.addCommand(CommandIDs.openJSON, {
        execute: async () => {
            if (tracker.currentWidget && !tracker.currentWidget.isDisposed) {
                if (!tracker.currentWidget.isAttached) {
                    shell.add(tracker.currentWidget, 'main', {
                        type: 'Advanced Settings'
                    });
                }
                shell.activateById(tracker.currentWidget.id);
                return;
            }
            const key = plugin.id;
            const when = app.restored;
            const { JsonSettingEditor } = await __webpack_require__.e(/* import() */ 5365).then(__webpack_require__.t.bind(__webpack_require__, 15365, 23));
            const editor = new JsonSettingEditor({
                commands: {
                    registry: commands,
                    revert: CommandIDs.revert,
                    save: CommandIDs.save
                },
                editorFactory,
                key,
                registry,
                rendermime,
                state,
                translator,
                when
            });
            let disposable = null;
            // Notify the command registry when the visibility status of the setting
            // editor's commands change. The setting editor toolbar listens for this
            // signal from the command registry.
            editor.commandsChanged.connect((sender, args) => {
                args.forEach(id => {
                    commands.notifyCommandChanged(id);
                });
                if (editor.canSaveRaw) {
                    if (!disposable) {
                        disposable = status.setDirty();
                    }
                }
                else if (disposable) {
                    disposable.dispose();
                    disposable = null;
                }
                editor.disposed.connect(() => {
                    if (disposable) {
                        disposable.dispose();
                    }
                });
            });
            const container = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({
                content: editor
            });
            container.id = namespace;
            container.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.settingsIcon;
            container.title.label = trans.__('Advanced Settings Editor');
            container.title.closable = true;
            void tracker.add(container);
            shell.add(container, 'main', { type: 'Advanced Settings' });
        },
        label: trans.__('Advanced Settings Editor')
    });
    if (palette) {
        palette.addItem({
            category: trans.__('Settings'),
            command: CommandIDs.openJSON
        });
    }
    commands.addCommand(CommandIDs.revert, {
        execute: () => {
            var _a;
            (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.revert();
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.undoIcon,
        label: trans.__('Revert User Settings'),
        isEnabled: () => { var _a, _b; return (_b = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.canRevertRaw) !== null && _b !== void 0 ? _b : false; }
    });
    commands.addCommand(CommandIDs.save, {
        execute: () => { var _a; return (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.save(); },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.saveIcon,
        label: trans.__('Save User Settings'),
        isEnabled: () => { var _a, _b; return (_b = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.canSaveRaw) !== null && _b !== void 0 ? _b : false; }
    });
    return tracker;
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([plugin, jsonPlugin]);


/***/ }),

/***/ 45104:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "O": () => (/* binding */ ISettingEditorTracker),
/* harmony export */   "g": () => (/* binding */ IJSONSettingEditorTracker)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(22100);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The setting editor tracker token.
 */
const ISettingEditorTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/settingeditor:ISettingEditorTracker', `A widget tracker for the interactive setting editor.
  Use this if you want to be able to iterate over and interact with setting editors
  created by the application.`);
/**
 * The setting editor tracker token.
 */
const IJSONSettingEditorTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/settingeditor:IJSONSettingEditorTracker', `A widget tracker for the JSON setting editor.
  Use this if you want to be able to iterate over and interact with setting editors
  created by the application.`);


/***/ })

}]);
//# sourceMappingURL=8321.cb3370c89607dac2ae3c.js.map?v=cb3370c89607dac2ae3c