"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[1047,6315],{

/***/ 21047:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(65681);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(89397);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(95691);
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(76351);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module toc-extension
 */





/**
 * A namespace for command IDs of table of contents plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.displayNumbering = 'toc:display-numbering';
    CommandIDs.displayH1Numbering = 'toc:display-h1-numbering';
    CommandIDs.displayOutputNumbering = 'toc:display-outputs-numbering';
    CommandIDs.showPanel = 'toc:show-panel';
    CommandIDs.toggleCollapse = 'toc:toggle-collapse';
})(CommandIDs || (CommandIDs = {}));
/**
 * Activates the ToC extension.
 *
 * @private
 * @param app - Jupyter application
 * @param tocRegistry - Table of contents registry
 * @param translator - translator
 * @param restorer - application layout restorer
 * @param labShell - Jupyter lab shell
 * @param settingRegistry - setting registry
 * @returns table of contents registry
 */
async function activateTOC(app, tocRegistry, translator, restorer, labShell, settingRegistry) {
    const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator).load('jupyterlab');
    let configuration = { ..._jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2__.TableOfContents.defaultConfig };
    // Create the ToC widget:
    const toc = new _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2__.TableOfContentsPanel(translator !== null && translator !== void 0 ? translator : undefined);
    toc.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.tocIcon;
    toc.title.caption = trans.__('Table of Contents');
    toc.id = 'table-of-contents';
    toc.node.setAttribute('role', 'region');
    toc.node.setAttribute('aria-label', trans.__('Table of Contents section'));
    app.commands.addCommand(CommandIDs.displayH1Numbering, {
        label: trans.__('Show first-level heading number'),
        execute: () => {
            if (toc.model) {
                toc.model.setConfiguration({
                    numberingH1: !toc.model.configuration.numberingH1
                });
            }
        },
        isEnabled: () => { var _a, _b; return (_b = (_a = toc.model) === null || _a === void 0 ? void 0 : _a.supportedOptions.includes('numberingH1')) !== null && _b !== void 0 ? _b : false; },
        isToggled: () => { var _a, _b; return (_b = (_a = toc.model) === null || _a === void 0 ? void 0 : _a.configuration.numberingH1) !== null && _b !== void 0 ? _b : false; }
    });
    app.commands.addCommand(CommandIDs.displayNumbering, {
        label: trans.__('Show heading number in the document'),
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.numberingIcon : undefined),
        execute: () => {
            if (toc.model) {
                toc.model.setConfiguration({
                    numberHeaders: !toc.model.configuration.numberHeaders
                });
                app.commands.notifyCommandChanged(CommandIDs.displayNumbering);
            }
        },
        isEnabled: () => { var _a, _b; return (_b = (_a = toc.model) === null || _a === void 0 ? void 0 : _a.supportedOptions.includes('numberHeaders')) !== null && _b !== void 0 ? _b : false; },
        isToggled: () => { var _a, _b; return (_b = (_a = toc.model) === null || _a === void 0 ? void 0 : _a.configuration.numberHeaders) !== null && _b !== void 0 ? _b : false; }
    });
    app.commands.addCommand(CommandIDs.displayOutputNumbering, {
        label: trans.__('Show output headings'),
        execute: () => {
            if (toc.model) {
                toc.model.setConfiguration({
                    includeOutput: !toc.model.configuration.includeOutput
                });
            }
        },
        isEnabled: () => { var _a, _b; return (_b = (_a = toc.model) === null || _a === void 0 ? void 0 : _a.supportedOptions.includes('includeOutput')) !== null && _b !== void 0 ? _b : false; },
        isToggled: () => { var _a, _b; return (_b = (_a = toc.model) === null || _a === void 0 ? void 0 : _a.configuration.includeOutput) !== null && _b !== void 0 ? _b : false; }
    });
    app.commands.addCommand(CommandIDs.showPanel, {
        label: trans.__('Table of Contents'),
        execute: () => {
            app.shell.activateById(toc.id);
        }
    });
    function someExpanded(model) {
        return model.headings.some(h => { var _a; return !((_a = h.collapsed) !== null && _a !== void 0 ? _a : false); });
    }
    app.commands.addCommand(CommandIDs.toggleCollapse, {
        label: () => toc.model && !someExpanded(toc.model)
            ? trans.__('Expand All Headings')
            : trans.__('Collapse All Headings'),
        icon: args => args.toolbar
            ? toc.model && !someExpanded(toc.model)
                ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.expandAllIcon
                : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.collapseAllIcon
            : undefined,
        execute: () => {
            if (toc.model) {
                if (someExpanded(toc.model)) {
                    toc.model.toggleCollapse({ collapsed: true });
                }
                else {
                    toc.model.toggleCollapse({ collapsed: false });
                }
            }
        },
        isEnabled: () => toc.model !== null
    });
    const tracker = new _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2__.TableOfContentsTracker();
    if (restorer) {
        // Add the ToC widget to the application restorer:
        restorer.add(toc, '@jupyterlab/toc:plugin');
    }
    // Attempt to load plugin settings:
    let settings;
    if (settingRegistry) {
        try {
            settings = await settingRegistry.load(registry.id);
            const updateSettings = (plugin) => {
                const composite = plugin.composite;
                for (const key of [...Object.keys(configuration)]) {
                    const value = composite[key];
                    if (value !== undefined) {
                        configuration[key] = value;
                    }
                }
                if (labShell) {
                    for (const widget of labShell.widgets('main')) {
                        const model = tracker.get(widget);
                        if (model) {
                            model.setConfiguration(configuration);
                        }
                    }
                }
                else {
                    if (app.shell.currentWidget) {
                        const model = tracker.get(app.shell.currentWidget);
                        if (model) {
                            model.setConfiguration(configuration);
                        }
                    }
                }
            };
            if (settings) {
                settings.changed.connect(updateSettings);
                updateSettings(settings);
            }
        }
        catch (error) {
            console.error(`Failed to load settings for the Table of Contents extension.\n\n${error}`);
        }
    }
    // Set up the panel toolbar
    const numbering = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.CommandToolbarButton({
        commands: app.commands,
        id: CommandIDs.displayNumbering,
        args: {
            toolbar: true
        },
        label: ''
    });
    numbering.addClass('jp-toc-numberingButton');
    toc.toolbar.addItem('display-numbering', numbering);
    toc.toolbar.addItem('spacer', _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.Toolbar.createSpacerItem());
    toc.toolbar.addItem('collapse-all', new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.CommandToolbarButton({
        commands: app.commands,
        id: CommandIDs.toggleCollapse,
        args: {
            toolbar: true
        },
        label: ''
    }));
    const toolbarMenu = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.MenuSvg({ commands: app.commands });
    toolbarMenu.addItem({
        command: CommandIDs.displayH1Numbering
    });
    toolbarMenu.addItem({
        command: CommandIDs.displayOutputNumbering
    });
    const menuButton = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.ToolbarButton({
        tooltip: trans.__('More actions…'),
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.ellipsesIcon,
        actualOnClick: true,
        onClick: () => {
            const bbox = menuButton.node.getBoundingClientRect();
            toolbarMenu.open(bbox.x, bbox.bottom);
        }
    });
    toc.toolbar.addItem('submenu', menuButton);
    // Add the ToC to the left area:
    app.shell.add(toc, 'left', { rank: 400, type: 'Table of Contents' });
    // Update the ToC when the active widget changes:
    if (labShell) {
        labShell.currentChanged.connect(onConnect);
    }
    // Connect to current widget
    void app.restored.then(() => {
        onConnect();
    });
    return tracker;
    /**
     * Callback invoked when the active widget changes.
     *
     * @private
     */
    function onConnect() {
        var _a;
        let widget = app.shell.currentWidget;
        if (!widget) {
            return;
        }
        let model = tracker.get(widget);
        if (!model) {
            model = (_a = tocRegistry.getModel(widget, configuration)) !== null && _a !== void 0 ? _a : null;
            if (model) {
                tracker.add(widget, model);
            }
            widget.disposed.connect(() => {
                model === null || model === void 0 ? void 0 : model.dispose();
            });
        }
        if (toc.model) {
            toc.model.headingsChanged.disconnect(onCollapseChange);
            toc.model.collapseChanged.disconnect(onCollapseChange);
        }
        toc.model = model;
        if (toc.model) {
            toc.model.headingsChanged.connect(onCollapseChange);
            toc.model.collapseChanged.connect(onCollapseChange);
        }
        setToolbarButtonsState();
    }
    function setToolbarButtonsState() {
        app.commands.notifyCommandChanged(CommandIDs.displayNumbering);
        app.commands.notifyCommandChanged(CommandIDs.toggleCollapse);
    }
    function onCollapseChange() {
        app.commands.notifyCommandChanged(CommandIDs.toggleCollapse);
    }
}
/**
 * Table of contents registry plugin.
 */
const registry = {
    id: '@jupyterlab/toc-extension:registry',
    description: 'Provides the table of contents registry.',
    autoStart: true,
    provides: _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2__.ITableOfContentsRegistry,
    activate: () => {
        // Create the ToC registry
        return new _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2__.TableOfContentsRegistry();
    }
};
/**
 * Table of contents tracker plugin.
 */
const tracker = {
    id: '@jupyterlab/toc-extension:tracker',
    description: 'Adds the table of content widget and provides its tracker.',
    autoStart: true,
    provides: _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2__.ITableOfContentsTracker,
    requires: [_jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2__.ITableOfContentsRegistry],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry],
    activate: activateTOC
};
/**
 * Exports.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([registry, tracker]);


/***/ })

}]);
//# sourceMappingURL=1047.5bcf41549b633d8715ec.js.map?v=5bcf41549b633d8715ec