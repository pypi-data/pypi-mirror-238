"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[9484],{

/***/ 99484:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ToolbarItems": () => (/* binding */ ToolbarItems),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "downloadPlugin": () => (/* binding */ downloadPlugin),
/* harmony export */   "openBrowserTabPlugin": () => (/* binding */ openBrowserTabPlugin),
/* harmony export */   "pathStatusPlugin": () => (/* binding */ pathStatusPlugin),
/* harmony export */   "savingStatusPlugin": () => (/* binding */ savingStatusPlugin)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(65681);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(82545);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(78254);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(7280);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(89397);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(34853);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(76351);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(16415);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(22100);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(30205);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(72234);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(52850);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_12__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module docmanager-extension
 */













/**
 * The command IDs used by the document manager plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.clone = 'docmanager:clone';
    CommandIDs.deleteFile = 'docmanager:delete-file';
    CommandIDs.newUntitled = 'docmanager:new-untitled';
    CommandIDs.open = 'docmanager:open';
    CommandIDs.openBrowserTab = 'docmanager:open-browser-tab';
    CommandIDs.reload = 'docmanager:reload';
    CommandIDs.rename = 'docmanager:rename';
    CommandIDs.del = 'docmanager:delete';
    CommandIDs.duplicate = 'docmanager:duplicate';
    CommandIDs.restoreCheckpoint = 'docmanager:restore-checkpoint';
    CommandIDs.save = 'docmanager:save';
    CommandIDs.saveAll = 'docmanager:save-all';
    CommandIDs.saveAs = 'docmanager:save-as';
    CommandIDs.download = 'docmanager:download';
    CommandIDs.toggleAutosave = 'docmanager:toggle-autosave';
    CommandIDs.showInFileBrowser = 'docmanager:show-in-file-browser';
})(CommandIDs || (CommandIDs = {}));
/**
 * The id of the document manager plugin.
 */
const docManagerPluginId = '@jupyterlab/docmanager-extension:plugin';
/**
 * A plugin to open documents in the main area.
 *
 */
const openerPlugin = {
    id: '@jupyterlab/docmanager-extension:opener',
    description: 'Provides the widget opener.',
    autoStart: true,
    provides: _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentWidgetOpener,
    activate: (app) => {
        const { shell } = app;
        return new (class {
            constructor() {
                this._opened = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_10__.Signal(this);
            }
            open(widget, options) {
                if (!widget.id) {
                    widget.id = `document-manager-${++Private.id}`;
                }
                widget.title.dataset = {
                    type: 'document-title',
                    ...widget.title.dataset
                };
                if (!widget.isAttached) {
                    shell.add(widget, 'main', options || {});
                }
                shell.activateById(widget.id);
                this._opened.emit(widget);
            }
            get opened() {
                return this._opened;
            }
        })();
    }
};
/**
 * A plugin to handle dirty states for open documents.
 */
const contextsPlugin = {
    id: '@jupyterlab/docmanager-extension:contexts',
    description: 'Adds the handling of opened documents dirty state.',
    autoStart: true,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager, _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentWidgetOpener],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabStatus],
    activate: (app, docManager, widgetOpener, status) => {
        const contexts = new WeakSet();
        widgetOpener.opened.connect((_, widget) => {
            // Handle dirty state for open documents.
            const context = docManager.contextForWidget(widget);
            if (context && !contexts.has(context)) {
                if (status) {
                    handleContext(status, context);
                }
                contexts.add(context);
            }
        });
    }
};
/**
 * A plugin providing the default document manager.
 */
const manager = {
    id: '@jupyterlab/docmanager-extension:manager',
    description: 'Provides the document manager.',
    provides: _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentWidgetOpener],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabStatus, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ISessionContextDialogs, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterLab.IInfo],
    activate: (app, widgetOpener, translator_, status, sessionDialogs_, info) => {
        var _a;
        const { serviceManager: manager, docRegistry: registry } = app;
        const translator = translator_ !== null && translator_ !== void 0 ? translator_ : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator;
        const sessionDialogs = sessionDialogs_ !== null && sessionDialogs_ !== void 0 ? sessionDialogs_ : new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SessionContextDialogs({ translator });
        const when = app.restored.then(() => void 0);
        const docManager = new _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.DocumentManager({
            registry,
            manager,
            opener: widgetOpener,
            when,
            setBusy: (_a = (status && (() => status.setBusy()))) !== null && _a !== void 0 ? _a : undefined,
            sessionDialogs,
            translator: translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator,
            isConnectedCallback: () => {
                if (info) {
                    return info.isConnected;
                }
                return true;
            }
        });
        return docManager;
    }
};
/**
 * The default document manager provider commands and settings.
 */
