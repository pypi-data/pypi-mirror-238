"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[1036],{

/***/ 51036:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "DocumentManager": () => (/* reexport */ DocumentManager),
  "DocumentWidgetManager": () => (/* reexport */ DocumentWidgetManager),
  "IDocumentManager": () => (/* reexport */ IDocumentManager),
  "IDocumentWidgetOpener": () => (/* reexport */ IDocumentWidgetOpener),
  "PathStatus": () => (/* reexport */ PathStatus),
  "SaveHandler": () => (/* reexport */ SaveHandler),
  "SavingStatus": () => (/* reexport */ SavingStatus),
  "isValidFileName": () => (/* reexport */ isValidFileName),
  "renameDialog": () => (/* reexport */ renameDialog),
  "renameFile": () => (/* reexport */ renameFile),
  "shouldOverwrite": () => (/* reexport */ shouldOverwrite)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var lib_index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/docmanager/lib/dialogs.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * The class name added to file dialogs.
 */
const FILE_DIALOG_CLASS = 'jp-FileDialog';
/**
 * The class name added for the new name label in the rename dialog
 */
const RENAME_NEW_NAME_TITLE_CLASS = 'jp-new-name-title';
/**
 * Rename a file with a dialog.
 */
function renameDialog(manager, context, translator) {
    translator = translator || translation_lib_index_js_.nullTranslator;
    const trans = translator.load('jupyterlab');
    const localPath = context.localPath.split('/');
    const fileName = localPath.pop() || context.localPath;
    return (0,index_js_.showDialog)({
        title: trans.__('Rename File'),
        body: new RenameHandler(fileName),
        focusNodeSelector: 'input',
        buttons: [
            index_js_.Dialog.cancelButton(),
            index_js_.Dialog.okButton({
                label: trans.__('Rename'),
                ariaLabel: trans.__('Rename File')
            })
        ]
    }).then(result => {
        if (!result.value) {
            return null;
        }
        if (!isValidFileName(result.value)) {
            void (0,index_js_.showErrorMessage)(trans.__('Rename Error'), Error(trans.__('"%1" is not a valid name for a file. Names must have nonzero length, and cannot include "/", "\\", or ":"', result.value)));
            return null;
        }
        return context.rename(result.value);
    });
}
/**
 * Rename a file, asking for confirmation if it is overwriting another.
 */
function renameFile(manager, oldPath, newPath) {
    return manager.rename(oldPath, newPath).catch(error => {
        if (error.response.status !== 409) {
            // if it's not caused by an already existing file, rethrow
            throw error;
        }
        // otherwise, ask for confirmation
        return shouldOverwrite(newPath).then((value) => {
            if (value) {
                return manager.overwrite(oldPath, newPath);
            }
            return Promise.reject('File not renamed');
        });
    });
}
/**
 * Ask the user whether to overwrite a file.
 */
function shouldOverwrite(path, translator) {
    translator = translator || translation_lib_index_js_.nullTranslator;
    const trans = translator.load('jupyterlab');
    const options = {
        title: trans.__('Overwrite file?'),
        body: trans.__('"%1" already exists, overwrite?', path),
        buttons: [
            index_js_.Dialog.cancelButton(),
            index_js_.Dialog.warnButton({
                label: trans.__('Overwrite'),
                ariaLabel: trans.__('Overwrite Existing File')
            })
        ]
    };
    return (0,index_js_.showDialog)(options).then(result => {
        return Promise.resolve(result.button.accept);
    });
}
/**
 * Test whether a name is a valid file name
 *
 * Disallows "/", "\", and ":" in file names, as well as names with zero length.
 */
function isValidFileName(name) {
    const validNameExp = /[\/\\:]/;
    return name.length > 0 && !validNameExp.test(name);
}
/**
 * A widget used to rename a file.
 */
class RenameHandler extends index_es6_js_.Widget {
    /**
     * Construct a new "rename" dialog.
     */
    constructor(oldPath) {
        super({ node: Private.createRenameNode(oldPath) });
        this.addClass(FILE_DIALOG_CLASS);
        const ext = lib_index_js_.PathExt.extname(oldPath);
        const value = (this.inputNode.value = lib_index_js_.PathExt.basename(oldPath));
        this.inputNode.setSelectionRange(0, value.length - ext.length);
    }
    /**
     * Get the input text node.
     */
    get inputNode() {
        return this.node.getElementsByTagName('input')[0];
    }
    /**
     * Get the value of the widget.
     */
    getValue() {
        return this.inputNode.value;
    }
}
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * Create the node for a rename handler.
     */
    function createRenameNode(oldPath, translator) {
        translator = translator || translation_lib_index_js_.nullTranslator;
        const trans = translator.load('jupyterlab');
        const body = document.createElement('div');
        const existingLabel = document.createElement('label');
        existingLabel.textContent = trans.__('File Path');
        const existingPath = document.createElement('span');
        existingPath.textContent = oldPath;
        const nameTitle = document.createElement('label');
        nameTitle.textContent = trans.__('New Name');
        nameTitle.className = RENAME_NEW_NAME_TITLE_CLASS;
        const name = document.createElement('input');
        body.appendChild(existingLabel);
        body.appendChild(existingPath);
        body.appendChild(nameTitle);
        body.appendChild(name);
        return body;
    }
    Private.createRenameNode = createRenameNode;
})(Private || (Private = {}));

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/docregistry@~4.1.0-alpha.2 (strict) (fallback: ../packages/docregistry/lib/index.js)
var docregistry_lib_index_js_ = __webpack_require__(16564);
// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(16415);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @lumino/properties@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/properties/dist/index.es6.js)
var properties_dist_index_es6_js_ = __webpack_require__(64260);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var signaling_dist_index_es6_js_ = __webpack_require__(30205);
;// CONCATENATED MODULE: ../packages/docmanager/lib/savehandler.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A class that manages the auto saving of a document.
 *
 * #### Notes
 * Implements https://github.com/ipython/ipython/wiki/IPEP-15:-Autosaving-the-IPython-Notebook.
 */
