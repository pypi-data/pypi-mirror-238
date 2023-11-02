"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[2626],{

/***/ 52626:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "ABCWidgetFactory": () => (/* reexport */ ABCWidgetFactory),
  "Base64ModelFactory": () => (/* reexport */ Base64ModelFactory),
  "Context": () => (/* reexport */ Context),
  "DocumentModel": () => (/* reexport */ DocumentModel),
  "DocumentRegistry": () => (/* reexport */ DocumentRegistry),
  "DocumentWidget": () => (/* reexport */ DocumentWidget),
  "MimeContent": () => (/* reexport */ MimeContent),
  "MimeDocument": () => (/* reexport */ MimeDocument),
  "MimeDocumentFactory": () => (/* reexport */ MimeDocumentFactory),
  "TextModelFactory": () => (/* reexport */ TextModelFactory),
  "createReadonlyLabel": () => (/* reexport */ createReadonlyLabel)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var lib_index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/rendermime@~4.1.0-alpha.2 (singleton) (fallback: ../packages/rendermime/lib/index.js)
var rendermime_lib_index_js_ = __webpack_require__(66866);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @lumino/disposable@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/disposable/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(78612);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(30205);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var widgets_dist_index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/docregistry/lib/context.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








/**
 * An implementation of a document context.
 *
 * This class is typically instantiated by the document manager.
 */
