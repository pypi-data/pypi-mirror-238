"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[9139],{

/***/ 69139:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "CodeExtractorsManager": () => (/* reexport */ CodeExtractorsManager),
  "DefaultMap": () => (/* reexport */ DefaultMap),
  "DocumentConnectionManager": () => (/* reexport */ DocumentConnectionManager),
  "EditorAdapter": () => (/* reexport */ EditorAdapter),
  "FeatureManager": () => (/* reexport */ FeatureManager),
  "ILSPCodeExtractorsManager": () => (/* reexport */ ILSPCodeExtractorsManager),
  "ILSPDocumentConnectionManager": () => (/* reexport */ ILSPDocumentConnectionManager),
  "ILSPFeatureManager": () => (/* reexport */ ILSPFeatureManager),
  "ILanguageServerManager": () => (/* reexport */ ILanguageServerManager),
  "IWidgetLSPAdapterTracker": () => (/* reexport */ IWidgetLSPAdapterTracker),
  "LanguageServerManager": () => (/* reexport */ LanguageServerManager),
  "Method": () => (/* reexport */ Method),
  "ProtocolCoordinates": () => (/* reexport */ ProtocolCoordinates),
  "TextForeignCodeExtractor": () => (/* reexport */ TextForeignCodeExtractor),
  "UpdateManager": () => (/* reexport */ UpdateManager),
  "VirtualDocument": () => (/* reexport */ VirtualDocument),
  "VirtualDocumentInfo": () => (/* reexport */ VirtualDocumentInfo),
  "WidgetLSPAdapter": () => (/* reexport */ WidgetLSPAdapter),
  "WidgetLSPAdapterTracker": () => (/* reexport */ WidgetLSPAdapterTracker),
  "collectDocuments": () => (/* reexport */ collectDocuments),
  "expandDottedPaths": () => (/* reexport */ expandDottedPaths),
  "expandPath": () => (/* reexport */ expandPath),
  "isEqual": () => (/* reexport */ isEqual),
  "isWithinRange": () => (/* reexport */ isWithinRange),
  "offsetAtPosition": () => (/* reexport */ offsetAtPosition),
  "positionAtOffset": () => (/* reexport */ positionAtOffset),
  "sleep": () => (/* reexport */ sleep),
  "untilReady": () => (/* reexport */ untilReady)
});

// EXTERNAL MODULE: ../node_modules/lodash.mergewith/index.js
var lodash_mergewith = __webpack_require__(95282);
var lodash_mergewith_default = /*#__PURE__*/__webpack_require__.n(lodash_mergewith);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(30205);
;// CONCATENATED MODULE: ../packages/lsp/lib/adapters/editorAdapter.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The CodeEditor.IEditor adapter.
 */
class EditorAdapter {
    /**
     * Instantiate a new EditorAdapter.
     *
     * @param options The instantiation options for a EditorAdapter.
     */
    constructor(options) {
        this._widgetAdapter = options.widgetAdapter;
        this._extensions = options.extensions;
        void options.editor.ready().then(editor => {
            this._injectExtensions(options.editor);
        });
    }
    /**
     * Dispose the handler.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.isDisposed = true;
        index_es6_js_.Signal.clearData(this);
    }
    /**
     * Setup the editor.
     */
    _injectExtensions(editor) {
        const codeEditor = editor.getEditor();
        if (codeEditor.isDisposed) {
            return;
        }
        this._extensions.forEach(factory => {
            const ext = factory.factory({
                path: this._widgetAdapter.widget.context.path,
                editor: editor,
                widgetAdapter: this._widgetAdapter,
                model: codeEditor.model,
                inline: true
            });
            if (!ext) {
                return;
            }
            codeEditor.injectExtension(ext.instance(codeEditor));
        });
    }
}

;// CONCATENATED MODULE: ../packages/lsp/lib/adapters/adapter.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





const createButton = index_js_.Dialog.createButton;
/**
 * The values should follow the https://microsoft.github.io/language-server-protocol/specification guidelines
 */
const MIME_TYPE_LANGUAGE_MAP = {
    'text/x-rsrc': 'r',
    'text/x-r-source': 'r',
    // currently there are no LSP servers for IPython we are aware of
    'text/x-ipython': 'python'
};
/**
 * Foreign code: low level adapter is not aware of the presence of foreign languages;
 * it operates on the virtual document and must not attempt to infer the language dependencies
 * as this would make the logic of inspections caching impossible to maintain, thus the WidgetAdapter
 * has to handle that, keeping multiple connections and multiple virtual documents.
 */