class SaveHandler {
    /**
     * Construct a new save handler.
     */
    constructor(options) {
        this._autosaveTimer = -1;
        this._minInterval = -1;
        this._interval = -1;
        this._isActive = false;
        this._inDialog = false;
        this._isDisposed = false;
        this._multiplier = 10;
        this._context = options.context;
        this._isConnectedCallback = options.isConnectedCallback || (() => true);
        const interval = options.saveInterval || 120;
        this._minInterval = interval * 1000;
        this._interval = this._minInterval;
        // Restart the timer when the contents model is updated.
        this._context.fileChanged.connect(this._setTimer, this);
        this._context.disposed.connect(this.dispose, this);
    }
    /**
     * The save interval used by the timer (in seconds).
     */
    get saveInterval() {
        return this._interval / 1000;
    }
    set saveInterval(value) {
        this._minInterval = this._interval = value * 1000;
        if (this._isActive) {
            this._setTimer();
        }
    }
    /**
     * Get whether the handler is active.
     */
    get isActive() {
        return this._isActive;
    }
    /**
     * Get whether the save handler is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources used by the save handler.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        clearTimeout(this._autosaveTimer);
        signaling_dist_index_es6_js_.Signal.clearData(this);
    }
    /**
     * Start the autosaver.
     */
    start() {
        this._isActive = true;
        this._setTimer();
    }
    /**
     * Stop the autosaver.
     */
    stop() {
        this._isActive = false;
        clearTimeout(this._autosaveTimer);
    }
    /**
     * Set the timer.
     */
    _setTimer() {
        clearTimeout(this._autosaveTimer);
        if (!this._isActive) {
            return;
        }
        this._autosaveTimer = window.setTimeout(() => {
            if (this._isConnectedCallback()) {
                this._save();
            }
        }, this._interval);
    }
    /**
     * Handle an autosave timeout.
     */
    _save() {
        const context = this._context;
        // Trigger the next update.
        this._setTimer();
        if (!context) {
            return;
        }
        // Bail if the model is not dirty or the file is not writable, or the dialog
        // is already showing.
        const writable = context.contentsModel && context.contentsModel.writable;
        if (!writable || !context.model.dirty || this._inDialog) {
            return;
        }
        const start = new Date().getTime();
        context
            .save()
            .then(() => {
            if (this.isDisposed) {
                return;
            }
            const duration = new Date().getTime() - start;
            // New save interval: higher of 10x save duration or min interval.
            this._interval = Math.max(this._multiplier * duration, this._minInterval);
            // Restart the update to pick up the new interval.
            this._setTimer();
        })
            .catch(err => {
            // If the user canceled the save, do nothing.
            const { name } = err;
            if (name === 'ModalCancelError' || name === 'ModalDuplicateError') {
                return;
            }
            // Otherwise, log the error.
            console.error('Error in Auto-Save', err.message);
        });
    }
}

// EXTERNAL MODULE: consume shared module (default) @lumino/disposable@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/disposable/dist/index.es6.js)
var disposable_dist_index_es6_js_ = __webpack_require__(78612);
// EXTERNAL MODULE: consume shared module (default) @lumino/messaging@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/messaging/dist/index.es6.js)
var messaging_dist_index_es6_js_ = __webpack_require__(85755);
;// CONCATENATED MODULE: ../packages/docmanager/lib/widgetmanager.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








/**
 * The class name added to document widgets.
 */
const DOCUMENT_CLASS = 'jp-Document';
/**
 * A class that maintains the lifecycle of file-backed widgets.
 */