const docManagerPlugin = {
    id: docManagerPluginId,
    description: 'Adds commands and settings to the document manager.',
    autoStart: true,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager, _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentWidgetOpener, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    activate: (app, docManager, widgetOpener, settingRegistry, translator, palette, labShell) => {
        translator = translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator;
        const trans = translator.load('jupyterlab');
        const registry = app.docRegistry;
        // Register the file operations commands.
        addCommands(app, docManager, widgetOpener, settingRegistry, translator, labShell, palette);
        // Keep up to date with the settings registry.
        const onSettingsUpdated = (settings) => {
            // Handle whether to autosave
            const autosave = settings.get('autosave').composite;
            docManager.autosave =
                autosave === true || autosave === false ? autosave : true;
            app.commands.notifyCommandChanged(CommandIDs.toggleAutosave);
            const confirmClosingDocument = settings.get('confirmClosingDocument')
                .composite;
            docManager.confirmClosingDocument = confirmClosingDocument !== null && confirmClosingDocument !== void 0 ? confirmClosingDocument : true;
            // Handle autosave interval
            const autosaveInterval = settings.get('autosaveInterval').composite;
            docManager.autosaveInterval = autosaveInterval || 120;
            // Handle last modified timestamp check margin
            const lastModifiedCheckMargin = settings.get('lastModifiedCheckMargin')
                .composite;
            docManager.lastModifiedCheckMargin = lastModifiedCheckMargin || 500;
            const renameUntitledFile = settings.get('renameUntitledFileOnSave')
                .composite;
            docManager.renameUntitledFileOnSave = renameUntitledFile !== null && renameUntitledFile !== void 0 ? renameUntitledFile : true;
            // Handle default widget factory overrides.
            const defaultViewers = settings.get('defaultViewers').composite;
            const overrides = {};
            // Filter the defaultViewers and file types for existing ones.
            Object.keys(defaultViewers).forEach(ft => {
                if (!registry.getFileType(ft)) {
                    console.warn(`File Type ${ft} not found`);
                    return;
                }
                if (!registry.getWidgetFactory(defaultViewers[ft])) {
                    console.warn(`Document viewer ${defaultViewers[ft]} not found`);
                }
                overrides[ft] = defaultViewers[ft];
            });
            // Set the default factory overrides. If not provided, this has the
            // effect of unsetting any previous overrides.
            for (const ft of registry.fileTypes()) {
                try {
                    registry.setDefaultWidgetFactory(ft.name, overrides[ft.name]);
                }
                catch (_a) {
                    console.warn(`Failed to set default viewer ${overrides[ft.name]} for file type ${ft.name}`);
                }
            }
        };
        // Fetch the initial state of the settings.
        Promise.all([settingRegistry.load(docManagerPluginId), app.restored])
            .then(([settings]) => {
            settings.changed.connect(onSettingsUpdated);
            onSettingsUpdated(settings);
            const onStateChanged = (sender, change) => {
                if ([
                    'autosave',
                    'autosaveInterval',
                    'confirmClosingDocument',
                    'lastModifiedCheckMargin',
                    'renameUntitledFileOnSave'
                ].includes(change.name) &&
                    settings.get(change.name).composite !== change.newValue) {
                    settings.set(change.name, change.newValue).catch(reason => {
                        console.error(`Failed to set the setting '${change.name}':\n${reason}`);
                    });
                }
            };
            docManager.stateChanged.connect(onStateChanged);
        })
            .catch((reason) => {
            console.error(reason.message);
        });
        // Register a fetch transformer for the settings registry,
        // allowing us to dynamically populate a help string with the
        // available document viewers and file types for the default
        // viewer overrides.
        settingRegistry.transform(docManagerPluginId, {
            fetch: plugin => {
                // Get the available file types.
                const fileTypes = Array.from(registry.fileTypes())
                    .map(ft => ft.name)
                    .join('    \n');
                // Get the available widget factories.
                const factories = Array.from(registry.widgetFactories())
                    .map(f => f.name)
                    .join('    \n');
                // Generate the help string.
                const description = trans.__(`Overrides for the default viewers for file types.
Specify a mapping from file type name to document viewer name, for example:

defaultViewers: {
  markdown: "Markdown Preview"
}

If you specify non-existent file types or viewers, or if a viewer cannot
open a given file type, the override will not function.

Available viewers:
%1

Available file types:
%2`, factories, fileTypes);
                const schema = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepCopy(plugin.schema);
                schema.properties.defaultViewers.description = description;
                return { ...plugin, schema };
            }
        });
        // If the document registry gains or loses a factory or file type,
        // regenerate the settings description with the available options.
        registry.changed.connect(() => settingRegistry.load(docManagerPluginId, true));
    }
};
/**
 * A plugin for adding a saving status item to the status bar.
 */