class WidgetLSPAdapter {
    // note: it could be using namespace/IOptions pattern,
    // but I do not know how to make it work with the generic type T
    // (other than using 'any' in the IOptions interface)
    constructor(widget, options) {
        this.widget = widget;
        this.options = options;
        /**
         * Signal emitted when the adapter is connected.
         */
        this._adapterConnected = new index_es6_js_.Signal(this);
        /**
         * Signal emitted when the active editor have changed.
         */
        this._activeEditorChanged = new index_es6_js_.Signal(this);
        /**
         * Signal emitted when an editor is changed.
         */
        this._editorAdded = new index_es6_js_.Signal(this);
        /**
         * Signal emitted when an editor is removed.
         */
        this._editorRemoved = new index_es6_js_.Signal(this);
        /**
         * Signal emitted when the adapter is disposed.
         */
        this._disposed = new index_es6_js_.Signal(this);
        this._isDisposed = false;
        this._virtualDocument = null;
        this._connectionManager = options.connectionManager;
        this._isConnected = false;
        this._trans = (options.translator || lib_index_js_.nullTranslator).load('jupyterlab');
        // set up signal connections
        this.widget.context.saveState.connect(this.onSaveState, this);
        this.connectionManager.closed.connect(this.onConnectionClosed, this);
        this.widget.disposed.connect(this.dispose, this);
        this._editorToAdapter = new WeakMap();
        this.editorAdded.connect(this._onEditorAdded, this);
        this.editorRemoved.connect(this._onEditorRemoved, this);
        this._connectionManager.languageServerManager.sessionsChanged.connect(this._onLspSessionOrFeatureChanged, this);
        this.options.featureManager.featureRegistered.connect(this._onLspSessionOrFeatureChanged, this);
    }
    /**
     * Check if the adapter is disposed
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Check if the document contains multiple editors
     */
    get hasMultipleEditors() {
        return this.editors.length > 1;
    }
    /**
     * Get the ID of the internal widget.
     */
    get widgetId() {
        return this.widget.id;
    }
    /**
     * Get the language identifier of the document
     */
    get language() {
        // the values should follow https://microsoft.github.io/language-server-protocol/specification guidelines,
        // see the table in https://microsoft.github.io/language-server-protocol/specification#textDocumentItem
        if (MIME_TYPE_LANGUAGE_MAP.hasOwnProperty(this.mimeType)) {
            return MIME_TYPE_LANGUAGE_MAP[this.mimeType];
        }
        else {
            let withoutParameters = this.mimeType.split(';')[0];
            let [type, subtype] = withoutParameters.split('/');
            if (type === 'application' || type === 'text') {
                if (subtype.startsWith('x-')) {
                    return subtype.substring(2);
                }
                else {
                    return subtype;
                }
            }
            else {
                return this.mimeType;
            }
        }
    }
    /**
     * Signal emitted when the adapter is connected.
     */
    get adapterConnected() {
        return this._adapterConnected;
    }
    /**
     * Signal emitted when the active editor have changed.
     */
    get activeEditorChanged() {
        return this._activeEditorChanged;
    }
    /**
     * Signal emitted when the adapter is disposed.
     */
    get disposed() {
        return this._disposed;
    }
    /**
     * Signal emitted when the an editor is changed.
     */
    get editorAdded() {
        return this._editorAdded;
    }
    /**
     * Signal emitted when the an editor is removed.
     */
    get editorRemoved() {
        return this._editorRemoved;
    }
    /**
     * The virtual document is connected or not
     */
    get isConnected() {
        return this._isConnected;
    }
    /**
     * The LSP document and connection manager instance.
     */
    get connectionManager() {
        return this._connectionManager;
    }
    /**
     * The translator provider.
     */
    get trans() {
        return this._trans;
    }
    /**
     * Promise that resolves once the document is updated
     */
    get updateFinished() {
        return this._updateFinished;
    }
    /**
     * Internal virtual document of the adapter.
     */
    get virtualDocument() {
        return this._virtualDocument;
    }
    /**
     * Callback on connection closed event.
     */
    onConnectionClosed(_, { virtualDocument }) {
        if (virtualDocument === this.virtualDocument) {
            this.dispose();
        }
    }
    /**
     * Dispose the adapter.
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this.editorAdded.disconnect(this._onEditorAdded, this);
        this.editorRemoved.disconnect(this._onEditorRemoved, this);
        this._connectionManager.languageServerManager.sessionsChanged.disconnect(this._onLspSessionOrFeatureChanged, this);
        this.options.featureManager.featureRegistered.disconnect(this._onLspSessionOrFeatureChanged, this);
        this._isDisposed = true;
        this.disconnect();
        this._virtualDocument = null;
        this._disposed.emit();
        index_es6_js_.Signal.clearData(this);
    }
    /**
     * Disconnect virtual document from the language server.
     */
    disconnect() {
        var _a, _b;
        const uri = (_a = this.virtualDocument) === null || _a === void 0 ? void 0 : _a.uri;
        const { model } = this.widget.context;
        if (uri) {
            this.connectionManager.unregisterDocument(uri);
        }
        model.contentChanged.disconnect(this._onContentChanged, this);
        // pretend that all editors were removed to trigger the disconnection of even handlers
        // they will be connected again on new connection
        for (let { ceEditor: editor } of this.editors) {
            this._editorRemoved.emit({
                editor: editor
            });
        }
        (_b = this.virtualDocument) === null || _b === void 0 ? void 0 : _b.dispose();
    }
    /**
     * Update the virtual document.
     */
    updateDocuments() {
        if (this._isDisposed) {
            console.warn('Cannot update documents: adapter disposed');
            return Promise.reject('Cannot update documents: adapter disposed');
        }
        return this.virtualDocument.updateManager.updateDocuments(this.editors);
    }
    /**
     * Callback called on the document changed event.
     */
    documentChanged(virtualDocument, document, isInit = false) {
        if (this._isDisposed) {
            console.warn('Cannot swap document: adapter disposed');
            return;
        }
        // TODO only send the difference, using connection.sendSelectiveChange()
        let connection = this.connectionManager.connections.get(virtualDocument.uri);
        if (!(connection === null || connection === void 0 ? void 0 : connection.isReady)) {
            console.log('Skipping document update signal: connection not ready');
            return;
        }
        connection.sendFullTextChange(virtualDocument.value, virtualDocument.documentInfo);
    }
    // equivalent to triggering didClose and didOpen, as per syncing specification,
    // but also reloads the connection; used during file rename (or when it was moved)
    reloadConnection() {
        // ignore premature calls (before the editor was initialized)
        if (this.virtualDocument === null) {
            return;
        }
        // disconnect all existing connections (and dispose adapters)
        this.disconnect();
        // recreate virtual document using current path and language
        // as virtual editor assumes it gets the virtual document at init,
        // just dispose virtual editor (which disposes virtual document too)
        // and re-initialize both virtual editor and document
        this.initVirtual();
        // reconnect
        this.connectDocument(this.virtualDocument, true).catch(console.warn);
    }
    /**
     * Callback on document saved event.
     */
    onSaveState(context, state) {
        // ignore premature calls (before the editor was initialized)
        if (this.virtualDocument === null) {
            return;
        }
        if (state === 'completed') {
            // note: must only be send to the appropriate connections as
            // some servers (Julia) break if they receive save notification
            // for a document that was not opened before, see:
            // https://github.com/jupyter-lsp/jupyterlab-lsp/issues/490
            const documentsToSave = [this.virtualDocument];
            for (let virtualDocument of documentsToSave) {
                let connection = this.connectionManager.connections.get(virtualDocument.uri);
                if (!connection) {
                    continue;
                }
                connection.sendSaved(virtualDocument.documentInfo);
                for (let foreign of virtualDocument.foreignDocuments.values()) {
                    documentsToSave.push(foreign);
                }
            }
        }
    }
    /**
     * Connect the virtual document with the language server.
     */
    async onConnected(data) {
        let { virtualDocument } = data;
        this._adapterConnected.emit(data);
        this._isConnected = true;
        try {
            await this.updateDocuments();
        }
        catch (reason) {
            console.warn('Could not update documents', reason);
            return;
        }
        // refresh the document on the LSP server
        this.documentChanged(virtualDocument, virtualDocument, true);
        data.connection.serverNotifications['$/logTrace'].connect((connection, message) => {
            console.log(data.connection.serverIdentifier, 'trace', virtualDocument.uri, message);
        });
        data.connection.serverNotifications['window/logMessage'].connect((connection, message) => {
            console.log(connection.serverIdentifier + ': ' + message.message);
        });
        data.connection.serverNotifications['window/showMessage'].connect((connection, message) => {
            void (0,index_js_.showDialog)({
                title: this.trans.__('Message from ') + connection.serverIdentifier,
                body: message.message
            });
        });
        data.connection.serverRequests['window/showMessageRequest'].setHandler(async (params) => {
            const actionItems = params.actions;
            const buttons = actionItems
                ? actionItems.map(action => {
                    return createButton({
                        label: action.title
                    });
                })
                : [createButton({ label: this.trans.__('Dismiss') })];
            const result = await (0,index_js_.showDialog)({
                title: this.trans.__('Message from ') + data.connection.serverIdentifier,
                body: params.message,
                buttons: buttons
            });
            const choice = buttons.indexOf(result.button);
            if (choice === -1) {
                return null;
            }
            if (actionItems) {
                return actionItems[choice];
            }
            return null;
        });
    }
    /**
     * Opens a connection for the document. The connection may or may
     * not be initialized, yet, and depending on when this is called, the client
     * may not be fully connected.
     *
     * @param virtualDocument a VirtualDocument
     * @param sendOpen whether to open the document immediately
     */
    async connectDocument(virtualDocument, sendOpen = false) {
        virtualDocument.foreignDocumentOpened.connect(this.onForeignDocumentOpened, this);
        const connectionContext = await this._connect(virtualDocument).catch(console.error);
        if (connectionContext && connectionContext.connection) {
            virtualDocument.changed.connect(this.documentChanged, this);
            if (sendOpen) {
                connectionContext.connection.sendOpenWhenReady(virtualDocument.documentInfo);
            }
        }
    }
    /**
     * Create the virtual document using current path and language.
     */
    initVirtual() {
        var _a;
        (_a = this._virtualDocument) === null || _a === void 0 ? void 0 : _a.dispose();
        this._virtualDocument = this.createVirtualDocument();
        this._onLspSessionOrFeatureChanged();
    }
    /**
     * Handler for opening a document contained in a parent document. The assumption
     * is that the editor already exists for this, and as such the document
     * should be queued for immediate opening.
     *
     * @param host the VirtualDocument that contains the VirtualDocument in another language
     * @param context information about the foreign VirtualDocument
     */
    async onForeignDocumentOpened(_, context) {
        const { foreignDocument } = context;
        await this.connectDocument(foreignDocument, true);
        foreignDocument.foreignDocumentClosed.connect(this._onForeignDocumentClosed, this);
    }
    _onEditorAdded(sender, change) {
        const { editor } = change;
        const editorAdapter = new EditorAdapter({
            editor: editor,
            widgetAdapter: this,
            extensions: this.options.featureManager.extensionFactories()
        });
        this._editorToAdapter.set(editor, editorAdapter);
    }
    _onEditorRemoved(sender, change) {
        const { editor } = change;
        const adapter = this._editorToAdapter.get(editor);
        adapter === null || adapter === void 0 ? void 0 : adapter.dispose();
        this._editorToAdapter.delete(editor);
    }
    /**
     * Callback called when a foreign document is closed,
     * the associated signals with this virtual document
     * are disconnected.
     */
    _onForeignDocumentClosed(_, context) {
        const { foreignDocument } = context;
        foreignDocument.foreignDocumentClosed.disconnect(this._onForeignDocumentClosed, this);
        foreignDocument.foreignDocumentOpened.disconnect(this.onForeignDocumentOpened, this);
        foreignDocument.changed.disconnect(this.documentChanged, this);
    }
    /**
     * Detect the capabilities for the document type then
     * open the websocket connection with the language server.
     */
    async _connect(virtualDocument) {
        let language = virtualDocument.language;
        let capabilities = {
            textDocument: {
                synchronization: {
                    dynamicRegistration: true,
                    willSave: false,
                    didSave: true,
                    willSaveWaitUntil: false
                }
            },
            workspace: {
                didChangeConfiguration: {
                    dynamicRegistration: true
                }
            }
        };
        capabilities = lodash_mergewith_default()(capabilities, this.options.featureManager.clientCapabilities());
        let options = {
            capabilities,
            virtualDocument,
            language,
            hasLspSupportedFile: virtualDocument.hasLspSupportedFile
        };
        let connection = await this.connectionManager.connect(options);
        if (connection) {
            await this.onConnected({ virtualDocument, connection });
            return {
                connection,
                virtualDocument
            };
        }
        else {
            return undefined;
        }
    }
    /**
     * Handle content changes and update all virtual documents after a change.
     *
     * #### Notes
     * Update to the state of a notebook may be done without a notice on the
     * CodeMirror level, e.g. when a cell is deleted. Therefore a
     * JupyterLab-specific signal is watched instead.
     *
     * While by not using the change event of CodeMirror editors we lose an easy
     * way to send selective (range) updates this can be still implemented by
     * comparison of before/after states of the virtual documents, which is
     * more resilient and editor-independent.
     */
    async _onContentChanged(_) {
        // Update the virtual documents.
        // Sending the updates to LSP is out of scope here.
        const promise = this.updateDocuments();
        if (!promise) {
            console.warn('Could not update documents');
            return;
        }
        this._updateFinished = promise.catch(console.warn);
        await this.updateFinished;
    }
    /**
     * Check if the virtual document should be updated on content
     * changed signal. Returns `true` if two following conditions are
     * are satisfied:
     *  - The LSP feature is enabled.
     *  - The LSP features list is not empty.
     */
    _shouldUpdateVirtualDocument() {
        const { languageServerManager } = this.connectionManager;
        return (languageServerManager.isEnabled &&
            this.options.featureManager.features.length > 0);
    }
    /**
     * Connect the virtual document update handler with the content
     * updated signal.This method is invoked at startup and when
     * the LSP server status changed or when a LSP feature is registered.
     */
    _onLspSessionOrFeatureChanged() {
        if (!this._virtualDocument) {
            return;
        }
        const { model } = this.widget.context;
        if (this._shouldUpdateVirtualDocument()) {
            model.contentChanged.connect(this._onContentChanged, this);
        }
        else {
            model.contentChanged.disconnect(this._onContentChanged, this);
        }
    }
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/docregistry@~4.1.0-alpha.2 (strict) (fallback: ../packages/docregistry/lib/index.js)
var docregistry_lib_index_js_ = __webpack_require__(16564);
;// CONCATENATED MODULE: ../packages/lsp/lib/adapters/tracker.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * A class that keeps track of widget adapter instances.
 *
 * @typeparam T - The type of widget being tracked. Defaults to `WidgetLSPAdapter`.
 */
class WidgetLSPAdapterTracker {
    /**
     * Create a new widget tracker.
     *
     * @param options - The instantiation options for a widget tracker.
     */
    constructor(options) {
        this._isDisposed = false;
        this._current = null;
        this._adapters = new Set();
        this._adapterAdded = new index_es6_js_.Signal(this);
        this._adapterUpdated = new index_es6_js_.Signal(this);
        this._currentChanged = new index_es6_js_.Signal(this);
        const shell = (this._shell = options.shell);
        shell.currentChanged.connect((_, args) => {
            let newValue = args.newValue;
            if (!newValue || !(newValue instanceof docregistry_lib_index_js_.DocumentWidget)) {
                console.log('No current widget');
                return;
            }
            const adapter = this.find(value => value.widget === newValue);
            if (!adapter) {
                return;
            }
            this._current = adapter;
            this._currentChanged.emit(adapter);
        });
    }
    /**
     * A signal emitted when the current adapter changes.
     */
    get currentChanged() {
        return this._currentChanged;
    }
    /**
     * The current adapter is the most recently focused or added adapter.
     *
     * #### Notes
     * It is the most recently focused adapter, or the most recently added
     * adapter if no adapter has taken focus.
     */
    get currentAdapter() {
        return this._current;
    }
    /**
     * The number of adapter held by the tracker.
     */
    get size() {
        return this._adapters.size;
    }
    /**
     * A signal emitted when an adapter is added.
     */
    get adapterAdded() {
        return this._adapterAdded;
    }
    /**
     * A signal emitted when an adapter is updated.
     */
    get adapterUpdated() {
        return this._adapterUpdated;
    }
    /**
     * Add a new adapter to the tracker.
     *
     * @param adapter - The adapter being added.
     *
     * #### Notes.
     * The newly added adapter becomes the current adapter unless the shell
     * already had a DocumentWidget as the activeWidget.
     */
    add(adapter) {
        if (adapter.isDisposed) {
            const warning = 'A disposed object cannot be added.';
            console.warn(warning, adapter);
            throw new Error(warning);
        }
        if (this._adapters.has(adapter)) {
            const warning = 'This object already exists in the pool.';
            console.warn(warning, adapter);
            throw new Error(warning);
        }
        this._adapters.add(adapter);
        this._adapterAdded.emit(adapter);
        adapter.disposed.connect(() => {
            this._adapters.delete(adapter);
            if (adapter === this._current) {
                this._current = null;
                this._currentChanged.emit(this._current);
            }
        }, this);
        // Only update the current adapter, when there is no shell.activeWidget
        // or the active widget is not a DocumentWidget
        // We will be able to use other panels while keeping the current adapter.
        const active = this._shell.activeWidget;
        if (!active || !(active instanceof docregistry_lib_index_js_.DocumentWidget)) {
            this._current = adapter;
            this._currentChanged.emit(adapter);
        }
    }
    /**
     * Test whether the tracker is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the tracker.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._adapters.clear();
        index_es6_js_.Signal.clearData(this);
    }
    /**
     * Find the first adapter in the tracker that satisfies a filter function.
     *
     * @param - fn The filter function to call on each adapter.
     *
     * #### Notes
     * If no adapter is found, the value returned is `undefined`.
     */
    find(fn) {
        const values = this._adapters.values();
        for (const value of values) {
            if (fn(value)) {
                return value;
            }
        }
        return undefined;
    }
    /**
     * Iterate through each adapter in the tracker.
     *
     * @param fn - The function to call on each adapter.
     */
    forEach(fn) {
        this._adapters.forEach(fn);
    }
    /**
     * Filter the adapter in the tracker based on a predicate.
     *
     * @param fn - The function by which to filter.
     */
    filter(fn) {
        const filtered = [];
        this.forEach(value => {
            if (fn(value)) {
                filtered.push(value);
            }
        });
        return filtered;
    }
    /**
     * Check if this tracker has the specified adapter.
     *
     * @param adapter - The adapter whose existence is being checked.
     */
    has(adapter) {
        return this._adapters.has(adapter);
    }
}

;// CONCATENATED MODULE: ../packages/lsp/lib/adapters/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var coreutils_lib_index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
;// CONCATENATED MODULE: ../packages/lsp/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

var ILanguageServerManager;
(function (ILanguageServerManager) {
    /**
     * LSP endpoint prefix.
     */
    ILanguageServerManager.URL_NS = 'lsp';
})(ILanguageServerManager || (ILanguageServerManager = {}));
/**
 * @alpha
 *
 * The virtual documents and language server connections manager
 * Require this token in your extension to access the associated virtual
 * document and LS connection of opened documents.
 *
 */
const ILSPDocumentConnectionManager = new dist_index_js_.Token('@jupyterlab/lsp:ILSPDocumentConnectionManager', 'Provides the virtual documents and language server connections service.');
/**
 * @alpha
 *
 * The language server feature manager. Require this token in your extension
 * to register the client capabilities implemented by your extension.
 *
 */
const ILSPFeatureManager = new dist_index_js_.Token('@jupyterlab/lsp:ILSPFeatureManager', 'Provides the language server feature manager. This token is required to register new client capabilities.');
/**
 * @alpha
 *
 * The code extractor manager. Require this token in your extension to
 * register new code extractors. Code extractor allows creating multiple
 * virtual documents from an opened document.
 *
 */
const ILSPCodeExtractorsManager = new dist_index_js_.Token('@jupyterlab/lsp:ILSPCodeExtractorsManager', 'Provides the code extractor manager. This token is required in your extension to register code extractor allowing the creation of multiple virtual document from an opened document.');
/**
 * @alpha
 *
 * The WidgetLSPAdapter tracker. Require this token in your extension to
 * track WidgetLSPAdapters.
 *
 */
const IWidgetLSPAdapterTracker = new dist_index_js_.Token('@jupyterlab/lsp:IWidgetLSPAdapterTracker', 'Provides the WidgetLSPAdapter tracker. This token is required in your extension to track WidgetLSPAdapters.');
/**
 * Method strings are reproduced here because a non-typing import of
 * `vscode-languageserver-protocol` is ridiculously expensive.
 */
var Method;
(function (Method) {
    /** Server notifications */
    let ServerNotification;
    (function (ServerNotification) {
        ServerNotification["PUBLISH_DIAGNOSTICS"] = "textDocument/publishDiagnostics";
        ServerNotification["SHOW_MESSAGE"] = "window/showMessage";
        ServerNotification["LOG_TRACE"] = "$/logTrace";
        ServerNotification["LOG_MESSAGE"] = "window/logMessage";
    })(ServerNotification = Method.ServerNotification || (Method.ServerNotification = {}));
    /** Client notifications */
    let ClientNotification;
    (function (ClientNotification) {
        ClientNotification["DID_CHANGE"] = "textDocument/didChange";
        ClientNotification["DID_CHANGE_CONFIGURATION"] = "workspace/didChangeConfiguration";
        ClientNotification["DID_OPEN"] = "textDocument/didOpen";
        ClientNotification["DID_SAVE"] = "textDocument/didSave";
        ClientNotification["INITIALIZED"] = "initialized";
        ClientNotification["SET_TRACE"] = "$/setTrace";
    })(ClientNotification = Method.ClientNotification || (Method.ClientNotification = {}));
    /** Server requests */
    let ServerRequest;
    (function (ServerRequest) {
        ServerRequest["REGISTER_CAPABILITY"] = "client/registerCapability";
        ServerRequest["SHOW_MESSAGE_REQUEST"] = "window/showMessageRequest";
        ServerRequest["UNREGISTER_CAPABILITY"] = "client/unregisterCapability";
        ServerRequest["WORKSPACE_CONFIGURATION"] = "workspace/configuration";
    })(ServerRequest = Method.ServerRequest || (Method.ServerRequest = {}));
    /** Client requests */
    let ClientRequest;
    (function (ClientRequest) {
        ClientRequest["CODE_ACTION"] = "textDocument/codeAction";
        ClientRequest["COMPLETION"] = "textDocument/completion";
        ClientRequest["COMPLETION_ITEM_RESOLVE"] = "completionItem/resolve";
        ClientRequest["DEFINITION"] = "textDocument/definition";
        ClientRequest["DOCUMENT_COLOR"] = "textDocument/documentColor";
        ClientRequest["DOCUMENT_HIGHLIGHT"] = "textDocument/documentHighlight";
        ClientRequest["DOCUMENT_SYMBOL"] = "textDocument/documentSymbol";
        ClientRequest["HOVER"] = "textDocument/hover";
        ClientRequest["IMPLEMENTATION"] = "textDocument/implementation";
        ClientRequest["INITIALIZE"] = "initialize";
        ClientRequest["REFERENCES"] = "textDocument/references";
        ClientRequest["RENAME"] = "textDocument/rename";
        ClientRequest["SIGNATURE_HELP"] = "textDocument/signatureHelp";
        ClientRequest["TYPE_DEFINITION"] = "textDocument/typeDefinition";
        ClientRequest["LINKED_EDITING_RANGE"] = "textDocument/linkedEditingRange";
        ClientRequest["INLINE_VALUE"] = "textDocument/inlineValue";
        ClientRequest["INLAY_HINT"] = "textDocument/inlayHint";
        ClientRequest["WORKSPACE_SYMBOL"] = "workspace/symbol";
        ClientRequest["WORKSPACE_SYMBOL_RESOLVE"] = "workspaceSymbol/resolve";
        ClientRequest["FORMATTING"] = "textDocument/formatting";
        ClientRequest["RANGE_FORMATTING"] = "textDocument/rangeFormatting";
    })(ClientRequest = Method.ClientRequest || (Method.ClientRequest = {}));
})(Method || (Method = {}));

;// CONCATENATED MODULE: ../packages/lsp/lib/utils.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * Helper to wait for timeout.
 *
 * @param  timeout - time out in ms
 */
async function sleep(timeout) {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve();
        }, timeout);
    });
}
/**
 * Wait for an event by pooling the `isReady` function.
 */