class DocumentWidgetManager {
    /**
     * Construct a new document widget manager.
     */
    constructor(options) {
        this._activateRequested = new signaling_dist_index_es6_js_.Signal(this);
        this._confirmClosingTab = false;
        this._isDisposed = false;
        this._stateChanged = new signaling_dist_index_es6_js_.Signal(this);
        this._registry = options.registry;
        this.translator = options.translator || translation_lib_index_js_.nullTranslator;
    }
    /**
     * A signal emitted when one of the documents is activated.
     */
    get activateRequested() {
        return this._activateRequested;
    }
    /**
     * Whether to ask confirmation to close a tab or not.
     */
    get confirmClosingDocument() {
        return this._confirmClosingTab;
    }
    set confirmClosingDocument(v) {
        if (this._confirmClosingTab !== v) {
            const oldValue = this._confirmClosingTab;
            this._confirmClosingTab = v;
            this._stateChanged.emit({
                name: 'confirmClosingDocument',
                oldValue,
                newValue: v
            });
        }
    }
    /**
     * Signal triggered when an attribute changes.
     */
    get stateChanged() {
        return this._stateChanged;
    }
    /**
     * Test whether the document widget manager is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources used by the widget manager.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        signaling_dist_index_es6_js_.Signal.disconnectReceiver(this);
    }
    /**
     * Create a widget for a document and handle its lifecycle.
     *
     * @param factory - The widget factory.
     *
     * @param context - The document context object.
     *
     * @returns A widget created by the factory.
     *
     * @throws If the factory is not registered.
     */
    createWidget(factory, context) {
        const widget = factory.createNew(context);
        this._initializeWidget(widget, factory, context);
        return widget;
    }
    /**
     * When a new widget is created, we need to hook it up
     * with some signals, update the widget extensions (for
     * this kind of widget) in the docregistry, among
     * other things.
     */
    _initializeWidget(widget, factory, context) {
        widgetmanager_Private.factoryProperty.set(widget, factory);
        // Handle widget extensions.
        const disposables = new disposable_dist_index_es6_js_.DisposableSet();
        for (const extender of this._registry.widgetExtensions(factory.name)) {
            const disposable = extender.createNew(widget, context);
            if (disposable) {
                disposables.add(disposable);
            }
        }
        widgetmanager_Private.disposablesProperty.set(widget, disposables);
        widget.disposed.connect(this._onWidgetDisposed, this);
        this.adoptWidget(context, widget);
        context.fileChanged.connect(this._onFileChanged, this);
        context.pathChanged.connect(this._onPathChanged, this);
        void context.ready.then(() => {
            void this.setCaption(widget);
        });
    }
    /**
     * Install the message hook for the widget and add to list
     * of known widgets.
     *
     * @param context - The document context object.
     *
     * @param widget - The widget to adopt.
     */
    adoptWidget(context, widget) {
        const widgets = widgetmanager_Private.widgetsProperty.get(context);
        widgets.push(widget);
        messaging_dist_index_es6_js_.MessageLoop.installMessageHook(widget, this);
        widget.addClass(DOCUMENT_CLASS);
        widget.title.closable = true;
        widget.disposed.connect(this._widgetDisposed, this);
        widgetmanager_Private.contextProperty.set(widget, context);
    }
    /**
     * See if a widget already exists for the given context and widget name.
     *
     * @param context - The document context object.
     *
     * @returns The found widget, or `undefined`.
     *
     * #### Notes
     * This can be used to use an existing widget instead of opening
     * a new widget.
     */
    findWidget(context, widgetName) {
        const widgets = widgetmanager_Private.widgetsProperty.get(context);
        if (!widgets) {
            return undefined;
        }
        return (0,dist_index_es6_js_.find)(widgets, widget => {
            const factory = widgetmanager_Private.factoryProperty.get(widget);
            if (!factory) {
                return false;
            }
            return factory.name === widgetName;
        });
    }
    /**
     * Get the document context for a widget.
     *
     * @param widget - The widget of interest.
     *
     * @returns The context associated with the widget, or `undefined`.
     */
    contextForWidget(widget) {
        return widgetmanager_Private.contextProperty.get(widget);
    }
    /**
     * Clone a widget.
     *
     * @param widget - The source widget.
     *
     * @returns A new widget or `undefined`.
     *
     * #### Notes
     *  Uses the same widget factory and context as the source, or throws
     *  if the source widget is not managed by this manager.
     */
    cloneWidget(widget) {
        const context = widgetmanager_Private.contextProperty.get(widget);
        if (!context) {
            return undefined;
        }
        const factory = widgetmanager_Private.factoryProperty.get(widget);
        if (!factory) {
            return undefined;
        }
        const newWidget = factory.createNew(context, widget);
        this._initializeWidget(newWidget, factory, context);
        return newWidget;
    }
    /**
     * Close the widgets associated with a given context.
     *
     * @param context - The document context object.
     */
    closeWidgets(context) {
        const widgets = widgetmanager_Private.widgetsProperty.get(context);
        return Promise.all(widgets.map(widget => this.onClose(widget))).then(() => undefined);
    }
    /**
     * Dispose of the widgets associated with a given context
     * regardless of the widget's dirty state.
     *
     * @param context - The document context object.
     */
    deleteWidgets(context) {
        const widgets = widgetmanager_Private.widgetsProperty.get(context);
        return Promise.all(widgets.map(widget => this.onDelete(widget))).then(() => undefined);
    }
    /**
     * Filter a message sent to a message handler.
     *
     * @param handler - The target handler of the message.
     *
     * @param msg - The message dispatched to the handler.
     *
     * @returns `false` if the message should be filtered, of `true`
     *   if the message should be dispatched to the handler as normal.
     */
    messageHook(handler, msg) {
        switch (msg.type) {
            case 'close-request':
                void this.onClose(handler);
                return false;
            case 'activate-request': {
                const context = this.contextForWidget(handler);
                if (context) {
                    this._activateRequested.emit(context.path);
                }
                break;
            }
            default:
                break;
        }
        return true;
    }
    /**
     * Set the caption for widget title.
     *
     * @param widget - The target widget.
     */
    async setCaption(widget) {
        const trans = this.translator.load('jupyterlab');
        const context = widgetmanager_Private.contextProperty.get(widget);
        if (!context) {
            return;
        }
        const model = context.contentsModel;
        if (!model) {
            widget.title.caption = '';
            return;
        }
        return context
            .listCheckpoints()
            .then((checkpoints) => {
            if (widget.isDisposed) {
                return;
            }
            const last = checkpoints[checkpoints.length - 1];
            const checkpoint = last ? lib_index_js_.Time.format(last.last_modified) : 'None';
            let caption = trans.__('Name: %1\nPath: %2\n', model.name, model.path);
            if (context.model.readOnly) {
                caption += trans.__('Read-only');
            }
            else {
                caption +=
                    trans.__('Last Saved: %1\n', lib_index_js_.Time.format(model.last_modified)) +
                        trans.__('Last Checkpoint: %1', checkpoint);
            }
            widget.title.caption = caption;
        });
    }
    /**
     * Handle `'close-request'` messages.
     *
     * @param widget - The target widget.
     *
     * @returns A promise that resolves with whether the widget was closed.
     */
    async onClose(widget) {
        var _a;
        // Handle dirty state.
        const [shouldClose, ignoreSave] = await this._maybeClose(widget, this.translator);
        if (widget.isDisposed) {
            return true;
        }
        if (shouldClose) {
            if (!ignoreSave) {
                const context = widgetmanager_Private.contextProperty.get(widget);
                if (!context) {
                    return true;
                }
                if ((_a = context.contentsModel) === null || _a === void 0 ? void 0 : _a.writable) {
                    await context.save();
                }
                else {
                    await context.saveAs();
                }
            }
            if (widget.isDisposed) {
                return true;
            }
            widget.dispose();
        }
        return shouldClose;
    }
    /**
     * Dispose of widget regardless of widget's dirty state.
     *
     * @param widget - The target widget.
     */
    onDelete(widget) {
        widget.dispose();
        return Promise.resolve(void 0);
    }
    /**
     * Ask the user whether to close an unsaved file.
     */
    async _maybeClose(widget, translator) {
        var _a, _b;
        translator = translator || translation_lib_index_js_.nullTranslator;
        const trans = translator.load('jupyterlab');
        // Bail if the model is not dirty or other widgets are using the model.)
        const context = widgetmanager_Private.contextProperty.get(widget);
        if (!context) {
            return Promise.resolve([true, true]);
        }
        let widgets = widgetmanager_Private.widgetsProperty.get(context);
        if (!widgets) {
            return Promise.resolve([true, true]);
        }
        // Filter by whether the factories are read only.
        widgets = widgets.filter(widget => {
            const factory = widgetmanager_Private.factoryProperty.get(widget);
            if (!factory) {
                return false;
            }
            return factory.readOnly === false;
        });
        const fileName = widget.title.label;
        const factory = widgetmanager_Private.factoryProperty.get(widget);
        const isDirty = context.model.dirty &&
            widgets.length <= 1 &&
            !((_a = factory === null || factory === void 0 ? void 0 : factory.readOnly) !== null && _a !== void 0 ? _a : true);
        // Ask confirmation
        if (this.confirmClosingDocument) {
            const buttons = [
                index_js_.Dialog.cancelButton(),
                index_js_.Dialog.okButton({
                    label: isDirty ? trans.__('Close and save') : trans.__('Close'),
                    ariaLabel: isDirty
                        ? trans.__('Close and save Document')
                        : trans.__('Close Document')
                })
            ];
            if (isDirty) {
                buttons.splice(1, 0, index_js_.Dialog.warnButton({
                    label: trans.__('Close without saving'),
                    ariaLabel: trans.__('Close Document without saving')
                }));
            }
            const confirm = await (0,index_js_.showDialog)({
                title: trans.__('Confirmation'),
                body: trans.__('Please confirm you want to close "%1".', fileName),
                checkbox: isDirty
                    ? null
                    : {
                        label: trans.__('Do not ask me again.'),
                        caption: trans.__('If checked, no confirmation to close a document will be asked in the future.')
                    },
                buttons
            });
            if (confirm.isChecked) {
                this.confirmClosingDocument = false;
            }
            return Promise.resolve([
                confirm.button.accept,
                isDirty ? confirm.button.displayType === 'warn' : true
            ]);
        }
        else {
            if (!isDirty) {
                return Promise.resolve([true, true]);
            }
            const saveLabel = ((_b = context.contentsModel) === null || _b === void 0 ? void 0 : _b.writable)
                ? trans.__('Save')
                : trans.__('Save as');
            const result = await (0,index_js_.showDialog)({
                title: trans.__('Save your work'),
                body: trans.__('Save changes in "%1" before closing?', fileName),
                buttons: [
                    index_js_.Dialog.cancelButton(),
                    index_js_.Dialog.warnButton({
                        label: trans.__('Discard'),
                        ariaLabel: trans.__('Discard changes to file')
                    }),
                    index_js_.Dialog.okButton({ label: saveLabel })
                ]
            });
            return [result.button.accept, result.button.displayType === 'warn'];
        }
    }
    /**
     * Handle the disposal of a widget.
     */
    _widgetDisposed(widget) {
        const context = widgetmanager_Private.contextProperty.get(widget);
        if (!context) {
            return;
        }
        const widgets = widgetmanager_Private.widgetsProperty.get(context);
        if (!widgets) {
            return;
        }
        // Remove the widget.
        dist_index_es6_js_.ArrayExt.removeFirstOf(widgets, widget);
        // Dispose of the context if this is the last widget using it.
        if (!widgets.length) {
            context.dispose();
        }
    }
    /**
     * Handle the disposal of a widget.
     */
    _onWidgetDisposed(widget) {
        const disposables = widgetmanager_Private.disposablesProperty.get(widget);
        disposables.dispose();
    }
    /**
     * Handle a file changed signal for a context.
     */
    _onFileChanged(context) {
        const widgets = widgetmanager_Private.widgetsProperty.get(context);
        for (const widget of widgets) {
            void this.setCaption(widget);
        }
    }
    /**
     * Handle a path changed signal for a context.
     */
    _onPathChanged(context) {
        const widgets = widgetmanager_Private.widgetsProperty.get(context);
        for (const widget of widgets) {
            void this.setCaption(widget);
        }
    }
}
/**
 * A private namespace for DocumentManager data.
 */