const savingStatusPlugin = {
    id: '@jupyterlab/docmanager-extension:saving-status',
    description: 'Adds a saving status indicator.',
    autoStart: true,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator, _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5__.IStatusBar],
    activate: (_, docManager, labShell, translator, statusBar) => {
        if (!statusBar) {
            // Automatically disable if statusbar missing
            return;
        }
        const saving = new _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.SavingStatus({
            docManager,
            translator: translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator
        });
        // Keep the currently active widget synchronized.
        saving.model.widget = labShell.currentWidget;
        labShell.currentChanged.connect(() => {
            saving.model.widget = labShell.currentWidget;
        });
        statusBar.registerStatusItem(savingStatusPlugin.id, {
            item: saving,
            align: 'middle',
            isActive: () => saving.model !== null && saving.model.status !== null,
            activeStateChanged: saving.model.stateChanged
        });
    }
};
/**
 * A plugin providing a file path widget to the status bar.
 */
const pathStatusPlugin = {
    id: '@jupyterlab/docmanager-extension:path-status',
    description: 'Adds a file path indicator in the status bar.',
    autoStart: true,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    optional: [_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5__.IStatusBar],
    activate: (_, docManager, labShell, statusBar) => {
        if (!statusBar) {
            // Automatically disable if statusbar missing
            return;
        }
        const path = new _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.PathStatus({ docManager });
        // Keep the file path widget up-to-date with the application active widget.
        path.model.widget = labShell.currentWidget;
        labShell.currentChanged.connect(() => {
            path.model.widget = labShell.currentWidget;
        });
        statusBar.registerStatusItem(pathStatusPlugin.id, {
            item: path,
            align: 'right',
            rank: 0
        });
    }
};
/**
 * A plugin providing download commands in the file menu and command palette.
 */
const downloadPlugin = {
    id: '@jupyterlab/docmanager-extension:download',
    description: 'Adds command to download files.',
    autoStart: true,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: (app, docManager, translator, palette) => {
        const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator).load('jupyterlab');
        const { commands, shell } = app;
        const isEnabled = () => {
            const { currentWidget } = shell;
            return !!(currentWidget && docManager.contextForWidget(currentWidget));
        };
        commands.addCommand(CommandIDs.download, {
            label: trans.__('Download'),
            caption: trans.__('Download the file to your computer'),
            isEnabled,
            execute: () => {
                // Checks that shell.currentWidget is valid:
                if (isEnabled()) {
                    const context = docManager.contextForWidget(shell.currentWidget);
                    if (!context) {
                        return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                            title: trans.__('Cannot Download'),
                            body: trans.__('No context found for current widget!'),
                            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton()]
                        });
                    }
                    return context.download();
                }
            }
        });
        const category = trans.__('File Operations');
        if (palette) {
            palette.addItem({ command: CommandIDs.download, category });
        }
    }
};
/**
 * A plugin providing open-browser-tab commands.
 *
 * This is its own plugin in case you would like to disable this feature.
 * e.g. jupyter labextension disable @jupyterlab/docmanager-extension:open-browser-tab
 *
 * Note: If disabling this, you may also want to disable:
 * @jupyterlab/filebrowser-extension:open-browser-tab
 */
