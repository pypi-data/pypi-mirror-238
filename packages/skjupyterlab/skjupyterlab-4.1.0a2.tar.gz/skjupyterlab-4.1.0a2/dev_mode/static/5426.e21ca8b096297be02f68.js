"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[5426,5728],{

/***/ 15426:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "CommandIDs": () => (/* binding */ CommandIDs),
  "default": () => (/* binding */ lib)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/application@~4.1.0-alpha.2 (singleton) (fallback: ../packages/application/lib/index.js)
var index_js_ = __webpack_require__(65681);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/running@~4.1.0-alpha.2 (strict) (fallback: ../packages/running/lib/index.js)
var lib_index_js_ = __webpack_require__(42319);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var coreutils_lib_index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: consume shared module (default) @lumino/polling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/polling/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(81967);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(30205);
;// CONCATENATED MODULE: ../packages/running-extension/lib/kernels.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





const ITEM_CLASS = 'jp-mod-kernel';
/**
 * Add the running kernel manager (notebooks & consoles) to the running panel.
 */
async function addKernelRunningSessionManager(managers, translator, app) {
    const { commands, contextMenu, serviceManager } = app;
    const { kernels, kernelspecs, sessions } = serviceManager;
    const { runningChanged, RunningKernel } = Private;
    const throttler = new index_es6_js_.Throttler(() => runningChanged.emit(undefined), 100);
    const trans = translator.load('jupyterlab');
    // Throttle signal emissions from the kernel and session managers.
    kernels.runningChanged.connect(() => void throttler.invoke());
    sessions.runningChanged.connect(() => void throttler.invoke());
    // Wait until the relevant services are ready.
    await Promise.all([kernels.ready, kernelspecs.ready, sessions.ready]);
    // Add the kernels pane to the running sidebar.
    managers.add({
        name: trans.__('Kernels'),
        running: () => Array.from(kernels.running()).map(kernel => {
            var _a;
            return new RunningKernel({
                commands,
                kernel,
                kernels,
                sessions,
                spec: (_a = kernelspecs.specs) === null || _a === void 0 ? void 0 : _a.kernelspecs[kernel.name],
                trans
            });
        }),
        shutdownAll: () => kernels.shutdownAll(),
        refreshRunning: () => Promise.all([kernels.refreshRunning(), sessions.refreshRunning()]),
        runningChanged,
        shutdownLabel: trans.__('Shut Down Kernel'),
        shutdownAllLabel: trans.__('Shut Down All'),
        shutdownAllConfirmationText: trans.__('Are you sure you want to permanently shut down all running kernels?')
    });
    // Add running kernels commands to the registry.
    const test = (node) => node.classList.contains(ITEM_CLASS);
    commands.addCommand(CommandIDs.kernelNewConsole, {
        icon: ui_components_lib_index_js_.consoleIcon,
        label: trans.__('New Console for Kernel'),
        execute: args => {
            var _a;
            const node = app.contextMenuHitTest(test);
            const id = (_a = args.id) !== null && _a !== void 0 ? _a : node === null || node === void 0 ? void 0 : node.dataset['context'];
            if (id) {
                return commands.execute('console:create', { kernelPreference: { id } });
            }
        }
    });
    commands.addCommand(CommandIDs.kernelNewNotebook, {
        icon: ui_components_lib_index_js_.notebookIcon,
        label: trans.__('New Notebook for Kernel'),
        execute: args => {
            var _a;
            const node = app.contextMenuHitTest(test);
            const id = (_a = args.id) !== null && _a !== void 0 ? _a : node === null || node === void 0 ? void 0 : node.dataset['context'];
            if (id) {
                return commands.execute('notebook:create-new', { kernelId: id });
            }
        }
    });
    commands.addCommand(CommandIDs.kernelOpenSession, {
        icon: args => args.type === 'console'
            ? ui_components_lib_index_js_.consoleIcon
            : args.type === 'notebook'
                ? ui_components_lib_index_js_.notebookIcon
                : undefined,
        isEnabled: ({ path, type }) => !!type || path !== undefined,
        label: ({ name, path }) => name ||
            coreutils_lib_index_js_.PathExt.basename(path || trans.__('Unknown Session')),
        execute: ({ path, type }) => {
            if (!type || path === undefined) {
                return;
            }
            const command = type === 'console' ? 'console:open' : 'docmanager:open';
            return commands.execute(command, { path });
        }
    });
    commands.addCommand(CommandIDs.kernelShutDown, {
        icon: ui_components_lib_index_js_.closeIcon,
        label: trans.__('Shut Down Kernel'),
        execute: args => {
            var _a;
            const node = app.contextMenuHitTest(test);
            const id = (_a = args.id) !== null && _a !== void 0 ? _a : node === null || node === void 0 ? void 0 : node.dataset['context'];
            if (id) {
                return kernels.shutdown(id);
            }
        }
    });
    const sessionsItems = [];
    // Populate connected sessions submenu when context menu is opened.
    contextMenu.opened.connect(async () => {
        var _a, _b, _c;
        const submenu = (_b = (_a = contextMenu.menu.items.find(item => {
            var _a;
            return item.type === 'submenu' &&
                ((_a = item.submenu) === null || _a === void 0 ? void 0 : _a.id) === 'jp-contextmenu-connected-sessions';
        })) === null || _a === void 0 ? void 0 : _a.submenu) !== null && _b !== void 0 ? _b : null;
        if (!submenu) {
            // Bail early if the connected session menu is not found
            return;
        }
        // Empty the connected sessions submenu.
        sessionsItems.forEach(item => item.dispose());
        sessionsItems.length = 0;
        submenu.clearItems();
        const node = app.contextMenuHitTest(test);
        const id = node === null || node === void 0 ? void 0 : node.dataset['context'];
        if (!id) {
            return;
        }
        // Populate the submenu with sessions connected to this kernel.
        const command = CommandIDs.kernelOpenSession;
        for (const session of sessions.running()) {
            if (id === ((_c = session.kernel) === null || _c === void 0 ? void 0 : _c.id)) {
                const { name, path, type } = session;
                sessionsItems.push(submenu.addItem({ command, args: { name, path, type } }));
            }
        }
    });
}
var Private;
(function (Private) {
    class RunningKernel {
        constructor(options) {
            this.className = ITEM_CLASS;
            this.commands = options.commands;
            this.kernel = options.kernel;
            this.context = this.kernel.id;
            this.kernels = options.kernels;
            this.sessions = options.sessions;
            this.spec = options.spec || null;
            this.trans = options.trans;
        }
        get children() {
            var _a;
            const children = [];
            const open = CommandIDs.kernelOpenSession;
            const { commands } = this;
            for (const session of this.sessions.running()) {
                if (this.kernel.id === ((_a = session.kernel) === null || _a === void 0 ? void 0 : _a.id)) {
                    const { name, path, type } = session;
                    children.push({
                        className: ITEM_CLASS,
                        context: this.kernel.id,
                        open: () => void commands.execute(open, { name, path, type }),
                        icon: () => type === 'console'
                            ? ui_components_lib_index_js_.consoleIcon
                            : type === 'notebook'
                                ? ui_components_lib_index_js_.notebookIcon
                                : ui_components_lib_index_js_.jupyterIcon,
                        label: () => name,
                        labelTitle: () => path
                    });
                }
            }
            return children;
        }
        shutdown() {
            return this.kernels.shutdown(this.kernel.id);
        }
        icon() {
            const { spec } = this;
            if (!spec || !spec.resources) {
                return ui_components_lib_index_js_.jupyterIcon;
            }
            return (spec.resources['logo-svg'] ||
                spec.resources['logo-64x64'] ||
                spec.resources['logo-32x32']);
        }
        label() {
            const { kernel, spec } = this;
            return (spec === null || spec === void 0 ? void 0 : spec.display_name) || kernel.name;
        }
        labelTitle() {
            var _a;
            const { trans } = this;
            const { id } = this.kernel;
            const title = [`${this.label()}: ${id}`];
            for (const session of this.sessions.running()) {
                if (this.kernel.id === ((_a = session.kernel) === null || _a === void 0 ? void 0 : _a.id)) {
                    const { path, type } = session;
                    title.push(trans.__(`%1\nPath: %2`, type, path));
                }
            }
            return title.join('\n\n');
        }
    }
    Private.RunningKernel = RunningKernel;
    Private.runningChanged = new dist_index_es6_js_.Signal({});
})(Private || (Private = {}));

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/docregistry@~4.1.0-alpha.2 (strict) (fallback: ../packages/docregistry/lib/index.js)
var docregistry_lib_index_js_ = __webpack_require__(16564);
;// CONCATENATED MODULE: ../packages/running-extension/lib/opentabs.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * A class used to consolidate the signals used to rerender the open tabs section.
 */
