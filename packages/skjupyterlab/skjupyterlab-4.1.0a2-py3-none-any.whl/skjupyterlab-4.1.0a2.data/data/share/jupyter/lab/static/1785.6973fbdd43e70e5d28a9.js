"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[1785],{

/***/ 71785:
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
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(5184);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(43411);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(89397);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(76351);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(16415);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(22100);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(72234);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_10__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module mainmenu-extension
 */











const PLUGIN_ID = '@jupyterlab/mainmenu-extension:plugin';
/**
 * A namespace for command IDs of semantic extension points.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.openEdit = 'editmenu:open';
    CommandIDs.undo = 'editmenu:undo';
    CommandIDs.redo = 'editmenu:redo';
    CommandIDs.clearCurrent = 'editmenu:clear-current';
    CommandIDs.clearAll = 'editmenu:clear-all';
    CommandIDs.find = 'editmenu:find';
    CommandIDs.goToLine = 'editmenu:go-to-line';
    CommandIDs.openFile = 'filemenu:open';
    CommandIDs.closeAndCleanup = 'filemenu:close-and-cleanup';
    CommandIDs.createConsole = 'filemenu:create-console';
    CommandIDs.shutdown = 'filemenu:shutdown';
    CommandIDs.logout = 'filemenu:logout';
    CommandIDs.openKernel = 'kernelmenu:open';
    CommandIDs.interruptKernel = 'kernelmenu:interrupt';
    CommandIDs.reconnectToKernel = 'kernelmenu:reconnect-to-kernel';
    CommandIDs.restartKernel = 'kernelmenu:restart';
    CommandIDs.restartKernelAndClear = 'kernelmenu:restart-and-clear';
    CommandIDs.changeKernel = 'kernelmenu:change';
    CommandIDs.shutdownKernel = 'kernelmenu:shutdown';
    CommandIDs.shutdownAllKernels = 'kernelmenu:shutdownAll';
    CommandIDs.openView = 'viewmenu:open';
    CommandIDs.wordWrap = 'viewmenu:word-wrap';
    CommandIDs.lineNumbering = 'viewmenu:line-numbering';
    CommandIDs.matchBrackets = 'viewmenu:match-brackets';
    CommandIDs.openRun = 'runmenu:open';
    CommandIDs.run = 'runmenu:run';
    CommandIDs.runAll = 'runmenu:run-all';
    CommandIDs.restartAndRunAll = 'runmenu:restart-and-run-all';
    CommandIDs.runAbove = 'runmenu:run-above';
    CommandIDs.runBelow = 'runmenu:run-below';
    CommandIDs.openTabs = 'tabsmenu:open';
    CommandIDs.activateById = 'tabsmenu:activate-by-id';
    CommandIDs.activatePreviouslyUsedTab = 'tabsmenu:activate-previously-used-tab';
    CommandIDs.openSettings = 'settingsmenu:open';
    CommandIDs.openHelp = 'helpmenu:open';
    CommandIDs.getKernel = 'helpmenu:get-kernel';
    CommandIDs.openFirst = 'mainmenu:open-first';
})(CommandIDs || (CommandIDs = {}));
/**
 * A service providing an interface to the main menu.
 */