const openBrowserTabPlugin = {
    id: '@jupyterlab/docmanager-extension:open-browser-tab',
    description: 'Adds command to open a browser tab.',
    autoStart: true,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    activate: (app, docManager, translator) => {
        const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator).load('jupyterlab');
        const { commands } = app;
        commands.addCommand(CommandIDs.openBrowserTab, {
            execute: args => {
                const path = typeof args['path'] === 'undefined' ? '' : args['path'];
                if (!path) {
                    return;
                }
                return docManager.services.contents.getDownloadUrl(path).then(url => {
                    const opened = window.open();
                    if (opened) {
                        opened.opener = null;
                        opened.location.href = url;
                    }
                    else {
                        throw new Error('Failed to open new browser tab.');
                    }
                });
            },
            iconClass: args => args['icon'] || '',
            label: () => trans.__('Open in New Browser Tab')
        });
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [
    manager,
    docManagerPlugin,
    contextsPlugin,
    pathStatusPlugin,
    savingStatusPlugin,
    downloadPlugin,
    openBrowserTabPlugin,
    openerPlugin
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);
/**
 * Toolbar item factory
 */
var ToolbarItems;
(function (ToolbarItems) {
    /**
     * Create save button toolbar item.
     *
     */
    function createSaveButton(commands, fileChanged) {
        return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.addCommandToolbarButtonClass)(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_12__.createElement(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.UseSignal, { signal: fileChanged }, () => (react__WEBPACK_IMPORTED_MODULE_12__.createElement(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.CommandToolbarButtonComponent, { commands: commands, id: CommandIDs.save, label: '', args: { toolbar: true } })))));
    }
    ToolbarItems.createSaveButton = createSaveButton;
})(ToolbarItems || (ToolbarItems = {}));
/* Widget to display the revert to checkpoint confirmation. */
class RevertConfirmWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_11__.Widget {
    /**
     * Construct a new revert confirmation widget.
     */
    constructor(checkpoint, trans, fileType = 'notebook') {
        super({
            node: Private.createRevertConfirmNode(checkpoint, fileType, trans)
        });
    }
}
// Returns the file type for a widget.
function fileType(widget, docManager) {
    if (!widget) {
        return 'File';
    }
    const context = docManager.contextForWidget(widget);
    if (!context) {
        return '';
    }
    const fts = docManager.registry.getFileTypesForPath(context.path);
    return fts.length && fts[0].displayName ? fts[0].displayName : 'File';
}
/**
 * Add the file operations commands to the application's command registry.
 */