class OpenTabsSignaler {
    constructor(labShell) {
        this._tabsChanged = new dist_index_es6_js_.Signal(this);
        this._widgets = [];
        this._labShell = labShell;
        this._labShell.layoutModified.connect(this._emitTabsChanged, this);
    }
    /**
     * A signal that fires when the open tabs section should be rerendered.
     */
    get tabsChanged() {
        return this._tabsChanged;
    }
    /**
     * Add a widget to watch for title changing.
     *
     * @param widget A widget whose title may change.
     */
    addWidget(widget) {
        widget.title.changed.connect(this._emitTabsChanged, this);
        this._widgets.push(widget);
    }
    /**
     * Emit the main signal that indicates the open tabs should be rerendered.
     */
    _emitTabsChanged() {
        this._widgets.forEach(widget => {
            widget.title.changed.disconnect(this._emitTabsChanged, this);
        });
        this._widgets = [];
        this._tabsChanged.emit(void 0);
    }
}
/**
 * Add the open tabs section to the running panel.
 *
 * @param managers - The IRunningSessionManagers used to register this section.
 * @param translator - The translator to use.
 * @param labShell - The ILabShell.
 */
function addOpenTabsSessionManager(managers, translator, labShell) {
    const signaler = new OpenTabsSignaler(labShell);
    const trans = translator.load('jupyterlab');
    managers.add({
        name: trans.__('Open Tabs'),
        running: () => {
            return Array.from(labShell.widgets('main')).map((widget) => {
                signaler.addWidget(widget);
                return new OpenTab(widget);
            });
        },
        shutdownAll: () => {
            for (const widget of labShell.widgets('main')) {
                widget.close();
            }
        },
        refreshRunning: () => {
            return void 0;
        },
        runningChanged: signaler.tabsChanged,
        shutdownLabel: trans.__('Close'),
        shutdownAllLabel: trans.__('Close All'),
        shutdownAllConfirmationText: trans.__('Are you sure you want to close all open tabs?')
    });
    class OpenTab {
        constructor(widget) {
            this._widget = widget;
        }
        open() {
            labShell.activateById(this._widget.id);
        }
        shutdown() {
            this._widget.close();
        }
        icon() {
            const widgetIcon = this._widget.title.icon;
            return widgetIcon instanceof ui_components_lib_index_js_.LabIcon ? widgetIcon : ui_components_lib_index_js_.fileIcon;
        }
        label() {
            return this._widget.title.label;
        }
        labelTitle() {
            let labelTitle;
            if (this._widget instanceof docregistry_lib_index_js_.DocumentWidget) {
                labelTitle = this._widget.context.path;
            }
            else {
                labelTitle = this._widget.title.label;
            }
            return labelTitle;
        }
    }
}