const plugin = {
    id: PLUGIN_ID,
    description: 'Adds and provides the application main menu.',
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.ISettingRegistry],
    provides: _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu,
    activate: async (app, router, translator, palette, labShell, registry) => {
        const { commands } = app;
        const trans = translator.load('jupyterlab');
        const menu = new _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.MainMenu(commands);
        menu.id = 'jp-MainMenu';
        menu.addClass('jp-scrollbar-tiny');
        // Built menu from settings
        if (registry) {
            await Private.loadSettingsMenu(registry, (aMenu) => {
                menu.addMenu(aMenu, false, { rank: aMenu.rank });
            }, options => _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.MainMenu.generateMenu(commands, options, trans), translator);
            // Trigger single update
            menu.update();
        }
        // Only add quit button if the back-end supports it by checking page config.
        const quitButton = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('quitButton').toLowerCase();
        menu.fileMenu.quitEntry = quitButton === 'true';
        // Create the application menus.
        createEditMenu(app, menu.editMenu, trans);
        createFileMenu(app, menu.fileMenu, router, trans);
        createKernelMenu(app, menu.kernelMenu, trans);
        createRunMenu(app, menu.runMenu, trans);
        createViewMenu(app, menu.viewMenu, trans);
        createHelpMenu(app, menu.helpMenu, trans);
        // The tabs menu relies on lab shell functionality.
        if (labShell) {
            createTabsMenu(app, menu.tabsMenu, labShell, trans);
        }
        // Create commands to open the main application menus.
        const activateMenu = (item) => {
            menu.activeMenu = item;
            menu.openActiveMenu();
        };
        commands.addCommand(CommandIDs.openEdit, {
            label: trans.__('Open Edit Menu'),
            execute: () => activateMenu(menu.editMenu)
        });
        commands.addCommand(CommandIDs.openFile, {
            label: trans.__('Open File Menu'),
            execute: () => activateMenu(menu.fileMenu)
        });
        commands.addCommand(CommandIDs.openKernel, {
            label: trans.__('Open Kernel Menu'),
            execute: () => activateMenu(menu.kernelMenu)
        });
        commands.addCommand(CommandIDs.openRun, {
            label: trans.__('Open Run Menu'),
            execute: () => activateMenu(menu.runMenu)
        });
        commands.addCommand(CommandIDs.openView, {
            label: trans.__('Open View Menu'),
            execute: () => activateMenu(menu.viewMenu)
        });
        commands.addCommand(CommandIDs.openSettings, {
            label: trans.__('Open Settings Menu'),
            execute: () => activateMenu(menu.settingsMenu)
        });
        commands.addCommand(CommandIDs.openTabs, {
            label: trans.__('Open Tabs Menu'),
            execute: () => activateMenu(menu.tabsMenu)
        });
        commands.addCommand(CommandIDs.openHelp, {
            label: trans.__('Open Help Menu'),
            execute: () => activateMenu(menu.helpMenu)
        });
        commands.addCommand(CommandIDs.openFirst, {
            label: trans.__('Open First Menu'),
            execute: () => {
                menu.activeIndex = 0;
                menu.openActiveMenu();
            }
        });
        if (palette) {
            // Add some of the commands defined here to the command palette.
            palette.addItem({
                command: CommandIDs.shutdown,
                category: trans.__('Main Area')
            });
            palette.addItem({
                command: CommandIDs.logout,
                category: trans.__('Main Area')
            });
            palette.addItem({
                command: CommandIDs.shutdownAllKernels,
                category: trans.__('Kernel Operations')
            });
            palette.addItem({
                command: CommandIDs.activatePreviouslyUsedTab,
                category: trans.__('Main Area')
            });
        }
        app.shell.add(menu, 'menu', { rank: 100 });
        return menu;
    }
};
/**
 * Create the basic `Edit` menu.
 */
function createEditMenu(app, menu, trans) {
    const commands = app.commands;
    // Add the undo/redo commands the the Edit menu.
    commands.addCommand(CommandIDs.undo, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.undoers.undo, {
        label: trans.__('Undo')
    }, trans));
    commands.addCommand(CommandIDs.redo, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.undoers.redo, {
        label: trans.__('Redo')
    }, trans));
    // Add the clear commands to the Edit menu.
    commands.addCommand(CommandIDs.clearCurrent, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.clearers.clearCurrent, {
        label: trans.__('Clear')
    }, trans));
    commands.addCommand(CommandIDs.clearAll, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.clearers.clearAll, {
        label: trans.__('Clear All')
    }, trans));
    commands.addCommand(CommandIDs.goToLine, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.goToLiners, {
        label: trans.__('Go to Line…')
    }, trans));
}
/**
 * Create the basic `File` menu.
 */