var widgetmanager_Private;
(function (Private) {
    /**
     * A private attached property for a widget context.
     */
    Private.contextProperty = new properties_dist_index_es6_js_.AttachedProperty({
        name: 'context',
        create: () => undefined
    });
    /**
     * A private attached property for a widget factory.
     */
    Private.factoryProperty = new properties_dist_index_es6_js_.AttachedProperty({
        name: 'factory',
        create: () => undefined
    });
    /**
     * A private attached property for the widgets associated with a context.
     */
    Private.widgetsProperty = new properties_dist_index_es6_js_.AttachedProperty({
        name: 'widgets',
        create: () => []
    });
    /**
     * A private attached property for a widget's disposables.
     */
    Private.disposablesProperty = new properties_dist_index_es6_js_.AttachedProperty({
        name: 'disposables',
        create: () => new disposable_dist_index_es6_js_.DisposableSet()
    });
})(widgetmanager_Private || (widgetmanager_Private = {}));

;// CONCATENATED MODULE: ../packages/docmanager/lib/manager.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.










/**
 * The document manager.
 *
 * #### Notes
 * The document manager is used to register model and widget creators,
 * and the file browser uses the document manager to create widgets. The
 * document manager maintains a context for each path and model type that is
 * open, and a list of widgets for each context. The document manager is in
 * control of the proper closing and disposal of the widgets and contexts.
 */