;// CONCATENATED MODULE: ../packages/running-extension/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module running-extension
 */






/**
 * The command IDs used by the running plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.kernelNewConsole = 'running:kernel-new-console';
    CommandIDs.kernelNewNotebook = 'running:kernel-new-notebook';
    CommandIDs.kernelOpenSession = 'running:kernel-open-session';
    CommandIDs.kernelShutDown = 'running:kernel-shut-down';
    CommandIDs.showPanel = 'running:show-panel';
})(CommandIDs || (CommandIDs = {}));
/**
 * The default running sessions extension.
 */
const lib_plugin = {
    activate,
    id: '@jupyterlab/running-extension:plugin',
    description: 'Provides the running session managers.',
    provides: lib_index_js_.IRunningSessionManagers,
    requires: [translation_lib_index_js_.ITranslator],
    optional: [index_js_.ILayoutRestorer, index_js_.ILabShell],
    autoStart: true
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const lib = (lib_plugin);
/**
 * Activate the running plugin.
 */
function activate(app, translator, restorer, labShell) {
    const trans = translator.load('jupyterlab');
    const runningSessionManagers = new lib_index_js_.RunningSessionManagers();
    const running = new lib_index_js_.RunningSessions(runningSessionManagers, translator);
    running.id = 'jp-running-sessions';
    running.title.caption = trans.__('Running Terminals and Kernels');
    running.title.icon = ui_components_lib_index_js_.runningIcon;
    running.node.setAttribute('role', 'region');
    running.node.setAttribute('aria-label', trans.__('Running Sessions section'));
    // Let the application restorer track the running panel for restoration of
    // application state (e.g. setting the running panel as the current side bar
    // widget).
    if (restorer) {
        restorer.add(running, 'running-sessions');
    }
    if (labShell) {
        addOpenTabsSessionManager(runningSessionManagers, translator, labShell);
    }
    void addKernelRunningSessionManager(runningSessionManagers, translator, app);
    // Rank has been chosen somewhat arbitrarily to give priority to the running
    // sessions widget in the sidebar.
    app.shell.add(running, 'left', { rank: 200, type: 'Sessions and Tabs' });
    app.commands.addCommand(CommandIDs.showPanel, {
        label: trans.__('Sessions and Tabs'),
        execute: () => {
            app.shell.activateById(running.id);
        }
    });
    return runningSessionManagers;
}


/***/ })

}]);
//# sourceMappingURL=5426.e21ca8b096297be02f68.js.map?v=e21ca8b096297be02f68