function createFileMenu(app, menu, router, trans) {
    const commands = app.commands;
    // Add a delegator command for closing and cleaning up an activity.
    // This one is a bit different, in that we consider it enabled
    // even if it cannot find a delegate for the activity.
    // In that case, we instead call the application `close` command.
    commands.addCommand(CommandIDs.closeAndCleanup, {
        ...(0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.closeAndCleaners, {
            execute: 'application:close',
            label: trans.__('Close and Shut Down'),
            isEnabled: true
        }, trans),
        isEnabled: () => !!app.shell.currentWidget && !!app.shell.currentWidget.title.closable
    });
    // Add a delegator command for creating a console for an activity.
    commands.addCommand(CommandIDs.createConsole, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.consoleCreators, {
        label: trans.__('New Console for Activity')
    }, trans));
    commands.addCommand(CommandIDs.shutdown, {
        label: trans.__('Shut Down'),
        caption: trans.__('Shut down JupyterLab'),
        isVisible: () => menu.quitEntry,
        isEnabled: () => menu.quitEntry,
        execute: () => {
            return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: trans.__('Shutdown confirmation'),
                body: trans.__('Please confirm you want to shut down JupyterLab.'),
                buttons: [
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(),
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: trans.__('Shut Down') })
                ]
            }).then(async (result) => {
                if (result.button.accept) {
                    const setting = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__.ServerConnection.makeSettings();
                    const apiURL = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(setting.baseUrl, 'api/shutdown');
                    // Shutdown all kernel and terminal sessions before shutting down the server
                    // If this fails, we continue execution so we can post an api/shutdown request
                    try {
                        await Promise.all([
                            app.serviceManager.sessions.shutdownAll(),
                            app.serviceManager.terminals.shutdownAll()
                        ]);
                    }
                    catch (e) {
                        // Do nothing
                        console.log(`Failed to shutdown sessions and terminals: ${e}`);
                    }
                    return _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__.ServerConnection.makeRequest(apiURL, { method: 'POST' }, setting)
                        .then(result => {
                        if (result.ok) {
                            // Close this window if the shutdown request has been successful
                            const body = document.createElement('div');
                            const p1 = document.createElement('p');
                            p1.textContent = trans.__('You have shut down the Jupyter server. You can now close this tab.');
                            const p2 = document.createElement('p');
                            p2.textContent = trans.__('To use JupyterLab again, you will need to relaunch it.');
                            body.appendChild(p1);
                            body.appendChild(p2);
                            void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                                title: trans.__('Server stopped'),
                                body: new _lumino_widgets__WEBPACK_IMPORTED_MODULE_10__.Widget({ node: body }),
                                buttons: []
                            });
                            window.close();
                        }
                        else {
                            throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__.ServerConnection.ResponseError(result);
                        }
                    })
                        .catch(data => {
                        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__.ServerConnection.NetworkError(data);
                    });
                }
            });
        }
    });
    commands.addCommand(CommandIDs.logout, {
        label: trans.__('Log Out'),
        caption: trans.__('Log out of JupyterLab'),
        isVisible: () => menu.quitEntry,
        isEnabled: () => menu.quitEntry,
        execute: () => {
            router.navigate('/logout', { hard: true });
        }
    });
}
/**
 * Create the basic `Kernel` menu.
 */
function createKernelMenu(app, menu, trans) {
    const commands = app.commands;
    commands.addCommand(CommandIDs.interruptKernel, {
        ...(0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.kernelUsers.interruptKernel, {
            label: trans.__('Interrupt Kernel'),
            caption: trans.__('Interrupt the kernel')
        }, trans),
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.stopIcon : undefined)
    });
    commands.addCommand(CommandIDs.reconnectToKernel, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.kernelUsers.reconnectToKernel, {
        label: trans.__('Reconnect to Kernel')
    }, trans));
    commands.addCommand(CommandIDs.restartKernel, {
        ...(0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.kernelUsers.restartKernel, {
            label: trans.__('Restart Kernel…'),
            caption: trans.__('Restart the kernel')
        }, trans),
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.refreshIcon : undefined)
    });
    commands.addCommand(CommandIDs.restartKernelAndClear, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, [menu.kernelUsers.restartKernel, menu.kernelUsers.clearWidget], {
        label: trans.__('Restart Kernel and Clear…')
    }, trans));
    commands.addCommand(CommandIDs.changeKernel, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.kernelUsers.changeKernel, {
        label: trans.__('Change Kernel…')
    }, trans));
    commands.addCommand(CommandIDs.shutdownKernel, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.kernelUsers.shutdownKernel, {
        label: trans.__('Shut Down Kernel'),
        caption: trans.__('Shut down kernel')
    }, trans));
    commands.addCommand(CommandIDs.shutdownAllKernels, {
        label: trans.__('Shut Down All Kernels…'),
        isEnabled: () => {
            return !app.serviceManager.sessions.running().next().done;
        },
        execute: () => {
            return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: trans.__('Shut Down All?'),
                body: trans.__('Shut down all kernels?'),
                buttons: [
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: trans.__('Dismiss') }),
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: trans.__('Shut Down All') })
                ]
            }).then(result => {
                if (result.button.accept) {
                    return app.serviceManager.sessions.shutdownAll();
                }
            });
        }
    });
}
/**
 * Create the basic `View` menu.
 */
function createViewMenu(app, menu, trans) {
    const commands = app.commands;
    commands.addCommand(CommandIDs.lineNumbering, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.editorViewers.toggleLineNumbers, {
        label: trans.__('Show Line Numbers')
    }, trans));
    commands.addCommand(CommandIDs.matchBrackets, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.editorViewers.toggleMatchBrackets, {
        label: trans.__('Match Brackets')
    }, trans));
    commands.addCommand(CommandIDs.wordWrap, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.editorViewers.toggleWordWrap, {
        label: trans.__('Wrap Words')
    }, trans));
}
/**
 * Create the basic `Run` menu.
 */