class DocumentManager {
    /**
     * Construct a new document manager.
     */
    constructor(options) {
        var _a;
        this._activateRequested = new signaling_dist_index_es6_js_.Signal(this);
        this._contexts = [];
        this._isDisposed = false;
        this._autosave = true;
        this._autosaveInterval = 120;
        this._lastModifiedCheckMargin = 500;
        this._renameUntitledFileOnSave = true;
        this._stateChanged = new signaling_dist_index_es6_js_.Signal(this);
        this.translator = options.translator || translation_lib_index_js_.nullTranslator;
        this.registry = options.registry;
        this.services = options.manager;
        this._dialogs =
            (_a = options.sessionDialogs) !== null && _a !== void 0 ? _a : new index_js_.SessionContextDialogs({ translator: options.translator });
        this._isConnectedCallback = options.isConnectedCallback || (() => true);
        this._opener = options.opener;
        this._when = options.when || options.manager.ready;
        const widgetManager = new DocumentWidgetManager({
            registry: this.registry,
            translator: this.translator
        });
        widgetManager.activateRequested.connect(this._onActivateRequested, this);
        widgetManager.stateChanged.connect(this._onWidgetStateChanged, this);
        this._widgetManager = widgetManager;
        this._setBusy = options.setBusy;
    }
    /**
     * A signal emitted when one of the documents is activated.
     */
    get activateRequested() {
        return this._activateRequested;
    }
    /**
     * Whether to autosave documents.
     */
    get autosave() {
        return this._autosave;
    }
    set autosave(value) {
        if (this._autosave !== value) {
            const oldValue = this._autosave;
            this._autosave = value;
            // For each existing context, start/stop the autosave handler as needed.
            this._contexts.forEach(context => {
                const handler = manager_Private.saveHandlerProperty.get(context);
                if (!handler) {
                    return;
                }
                if (value === true && !handler.isActive) {
                    handler.start();
                }
                else if (value === false && handler.isActive) {
                    handler.stop();
                }
            });
            this._stateChanged.emit({
                name: 'autosave',
                oldValue,
                newValue: value
            });
        }
    }
    /**
     * Determines the time interval for autosave in seconds.
     */
    get autosaveInterval() {
        return this._autosaveInterval;
    }
    set autosaveInterval(value) {
        if (this._autosaveInterval !== value) {
            const oldValue = this._autosaveInterval;
            this._autosaveInterval = value;
            // For each existing context, set the save interval as needed.
            this._contexts.forEach(context => {
                const handler = manager_Private.saveHandlerProperty.get(context);
                if (!handler) {
                    return;
                }
                handler.saveInterval = value || 120;
            });
            this._stateChanged.emit({
                name: 'autosaveInterval',
                oldValue,
                newValue: value
            });
        }
    }
    /**
     * Whether to ask confirmation to close a tab or not.
     */
    get confirmClosingDocument() {
        return this._widgetManager.confirmClosingDocument;
    }
    set confirmClosingDocument(value) {
        if (this._widgetManager.confirmClosingDocument !== value) {
            const oldValue = this._widgetManager.confirmClosingDocument;
            this._widgetManager.confirmClosingDocument = value;
            this._stateChanged.emit({
                name: 'confirmClosingDocument',
                oldValue,
                newValue: value
            });
        }
    }
    /**
     * Defines max acceptable difference, in milliseconds, between last modified timestamps on disk and client
     */
    get lastModifiedCheckMargin() {
        return this._lastModifiedCheckMargin;
    }
    set lastModifiedCheckMargin(value) {
        if (this._lastModifiedCheckMargin !== value) {
            const oldValue = this._lastModifiedCheckMargin;
            this._lastModifiedCheckMargin = value;
            // For each existing context, update the margin value.
            this._contexts.forEach(context => {
                context.lastModifiedCheckMargin = value;
            });
            this._stateChanged.emit({
                name: 'lastModifiedCheckMargin',
                oldValue,
                newValue: value
            });
        }
    }
    /**
     * Whether to ask the user to rename untitled file on first manual save.
     */
    get renameUntitledFileOnSave() {
        return this._renameUntitledFileOnSave;
    }
    set renameUntitledFileOnSave(value) {
        if (this._renameUntitledFileOnSave !== value) {
            const oldValue = this._renameUntitledFileOnSave;
            this._renameUntitledFileOnSave = value;
            this._stateChanged.emit({
                name: 'renameUntitledFileOnSave',
                oldValue,
                newValue: value
            });
        }
    }
    /**
     * Signal triggered when an attribute changes.
     */
    get stateChanged() {
        return this._stateChanged;
    }
    /**
     * Get whether the document manager has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the document manager.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        // Clear any listeners for our signals.
        signaling_dist_index_es6_js_.Signal.clearData(this);
        // Close all the widgets for our contexts and dispose the widget manager.
        this._contexts.forEach(context => {
            return this._widgetManager.closeWidgets(context);
        });
        this._widgetManager.dispose();
        // Clear the context list.
        this._contexts.length = 0;
    }
    /**
     * Clone a widget.
     *
     * @param widget - The source widget.
     *
     * @returns A new widget or `undefined`.
     *
     * #### Notes
     *  Uses the same widget factory and context as the source, or returns
     *  `undefined` if the source widget is not managed by this manager.
     */
    cloneWidget(widget) {
        return this._widgetManager.cloneWidget(widget);
    }
    /**
     * Close all of the open documents.
     *
     * @returns A promise resolving when the widgets are closed.
     */
    closeAll() {
        return Promise.all(this._contexts.map(context => this._widgetManager.closeWidgets(context))).then(() => undefined);
    }
    /**
     * Close the widgets associated with a given path.
     *
     * @param path - The target path.
     *
     * @returns A promise resolving when the widgets are closed.
     */
    closeFile(path) {
        const close = this._contextsForPath(path).map(c => this._widgetManager.closeWidgets(c));
        return Promise.all(close).then(x => undefined);
    }
    /**
     * Get the document context for a widget.
     *
     * @param widget - The widget of interest.
     *
     * @returns The context associated with the widget, or `undefined` if no such
     * context exists.
     */
    contextForWidget(widget) {
        return this._widgetManager.contextForWidget(widget);
    }
    /**
     * Copy a file.
     *
     * @param fromFile - The full path of the original file.
     *
     * @param toDir - The full path to the target directory.
     *
     * @returns A promise which resolves to the contents of the file.
     */
    copy(fromFile, toDir) {
        return this.services.contents.copy(fromFile, toDir);
    }
    /**
     * Create a new file and return the widget used to view it.
     *
     * @param path - The file path to create.
     *
     * @param widgetName - The name of the widget factory to use. 'default' will use the default widget.
     *
     * @param kernel - An optional kernel name/id to override the default.
     *
     * @returns The created widget, or `undefined`.
     *
     * #### Notes
     * This function will return `undefined` if a valid widget factory
     * cannot be found.
     */
    createNew(path, widgetName = 'default', kernel) {
        return this._createOrOpenDocument('create', path, widgetName, kernel);
    }
    /**
     * Delete a file.
     *
     * @param path - The full path to the file to be deleted.
     *
     * @returns A promise which resolves when the file is deleted.
     *
     * #### Notes
     * If there is a running session associated with the file and no other
     * sessions are using the kernel, the session will be shut down.
     */
    deleteFile(path) {
        return this.services.sessions
            .stopIfNeeded(path)
            .then(() => {
            return this.services.contents.delete(path);
        })
            .then(() => {
            this._contextsForPath(path).forEach(context => this._widgetManager.deleteWidgets(context));
            return Promise.resolve(void 0);
        });
    }
    /**
     * Duplicate a file.
     *
     * @param path - The full path to the file to be duplicated.
     *
     * @returns A promise which resolves when the file is duplicated.
     */
    duplicate(path) {
        const basePath = lib_index_js_.PathExt.dirname(path);
        return this.services.contents.copy(path, basePath);
    }
    /**
     * See if a widget already exists for the given path and widget name.
     *
     * @param path - The file path to use.
     *
     * @param widgetName - The name of the widget factory to use. 'default' will use the default widget.
     *
     * @returns The found widget, or `undefined`.
     *
     * #### Notes
     * This can be used to find an existing widget instead of opening
     * a new widget.
     */
    findWidget(path, widgetName = 'default') {
        const newPath = lib_index_js_.PathExt.normalize(path);
        let widgetNames = [widgetName];
        if (widgetName === 'default') {
            const factory = this.registry.defaultWidgetFactory(newPath);
            if (!factory) {
                return undefined;
            }
            widgetNames = [factory.name];
        }
        else if (widgetName === null) {
            widgetNames = this.registry
                .preferredWidgetFactories(newPath)
                .map(f => f.name);
        }
        for (const context of this._contextsForPath(newPath)) {
            for (const widgetName of widgetNames) {
                if (widgetName !== null) {
                    const widget = this._widgetManager.findWidget(context, widgetName);
                    if (widget) {
                        return widget;
                    }
                }
            }
        }
        return undefined;
    }
    /**
     * Create a new untitled file.
     *
     * @param options - The file content creation options.
     */
    newUntitled(options) {
        if (options.type === 'file') {
            options.ext = options.ext || '.txt';
        }
        return this.services.contents.newUntitled(options);
    }
    /**
     * Open a file and return the widget used to view it.
     *
     * @param path - The file path to open.
     *
     * @param widgetName - The name of the widget factory to use. 'default' will use the default widget.
     *
     * @param kernel - An optional kernel name/id to override the default.
     *
     * @returns The created widget, or `undefined`.
     *
     * #### Notes
     * This function will return `undefined` if a valid widget factory
     * cannot be found.
     */
    open(path, widgetName = 'default', kernel, options) {
        return this._createOrOpenDocument('open', path, widgetName, kernel, options);
    }
    /**
     * Open a file and return the widget used to view it.
     * Reveals an already existing editor.
     *
     * @param path - The file path to open.
     *
     * @param widgetName - The name of the widget factory to use. 'default' will use the default widget.
     *
     * @param kernel - An optional kernel name/id to override the default.
     *
     * @returns The created widget, or `undefined`.
     *
     * #### Notes
     * This function will return `undefined` if a valid widget factory
     * cannot be found.
     */
    openOrReveal(path, widgetName = 'default', kernel, options) {
        const widget = this.findWidget(path, widgetName);
        if (widget) {
            this._opener.open(widget, {
                type: widgetName,
                ...options
            });
            return widget;
        }
        return this.open(path, widgetName, kernel, options !== null && options !== void 0 ? options : {});
    }
    /**
     * Overwrite a file.
     *
     * @param oldPath - The full path to the original file.
     *
     * @param newPath - The full path to the new file.
     *
     * @returns A promise containing the new file contents model.
     */
    overwrite(oldPath, newPath) {
        // Cleanly overwrite the file by moving it, making sure the original does
        // not exist, and then renaming to the new path.
        const tempPath = `${newPath}.${dist_index_js_.UUID.uuid4()}`;
        const cb = () => this.rename(tempPath, newPath);
        return this.rename(oldPath, tempPath)
            .then(() => {
            return this.deleteFile(newPath);
        })
            .then(cb, cb);
    }
    /**
     * Rename a file or directory.
     *
     * @param oldPath - The full path to the original file.
     *
     * @param newPath - The full path to the new file.
     *
     * @returns A promise containing the new file contents model.  The promise
     * will reject if the newPath already exists.  Use [[overwrite]] to overwrite
     * a file.
     */
    rename(oldPath, newPath) {
        return this.services.contents.rename(oldPath, newPath);
    }
    /**
     * Find a context for a given path and factory name.
     */
    _findContext(path, factoryName) {
        const normalizedPath = this.services.contents.normalize(path);
        return (0,dist_index_es6_js_.find)(this._contexts, context => {
            return (context.path === normalizedPath && context.factoryName === factoryName);
        });
    }
    /**
     * Get the contexts for a given path.
     *
     * #### Notes
     * There may be more than one context for a given path if the path is open
     * with multiple model factories (for example, a notebook can be open with a
     * notebook model factory and a text model factory).
     */
    _contextsForPath(path) {
        const normalizedPath = this.services.contents.normalize(path);
        return this._contexts.filter(context => context.path === normalizedPath);
    }
    /**
     * Create a context from a path and a model factory.
     */
    _createContext(path, factory, kernelPreference) {
        // TODO: Make it impossible to open two different contexts for the same
        // path. Or at least prompt the closing of all widgets associated with the
        // old context before opening the new context. This will make things much
        // more consistent for the users, at the cost of some confusion about what
        // models are and why sometimes they cannot open the same file in different
        // widgets that have different models.
        // Allow options to be passed when adding a sibling.
        const adopter = (widget, options) => {
            this._widgetManager.adoptWidget(context, widget);
            // TODO should we pass the type for layout customization
            this._opener.open(widget, options);
        };
        const context = new docregistry_lib_index_js_.Context({
            opener: adopter,
            manager: this.services,
            factory,
            path,
            kernelPreference,
            setBusy: this._setBusy,
            sessionDialogs: this._dialogs,
            lastModifiedCheckMargin: this._lastModifiedCheckMargin,
            translator: this.translator
        });
        const handler = new SaveHandler({
            context,
            isConnectedCallback: this._isConnectedCallback,
            saveInterval: this.autosaveInterval
        });
        manager_Private.saveHandlerProperty.set(context, handler);
        void context.ready.then(() => {
            if (this.autosave) {
                handler.start();
            }
        });
        context.disposed.connect(this._onContextDisposed, this);
        this._contexts.push(context);
        return context;
    }
    /**
     * Handle a context disposal.
     */
    _onContextDisposed(context) {
        dist_index_es6_js_.ArrayExt.removeFirstOf(this._contexts, context);
    }
    /**
     * Get the widget factory for a given widget name.
     */
    _widgetFactoryFor(path, widgetName) {
        const { registry } = this;
        if (widgetName === 'default') {
            const factory = registry.defaultWidgetFactory(path);
            if (!factory) {
                return undefined;
            }
            widgetName = factory.name;
        }
        return registry.getWidgetFactory(widgetName);
    }
    /**
     * Creates a new document, or loads one from disk, depending on the `which` argument.
     * If `which==='create'`, then it creates a new document. If `which==='open'`,
     * then it loads the document from disk.
     *
     * The two cases differ in how the document context is handled, but the creation
     * of the widget and launching of the kernel are identical.
     */
    _createOrOpenDocument(which, path, widgetName = 'default', kernel, options) {
        const widgetFactory = this._widgetFactoryFor(path, widgetName);
        if (!widgetFactory) {
            return undefined;
        }
        const modelName = widgetFactory.modelName || 'text';
        const factory = this.registry.getModelFactory(modelName);
        if (!factory) {
            return undefined;
        }
        // Handle the kernel preference.
        const preference = this.registry.getKernelPreference(path, widgetFactory.name, kernel);
        let context;
        let ready = Promise.resolve(undefined);
        // Handle the load-from-disk case
        if (which === 'open') {
            // Use an existing context if available.
            context = this._findContext(path, factory.name) || null;
            if (!context) {
                context = this._createContext(path, factory, preference);
                // Populate the model, either from disk or a
                // model backend.
                ready = this._when.then(() => context.initialize(false));
            }
        }
        else if (which === 'create') {
            context = this._createContext(path, factory, preference);
            // Immediately save the contents to disk.
            ready = this._when.then(() => context.initialize(true));
        }
        else {
            throw new Error(`Invalid argument 'which': ${which}`);
        }
        const widget = this._widgetManager.createWidget(widgetFactory, context);
        this._opener.open(widget, { type: widgetFactory.name, ...options });
        // If the initial opening of the context fails, dispose of the widget.
        ready.catch(err => {
            console.error(`Failed to initialize the context with '${factory.name}' for ${path}`, err);
            widget.close();
        });
        return widget;
    }
    /**
     * Handle an activateRequested signal from the widget manager.
     */
    _onActivateRequested(sender, args) {
        this._activateRequested.emit(args);
    }
    _onWidgetStateChanged(sender, args) {
        if (args.name === 'confirmClosingDocument') {
            this._stateChanged.emit(args);
        }
    }
}
/**
 * A namespace for private data.
 */