function untilReady(isReady, maxRetrials = 35, interval = 50, intervalModifier = (i) => i) {
    return (async () => {
        let i = 0;
        while (isReady() !== true) {
            i += 1;
            if (maxRetrials !== -1 && i > maxRetrials) {
                throw Error('Too many retrials');
            }
            interval = intervalModifier(interval);
            await sleep(interval);
        }
        return isReady;
    })();
}
/**
 * Convert dotted path into dictionary.
 */
function expandDottedPaths(obj) {
    const settings = [];
    for (let key in obj) {
        const parsed = expandPath(key.split('.'), obj[key]);
        settings.push(parsed);
    }
    return lodash_mergewith_default()({}, ...settings);
}
/**
 * The docs for many language servers show settings in the
 * VSCode format, e.g.: "pyls.plugins.pyflakes.enabled"
 *
 * VSCode converts that dot notation to JSON behind the scenes,
 * as the language servers themselves don't accept that syntax.
 */
const expandPath = (path, value) => {
    const obj = Object.create(null);
    let curr = obj;
    path.forEach((prop, i) => {
        curr[prop] = Object.create(null);
        if (i === path.length - 1) {
            curr[prop] = value;
        }
        else {
            curr = curr[prop];
        }
    });
    return obj;
};
/**
 * An extended map which will create value for key on the fly.
 */
class DefaultMap extends Map {
    constructor(defaultFactory, entries) {
        super(entries);
        this.defaultFactory = defaultFactory;
    }
    get(k) {
        return this.getOrCreate(k);
    }
    getOrCreate(k, ...args) {
        if (this.has(k)) {
            return super.get(k);
        }
        else {
            let v = this.defaultFactory(k, ...args);
            this.set(k, v);
            return v;
        }
    }
}

;// CONCATENATED MODULE: ../packages/lsp/lib/ws-connection/server-capability-registration.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */
/**
 * Register the capabilities with the server capabilities provider
 *
 * @param serverCapabilities - server capabilities provider.
 * @param registration -  capabilities to be registered.
 * @return - the new server capabilities provider
 */
function registerServerCapability(serverCapabilities, registration) {
    const serverCapabilitiesCopy = JSON.parse(JSON.stringify(serverCapabilities));
    const { method, registerOptions } = registration;
    const providerName = method.substring(13) + 'Provider';
    if (providerName) {
        if (!registerOptions) {
            serverCapabilitiesCopy[providerName] = true;
        }
        else {
            serverCapabilitiesCopy[providerName] = JSON.parse(JSON.stringify(registerOptions));
        }
    }
    else {
        console.warn('Could not register server capability.', registration);
        return null;
    }
    return serverCapabilitiesCopy;
}
/**
 * Unregister the capabilities with the server capabilities provider
 *
 * @param serverCapabilities - server capabilities provider.
 * @param registration -  capabilities to be unregistered.
 * @return - the new server capabilities provider
 */
function unregisterServerCapability(serverCapabilities, unregistration) {
    const serverCapabilitiesCopy = JSON.parse(JSON.stringify(serverCapabilities));
    const { method } = unregistration;
    const providerName = method.substring(13) + 'Provider';
    delete serverCapabilitiesCopy[providerName];
    return serverCapabilitiesCopy;
}


// EXTERNAL MODULE: ../node_modules/vscode-ws-jsonrpc/lib/index.js + 7 modules
var lib = __webpack_require__(86800);
;// CONCATENATED MODULE: ../packages/lsp/lib/ws-connection/ws-connection.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */
// Disclaimer/acknowledgement: Fragments are based on https://github.com/wylieconlon/lsp-editor-adapter,
// which is copyright of wylieconlon and contributors and ISC licenced.
// ISC licence is, quote, "functionally equivalent to the simplified BSD and MIT licenses,
// but without language deemed unnecessary following the Berne Convention." (Wikipedia).
// Introduced modifications are BSD licenced, copyright JupyterLab development team.



class LspWsConnection {
    constructor(options) {
        /**
         * Map to track opened virtual documents..
         */
        this.openedUris = new Map();
        /**
         * The connection is connected?
         */
        this._isConnected = false;
        /**
         * The connection is initialized?
         */
        this._isInitialized = false;
        /**
         * Array of LSP callback disposables, it is used to
         * clear the callbacks when the connection is disposed.
         */
        this._disposables = [];
        this._disposed = new index_es6_js_.Signal(this);
        this._isDisposed = false;
        this._rootUri = options.rootUri;
    }
    /**
     * Is the language server is connected?
     */
    get isConnected() {
        return this._isConnected;
    }
    /**
     * Is the language server is initialized?
     */
    get isInitialized() {
        return this._isInitialized;
    }
    /**
     * Is the language server is connected and initialized?
     */
    get isReady() {
        return this._isConnected && this._isInitialized;
    }
    /**
     * A signal emitted when the connection is disposed.
     */
    get disposed() {
        return this._disposed;
    }
    /**
     * Check if the connection is disposed
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Initialize a connection over a web socket that speaks the LSP protocol
     */
    connect(socket) {
        this.socket = socket;
        (0,lib.listen)({
            webSocket: this.socket,
            logger: new lib.ConsoleLogger(),
            onConnection: (connection) => {
                connection.listen();
                this._isConnected = true;
                this.connection = connection;
                this.sendInitialize();
                const registerCapabilityDisposable = this.connection.onRequest('client/registerCapability', (params) => {
                    params.registrations.forEach((capabilityRegistration) => {
                        try {
                            this.serverCapabilities = registerServerCapability(this.serverCapabilities, capabilityRegistration);
                        }
                        catch (err) {
                            console.error(err);
                        }
                    });
                });
                this._disposables.push(registerCapabilityDisposable);
                const unregisterCapabilityDisposable = this.connection.onRequest('client/unregisterCapability', (params) => {
                    params.unregisterations.forEach((capabilityUnregistration) => {
                        this.serverCapabilities = unregisterServerCapability(this.serverCapabilities, capabilityUnregistration);
                    });
                });
                this._disposables.push(unregisterCapabilityDisposable);
                const disposable = this.connection.onClose(() => {
                    this._isConnected = false;
                });
                this._disposables.push(disposable);
            }
        });
    }
    /**
     * Close the connection
     */
    close() {
        if (this.connection) {
            this.connection.dispose();
        }
        this.openedUris.clear();
        this.socket.close();
    }
    /**
     * The initialize request telling the server which options the client supports
     */
    sendInitialize() {
        if (!this._isConnected) {
            return;
        }
        this.openedUris.clear();
        const message = this.initializeParams();
        this.connection
            .sendRequest('initialize', message)
            .then(params => {
            this.onServerInitialized(params);
        }, e => {
            console.warn('LSP websocket connection initialization failure', e);
        });
    }
    /**
     * Inform the server that the document was opened
     */
    sendOpen(documentInfo) {
        const textDocumentMessage = {
            textDocument: {
                uri: documentInfo.uri,
                languageId: documentInfo.languageId,
                text: documentInfo.text,
                version: documentInfo.version
            }
        };
        this.connection
            .sendNotification('textDocument/didOpen', textDocumentMessage)
            .catch(console.error);
        this.openedUris.set(documentInfo.uri, true);
        this.sendChange(documentInfo);
    }
    /**
     * Sends the full text of the document to the server
     */
    sendChange(documentInfo) {
        if (!this.isReady) {
            return;
        }
        if (!this.openedUris.get(documentInfo.uri)) {
            this.sendOpen(documentInfo);
            return;
        }
        const textDocumentChange = {
            textDocument: {
                uri: documentInfo.uri,
                version: documentInfo.version
            },
            contentChanges: [{ text: documentInfo.text }]
        };
        this.connection
            .sendNotification('textDocument/didChange', textDocumentChange)
            .catch(console.error);
        documentInfo.version++;
    }
    /**
     * Send save notification to the server.
     */
    sendSaved(documentInfo) {
        if (!this.isReady) {
            return;
        }
        const textDocumentChange = {
            textDocument: {
                uri: documentInfo.uri,
                version: documentInfo.version
            },
            text: documentInfo.text
        };
        this.connection
            .sendNotification('textDocument/didSave', textDocumentChange)
            .catch(console.error);
    }
    /**
     * Send configuration change to the server.
     */
    sendConfigurationChange(settings) {
        if (!this.isReady) {
            return;
        }
        this.connection
            .sendNotification('workspace/didChangeConfiguration', settings)
            .catch(console.error);
    }
    /**
     * Dispose the connection.
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._disposables.forEach(disposable => {
            disposable.dispose();
        });
        this._disposed.emit();
        index_es6_js_.Signal.clearData(this);
    }
    /**
     * Callback called when the server is initialized.
     */
    onServerInitialized(params) {
        this._isInitialized = true;
        this.serverCapabilities = params.capabilities;
        this.connection.sendNotification('initialized', {}).catch(console.error);
        this.connection
            .sendNotification('workspace/didChangeConfiguration', {
            settings: {}
        })
            .catch(console.error);
    }
    /**
     * Initialization parameters to be sent to the language server.
     * Subclasses should override this when adding more features.
     */
    initializeParams() {
        return {
            capabilities: {},
            processId: null,
            rootUri: this._rootUri,
            workspaceFolders: null
        };
    }
}

;// CONCATENATED MODULE: ../packages/lsp/lib/connection.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * Helper class to handle client request
 */