function createRunMenu(app, menu, trans) {
    const commands = app.commands;
    commands.addCommand(CommandIDs.run, {
        ...(0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.codeRunners.run, {
            label: trans.__('Run Selected'),
            caption: trans.__('Run Selected')
        }, trans),
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.runIcon : undefined)
    });
    commands.addCommand(CommandIDs.runAll, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.codeRunners.runAll, {
        label: trans.__('Run All'),
        caption: trans.__('Run All')
    }, trans));
    commands.addCommand(CommandIDs.restartAndRunAll, {
        ...(0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, [menu.codeRunners.restart, menu.codeRunners.runAll], {
            label: trans.__('Restart Kernel and Run All'),
            caption: trans.__('Restart Kernel and Run All')
        }, trans),
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.fastForwardIcon : undefined)
    });
}
/**
 * Create the basic `Tabs` menu.
 */
function createTabsMenu(app, menu, labShell, trans) {
    const commands = app.commands;
    // A list of the active tabs in the main area.
    const tabGroup = [];
    // A disposable for getting rid of the out-of-date tabs list.
    let disposable;
    // Command to activate a widget by id.
    commands.addCommand(CommandIDs.activateById, {
        label: args => {
            if (args.id === undefined) {
                return trans.__('Activate a widget by its `id`.');
            }
            const id = args['id'] || '';
            const widget = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__.find)(app.shell.widgets('main'), w => w.id === id);
            return (widget && widget.title.label) || '';
        },
        isToggled: args => {
            const id = args['id'] || '';
            return !!app.shell.currentWidget && app.shell.currentWidget.id === id;
        },
        execute: args => app.shell.activateById(args['id'] || '')
    });
    let previousId = '';
    // Command to toggle between the current
    // tab and the last modified tab.
    commands.addCommand(CommandIDs.activatePreviouslyUsedTab, {
        label: trans.__('Activate Previously Used Tab'),
        isEnabled: () => !!previousId,
        execute: () => commands.execute(CommandIDs.activateById, { id: previousId })
    });
    if (labShell) {
        void app.restored.then(() => {
            // Iterate over the current widgets in the
            // main area, and add them to the tab group
            // of the menu.
            const populateTabs = () => {
                // remove the previous tab list
                if (disposable && !disposable.isDisposed) {
                    disposable.dispose();
                }
                tabGroup.length = 0;
                let isPreviouslyUsedTabAttached = false;
                for (const widget of app.shell.widgets('main')) {
                    if (widget.id === previousId) {
                        isPreviouslyUsedTabAttached = true;
                    }
                    tabGroup.push({
                        command: CommandIDs.activateById,
                        args: { id: widget.id }
                    });
                }
                disposable = menu.addGroup(tabGroup, 1);
                previousId = isPreviouslyUsedTabAttached ? previousId : '';
            };
            populateTabs();
            labShell.layoutModified.connect(() => {
                populateTabs();
            });
            // Update the ID of the previous active tab if a new tab is selected.
            labShell.currentChanged.connect((_, args) => {
                const widget = args.oldValue;
                if (!widget) {
                    return;
                }
                previousId = widget.id;
            });
        });
    }
}
/**
 * Create the basic `Help` menu.
 */
function createHelpMenu(app, menu, trans) {
    app.commands.addCommand(CommandIDs.getKernel, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.getKernel, {
        label: trans.__('Get Kernel'),
        isVisible: false
    }, trans));
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * A namespace for Private data.
 */