var manager_Private;
(function (Private) {
    /**
     * An attached property for a context save handler.
     */
    Private.saveHandlerProperty = new properties_dist_index_es6_js_.AttachedProperty({
        name: 'saveHandler',
        create: () => undefined
    });
})(manager_Private || (manager_Private = {}));

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/statusbar@~4.1.0-alpha.2 (singleton) (fallback: ../packages/statusbar/lib/index.js)
var statusbar_lib_index_js_ = __webpack_require__(34853);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
var react_index_js_default = /*#__PURE__*/__webpack_require__.n(react_index_js_);
;// CONCATENATED MODULE: ../packages/docmanager/lib/pathstatus.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * A pure component for rendering a file path (or activity name).
 *
 * @param props - the props for the component.
 *
 * @returns a tsx component for a file path.
 */
function PathStatusComponent(props) {
    return react_index_js_default().createElement(statusbar_lib_index_js_.TextItem, { source: props.name, title: props.fullPath });
}
/**
 * A status bar item for the current file path (or activity name).
 */
class PathStatus extends ui_components_lib_index_js_.VDomRenderer {
    /**
     * Construct a new PathStatus status item.
     */
    constructor(opts) {
        super(new PathStatus.Model(opts.docManager));
        this.node.title = this.model.path;
    }
    /**
     * Render the status item.
     */
    render() {
        return (react_index_js_default().createElement(PathStatusComponent, { fullPath: this.model.path, name: this.model.name }));
    }
}
/**
 * A namespace for PathStatus statics.
 */