class Context {
    /**
     * Construct a new document context.
     */
    constructor(options) {
        var _a, _b;
        this._isReady = false;
        this._isDisposed = false;
        this._isPopulated = false;
        this._path = '';
        this._lineEnding = null;
        this._contentsModel = null;
        this._populatedPromise = new dist_index_js_.PromiseDelegate();
        this._pathChanged = new dist_index_es6_js_.Signal(this);
        this._fileChanged = new dist_index_es6_js_.Signal(this);
        this._saveState = new dist_index_es6_js_.Signal(this);
        this._disposed = new dist_index_es6_js_.Signal(this);
        this._lastModifiedCheckMargin = 500;
        this._timeConflictModalIsOpen = false;
        const manager = (this._manager = options.manager);
        this.translator = options.translator || translation_lib_index_js_.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this._factory = options.factory;
        this._dialogs =
            (_a = options.sessionDialogs) !== null && _a !== void 0 ? _a : new index_js_.SessionContextDialogs({ translator: options.translator });
        this._opener = options.opener || Private.noOp;
        this._path = this._manager.contents.normalize(options.path);
        this._lastModifiedCheckMargin = options.lastModifiedCheckMargin || 500;
        const localPath = this._manager.contents.localPath(this._path);
        const lang = this._factory.preferredLanguage(lib_index_js_.PathExt.basename(localPath));
        const sharedFactory = this._manager.contents.getSharedModelFactory(this._path);
        const sharedModel = sharedFactory === null || sharedFactory === void 0 ? void 0 : sharedFactory.createNew({
            path: localPath,
            format: this._factory.fileFormat,
            contentType: this._factory.contentType,
            collaborative: this._factory.collaborative
        });
        this._model = this._factory.createNew({
            languagePreference: lang,
            sharedModel,
            collaborationEnabled: (_b = sharedFactory === null || sharedFactory === void 0 ? void 0 : sharedFactory.collaborative) !== null && _b !== void 0 ? _b : false
        });
        this._readyPromise = manager.ready.then(() => {
            return this._populatedPromise.promise;
        });
        const ext = lib_index_js_.PathExt.extname(this._path);
        this.sessionContext = new index_js_.SessionContext({
            sessionManager: manager.sessions,
            specsManager: manager.kernelspecs,
            path: localPath,
            type: ext === '.ipynb' ? 'notebook' : 'file',
            name: lib_index_js_.PathExt.basename(localPath),
            kernelPreference: options.kernelPreference || { shouldStart: false },
            setBusy: options.setBusy
        });
        this.sessionContext.propertyChanged.connect(this._onSessionChanged, this);
        manager.contents.fileChanged.connect(this._onFileChanged, this);
        this.urlResolver = new rendermime_lib_index_js_.RenderMimeRegistry.UrlResolver({
            path: this._path,
            contents: manager.contents
        });
    }
    /**
     * A signal emitted when the path changes.
     */
    get pathChanged() {
        return this._pathChanged;
    }
    /**
     * A signal emitted when the model is saved or reverted.
     */
    get fileChanged() {
        return this._fileChanged;
    }
    /**
     * A signal emitted on the start and end of a saving operation.
     */
    get saveState() {
        return this._saveState;
    }
    /**
     * A signal emitted when the context is disposed.
     */
    get disposed() {
        return this._disposed;
    }
    /**
     * Configurable margin used to detect document modification conflicts, in milliseconds
     */
    get lastModifiedCheckMargin() {
        return this._lastModifiedCheckMargin;
    }
    set lastModifiedCheckMargin(value) {
        this._lastModifiedCheckMargin = value;
    }
    /**
     * Get the model associated with the document.
     */
    get model() {
        return this._model;
    }
    /**
     * The current path associated with the document.
     */
    get path() {
        return this._path;
    }
    /**
     * The current local path associated with the document.
     * If the document is in the default notebook file browser,
     * this is the same as the path.
     */
    get localPath() {
        return this._manager.contents.localPath(this._path);
    }
    /**
     * The document metadata, stored as a services contents model.
     *
     * #### Notes
     * The contents model will be `null` until the context is populated.
     * It will not have a `content` field.
     */
    get contentsModel() {
        return this._contentsModel ? { ...this._contentsModel } : null;
    }
    /**
     * Get the model factory name.
     *
     * #### Notes
     * This is not part of the `IContext` API.
     */
    get factoryName() {
        return this.isDisposed ? '' : this._factory.name;
    }
    /**
     * Test whether the context is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the context.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this.sessionContext.dispose();
        this._model.dispose();
        // Ensure we dispose the `sharedModel` as it may have been generated in the context
        // through the shared model factory.
        this._model.sharedModel.dispose();
        this._disposed.emit(void 0);
        dist_index_es6_js_.Signal.clearData(this);
    }
    /**
     * Whether the context is ready.
     */
    get isReady() {
        return this._isReady;
    }
    /**
     * A promise that is fulfilled when the context is ready.
     */
    get ready() {
        return this._readyPromise;
    }
    /**
     * Whether the document can be saved via the Contents API.
     */
    get canSave() {
        var _a;
        return !!(((_a = this._contentsModel) === null || _a === void 0 ? void 0 : _a.writable) && !this._model.collaborative);
    }
    /**
     * Initialize the context.
     *
     * @param isNew - Whether it is a new file.
     *
     * @returns a promise that resolves upon initialization.
     */
    async initialize(isNew) {
        if (isNew) {
            await this._save();
        }
        else {
            await this._revert();
        }
        this.model.sharedModel.clearUndoHistory();
    }
    /**
     * Rename the document.
     *
     * @param newName - the new name for the document.
     */
    rename(newName) {
        return this.ready.then(() => {
            return this._manager.ready.then(() => {
                return this._rename(newName);
            });
        });
    }
    /**
     * Save the document contents to disk.
     */
    async save() {
        await this.ready;
        await this._save();
    }
    /**
     * Save the document to a different path chosen by the user.
     *
     * It will be rejected if the user abort providing a new path.
     */
    async saveAs() {
        await this.ready;
        const localPath = this._manager.contents.localPath(this.path);
        const newLocalPath = await Private.getSavePath(localPath);
        if (this.isDisposed || !newLocalPath) {
            return;
        }
        const drive = this._manager.contents.driveName(this.path);
        const newPath = drive == '' ? newLocalPath : `${drive}:${newLocalPath}`;
        if (newPath === this._path) {
            return this.save();
        }
        // Make sure the path does not exist.
        try {
            await this._manager.ready;
            await this._manager.contents.get(newPath);
            await this._maybeOverWrite(newPath);
        }
        catch (err) {
            if (!err.response || err.response.status !== 404) {
                throw err;
            }
            await this._finishSaveAs(newPath);
        }
    }
    /**
     * Download a file.
     *
     * @param path - The path of the file to be downloaded.
     *
     * @returns A promise which resolves when the file has begun
     *   downloading.
     */
    async download() {
        const url = await this._manager.contents.getDownloadUrl(this._path);
        const element = document.createElement('a');
        element.href = url;
        element.download = '';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
        return void 0;
    }
    /**
     * Revert the document contents to disk contents.
     */
    async revert() {
        await this.ready;
        await this._revert();
    }
    /**
     * Create a checkpoint for the file.
     */
    createCheckpoint() {
        const contents = this._manager.contents;
        return this._manager.ready.then(() => {
            return contents.createCheckpoint(this._path);
        });
    }
    /**
     * Delete a checkpoint for the file.
     */
    deleteCheckpoint(checkpointId) {
        const contents = this._manager.contents;
        return this._manager.ready.then(() => {
            return contents.deleteCheckpoint(this._path, checkpointId);
        });
    }
    /**
     * Restore the file to a known checkpoint state.
     */
    restoreCheckpoint(checkpointId) {
        const contents = this._manager.contents;
        const path = this._path;
        return this._manager.ready.then(() => {
            if (checkpointId) {
                return contents.restoreCheckpoint(path, checkpointId);
            }
            return this.listCheckpoints().then(checkpoints => {
                if (this.isDisposed || !checkpoints.length) {
                    return;
                }
                checkpointId = checkpoints[checkpoints.length - 1].id;
                return contents.restoreCheckpoint(path, checkpointId);
            });
        });
    }
    /**
     * List available checkpoints for a file.
     */
    listCheckpoints() {
        const contents = this._manager.contents;
        return this._manager.ready.then(() => {
            return contents.listCheckpoints(this._path);
        });
    }
    /**
     * Add a sibling widget to the document manager.
     *
     * @param widget - The widget to add to the document manager.
     *
     * @param options - The desired options for adding the sibling.
     *
     * @returns A disposable used to remove the sibling if desired.
     *
     * #### Notes
     * It is assumed that the widget has the same model and context
     * as the original widget.
     */
    addSibling(widget, options = {}) {
        const opener = this._opener;
        if (opener) {
            opener(widget, options);
        }
        return new index_es6_js_.DisposableDelegate(() => {
            widget.close();
        });
    }
    /**
     * Handle a change on the contents manager.
     */
    _onFileChanged(sender, change) {
        var _a;
        if (change.type !== 'rename') {
            return;
        }
        let oldPath = change.oldValue && change.oldValue.path;
        let newPath = change.newValue && change.newValue.path;
        if (newPath && this._path.indexOf(oldPath || '') === 0) {
            let changeModel = change.newValue;
            // When folder name changed, `oldPath` is `foo`, `newPath` is `bar` and `this._path` is `foo/test`,
            // we should update `foo/test` to `bar/test` as well
            if (oldPath !== this._path) {
                newPath = this._path.replace(new RegExp(`^${oldPath}/`), `${newPath}/`);
                oldPath = this._path;
                // Update client file model from folder change
                changeModel = {
                    last_modified: (_a = change.newValue) === null || _a === void 0 ? void 0 : _a.created,
                    path: newPath
                };
            }
            this._updateContentsModel({
                ...this._contentsModel,
                ...changeModel
            });
            this._updatePath(newPath);
        }
    }
    /**
     * Handle a change to a session property.
     */
    _onSessionChanged(sender, type) {
        if (type !== 'path') {
            return;
        }
        // The session uses local paths.
        // We need to convert it to a global path.
        const driveName = this._manager.contents.driveName(this.path);
        let newPath = this.sessionContext.session.path;
        if (driveName) {
            newPath = `${driveName}:${newPath}`;
        }
        this._updatePath(newPath);
    }
    /**
     * Update our contents model, without the content.
     */
    _updateContentsModel(model) {
        var _a, _b;
        const writable = model.writable && !this._model.collaborative;
        const newModel = {
            path: model.path,
            name: model.name,
            type: model.type,
            writable,
            created: model.created,
            last_modified: model.last_modified,
            mimetype: model.mimetype,
            format: model.format
        };
        const mod = (_b = (_a = this._contentsModel) === null || _a === void 0 ? void 0 : _a.last_modified) !== null && _b !== void 0 ? _b : null;
        this._contentsModel = newModel;
        if (!mod || newModel.last_modified !== mod) {
            this._fileChanged.emit(newModel);
        }
    }
    _updatePath(newPath) {
        var _a, _b, _c, _d;
        if (this._path === newPath) {
            return;
        }
        this._path = newPath;
        const localPath = this._manager.contents.localPath(newPath);
        const name = lib_index_js_.PathExt.basename(localPath);
        if (((_a = this.sessionContext.session) === null || _a === void 0 ? void 0 : _a.path) !== localPath) {
            void ((_b = this.sessionContext.session) === null || _b === void 0 ? void 0 : _b.setPath(localPath));
        }
        if (((_c = this.sessionContext.session) === null || _c === void 0 ? void 0 : _c.name) !== name) {
            void ((_d = this.sessionContext.session) === null || _d === void 0 ? void 0 : _d.setName(name));
        }
        if (this.urlResolver.path !== newPath) {
            this.urlResolver.path = newPath;
        }
        if (this._contentsModel &&
            (this._contentsModel.path !== newPath ||
                this._contentsModel.name !== name)) {
            const contentsModel = {
                ...this._contentsModel,
                name: name,
                path: newPath
            };
            this._updateContentsModel(contentsModel);
        }
        this._pathChanged.emit(newPath);
    }
    /**
     * Handle an initial population.
     */
    async _populate() {
        this._isPopulated = true;
        this._isReady = true;
        this._populatedPromise.resolve(void 0);
        // Add a checkpoint if none exists and the file is writable.
        await this._maybeCheckpoint(false);
        if (this.isDisposed) {
            return;
        }
        // Update the kernel preference.
        const name = this._model.defaultKernelName ||
            this.sessionContext.kernelPreference.name;
        this.sessionContext.kernelPreference = {
            ...this.sessionContext.kernelPreference,
            name,
            language: this._model.defaultKernelLanguage
        };
        // Note: we don't wait on the session to initialize
        // so that the user can be shown the content before
        // any kernel has started.
        void this.sessionContext.initialize().then(shouldSelect => {
            if (shouldSelect) {
                void this._dialogs.selectKernel(this.sessionContext);
            }
        });
    }
    /**
     * Rename the document.
     *
     * @param newName - the new name for the document.
     */
    async _rename(newName) {
        const splitPath = this.localPath.split('/');
        splitPath[splitPath.length - 1] = newName;
        let newPath = lib_index_js_.PathExt.join(...splitPath);
        const driveName = this._manager.contents.driveName(this.path);
        if (driveName) {
            newPath = `${driveName}:${newPath}`;
        }
        // rename triggers a fileChanged which updates the contents model
        await this._manager.contents.rename(this.path, newPath);
    }
    /**
     * Save the document contents to disk.
     */
    async _save() {
        this._saveState.emit('started');
        const options = this._createSaveOptions();
        try {
            await this._manager.ready;
            const value = await this._maybeSave(options);
            if (this.isDisposed) {
                return;
            }
            this._model.dirty = false;
            this._updateContentsModel(value);
            if (!this._isPopulated) {
                await this._populate();
            }
            // Emit completion.
            this._saveState.emit('completed');
        }
        catch (err) {
            // If the save has been canceled by the user, throw the error
            // so that whoever called save() can decide what to do.
            const { name } = err;
            if (name === 'ModalCancelError' || name === 'ModalDuplicateError') {
                throw err;
            }
            // Otherwise show an error message and throw the error.
            const localPath = this._manager.contents.localPath(this._path);
            const file = lib_index_js_.PathExt.basename(localPath);
            void this._handleError(err, this._trans.__('File Save Error for %1', file));
            // Emit failure.
            this._saveState.emit('failed');
            throw err;
        }
    }
    /**
     * Revert the document contents to disk contents.
     *
     * @param initializeModel - call the model's initialization function after
     * deserializing the content.
     */
    _revert(initializeModel = false) {
        const opts = {
            type: this._factory.contentType,
            content: this._factory.fileFormat !== null,
            ...(this._factory.fileFormat !== null
                ? { format: this._factory.fileFormat }
                : {})
        };
        const path = this._path;
        const model = this._model;
        return this._manager.ready
            .then(() => {
            return this._manager.contents.get(path, opts);
        })
            .then(contents => {
            if (this.isDisposed) {
                return;
            }
            if (contents.content) {
                if (contents.format === 'json') {
                    model.fromJSON(contents.content);
                }
                else {
                    let content = contents.content;
                    // Convert line endings if necessary, marking the file
                    // as dirty.
                    if (content.indexOf('\r\n') !== -1) {
                        this._lineEnding = '\r\n';
                        content = content.replace(/\r\n/g, '\n');
                    }
                    else if (content.indexOf('\r') !== -1) {
                        this._lineEnding = '\r';
                        content = content.replace(/\r/g, '\n');
                    }
                    else {
                        this._lineEnding = null;
                    }
                    model.fromString(content);
                }
            }
            this._updateContentsModel(contents);
            model.dirty = false;
            if (!this._isPopulated) {
                return this._populate();
            }
        })
            .catch(async (err) => {
            const localPath = this._manager.contents.localPath(this._path);
            const name = lib_index_js_.PathExt.basename(localPath);
            void this._handleError(err, this._trans.__('File Load Error for %1', name));
            throw err;
        });
    }
    /**
     * Save a file, dealing with conflicts.
     */
    _maybeSave(options) {
        const path = this._path;
        // Make sure the file has not changed on disk.
        const promise = this._manager.contents.get(path, { content: false });
        return promise.then(model => {
            var _a;
            if (this.isDisposed) {
                return Promise.reject(new Error('Disposed'));
            }
            // We want to check last_modified (disk) > last_modified (client)
            // (our last save)
            // In some cases the filesystem reports an inconsistent time, so we allow buffer when comparing.
            const lastModifiedCheckMargin = this._lastModifiedCheckMargin;
            const modified = (_a = this.contentsModel) === null || _a === void 0 ? void 0 : _a.last_modified;
            const tClient = modified ? new Date(modified) : new Date();
            const tDisk = new Date(model.last_modified);
            if (modified &&
                tDisk.getTime() - tClient.getTime() > lastModifiedCheckMargin) {
                return this._timeConflict(tClient, model, options);
            }
            return this._manager.contents.save(path, options);
        }, err => {
            if (err.response && err.response.status === 404) {
                return this._manager.contents.save(path, options);
            }
            throw err;
        });
    }
    /**
     * Handle a save/load error with a dialog.
     */
    async _handleError(err, title) {
        await (0,index_js_.showErrorMessage)(title, err);
        return;
    }
    /**
     * Add a checkpoint the file is writable.
     */
    _maybeCheckpoint(force) {
        let promise = Promise.resolve(void 0);
        if (!this.canSave) {
            return promise;
        }
        if (force) {
            promise = this.createCheckpoint().then( /* no-op */);
        }
        else {
            promise = this.listCheckpoints().then(checkpoints => {
                if (!this.isDisposed && !checkpoints.length && this.canSave) {
                    return this.createCheckpoint().then( /* no-op */);
                }
            });
        }
        return promise.catch(err => {
            // Handle a read-only folder.
            if (!err.response || err.response.status !== 403) {
                throw err;
            }
        });
    }
    /**
     * Handle a time conflict.
     */
    _timeConflict(tClient, model, options) {
        const tDisk = new Date(model.last_modified);
        console.warn(`Last saving performed ${tClient} ` +
            `while the current file seems to have been saved ` +
            `${tDisk}`);
        if (this._timeConflictModalIsOpen) {
            const error = new Error('Modal is already displayed');
            error.name = 'ModalDuplicateError';
            return Promise.reject(error);
        }
        const body = this._trans.__(`"%1" has changed on disk since the last time it was opened or saved.
Do you want to overwrite the file on disk with the version open here,
or load the version on disk (revert)?`, this.path);
        const revertBtn = index_js_.Dialog.okButton({
            label: this._trans.__('Revert'),
            actions: ['revert']
        });
        const overwriteBtn = index_js_.Dialog.warnButton({
            label: this._trans.__('Overwrite'),
            actions: ['overwrite']
        });
        this._timeConflictModalIsOpen = true;
        return (0,index_js_.showDialog)({
            title: this._trans.__('File Changed'),
            body,
            buttons: [index_js_.Dialog.cancelButton(), revertBtn, overwriteBtn]
        }).then(result => {
            this._timeConflictModalIsOpen = false;
            if (this.isDisposed) {
                return Promise.reject(new Error('Disposed'));
            }
            if (result.button.actions.includes('overwrite')) {
                return this._manager.contents.save(this._path, options);
            }
            if (result.button.actions.includes('revert')) {
                return this.revert().then(() => {
                    return model;
                });
            }
            const error = new Error('Cancel');
            error.name = 'ModalCancelError';
            return Promise.reject(error); // Otherwise cancel the save.
        });
    }
    /**
     * Handle a time conflict.
     */
    _maybeOverWrite(path) {
        const body = this._trans.__('"%1" already exists. Do you want to replace it?', path);
        const overwriteBtn = index_js_.Dialog.warnButton({
            label: this._trans.__('Overwrite'),
            accept: true
        });
        return (0,index_js_.showDialog)({
            title: this._trans.__('File Overwrite?'),
            body,
            buttons: [index_js_.Dialog.cancelButton(), overwriteBtn]
        }).then(result => {
            if (this.isDisposed) {
                return Promise.reject(new Error('Disposed'));
            }
            if (result.button.accept) {
                return this._manager.contents.delete(path).then(() => {
                    return this._finishSaveAs(path);
                });
            }
        });
    }
    /**
     * Finish a saveAs operation given a new path.
     */
    async _finishSaveAs(newPath) {
        this._saveState.emit('started');
        try {
            await this._manager.ready;
            const options = this._createSaveOptions();
            await this._manager.contents.save(newPath, options);
            await this._maybeCheckpoint(true);
            // Emit completion.
            this._saveState.emit('completed');
        }
        catch (err) {
            // If the save has been canceled by the user,
            // throw the error so that whoever called save()
            // can decide what to do.
            if (err.message === 'Cancel' ||
                err.message === 'Modal is already displayed') {
                throw err;
            }
            // Otherwise show an error message and throw the error.
            const localPath = this._manager.contents.localPath(this._path);
            const name = lib_index_js_.PathExt.basename(localPath);
            void this._handleError(err, this._trans.__('File Save Error for %1', name));
            // Emit failure.
            this._saveState.emit('failed');
            return;
        }
    }
    _createSaveOptions() {
        let content = null;
        if (this._factory.fileFormat === 'json') {
            content = this._model.toJSON();
        }
        else {
            content = this._model.toString();
            if (this._lineEnding) {
                content = content.replace(/\n/g, this._lineEnding);
            }
        }
        return {
            type: this._factory.contentType,
            format: this._factory.fileFormat,
            content
        };
    }
}
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * Get a new file path from the user.
     */
    function getSavePath(path, translator) {
        translator = translator || translation_lib_index_js_.nullTranslator;
        const trans = translator.load('jupyterlab');
        const saveBtn = index_js_.Dialog.okButton({ label: trans.__('Save'), accept: true });
        return (0,index_js_.showDialog)({
            title: trans.__('Save File As…'),
            body: new SaveWidget(path),
            buttons: [index_js_.Dialog.cancelButton(), saveBtn]
        }).then(result => {
            var _a;
            if (result.button.accept) {
                return (_a = result.value) !== null && _a !== void 0 ? _a : undefined;
            }
            return;
        });
    }
    Private.getSavePath = getSavePath;
    /**
     * A no-op function.
     */
    function noOp() {
        /* no-op */
    }
    Private.noOp = noOp;
    /*
     * A widget that gets a file path from a user.
     */
    class SaveWidget extends widgets_dist_index_es6_js_.Widget {
        /**
         * Construct a new save widget.
         */
        constructor(path) {
            super({ node: createSaveNode(path) });
        }
        /**
         * Get the value for the widget.
         */
        getValue() {
            return this.node.value;
        }
    }
    /**
     * Create the node for a save widget.
     */
    function createSaveNode(path) {
        const input = document.createElement('input');
        input.value = path;
        return input;
    }
})(Private || (Private = {}));

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/codeeditor@~4.1.0-alpha.2 (singleton) (fallback: ../packages/codeeditor/lib/index.js)
var codeeditor_lib_index_js_ = __webpack_require__(40200);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
;// CONCATENATED MODULE: ../packages/docregistry/lib/components.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */



/**
 * create readonly label toolbar item
 */
function createReadonlyLabel(panel, translator) {
    var _a;
    let trans = (translator !== null && translator !== void 0 ? translator : translation_lib_index_js_.nullTranslator).load('jupyterlab');
    return index_js_.ReactWidget.create(react_index_js_.createElement("div", null,
        react_index_js_.createElement("span", { className: "jp-ToolbarLabelComponent", title: trans.__(`Document is permissioned read-only; "save" is disabled, use "save as..." instead`) }, trans.__(`%1 is read-only`, (_a = panel.context.contentsModel) === null || _a === void 0 ? void 0 : _a.type))));
}

;// CONCATENATED MODULE: ../packages/docregistry/lib/default.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






/**
 * The default implementation of a document model.
 */
class DocumentModel extends codeeditor_lib_index_js_.CodeEditor.Model {
    /**
     * Construct a new document model.
     */
    constructor(options = {}) {
        var _a;
        super({ sharedModel: options.sharedModel });
        this._defaultLang = '';
        this._dirty = false;
        this._readOnly = false;
        this._contentChanged = new dist_index_es6_js_.Signal(this);
        this._stateChanged = new dist_index_es6_js_.Signal(this);
        this._defaultLang = (_a = options.languagePreference) !== null && _a !== void 0 ? _a : '';
        this._collaborationEnabled = !!options.collaborationEnabled;
        this.sharedModel.changed.connect(this._onStateChanged, this);
    }
    /**
     * A signal emitted when the document content changes.
     */
    get contentChanged() {
        return this._contentChanged;
    }
    /**
     * A signal emitted when the document state changes.
     */
    get stateChanged() {
        return this._stateChanged;
    }
    /**
     * The dirty state of the document.
     */
    get dirty() {
        return this._dirty;
    }
    set dirty(newValue) {
        const oldValue = this._dirty;
        if (newValue === oldValue) {
            return;
        }
        this._dirty = newValue;
        this.triggerStateChange({
            name: 'dirty',
            oldValue,
            newValue
        });
    }
    /**
     * The read only state of the document.
     */
    get readOnly() {
        return this._readOnly;
    }
    set readOnly(newValue) {
        if (newValue === this._readOnly) {
            return;
        }
        const oldValue = this._readOnly;
        this._readOnly = newValue;
        this.triggerStateChange({ name: 'readOnly', oldValue, newValue });
    }
    /**
     * The default kernel name of the document.
     *
     * #### Notes
     * This is a read-only property.
     */
    get defaultKernelName() {
        return '';
    }
    /**
     * The default kernel language of the document.
     *
     * #### Notes
     * This is a read-only property.
     */
    get defaultKernelLanguage() {
        return this._defaultLang;
    }
    /**
     * Whether the model is collaborative or not.
     */
    get collaborative() {
        return this._collaborationEnabled;
    }
    /**
     * Serialize the model to a string.
     */
    toString() {
        return this.sharedModel.getSource();
    }
    /**
     * Deserialize the model from a string.
     *
     * #### Notes
     * Should emit a [contentChanged] signal.
     */
    fromString(value) {
        this.sharedModel.setSource(value);
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        return JSON.parse(this.sharedModel.getSource() || 'null');
    }
    /**
     * Deserialize the model from JSON.
     *
     * #### Notes
     * Should emit a [contentChanged] signal.
     */
    fromJSON(value) {
        this.fromString(JSON.stringify(value));
    }
    /**
     * Initialize the model with its current state.
     */
    initialize() {
        return;
    }
    /**
     * Trigger a state change signal.
     */
    triggerStateChange(args) {
        this._stateChanged.emit(args);
    }
    /**
     * Trigger a content changed signal.
     */
    triggerContentChange() {
        this._contentChanged.emit(void 0);
        this.dirty = true;
    }
    _onStateChanged(sender, changes) {
        if (changes.sourceChange) {
            this.triggerContentChange();
        }
        if (changes.stateChange) {
            changes.stateChange.forEach(value => {
                if (value.name === 'dirty') {
                    // Setting `dirty` will trigger the state change.
                    // We always set `dirty` because the shared model state
                    // and the local attribute are synchronized one way shared model -> _dirty
                    this.dirty = value.newValue;
                }
                else if (value.oldValue !== value.newValue) {
                    this.triggerStateChange({
                        newValue: undefined,
                        oldValue: undefined,
                        ...value
                    });
                }
            });
        }
    }
}
/**
 * An implementation of a model factory for text files.
 */