class ClientRequestHandler {
    constructor(connection, method, emitter) {
        this.connection = connection;
        this.method = method;
        this.emitter = emitter;
    }
    request(params) {
        // TODO check if is ready?
        this.emitter.log(MessageKind.clientRequested, {
            method: this.method,
            message: params
        });
        return this.connection
            .sendRequest(this.method, params)
            .then((result) => {
            this.emitter.log(MessageKind.resultForClient, {
                method: this.method,
                message: params
            });
            return result;
        });
    }
}
/**
 * Helper class to handle server responses
 */
class ServerRequestHandler {
    constructor(connection, method, emitter) {
        this.connection = connection;
        this.method = method;
        this.emitter = emitter;
        // on request accepts "thenable"
        this.connection.onRequest(method, this._handle.bind(this));
        this._handler = null;
    }
    setHandler(handler) {
        this._handler = handler;
    }
    clearHandler() {
        this._handler = null;
    }
    _handle(request) {
        this.emitter.log(MessageKind.serverRequested, {
            method: this.method,
            message: request
        });
        if (!this._handler) {
            return new Promise(() => undefined);
        }
        return this._handler(request, this.emitter).then(result => {
            this.emitter.log(MessageKind.responseForServer, {
                method: this.method,
                message: result
            });
            return result;
        });
    }
}
const Provider = {
    TEXT_DOCUMENT_SYNC: 'textDocumentSync',
    COMPLETION: 'completionProvider',
    HOVER: 'hoverProvider',
    SIGNATURE_HELP: 'signatureHelpProvider',
    DECLARATION: 'declarationProvider',
    DEFINITION: 'definitionProvider',
    TYPE_DEFINITION: 'typeDefinitionProvider',
    IMPLEMENTATION: 'implementationProvider',
    REFERENCES: 'referencesProvider',
    DOCUMENT_HIGHLIGHT: 'documentHighlightProvider',
    DOCUMENT_SYMBOL: 'documentSymbolProvider',
    CODE_ACTION: 'codeActionProvider',
    CODE_LENS: 'codeLensProvider',
    DOCUMENT_LINK: 'documentLinkProvider',
    COLOR: 'colorProvider',
    DOCUMENT_FORMATTING: 'documentFormattingProvider',
    DOCUMENT_RANGE_FORMATTING: 'documentRangeFormattingProvider',
    DOCUMENT_ON_TYPE_FORMATTING: 'documentOnTypeFormattingProvider',
    RENAME: 'renameProvider',
    FOLDING_RANGE: 'foldingRangeProvider',
    EXECUTE_COMMAND: 'executeCommandProvider',
    SELECTION_RANGE: 'selectionRangeProvider',
    WORKSPACE_SYMBOL: 'workspaceSymbolProvider',
    WORKSPACE: 'workspace'
};
/**
 * Create a map between the request method and its handler
 */
function createMethodMap(methods, handlerFactory) {
    const result = {};
    for (let method of Object.values(methods)) {
        result[method] = handlerFactory(method);
    }
    return result;
}
var MessageKind;
(function (MessageKind) {
    MessageKind[MessageKind["clientNotifiedServer"] = 0] = "clientNotifiedServer";
    MessageKind[MessageKind["serverNotifiedClient"] = 1] = "serverNotifiedClient";
    MessageKind[MessageKind["serverRequested"] = 2] = "serverRequested";
    MessageKind[MessageKind["clientRequested"] = 3] = "clientRequested";
    MessageKind[MessageKind["resultForClient"] = 4] = "resultForClient";
    MessageKind[MessageKind["responseForServer"] = 5] = "responseForServer";
})(MessageKind || (MessageKind = {}));
class LSPConnection extends LspWsConnection {
    constructor(options) {
        super(options);
        /**
         * Is the connection is closed manually?
         */
        this._closingManually = false;
        this._closeSignal = new index_es6_js_.Signal(this);
        this._errorSignal = new index_es6_js_.Signal(this);
        this._serverInitialized = new index_es6_js_.Signal(this);
        this._options = options;
        this.logAllCommunication = false;
        this.serverIdentifier = options.serverIdentifier;
        this.serverLanguage = options.languageId;
        this.documentsToOpen = [];
        this.clientNotifications =
            this.constructNotificationHandlers(Method.ClientNotification);
        this.serverNotifications =
            this.constructNotificationHandlers(Method.ServerNotification);
    }
    /**
     * Signal emitted when the connection is closed.
     */
    get closeSignal() {
        return this._closeSignal;
    }
    /**
     * Signal emitted when the connection receives an error
     * message.
     */
    get errorSignal() {
        return this._errorSignal;
    }
    /**
     * Signal emitted when the connection is initialized.
     */
    get serverInitialized() {
        return this._serverInitialized;
    }
    /**
     * Dispose the connection.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        Object.values(this.serverRequests).forEach(request => request.clearHandler());
        this.close();
        super.dispose();
    }
    /**
     * Helper to print the logs to logger, for now we are using
     * directly the browser's console.
     */
    log(kind, message) {
        if (this.logAllCommunication) {
            console.log(kind, message);
        }
    }
    /**
     * Send the open request to the backend when the server is
     * ready.
     */
    sendOpenWhenReady(documentInfo) {
        if (this.isReady) {
            this.sendOpen(documentInfo);
        }
        else {
            this.documentsToOpen.push(documentInfo);
        }
    }
    /**
     * Send the document changes to the server.
     */
    sendSelectiveChange(changeEvent, documentInfo) {
        this._sendChange([changeEvent], documentInfo);
    }
    /**
     * Send all changes to the server.
     */
    sendFullTextChange(text, documentInfo) {
        this._sendChange([{ text }], documentInfo);
    }
    /**
     * Check if a capability is available in the server capabilities.
     */
    provides(capability) {
        return !!(this.serverCapabilities && this.serverCapabilities[capability]);
    }
    /**
     * Close the connection to the server.
     */
    close() {
        try {
            this._closingManually = true;
            super.close();
        }
        catch (e) {
            this._closingManually = false;
        }
    }
    /**
     * Initialize a connection over a web socket that speaks the LSP.
     */
    connect(socket) {
        super.connect(socket);
        untilReady(() => {
            return this.isConnected;
        }, -1)
            .then(() => {
            const disposable = this.connection.onClose(() => {
                this._isConnected = false;
                this._closeSignal.emit(this._closingManually);
            });
            this._disposables.push(disposable);
        })
            .catch(() => {
            console.error('Could not connect onClose signal');
        });
    }
    /**
     * Get send request to the server to get completion results
     * from a completion item
     */
    async getCompletionResolve(completionItem) {
        if (!this.isReady) {
            return;
        }
        return this.connection.sendRequest('completionItem/resolve', completionItem);
    }
    /**
     * Generate the notification handlers
     */
    constructNotificationHandlers(methods) {
        const factory = () => new index_es6_js_.Signal(this);
        return createMethodMap(methods, factory);
    }
    /**
     * Generate the client request handler
     */
    constructClientRequestHandler(methods) {
        return createMethodMap(methods, method => new ClientRequestHandler(this.connection, method, this));
    }
    /**
     * Generate the server response handler
     */
    constructServerRequestHandler(methods) {
        return createMethodMap(methods, method => new ServerRequestHandler(this.connection, method, this));
    }
    /**
     * Initialization parameters to be sent to the language server.
     * Subclasses can overload this when adding more features.
     */
    initializeParams() {
        return {
            ...super.initializeParams(),
            capabilities: this._options.capabilities,
            initializationOptions: null,
            processId: null,
            workspaceFolders: null
        };
    }
    /**
     * Callback called when the server is initialized.
     */
    onServerInitialized(params) {
        this.afterInitialized();
        super.onServerInitialized(params);
        while (this.documentsToOpen.length) {
            this.sendOpen(this.documentsToOpen.pop());
        }
        this._serverInitialized.emit(this.serverCapabilities);
    }
    /**
     * Once the server is initialized, this method generates the
     * client and server handlers
     */
    afterInitialized() {
        const disposable = this.connection.onError(e => this._errorSignal.emit(e));
        this._disposables.push(disposable);
        for (const method of Object.values(Method.ServerNotification)) {
            const signal = this.serverNotifications[method];
            const disposable = this.connection.onNotification(method, params => {
                this.log(MessageKind.serverNotifiedClient, {
                    method,
                    message: params
                });
                signal.emit(params);
            });
            this._disposables.push(disposable);
        }
        for (const method of Object.values(Method.ClientNotification)) {
            const signal = this.clientNotifications[method];
            signal.connect((emitter, params) => {
                this.log(MessageKind.clientNotifiedServer, {
                    method,
                    message: params
                });
                this.connection.sendNotification(method, params).catch(console.error);
            });
        }
        this.clientRequests = this.constructClientRequestHandler(Method.ClientRequest);
        this.serverRequests = this.constructServerRequestHandler(Method.ServerRequest);
        this.serverRequests['client/registerCapability'].setHandler(async (params) => {
            params.registrations.forEach((capabilityRegistration) => {
                try {
                    const updatedCapabilities = registerServerCapability(this.serverCapabilities, capabilityRegistration);
                    if (updatedCapabilities === null) {
                        console.error(`Failed to register server capability: ${capabilityRegistration}`);
                        return;
                    }
                    this.serverCapabilities = updatedCapabilities;
                }
                catch (err) {
                    console.error(err);
                }
            });
        });
        this.serverRequests['client/unregisterCapability'].setHandler(async (params) => {
            params.unregisterations.forEach((capabilityUnregistration) => {
                this.serverCapabilities = unregisterServerCapability(this.serverCapabilities, capabilityUnregistration);
            });
        });
        this.serverRequests['workspace/configuration'].setHandler(async (params) => {
            return params.items.map(item => {
                // LSP: "If the client can’t provide a configuration setting for a given scope
                // then `null` needs to be present in the returned array."
                // for now we do not support configuration, but yaml server does not respect
                // client capability so we have a handler just for that
                return null;
            });
        });
    }
    /**
     * Send the document changed data to the server.
     */
    _sendChange(changeEvents, documentInfo) {
        if (!this.isReady) {
            return;
        }
        if (documentInfo.uri.length === 0) {
            return;
        }
        if (!this.openedUris.get(documentInfo.uri)) {
            this.sendOpen(documentInfo);
        }
        const textDocumentChange = {
            textDocument: {
                uri: documentInfo.uri,
                version: documentInfo.version
            },
            contentChanges: changeEvents
        };
        this.connection
            .sendNotification('textDocument/didChange', textDocumentChange)
            .catch(console.error);
        documentInfo.version++;
    }
}

;// CONCATENATED MODULE: ../packages/lsp/lib/connection_manager.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * Each Widget with a document (whether file or a notebook) has the same DocumentConnectionManager
 * (see JupyterLabWidgetAdapter). Using id_path instead of uri led to documents being overwritten
 * as two identical id_paths could be created for two different notebooks.
 */