(function (PathStatus) {
    /**
     * A VDomModel for rendering the PathStatus status item.
     */
    class Model extends ui_components_lib_index_js_.VDomModel {
        /**
         * Construct a new model.
         *
         * @param docManager: the application document manager. Used to check
         *   whether the current widget is a document.
         */
        constructor(docManager) {
            super();
            /**
             * React to a title change for the current widget.
             */
            this._onTitleChange = (title) => {
                const oldState = this._getAllState();
                this._name = title.label;
                this._triggerChange(oldState, this._getAllState());
            };
            /**
             * React to a path change for the current document.
             */
            this._onPathChange = (_documentModel, newPath) => {
                const oldState = this._getAllState();
                this._path = newPath;
                this._name = lib_index_js_.PathExt.basename(newPath);
                this._triggerChange(oldState, this._getAllState());
            };
            this._path = '';
            this._name = '';
            this._widget = null;
            this._docManager = docManager;
        }
        /**
         * The current path for the application.
         */
        get path() {
            return this._path;
        }
        /**
         * The name of the current activity.
         */
        get name() {
            return this._name;
        }
        /**
         * The current widget for the application.
         */
        get widget() {
            return this._widget;
        }
        set widget(widget) {
            const oldWidget = this._widget;
            if (oldWidget !== null) {
                const oldContext = this._docManager.contextForWidget(oldWidget);
                if (oldContext) {
                    oldContext.pathChanged.disconnect(this._onPathChange);
                }
                else {
                    oldWidget.title.changed.disconnect(this._onTitleChange);
                }
            }
            const oldState = this._getAllState();
            this._widget = widget;
            if (this._widget === null) {
                this._path = '';
                this._name = '';
            }
            else {
                const widgetContext = this._docManager.contextForWidget(this._widget);
                if (widgetContext) {
                    this._path = widgetContext.path;
                    this._name = lib_index_js_.PathExt.basename(widgetContext.path);
                    widgetContext.pathChanged.connect(this._onPathChange);
                }
                else {
                    this._path = '';
                    this._name = this._widget.title.label;
                    this._widget.title.changed.connect(this._onTitleChange);
                }
            }
            this._triggerChange(oldState, this._getAllState());
        }
        /**
         * Get the current state of the model.
         */
        _getAllState() {
            return [this._path, this._name];
        }
        /**
         * Trigger a state change to rerender.
         */
        _triggerChange(oldState, newState) {
            if (oldState[0] !== newState[0] || oldState[1] !== newState[1]) {
                this.stateChanged.emit(void 0);
            }
        }
    }
    PathStatus.Model = Model;
})(PathStatus || (PathStatus = {}));