class TextModelFactory {
    /**
     * Instantiates a TextModelFactory.
     */
    constructor(collaborative) {
        this._isDisposed = false;
        this._collaborative = collaborative !== null && collaborative !== void 0 ? collaborative : true;
    }
    /**
     * The name of the model type.
     *
     * #### Notes
     * This is a read-only property.
     */
    get name() {
        return 'text';
    }
    /**
     * The type of the file.
     *
     * #### Notes
     * This is a read-only property.
     */
    get contentType() {
        return 'file';
    }
    /**
     * The format of the file.
     *
     * This is a read-only property.
     */
    get fileFormat() {
        return 'text';
    }
    /**
     * Whether the model is collaborative or not.
     */
    get collaborative() {
        return this._collaborative;
    }
    /**
     * Get whether the model factory has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the model factory.
     */
    dispose() {
        this._isDisposed = true;
    }
    /**
     * Create a new model.
     *
     * @param options - Model options.
     *
     * @returns A new document model.
     */
    createNew(options = {}) {
        const collaborative = options.collaborationEnabled && this.collaborative;
        return new DocumentModel({
            ...options,
            collaborationEnabled: collaborative
        });
    }
    /**
     * Get the preferred kernel language given a file path.
     */
    preferredLanguage(path) {
        return '';
    }
}
/**
 * An implementation of a model factory for base64 files.
 */
class Base64ModelFactory extends TextModelFactory {
    /**
     * The name of the model type.
     *
     * #### Notes
     * This is a read-only property.
     */
    get name() {
        return 'base64';
    }
    /**
     * The type of the file.
     *
     * #### Notes
     * This is a read-only property.
     */
    get contentType() {
        return 'file';
    }
    /**
     * The format of the file.
     *
     * This is a read-only property.
     */
    get fileFormat() {
        return 'base64';
    }
}
/**
 * The default implementation of a widget factory.
 */
class ABCWidgetFactory {
    /**
     * Construct a new `ABCWidgetFactory`.
     */
    constructor(options) {
        this._isDisposed = false;
        this._widgetCreated = new dist_index_es6_js_.Signal(this);
        this._translator = options.translator || translation_lib_index_js_.nullTranslator;
        this._name = options.name;
        this._label = options.label || options.name;
        this._readOnly = options.readOnly === undefined ? false : options.readOnly;
        this._defaultFor = options.defaultFor ? options.defaultFor.slice() : [];
        this._defaultRendered = (options.defaultRendered || []).slice();
        this._fileTypes = options.fileTypes.slice();
        this._modelName = options.modelName || 'text';
        this._preferKernel = !!options.preferKernel;
        this._canStartKernel = !!options.canStartKernel;
        this._shutdownOnClose = !!options.shutdownOnClose;
        this._autoStartDefault = !!options.autoStartDefault;
        this._toolbarFactory = options.toolbarFactory;
    }
    /**
     * A signal emitted when a widget is created.
     */
    get widgetCreated() {
        return this._widgetCreated;
    }
    /**
     * Get whether the model factory has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources used by the document manager.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        dist_index_es6_js_.Signal.clearData(this);
    }
    /**
     * Whether the widget factory is read only.
     */
    get readOnly() {
        return this._readOnly;
    }
    /**
     * A unique name identifying of the widget.
     */
    get name() {
        return this._name;
    }
    /**
     * The label of the widget to display in dialogs.
     * If not given, name is used instead.
     */
    get label() {
        return this._label;
    }
    /**
     * The file types the widget can view.
     */
    get fileTypes() {
        return this._fileTypes.slice();
    }
    /**
     * The registered name of the model type used to create the widgets.
     */
    get modelName() {
        return this._modelName;
    }
    /**
     * The file types for which the factory should be the default.
     */
    get defaultFor() {
        return this._defaultFor.slice();
    }
    /**
     * The file types for which the factory should be the default for
     * rendering a document model, if different from editing.
     */
    get defaultRendered() {
        return this._defaultRendered.slice();
    }
    /**
     * Whether the widgets prefer having a kernel started.
     */
    get preferKernel() {
        return this._preferKernel;
    }
    /**
     * Whether the widgets can start a kernel when opened.
     */
    get canStartKernel() {
        return this._canStartKernel;
    }
    /**
     * The application language translator.
     */
    get translator() {
        return this._translator;
    }
    /**
     * Whether the kernel should be shutdown when the widget is closed.
     */
    get shutdownOnClose() {
        return this._shutdownOnClose;
    }
    set shutdownOnClose(value) {
        this._shutdownOnClose = value;
    }
    /**
     * Whether to automatically select the preferred kernel during a kernel start
     */
    get autoStartDefault() {
        return this._autoStartDefault;
    }
    set autoStartDefault(value) {
        this._autoStartDefault = value;
    }
    /**
     * Create a new widget given a document model and a context.
     *
     * #### Notes
     * It should emit the [widgetCreated] signal with the new widget.
     */
    createNew(context, source) {
        var _a;
        // Create the new widget
        const widget = this.createNewWidget(context, source);
        // Add toolbar
        (0,index_js_.setToolbar)(widget, (_a = this._toolbarFactory) !== null && _a !== void 0 ? _a : this.defaultToolbarFactory.bind(this));
        // Emit widget created signal
        this._widgetCreated.emit(widget);
        return widget;
    }
    /**
     * Default factory for toolbar items to be added after the widget is created.
     */
    defaultToolbarFactory(widget) {
        return [];
    }
}
/**
 * The class name added to a dirty widget.
 */
const DIRTY_CLASS = 'jp-mod-dirty';
/**
 * A document widget implementation.
 */
class DocumentWidget extends index_js_.MainAreaWidget {
    constructor(options) {
        var _a;
        // Include the context ready promise in the widget reveal promise
        options.reveal = Promise.all([options.reveal, options.context.ready]);
        super(options);
        this._trans = ((_a = options.translator) !== null && _a !== void 0 ? _a : translation_lib_index_js_.nullTranslator).load('jupyterlab');
        this.context = options.context;
        // Handle context path changes
        this.context.pathChanged.connect(this._onPathChanged, this);
        this._onPathChanged(this.context, this.context.path);
        // Listen for changes in the dirty state.
        this.context.model.stateChanged.connect(this._onModelStateChanged, this);
        void this.context.ready.then(() => {
            this._handleDirtyState();
        });
        // listen for changes to the title object
        this.title.changed.connect(this._onTitleChanged, this);
    }
    /**
     * Set URI fragment identifier.
     */
    setFragment(fragment) {
        /* no-op */
    }
    /**
     * Handle a title change.
     */
    async _onTitleChanged(_sender) {
        const validNameExp = /[\/\\:]/;
        const name = this.title.label;
        // Use localPath to avoid the drive name
        const filename = this.context.localPath.split('/').pop() || this.context.localPath;
        if (name === filename) {
            return;
        }
        if (name.length > 0 && !validNameExp.test(name)) {
            const oldPath = this.context.path;
            await this.context.rename(name);
            if (this.context.path !== oldPath) {
                // Rename succeeded
                return;
            }
        }
        // Reset title if name is invalid or rename fails
        this.title.label = filename;
    }
    /**
     * Handle a path change.
     */
    _onPathChanged(sender, path) {
        this.title.label = lib_index_js_.PathExt.basename(sender.localPath);
        // The document is not untitled any more.
        this.isUntitled = false;
    }
    /**
     * Handle a change to the context model state.
     */
    _onModelStateChanged(sender, args) {
        var _a;
        if (args.name === 'dirty') {
            this._handleDirtyState();
        }
        if (!this.context.model.dirty) {
            if (!this.context.model.collaborative) {
                if (!((_a = this.context.contentsModel) === null || _a === void 0 ? void 0 : _a.writable)) {
                    const readOnlyIndicator = createReadonlyLabel(this);
                    let roi = this.toolbar.insertBefore('kernelName', 'read-only-indicator', readOnlyIndicator);
                    if (!roi) {
                        this.toolbar.addItem('read-only-indicator', readOnlyIndicator);
                    }
                }
            }
        }
    }
    /**
     * Handle the dirty state of the context model.
     */
    _handleDirtyState() {
        if (this.context.model.dirty &&
            !this.title.className.includes(DIRTY_CLASS)) {
            this.title.className += ` ${DIRTY_CLASS}`;
        }
        else {
            this.title.className = this.title.className.replace(DIRTY_CLASS, '');
        }
    }
}