function addCommands(app, docManager, widgetOpener, settingRegistry, translator, labShell, palette) {
    const trans = translator.load('jupyterlab');
    const { commands, shell } = app;
    const category = trans.__('File Operations');
    const isEnabled = () => {
        const { currentWidget } = shell;
        return !!(currentWidget && docManager.contextForWidget(currentWidget));
    };
    const isWritable = () => {
        var _a;
        const { currentWidget } = shell;
        if (!currentWidget) {
            return false;
        }
        const context = docManager.contextForWidget(currentWidget);
        return !!((_a = context === null || context === void 0 ? void 0 : context.contentsModel) === null || _a === void 0 ? void 0 : _a.writable);
    };
    // If inside a rich application like JupyterLab, add additional functionality.
    if (labShell) {
        addLabCommands(app, docManager, labShell, widgetOpener, translator);
    }
    commands.addCommand(CommandIDs.deleteFile, {
        label: () => `Delete ${fileType(shell.currentWidget, docManager)}`,
        execute: args => {
            const path = typeof args['path'] === 'undefined' ? '' : args['path'];
            if (!path) {
                const command = CommandIDs.deleteFile;
                throw new Error(`A non-empty path is required for ${command}.`);
            }
            return docManager.deleteFile(path);
        }
    });
    commands.addCommand(CommandIDs.newUntitled, {
        execute: args => {
            const errorTitle = args['error'] || trans.__('Error');
            const path = typeof args['path'] === 'undefined' ? '' : args['path'];
            const options = {
                type: args['type'],
                path
            };
            if (args['type'] === 'file') {
                options.ext = args['ext'] || '.txt';
            }
            return docManager.services.contents
                .newUntitled(options)
                .catch(error => (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)(errorTitle, error));
        },
        label: args => args['label'] || `New ${args['type']}`
    });
    commands.addCommand(CommandIDs.open, {
        execute: args => {
            const path = typeof args['path'] === 'undefined' ? '' : args['path'];
            const factory = args['factory'] || void 0;
            const kernel = args === null || args === void 0 ? void 0 : args.kernel;
            const options = args['options'] || void 0;
            return docManager.services.contents
                .get(path, { content: false })
                .then(() => docManager.openOrReveal(path, factory, kernel, options));
        },
        iconClass: args => args['icon'] || '',
        label: args => {
            var _a;
            return ((_a = (args['label'] || args['factory'])) !== null && _a !== void 0 ? _a : trans.__('Open the provided `path`.'));
        },
        mnemonic: args => args['mnemonic'] || -1
    });
    commands.addCommand(CommandIDs.reload, {
        label: () => trans.__('Reload %1 from Disk', fileType(shell.currentWidget, docManager)),
        caption: trans.__('Reload contents from disk'),
        isEnabled,
        execute: () => {
            // Checks that shell.currentWidget is valid:
            if (!isEnabled()) {
                return;
            }
            const context = docManager.contextForWidget(shell.currentWidget);
            const type = fileType(shell.currentWidget, docManager);
            if (!context) {
                return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Cannot Reload'),
                    body: trans.__('No context found for current widget!'),
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton()]
                });
            }
            if (context.model.dirty) {
                return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Reload %1 from Disk', type),
                    body: trans.__('Are you sure you want to reload the %1 from the disk?', type),
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(),
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: trans.__('Reload') })
                    ]
                }).then(result => {
                    if (result.button.accept && !context.isDisposed) {
                        return context.revert();
                    }
                });
            }
            else {
                if (!context.isDisposed) {
                    return context.revert();
                }
            }
        }
    });
    commands.addCommand(CommandIDs.restoreCheckpoint, {
        label: () => trans.__('Revert %1 to Checkpoint…', fileType(shell.currentWidget, docManager)),
        caption: trans.__('Revert contents to previous checkpoint'),
        isEnabled,
        execute: () => {
            // Checks that shell.currentWidget is valid:
            if (!isEnabled()) {
                return;
            }
            const context = docManager.contextForWidget(shell.currentWidget);
            if (!context) {
                return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Cannot Revert'),
                    body: trans.__('No context found for current widget!'),
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton()]
                });
            }
            return context.listCheckpoints().then(async (checkpoints) => {
                const type = fileType(shell.currentWidget, docManager);
                if (checkpoints.length < 1) {
                    await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)(trans.__('No checkpoints'), trans.__('No checkpoints are available for this %1.', type));
                    return;
                }
                const targetCheckpoint = checkpoints.length === 1
                    ? checkpoints[0]
                    : await Private.getTargetCheckpoint(checkpoints.reverse(), trans);
                if (!targetCheckpoint) {
                    return;
                }
                return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Revert %1 to checkpoint', type),
                    body: new RevertConfirmWidget(targetCheckpoint, trans, type),
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(),
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({
                            label: trans.__('Revert'),
                            ariaLabel: trans.__('Revert to Checkpoint')
                        })
                    ]
                }).then(result => {
                    if (context.isDisposed) {
                        return;
                    }
                    if (result.button.accept) {
                        if (context.model.readOnly) {
                            return context.revert();
                        }
                        return context
                            .restoreCheckpoint(targetCheckpoint.id)
                            .then(() => context.revert());
                    }
                });
            });
        }
    });
    const caption = () => {
        if (shell.currentWidget) {
            const context = docManager.contextForWidget(shell.currentWidget);
            if (context === null || context === void 0 ? void 0 : context.model.collaborative) {
                return trans.__('In collaborative mode, the document is saved automatically after every change');
            }
            if (!isWritable()) {
                return trans.__(`document is permissioned readonly; "save" is disabled, use "save as..." instead`);
            }
        }
        return trans.__('Save and create checkpoint');
    };
    const saveInProgress = new WeakSet();
    commands.addCommand(CommandIDs.save, {
        label: () => trans.__('Save %1', fileType(shell.currentWidget, docManager)),
        caption,
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.saveIcon : undefined),
        isEnabled: isWritable,
        execute: async () => {
            var _a, _b, _c;
            // Checks that shell.currentWidget is valid:
            const widget = shell.currentWidget;
            const context = docManager.contextForWidget(widget);
            if (isEnabled()) {
                if (!context) {
                    return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                        title: trans.__('Cannot Save'),
                        body: trans.__('No context found for current widget!'),
                        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton()]
                    });
                }
                else {
                    if (saveInProgress.has(context)) {
                        return;
                    }
                    if (context.model.readOnly) {
                        return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                            title: trans.__('Cannot Save'),
                            body: trans.__('Document is read-only'),
                            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton()]
                        });
                    }
                    saveInProgress.add(context);
                    const oldName = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PathExt.basename((_b = (_a = context.contentsModel) === null || _a === void 0 ? void 0 : _a.path) !== null && _b !== void 0 ? _b : '');
                    let newName = oldName;
                    if (docManager.renameUntitledFileOnSave &&
                        widget.isUntitled === true) {
                        const result = await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getText({
                            title: trans.__('Rename file'),
                            okLabel: trans.__('Rename'),
                            placeholder: trans.__('File name'),
                            text: oldName,
                            selectionRange: oldName.length - _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PathExt.extname(oldName).length,
                            checkbox: {
                                label: trans.__('Do not ask me again.'),
                                caption: trans.__('If checked, you will not be asked to rename future untitled files when saving them.')
                            }
                        });
                        if (result.button.accept) {
                            newName = (_c = result.value) !== null && _c !== void 0 ? _c : oldName;
                            widget.isUntitled = false;
                            if (typeof result.isChecked === 'boolean') {
                                const currentSetting = (await settingRegistry.get(docManagerPluginId, 'renameUntitledFileOnSave')).composite;
                                if (result.isChecked === currentSetting) {
                                    settingRegistry
                                        .set(docManagerPluginId, 'renameUntitledFileOnSave', !result.isChecked)
                                        .catch(reason => {
                                        console.error(`Fail to set 'renameUntitledFileOnSave:\n${reason}`);
                                    });
                                }
                            }
                        }
                    }
                    try {
                        await context.save();
                        if (!(widget === null || widget === void 0 ? void 0 : widget.isDisposed)) {
                            return context.createCheckpoint();
                        }
                    }
                    catch (err) {
                        // If the save was canceled by user-action, do nothing.
                        if (err.name === 'ModalCancelError') {
                            return;
                        }
                        throw err;
                    }
                    finally {
                        saveInProgress.delete(context);
                        if (newName !== oldName) {
                            await context.rename(newName);
                        }
                    }
                }
            }
        }
    });
    commands.addCommand(CommandIDs.saveAll, {
        label: () => trans.__('Save All'),
        caption: trans.__('Save all open documents'),
        isEnabled: () => {
            return (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__.some)(shell.widgets('main'), w => { var _a, _b, _c; return (_c = (_b = (_a = docManager.contextForWidget(w)) === null || _a === void 0 ? void 0 : _a.contentsModel) === null || _b === void 0 ? void 0 : _b.writable) !== null && _c !== void 0 ? _c : false; });
        },
        execute: () => {
            var _a;
            const promises = [];
            const paths = new Set(); // Cache so we don't double save files.
            for (const widget of shell.widgets('main')) {
                const context = docManager.contextForWidget(widget);
                if (context && !paths.has(context.path)) {
                    if ((_a = context.contentsModel) === null || _a === void 0 ? void 0 : _a.writable) {
                        paths.add(context.path);
                        promises.push(context.save());
                    }
                    else {
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.warning(trans.__(`%1 is permissioned as readonly. Use "save as..." instead.`, context.path), { autoClose: 5000 });
                    }
                }
            }
            return Promise.all(promises);
        }
    });
    commands.addCommand(CommandIDs.saveAs, {
        label: () => trans.__('Save %1 As…', fileType(shell.currentWidget, docManager)),
        caption: trans.__('Save with new path'),
        isEnabled,
        execute: () => {
            // Checks that shell.currentWidget is valid:
            if (isEnabled()) {
                const context = docManager.contextForWidget(shell.currentWidget);
                if (!context) {
                    return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                        title: trans.__('Cannot Save'),
                        body: trans.__('No context found for current widget!'),
                        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton()]
                    });
                }
                const onChange = (sender, args) => {
                    if (args.type === 'save' &&
                        args.newValue &&
                        args.newValue.path !== context.path) {
                        void docManager.closeFile(context.path);
                        void commands.execute(CommandIDs.open, {
                            path: args.newValue.path
                        });
                    }
                };
                docManager.services.contents.fileChanged.connect(onChange);
                context
                    .saveAs()
                    .finally(() => docManager.services.contents.fileChanged.disconnect(onChange));
            }
        }
    });
    commands.addCommand(CommandIDs.toggleAutosave, {
        label: trans.__('Autosave Documents'),
        isToggled: () => docManager.autosave,
        execute: () => {
            const value = !docManager.autosave;
            const key = 'autosave';
            return settingRegistry
                .set(docManagerPluginId, key, value)
                .catch((reason) => {
                console.error(`Failed to set ${docManagerPluginId}:${key} - ${reason.message}`);
            });
        }
    });
    if (palette) {
        [
            CommandIDs.reload,
            CommandIDs.restoreCheckpoint,
            CommandIDs.save,
            CommandIDs.saveAs,
            CommandIDs.toggleAutosave,
            CommandIDs.duplicate
        ].forEach(command => {
            palette.addItem({ command, category });
        });
    }
}
function addLabCommands(app, docManager, labShell, widgetOpener, translator) {
    const trans = translator.load('jupyterlab');
    const { commands } = app;
    // Returns the doc widget associated with the most recent contextmenu event.
    const contextMenuWidget = () => {
        var _a;
        const pathRe = /[Pp]ath:\s?(.*)\n?/;
        const test = (node) => { var _a; return !!((_a = node['title']) === null || _a === void 0 ? void 0 : _a.match(pathRe)); };
        const node = app.contextMenuHitTest(test);
        const pathMatch = node === null || node === void 0 ? void 0 : node['title'].match(pathRe);
        return ((_a = (pathMatch && docManager.findWidget(pathMatch[1], null))) !== null && _a !== void 0 ? _a : 
        // Fall back to active doc widget if path cannot be obtained from event.
        labShell.currentWidget);
    };
    // Returns `true` if the current widget has a document context.
    const isEnabled = () => {
        const { currentWidget } = labShell;
        return !!(currentWidget && docManager.contextForWidget(currentWidget));
    };
    commands.addCommand(CommandIDs.clone, {
        label: () => trans.__('New View for %1', fileType(contextMenuWidget(), docManager)),
        isEnabled,
        execute: args => {
            const widget = contextMenuWidget();
            const options = args['options'] || {
                mode: 'split-right'
            };
            if (!widget) {
                return;
            }
            // Clone the widget.
            const child = docManager.cloneWidget(widget);
            if (child) {
                widgetOpener.open(child, options);
            }
        }
    });
    commands.addCommand(CommandIDs.rename, {
        label: () => {
            let t = fileType(contextMenuWidget(), docManager);
            if (t) {
                t = ' ' + t;
            }
            return trans.__('Rename%1…', t);
        },
        isEnabled,
        execute: () => {
            // Implies contextMenuWidget() !== null
            if (isEnabled()) {
                const context = docManager.contextForWidget(contextMenuWidget());
                return (0,_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.renameDialog)(docManager, context);
            }
        }
    });
    commands.addCommand(CommandIDs.duplicate, {
        label: () => trans.__('Duplicate %1', fileType(contextMenuWidget(), docManager)),
        isEnabled,
        execute: () => {
            if (isEnabled()) {
                const context = docManager.contextForWidget(contextMenuWidget());
                if (!context) {
                    return;
                }
                return docManager.duplicate(context.path);
            }
        }
    });
    commands.addCommand(CommandIDs.del, {
        label: () => trans.__('Delete %1', fileType(contextMenuWidget(), docManager)),
        isEnabled,
        execute: async () => {
            // Implies contextMenuWidget() !== null
            if (isEnabled()) {
                const context = docManager.contextForWidget(contextMenuWidget());
                if (!context) {
                    return;
                }
                const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Delete'),
                    body: trans.__('Are you sure you want to delete %1', context.path),
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(),
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: trans.__('Delete') })
                    ]
                });
                if (result.button.accept) {
                    await app.commands.execute('docmanager:delete-file', {
                        path: context.path
                    });
                }
            }
        }
    });
    commands.addCommand(CommandIDs.showInFileBrowser, {
        label: () => trans.__('Show in File Browser'),
        isEnabled,
        execute: async () => {
            const widget = contextMenuWidget();
            const context = widget && docManager.contextForWidget(widget);
            if (!context) {
                return;
            }
            // 'activate' is needed if this command is selected in the "open tabs" sidebar
            await commands.execute('filebrowser:activate', { path: context.path });
            await commands.execute('filebrowser:go-to-path', { path: context.path });
        }
    });
}
/**
 * Handle dirty state for a context.
 */