class DocumentConnectionManager {
    constructor(options) {
        /**
         * Fired the first time a connection is opened. These _should_ be the only
         * invocation of `.on` (once remaining LSPFeature.connection_handlers are made
         * singletons).
         */
        this.onNewConnection = (connection) => {
            const errorSignalSlot = (_, e) => {
                console.error(e);
                let error = e.length && e.length >= 1 ? e[0] : new Error();
                if (error.message.indexOf('code = 1005') !== -1) {
                    console.error(`Connection failed for ${connection}`);
                    this._forEachDocumentOfConnection(connection, virtualDocument => {
                        console.error('disconnecting ' + virtualDocument.uri);
                        this._closed.emit({ connection, virtualDocument });
                        this._ignoredLanguages.add(virtualDocument.language);
                        console.error(`Cancelling further attempts to connect ${virtualDocument.uri} and other documents for this language (no support from the server)`);
                    });
                }
                else if (error.message.indexOf('code = 1006') !== -1) {
                    console.error('Connection closed by the server');
                }
                else {
                    console.error('Connection error:', e);
                }
            };
            connection.errorSignal.connect(errorSignalSlot);
            const serverInitializedSlot = () => {
                // Initialize using settings stored in the SettingRegistry
                this._forEachDocumentOfConnection(connection, virtualDocument => {
                    // TODO: is this still necessary, e.g. for status bar to update responsively?
                    this._initialized.emit({ connection, virtualDocument });
                });
                this.updateServerConfigurations(this.initialConfigurations);
            };
            connection.serverInitialized.connect(serverInitializedSlot);
            const closeSignalSlot = (_, closedManually) => {
                if (!closedManually) {
                    console.error('Connection unexpectedly disconnected');
                }
                else {
                    console.log('Connection closed');
                    this._forEachDocumentOfConnection(connection, virtualDocument => {
                        this._closed.emit({ connection, virtualDocument });
                    });
                }
            };
            connection.closeSignal.connect(closeSignalSlot);
        };
        this._initialized = new index_es6_js_.Signal(this);
        this._connected = new index_es6_js_.Signal(this);
        this._disconnected = new index_es6_js_.Signal(this);
        this._closed = new index_es6_js_.Signal(this);
        this._documentsChanged = new index_es6_js_.Signal(this);
        this.connections = new Map();
        this.documents = new Map();
        this.adapters = new Map();
        this._ignoredLanguages = new Set();
        this.languageServerManager = options.languageServerManager;
        Private.setLanguageServerManager(options.languageServerManager);
        options.adapterTracker.adapterAdded.connect((_, adapter) => {
            const path = adapter.widget.context.path;
            this.registerAdapter(path, adapter);
        });
    }
    /**
     * Signal emitted when the manager is initialized.
     */
    get initialized() {
        return this._initialized;
    }
    /**
     * Signal emitted when the manager is connected to the server
     */
    get connected() {
        return this._connected;
    }
    /**
     * Connection temporarily lost or could not be fully established; a re-connection will be attempted;
     */
    get disconnected() {
        return this._disconnected;
    }
    /**
     * Connection was closed permanently and no-reconnection will be attempted, e.g.:
     *  - there was a serious server error
     *  - user closed the connection,
     *  - re-connection attempts exceeded,
     */
    get closed() {
        return this._closed;
    }
    /**
     * Signal emitted when the document is changed.
     */
    get documentsChanged() {
        return this._documentsChanged;
    }
    /**
     * Promise resolved when the language server manager is ready.
     */
    get ready() {
        return Private.getLanguageServerManager().ready;
    }
    /**
     * Helper to connect various virtual document signal with callbacks of
     * this class.
     *
     * @param  virtualDocument - virtual document to be connected.
     */
    connectDocumentSignals(virtualDocument) {
        virtualDocument.foreignDocumentOpened.connect(this.onForeignDocumentOpened, this);
        virtualDocument.foreignDocumentClosed.connect(this.onForeignDocumentClosed, this);
        this.documents.set(virtualDocument.uri, virtualDocument);
        this._documentsChanged.emit(this.documents);
    }
    /**
     * Helper to disconnect various virtual document signal with callbacks of
     * this class.
     *
     * @param  virtualDocument - virtual document to be disconnected.
     */
    disconnectDocumentSignals(virtualDocument, emit = true) {
        virtualDocument.foreignDocumentOpened.disconnect(this.onForeignDocumentOpened, this);
        virtualDocument.foreignDocumentClosed.disconnect(this.onForeignDocumentClosed, this);
        this.documents.delete(virtualDocument.uri);
        for (const foreign of virtualDocument.foreignDocuments.values()) {
            this.disconnectDocumentSignals(foreign, false);
        }
        if (emit) {
            this._documentsChanged.emit(this.documents);
        }
    }
    /**
     * Handle foreign document opened event.
     */
    onForeignDocumentOpened(_host, context) {
        /** no-op */
    }
    /**
     * Handle foreign document closed event.
     */
    onForeignDocumentClosed(_host, context) {
        const { foreignDocument } = context;
        this.unregisterDocument(foreignDocument.uri, false);
        this.disconnectDocumentSignals(foreignDocument);
    }
    /**
     * @deprecated
     *
     * Register a widget adapter with this manager
     *
     * @param  path - path to the inner document of the adapter
     * @param  adapter - the adapter to be registered
     */
    registerAdapter(path, adapter) {
        this.adapters.set(path, adapter);
        adapter.widget.context.pathChanged.connect((context, newPath) => {
            this.adapters.delete(path);
            this.adapters.set(newPath, adapter);
        });
        adapter.disposed.connect(() => {
            if (adapter.virtualDocument) {
                this.documents.delete(adapter.virtualDocument.uri);
            }
            this.adapters.delete(path);
        });
    }
    /**
     * Handles the settings that do not require an existing connection
     * with a language server (or can influence to which server the
     * connection will be created, e.g. `rank`).
     *
     * This function should be called **before** initialization of servers.
     */
    updateConfiguration(allServerSettings) {
        this.languageServerManager.setConfiguration(allServerSettings);
    }
    /**
     * Handles the settings that the language servers accept using
     * `onDidChangeConfiguration` messages, which should be passed under
     * the "serverSettings" keyword in the setting registry.
     * Other configuration options are handled by `updateConfiguration` instead.
     *
     * This function should be called **after** initialization of servers.
     */
    updateServerConfigurations(allServerSettings) {
        let languageServerId;
        for (languageServerId in allServerSettings) {
            if (!allServerSettings.hasOwnProperty(languageServerId)) {
                continue;
            }
            const rawSettings = allServerSettings[languageServerId];
            const parsedSettings = expandDottedPaths(rawSettings.configuration || {});
            const serverSettings = {
                settings: parsedSettings
            };
            Private.updateServerConfiguration(languageServerId, serverSettings);
        }
    }
    /**
     * Retry to connect to the server each `reconnectDelay` seconds
     * and for `retrialsLeft` times.
     * TODO: presently no longer referenced. A failing connection would close
     * the socket, triggering the language server on the other end to exit.
     */
    async retryToConnect(options, reconnectDelay, retrialsLeft = -1) {
        let { virtualDocument } = options;
        if (this._ignoredLanguages.has(virtualDocument.language)) {
            return;
        }
        let interval = reconnectDelay * 1000;
        let success = false;
        while (retrialsLeft !== 0 && !success) {
            await this.connect(options)
                .then(() => {
                success = true;
            })
                .catch(e => {
                console.warn(e);
            });
            console.log('will attempt to re-connect in ' + interval / 1000 + ' seconds');
            await sleep(interval);
            // gradually increase the time delay, up to 5 sec
            interval = interval < 5 * 1000 ? interval + 500 : interval;
        }
    }
    /**
     * Disconnect the connection to the language server of the requested
     * language.
     */
    disconnect(languageId) {
        Private.disconnect(languageId);
    }
    /**
     * Create a new connection to the language server
     * @return A promise of the LSP connection
     */
    async connect(options, firstTimeoutSeconds = 30, secondTimeoutMinutes = 5) {
        let connection = await this._connectSocket(options);
        let { virtualDocument } = options;
        if (!connection) {
            return;
        }
        if (!connection.isReady) {
            try {
                // user feedback hinted that 40 seconds was too short and some users are willing to wait more;
                // to make the best of both worlds we first check frequently (6.6 times a second) for the first
                // 30 seconds, and show the warning early in case if something is wrong; we then continue retrying
                // for another 5 minutes, but only once per second.
                await untilReady(() => connection.isReady, Math.round((firstTimeoutSeconds * 1000) / 150), 150);
            }
            catch (_a) {
                console.log(`Connection to ${virtualDocument.uri} timed out after ${firstTimeoutSeconds} seconds, will continue retrying for another ${secondTimeoutMinutes} minutes`);
                try {
                    await untilReady(() => connection.isReady, 60 * secondTimeoutMinutes, 1000);
                }
                catch (_b) {
                    console.log(`Connection to ${virtualDocument.uri} timed out again after ${secondTimeoutMinutes} minutes, giving up`);
                    return;
                }
            }
        }
        this._connected.emit({ connection, virtualDocument });
        return connection;
    }
    /**
     * Disconnect the signals of requested virtual document URI.
     */
    unregisterDocument(uri, emit = true) {
        const connection = this.connections.get(uri);
        if (connection) {
            this.connections.delete(uri);
            const allConnection = new Set(this.connections.values());
            if (!allConnection.has(connection)) {
                this.disconnect(connection.serverIdentifier);
                connection.dispose();
            }
            if (emit) {
                this._documentsChanged.emit(this.documents);
            }
        }
    }
    /**
     * Enable or disable the logging of language server communication.
     */
    updateLogging(logAllCommunication, setTrace) {
        for (const connection of this.connections.values()) {
            connection.logAllCommunication = logAllCommunication;
            if (setTrace !== null) {
                connection.clientNotifications['$/setTrace'].emit({ value: setTrace });
            }
        }
    }
    /**
     * Create the LSP connection for requested virtual document.
     *
     * @return  Return the promise of the LSP connection.
     */
    async _connectSocket(options) {
        let { language, capabilities, virtualDocument } = options;
        this.connectDocumentSignals(virtualDocument);
        const uris = DocumentConnectionManager.solveUris(virtualDocument, language);
        const matchingServers = this.languageServerManager.getMatchingServers({
            language
        });
        // for now use only the server with the highest rank.
        const languageServerId = matchingServers.length === 0 ? null : matchingServers[0];
        // lazily load 1) the underlying library (1.5mb) and/or 2) a live WebSocket-
        // like connection: either already connected or potentially in the process
        // of connecting.
        if (!uris) {
            return;
        }
        const connection = await Private.connection(language, languageServerId, uris, this.onNewConnection, capabilities);
        // if connecting for the first time, all documents subsequent documents will
        // be re-opened and synced
        this.connections.set(virtualDocument.uri, connection);
        return connection;
    }
    /**
     * Helper to apply callback on all documents of a connection.
     */
    _forEachDocumentOfConnection(connection, callback) {
        for (const [virtualDocumentUri, currentConnection] of this.connections.entries()) {
            if (connection !== currentConnection) {
                continue;
            }
            callback(this.documents.get(virtualDocumentUri));
        }
    }
}
(function (DocumentConnectionManager) {
    /**
     * Generate the URI of a virtual document from input
     *
     * @param  virtualDocument - the virtual document
     * @param  language - language of the document
     */
    function solveUris(virtualDocument, language) {
        var _a;
        const serverManager = Private.getLanguageServerManager();
        const wsBase = serverManager.settings.wsUrl;
        const rootUri = coreutils_lib_index_js_.PageConfig.getOption('rootUri');
        const virtualDocumentsUri = coreutils_lib_index_js_.PageConfig.getOption('virtualDocumentsUri');
        // for now take the best match only
        const serverOptions = {
            language
        };
        const matchingServers = serverManager.getMatchingServers(serverOptions);
        const languageServerId = matchingServers.length === 0 ? null : matchingServers[0];
        if (languageServerId === null) {
            return;
        }
        const specs = serverManager.getMatchingSpecs(serverOptions);
        const spec = specs.get(languageServerId);
        if (!spec) {
            console.warn(`Specification not available for server ${languageServerId}`);
        }
        const requiresOnDiskFiles = (_a = spec === null || spec === void 0 ? void 0 : spec.requires_documents_on_disk) !== null && _a !== void 0 ? _a : true;
        const supportsInMemoryFiles = !requiresOnDiskFiles;
        const baseUri = virtualDocument.hasLspSupportedFile || supportsInMemoryFiles
            ? rootUri
            : virtualDocumentsUri;
        // workaround url-parse bug(s) (see https://github.com/jupyter-lsp/jupyterlab-lsp/issues/595)
        let documentUri = coreutils_lib_index_js_.URLExt.join(baseUri, virtualDocument.uri);
        if (!documentUri.startsWith('file:///') &&
            documentUri.startsWith('file://')) {
            documentUri = documentUri.replace('file://', 'file:///');
            if (documentUri.startsWith('file:///users/') &&
                baseUri.startsWith('file:///Users/')) {
                documentUri = documentUri.replace('file:///users/', 'file:///Users/');
            }
        }
        return {
            base: baseUri,
            document: documentUri,
            server: coreutils_lib_index_js_.URLExt.join('ws://jupyter-lsp', language),
            socket: coreutils_lib_index_js_.URLExt.join(wsBase, 'lsp', 'ws', languageServerId)
        };
    }
    DocumentConnectionManager.solveUris = solveUris;
})(DocumentConnectionManager || (DocumentConnectionManager = {}));
/**
 * Namespace primarily for language-keyed cache of LSPConnections
 */
var Private;
(function (Private) {
    const _connections = new Map();
    let _languageServerManager;
    function getLanguageServerManager() {
        return _languageServerManager;
    }
    Private.getLanguageServerManager = getLanguageServerManager;
    function setLanguageServerManager(languageServerManager) {
        _languageServerManager = languageServerManager;
    }
    Private.setLanguageServerManager = setLanguageServerManager;
    function disconnect(languageServerId) {
        const connection = _connections.get(languageServerId);
        if (connection) {
            connection.close();
            _connections.delete(languageServerId);
        }
    }
    Private.disconnect = disconnect;
    /**
     * Return (or create and initialize) the WebSocket associated with the language
     */
    async function connection(language, languageServerId, uris, onCreate, capabilities) {
        let connection = _connections.get(languageServerId);
        if (!connection) {
            const { settings } = Private.getLanguageServerManager();
            const socket = new settings.WebSocket(uris.socket);
            const connection = new LSPConnection({
                languageId: language,
                serverUri: uris.server,
                rootUri: uris.base,
                serverIdentifier: languageServerId,
                capabilities: capabilities
            });
            _connections.set(languageServerId, connection);
            connection.connect(socket);
            onCreate(connection);
        }
        connection = _connections.get(languageServerId);
        return connection;
    }
    Private.connection = connection;
    function updateServerConfiguration(languageServerId, settings) {
        const connection = _connections.get(languageServerId);
        if (connection) {
            connection.sendConfigurationChange(settings);
        }
    }
    Private.updateServerConfiguration = updateServerConfiguration;
})(Private || (Private = {}));