// EXTERNAL MODULE: consume shared module (default) @lumino/messaging@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/messaging/dist/index.es6.js)
var messaging_dist_index_es6_js_ = __webpack_require__(85755);
;// CONCATENATED MODULE: ../packages/docregistry/lib/mimedocument.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.









/**
 * A content widget for a rendered mimetype document.
 */
class MimeContent extends widgets_dist_index_es6_js_.Widget {
    /**
     * Construct a new widget.
     */
    constructor(options) {
        super();
        /**
         * A bound change callback.
         */
        this._changeCallback = (options) => {
            if (!options.data || !options.data[this.mimeType]) {
                return;
            }
            const data = options.data[this.mimeType];
            if (typeof data === 'string') {
                if (data !== this._context.model.toString()) {
                    this._context.model.fromString(data);
                }
            }
            else if (data !== null &&
                data !== undefined &&
                !dist_index_js_.JSONExt.deepEqual(data, this._context.model.toJSON())) {
                this._context.model.fromJSON(data);
            }
        };
        this._fragment = '';
        this._ready = new dist_index_js_.PromiseDelegate();
        this._isRendering = false;
        this._renderRequested = false;
        this.addClass('jp-MimeDocument');
        this.translator = options.translator || translation_lib_index_js_.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this.mimeType = options.mimeType;
        this._dataType = options.dataType || 'string';
        this._context = options.context;
        this.renderer = options.renderer;
        const layout = (this.layout = new widgets_dist_index_es6_js_.StackedLayout());
        layout.addWidget(this.renderer);
        this._context.ready
            .then(() => {
            return this._render();
        })
            .then(() => {
            // After rendering for the first time, send an activation request if we
            // are currently focused.
            if (this.node === document.activeElement) {
                // We want to synchronously send (not post) the activate message, while
                // we know this node still has focus.
                messaging_dist_index_es6_js_.MessageLoop.sendMessage(this.renderer, widgets_dist_index_es6_js_.Widget.Msg.ActivateRequest);
            }
            // Throttle the rendering rate of the widget.
            this._monitor = new lib_index_js_.ActivityMonitor({
                signal: this._context.model.contentChanged,
                timeout: options.renderTimeout
            });
            this._monitor.activityStopped.connect(this.update, this);
            this._ready.resolve(undefined);
        })
            .catch(reason => {
            // Dispose the document if rendering fails.
            requestAnimationFrame(() => {
                this.dispose();
            });
            void (0,index_js_.showErrorMessage)(this._trans.__('Renderer Failure: %1', this._context.path), reason);
        });
    }
    /**
     * Print method. Deferred to the renderer.
     */
    [index_js_.Printing.symbol]() {
        return index_js_.Printing.getPrintFunction(this.renderer);
    }
    /**
     * A promise that resolves when the widget is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * Set URI fragment identifier.
     */
    setFragment(fragment) {
        this._fragment = fragment;
        this.update();
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        if (this._monitor) {
            this._monitor.dispose();
        }
        this._monitor = null;
        super.dispose();
    }
    /**
     * Handle an `update-request` message to the widget.
     */
    onUpdateRequest(msg) {
        if (this._context.isReady) {
            void this._render();
            this._fragment = '';
        }
    }
    /**
     * Render the mime content.
     */
    async _render() {
        if (this.isDisposed) {
            return;
        }
        // Since rendering is async, we note render requests that happen while we
        // actually are rendering for a future rendering.
        if (this._isRendering) {
            this._renderRequested = true;
            return;
        }
        // Set up for this rendering pass.
        this._renderRequested = false;
        const context = this._context;
        const model = context.model;
        const data = {};
        if (this._dataType === 'string') {
            data[this.mimeType] = model.toString();
        }
        else {
            data[this.mimeType] = model.toJSON();
        }
        const mimeModel = new rendermime_lib_index_js_.MimeModel({
            data,
            callback: this._changeCallback,
            metadata: { fragment: this._fragment }
        });
        try {
            // Do the rendering asynchronously.
            this._isRendering = true;
            await this.renderer.renderModel(mimeModel);
            this._isRendering = false;
            // If there is an outstanding request to render, go ahead and render
            if (this._renderRequested) {
                return this._render();
            }
        }
        catch (reason) {
            // Dispose the document if rendering fails.
            requestAnimationFrame(() => {
                this.dispose();
            });
            void (0,index_js_.showErrorMessage)(this._trans.__('Renderer Failure: %1', context.path), reason);
        }
    }
}
/**
 * A document widget for mime content.
 */
class MimeDocument extends DocumentWidget {
    setFragment(fragment) {
        this.content.setFragment(fragment);
    }
}
/**
 * An implementation of a widget factory for a rendered mimetype document.
 */
class MimeDocumentFactory extends ABCWidgetFactory {
    /**
     * Construct a new mimetype widget factory.
     */
    constructor(options) {
        super(mimedocument_Private.createRegistryOptions(options));
        this._rendermime = options.rendermime;
        this._renderTimeout = options.renderTimeout || 1000;
        this._dataType = options.dataType || 'string';
        this._fileType = options.primaryFileType;
        this._factory = options.factory;
    }
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        var _a, _b;
        const ft = this._fileType;
        const mimeType = (ft === null || ft === void 0 ? void 0 : ft.mimeTypes.length)
            ? ft.mimeTypes[0]
            : codeeditor_lib_index_js_.IEditorMimeTypeService.defaultMimeType;
        const rendermime = this._rendermime.clone({
            resolver: context.urlResolver
        });
        let renderer;
        if (this._factory && this._factory.mimeTypes.includes(mimeType)) {
            renderer = this._factory.createRenderer({
                mimeType,
                resolver: rendermime.resolver,
                sanitizer: rendermime.sanitizer,
                linkHandler: rendermime.linkHandler,
                latexTypesetter: rendermime.latexTypesetter,
                markdownParser: rendermime.markdownParser
            });
        }
        else {
            renderer = rendermime.createRenderer(mimeType);
        }
        const content = new MimeContent({
            context,
            renderer,
            mimeType,
            renderTimeout: this._renderTimeout,
            dataType: this._dataType
        });
        content.title.icon = ft === null || ft === void 0 ? void 0 : ft.icon;
        content.title.iconClass = (_a = ft === null || ft === void 0 ? void 0 : ft.iconClass) !== null && _a !== void 0 ? _a : '';
        content.title.iconLabel = (_b = ft === null || ft === void 0 ? void 0 : ft.iconLabel) !== null && _b !== void 0 ? _b : '';
        const widget = new MimeDocument({ content, context });
        return widget;
    }
}
/**
 * The namespace for the module implementation details.
 */
var mimedocument_Private;
(function (Private) {
    /**
     * Create the document registry options.
     */
    function createRegistryOptions(options) {
        return {
            ...options,
            readOnly: true
        };
    }
    Private.createRegistryOptions = createRegistryOptions;
})(mimedocument_Private || (mimedocument_Private = {}));

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var algorithm_dist_index_es6_js_ = __webpack_require__(16415);
;// CONCATENATED MODULE: ../packages/docregistry/lib/registry.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/**
 * The document registry.
 */
