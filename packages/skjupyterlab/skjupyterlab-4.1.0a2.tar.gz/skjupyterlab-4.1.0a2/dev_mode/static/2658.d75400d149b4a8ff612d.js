"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[2658],{

/***/ 62658:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "DEFAULT_CONTEXT_ITEM_RANK": () => (/* binding */ DEFAULT_CONTEXT_ITEM_RANK),
  "default": () => (/* binding */ lib)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/application@~4.1.0-alpha.2 (singleton) (fallback: ../packages/application/lib/index.js)
var index_js_ = __webpack_require__(65681);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var lib_index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var coreutils_lib_index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/property-inspector@~4.1.0-alpha.2 (strict) (fallback: ../packages/property-inspector/lib/index.js)
var property_inspector_lib_index_js_ = __webpack_require__(28067);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/settingregistry@~4.1.0-alpha.2 (singleton) (fallback: ../packages/settingregistry/lib/index.js)
var settingregistry_lib_index_js_ = __webpack_require__(89397);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/statedb@~4.1.0-alpha.2 (singleton) (fallback: ../packages/statedb/lib/index.js)
var statedb_lib_index_js_ = __webpack_require__(1458);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/statusbar@~4.1.0-alpha.2 (singleton) (fallback: ../packages/statusbar/lib/index.js)
var statusbar_lib_index_js_ = __webpack_require__(34853);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(16415);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @lumino/commands@^2.0.1 (singleton) (fallback: ../node_modules/@lumino/commands/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(18955);
// EXTERNAL MODULE: consume shared module (default) @lumino/disposable@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/disposable/dist/index.es6.js)
var disposable_dist_index_es6_js_ = __webpack_require__(78612);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var widgets_dist_index_es6_js_ = __webpack_require__(72234);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
;// CONCATENATED MODULE: ../packages/application-extension/lib/topbar.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */




const TOPBAR_FACTORY = 'TopBar';
/**
 * A plugin adding a toolbar to the top area.
 */
const topbar = {
    id: '@jupyterlab/application-extension:top-bar',
    description: 'Adds a toolbar to the top area (next to the main menu bar).',
    autoStart: true,
    requires: [settingregistry_lib_index_js_.ISettingRegistry, lib_index_js_.IToolbarWidgetRegistry],
    optional: [translation_lib_index_js_.ITranslator],
    activate: (app, settingRegistry, toolbarRegistry, translator) => {
        const toolbar = new ui_components_lib_index_js_.Toolbar();
        toolbar.id = 'jp-top-bar';
        // Set toolbar
        (0,lib_index_js_.setToolbar)(toolbar, (0,lib_index_js_.createToolbarFactory)(toolbarRegistry, settingRegistry, TOPBAR_FACTORY, topbar.id, translator !== null && translator !== void 0 ? translator : translation_lib_index_js_.nullTranslator), toolbar);
        app.shell.add(toolbar, 'top', { rank: 900 });
    }
};

;// CONCATENATED MODULE: ../packages/application-extension/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module application-extension
 */
















/**
 * Default context menu item rank
 */
const DEFAULT_CONTEXT_ITEM_RANK = 100;
/**
 * The command IDs used by the application plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.activateNextTab = 'application:activate-next-tab';
    CommandIDs.activatePreviousTab = 'application:activate-previous-tab';
    CommandIDs.activateNextTabBar = 'application:activate-next-tab-bar';
    CommandIDs.activatePreviousTabBar = 'application:activate-previous-tab-bar';
    CommandIDs.close = 'application:close';
    CommandIDs.closeOtherTabs = 'application:close-other-tabs';
    CommandIDs.closeRightTabs = 'application:close-right-tabs';
    CommandIDs.closeAll = 'application:close-all';
    CommandIDs.setMode = 'application:set-mode';
    CommandIDs.showPropertyPanel = 'property-inspector:show-panel';
    CommandIDs.resetLayout = 'application:reset-layout';
    CommandIDs.toggleHeader = 'application:toggle-header';
    CommandIDs.toggleMode = 'application:toggle-mode';
    CommandIDs.toggleLeftArea = 'application:toggle-left-area';
    CommandIDs.toggleRightArea = 'application:toggle-right-area';
    CommandIDs.toggleSideTabBar = 'application:toggle-side-tabbar';
    CommandIDs.togglePresentationMode = 'application:toggle-presentation-mode';
    CommandIDs.tree = 'router:tree';
    CommandIDs.switchSidebar = 'sidebar:switch';
})(CommandIDs || (CommandIDs = {}));
/**
 * A plugin to register the commands for the main application.
 */
const mainCommands = {
    id: '@jupyterlab/application-extension:commands',
    description: 'Adds commands related to the shell.',
    autoStart: true,
    requires: [translation_lib_index_js_.ITranslator],
    optional: [index_js_.ILabShell, lib_index_js_.ICommandPalette],
    activate: (app, translator, labShell, palette) => {
        const { commands, shell } = app;
        const trans = translator.load('jupyterlab');
        const category = trans.__('Main Area');
        // Add Command to override the JLab context menu.
        commands.addCommand(index_js_.JupyterFrontEndContextMenu.contextMenu, {
            label: trans.__('Shift+Right Click for Browser Menu'),
            isEnabled: () => false,
            execute: () => void 0
        });
        // Returns the widget associated with the most recent contextmenu event.
        const contextMenuWidget = () => {
            const test = (node) => !!node.dataset.id;
            const node = app.contextMenuHitTest(test);
            if (!node) {
                // Fall back to active widget if path cannot be obtained from event.
                return shell.currentWidget;
            }
            return ((0,index_es6_js_.find)(shell.widgets('main'), widget => widget.id === node.dataset.id) ||
                shell.currentWidget);
        };
        // Closes an array of widgets.
        const closeWidgets = (widgets) => {
            widgets.forEach(widget => widget.close());
        };
        // Find the tab area for a widget within a specific dock area.
        const findTab = (area, widget) => {
            if (area.type === 'tab-area') {
                return area.widgets.includes(widget) ? area : null;
            }
            if (area.type === 'split-area') {
                for (const child of area.children) {
                    const found = findTab(child, widget);
                    if (found) {
                        return found;
                    }
                }
            }
            return null;
        };
        // Find the tab area for a widget within the main dock area.
        const tabAreaFor = (widget) => {
            var _a;
            const layout = labShell === null || labShell === void 0 ? void 0 : labShell.saveLayout();
            const mainArea = layout === null || layout === void 0 ? void 0 : layout.mainArea;
            if (!mainArea || coreutils_lib_index_js_.PageConfig.getOption('mode') !== 'multiple-document') {
                return null;
            }
            const area = (_a = mainArea.dock) === null || _a === void 0 ? void 0 : _a.main;
            return area ? findTab(area, widget) : null;
        };
        // Returns an array of all widgets to the right of a widget in a tab area.
        const widgetsRightOf = (widget) => {
            const { id } = widget;
            const tabArea = tabAreaFor(widget);
            const widgets = tabArea ? tabArea.widgets || [] : [];
            const index = widgets.findIndex(widget => widget.id === id);
            if (index < 0) {
                return [];
            }
            return widgets.slice(index + 1);
        };
        commands.addCommand(CommandIDs.close, {
            label: () => trans.__('Close Tab'),
            isEnabled: () => {
                const widget = contextMenuWidget();
                return !!widget && widget.title.closable;
            },
            execute: () => {
                const widget = contextMenuWidget();
                if (widget) {
                    widget.close();
                }
            }
        });
        commands.addCommand(CommandIDs.closeOtherTabs, {
            label: () => trans.__('Close All Other Tabs'),
            isEnabled: () => {
                // Ensure there are at least two widgets.
                return (0,index_es6_js_.some)(shell.widgets('main'), (_, i) => i === 1);
            },
            execute: () => {
                const widget = contextMenuWidget();
                if (!widget) {
                    return;
                }
                const { id } = widget;
                for (const widget of shell.widgets('main')) {
                    if (widget.id !== id) {
                        widget.close();
                    }
                }
            }
        });
        commands.addCommand(CommandIDs.closeRightTabs, {
            label: () => trans.__('Close Tabs to Right'),
            isEnabled: () => !!contextMenuWidget() &&
                widgetsRightOf(contextMenuWidget()).length > 0,
            execute: () => {
                const widget = contextMenuWidget();
                if (!widget) {
                    return;
                }
                closeWidgets(widgetsRightOf(widget));
            }
        });
        if (labShell) {
            commands.addCommand(CommandIDs.activateNextTab, {
                label: trans.__('Activate Next Tab'),
                execute: () => {
                    labShell.activateNextTab();
                }
            });
            commands.addCommand(CommandIDs.activatePreviousTab, {
                label: trans.__('Activate Previous Tab'),
                execute: () => {
                    labShell.activatePreviousTab();
                }
            });
            commands.addCommand(CommandIDs.activateNextTabBar, {
                label: trans.__('Activate Next Tab Bar'),
                execute: () => {
                    labShell.activateNextTabBar();
                }
            });
            commands.addCommand(CommandIDs.activatePreviousTabBar, {
                label: trans.__('Activate Previous Tab Bar'),
                execute: () => {
                    labShell.activatePreviousTabBar();
                }
            });
            commands.addCommand(CommandIDs.closeAll, {
                label: trans.__('Close All Tabs'),
                execute: () => {
                    labShell.closeAll();
                }
            });
            commands.addCommand(CommandIDs.toggleHeader, {
                label: trans.__('Show Header'),
                execute: () => {
                    if (labShell.mode === 'single-document') {
                        labShell.toggleTopInSimpleModeVisibility();
                    }
                },
                isToggled: () => labShell.isTopInSimpleModeVisible(),
                isVisible: () => labShell.mode === 'single-document'
            });
            commands.addCommand(CommandIDs.toggleLeftArea, {
                label: trans.__('Show Left Sidebar'),
                execute: () => {
                    if (labShell.leftCollapsed) {
                        labShell.expandLeft();
                    }
                    else {
                        labShell.collapseLeft();
                        if (labShell.currentWidget) {
                            labShell.activateById(labShell.currentWidget.id);
                        }
                    }
                },
                isToggled: () => !labShell.leftCollapsed,
                isEnabled: () => !labShell.isEmpty('left')
            });
            commands.addCommand(CommandIDs.toggleRightArea, {
                label: trans.__('Show Right Sidebar'),
                execute: () => {
                    if (labShell.rightCollapsed) {
                        labShell.expandRight();
                    }
                    else {
                        labShell.collapseRight();
                        if (labShell.currentWidget) {
                            labShell.activateById(labShell.currentWidget.id);
                        }
                    }
                },
                isToggled: () => !labShell.rightCollapsed,
                isEnabled: () => !labShell.isEmpty('right')
            });
            commands.addCommand(CommandIDs.toggleSideTabBar, {
                label: args => args.side === 'right'
                    ? trans.__('Show Right Activity Bar')
                    : trans.__('Show Left Activity Bar'),
                execute: args => {
                    if (args.side === 'right') {
                        labShell.toggleSideTabBarVisibility('right');
                    }
                    else {
                        labShell.toggleSideTabBarVisibility('left');
                    }
                },
                isToggled: args => args.side === 'right'
                    ? labShell.isSideTabBarVisible('right')
                    : labShell.isSideTabBarVisible('left'),
                isEnabled: args => args.side === 'right'
                    ? !labShell.isEmpty('right')
                    : !labShell.isEmpty('left')
            });
            commands.addCommand(CommandIDs.togglePresentationMode, {
                label: () => trans.__('Presentation Mode'),
                execute: () => {
                    labShell.presentationMode = !labShell.presentationMode;
                },
                isToggled: () => labShell.presentationMode,
                isVisible: () => true
            });
            commands.addCommand(CommandIDs.setMode, {
                label: args => args['mode']
                    ? trans.__('Set %1 mode.', args['mode'])
                    : trans.__('Set the layout `mode`.'),
                caption: trans.__('The layout `mode` can be "single-document" or "multiple-document".'),
                isVisible: args => {
                    const mode = args['mode'];
                    return mode === 'single-document' || mode === 'multiple-document';
                },
                execute: args => {
                    const mode = args['mode'];
                    if (mode === 'single-document' || mode === 'multiple-document') {
                        labShell.mode = mode;
                        return;
                    }
                    throw new Error(`Unsupported application shell mode: ${mode}`);
                }
            });
            commands.addCommand(CommandIDs.toggleMode, {
                label: trans.__('Simple Interface'),
                isToggled: () => labShell.mode === 'single-document',
                execute: () => {
                    const args = labShell.mode === 'multiple-document'
                        ? { mode: 'single-document' }
                        : { mode: 'multiple-document' };
                    return commands.execute(CommandIDs.setMode, args);
                }
            });
            commands.addCommand(CommandIDs.resetLayout, {
                label: trans.__('Reset Default Layout'),
                execute: () => {
                    // Turn off presentation mode
                    if (labShell.presentationMode) {
                        commands
                            .execute(CommandIDs.togglePresentationMode)
                            .catch(reason => {
                            console.error('Failed to undo presentation mode.', reason);
                        });
                    }
                    // Display top header
                    if (labShell.mode === 'single-document' &&
                        !labShell.isTopInSimpleModeVisible()) {
                        commands.execute(CommandIDs.toggleHeader).catch(reason => {
                            console.error('Failed to display title header.', reason);
                        });
                    }
                    // Display side tabbar
                    ['left', 'right'].forEach(side => {
                        if (!labShell.isSideTabBarVisible(side) &&
                            !labShell.isEmpty(side)) {
                            commands
                                .execute(CommandIDs.toggleSideTabBar, { side })
                                .catch(reason => {
                                console.error(`Failed to show ${side} activity bar.`, reason);
                            });
                        }
                    });
                    // Some actions are also trigger indirectly
                    // - by listening to this command execution.
                }
            });
        }
        if (palette) {
            [
                CommandIDs.activateNextTab,
                CommandIDs.activatePreviousTab,
                CommandIDs.activateNextTabBar,
                CommandIDs.activatePreviousTabBar,
                CommandIDs.close,
                CommandIDs.closeAll,
                CommandIDs.closeOtherTabs,
                CommandIDs.closeRightTabs,
                CommandIDs.toggleHeader,
                CommandIDs.toggleLeftArea,
                CommandIDs.toggleRightArea,
                CommandIDs.togglePresentationMode,
                CommandIDs.toggleMode,
                CommandIDs.resetLayout
            ].forEach(command => palette.addItem({ command, category }));
            ['right', 'left'].forEach(side => {
                palette.addItem({
                    command: CommandIDs.toggleSideTabBar,
                    category,
                    args: { side }
                });
            });
        }
    }
};
/**
 * The main extension.
 */
const main = {
    id: '@jupyterlab/application-extension:main',
    description: 'Initializes the application and provides the URL tree path handler.',
    requires: [
        index_js_.IRouter,
        lib_index_js_.IWindowResolver,
        translation_lib_index_js_.ITranslator,
        index_js_.JupyterFrontEnd.ITreeResolver
    ],
    optional: [index_js_.IConnectionLost],
    provides: index_js_.ITreePathUpdater,
    activate: (app, router, resolver, translator, treeResolver, connectionLost) => {
        const trans = translator.load('jupyterlab');
        if (!(app instanceof index_js_.JupyterLab)) {
            throw new Error(`${main.id} must be activated in JupyterLab.`);
        }
        // These two internal state variables are used to manage the two source
        // of the tree part of the URL being updated: 1) path of the active document,
        // 2) path of the default browser if the active main area widget isn't a document.
        let _docTreePath = '';
        let _defaultBrowserTreePath = '';
        function updateTreePath(treePath) {
            // Wait for tree resolver to finish before updating the path because it use the PageConfig['treePath']
            void treeResolver.paths.then(() => {
                _defaultBrowserTreePath = treePath;
                if (!_docTreePath) {
                    const url = coreutils_lib_index_js_.PageConfig.getUrl({ treePath });
                    const path = coreutils_lib_index_js_.URLExt.parse(url).pathname;
                    router.navigate(path, { skipRouting: true });
                    // Persist the new tree path to PageConfig as it is used elsewhere at runtime.
                    coreutils_lib_index_js_.PageConfig.setOption('treePath', treePath);
                }
            });
        }
        // Requiring the window resolver guarantees that the application extension
        // only loads if there is a viable window name. Otherwise, the application
        // will short-circuit and ask the user to navigate away.
        const workspace = resolver.name;
        console.debug(`Starting application in workspace: "${workspace}"`);
        // If there were errors registering plugins, tell the user.
        if (app.registerPluginErrors.length !== 0) {
            const body = (react_index_js_.createElement("pre", null, app.registerPluginErrors.map(e => e.message).join('\n')));
            void (0,lib_index_js_.showErrorMessage)(trans.__('Error Registering Plugins'), {
                message: body
            });
        }
        // If the application shell layout is modified,
        // trigger a refresh of the commands.
        app.shell.layoutModified.connect(() => {
            app.commands.notifyCommandChanged();
        });
        // Watch the mode and update the page URL to /lab or /doc to reflect the
        // change.
        app.shell.modeChanged.connect((_, args) => {
            const url = coreutils_lib_index_js_.PageConfig.getUrl({ mode: args });
            const path = coreutils_lib_index_js_.URLExt.parse(url).pathname;
            router.navigate(path, { skipRouting: true });
            // Persist this mode change to PageConfig as it is used elsewhere at runtime.
            coreutils_lib_index_js_.PageConfig.setOption('mode', args);
        });
        // Wait for tree resolver to finish before updating the path because it use the PageConfig['treePath']
        void treeResolver.paths.then(() => {
            // Watch the path of the current widget in the main area and update the page
            // URL to reflect the change.
            app.shell.currentPathChanged.connect((_, args) => {
                const maybeTreePath = args.newValue;
                const treePath = maybeTreePath || _defaultBrowserTreePath;
                const url = coreutils_lib_index_js_.PageConfig.getUrl({ treePath: treePath });
                const path = coreutils_lib_index_js_.URLExt.parse(url).pathname;
                router.navigate(path, { skipRouting: true });
                // Persist the new tree path to PageConfig as it is used elsewhere at runtime.
                coreutils_lib_index_js_.PageConfig.setOption('treePath', treePath);
                _docTreePath = maybeTreePath;
            });
        });
        // If the connection to the server is lost, handle it with the
        // connection lost handler.
        connectionLost = connectionLost || index_js_.ConnectionLost;
        app.serviceManager.connectionFailure.connect((manager, error) => connectionLost(manager, error, translator));
        const builder = app.serviceManager.builder;
        const build = () => {
            return builder
                .build()
                .then(() => {
                return (0,lib_index_js_.showDialog)({
                    title: trans.__('Build Complete'),
                    body: (react_index_js_.createElement("div", null,
                        trans.__('Build successfully completed, reload page?'),
                        react_index_js_.createElement("br", null),
                        trans.__('You will lose any unsaved changes.'))),
                    buttons: [
                        lib_index_js_.Dialog.cancelButton({
                            label: trans.__('Reload Without Saving'),
                            actions: ['reload']
                        }),
                        lib_index_js_.Dialog.okButton({ label: trans.__('Save and Reload') })
                    ],
                    hasClose: true
                });
            })
                .then(({ button: { accept, actions } }) => {
                if (accept) {
                    void app.commands
                        .execute('docmanager:save')
                        .then(() => {
                        router.reload();
                    })
                        .catch(err => {
                        void (0,lib_index_js_.showErrorMessage)(trans.__('Save Failed'), {
                            message: react_index_js_.createElement("pre", null, err.message)
                        });
                    });
                }
                else if (actions.includes('reload')) {
                    router.reload();
                }
            })
                .catch(err => {
                void (0,lib_index_js_.showErrorMessage)(trans.__('Build Failed'), {
                    message: react_index_js_.createElement("pre", null, err.message)
                });
            });
        };
        if (builder.isAvailable && builder.shouldCheck) {
            void builder.getStatus().then(response => {
                if (response.status === 'building') {
                    return build();
                }
                if (response.status !== 'needed') {
                    return;
                }
                const body = (react_index_js_.createElement("div", null,
                    trans.__('JupyterLab build is suggested:'),
                    react_index_js_.createElement("br", null),
                    react_index_js_.createElement("pre", null, response.message)));
                void (0,lib_index_js_.showDialog)({
                    title: trans.__('Build Recommended'),
                    body,
                    buttons: [
                        lib_index_js_.Dialog.cancelButton(),
                        lib_index_js_.Dialog.okButton({ label: trans.__('Build') })
                    ]
                }).then(result => (result.button.accept ? build() : undefined));
            });
        }
        return updateTreePath;
    },
    autoStart: true
};
/**
 * Plugin to build the context menu from the settings.
 */
const contextMenuPlugin = {
    id: '@jupyterlab/application-extension:context-menu',
    description: 'Populates the context menu.',
    autoStart: true,
    requires: [settingregistry_lib_index_js_.ISettingRegistry, translation_lib_index_js_.ITranslator],
    activate: (app, settingRegistry, translator) => {
        const trans = translator.load('jupyterlab');
        function createMenu(options) {
            const menu = new ui_components_lib_index_js_.RankedMenu({ ...options, commands: app.commands });
            if (options.label) {
                menu.title.label = trans.__(options.label);
            }
            return menu;
        }
        // Load the context menu lately so plugins are loaded.
        app.started
            .then(() => {
            return Private.loadSettingsContextMenu(app.contextMenu, settingRegistry, createMenu, translator);
        })
            .catch(reason => {
            console.error('Failed to load context menu items from settings registry.', reason);
        });
    }
};
/**
 * Check if the application is dirty before closing the browser tab.
 */
const dirty = {
    id: '@jupyterlab/application-extension:dirty',
    description: 'Adds safeguard dialog when closing the browser tab with unsaved modifications.',
    autoStart: true,
    requires: [translation_lib_index_js_.ITranslator],
    activate: (app, translator) => {
        if (!(app instanceof index_js_.JupyterLab)) {
            throw new Error(`${dirty.id} must be activated in JupyterLab.`);
        }
        const trans = translator.load('jupyterlab');
        const message = trans.__('Are you sure you want to exit JupyterLab?\n\nAny unsaved changes will be lost.');
        // The spec for the `beforeunload` event is implemented differently by
        // the different browser vendors. Consequently, the `event.returnValue`
        // attribute needs to set in addition to a return value being returned.
        // For more information, see:
        // https://developer.mozilla.org/en/docs/Web/Events/beforeunload
        window.addEventListener('beforeunload', event => {
            if (app.status.isDirty) {
                return (event.returnValue = message);
            }
        });
    }
};
/**
 * The default layout restorer provider.
 */
const layout = {
    id: '@jupyterlab/application-extension:layout',
    description: 'Provides the shell layout restorer.',
    requires: [statedb_lib_index_js_.IStateDB, index_js_.ILabShell, settingregistry_lib_index_js_.ISettingRegistry],
    optional: [translation_lib_index_js_.ITranslator],
    activate: (app, state, labShell, settingRegistry, translator) => {
        const trans = (translator !== null && translator !== void 0 ? translator : translation_lib_index_js_.nullTranslator).load('jupyterlab');
        const first = app.started;
        const registry = app.commands;
        const mode = coreutils_lib_index_js_.PageConfig.getOption('mode');
        const restorer = new index_js_.LayoutRestorer({
            connector: state,
            first,
            registry,
            mode
        });
        settingRegistry
            .load(shell.id)
            .then(settings => {
            var _a, _b;
            // Add a layer of customization to support app shell mode
            const customizedLayout = settings.composite['layout'];
            // Restore the layout.
            void labShell
                .restoreLayout(mode, restorer, {
                'multiple-document': (_a = customizedLayout.multiple) !== null && _a !== void 0 ? _a : {},
                'single-document': (_b = customizedLayout.single) !== null && _b !== void 0 ? _b : {}
            })
                .then(() => {
                labShell.layoutModified.connect(() => {
                    void restorer.save(labShell.saveLayout());
                });
                settings.changed.connect(onSettingsChanged);
                Private.activateSidebarSwitcher(app, labShell, settings, trans);
            });
        })
            .catch(reason => {
            console.error('Fail to load settings for the layout restorer.');
            console.error(reason);
        });
        return restorer;
        async function onSettingsChanged(settings) {
            if (!dist_index_js_.JSONExt.deepEqual(settings.composite['layout'], {
                single: labShell.userLayout['single-document'],
                multiple: labShell.userLayout['multiple-document']
            })) {
                const result = await (0,lib_index_js_.showDialog)({
                    title: trans.__('Information'),
                    body: trans.__('User layout customization has changed. You may need to reload JupyterLab to see the changes.'),
                    buttons: [
                        lib_index_js_.Dialog.cancelButton(),
                        lib_index_js_.Dialog.okButton({ label: trans.__('Reload') })
                    ]
                });
                if (result.button.accept) {
                    location.reload();
                }
            }
        }
    },
    autoStart: true,
    provides: index_js_.ILayoutRestorer
};
/**
 * The default URL router provider.
 */
const router = {
    id: '@jupyterlab/application-extension:router',
    description: 'Provides the URL router',
    requires: [index_js_.JupyterFrontEnd.IPaths],
    activate: (app, paths) => {
        const { commands } = app;
        const base = paths.urls.base;
        const router = new index_js_.Router({ base, commands });
        void app.started.then(() => {
            // Route the very first request on load.
            void router.route();
            // Route all pop state events.
            window.addEventListener('popstate', () => {
                void router.route();
            });
        });
        return router;
    },
    autoStart: true,
    provides: index_js_.IRouter
};
/**
 * The default tree route resolver plugin.
 */
const tree = {
    id: '@jupyterlab/application-extension:tree-resolver',
    description: 'Provides the tree route resolver',
    autoStart: true,
    requires: [index_js_.IRouter],
    provides: index_js_.JupyterFrontEnd.ITreeResolver,
    activate: (app, router) => {
        const { commands } = app;
        const set = new disposable_dist_index_es6_js_.DisposableSet();
        const delegate = new dist_index_js_.PromiseDelegate();
        const treePattern = new RegExp('/(lab|doc)(/workspaces/[a-zA-Z0-9-_]+)?(/tree/.*)?');
        set.add(commands.addCommand(CommandIDs.tree, {
            execute: async (args) => {
                var _a;
                if (set.isDisposed) {
                    return;
                }
                const query = coreutils_lib_index_js_.URLExt.queryStringToObject((_a = args.search) !== null && _a !== void 0 ? _a : '');
                const browser = query['file-browser-path'] || '';
                // Remove the file browser path from the query string.
                delete query['file-browser-path'];
                // Clean up artifacts immediately upon routing.
                set.dispose();
                delegate.resolve({ browser, file: coreutils_lib_index_js_.PageConfig.getOption('treePath') });
            }
        }));
        set.add(router.register({ command: CommandIDs.tree, pattern: treePattern }));
        // If a route is handled by the router without the tree command being
        // invoked, resolve to `null` and clean up artifacts.
        const listener = () => {
            if (set.isDisposed) {
                return;
            }
            set.dispose();
            delegate.resolve(null);
        };
        router.routed.connect(listener);
        set.add(new disposable_dist_index_es6_js_.DisposableDelegate(() => {
            router.routed.disconnect(listener);
        }));
        return { paths: delegate.promise };
    }
};
/**
 * The default URL not found extension.
 */
const notfound = {
    id: '@jupyterlab/application-extension:notfound',
    description: 'Defines the behavior for not found URL (aka route).',
    requires: [index_js_.JupyterFrontEnd.IPaths, index_js_.IRouter, translation_lib_index_js_.ITranslator],
    activate: (_, paths, router, translator) => {
        const trans = translator.load('jupyterlab');
        const bad = paths.urls.notFound;
        if (!bad) {
            return;
        }
        const base = router.base;
        const message = trans.__('The path: %1 was not found. JupyterLab redirected to: %2', bad, base);
        // Change the URL back to the base application URL.
        router.navigate('');
        void (0,lib_index_js_.showErrorMessage)(trans.__('Path Not Found'), { message });
    },
    autoStart: true
};
/**
 * Change the favicon changing based on the busy status;
 */
const busy = {
    id: '@jupyterlab/application-extension:faviconbusy',
    description: 'Handles the favicon depending on the application status.',
    requires: [index_js_.ILabStatus],
    activate: async (_, status) => {
        status.busySignal.connect((_, isBusy) => {
            const favicon = document.querySelector(`link[rel="icon"]${isBusy ? '.idle.favicon' : '.busy.favicon'}`);
            if (!favicon) {
                return;
            }
            const newFavicon = document.querySelector(`link${isBusy ? '.busy.favicon' : '.idle.favicon'}`);
            if (!newFavicon) {
                return;
            }
            // If we have the two icons with the special classes, then toggle them.
            if (favicon !== newFavicon) {
                favicon.rel = '';
                newFavicon.rel = 'icon';
                // Firefox doesn't seem to recognize just changing rel, so we also
                // reinsert the link into the DOM.
                newFavicon.parentNode.replaceChild(newFavicon, newFavicon);
            }
        });
    },
    autoStart: true
};
/**
 * The default JupyterLab application shell.
 */
const shell = {
    id: '@jupyterlab/application-extension:shell',
    description: 'Provides the JupyterLab shell. It has an extended API compared to `app.shell`.',
    optional: [settingregistry_lib_index_js_.ISettingRegistry],
    activate: (app, settingRegistry) => {
        if (!(app.shell instanceof index_js_.LabShell)) {
            throw new Error(`${shell.id} did not find a LabShell instance.`);
        }
        if (settingRegistry) {
            void settingRegistry.load(shell.id).then(settings => {
                app.shell.updateConfig(settings.composite);
                settings.changed.connect(() => {
                    app.shell.updateConfig(settings.composite);
                });
            });
        }
        return app.shell;
    },
    autoStart: true,
    provides: index_js_.ILabShell
};
/**
 * The default JupyterLab application status provider.
 */
const lib_status = {
    id: '@jupyterlab/application-extension:status',
    description: 'Provides the application status.',
    activate: (app) => {
        if (!(app instanceof index_js_.JupyterLab)) {
            throw new Error(`${lib_status.id} must be activated in JupyterLab.`);
        }
        return app.status;
    },
    autoStart: true,
    provides: index_js_.ILabStatus
};
/**
 * The default JupyterLab application-specific information provider.
 *
 * #### Notes
 * This plugin should only be used by plugins that specifically need to access
 * JupyterLab application information, e.g., listing extensions that have been
 * loaded or deferred within JupyterLab.
 */
const info = {
    id: '@jupyterlab/application-extension:info',
    description: 'Provides the application information.',
    activate: (app) => {
        if (!(app instanceof index_js_.JupyterLab)) {
            throw new Error(`${info.id} must be activated in JupyterLab.`);
        }
        return app.info;
    },
    autoStart: true,
    provides: index_js_.JupyterLab.IInfo
};
/**
 * The default JupyterLab paths dictionary provider.
 */
const paths = {
    id: '@jupyterlab/application-extension:paths',
    description: 'Provides the application paths.',
    activate: (app) => {
        if (!(app instanceof index_js_.JupyterLab)) {
            throw new Error(`${paths.id} must be activated in JupyterLab.`);
        }
        return app.paths;
    },
    autoStart: true,
    provides: index_js_.JupyterFrontEnd.IPaths
};
/**
 * The default property inspector provider.
 */
const propertyInspector = {
    id: '@jupyterlab/application-extension:property-inspector',
    description: 'Provides the property inspector.',
    autoStart: true,
    requires: [index_js_.ILabShell, translation_lib_index_js_.ITranslator],
    optional: [index_js_.ILayoutRestorer],
    provides: property_inspector_lib_index_js_.IPropertyInspectorProvider,
    activate: (app, labshell, translator, restorer) => {
        const trans = translator.load('jupyterlab');
        const widget = new property_inspector_lib_index_js_.SideBarPropertyInspectorProvider({
            shell: labshell,
            translator
        });
        widget.title.icon = ui_components_lib_index_js_.buildIcon;
        widget.title.caption = trans.__('Property Inspector');
        widget.id = 'jp-property-inspector';
        labshell.add(widget, 'right', { rank: 100, type: 'Property Inspector' });
        app.commands.addCommand(CommandIDs.showPropertyPanel, {
            label: trans.__('Property Inspector'),
            execute: () => {
                labshell.activateById(widget.id);
            }
        });
        if (restorer) {
            restorer.add(widget, 'jp-property-inspector');
        }
        return widget;
    }
};
const jupyterLogo = {
    id: '@jupyterlab/application-extension:logo',
    description: 'Sets the application logo.',
    autoStart: true,
    requires: [index_js_.ILabShell],
    activate: (app, shell) => {
        const logo = new widgets_dist_index_es6_js_.Widget();
        ui_components_lib_index_js_.jupyterIcon.element({
            container: logo.node,
            elementPosition: 'center',
            margin: '2px 18px 2px 9px',
            height: 'auto',
            width: '32px'
        });
        logo.id = 'jp-MainLogo';
        shell.add(logo, 'top', { rank: 0 });
    }
};
/**
 * The simple interface mode switch in the status bar.
 */
const modeSwitchPlugin = {
    id: '@jupyterlab/application-extension:mode-switch',
    description: 'Adds the interface mode switch',
    requires: [index_js_.ILabShell, translation_lib_index_js_.ITranslator],
    optional: [statusbar_lib_index_js_.IStatusBar, settingregistry_lib_index_js_.ISettingRegistry],
    activate: (app, labShell, translator, statusBar, settingRegistry) => {
        if (statusBar === null) {
            // Bail early
            return;
        }
        const trans = translator.load('jupyterlab');
        const modeSwitch = new ui_components_lib_index_js_.Switch();
        modeSwitch.id = 'jp-single-document-mode';
        modeSwitch.valueChanged.connect((_, args) => {
            labShell.mode = args.newValue ? 'single-document' : 'multiple-document';
        });
        labShell.modeChanged.connect((_, mode) => {
            modeSwitch.value = mode === 'single-document';
        });
        if (settingRegistry) {
            const loadSettings = settingRegistry.load(shell.id);
            const updateSettings = (settings) => {
                const startMode = settings.get('startMode').composite;
                if (startMode) {
                    labShell.mode =
                        startMode === 'single' ? 'single-document' : 'multiple-document';
                }
            };
            Promise.all([loadSettings, app.restored])
                .then(([settings]) => {
                updateSettings(settings);
            })
                .catch((reason) => {
                console.error(reason.message);
            });
        }
        // Show the current file browser shortcut in its title.
        const updateModeSwitchTitle = () => {
            const binding = app.commands.keyBindings.find(b => b.command === 'application:toggle-mode');
            if (binding) {
                const ks = binding.keys.map(dist_index_es6_js_.CommandRegistry.formatKeystroke).join(', ');
                modeSwitch.caption = trans.__('Simple Interface (%1)', ks);
            }
            else {
                modeSwitch.caption = trans.__('Simple Interface');
            }
        };
        updateModeSwitchTitle();
        app.commands.keyBindingChanged.connect(() => {
            updateModeSwitchTitle();
        });
        modeSwitch.label = trans.__('Simple');
        statusBar.registerStatusItem(modeSwitchPlugin.id, {
            item: modeSwitch,
            align: 'left',
            rank: -1
        });
    },
    autoStart: true
};
/**
 * Export the plugins as default.
 */
const plugins = [
    contextMenuPlugin,
    dirty,
    main,
    mainCommands,
    layout,
    router,
    tree,
    notfound,
    busy,
    shell,
    lib_status,
    info,
    modeSwitchPlugin,
    paths,
    propertyInspector,
    jupyterLogo,
    topbar
];
/* harmony default export */ const lib = (plugins);
var Private;
(function (Private) {
    async function displayInformation(trans) {
        const result = await (0,lib_index_js_.showDialog)({
            title: trans.__('Information'),
            body: trans.__('Context menu customization has changed. You will need to reload JupyterLab to see the changes.'),
            buttons: [
                lib_index_js_.Dialog.cancelButton(),
                lib_index_js_.Dialog.okButton({ label: trans.__('Reload') })
            ]
        });
        if (result.button.accept) {
            location.reload();
        }
    }
    async function loadSettingsContextMenu(contextMenu, registry, menuFactory, translator) {
        var _a;
        const trans = translator.load('jupyterlab');
        const pluginId = contextMenuPlugin.id;
        let canonical = null;
        let loaded = {};
        /**
         * Populate the plugin's schema defaults.
         *
         * We keep track of disabled entries in case the plugin is loaded
         * after the menu initialization.
         */
        function populate(schema) {
            var _a, _b;
            loaded = {};
            const pluginDefaults = Object.keys(registry.plugins)
                .map(plugin => {
                var _a, _b;
                const items = (_b = (_a = registry.plugins[plugin].schema['jupyter.lab.menus']) === null || _a === void 0 ? void 0 : _a.context) !== null && _b !== void 0 ? _b : [];
                loaded[plugin] = items;
                return items;
            })
                .concat([(_b = (_a = schema['jupyter.lab.menus']) === null || _a === void 0 ? void 0 : _a.context) !== null && _b !== void 0 ? _b : []])
                .reduceRight((acc, val) => settingregistry_lib_index_js_.SettingRegistry.reconcileItems(acc, val, true), []);
            // Apply default value as last step to take into account overrides.json
            // The standard default being [] as the plugin must use `jupyter.lab.menus.context`
            // to define their default value.
            schema.properties.contextMenu.default = settingregistry_lib_index_js_.SettingRegistry.reconcileItems(pluginDefaults, schema.properties.contextMenu.default, true)
                // flatten one level
                .sort((a, b) => { var _a, _b; return ((_a = a.rank) !== null && _a !== void 0 ? _a : Infinity) - ((_b = b.rank) !== null && _b !== void 0 ? _b : Infinity); });
        }
        // Transform the plugin object to return different schema than the default.
        registry.transform(pluginId, {
            compose: plugin => {
                var _a, _b, _c, _d;
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = dist_index_js_.JSONExt.deepCopy(plugin.schema);
                    populate(canonical);
                }
                const defaults = (_c = (_b = (_a = canonical.properties) === null || _a === void 0 ? void 0 : _a.contextMenu) === null || _b === void 0 ? void 0 : _b.default) !== null && _c !== void 0 ? _c : [];
                const user = {
                    ...plugin.data.user,
                    contextMenu: (_d = plugin.data.user.contextMenu) !== null && _d !== void 0 ? _d : []
                };
                const composite = {
                    ...plugin.data.composite,
                    contextMenu: settingregistry_lib_index_js_.SettingRegistry.reconcileItems(defaults, user.contextMenu, false)
                };
                plugin.data = { composite, user };
                return plugin;
            },
            fetch: plugin => {
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = dist_index_js_.JSONExt.deepCopy(plugin.schema);
                    populate(canonical);
                }
                return {
                    data: plugin.data,
                    id: plugin.id,
                    raw: plugin.raw,
                    schema: canonical,
                    version: plugin.version
                };
            }
        });
        // Repopulate the canonical variable after the setting registry has
        // preloaded all initial plugins.
        const settings = await registry.load(pluginId);
        const contextItems = (_a = settings.composite.contextMenu) !== null && _a !== void 0 ? _a : [];
        // Create menu item for non-disabled element
        settingregistry_lib_index_js_.SettingRegistry.filterDisabledItems(contextItems).forEach(item => {
            lib_index_js_.MenuFactory.addContextItem({
                // We have to set the default rank because Lumino is sorting the visible items
                rank: DEFAULT_CONTEXT_ITEM_RANK,
                ...item
            }, contextMenu, menuFactory);
        });
        settings.changed.connect(() => {
            var _a;
            // As extension may change the context menu through API,
            // prompt the user to reload if the menu has been updated.
            const newItems = (_a = settings.composite.contextMenu) !== null && _a !== void 0 ? _a : [];
            if (!dist_index_js_.JSONExt.deepEqual(contextItems, newItems)) {
                void displayInformation(trans);
            }
        });
        registry.pluginChanged.connect(async (sender, plugin) => {
            var _a, _b, _c, _d;
            if (plugin !== pluginId) {
                // If the plugin changed its menu.
                const oldItems = (_a = loaded[plugin]) !== null && _a !== void 0 ? _a : [];
                const newItems = (_c = (_b = registry.plugins[plugin].schema['jupyter.lab.menus']) === null || _b === void 0 ? void 0 : _b.context) !== null && _c !== void 0 ? _c : [];
                if (!dist_index_js_.JSONExt.deepEqual(oldItems, newItems)) {
                    if (loaded[plugin]) {
                        // The plugin has changed, request the user to reload the UI
                        await displayInformation(trans);
                    }
                    else {
                        // The plugin was not yet loaded when the menu was built => update the menu
                        loaded[plugin] = dist_index_js_.JSONExt.deepCopy(newItems);
                        // Merge potential disabled state
                        const toAdd = (_d = settingregistry_lib_index_js_.SettingRegistry.reconcileItems(newItems, contextItems, false, false)) !== null && _d !== void 0 ? _d : [];
                        settingregistry_lib_index_js_.SettingRegistry.filterDisabledItems(toAdd).forEach(item => {
                            lib_index_js_.MenuFactory.addContextItem({
                                // We have to set the default rank because Lumino is sorting the visible items
                                rank: DEFAULT_CONTEXT_ITEM_RANK,
                                ...item
                            }, contextMenu, menuFactory);
                        });
                    }
                }
            }
        });
    }
    Private.loadSettingsContextMenu = loadSettingsContextMenu;
    function activateSidebarSwitcher(app, labShell, settings, trans) {
        // Add a command to switch a side panels's side
        app.commands.addCommand(CommandIDs.switchSidebar, {
            label: trans.__('Switch Sidebar Side'),
            execute: () => {
                // First, try to find the correct panel based on the application
                // context menu click. Bail if we don't find a sidebar for the widget.
                const contextNode = app.contextMenuHitTest(node => !!node.dataset.id);
                if (!contextNode) {
                    return;
                }
                const id = contextNode.dataset['id'];
                const leftPanel = document.getElementById('jp-left-stack');
                const node = document.getElementById(id);
                let newLayout = null;
                // Move the panel to the other side.
                if (leftPanel && node && leftPanel.contains(node)) {
                    const widget = (0,index_es6_js_.find)(labShell.widgets('left'), w => w.id === id);
                    if (widget) {
                        newLayout = labShell.move(widget, 'right');
                        labShell.activateById(widget.id);
                    }
                }
                else {
                    const widget = (0,index_es6_js_.find)(labShell.widgets('right'), w => w.id === id);
                    if (widget) {
                        newLayout = labShell.move(widget, 'left');
                        labShell.activateById(widget.id);
                    }
                }
                if (newLayout) {
                    settings
                        .set('layout', {
                        single: newLayout['single-document'],
                        multiple: newLayout['multiple-document']
                    })
                        .catch(reason => {
                        console.error('Failed to save user layout customization.', reason);
                    });
                }
            }
        });
        app.commands.commandExecuted.connect((registry, executed) => {
            if (executed.id === CommandIDs.resetLayout) {
                settings.remove('layout').catch(reason => {
                    console.error('Failed to remove user layout customization.', reason);
                });
            }
        });
    }
    Private.activateSidebarSwitcher = activateSidebarSwitcher;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=2658.d75400d149b4a8ff612d.js.map?v=d75400d149b4a8ff612d