;// CONCATENATED MODULE: ../packages/docmanager/lib/savingstatus.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * A pure functional component for a Saving status item.
 *
 * @param props - the props for the component.
 *
 * @returns a tsx component for rendering the saving state.
 */
function SavingStatusComponent(props) {
    return react_index_js_default().createElement(statusbar_lib_index_js_.TextItem, { source: props.fileStatus });
}
/**
 * The amount of time (in ms) to retain the saving completed message
 * before hiding the status item.
 */
const SAVING_COMPLETE_MESSAGE_MILLIS = 2000;
/**
 * A VDomRenderer for a saving status item.
 */
class SavingStatus extends ui_components_lib_index_js_.VDomRenderer {
    /**
     * Create a new SavingStatus item.
     */
    constructor(opts) {
        super(new SavingStatus.Model(opts.docManager));
        const translator = opts.translator || translation_lib_index_js_.nullTranslator;
        const trans = translator.load('jupyterlab');
        this._statusMap = {
            completed: trans.__('Saving completed'),
            started: trans.__('Saving started'),
            failed: trans.__('Saving failed')
        };
    }
    /**
     * Render the SavingStatus item.
     */
    render() {
        if (this.model === null || this.model.status === null) {
            return null;
        }
        else {
            return (react_index_js_default().createElement(SavingStatusComponent, { fileStatus: this._statusMap[this.model.status] }));
        }
    }
}
/**
 * A namespace for SavingStatus statics.
 */
(function (SavingStatus) {
    /**
     * A VDomModel for the SavingStatus item.
     */
    class Model extends ui_components_lib_index_js_.VDomModel {
        /**
         * Create a new SavingStatus model.
         */
        constructor(docManager) {
            super();
            /**
             * React to a saving status change from the current document widget.
             */
            this._onStatusChange = (_, newStatus) => {
                this._status = newStatus;
                if (this._status === 'completed') {
                    setTimeout(() => {
                        this._status = null;
                        this.stateChanged.emit(void 0);
                    }, SAVING_COMPLETE_MESSAGE_MILLIS);
                    this.stateChanged.emit(void 0);
                }
                else {
                    this.stateChanged.emit(void 0);
                }
            };
            this._status = null;
            this._widget = null;
            this._status = null;
            this.widget = null;
            this._docManager = docManager;
        }
        /**
         * The current status of the model.
         */
        get status() {
            return this._status;
        }
        /**
         * The current widget for the model. Any widget can be assigned,
         * but it only has any effect if the widget is an IDocument widget
         * known to the application document manager.
         */
        get widget() {
            return this._widget;
        }
        set widget(widget) {
            var _a, _b;
            const oldWidget = this._widget;
            if (oldWidget !== null) {
                const oldContext = this._docManager.contextForWidget(oldWidget);
                if (oldContext) {
                    oldContext.saveState.disconnect(this._onStatusChange);
                }
                else if ((_a = this._widget.content) === null || _a === void 0 ? void 0 : _a.saveStateChanged) {
                    this._widget.content.saveStateChanged.disconnect(this._onStatusChange);
                }
            }
            this._widget = widget;
            if (this._widget === null) {
                this._status = null;
            }
            else {
                const widgetContext = this._docManager.contextForWidget(this._widget);
                if (widgetContext) {
                    widgetContext.saveState.connect(this._onStatusChange);
                }
                else if ((_b = this._widget.content) === null || _b === void 0 ? void 0 : _b.saveStateChanged) {
                    this._widget.content.saveStateChanged.connect(this._onStatusChange);
                }
            }
        }
    }
    SavingStatus.Model = Model;
})(SavingStatus || (SavingStatus = {}));

;// CONCATENATED MODULE: ../packages/docmanager/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The document registry token.
 */
const IDocumentManager = new dist_index_js_.Token('@jupyterlab/docmanager:IDocumentManager', `A service for the manager for all
  documents used by the application. Use this if you want to open and close documents,
  create and delete files, and otherwise interact with the file system.`);
/**
 * The document widget opener token.
 */
const IDocumentWidgetOpener = new dist_index_js_.Token('@jupyterlab/docmanager:IDocumentWidgetOpener', `A service to open a widget.`);

;// CONCATENATED MODULE: ../packages/docmanager/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module docmanager
 */









/***/ })

}]);
//# sourceMappingURL=1036.afe3c626924dff86b08d.js.map?v=afe3c626924dff86b08d