;// CONCATENATED MODULE: ../packages/lsp/lib/extractors/manager.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * Manager for the code extractors
 */
class CodeExtractorsManager {
    constructor() {
        this._extractorMap = new Map();
        this._extractorMapAnyLanguage = new Map();
    }
    /**
     * Get the extractors for the input cell type and the main language of
     * the document
     *
     * @param  cellType - type of cell
     * @param  hostLanguage - main language of the document
     */
    getExtractors(cellType, hostLanguage) {
        var _a, _b;
        if (hostLanguage) {
            const currentMap = this._extractorMap.get(cellType);
            if (!currentMap) {
                return [];
            }
            return (_a = currentMap.get(hostLanguage)) !== null && _a !== void 0 ? _a : [];
        }
        else {
            return (_b = this._extractorMapAnyLanguage.get(cellType)) !== null && _b !== void 0 ? _b : [];
        }
    }
    /**
     * Register an extractor to extract foreign code from host documents of specified language.
     */
    register(extractor, hostLanguage) {
        const cellType = extractor.cellType;
        if (hostLanguage) {
            cellType.forEach(type => {
                if (!this._extractorMap.has(type)) {
                    this._extractorMap.set(type, new Map());
                }
                const currentMap = this._extractorMap.get(type);
                const extractorList = currentMap.get(hostLanguage);
                if (!extractorList) {
                    currentMap.set(hostLanguage, [extractor]);
                }
                else {
                    extractorList.push(extractor);
                }
            });
        }
        else {
            cellType.forEach(type => {
                if (!this._extractorMapAnyLanguage.has(type)) {
                    this._extractorMapAnyLanguage.set(type, []);
                }
                this._extractorMapAnyLanguage.get(type).push(extractor);
            });
        }
    }
}

;// CONCATENATED MODULE: ../packages/lsp/lib/positioning.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * Compare two `IPosition` variable.
 *
 */
function isEqual(self, other) {
    return other && self.line === other.line && self.ch === other.ch;
}
/**
 * Given a list of line and an offset from the start, compute the corresponding
 * position in form of line and column number
 *
 * @param offset - number of spaces counted from the start of first line
 * @param  lines - list of lines to compute the position
 * @return  - the position of cursor
 */
function positionAtOffset(offset, lines) {
    let line = 0;
    let column = 0;
    for (let textLine of lines) {
        // each line has a new line symbol which is accounted for in offset!
        if (textLine.length + 1 <= offset) {
            offset -= textLine.length + 1;
            line += 1;
        }
        else {
            column = offset;
            break;
        }
    }
    return { line, column };
}
/**
 * Given a list of line and position in form of line and column number,
 * compute the offset from the start of first line.
 * @param position - postion of cursor
 * @param  lines - list of lines to compute the position
 * @param linesIncludeBreaks - should count the line break as space?
 * return - offset number
 */
function offsetAtPosition(position, lines, linesIncludeBreaks = false) {
    let breakIncrement = linesIncludeBreaks ? 0 : 1;
    let offset = 0;
    for (let i = 0; i < lines.length; i++) {
        let textLine = lines[i];
        if (position.line > i) {
            offset += textLine.length + breakIncrement;
        }
        else {
            offset += position.column;
            break;
        }
    }
    return offset;
}
var ProtocolCoordinates;
(function (ProtocolCoordinates) {
    /**
     * Check if the position is in the input range
     *
     * @param position - position in form of line and character number.
     * @param  range - range in from of start and end position.
     */
    function isWithinRange(position, range) {
        const { line, character } = position;
        return (line >= range.start.line &&
            line <= range.end.line &&
            // need to be non-overlapping see https://github.com/jupyter-lsp/jupyterlab-lsp/issues/628
            (line != range.start.line || character > range.start.character) &&
            (line != range.end.line || character <= range.end.character));
    }
    ProtocolCoordinates.isWithinRange = isWithinRange;
})(ProtocolCoordinates || (ProtocolCoordinates = {}));

;// CONCATENATED MODULE: ../packages/lsp/lib/extractors/text_extractor.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The code extractor for the raw and markdown text.
 */
class TextForeignCodeExtractor {
    constructor(options) {
        this.language = options.language;
        this.standalone = options.isStandalone;
        this.fileExtension = options.file_extension;
        this.cellType = options.cellType;
    }
    /**
     * Test if there is any foreign code in provided code snippet.
     */
    hasForeignCode(code, cellType) {
        return this.cellType.includes(cellType);
    }
    /**
     * Split the code into the host and foreign code (if any foreign code was detected)
     */
    extractForeignCode(code) {
        let lines = code.split('\n');
        let extracts = new Array();
        let foreignCodeFragment = code;
        let start = positionAtOffset(0, lines);
        let end = positionAtOffset(foreignCodeFragment.length, lines);
        extracts.push({
            hostCode: '',
            foreignCode: foreignCodeFragment,
            range: { start, end },
            virtualShift: null
        });
        return extracts;
    }
}

;// CONCATENATED MODULE: ../packages/lsp/lib/extractors/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




;// CONCATENATED MODULE: ../packages/lsp/lib/feature.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * Class to manager the registered features of the language servers.
 */
