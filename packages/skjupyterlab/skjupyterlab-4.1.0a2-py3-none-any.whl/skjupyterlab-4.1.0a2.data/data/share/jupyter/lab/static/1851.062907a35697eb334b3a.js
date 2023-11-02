"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[1851,3580],{

/***/ 63580:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(65681);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(82545);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(76351);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(42819);
/* harmony import */ var _jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_4__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module pluginmanager-extension
 */





/**
 * The command IDs used by the pluginmanager plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'pluginmanager:open';
    CommandIDs.refreshPlugins = 'pluginmanager:refresh';
})(CommandIDs || (CommandIDs = {}));
const PLUGIN_ID = '@jupyterlab/pluginmanager-extension:plugin';
/**
 * A plugin for managing status of other plugins.
 */
const pluginmanager = {
    id: PLUGIN_ID,
    description: 'Enable or disable individual plugins.',
    autoStart: true,
    requires: [],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.ITranslator, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    provides: _jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_4__.IPluginManager,
    activate: (app, translator, palette, restorer) => {
        const { commands, shell } = app;
        translator = translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        const trans = translator.load('jupyterlab');
        // Translation strings.
        const category = trans.__('Plugin Manager');
        const widgetLabel = trans.__('Advanced Plugin Manager');
        const refreshPlugins = trans.__('Refresh Plugin List');
        const namespace = 'plugin-manager';
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: namespace
        });
        /**
         * Create a MainAreaWidget for Plugin Manager.
         */
        function createWidget(args) {
            const model = new _jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_4__.PluginListModel({
                ...args,
                pluginData: {
                    availablePlugins: app.info.availablePlugins
                },
                serverSettings: app.serviceManager.serverSettings,
                extraLockedPlugins: [
                    PLUGIN_ID,
                    // UI will not proceed beyond splash without `layout` plugin
                    '@jupyterlab/application-extension:layout',
                    // State restoration does not work well without resolver,
                    // can leave user locked out of the plugin manager
                    // (if command palette and menu are disabled too)
                    '@jupyterlab/apputils-extension:resolver'
                ],
                translator: translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator
            });
            const content = new _jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_4__.Plugins({
                model,
                translator: translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator
            });
            content.title.label = widgetLabel;
            content.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.extensionIcon;
            const main = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content, reveal: model.ready });
            main.toolbar.addItem('refresh-plugins', new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.CommandToolbarButton({
                id: CommandIDs.refreshPlugins,
                args: { noLabel: true },
                commands
            }));
            return main;
        }
        // Register commands.
        commands.addCommand(CommandIDs.open, {
            label: widgetLabel,
            execute: args => {
                const main = createWidget(args);
                shell.add(main, 'main', { type: 'Plugins' });
                // add to tracker so it can be restored, and update when choices change
                void tracker.add(main);
                main.content.model.trackerDataChanged.connect(() => {
                    void tracker.save(main);
                });
                return main;
            }
        });
        commands.addCommand(CommandIDs.refreshPlugins, {
            label: args => (args.noLabel ? '' : refreshPlugins),
            caption: trans.__('Refresh plugins list'),
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.refreshIcon,
            execute: async () => {
                var _a;
                return (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.model.refresh().catch((reason) => {
                    console.error(`Failed to refresh the available plugins list:\n${reason}`);
                });
            }
        });
        if (palette) {
            palette.addItem({ command: CommandIDs.open, category });
        }
        if (restorer) {
            void restorer.restore(tracker, {
                command: CommandIDs.open,
                name: _ => 'plugins',
                args: widget => {
                    const { query, isDisclaimed } = widget.content.model;
                    const args = {
                        query,
                        isDisclaimed
                    };
                    return args;
                }
            });
        }
        return {
            open: () => {
                return app.commands.execute(CommandIDs.open);
            }
        };
    }
};
const plugins = [pluginmanager];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=1851.062907a35697eb334b3a.js.map?v=062907a35697eb334b3a