class DocumentRegistry {
    /**
     * Construct a new document registry.
     */
    constructor(options = {}) {
        this._modelFactories = Object.create(null);
        this._widgetFactories = Object.create(null);
        this._defaultWidgetFactory = '';
        this._defaultWidgetFactoryOverrides = Object.create(null);
        this._defaultWidgetFactories = Object.create(null);
        this._defaultRenderedWidgetFactories = Object.create(null);
        this._widgetFactoriesForFileType = Object.create(null);
        this._fileTypes = [];
        this._extenders = Object.create(null);
        this._changed = new dist_index_es6_js_.Signal(this);
        this._isDisposed = false;
        const factory = options.textModelFactory;
        this.translator = options.translator || translation_lib_index_js_.nullTranslator;
        if (factory && factory.name !== 'text') {
            throw new Error('Text model factory must have the name `text`');
        }
        this._modelFactories['text'] = factory || new TextModelFactory(true);
        const fts = options.initialFileTypes ||
            DocumentRegistry.getDefaultFileTypes(this.translator);
        fts.forEach(ft => {
            const value = {
                ...DocumentRegistry.getFileTypeDefaults(this.translator),
                ...ft
            };
            this._fileTypes.push(value);
        });
    }
    /**
     * A signal emitted when the registry has changed.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Get whether the document registry has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the document registry.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        for (const modelName in this._modelFactories) {
            this._modelFactories[modelName].dispose();
        }
        for (const widgetName in this._widgetFactories) {
            this._widgetFactories[widgetName].dispose();
        }
        for (const widgetName in this._extenders) {
            this._extenders[widgetName].length = 0;
        }
        this._fileTypes.length = 0;
        dist_index_es6_js_.Signal.clearData(this);
    }
    /**
     * Add a widget factory to the registry.
     *
     * @param factory - The factory instance to register.
     *
     * @returns A disposable which will unregister the factory.
     *
     * #### Notes
     * If a factory with the given `'name'` is already registered,
     * a warning will be logged, and this will be a no-op.
     * If `'*'` is given as a default extension, the factory will be registered
     * as the global default.
     * If an extension or global default is already registered, this factory
     * will override the existing default.
     * The factory cannot be named an empty string or the string `'default'`.
     */
    addWidgetFactory(factory) {
        const name = factory.name.toLowerCase();
        if (!name || name === 'default') {
            throw Error('Invalid factory name');
        }
        if (this._widgetFactories[name]) {
            console.warn(`Duplicate registered factory ${name}`);
            return new index_es6_js_.DisposableDelegate(registry_Private.noOp);
        }
        this._widgetFactories[name] = factory;
        for (const ft of factory.defaultFor || []) {
            if (factory.fileTypes.indexOf(ft) === -1) {
                continue;
            }
            if (ft === '*') {
                this._defaultWidgetFactory = name;
            }
            else {
                this._defaultWidgetFactories[ft] = name;
            }
        }
        for (const ft of factory.defaultRendered || []) {
            if (factory.fileTypes.indexOf(ft) === -1) {
                continue;
            }
            this._defaultRenderedWidgetFactories[ft] = name;
        }
        // For convenience, store a mapping of file type name -> name
        for (const ft of factory.fileTypes) {
            if (!this._widgetFactoriesForFileType[ft]) {
                this._widgetFactoriesForFileType[ft] = [];
            }
            this._widgetFactoriesForFileType[ft].push(name);
        }
        this._changed.emit({
            type: 'widgetFactory',
            name,
            change: 'added'
        });
        return new index_es6_js_.DisposableDelegate(() => {
            delete this._widgetFactories[name];
            if (this._defaultWidgetFactory === name) {
                this._defaultWidgetFactory = '';
            }
            for (const ext of Object.keys(this._defaultWidgetFactories)) {
                if (this._defaultWidgetFactories[ext] === name) {
                    delete this._defaultWidgetFactories[ext];
                }
            }
            for (const ext of Object.keys(this._defaultRenderedWidgetFactories)) {
                if (this._defaultRenderedWidgetFactories[ext] === name) {
                    delete this._defaultRenderedWidgetFactories[ext];
                }
            }
            for (const ext of Object.keys(this._widgetFactoriesForFileType)) {
                algorithm_dist_index_es6_js_.ArrayExt.removeFirstOf(this._widgetFactoriesForFileType[ext], name);
                if (this._widgetFactoriesForFileType[ext].length === 0) {
                    delete this._widgetFactoriesForFileType[ext];
                }
            }
            for (const ext of Object.keys(this._defaultWidgetFactoryOverrides)) {
                if (this._defaultWidgetFactoryOverrides[ext] === name) {
                    delete this._defaultWidgetFactoryOverrides[ext];
                }
            }
            this._changed.emit({
                type: 'widgetFactory',
                name,
                change: 'removed'
            });
        });
    }
    /**
     * Add a model factory to the registry.
     *
     * @param factory - The factory instance.
     *
     * @returns A disposable which will unregister the factory.
     *
     * #### Notes
     * If a factory with the given `name` is already registered, or
     * the given factory is already registered, a warning will be logged
     * and this will be a no-op.
     */
    addModelFactory(factory) {
        const name = factory.name.toLowerCase();
        if (this._modelFactories[name]) {
            console.warn(`Duplicate registered factory ${name}`);
            return new index_es6_js_.DisposableDelegate(registry_Private.noOp);
        }
        this._modelFactories[name] = factory;
        this._changed.emit({
            type: 'modelFactory',
            name,
            change: 'added'
        });
        return new index_es6_js_.DisposableDelegate(() => {
            delete this._modelFactories[name];
            this._changed.emit({
                type: 'modelFactory',
                name,
                change: 'removed'
            });
        });
    }
    /**
     * Add a widget extension to the registry.
     *
     * @param widgetName - The name of the widget factory.
     *
     * @param extension - A widget extension.
     *
     * @returns A disposable which will unregister the extension.
     *
     * #### Notes
     * If the extension is already registered for the given
     * widget name, a warning will be logged and this will be a no-op.
     */
    addWidgetExtension(widgetName, extension) {
        widgetName = widgetName.toLowerCase();
        if (!(widgetName in this._extenders)) {
            this._extenders[widgetName] = [];
        }
        const extenders = this._extenders[widgetName];
        const index = algorithm_dist_index_es6_js_.ArrayExt.firstIndexOf(extenders, extension);
        if (index !== -1) {
            console.warn(`Duplicate registered extension for ${widgetName}`);
            return new index_es6_js_.DisposableDelegate(registry_Private.noOp);
        }
        this._extenders[widgetName].push(extension);
        this._changed.emit({
            type: 'widgetExtension',
            name: widgetName,
            change: 'added'
        });
        return new index_es6_js_.DisposableDelegate(() => {
            algorithm_dist_index_es6_js_.ArrayExt.removeFirstOf(this._extenders[widgetName], extension);
            this._changed.emit({
                type: 'widgetExtension',
                name: widgetName,
                change: 'removed'
            });
        });
    }
    /**
     * Add a file type to the document registry.
     *
     * @param fileType - The file type object to register.
     * @param factories - Optional factories to use for the file type.
     *
     * @returns A disposable which will unregister the command.
     *
     * #### Notes
     * These are used to populate the "Create New" dialog.
     *
     * If no default factory exists for the file type, the first factory will
     * be defined as default factory.
     */
    addFileType(fileType, factories) {
        const value = {
            ...DocumentRegistry.getFileTypeDefaults(this.translator),
            ...fileType,
            // fall back to fileIcon if needed
            ...(!(fileType.icon || fileType.iconClass) && { icon: ui_components_lib_index_js_.fileIcon })
        };
        this._fileTypes.push(value);
        // Add the filetype to the factory - filetype mapping
        //  We do not change the factory itself
        if (factories) {
            const fileTypeName = value.name.toLowerCase();
            factories
                .map(factory => factory.toLowerCase())
                .forEach(factory => {
                if (!this._widgetFactoriesForFileType[fileTypeName]) {
                    this._widgetFactoriesForFileType[fileTypeName] = [];
                }
                if (!this._widgetFactoriesForFileType[fileTypeName].includes(factory)) {
                    this._widgetFactoriesForFileType[fileTypeName].push(factory);
                }
            });
            if (!this._defaultWidgetFactories[fileTypeName]) {
                this._defaultWidgetFactories[fileTypeName] =
                    this._widgetFactoriesForFileType[fileTypeName][0];
            }
        }
        this._changed.emit({
            type: 'fileType',
            name: value.name,
            change: 'added'
        });
        return new index_es6_js_.DisposableDelegate(() => {
            algorithm_dist_index_es6_js_.ArrayExt.removeFirstOf(this._fileTypes, value);
            if (factories) {
                const fileTypeName = value.name.toLowerCase();
                for (const name of factories.map(factory => factory.toLowerCase())) {
                    algorithm_dist_index_es6_js_.ArrayExt.removeFirstOf(this._widgetFactoriesForFileType[fileTypeName], name);
                }
                if (this._defaultWidgetFactories[fileTypeName] ===
                    factories[0].toLowerCase()) {
                    delete this._defaultWidgetFactories[fileTypeName];
                }
            }
            this._changed.emit({
                type: 'fileType',
                name: fileType.name,
                change: 'removed'
            });
        });
    }
    /**
     * Get a list of the preferred widget factories.
     *
     * @param path - The file path to filter the results.
     *
     * @returns A new array of widget factories.
     *
     * #### Notes
     * Only the widget factories whose associated model factory have
     * been registered will be returned.
     * The first item is considered the default. The returned array
     * has widget factories in the following order:
     * - path-specific default factory
     * - path-specific default rendered factory
     * - global default factory
     * - all other path-specific factories
     * - all other global factories
     */
    preferredWidgetFactories(path) {
        const factories = new Set();
        // Get the ordered matching file types.
        const fts = this.getFileTypesForPath(lib_index_js_.PathExt.basename(path));
        // Start with any user overrides for the defaults.
        fts.forEach(ft => {
            if (ft.name in this._defaultWidgetFactoryOverrides) {
                factories.add(this._defaultWidgetFactoryOverrides[ft.name]);
            }
        });
        // Next add the file type default factories.
        fts.forEach(ft => {
            if (ft.name in this._defaultWidgetFactories) {
                factories.add(this._defaultWidgetFactories[ft.name]);
            }
        });
        // Add the file type default rendered factories.
        fts.forEach(ft => {
            if (ft.name in this._defaultRenderedWidgetFactories) {
                factories.add(this._defaultRenderedWidgetFactories[ft.name]);
            }
        });
        // Add the global default factory.
        if (this._defaultWidgetFactory) {
            factories.add(this._defaultWidgetFactory);
        }
        // Add the file type factories in registration order.
        for (const ft of fts) {
            if (ft.name in this._widgetFactoriesForFileType) {
                for (const n of this._widgetFactoriesForFileType[ft.name]) {
                    factories.add(n);
                }
            }
        }
        // Add the rest of the global factories, in registration order.
        if ('*' in this._widgetFactoriesForFileType) {
            for (const n of this._widgetFactoriesForFileType['*']) {
                factories.add(n);
            }
        }
        // Construct the return list, checking to make sure the corresponding
        // model factories are registered.
        const factoryList = [];
        for (const name of factories) {
            const factory = this._widgetFactories[name];
            if (!factory) {
                continue;
            }
            const modelName = factory.modelName || 'text';
            if (modelName in this._modelFactories) {
                factoryList.push(factory);
            }
        }
        return factoryList;
    }
    /**
     * Get the default rendered widget factory for a path.
     *
     * @param path - The path to for which to find a widget factory.
     *
     * @returns The default rendered widget factory for the path.
     *
     * ### Notes
     * If the widget factory has registered a separate set of `defaultRendered`
     * file types and there is a match in that set, this returns that.
     * Otherwise, this returns the same widget factory as
     * [[defaultWidgetFactory]].
     *
     * The user setting `defaultViewers` took precedence on this one too.
     */
    defaultRenderedWidgetFactory(path) {
        // Get the matching file types.
        const ftNames = this.getFileTypesForPath(lib_index_js_.PathExt.basename(path)).map(ft => ft.name);
        // Start with any user overrides for the defaults.
        for (const name in ftNames) {
            if (name in this._defaultWidgetFactoryOverrides) {
                return this._widgetFactories[this._defaultWidgetFactoryOverrides[name]];
            }
        }
        // Find if a there is a default rendered factory for this type.
        for (const name in ftNames) {
            if (name in this._defaultRenderedWidgetFactories) {
                return this._widgetFactories[this._defaultRenderedWidgetFactories[name]];
            }
        }
        // Fallback to the default widget factory
        return this.defaultWidgetFactory(path);
    }
    /**
     * Get the default widget factory for a path.
     *
     * @param path - An optional file path to filter the results.
     *
     * @returns The default widget factory for an path.
     *
     * #### Notes
     * This is equivalent to the first value in [[preferredWidgetFactories]].
     */
    defaultWidgetFactory(path) {
        if (!path) {
            return this._widgetFactories[this._defaultWidgetFactory];
        }
        return this.preferredWidgetFactories(path)[0];
    }
    /**
     * Set overrides for the default widget factory for a file type.
     *
     * Normally, a widget factory informs the document registry which file types
     * it should be the default for using the `defaultFor` option in the
     * IWidgetFactoryOptions. This function can be used to override that after
     * the fact.
     *
     * @param fileType: The name of the file type.
     *
     * @param factory: The name of the factory.
     *
     * #### Notes
     * If `factory` is undefined, then any override will be unset, and the
     * default factory will revert to the original value.
     *
     * If `factory` or `fileType` are not known to the docregistry, or
     * if `factory` cannot open files of type `fileType`, this will throw
     * an error.
     */
    setDefaultWidgetFactory(fileType, factory) {
        fileType = fileType.toLowerCase();
        if (!this.getFileType(fileType)) {
            throw Error(`Cannot find file type ${fileType}`);
        }
        if (!factory) {
            if (this._defaultWidgetFactoryOverrides[fileType]) {
                delete this._defaultWidgetFactoryOverrides[fileType];
            }
            return;
        }
        if (!this.getWidgetFactory(factory)) {
            throw Error(`Cannot find widget factory ${factory}`);
        }
        factory = factory.toLowerCase();
        const factories = this._widgetFactoriesForFileType[fileType];
        if (factory !== this._defaultWidgetFactory &&
            !(factories && factories.includes(factory))) {
            throw Error(`Factory ${factory} cannot view file type ${fileType}`);
        }
        this._defaultWidgetFactoryOverrides[fileType] = factory;
    }
    /**
     * Create an iterator over the widget factories that have been registered.
     *
     * @returns A new iterator of widget factories.
     */
    *widgetFactories() {
        for (const name in this._widgetFactories) {
            yield this._widgetFactories[name];
        }
    }
    /**
     * Create an iterator over the model factories that have been registered.
     *
     * @returns A new iterator of model factories.
     */
    *modelFactories() {
        for (const name in this._modelFactories) {
            yield this._modelFactories[name];
        }
    }
    /**
     * Create an iterator over the registered extensions for a given widget.
     *
     * @param widgetName - The name of the widget factory.
     *
     * @returns A new iterator over the widget extensions.
     */
    *widgetExtensions(widgetName) {
        widgetName = widgetName.toLowerCase();
        if (widgetName in this._extenders) {
            for (const extension of this._extenders[widgetName]) {
                yield extension;
            }
        }
    }
    /**
     * Create an iterator over the file types that have been registered.
     *
     * @returns A new iterator of file types.
     */
    *fileTypes() {
        for (const type of this._fileTypes) {
            yield type;
        }
    }
    /**
     * Get a widget factory by name.
     *
     * @param widgetName - The name of the widget factory.
     *
     * @returns A widget factory instance.
     */
    getWidgetFactory(widgetName) {
        return this._widgetFactories[widgetName.toLowerCase()];
    }
    /**
     * Get a model factory by name.
     *
     * @param name - The name of the model factory.
     *
     * @returns A model factory instance.
     */
    getModelFactory(name) {
        return this._modelFactories[name.toLowerCase()];
    }
    /**
     * Get a file type by name.
     */
    getFileType(name) {
        name = name.toLowerCase();
        return (0,algorithm_dist_index_es6_js_.find)(this._fileTypes, fileType => {
            return fileType.name.toLowerCase() === name;
        });
    }
    /**
     * Get a kernel preference.
     *
     * @param path - The file path.
     *
     * @param widgetName - The name of the widget factory.
     *
     * @param kernel - An optional existing kernel model.
     *
     * @returns A kernel preference.
     */
    getKernelPreference(path, widgetName, kernel) {
        widgetName = widgetName.toLowerCase();
        const widgetFactory = this._widgetFactories[widgetName];
        if (!widgetFactory) {
            return void 0;
        }
        const modelFactory = this.getModelFactory(widgetFactory.modelName || 'text');
        if (!modelFactory) {
            return void 0;
        }
        const language = modelFactory.preferredLanguage(lib_index_js_.PathExt.basename(path));
        const name = kernel && kernel.name;
        const id = kernel && kernel.id;
        return {
            id,
            name,
            language,
            shouldStart: widgetFactory.preferKernel,
            canStart: widgetFactory.canStartKernel,
            shutdownOnDispose: widgetFactory.shutdownOnClose,
            autoStartDefault: widgetFactory.autoStartDefault
        };
    }
    /**
     * Get the best file type given a contents model.
     *
     * @param model - The contents model of interest.
     *
     * @returns The best matching file type.
     */
    getFileTypeForModel(model) {
        switch (model.type) {
            case 'directory':
                return ((0,algorithm_dist_index_es6_js_.find)(this._fileTypes, ft => ft.contentType === 'directory') ||
                    DocumentRegistry.getDefaultDirectoryFileType(this.translator));
            case 'notebook':
                return ((0,algorithm_dist_index_es6_js_.find)(this._fileTypes, ft => ft.contentType === 'notebook') ||
                    DocumentRegistry.getDefaultNotebookFileType(this.translator));
            default:
                // Find the best matching extension.
                if (model.name || model.path) {
                    const name = model.name || lib_index_js_.PathExt.basename(model.path);
                    const fts = this.getFileTypesForPath(name);
                    if (fts.length > 0) {
                        return fts[0];
                    }
                }
                return (this.getFileType('text') ||
                    DocumentRegistry.getDefaultTextFileType(this.translator));
        }
    }
    /**
     * Get the file types that match a file name.
     *
     * @param path - The path of the file.
     *
     * @returns An ordered list of matching file types.
     */
    getFileTypesForPath(path) {
        const fts = [];
        const name = lib_index_js_.PathExt.basename(path);
        // Look for a pattern match first.
        let ft = (0,algorithm_dist_index_es6_js_.find)(this._fileTypes, ft => {
            return !!(ft.pattern && name.match(ft.pattern) !== null);
        });
        if (ft) {
            fts.push(ft);
        }
        // Then look by extension name, starting with the longest
        let ext = registry_Private.extname(name);
        while (ext.length > 1) {
            const ftSubset = this._fileTypes.filter(ft => 
            // In Private.extname, the extension is transformed to lower case
            ft.extensions.map(extension => extension.toLowerCase()).includes(ext));
            fts.push(...ftSubset);
            ext = '.' + ext.split('.').slice(2).join('.');
        }
        return fts;
    }
}
/**
 * The namespace for the `DocumentRegistry` class statics.
 */