function handleContext(status, context) {
    let disposable = null;
    const onStateChanged = (sender, args) => {
        if (args.name === 'dirty') {
            if (args.newValue === true) {
                if (!disposable) {
                    disposable = status.setDirty();
                }
            }
            else if (disposable) {
                disposable.dispose();
                disposable = null;
            }
        }
    };
    void context.ready.then(() => {
        context.model.stateChanged.connect(onStateChanged);
        if (context.model.dirty) {
            disposable = status.setDirty();
        }
    });
    context.disposed.connect(() => {
        if (disposable) {
            disposable.dispose();
        }
    });
}
/**
 * A namespace for private module data.
 */
var Private;
(function (Private) {
    /**
     * A counter for unique IDs.
     */
    Private.id = 0;
    function createRevertConfirmNode(checkpoint, fileType, trans) {
        const body = document.createElement('div');
        const confirmMessage = document.createElement('p');
        const confirmText = document.createTextNode(trans.__('Are you sure you want to revert the %1 to checkpoint? ', fileType));
        const cannotUndoText = document.createElement('strong');
        cannotUndoText.textContent = trans.__('This cannot be undone.');
        confirmMessage.appendChild(confirmText);
        confirmMessage.appendChild(cannotUndoText);
        const lastCheckpointMessage = document.createElement('p');
        const lastCheckpointText = document.createTextNode(trans.__('The checkpoint was last updated at: '));
        const lastCheckpointDate = document.createElement('p');
        const date = new Date(checkpoint.last_modified);
        lastCheckpointDate.style.textAlign = 'center';
        lastCheckpointDate.textContent =
            _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.Time.format(date) + ' (' + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.Time.formatHuman(date) + ')';
        lastCheckpointMessage.appendChild(lastCheckpointText);
        lastCheckpointMessage.appendChild(lastCheckpointDate);
        body.appendChild(confirmMessage);
        body.appendChild(lastCheckpointMessage);
        return body;
    }
    Private.createRevertConfirmNode = createRevertConfirmNode;
    /**
     * Ask user for a checkpoint to revert to.
     */
    async function getTargetCheckpoint(checkpoints, trans) {
        // the id could be too long to show so use the index instead
        const indexSeparator = '.';
        const items = checkpoints.map((checkpoint, index) => {
            const isoDate = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.Time.format(checkpoint.last_modified);
            const humanDate = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.Time.formatHuman(checkpoint.last_modified);
            return `${index}${indexSeparator} ${isoDate} (${humanDate})`;
        });
        const selectedItem = (await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getItem({
            items: items,
            title: trans.__('Choose a checkpoint')
        })).value;
        if (!selectedItem) {
            return;
        }
        const selectedIndex = selectedItem.split(indexSeparator, 1)[0];
        return checkpoints[parseInt(selectedIndex, 10)];
    }
    Private.getTargetCheckpoint = getTargetCheckpoint;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=9484.d7dff0d9d5aea8123c91.js.map?v=d7dff0d9d5aea8123c91