class FeatureManager {
    constructor() {
        /**
         * List of registered features
         */
        this.features = [];
        this._featureRegistered = new index_es6_js_.Signal(this);
    }
    /**
     * Signal emitted when a new feature is registered.
     */
    get featureRegistered() {
        return this._featureRegistered;
    }
    /**
     * Register a new feature, skip if it is already registered.
     */
    register(feature) {
        if (this.features.some(ft => ft.id === feature.id)) {
            console.warn(`Feature with id ${feature.id} is already registered, skipping.`);
        }
        else {
            this.features.push(feature);
            this._featureRegistered.emit(feature);
        }
    }
    /**
     * Get the capabilities of all clients.
     */
    clientCapabilities() {
        let capabilities = {};
        for (const feature of this.features) {
            if (!feature.capabilities) {
                continue;
            }
            capabilities = lodash_mergewith_default()(capabilities, feature.capabilities);
        }
        return capabilities;
    }
    /**
     * Get the extension factories of all clients.
     */
    extensionFactories() {
        const factories = [];
        for (const feature of this.features) {
            if (!feature.extensionFactory) {
                continue;
            }
            factories.push(feature.extensionFactory);
        }
        return factories;
    }
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/services@~7.1.0-alpha.2 (singleton) (fallback: ../packages/services/lib/index.js)
var services_lib_index_js_ = __webpack_require__(43411);
;// CONCATENATED MODULE: ../packages/lsp/lib/manager.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





class LanguageServerManager {
    constructor(options) {
        /**
         * map of language server sessions.
         */
        this._sessions = new Map();
        /**
         * Map of language server specs.
         */
        this._specs = new Map();
        /**
         * Set of emitted warning message, message in this set will not be warned again.
         */
        this._warningsEmitted = new Set();
        /**
         * A promise resolved when this server manager is ready.
         */
        this._ready = new dist_index_js_.PromiseDelegate();
        /**
         * Signal emitted when a  language server session is changed
         */
        this._sessionsChanged = new index_es6_js_.Signal(this);
        this._isDisposed = false;
        /**
         * Check if the manager is enabled or disabled
         */
        this._enabled = true;
        this._settings = options.settings || services_lib_index_js_.ServerConnection.makeSettings();
        this._baseUrl = options.baseUrl || coreutils_lib_index_js_.PageConfig.getBaseUrl();
        this._retries = options.retries || 2;
        this._retriesInterval = options.retriesInterval || 10000;
        this._statusCode = -1;
        this._configuration = {};
        this.fetchSessions().catch(e => console.log(e));
    }
    /**
     * Check if the manager is enabled or disabled
     */
    get isEnabled() {
        return this._enabled;
    }
    /**
     * Check if the manager is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Get server connection settings.
     */
    get settings() {
        return this._settings;
    }
    /**
     * Get the language server specs.
     */
    get specs() {
        return this._specs;
    }
    /**
     * Get the status end point.
     */
    get statusUrl() {
        return coreutils_lib_index_js_.URLExt.join(this._baseUrl, ILanguageServerManager.URL_NS, 'status');
    }
    /**
     * Signal emitted when a  language server session is changed
     */
    get sessionsChanged() {
        return this._sessionsChanged;
    }
    /**
     * Get the map of language server sessions.
     */
    get sessions() {
        return this._sessions;
    }
    /**
     * A promise resolved when this server manager is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * Get the status code of server's responses.
     */
    get statusCode() {
        return this._statusCode;
    }
    /**
     * Enable the language server services
     */
    async enable() {
        this._enabled = true;
        await this.fetchSessions();
    }
    /**
     * Disable the language server services
     */
    disable() {
        this._enabled = false;
        this._sessions = new Map();
        this._sessionsChanged.emit(void 0);
    }
    /**
     * Dispose the manager.
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        index_es6_js_.Signal.clearData(this);
    }
    /**
     * Update the language server configuration.
     */
    setConfiguration(configuration) {
        this._configuration = configuration;
    }
    /**
     * Get matching language server for input language option.
     */
    getMatchingServers(options) {
        if (!options.language) {
            console.error('Cannot match server by language: language not available; ensure that kernel and specs provide language and MIME type');
            return [];
        }
        const matchingSessionsKeys = [];
        for (const [key, session] of this._sessions.entries()) {
            if (this.isMatchingSpec(options, session.spec)) {
                matchingSessionsKeys.push(key);
            }
        }
        return matchingSessionsKeys.sort(this.compareRanks.bind(this));
    }
    /**
     * Get matching language server spec for input language option.
     */
    getMatchingSpecs(options) {
        const result = new Map();
        for (const [key, specification] of this._specs.entries()) {
            if (this.isMatchingSpec(options, specification)) {
                result.set(key, specification);
            }
        }
        return result;
    }
    /**
     * Fetch the server session list from the status endpoint. The server
     * manager is ready once this method finishes.
     */
    async fetchSessions() {
        if (!this._enabled) {
            return;
        }
        let response = await services_lib_index_js_.ServerConnection.makeRequest(this.statusUrl, { method: 'GET' }, this._settings);
        this._statusCode = response.status;
        if (!response.ok) {
            if (this._retries > 0) {
                this._retries -= 1;
                setTimeout(this.fetchSessions.bind(this), this._retriesInterval);
            }
            else {
                this._ready.resolve(undefined);
                console.log('Missing jupyter_lsp server extension, skipping.');
            }
            return;
        }
        let sessions;
        try {
            const data = await response.json();
            sessions = data.sessions;
            try {
                this.version = data.version;
                this._specs = new Map(Object.entries(data.specs));
            }
            catch (err) {
                console.warn(err);
            }
        }
        catch (err) {
            console.warn(err);
            this._ready.resolve(undefined);
            return;
        }
        for (let key of Object.keys(sessions)) {
            let id = key;
            if (this._sessions.has(id)) {
                Object.assign(this._sessions.get(id) || {}, sessions[key]);
            }
            else {
                this._sessions.set(id, sessions[key]);
            }
        }
        const oldKeys = this._sessions.keys();
        for (const oldKey in oldKeys) {
            if (!sessions[oldKey]) {
                let oldId = oldKey;
                this._sessions.delete(oldId);
            }
        }
        this._sessionsChanged.emit(void 0);
        this._ready.resolve(undefined);
    }
    /**
     * Check if input language option maths the language server spec.
     */
    isMatchingSpec(options, spec) {
        // most things speak language
        // if language is not known, it is guessed based on MIME type earlier
        // so some language should be available by now (which can be not so obvious, e.g. "plain" for txt documents)
        const lowerCaseLanguage = options.language.toLocaleLowerCase();
        return spec.languages.some((language) => language.toLocaleLowerCase() == lowerCaseLanguage);
    }
    /**
     * Helper function to warn a message only once.
     */
    warnOnce(arg) {
        if (!this._warningsEmitted.has(arg)) {
            this._warningsEmitted.add(arg);
            console.warn(arg);
        }
    }
    /**
     * Compare the rank of two servers with the same language.
     */
    compareRanks(a, b) {
        var _a, _b, _c, _d;
        const DEFAULT_RANK = 50;
        const aRank = (_b = (_a = this._configuration[a]) === null || _a === void 0 ? void 0 : _a.rank) !== null && _b !== void 0 ? _b : DEFAULT_RANK;
        const bRank = (_d = (_c = this._configuration[b]) === null || _c === void 0 ? void 0 : _c.rank) !== null && _d !== void 0 ? _d : DEFAULT_RANK;
        if (aRank == bRank) {
            this.warnOnce(`Two matching servers: ${a} and ${b} have the same rank; choose which one to use by changing the rank in Advanced Settings Editor`);
            return a.localeCompare(b);
        }
        // higher rank = higher in the list (descending order)
        return bRank - aRank;
    }
}

;// CONCATENATED MODULE: ../packages/lsp/lib/virtual/document.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * Check if given position is within range.
 * Both start and end are inclusive.
 * @param position
 * @param range
 */
function isWithinRange(position, range) {
    if (range.start.line === range.end.line) {
        return (position.line === range.start.line &&
            position.column >= range.start.column &&
            position.column <= range.end.column);
    }
    return ((position.line === range.start.line &&
        position.column >= range.start.column &&
        position.line < range.end.line) ||
        (position.line > range.start.line &&
            position.column <= range.end.column &&
            position.line === range.end.line) ||
        (position.line > range.start.line && position.line < range.end.line));
}
/**
 * A virtual implementation of IDocumentInfo
 */
class VirtualDocumentInfo {
    /**
     * Creates an instance of VirtualDocumentInfo.
     * @param document - the virtual document need to
     * be wrapped.
     */
    constructor(document) {
        /**
         * Current version of the virtual document.
         */
        this.version = 0;
        this._document = document;
    }
    /**
     * Get the text content of the virtual document.
     */
    get text() {
        return this._document.value;
    }
    /**
     * Get the uri of the virtual document, if the document is not available,
     * it returns an empty string, users need to check for the length of returned
     * value before using it.
     */
    get uri() {
        const uris = DocumentConnectionManager.solveUris(this._document, this.languageId);
        if (!uris) {
            return '';
        }
        return uris.document;
    }
    /**
     * Get the language identifier of the document.
     */
    get languageId() {
        return this._document.language;
    }
}
/**
 *
 * A notebook can hold one or more virtual documents; there is always one,
 * "root" document, corresponding to the language of the kernel. All other
 * virtual documents are extracted out of the notebook, based on magics,
 * or other syntax constructs, depending on the kernel language.
 *
 * Virtual documents represent the underlying code in a single language,
 * which has been parsed excluding interactive kernel commands (magics)
 * which could be misunderstood by the specific LSP server.
 *
 * VirtualDocument has no awareness of the notebook or editor it lives in,
 * however it is able to transform its content back to the notebook space,
 * as it keeps editor coordinates for each virtual line.
 *
 * The notebook/editor aware transformations are preferred to be placed in
 * VirtualEditor descendants rather than here.
 *
 * No dependency on editor implementation (such as CodeMirrorEditor)
 * is allowed for VirtualEditor.
 */
class VirtualDocument {
    constructor(options) {
        /**
         * Number of blank lines appended to the virtual document between
         * each cell.
         */
        this.blankLinesBetweenCells = 2;
        this._isDisposed = false;
        this._foreignDocumentClosed = new index_es6_js_.Signal(this);
        this._foreignDocumentOpened = new index_es6_js_.Signal(this);
        this._changed = new index_es6_js_.Signal(this);
        this.options = options;
        this.path = this.options.path;
        this.fileExtension = options.fileExtension;
        this.hasLspSupportedFile = options.hasLspSupportedFile;
        this.parent = options.parent;
        this.language = options.language;
        this.virtualLines = new Map();
        this.sourceLines = new Map();
        this.foreignDocuments = new Map();
        this._editorToSourceLine = new Map();
        this._foreignCodeExtractors = options.foreignCodeExtractors;
        this.standalone = options.standalone || false;
        this.instanceId = VirtualDocument.instancesCount;
        VirtualDocument.instancesCount += 1;
        this.unusedStandaloneDocuments = new DefaultMap(() => new Array());
        this._remainingLifetime = 6;
        this.documentInfo = new VirtualDocumentInfo(this);
        this.updateManager = new UpdateManager(this);
        this.updateManager.updateBegan.connect(this._updateBeganSlot, this);
        this.updateManager.blockAdded.connect(this._blockAddedSlot, this);
        this.updateManager.updateFinished.connect(this._updateFinishedSlot, this);
        this.clear();
    }
    /**
     * Convert from code editor position into code mirror position.
     */
    static ceToCm(position) {
        return { line: position.line, ch: position.column };
    }
    /**
     * Test whether the document is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Signal emitted when the foreign document is closed
     */
    get foreignDocumentClosed() {
        return this._foreignDocumentClosed;
    }
    /**
     * Signal emitted when the foreign document is opened
     */
    get foreignDocumentOpened() {
        return this._foreignDocumentOpened;
    }
    /**
     * Signal emitted when the foreign document is changed
     */
    get changed() {
        return this._changed;
    }
    /**
     * Id of the virtual document.
     */
    get virtualId() {
        // for easier debugging, the language information is included in the ID:
        return this.standalone
            ? this.instanceId + '(' + this.language + ')'
            : this.language;
    }
    /**
     * Return the ancestry to this document.
     */
    get ancestry() {
        if (!this.parent) {
            return [this];
        }
        return this.parent.ancestry.concat([this]);
    }
    /**
     * Return the id path to the virtual document.
     */
    get idPath() {
        if (!this.parent) {
            return this.virtualId;
        }
        return this.parent.idPath + '-' + this.virtualId;
    }
    /**
     * Get the uri of the virtual document.
     */
    get uri() {
        const encodedPath = encodeURI(this.path);
        if (!this.parent) {
            return encodedPath;
        }
        return encodedPath + '.' + this.idPath + '.' + this.fileExtension;
    }
    /**
     * Get the text value of the document
     */
    get value() {
        let linesPadding = '\n'.repeat(this.blankLinesBetweenCells);
        return this.lineBlocks.join(linesPadding);
    }
    /**
     * Get the last line in the virtual document
     */
    get lastLine() {
        const linesInLastBlock = this.lineBlocks[this.lineBlocks.length - 1].split('\n');
        return linesInLastBlock[linesInLastBlock.length - 1];
    }
    /**
     * Get the root document of current virtual document.
     */
    get root() {
        return this.parent ? this.parent.root : this;
    }
    /**
     * Dispose the virtual document.
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        this.parent = null;
        this.closeAllForeignDocuments();
        this.updateManager.dispose();
        // clear all the maps
        this.foreignDocuments.clear();
        this.sourceLines.clear();
        this.unusedStandaloneDocuments.clear();
        this.virtualLines.clear();
        // just to be sure - if anything is accessed after disposal (it should not) we
        // will get altered by errors in the console AND this will limit memory leaks
        this.documentInfo = null;
        this.lineBlocks = null;
        index_es6_js_.Signal.clearData(this);
    }
    /**
     * Clear the virtual document and all related stuffs
     */
    clear() {
        for (let document of this.foreignDocuments.values()) {
            document.clear();
        }
        // TODO - deep clear (assure that there is no memory leak)
        this.unusedStandaloneDocuments.clear();
        this.virtualLines.clear();
        this.sourceLines.clear();
        this.lastVirtualLine = 0;
        this.lastSourceLine = 0;
        this.lineBlocks = [];
    }
    /**
     * Get the virtual document from the cursor position of the source
     * document
     * @param position - position in source document
     */
    documentAtSourcePosition(position) {
        let sourceLine = this.sourceLines.get(position.line);
        if (!sourceLine) {
            return this;
        }
        let sourcePositionCe = {
            line: sourceLine.editorLine,
            column: position.ch
        };
        for (let [range, { virtualDocument: document }] of sourceLine.foreignDocumentsMap) {
            if (isWithinRange(sourcePositionCe, range)) {
                let sourcePositionCm = {
                    line: sourcePositionCe.line - range.start.line,
                    ch: sourcePositionCe.column - range.start.column
                };
                return document.documentAtSourcePosition(sourcePositionCm);
            }
        }
        return this;
    }
    /**
     * Detect if the input source position is belong to the current
     * virtual document.
     *
     * @param sourcePosition - position in the source document
     */
    isWithinForeign(sourcePosition) {
        let sourceLine = this.sourceLines.get(sourcePosition.line);
        let sourcePositionCe = {
            line: sourceLine.editorLine,
            column: sourcePosition.ch
        };
        for (let [range] of sourceLine.foreignDocumentsMap) {
            if (isWithinRange(sourcePositionCe, range)) {
                return true;
            }
        }
        return false;
    }
    /**
     * Compute the position in root document from the position of
     * a child editor.
     *
     * @param editor - the active editor.
     * @param position - position in the active editor.
     */
    transformFromEditorToRoot(editor, position) {
        if (!this._editorToSourceLine.has(editor)) {
            console.log('Editor not found in _editorToSourceLine map');
            return null;
        }
        let shift = this._editorToSourceLine.get(editor);
        return {
            ...position,
            line: position.line + shift
        };
    }
    /**
     * Compute the position in the virtual document from the position
     * if the source document.
     *
     * @param sourcePosition - position in source document
     */
    virtualPositionAtDocument(sourcePosition) {
        let sourceLine = this.sourceLines.get(sourcePosition.line);
        if (sourceLine == null) {
            throw new Error('Source line not mapped to virtual position');
        }
        let virtualLine = sourceLine.virtualLine;
        // position inside the cell (block)
        let sourcePositionCe = {
            line: sourceLine.editorLine,
            column: sourcePosition.ch
        };
        for (let [range, content] of sourceLine.foreignDocumentsMap) {
            const { virtualLine, virtualDocument: document } = content;
            if (isWithinRange(sourcePositionCe, range)) {
                // position inside the foreign document block
                let sourcePositionCm = {
                    line: sourcePositionCe.line - range.start.line,
                    ch: sourcePositionCe.column - range.start.column
                };
                if (document.isWithinForeign(sourcePositionCm)) {
                    return this.virtualPositionAtDocument(sourcePositionCm);
                }
                else {
                    // where in this block in the entire foreign document?
                    sourcePositionCm.line += virtualLine;
                    return sourcePositionCm;
                }
            }
        }
        return {
            ch: sourcePosition.ch,
            line: virtualLine
        };
    }
    /**
     * Append a code block to the end of the virtual document.
     *
     * @param  block - block to be appended
     * @param  editorShift - position shift in source
     * document
     * @param  [virtualShift] - position shift in
     * virtual document.
     */
    appendCodeBlock(block, editorShift = { line: 0, column: 0 }, virtualShift) {
        let cellCode = block.value;
        let ceEditor = block.ceEditor;
        if (this.isDisposed) {
            console.warn('Cannot append code block: document disposed');
            return;
        }
        let sourceCellLines = cellCode.split('\n');
        let { lines, foreignDocumentsMap } = this.prepareCodeBlock(block, editorShift);
        for (let i = 0; i < lines.length; i++) {
            this.virtualLines.set(this.lastVirtualLine + i, {
                skipInspect: [],
                editor: ceEditor,
                // TODO this is incorrect, wont work if something was extracted
                sourceLine: this.lastSourceLine + i
            });
        }
        for (let i = 0; i < sourceCellLines.length; i++) {
            this.sourceLines.set(this.lastSourceLine + i, {
                editorLine: i,
                editorShift: {
                    line: editorShift.line - ((virtualShift === null || virtualShift === void 0 ? void 0 : virtualShift.line) || 0),
                    column: i === 0 ? editorShift.column - ((virtualShift === null || virtualShift === void 0 ? void 0 : virtualShift.column) || 0) : 0
                },
                // TODO: move those to a new abstraction layer (DocumentBlock class)
                editor: ceEditor,
                foreignDocumentsMap,
                // TODO this is incorrect, wont work if something was extracted
                virtualLine: this.lastVirtualLine + i
            });
        }
        this.lastVirtualLine += lines.length;
        // one empty line is necessary to separate code blocks, next 'n' lines are to silence linters;
        // the final cell does not get the additional lines (thanks to the use of join, see below)
        this.lineBlocks.push(lines.join('\n') + '\n');
        // adding the virtual lines for the blank lines
        for (let i = 0; i < this.blankLinesBetweenCells; i++) {
            this.virtualLines.set(this.lastVirtualLine + i, {
                skipInspect: [this.idPath],
                editor: ceEditor,
                sourceLine: null
            });
        }
        this.lastVirtualLine += this.blankLinesBetweenCells;
        this.lastSourceLine += sourceCellLines.length;
    }
    /**
     * Extract a code block into list of string in supported language and
     * a map of foreign document if any.
     * @param  block - block to be appended
     * @param  editorShift - position shift in source document
     */
    prepareCodeBlock(block, editorShift = { line: 0, column: 0 }) {
        let { cellCodeKept, foreignDocumentsMap } = this.extractForeignCode(block, editorShift);
        let lines = cellCodeKept.split('\n');
        return { lines, foreignDocumentsMap };
    }
    /**
     * Extract the foreign code from input block by using the registered
     * extractors.
     * @param  block - block to be appended
     * @param  editorShift - position shift in source document
     */
    extractForeignCode(block, editorShift) {
        let foreignDocumentsMap = new Map();
        let cellCode = block.value;
        const extractorsForAnyLang = this._foreignCodeExtractors.getExtractors(block.type, null);
        const extractorsForCurrentLang = this._foreignCodeExtractors.getExtractors(block.type, this.language);
        for (let extractor of [
            ...extractorsForAnyLang,
            ...extractorsForCurrentLang
        ]) {
            if (!extractor.hasForeignCode(cellCode, block.type)) {
                continue;
            }
            let results = extractor.extractForeignCode(cellCode);
            let keptCellCode = '';
            for (let result of results) {
                if (result.foreignCode !== null) {
                    // result.range should only be null if result.foregin_code is null
                    if (result.range === null) {
                        console.log('Failure in foreign code extraction: `range` is null but `foreign_code` is not!');
                        continue;
                    }
                    let foreignDocument = this.chooseForeignDocument(extractor);
                    foreignDocumentsMap.set(result.range, {
                        virtualLine: foreignDocument.lastVirtualLine,
                        virtualDocument: foreignDocument,
                        editor: block.ceEditor
                    });
                    let foreignShift = {
                        line: editorShift.line + result.range.start.line,
                        column: editorShift.column + result.range.start.column
                    };
                    foreignDocument.appendCodeBlock({
                        value: result.foreignCode,
                        ceEditor: block.ceEditor,
                        type: 'code'
                    }, foreignShift, result.virtualShift);
                }
                if (result.hostCode != null) {
                    keptCellCode += result.hostCode;
                }
            }
            // not breaking - many extractors are allowed to process the code, one after each other
            // (think JS and CSS in HTML, or %R inside of %%timeit).
            cellCode = keptCellCode;
        }
        return { cellCodeKept: cellCode, foreignDocumentsMap };
    }
    /**
     * Close a foreign document and disconnect all associated signals
     */
    closeForeign(document) {
        this._foreignDocumentClosed.emit({
            foreignDocument: document,
            parentHost: this
        });
        // remove it from foreign documents list
        this.foreignDocuments.delete(document.virtualId);
        // and delete the documents within it
        document.closeAllForeignDocuments();
        document.foreignDocumentClosed.disconnect(this.forwardClosedSignal, this);
        document.foreignDocumentOpened.disconnect(this.forwardOpenedSignal, this);
        document.dispose();
    }
    /**
     * Close all foreign documents.
     */
    closeAllForeignDocuments() {
        for (let document of this.foreignDocuments.values()) {
            this.closeForeign(document);
        }
    }
    /**
     * Close all expired documents.
     */
    closeExpiredDocuments() {
        const usedDocuments = new Set();
        for (const line of this.sourceLines.values()) {
            for (const block of line.foreignDocumentsMap.values()) {
                usedDocuments.add(block.virtualDocument);
            }
        }
        const documentIDs = new Map();
        for (const [id, document] of this.foreignDocuments.entries()) {
            const ids = documentIDs.get(document);
            if (typeof ids !== 'undefined') {
                documentIDs.set(document, [...ids, id]);
            }
            documentIDs.set(document, [id]);
        }
        const allDocuments = new Set(documentIDs.keys());
        const unusedVirtualDocuments = new Set([...allDocuments].filter(x => !usedDocuments.has(x)));
        for (let document of unusedVirtualDocuments.values()) {
            document.remainingLifetime -= 1;
            if (document.remainingLifetime <= 0) {
                document.dispose();
                const ids = documentIDs.get(document);
                for (const id of ids) {
                    this.foreignDocuments.delete(id);
                }
            }
        }
    }
    /**
     * Transform the position of the source to the editor
     * position.
     *
     * @param  pos - position in the source document
     * @return position in the editor.
     */
    transformSourceToEditor(pos) {
        let sourceLine = this.sourceLines.get(pos.line);
        let editorLine = sourceLine.editorLine;
        let editorShift = sourceLine.editorShift;
        return {
            // only shift column in the line beginning the virtual document (first list of the editor in cell magics, but might be any line of editor in line magics!)
            ch: pos.ch + (editorLine === 0 ? editorShift.column : 0),
            line: editorLine + editorShift.line
            // TODO or:
            //  line: pos.line + editor_shift.line - this.first_line_of_the_block(editor)
        };
    }
    /**
     * Transform the position in the virtual document to the
     * editor position.
     * Can be null because some lines are added as padding/anchors
     * to the virtual document and those do not exist in the source document
     * and thus they are absent in the editor.
     */
    transformVirtualToEditor(virtualPosition) {
        let sourcePosition = this.transformVirtualToSource(virtualPosition);
        if (sourcePosition == null) {
            return null;
        }
        return this.transformSourceToEditor(sourcePosition);
    }
    /**
     * Transform the position in the virtual document to the source.
     * Can be null because some lines are added as padding/anchors
     * to the virtual document and those do not exist in the source document.
     */
    transformVirtualToSource(position) {
        const line = this.virtualLines.get(position.line).sourceLine;
        if (line == null) {
            return null;
        }
        return {
            ch: position.ch,
            line: line
        };
    }
    /**
     * Get the corresponding editor of the virtual line.
     */
    getEditorAtVirtualLine(pos) {
        let line = pos.line;
        // tolerate overshot by one (the hanging blank line at the end)
        if (!this.virtualLines.has(line)) {
            line -= 1;
        }
        return this.virtualLines.get(line).editor;
    }
    /**
     * Get the corresponding editor of the source line
     */
    getEditorAtSourceLine(pos) {
        return this.sourceLines.get(pos.line).editor;
    }
    /**
     * Recursively emits changed signal from the document or any descendant foreign document.
     */
    maybeEmitChanged() {
        if (this.value !== this.previousValue) {
            this._changed.emit(this);
        }
        this.previousValue = this.value;
        for (let document of this.foreignDocuments.values()) {
            document.maybeEmitChanged();
        }
    }
    /**
     * When this counter goes down to 0, the document will be destroyed and the associated connection will be closed;
     * This is meant to reduce the number of open connections when a foreign code snippet was removed from the document.
     *
     * Note: top level virtual documents are currently immortal (unless killed by other means); it might be worth
     * implementing culling of unused documents, but if and only if JupyterLab will also implement culling of
     * idle kernels - otherwise the user experience could be a bit inconsistent, and we would need to invent our own rules.
     */
    get remainingLifetime() {
        if (!this.parent) {
            return Infinity;
        }
        return this._remainingLifetime;
    }
    set remainingLifetime(value) {
        if (this.parent) {
            this._remainingLifetime = value;
        }
    }
    /**
     * Get the foreign document that can be opened with the input extractor.
     */
    chooseForeignDocument(extractor) {
        let foreignDocument;
        // if not standalone, try to append to existing document
        let foreignExists = this.foreignDocuments.has(extractor.language);
        if (!extractor.standalone && foreignExists) {
            foreignDocument = this.foreignDocuments.get(extractor.language);
        }
        else {
            // if (previous document does not exists) or (extractor produces standalone documents
            // and no old standalone document could be reused): create a new document
            foreignDocument = this.openForeign(extractor.language, extractor.standalone, extractor.fileExtension);
        }
        return foreignDocument;
    }
    /**
     * Create a foreign document from input language and file extension.
     *
     * @param  language - the required language
     * @param  standalone - the document type is supported natively by LSP?
     * @param  fileExtension - File extension.
     */
    openForeign(language, standalone, fileExtension) {
        let document = new VirtualDocument({
            ...this.options,
            parent: this,
            standalone: standalone,
            fileExtension: fileExtension,
            language: language
        });
        const context = {
            foreignDocument: document,
            parentHost: this
        };
        this._foreignDocumentOpened.emit(context);
        // pass through any future signals
        document.foreignDocumentClosed.connect(this.forwardClosedSignal, this);
        document.foreignDocumentOpened.connect(this.forwardOpenedSignal, this);
        this.foreignDocuments.set(document.virtualId, document);
        return document;
    }
    /**
     * Forward the closed signal from the foreign document to the host document's
     * signal
     */
    forwardClosedSignal(host, context) {
        this._foreignDocumentClosed.emit(context);
    }
    /**
     * Forward the opened signal from the foreign document to the host document's
     * signal
     */
    forwardOpenedSignal(host, context) {
        this._foreignDocumentOpened.emit(context);
    }
    /**
     * Slot of the `updateBegan` signal.
     */
    _updateBeganSlot() {
        this._editorToSourceLineNew = new Map();
    }
    /**
     * Slot of the `blockAdded` signal.
     */
    _blockAddedSlot(updateManager, blockData) {
        this._editorToSourceLineNew.set(blockData.block.ceEditor, blockData.virtualDocument.lastSourceLine);
    }
    /**
     * Slot of the `updateFinished` signal.
     */
    _updateFinishedSlot() {
        this._editorToSourceLine = this._editorToSourceLineNew;
    }
}
VirtualDocument.instancesCount = 0;

/**
 * Create foreign documents if available from input virtual documents.
 * @param virtualDocument - the virtual document to be collected
 * @return - Set of generated foreign documents
 */
function collectDocuments(virtualDocument) {
    let collected = new Set();
    collected.add(virtualDocument);
    for (let foreign of virtualDocument.foreignDocuments.values()) {
        let foreignLanguages = collectDocuments(foreign);
        foreignLanguages.forEach(collected.add, collected);
    }
    return collected;
}
class UpdateManager {
    constructor(virtualDocument) {
        this.virtualDocument = virtualDocument;
        this._isDisposed = false;
        /**
         * Promise resolved when the updating process finishes.
         */
        this._updateDone = new Promise(resolve => {
            resolve();
        });
        /**
         * Virtual documents update guard.
         */
        this._isUpdateInProgress = false;
        /**
         * Update lock to prevent multiple updates are applied at the same time.
         */
        this._updateLock = false;
        this._blockAdded = new index_es6_js_.Signal(this);
        this._documentUpdated = new index_es6_js_.Signal(this);
        this._updateBegan = new index_es6_js_.Signal(this);
        this._updateFinished = new index_es6_js_.Signal(this);
        this.documentUpdated.connect(this._onUpdated, this);
    }
    /**
     * Promise resolved when the updating process finishes.
     */
    get updateDone() {
        return this._updateDone;
    }
    /**
     * Test whether the document is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Signal emitted when a code block is added to the document.
     */
    get blockAdded() {
        return this._blockAdded;
    }
    /**
     * Signal emitted by the editor that triggered the update,
     * providing the root document of the updated documents.
     */
    get documentUpdated() {
        return this._documentUpdated;
    }
    /**
     * Signal emitted when the update is started
     */
    get updateBegan() {
        return this._updateBegan;
    }
    /**
     * Signal emitted when the update is finished
     */
    get updateFinished() {
        return this._updateFinished;
    }
    /**
     * Dispose the class
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        this.documentUpdated.disconnect(this._onUpdated);
        index_es6_js_.Signal.clearData(this);
    }
    /**
     * Execute provided callback within an update-locked context, which guarantees that:
     *  - the previous updates must have finished before the callback call, and
     *  - no update will happen when executing the callback
     * @param fn - the callback to execute in update lock
     */
    async withUpdateLock(fn) {
        await untilReady(() => this._canUpdate(), 12, 10).then(() => {
            try {
                this._updateLock = true;
                fn();
            }
            finally {
                this._updateLock = false;
            }
        });
    }
    /**
     * Update all the virtual documents, emit documents updated with root document if succeeded,
     * and resolve a void promise. The promise does not contain the text value of the root document,
     * as to avoid an easy trap of ignoring the changes in the virtual documents.
     */
    async updateDocuments(blocks) {
        let update = new Promise((resolve, reject) => {
            // defer the update by up to 50 ms (10 retrials * 5 ms break),
            // awaiting for the previous update to complete.
            untilReady(() => this._canUpdate(), 10, 5)
                .then(() => {
                if (this.isDisposed || !this.virtualDocument) {
                    resolve();
                }
                try {
                    this._isUpdateInProgress = true;
                    this._updateBegan.emit(blocks);
                    this.virtualDocument.clear();
                    for (let codeBlock of blocks) {
                        this._blockAdded.emit({
                            block: codeBlock,
                            virtualDocument: this.virtualDocument
                        });
                        this.virtualDocument.appendCodeBlock(codeBlock);
                    }
                    this._updateFinished.emit(blocks);
                    if (this.virtualDocument) {
                        this._documentUpdated.emit(this.virtualDocument);
                        this.virtualDocument.maybeEmitChanged();
                    }
                    resolve();
                }
                catch (e) {
                    console.warn('Documents update failed:', e);
                    reject(e);
                }
                finally {
                    this._isUpdateInProgress = false;
                }
            })
                .catch(console.error);
        });
        this._updateDone = update;
        return update;
    }
    /**
     * Once all the foreign documents were refreshed, the unused documents (and their connections)
     * should be terminated if their lifetime has expired.
     */
    _onUpdated(manager, rootDocument) {
        try {
            rootDocument.closeExpiredDocuments();
        }
        catch (e) {
            console.warn('Failed to close expired documents');
        }
    }
    /**
     * Check if the document can be updated.
     */
    _canUpdate() {
        return !this.isDisposed && !this._isUpdateInProgress && !this._updateLock;
    }
}

;// CONCATENATED MODULE: ../packages/lsp/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module lsp
 */












/***/ })

}]);
//# sourceMappingURL=9139.8cd36e28b46ff09bc07e.js.map?v=8cd36e28b46ff09bc07e