var Private;
(function (Private) {
    async function displayInformation(trans) {
        const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
            title: trans.__('Information'),
            body: trans.__('Menu customization has changed. You will need to reload JupyterLab to see the changes.'),
            buttons: [
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(),
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Reload') })
            ]
        });
        if (result.button.accept) {
            location.reload();
        }
    }
    async function loadSettingsMenu(registry, addMenu, menuFactory, translator) {
        var _a;
        const trans = translator.load('jupyterlab');
        let canonical = null;
        let loaded = {};
        /**
         * Populate the plugin's schema defaults.
         */
        function populate(schema) {
            var _a, _b;
            loaded = {};
            const pluginDefaults = Object.keys(registry.plugins)
                .map(plugin => {
                var _a, _b;
                const menus = (_b = (_a = registry.plugins[plugin].schema['jupyter.lab.menus']) === null || _a === void 0 ? void 0 : _a.main) !== null && _b !== void 0 ? _b : [];
                loaded[plugin] = menus;
                return menus;
            })
                .concat([(_b = (_a = schema['jupyter.lab.menus']) === null || _a === void 0 ? void 0 : _a.main) !== null && _b !== void 0 ? _b : []])
                .reduceRight((acc, val) => _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.SettingRegistry.reconcileMenus(acc, val, true), schema.properties.menus.default);
            // Apply default value as last step to take into account overrides.json
            // The standard default being [] as the plugin must use `jupyter.lab.menus.main`
            // to define their default value.
            schema.properties.menus.default = _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.SettingRegistry.reconcileMenus(pluginDefaults, schema.properties.menus.default, true)
                // flatten one level
                .sort((a, b) => { var _a, _b; return ((_a = a.rank) !== null && _a !== void 0 ? _a : Infinity) - ((_b = b.rank) !== null && _b !== void 0 ? _b : Infinity); });
        }
        // Transform the plugin object to return different schema than the default.
        registry.transform(PLUGIN_ID, {
            compose: plugin => {
                var _a, _b, _c, _d;
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepCopy(plugin.schema);
                    populate(canonical);
                }
                const defaults = (_c = (_b = (_a = canonical.properties) === null || _a === void 0 ? void 0 : _a.menus) === null || _b === void 0 ? void 0 : _b.default) !== null && _c !== void 0 ? _c : [];
                const user = {
                    ...plugin.data.user,
                    menus: (_d = plugin.data.user.menus) !== null && _d !== void 0 ? _d : []
                };
                const composite = {
                    ...plugin.data.composite,
                    menus: _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.SettingRegistry.reconcileMenus(defaults, user.menus)
                };
                plugin.data = { composite, user };
                return plugin;
            },
            fetch: plugin => {
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepCopy(plugin.schema);
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
        const settings = await registry.load(PLUGIN_ID);
        const currentMenus = (_a = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepCopy(settings.composite.menus)) !== null && _a !== void 0 ? _a : [];
        const menus = new Array();
        // Create menu for non-disabled element
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MenuFactory.createMenus(currentMenus
            .filter(menu => !menu.disabled)
            .map(menu => {
            var _a;
            return {
                ...menu,
                items: _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.SettingRegistry.filterDisabledItems((_a = menu.items) !== null && _a !== void 0 ? _a : [])
            };
        }), menuFactory).forEach(menu => {
            menus.push(menu);
            addMenu(menu);
        });
        settings.changed.connect(() => {
            var _a;
            // As extension may change menu through API, prompt the user to reload if the
            // menu has been updated.
            const newMenus = (_a = settings.composite.menus) !== null && _a !== void 0 ? _a : [];
            if (!_lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepEqual(currentMenus, newMenus)) {
                void displayInformation(trans);
            }
        });
        registry.pluginChanged.connect(async (sender, plugin) => {
            var _a, _b, _c;
            if (plugin !== PLUGIN_ID) {
                // If the plugin changed its menu.
                const oldMenus = (_a = loaded[plugin]) !== null && _a !== void 0 ? _a : [];
                const newMenus = (_c = (_b = registry.plugins[plugin].schema['jupyter.lab.menus']) === null || _b === void 0 ? void 0 : _b.main) !== null && _c !== void 0 ? _c : [];
                if (!_lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepEqual(oldMenus, newMenus)) {
                    if (loaded[plugin]) {
                        // The plugin has changed, request the user to reload the UI - this should not happen
                        await displayInformation(trans);
                    }
                    else {
                        // The plugin was not yet loaded when the menu was built => update the menu
                        loaded[plugin] = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepCopy(newMenus);
                        // Merge potential disabled state
                        const toAdd = _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.SettingRegistry.reconcileMenus(newMenus, currentMenus, false, false)
                            .filter(menu => !menu.disabled)
                            .map(menu => {
                            var _a;
                            return {
                                ...menu,
                                items: _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.SettingRegistry.filterDisabledItems((_a = menu.items) !== null && _a !== void 0 ? _a : [])
                            };
                        });
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MenuFactory.updateMenus(menus, toAdd, menuFactory).forEach(menu => {
                            addMenu(menu);
                        });
                    }
                }
            }
        });
    }
    Private.loadSettingsMenu = loadSettingsMenu;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=1785.6973fbdd43e70e5d28a9.js.map?v=6973fbdd43e70e5d28a9