(function (DocumentRegistry) {
    /**
     * The defaults used for a file type.
     *
     * @param translator - The application language translator.
     *
     * @returns The default file type.
     */
    function getFileTypeDefaults(translator) {
        translator = translator || translation_lib_index_js_.nullTranslator;
        const trans = translator === null || translator === void 0 ? void 0 : translator.load('jupyterlab');
        return {
            name: 'default',
            displayName: trans.__('default'),
            extensions: [],
            mimeTypes: [],
            contentType: 'file',
            fileFormat: 'text'
        };
    }
    DocumentRegistry.getFileTypeDefaults = getFileTypeDefaults;
    /**
     * The default text file type used by the document registry.
     *
     * @param translator - The application language translator.
     *
     * @returns The default text file type.
     */
    function getDefaultTextFileType(translator) {
        translator = translator || translation_lib_index_js_.nullTranslator;
        const trans = translator === null || translator === void 0 ? void 0 : translator.load('jupyterlab');
        const fileTypeDefaults = getFileTypeDefaults(translator);
        return {
            ...fileTypeDefaults,
            name: 'text',
            displayName: trans.__('Text'),
            mimeTypes: ['text/plain'],
            extensions: ['.txt'],
            icon: ui_components_lib_index_js_.fileIcon
        };
    }
    DocumentRegistry.getDefaultTextFileType = getDefaultTextFileType;
    /**
     * The default notebook file type used by the document registry.
     *
     * @param translator - The application language translator.
     *
     * @returns The default notebook file type.
     */
    function getDefaultNotebookFileType(translator) {
        translator = translator || translation_lib_index_js_.nullTranslator;
        const trans = translator === null || translator === void 0 ? void 0 : translator.load('jupyterlab');
        return {
            ...getFileTypeDefaults(translator),
            name: 'notebook',
            displayName: trans.__('Notebook'),
            mimeTypes: ['application/x-ipynb+json'],
            extensions: ['.ipynb'],
            contentType: 'notebook',
            fileFormat: 'json',
            icon: ui_components_lib_index_js_.notebookIcon
        };
    }
    DocumentRegistry.getDefaultNotebookFileType = getDefaultNotebookFileType;
    /**
     * The default directory file type used by the document registry.
     *
     * @param translator - The application language translator.
     *
     * @returns The default directory file type.
     */
    function getDefaultDirectoryFileType(translator) {
        translator = translator || translation_lib_index_js_.nullTranslator;
        const trans = translator === null || translator === void 0 ? void 0 : translator.load('jupyterlab');
        return {
            ...getFileTypeDefaults(translator),
            name: 'directory',
            displayName: trans.__('Directory'),
            extensions: [],
            mimeTypes: ['text/directory'],
            contentType: 'directory',
            icon: ui_components_lib_index_js_.folderIcon
        };
    }
    DocumentRegistry.getDefaultDirectoryFileType = getDefaultDirectoryFileType;
    /**
     * The default file types used by the document registry.
     *
     * @param translator - The application language translator.
     *
     * @returns The default directory file types.
     */
    function getDefaultFileTypes(translator) {
        translator = translator || translation_lib_index_js_.nullTranslator;
        const trans = translator === null || translator === void 0 ? void 0 : translator.load('jupyterlab');
        return [
            getDefaultTextFileType(translator),
            getDefaultNotebookFileType(translator),
            getDefaultDirectoryFileType(translator),
            {
                name: 'markdown',
                displayName: trans.__('Markdown File'),
                extensions: ['.md'],
                mimeTypes: ['text/markdown'],
                icon: ui_components_lib_index_js_.markdownIcon
            },
            {
                name: 'PDF',
                displayName: trans.__('PDF File'),
                extensions: ['.pdf'],
                mimeTypes: ['application/pdf'],
                icon: ui_components_lib_index_js_.pdfIcon
            },
            {
                name: 'python',
                displayName: trans.__('Python File'),
                extensions: ['.py'],
                mimeTypes: ['text/x-python'],
                icon: ui_components_lib_index_js_.pythonIcon
            },
            {
                name: 'json',
                displayName: trans.__('JSON File'),
                extensions: ['.json'],
                mimeTypes: ['application/json'],
                icon: ui_components_lib_index_js_.jsonIcon
            },
            {
                name: 'jsonl',
                displayName: trans.__('JSONLines File'),
                extensions: ['.jsonl', '.ndjson'],
                mimeTypes: [
                    'text/jsonl',
                    'application/jsonl',
                    'application/json-lines'
                ],
                icon: ui_components_lib_index_js_.jsonIcon
            },
            {
                name: 'julia',
                displayName: trans.__('Julia File'),
                extensions: ['.jl'],
                mimeTypes: ['text/x-julia'],
                icon: ui_components_lib_index_js_.juliaIcon
            },
            {
                name: 'csv',
                displayName: trans.__('CSV File'),
                extensions: ['.csv'],
                mimeTypes: ['text/csv'],
                icon: ui_components_lib_index_js_.spreadsheetIcon
            },
            {
                name: 'tsv',
                displayName: trans.__('TSV File'),
                extensions: ['.tsv'],
                mimeTypes: ['text/csv'],
                icon: ui_components_lib_index_js_.spreadsheetIcon
            },
            {
                name: 'r',
                displayName: trans.__('R File'),
                mimeTypes: ['text/x-rsrc'],
                extensions: ['.R'],
                icon: ui_components_lib_index_js_.rKernelIcon
            },
            {
                name: 'yaml',
                displayName: trans.__('YAML File'),
                mimeTypes: ['text/x-yaml', 'text/yaml'],
                extensions: ['.yaml', '.yml'],
                icon: ui_components_lib_index_js_.yamlIcon
            },
            {
                name: 'svg',
                displayName: trans.__('Image'),
                mimeTypes: ['image/svg+xml'],
                extensions: ['.svg'],
                icon: ui_components_lib_index_js_.imageIcon,
                fileFormat: 'base64'
            },
            {
                name: 'tiff',
                displayName: trans.__('Image'),
                mimeTypes: ['image/tiff'],
                extensions: ['.tif', '.tiff'],
                icon: ui_components_lib_index_js_.imageIcon,
                fileFormat: 'base64'
            },
            {
                name: 'jpeg',
                displayName: trans.__('Image'),
                mimeTypes: ['image/jpeg'],
                extensions: ['.jpg', '.jpeg'],
                icon: ui_components_lib_index_js_.imageIcon,
                fileFormat: 'base64'
            },
            {
                name: 'gif',
                displayName: trans.__('Image'),
                mimeTypes: ['image/gif'],
                extensions: ['.gif'],
                icon: ui_components_lib_index_js_.imageIcon,
                fileFormat: 'base64'
            },
            {
                name: 'png',
                displayName: trans.__('Image'),
                mimeTypes: ['image/png'],
                extensions: ['.png'],
                icon: ui_components_lib_index_js_.imageIcon,
                fileFormat: 'base64'
            },
            {
                name: 'bmp',
                displayName: trans.__('Image'),
                mimeTypes: ['image/bmp'],
                extensions: ['.bmp'],
                icon: ui_components_lib_index_js_.imageIcon,
                fileFormat: 'base64'
            },
            {
                name: 'webp',
                displayName: trans.__('Image'),
                mimeTypes: ['image/webp'],
                extensions: ['.webp'],
                icon: ui_components_lib_index_js_.imageIcon,
                fileFormat: 'base64'
            }
        ];
    }
    DocumentRegistry.getDefaultFileTypes = getDefaultFileTypes;
})(DocumentRegistry || (DocumentRegistry = {}));
/**
 * A private namespace for DocumentRegistry data.
 */
var registry_Private;
(function (Private) {
    /**
     * Get the extension name of a path.
     *
     * @param path - string.
     *
     * #### Notes
     * Dotted filenames (e.g. `".table.json"` are allowed).
     */
    function extname(path) {
        const parts = lib_index_js_.PathExt.basename(path).split('.');
        parts.shift();
        const ext = '.' + parts.join('.');
        return ext.toLowerCase();
    }
    Private.extname = extname;
    /**
     * A no-op function.
     */
    function noOp() {
        /* no-op */
    }
    Private.noOp = noOp;
})(registry_Private || (registry_Private = {}));

;// CONCATENATED MODULE: ../packages/docregistry/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module docregistry
 */







/***/ })

}]);
//# sourceMappingURL=2626.101b8afad9db26cbb6c7.js.map?v=101b8afad9db26cbb6c7