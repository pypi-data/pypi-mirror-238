"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[7748],{

/***/ 97748:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "CONTEXT_PROVIDER_ID": () => (/* reexport */ CONTEXT_PROVIDER_ID),
  "Completer": () => (/* reexport */ Completer),
  "CompleterModel": () => (/* reexport */ CompleterModel),
  "CompletionHandler": () => (/* reexport */ CompletionHandler),
  "CompletionProviderManager": () => (/* reexport */ CompletionProviderManager),
  "CompletionTriggerKind": () => (/* reexport */ CompletionTriggerKind),
  "ContextCompleterProvider": () => (/* reexport */ ContextCompleterProvider),
  "ICompletionProviderManager": () => (/* reexport */ ICompletionProviderManager),
  "KERNEL_PROVIDER_ID": () => (/* reexport */ KERNEL_PROVIDER_ID),
  "KernelCompleterProvider": () => (/* reexport */ KernelCompleterProvider),
  "ProviderReconciliator": () => (/* reexport */ ProviderReconciliator)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: consume shared module (default) @lumino/messaging@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/messaging/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(85755);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(30205);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
;// CONCATENATED MODULE: ../packages/completer/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The type of completion request.
 */
var CompletionTriggerKind;
(function (CompletionTriggerKind) {
    CompletionTriggerKind[CompletionTriggerKind["Invoked"] = 1] = "Invoked";
    CompletionTriggerKind[CompletionTriggerKind["TriggerCharacter"] = 2] = "TriggerCharacter";
    CompletionTriggerKind[CompletionTriggerKind["TriggerForIncompleteCompletions"] = 3] = "TriggerForIncompleteCompletions";
})(CompletionTriggerKind || (CompletionTriggerKind = {}));
/**
 * The exported token used to register new provider.
 */
const ICompletionProviderManager = new dist_index_js_.Token('@jupyterlab/completer:ICompletionProviderManager', 'A service for the completion providers management.');

;// CONCATENATED MODULE: ../packages/completer/lib/handler.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * A class added to editors that can host a completer.
 */
const COMPLETER_ENABLED_CLASS = 'jp-mod-completer-enabled';
/**
 * A class added to editors that have an active completer.
 */
const COMPLETER_ACTIVE_CLASS = 'jp-mod-completer-active';
/**
 * A completion handler for editors.
 */
class CompletionHandler {
    /**
     * Construct a new completion handler for a widget.
     */
    constructor(options) {
        this._editor = null;
        this._enabled = false;
        this._isDisposed = false;
        this._autoCompletion = false;
        this.completer = options.completer;
        this.completer.selected.connect(this.onCompletionSelected, this);
        this.completer.visibilityChanged.connect(this.onVisibilityChanged, this);
        this._reconciliator = options.reconciliator;
    }
    set reconciliator(reconciliator) {
        this._reconciliator = reconciliator;
    }
    /**
     * The editor used by the completion handler.
     */
    get editor() {
        return this._editor;
    }
    set editor(newValue) {
        if (newValue === this._editor) {
            return;
        }
        let editor = this._editor;
        // Clean up and disconnect from old editor.
        if (editor && !editor.isDisposed) {
            const model = editor.model;
            editor.host.classList.remove(COMPLETER_ENABLED_CLASS);
            editor.host.classList.remove(COMPLETER_ACTIVE_CLASS);
            model.selections.changed.disconnect(this.onSelectionsChanged, this);
            model.sharedModel.changed.disconnect(this.onTextChanged, this);
        }
        // Reset completer state.
        this.completer.reset();
        this.completer.editor = newValue;
        // Update the editor and signal connections.
        editor = this._editor = newValue;
        if (editor) {
            const model = editor.model;
            this._enabled = false;
            model.selections.changed.connect(this.onSelectionsChanged, this);
            model.sharedModel.changed.connect(this.onTextChanged, this);
            // On initial load, manually check the cursor position.
            this.onSelectionsChanged();
        }
    }
    /**
     * Get whether the completion handler is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Enable/disable continuous hinting mode.
     */
    set autoCompletion(value) {
        this._autoCompletion = value;
    }
    get autoCompletion() {
        return this._autoCompletion;
    }
    /**
     * Dispose of the resources used by the handler.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        dist_index_es6_js_.Signal.clearData(this);
    }
    /**
     * Invoke the handler and launch a completer.
     */
    invoke() {
        index_es6_js_.MessageLoop.sendMessage(this, CompletionHandler.Msg.InvokeRequest);
    }
    /**
     * Process a message sent to the completion handler.
     */
    processMessage(msg) {
        switch (msg.type) {
            case CompletionHandler.Msg.InvokeRequest.type:
                this.onInvokeRequest(msg);
                break;
            default:
                break;
        }
    }
    /**
     * Get the state of the text editor at the given position.
     */
    getState(editor, position) {
        return {
            text: editor.model.sharedModel.getSource(),
            line: position.line,
            column: position.column
        };
    }
    /**
     * Handle a completion selected signal from the completion widget.
     */
    onCompletionSelected(completer, val) {
        const model = completer.model;
        const editor = this._editor;
        if (!editor || !model) {
            return;
        }
        const patch = model.createPatch(val);
        if (!patch) {
            return;
        }
        const { start, end, value } = patch;
        const cursorBeforeChange = editor.getOffsetAt(editor.getCursorPosition());
        // we need to update the shared model in a single transaction so that the undo manager works as expected
        editor.model.sharedModel.updateSource(start, end, value);
        if (cursorBeforeChange <= end && cursorBeforeChange >= start) {
            editor.setCursorPosition(editor.getPositionAt(start + value.length));
        }
    }
    /**
     * Handle `invoke-request` messages.
     */
    onInvokeRequest(msg) {
        // If there is no completer model, bail.
        if (!this.completer.model) {
            return;
        }
        // If a completer session is already active, bail.
        if (this.completer.model.original) {
            return;
        }
        const editor = this._editor;
        if (editor) {
            this._makeRequest(editor.getCursorPosition(), CompletionTriggerKind.Invoked).catch(reason => {
                console.warn('Invoke request bailed', reason);
            });
        }
    }
    /**
     * Handle selection changed signal from an editor.
     *
     * #### Notes
     * If a sub-class reimplements this method, then that class must either call
     * its super method or it must take responsibility for adding and removing
     * the completer completable class to the editor host node.
     *
     * Despite the fact that the editor widget adds a class whenever there is a
     * primary selection, this method checks independently for two reasons:
     *
     * 1. The editor widget connects to the same signal to add that class, so
     *    there is no guarantee that the class will be added before this method
     *    is invoked so simply checking for the CSS class's existence is not an
     *    option. Secondarily, checking the editor state should be faster than
     *    querying the DOM in either case.
     * 2. Because this method adds a class that indicates whether completer
     *    functionality ought to be enabled, relying on the behavior of the
     *    `jp-mod-has-primary-selection` to filter out any editors that have
     *    a selection means the semantic meaning of `jp-mod-completer-enabled`
     *    is obscured because there may be cases where the enabled class is added
     *    even though the completer is not available.
     */
    onSelectionsChanged() {
        const model = this.completer.model;
        const editor = this._editor;
        if (!editor) {
            return;
        }
        const host = editor.host;
        // If there is no model, return.
        if (!model) {
            this._enabled = false;
            host.classList.remove(COMPLETER_ENABLED_CLASS);
            return;
        }
        // If we are currently performing a subset match,
        // return without resetting the completer.
        if (model.subsetMatch) {
            return;
        }
        const position = editor.getCursorPosition();
        const line = editor.getLine(position.line);
        if (!line) {
            this._enabled = false;
            model.reset(true);
            host.classList.remove(COMPLETER_ENABLED_CLASS);
            return;
        }
        const { start, end } = editor.getSelection();
        // If there is a text selection, return.
        if (start.column !== end.column || start.line !== end.line) {
            this._enabled = false;
            model.reset(true);
            host.classList.remove(COMPLETER_ENABLED_CLASS);
            return;
        }
        // If the part of the line before the cursor is white space, return.
        if (line.slice(0, position.column).match(/^\s*$/)) {
            this._enabled = false;
            model.reset(true);
            host.classList.remove(COMPLETER_ENABLED_CLASS);
            return;
        }
        // Enable completion.
        if (!this._enabled) {
            this._enabled = true;
            host.classList.add(COMPLETER_ENABLED_CLASS);
        }
        // Dispatch the cursor change.
        model.handleCursorChange(this.getState(editor, editor.getCursorPosition()));
    }
    /**
     * Handle a text changed signal from an editor.
     */
    async onTextChanged(str, changed) {
        const model = this.completer.model;
        if (!model || !this._enabled) {
            return;
        }
        // If there is a text selection, no completion is allowed.
        const editor = this.editor;
        if (!editor) {
            return;
        }
        if (this._autoCompletion &&
            this._reconciliator.shouldShowContinuousHint &&
            (await this._reconciliator.shouldShowContinuousHint(this.completer.isVisible, changed))) {
            void this._makeRequest(editor.getCursorPosition(), CompletionTriggerKind.TriggerCharacter);
        }
        const { start, end } = editor.getSelection();
        if (start.column !== end.column || start.line !== end.line) {
            return;
        }
        // Dispatch the text change.
        model.handleTextChange(this.getState(editor, editor.getCursorPosition()));
    }
    /**
     * Handle a visibility change signal from a completer widget.
     */
    onVisibilityChanged(completer) {
        // Completer is not active.
        if (completer.isDisposed || completer.isHidden) {
            if (this._editor) {
                this._editor.host.classList.remove(COMPLETER_ACTIVE_CLASS);
                this._editor.focus();
            }
            return;
        }
        // Completer is active.
        if (this._editor) {
            this._editor.host.classList.add(COMPLETER_ACTIVE_CLASS);
        }
    }
    /**
     * Make a completion request.
     */
    _makeRequest(position, trigger) {
        const editor = this.editor;
        if (!editor) {
            return Promise.reject(new Error('No active editor'));
        }
        const text = editor.model.sharedModel.getSource();
        const offset = index_js_.Text.jsIndexToCharIndex(editor.getOffsetAt(position), text);
        const state = this.getState(editor, position);
        const request = { text, offset };
        return this._reconciliator
            .fetch(request, trigger)
            .then(reply => {
            if (!reply) {
                return;
            }
            const model = this._updateModel(state, reply.start, reply.end);
            if (!model) {
                return;
            }
            if (model.setCompletionItems) {
                model.setCompletionItems(reply.items);
            }
        })
            .catch(p => {
            /* Fails silently. */
        });
    }
    /**
     * Updates model with text state and current cursor position.
     */
    _updateModel(state, start, end) {
        const model = this.completer.model;
        const text = state.text;
        if (!model) {
            return null;
        }
        // Update the original request.
        model.original = state;
        // Update the cursor.
        model.cursor = {
            start: index_js_.Text.charIndexToJsIndex(start, text),
            end: index_js_.Text.charIndexToJsIndex(end, text)
        };
        return model;
    }
}
/**
 * A namespace for cell completion handler statics.
 */
(function (CompletionHandler) {
    /**
     * A namespace for completion handler messages.
     */
    let Msg;
    (function (Msg) {
        /**
         * A singleton `'invoke-request'` message.
         */
        Msg.InvokeRequest = new index_es6_js_.Message('invoke-request');
    })(Msg = CompletionHandler.Msg || (CompletionHandler.Msg = {}));
})(CompletionHandler || (CompletionHandler = {}));

// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var algorithm_dist_index_es6_js_ = __webpack_require__(16415);
;// CONCATENATED MODULE: ../packages/completer/lib/model.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * Escape HTML by native means of the browser.
 */
function escapeHTML(text) {
    const node = document.createElement('span');
    node.textContent = text;
    return node.innerHTML;
}
/**
 * An implementation of a completer model.
 */
class CompleterModel {
    constructor() {
        this.processedItemsCache = null;
        this._current = null;
        this._cursor = null;
        this._isDisposed = false;
        this._completionItems = [];
        this._original = null;
        this._query = '';
        this._subsetMatch = false;
        this._typeMap = {};
        this._orderedTypes = [];
        this._stateChanged = new dist_index_es6_js_.Signal(this);
        this._queryChanged = new dist_index_es6_js_.Signal(this);
        /**
         * The weak map between a processed completion item with the original item.
         * It's used to keep track of original completion item in case of displaying
         * the completer with query.
         */
        this._processedToOriginalItem = null;
        /**
         * A counter to cancel ongoing `resolveItem` call.
         */
        this._resolvingItem = 0;
    }
    /**
     * A signal emitted when state of the completer menu changes.
     */
    get stateChanged() {
        return this._stateChanged;
    }
    /**
     * A signal emitted when query string changes (at invocation, or as user types).
     */
    get queryChanged() {
        return this._queryChanged;
    }
    /**
     * The original completion request details.
     */
    get original() {
        return this._original;
    }
    set original(newValue) {
        const unchanged = this._original === newValue ||
            (this._original &&
                newValue &&
                dist_index_js_.JSONExt.deepEqual(newValue, this._original));
        if (unchanged) {
            return;
        }
        this._reset();
        // Set both the current and original to the same value when original is set.
        this._current = this._original = newValue;
        this._stateChanged.emit(undefined);
    }
    /**
     * The current text change details.
     */
    get current() {
        return this._current;
    }
    set current(newValue) {
        const unchanged = this._current === newValue ||
            (this._current && newValue && dist_index_js_.JSONExt.deepEqual(newValue, this._current));
        if (unchanged) {
            return;
        }
        const original = this._original;
        // Original request must always be set before a text change. If it isn't
        // the model fails silently.
        if (!original) {
            return;
        }
        const cursor = this._cursor;
        // Cursor must always be set before a text change. This happens
        // automatically in the completer handler, but since `current` is a public
        // attribute, this defensive check is necessary.
        if (!cursor) {
            return;
        }
        const current = (this._current = newValue);
        if (!current) {
            this._stateChanged.emit(undefined);
            return;
        }
        const originalLine = original.text.split('\n')[original.line];
        const currentLine = current.text.split('\n')[current.line];
        // If the text change means that the original start point has been preceded,
        // then the completion is no longer valid and should be reset.
        if (!this._subsetMatch && currentLine.length < originalLine.length) {
            this.reset(true);
            return;
        }
        const { start, end } = cursor;
        // Clip the front of the current line.
        let query = current.text.substring(start);
        // Clip the back of the current line by calculating the end of the original.
        const ending = original.text.substring(end);
        query = query.substring(0, query.lastIndexOf(ending));
        this._query = query;
        this.processedItemsCache = null;
        this._processedToOriginalItem = null;
        this._queryChanged.emit({ newValue: this._query, origin: 'editorUpdate' });
        this._stateChanged.emit(undefined);
    }
    /**
     * The cursor details that the API has used to return matching options.
     */
    get cursor() {
        return this._cursor;
    }
    set cursor(newValue) {
        // Original request must always be set before a cursor change. If it isn't
        // the model fails silently.
        if (!this.original) {
            return;
        }
        this._cursor = newValue;
    }
    /**
     * The query against which items are filtered.
     */
    get query() {
        return this._query;
    }
    set query(newValue) {
        this._query = newValue;
        this.processedItemsCache = null;
        this._processedToOriginalItem = null;
        this._queryChanged.emit({ newValue: this._query, origin: 'setter' });
    }
    /**
     * A flag that is true when the model value was modified by a subset match.
     */
    get subsetMatch() {
        return this._subsetMatch;
    }
    set subsetMatch(newValue) {
        this._subsetMatch = newValue;
    }
    /**
     * Get whether the model is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the model.
     */
    dispose() {
        // Do nothing if already disposed.
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        dist_index_es6_js_.Signal.clearData(this);
    }
    /**
     * The list of visible items in the completer menu.
     *
     * #### Notes
     * This is a read-only property.
     * When overriding it is recommended to cache results in `processedItemsCache`
     * property which will be automatically nullified when needed.
     */
    completionItems() {
        if (!this.processedItemsCache) {
            let query = this._query;
            if (query) {
                const markedItems = this._markup(query);
                this.processedItemsCache = markedItems.map(it => it.processedItem);
                this._processedToOriginalItem = new WeakMap(markedItems.map(it => [it.processedItem, it.originalItem]));
            }
            else {
                this.processedItemsCache = this._completionItems.map(item => {
                    return this._escapeItemLabel(item);
                });
                this._processedToOriginalItem = null;
            }
        }
        return this.processedItemsCache;
    }
    /**
     * Set the list of visible items in the completer menu, and append any
     * new types to KNOWN_TYPES.
     */
    setCompletionItems(newValue) {
        if (dist_index_js_.JSONExt.deepEqual(newValue, this._completionItems)) {
            return;
        }
        this._completionItems = newValue;
        this._orderedTypes = Private.findOrderedCompletionItemTypes(this._completionItems);
        this.processedItemsCache = null;
        this._processedToOriginalItem = null;
        this._stateChanged.emit(undefined);
    }
    /**
     * The map from identifiers (a.b) to types (function, module, class, instance,
     * etc.).
     *
     * #### Notes
     * A type map is currently only provided by the latest IPython kernel using
     * the completer reply metadata field `_jupyter_types_experimental`. The
     * values are completely up to the kernel.
     *
     */
    typeMap() {
        return this._typeMap;
    }
    /**
     * An ordered list of all the known types in the typeMap.
     *
     * #### Notes
     * To visually encode the types of the completer matches, we assemble an
     * ordered list. This list begins with:
     * ```
     * ['function', 'instance', 'class', 'module', 'keyword']
     * ```
     * and then has any remaining types listed alphabetically. This will give
     * reliable visual encoding for these known types, but allow kernels to
     * provide new types.
     */
    orderedTypes() {
        return this._orderedTypes;
    }
    /**
     * Handle a cursor change.
     */
    handleCursorChange(change) {
        // If there is no active completion, return.
        if (!this._original) {
            return;
        }
        const { column, line } = change;
        const { current, original } = this;
        if (!original) {
            return;
        }
        // If a cursor change results in a the cursor being on a different line
        // than the original request, cancel.
        if (line !== original.line) {
            this.reset(true);
            return;
        }
        // If a cursor change results in the cursor being set to a position that
        // precedes the original column, cancel.
        if (column < original.column) {
            this.reset(true);
            return;
        }
        const { cursor } = this;
        if (!cursor || !current) {
            return;
        }
        // If a cursor change results in the cursor being set to a position beyond
        // the end of the area that would be affected by completion, cancel.
        const cursorDelta = cursor.end - cursor.start;
        const originalLine = original.text.split('\n')[original.line];
        const currentLine = current.text.split('\n')[current.line];
        const inputDelta = currentLine.length - originalLine.length;
        if (column > original.column + cursorDelta + inputDelta) {
            this.reset(true);
            return;
        }
    }
    /**
     * Handle a text change.
     */
    handleTextChange(change) {
        const original = this._original;
        // If there is no active completion, return.
        if (!original) {
            return;
        }
        const { text, column, line } = change;
        const last = text.split('\n')[line][column - 1];
        // If last character entered is not whitespace or if the change column is
        // greater than or equal to the original column, update completion.
        if ((last && last.match(/\S/)) || change.column >= original.column) {
            this.current = change;
            return;
        }
        // If final character is whitespace, reset completion.
        this.reset(false);
    }
    /**
     * Create a resolved patch between the original state and a patch string.
     *
     * @param patch - The patch string to apply to the original value.
     *
     * @returns A patched text change or undefined if original value did not exist.
     */
    createPatch(patch) {
        const original = this._original;
        const cursor = this._cursor;
        const current = this._current;
        if (!original || !cursor || !current) {
            return undefined;
        }
        let { start, end } = cursor;
        // Also include any filtering/additional-typing that has occurred
        // since the completion request in the patched length.
        end = end + (current.text.length - original.text.length);
        return { start, end, value: patch };
    }
    /**
     * Reset the state of the model and emit a state change signal.
     *
     * @param hard - Reset even if a subset match is in progress.
     */
    reset(hard = false) {
        // When the completer detects a common subset prefix for all options,
        // it updates the model and sets the model source to that value, triggering
        // a reset. Unless explicitly a hard reset, this should be ignored.
        if (!hard && this._subsetMatch) {
            return;
        }
        this._reset();
        this._stateChanged.emit(undefined);
    }
    /**
     * Check if CompletionItem matches against query.
     * Highlight matching prefix by adding <mark> tags.
     */
    _markup(query) {
        var _a;
        const items = this._completionItems;
        let results = [];
        for (const originalItem of items) {
            // See if label matches query string
            // With ICompletionItems, the label may include parameters,
            // so we exclude them from the matcher.
            // e.g. Given label `foo(b, a, r)` and query `bar`,
            // don't count parameters, `b`, `a`, and `r` as matches.
            const index = originalItem.label.indexOf('(');
            const text = index > -1
                ? originalItem.label.substring(0, index)
                : originalItem.label;
            const match = algorithm_dist_index_es6_js_.StringExt.matchSumOfSquares(escapeHTML(text), query);
            // Filter non-matching items.
            if (match) {
                // Highlight label text if there's a match
                let marked = algorithm_dist_index_es6_js_.StringExt.highlight(escapeHTML(originalItem.label), match.indices, Private.mark);
                // Use `Object.assign` to evaluate getters.
                const highlightedItem = Object.assign({}, originalItem);
                highlightedItem.label = marked.join('');
                highlightedItem.insertText =
                    (_a = originalItem.insertText) !== null && _a !== void 0 ? _a : originalItem.label;
                results.push({
                    item: highlightedItem,
                    score: match.score,
                    originalItem
                });
            }
        }
        results.sort(Private.scoreCmp);
        // Extract only the item (dropping the extra score attribute to not leak
        // implementation details to JavaScript callers.
        return results.map(match => ({
            processedItem: match.item,
            originalItem: match.originalItem
        }));
    }
    /**
     * Lazy load missing data of an item.
     * @param indexOrValue - the item or its index
     * @remarks
     * Resolving item by index will be deprecated in
     * the JupyterLab 5.0 and removed in JupyterLab 6.0.
     *
     * @return Return `undefined` if the completion item with `activeIndex` index can not be found.
     *  Return a promise of `null` if another `resolveItem` is called. Otherwise return the
     * promise of resolved completion item.
     */
    resolveItem(indexOrValue) {
        let processedItem;
        if (typeof indexOrValue === 'number') {
            const completionItems = this.completionItems();
            if (!completionItems || !completionItems[indexOrValue]) {
                return undefined;
            }
            processedItem = completionItems[indexOrValue];
        }
        else {
            processedItem = indexOrValue;
        }
        if (!processedItem) {
            return undefined;
        }
        let originalItem;
        if (this._processedToOriginalItem) {
            originalItem = this._processedToOriginalItem.get(processedItem);
        }
        else {
            originalItem = processedItem;
        }
        if (!originalItem) {
            return undefined;
        }
        return this._resolveItemByValue(originalItem);
    }
    /**
     * Lazy load missing data of a completion item.
     *
     * @param  completionItem - the item to be resolved
     * @return See `resolveItem` method
     */
    _resolveItemByValue(completionItem) {
        const current = ++this._resolvingItem;
        let resolvedItem;
        if (completionItem.resolve) {
            let patch;
            if (completionItem.insertText) {
                patch = this.createPatch(completionItem.insertText);
            }
            resolvedItem = completionItem.resolve(patch);
        }
        else {
            resolvedItem = Promise.resolve(completionItem);
        }
        return resolvedItem
            .then(activeItem => {
            // Escape the label it in place
            this._escapeItemLabel(activeItem, true);
            Object.keys(activeItem).forEach((key) => {
                completionItem[key] = activeItem[key];
            });
            completionItem.resolve = undefined;
            if (current !== this._resolvingItem) {
                return Promise.resolve(null);
            }
            return activeItem;
        })
            .catch(e => {
            console.error(e);
            // Failed to resolve missing data, return the original item.
            return Promise.resolve(completionItem);
        });
    }
    /**
     * Escape item label, storing the original label and adding `insertText` if needed.
     * If escaping changes label creates a new item unless `inplace` is true.
     */
    _escapeItemLabel(item, inplace = false) {
        var _a;
        const escapedLabel = escapeHTML(item.label);
        // If there was no insert text, use the original (unescaped) label.
        if (escapedLabel !== item.label) {
            const newItem = inplace ? item : Object.assign({}, item);
            newItem.insertText = (_a = item.insertText) !== null && _a !== void 0 ? _a : item.label;
            newItem.label = escapedLabel;
            return newItem;
        }
        return item;
    }
    /**
     * Reset the state of the model.
     */
    _reset() {
        const hadQuery = this._query;
        this._current = null;
        this._cursor = null;
        this._completionItems = [];
        this._original = null;
        this._query = '';
        this.processedItemsCache = null;
        this._processedToOriginalItem = null;
        this._subsetMatch = false;
        this._typeMap = {};
        this._orderedTypes = [];
        if (hadQuery) {
            this._queryChanged.emit({ newValue: this._query, origin: 'reset' });
        }
    }
}
/**
 * A namespace for completer model private data.
 */
var Private;
(function (Private) {
    /**
     * The list of known type annotations of completer matches.
     */
    const KNOWN_TYPES = ['function', 'instance', 'class', 'module', 'keyword'];
    /**
     * The map of known type annotations of completer matches.
     */
    const KNOWN_MAP = KNOWN_TYPES.reduce((acc, type) => {
        acc[type] = null;
        return acc;
    }, {});
    /**
     * Mark a highlighted chunk of text.
     */
    function mark(value) {
        return `<mark>${value}</mark>`;
    }
    Private.mark = mark;
    /**
     * A sort comparison function for item match scores.
     *
     * #### Notes
     * This orders the items first based on score (lower is better), then
     * by locale order of the item text.
     */
    function scoreCmp(a, b) {
        var _a, _b, _c;
        const delta = a.score - b.score;
        if (delta !== 0) {
            return delta;
        }
        return (_c = (_a = a.item.insertText) === null || _a === void 0 ? void 0 : _a.localeCompare((_b = b.item.insertText) !== null && _b !== void 0 ? _b : '')) !== null && _c !== void 0 ? _c : 0;
    }
    Private.scoreCmp = scoreCmp;
    /**
     * Compute a reliably ordered list of types for ICompletionItems.
     *
     * #### Notes
     * The resulting list always begins with the known types:
     * ```
     * ['function', 'instance', 'class', 'module', 'keyword']
     * ```
     * followed by other types in alphabetical order.
     *
     */
    function findOrderedCompletionItemTypes(items) {
        const newTypeSet = new Set();
        items.forEach(item => {
            if (item.type &&
                !KNOWN_TYPES.includes(item.type) &&
                !newTypeSet.has(item.type)) {
                newTypeSet.add(item.type);
            }
        });
        const newTypes = Array.from(newTypeSet);
        newTypes.sort((a, b) => a.localeCompare(b));
        return KNOWN_TYPES.concat(newTypes);
    }
    Private.findOrderedCompletionItemTypes = findOrderedCompletionItemTypes;
    /**
     * Compute a reliably ordered list of types.
     *
     * #### Notes
     * The resulting list always begins with the known types:
     * ```
     * ['function', 'instance', 'class', 'module', 'keyword']
     * ```
     * followed by other types in alphabetical order.
     */
    function findOrderedTypes(typeMap) {
        const filtered = Object.keys(typeMap)
            .map(key => typeMap[key])
            .filter((value) => !!value && !(value in KNOWN_MAP))
            .sort((a, b) => a.localeCompare(b));
        return KNOWN_TYPES.concat(filtered);
    }
    Private.findOrderedTypes = findOrderedTypes;
})(Private || (Private = {}));

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var lib_index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/rendermime@~4.1.0-alpha.2 (singleton) (fallback: ../packages/rendermime/lib/index.js)
var rendermime_lib_index_js_ = __webpack_require__(66866);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/domutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/domutils/dist/index.es6.js)
var domutils_dist_index_es6_js_ = __webpack_require__(92654);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var widgets_dist_index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/completer/lib/widget.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






/**
 * The class name added to completer menu items.
 */
const ITEM_CLASS = 'jp-Completer-item';
/**
 * The class name added to an active completer menu item.
 */
const ACTIVE_CLASS = 'jp-mod-active';
/**
 * The class used by item listing which determines the height of the completer.
 */
const LIST_CLASS = 'jp-Completer-list';
/**
 * Class of the documentation panel.
 */
const DOC_PANEL_CLASS = 'jp-Completer-docpanel';
/**
 * A flag to indicate that event handlers are caught in the capture phase.
 */
const USE_CAPTURE = true;
/**
 * The number of colors defined for the completer type annotations.
 * These are listed in completer/style/index.css#102-152.
 */
const N_COLORS = 10;
/**
 * A widget that enables text completion.
 *
 * #### Notes
 * The completer is intended to be absolutely positioned on the
 * page and hover over any other content, so it should be attached directly
 * to `document.body`, or a node that is the full size of `document.body`.
 * Attaching it to other nodes may incorrectly locate the completer.
 */
class Completer extends widgets_dist_index_es6_js_.Widget {
    /**
     * Construct a text completer menu widget.
     */
    constructor(options) {
        var _a, _b, _c, _d;
        super({ node: document.createElement('div') });
        this._activeIndex = 0;
        this._editor = null;
        this._model = null;
        this._selected = new dist_index_es6_js_.Signal(this);
        this._visibilityChanged = new dist_index_es6_js_.Signal(this);
        this._indexChanged = new dist_index_es6_js_.Signal(this);
        this._lastSubsetMatch = '';
        this._geometryLock = false;
        /**
         * Increasing this counter invalidates previous request to save geometry cache in animation callback.
         */
        this._geometryCounter = 0;
        this._docPanelExpanded = false;
        this._renderCounter = 0;
        this.sanitizer = (_a = options.sanitizer) !== null && _a !== void 0 ? _a : new lib_index_js_.Sanitizer();
        this._defaultRenderer = Completer.getDefaultRenderer(this.sanitizer);
        this._renderer = (_b = options.renderer) !== null && _b !== void 0 ? _b : this._defaultRenderer;
        this._docPanel = this._createDocPanelNode();
        this.model = (_c = options.model) !== null && _c !== void 0 ? _c : null;
        this.editor = (_d = options.editor) !== null && _d !== void 0 ? _d : null;
        this.addClass('jp-Completer');
        this._updateConstraints();
    }
    /**
     * Cache style constraints from CSS.
     */
    _updateConstraints() {
        const tempNode = document.createElement('div');
        tempNode.classList.add(LIST_CLASS);
        tempNode.style.visibility = 'hidden';
        tempNode.style.overflowY = 'scroll';
        document.body.appendChild(tempNode);
        const computedStyle = window.getComputedStyle(tempNode);
        this._maxHeight = parseInt(computedStyle.maxHeight, 10);
        this._minHeight = parseInt(computedStyle.minHeight, 10);
        this._scrollbarWidth = tempNode.offsetWidth - tempNode.clientWidth;
        document.body.removeChild(tempNode);
        const tempDocPanel = this._createDocPanelNode();
        this._docPanelWidth = widget_Private.measureSize(tempDocPanel, 'inline-block').width;
    }
    /**
     * The active index.
     */
    get activeIndex() {
        return this._activeIndex;
    }
    /**
     * The editor used by the completion widget.
     */
    get editor() {
        return this._editor;
    }
    set editor(newValue) {
        this._editor = newValue;
    }
    /**
     * A signal emitted when a selection is made from the completer menu.
     */
    get selected() {
        return this._selected;
    }
    /**
     * A signal emitted when the completer widget's visibility changes.
     *
     * #### Notes
     * This signal is useful when there are multiple floating widgets that may
     * contend with the same space and ought to be mutually exclusive.
     */
    get visibilityChanged() {
        return this._visibilityChanged;
    }
    /**
     * A signal emitted when the active index changes.
     */
    get indexChanged() {
        return this._indexChanged;
    }
    /**
     * The model used by the completer widget.
     */
    get model() {
        return this._model;
    }
    set model(model) {
        if ((!model && !this._model) || model === this._model) {
            return;
        }
        if (this._model) {
            this._model.stateChanged.disconnect(this.onModelStateChanged, this);
            this._model.queryChanged.disconnect(this.onModelQueryChanged, this);
        }
        this._model = model;
        if (this._model) {
            this._model.stateChanged.connect(this.onModelStateChanged, this);
            this._model.queryChanged.connect(this.onModelQueryChanged, this);
        }
    }
    /**
     * The completer used by the completer widget.
     */
    get renderer() {
        return this._renderer;
    }
    set renderer(renderer) {
        this._renderer = renderer;
    }
    /**
     * Enable/disable the document panel.
     */
    set showDocsPanel(showDoc) {
        this._showDoc = showDoc;
    }
    get showDocsPanel() {
        return this._showDoc;
    }
    /**
     * Dispose of the resources held by the completer widget.
     */
    dispose() {
        this._sizeCache = undefined;
        this._model = null;
        super.dispose();
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the dock panel's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        if (this.isHidden || !this._editor) {
            return;
        }
        switch (event.type) {
            case 'keydown':
                this._evtKeydown(event);
                break;
            case 'pointerdown':
                this._evtPointerdown(event);
                break;
            case 'scroll':
                this._evtScroll(event);
                break;
            default:
                break;
        }
    }
    /**
     * Reset the widget.
     */
    reset() {
        this._activeIndex = 0;
        this._lastSubsetMatch = '';
        if (this._model) {
            this._model.reset(true);
        }
        this._docPanel.style.display = 'none';
        // Clear size cache.
        this._sizeCache = undefined;
        this.node.scrollTop = 0;
    }
    /**
     * Emit the selected signal for the current active item and reset.
     */
    selectActive() {
        const active = this.node.querySelector(`.${ACTIVE_CLASS}`);
        if (!active) {
            this.reset();
            return;
        }
        this._selected.emit(active.getAttribute('data-value'));
        this.reset();
    }
    /**
     * Handle `after-attach` messages for the widget.
     */
    onAfterAttach(msg) {
        document.addEventListener('keydown', this, USE_CAPTURE);
        document.addEventListener('pointerdown', this, USE_CAPTURE);
        document.addEventListener('scroll', this, USE_CAPTURE);
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        document.removeEventListener('keydown', this, USE_CAPTURE);
        document.removeEventListener('pointerdown', this, USE_CAPTURE);
        document.removeEventListener('scroll', this, USE_CAPTURE);
    }
    /**
     * Handle model state changes.
     */
    onModelStateChanged() {
        if (this.isAttached) {
            this._activeIndex = 0;
            this._indexChanged.emit(this._activeIndex);
            this.update();
        }
    }
    /**
     * Handle model query changes.
     */
    onModelQueryChanged(model, queryChange) {
        // If query was changed by the user typing, the filtered down items
        // may no longer reach/exceed the maxHeight of the completer widget,
        // hence size needs to be recalculated.
        if (this._sizeCache && queryChange.origin === 'editorUpdate') {
            const newItems = model.completionItems();
            const oldItems = this._sizeCache.items;
            // Only reset size if the number of items changed, or the longest item changed.
            const oldWidest = oldItems[this._findWidestItemIndex(oldItems)];
            const newWidest = newItems[this._findWidestItemIndex(newItems)];
            const heuristic = this._getPreferredItemWidthHeuristic();
            if (newItems.length !== this._sizeCache.items.length ||
                heuristic(oldWidest) !== heuristic(newWidest)) {
                this._sizeCache = undefined;
            }
        }
    }
    /**
     * Handle `update-request` messages.
     */
    onUpdateRequest(msg) {
        var _a;
        const model = this._model;
        if (!model) {
            return;
        }
        // If this is the first time the current completer session has loaded,
        // populate any initial subset match. This is being done before node
        // gets rendered to avoid rendering it twice.
        if (!model.query) {
            this._populateSubset();
        }
        let items = model.completionItems();
        // If there are no items, reset and bail.
        if (!items.length) {
            if (!this.isHidden) {
                this.reset();
                this.hide();
                this._visibilityChanged.emit(undefined);
            }
            return;
        }
        // Update constraints before any DOM modifications
        this._updateConstraints();
        // Do not trigger any geometry updates from async code when in lock.
        this._geometryLock = true;
        const node = this._createCompleterNode(model, items);
        let active = node.querySelectorAll(`.${ITEM_CLASS}`)[this._activeIndex];
        active.classList.add(ACTIVE_CLASS);
        const resolvedItem = (_a = this.model) === null || _a === void 0 ? void 0 : _a.resolveItem(items[this._activeIndex]);
        // Add the documentation panel
        if (this._showDoc) {
            this._docPanel.innerText = '';
            node.appendChild(this._docPanel);
            this._docPanelExpanded = false;
            this._docPanel.style.display = 'none';
            this._updateDocPanel(resolvedItem, active);
        }
        if (this.isHidden) {
            this.show();
            this._setGeometry();
            this._visibilityChanged.emit(undefined);
        }
        else {
            this._setGeometry();
        }
        this._geometryLock = false;
    }
    /**
     * Get cached dimensions of the completer box.
     */
    get sizeCache() {
        if (!this._sizeCache) {
            return;
        }
        return {
            width: this._sizeCache.width + this._sizeCache.docPanelWidth,
            height: Math.max(this._sizeCache.height, this._sizeCache.docPanelHeight)
        };
    }
    _createDocPanelNode() {
        const docPanel = document.createElement('div');
        docPanel.className = DOC_PANEL_CLASS;
        return docPanel;
    }
    _createCompleterNode(model, items) {
        const current = ++this._renderCounter;
        // Clear the node.
        let node = this.node;
        node.textContent = '';
        // Compute an ordered list of all the types in the typeMap, this is computed
        // once by the model each time new data arrives for efficiency.
        let orderedTypes = model.orderedTypes();
        // Populate the completer items.
        let ul = document.createElement('ul');
        ul.className = LIST_CLASS;
        // Add first N items to fill the first "page" assuming that the completer
        // would reach its maximum allowed height.
        const first = this._renderer.createCompletionItemNode(items[0], orderedTypes);
        const renderedItems = [first];
        const firstItemSize = widget_Private.measureSize(first, 'inline-grid');
        const pageSize = Math.max(Math.ceil(this._maxHeight / firstItemSize.height), 5);
        // We add one item in case if height heuristic is inaccurate.
        const toRenderImmediately = Math.min(pageSize + 1, items.length);
        const start = performance.now();
        for (let i = 1; i < toRenderImmediately; i++) {
            const li = this._renderer.createCompletionItemNode(items[i], orderedTypes);
            renderedItems.push(li);
        }
        for (const li of renderedItems) {
            ul.appendChild(li);
        }
        // Pre-calculate size:
        //  - height will equal first element height times number of items,
        //    or maximum allowed height if there are more items than fit on a page,
        //  - width will be estimated from the widest item.
        const widestItemIndex = this._findWidestItemIndex(items);
        const widestItem = widestItemIndex < renderedItems.length
            ? renderedItems[widestItemIndex]
            : this._renderer.createCompletionItemNode(items[widestItemIndex], orderedTypes);
        // The node needs to be cloned to avoid side-effect of detaching it.
        const widestItemSize = widget_Private.measureSize(widestItem.cloneNode(true), 'inline-grid');
        this._sizeCache = {
            height: Math.min(this._maxHeight, firstItemSize.height * items.length),
            width: widestItemSize.width + this._scrollbarWidth,
            items: items,
            docPanelWidth: 0,
            docPanelHeight: 0
        };
        if (toRenderImmediately < items.length) {
            // Render remaining items on idle in subsequent animation frames,
            // in chunks of size such that each frame would take about 16ms
            // allowing for 4ms of overhead, but keep the chunks no smaller
            // than 5 items at a time.
            const timePerItem = (performance.now() - start) / toRenderImmediately;
            const chunkSize = Math.max(5, Math.floor(12 / timePerItem));
            let alreadyRendered = toRenderImmediately;
            let previousChunkFinal = renderedItems[renderedItems.length - 1];
            const renderChunk = () => {
                if (alreadyRendered >= items.length) {
                    return;
                }
                // Add a filler so that the list with partially rendered items has the total
                // height equal to the (predicted) final height to avoid scrollbar jitter.
                const predictedMissingHeight = firstItemSize.height * (items.length - alreadyRendered);
                previousChunkFinal.style.marginBottom = `${predictedMissingHeight}px`;
                requestAnimationFrame(() => {
                    if (current != this._renderCounter) {
                        // Bail if rendering afresh was requested in the meantime.
                        return;
                    }
                    previousChunkFinal.style.marginBottom = '';
                    const limit = Math.min(items.length, alreadyRendered + chunkSize);
                    for (let i = alreadyRendered; i < limit; i++) {
                        const li = this._renderer.createCompletionItemNode(items[i], orderedTypes);
                        ul.appendChild(li);
                        previousChunkFinal = li;
                    }
                    alreadyRendered = limit;
                    renderChunk();
                });
            };
            renderChunk();
        }
        node.appendChild(ul);
        return node;
    }
    /**
     * Use preferred heuristic to find the index of the widest item.
     */
    _findWidestItemIndex(items) {
        const widthHeuristic = this._getPreferredItemWidthHeuristic();
        const widthHeuristics = items.map(widthHeuristic);
        return widthHeuristics.indexOf(Math.max(...widthHeuristics));
    }
    /**
     * Get item width heuristic function from renderer if available,
     * or the default one otherwise.
     */
    _getPreferredItemWidthHeuristic() {
        return this._renderer.itemWidthHeuristic
            ? this._renderer.itemWidthHeuristic.bind(this._renderer)
            : this._defaultRenderer.itemWidthHeuristic.bind(this._defaultRenderer);
    }
    /**
     * Cycle through the available completer items.
     *
     * #### Notes
     * When the user cycles all the way `down` to the last index, subsequent
     * `down` cycles will cycle to the first index. When the user cycles `up` to
     * the first item, subsequent `up` cycles will cycle to the last index.
     */
    _cycle(direction) {
        var _a, _b;
        const items = this.node.querySelectorAll(`.${ITEM_CLASS}`);
        const index = this._activeIndex;
        const last = items.length - 1;
        let active = this.node.querySelector(`.${ACTIVE_CLASS}`);
        active.classList.remove(ACTIVE_CLASS);
        switch (direction) {
            case 'up':
                this._activeIndex = index === 0 ? last : index - 1;
                break;
            case 'down':
                this._activeIndex = index < last ? index + 1 : 0;
                break;
            case 'pageUp':
            case 'pageDown': {
                // Measure the number of items on a page and clamp to the list length.
                const container = this.node.getBoundingClientRect();
                const current = active.getBoundingClientRect();
                const page = Math.floor(container.height / current.height);
                const sign = direction === 'pageUp' ? -1 : 1;
                this._activeIndex = Math.min(Math.max(0, index + sign * page), last);
                break;
            }
        }
        active = items[this._activeIndex];
        active.classList.add(ACTIVE_CLASS);
        let completionList = this.node.querySelector(`.${LIST_CLASS}`);
        domutils_dist_index_es6_js_.ElementExt.scrollIntoViewIfNeeded(completionList, active);
        this._indexChanged.emit(this._activeIndex);
        const visibleCompletionItems = (_a = this.model) === null || _a === void 0 ? void 0 : _a.completionItems();
        const activeCompletionItem = visibleCompletionItems === null || visibleCompletionItems === void 0 ? void 0 : visibleCompletionItems[this._activeIndex];
        if (activeCompletionItem) {
            const resolvedItem = (_b = this.model) === null || _b === void 0 ? void 0 : _b.resolveItem(activeCompletionItem);
            if (this._showDoc) {
                this._updateDocPanel(resolvedItem, active);
            }
        }
    }
    /**
     * Handle keydown events for the widget.
     */
    _evtKeydown(event) {
        if (this.isHidden || !this._editor) {
            return;
        }
        if (!this._editor.host.contains(event.target)) {
            this.reset();
            return;
        }
        switch (event.keyCode) {
            case 9: {
                // Tab key
                event.preventDefault();
                event.stopPropagation();
                event.stopImmediatePropagation();
                const model = this._model;
                if (!model) {
                    return;
                }
                // Autoinsert single completions on manual request (tab)
                const items = model.completionItems();
                if (items && items.length === 1) {
                    this._selected.emit(items[0].insertText || items[0].label);
                    this.reset();
                    return;
                }
                const populated = this._populateSubset();
                // If the common subset was found and set on `query`,
                // or if there is a `query` in the initialization options,
                // then emit a completion signal with that `query` (=subset match),
                // but only if the query has actually changed.
                // See: https://github.com/jupyterlab/jupyterlab/issues/10439#issuecomment-875189540
                if (model.query && model.query !== this._lastSubsetMatch) {
                    model.subsetMatch = true;
                    this._selected.emit(model.query);
                    model.subsetMatch = false;
                    this._lastSubsetMatch = model.query;
                }
                // If the query changed, update rendering of the options.
                if (populated) {
                    this.update();
                }
                this._cycle(event.shiftKey ? 'up' : 'down');
                return;
            }
            case 27: // Esc key
                event.preventDefault();
                event.stopPropagation();
                event.stopImmediatePropagation();
                this.reset();
                return;
            case 33: // PageUp
            case 34: // PageDown
            case 38: // Up arrow key
            case 40: {
                // Down arrow key
                event.preventDefault();
                event.stopPropagation();
                event.stopImmediatePropagation();
                const cycle = widget_Private.keyCodeMap[event.keyCode];
                this._cycle(cycle);
                return;
            }
            default:
                return;
        }
    }
    /**
     * Handle mousedown events for the widget.
     */
    _evtPointerdown(event) {
        if (this.isHidden || !this._editor) {
            return;
        }
        if (widget_Private.nonstandardClick(event)) {
            this.reset();
            return;
        }
        let target = event.target;
        while (target !== document.documentElement) {
            // If the user has made a selection, emit its value and reset the widget.
            if (target.classList.contains(ITEM_CLASS)) {
                event.preventDefault();
                event.stopPropagation();
                event.stopImmediatePropagation();
                this._selected.emit(target.getAttribute('data-value'));
                this.reset();
                return;
            }
            // If the mouse event happened anywhere else in the widget, bail.
            if (target === this.node) {
                event.preventDefault();
                event.stopPropagation();
                event.stopImmediatePropagation();
                return;
            }
            target = target.parentElement;
        }
        this.reset();
    }
    /**
     * Handle scroll events for the widget
     */
    _evtScroll(event) {
        if (this.isHidden || !this._editor) {
            return;
        }
        const { node } = this;
        // All scrolls except scrolls in the actual hover box node may cause the
        // referent editor that anchors the node to move, so the only scroll events
        // that can safely be ignored are ones that happen inside the hovering node.
        if (node.contains(event.target)) {
            return;
        }
        // Set the geometry of the node asynchronously.
        requestAnimationFrame(() => {
            this._setGeometry();
        });
    }
    /**
     * Populate the completer up to the longest initial subset of items.
     *
     * @returns `true` if a subset match was found and populated.
     */
    _populateSubset() {
        const { model } = this;
        if (!model) {
            return false;
        }
        const items = model.completionItems();
        const subset = widget_Private.commonSubset(items.map(item => item.insertText || item.label));
        const { query } = model;
        // If a common subset exists and it is not the current query, highlight it.
        if (subset && subset !== query && subset.indexOf(query) === 0) {
            model.query = subset;
            return true;
        }
        return false;
    }
    /**
     * Set the visible dimensions of the widget.
     */
    _setGeometry() {
        const { node } = this;
        const model = this._model;
        const editor = this._editor;
        // This is an overly defensive test: `cursor` will always exist if
        // `original` exists, except in contrived tests. But since it is possible
        // to generate a runtime error, the check occurs here.
        if (!editor || !model || !model.original || !model.cursor) {
            return;
        }
        const start = model.cursor.start;
        const position = editor.getPositionAt(start);
        const anchor = editor.getCoordinateForPosition(position);
        const style = window.getComputedStyle(node);
        const borderLeft = parseInt(style.borderLeftWidth, 10) || 0;
        const paddingLeft = parseInt(style.paddingLeft, 10) || 0;
        // When the editor is attached to the main area, contain the completer hover box
        // to the full area available (rather than to the editor itself); the available
        // area excludes the toolbar, hence the first Widget child between MainAreaWidget
        // and editor is preferred. The difference is negligible in File Editor, but
        // substantial for Notebooks.
        const host = editor.host.closest('.jp-MainAreaWidget > .lm-Widget') ||
            editor.host;
        const items = model.completionItems();
        // Fast cache invalidation (only checks for length rather than length + width)
        if (this._sizeCache && this._sizeCache.items.length !== items.length) {
            this._sizeCache = undefined;
        }
        // Calculate the geometry of the completer.
        ui_components_lib_index_js_.HoverBox.setGeometry({
            anchor,
            host: host,
            maxHeight: this._maxHeight,
            minHeight: this._minHeight,
            node: node,
            size: this.sizeCache,
            offset: { horizontal: borderLeft + paddingLeft },
            privilege: 'below',
            style: style,
            outOfViewDisplay: {
                top: 'stick-inside',
                bottom: 'stick-inside',
                left: 'stick-inside',
                right: 'stick-outside'
            }
        });
        const current = ++this._geometryCounter;
        if (!this._sizeCache) {
            // If size was not pre-calculated using heuristics, save the actual
            // size into cache once rendered.
            requestAnimationFrame(() => {
                if (current != this._geometryCounter) {
                    // Do not set size to cache if it may already be outdated.
                    return;
                }
                let rect = node.getBoundingClientRect();
                let panel = this._docPanel.getBoundingClientRect();
                this._sizeCache = {
                    width: rect.width - panel.width,
                    height: rect.height,
                    items: items,
                    docPanelWidth: panel.width,
                    docPanelHeight: panel.height
                };
            });
        }
    }
    /**
     * Update the display-state and contents of the documentation panel
     */
    _updateDocPanel(resolvedItem, activeNode) {
        var _a, _b, _c;
        let docPanel = this._docPanel;
        if (!resolvedItem) {
            this._toggleDocPanel(false);
            return;
        }
        const loadingIndicator = (_c = (_b = (_a = this._renderer).createLoadingDocsIndicator) === null || _b === void 0 ? void 0 : _b.call(_a)) !== null && _c !== void 0 ? _c : this._defaultRenderer.createLoadingDocsIndicator();
        activeNode.appendChild(loadingIndicator);
        resolvedItem
            .then(activeItem => {
            var _a, _b, _c;
            if (!activeItem) {
                return;
            }
            if (!docPanel) {
                return;
            }
            if (activeItem.documentation) {
                const node = (_c = (_b = (_a = this._renderer).createDocumentationNode) === null || _b === void 0 ? void 0 : _b.call(_a, activeItem)) !== null && _c !== void 0 ? _c : this._defaultRenderer.createDocumentationNode(activeItem);
                docPanel.textContent = '';
                docPanel.appendChild(node);
                this._toggleDocPanel(true);
            }
            else {
                this._toggleDocPanel(false);
            }
        })
            .catch(e => console.error(e))
            .finally(() => {
            activeNode.removeChild(loadingIndicator);
        });
    }
    _toggleDocPanel(show) {
        let docPanel = this._docPanel;
        if (show) {
            if (this._docPanelExpanded) {
                return;
            }
            docPanel.style.display = '';
            this._docPanelExpanded = true;
        }
        else {
            if (!this._docPanelExpanded) {
                return;
            }
            docPanel.style.display = 'none';
            this._docPanelExpanded = false;
        }
        const sizeCache = this._sizeCache;
        if (sizeCache) {
            sizeCache.docPanelHeight = show ? this._maxHeight : 0;
            sizeCache.docPanelWidth = show ? this._docPanelWidth : 0;
            if (!this._geometryLock) {
                this._setGeometry();
            }
        }
    }
}
(function (Completer) {
    /**
     * The default implementation of an `IRenderer`.
     */
    class Renderer {
        constructor(options) {
            this.sanitizer = (options === null || options === void 0 ? void 0 : options.sanitizer) || new lib_index_js_.Sanitizer();
        }
        /**
         * Create an item node from an ICompletionItem for a text completer menu.
         */
        createCompletionItemNode(item, orderedTypes) {
            let wrapperNode = this._createWrapperNode(item.insertText || item.label);
            if (item.deprecated) {
                wrapperNode.classList.add('jp-Completer-deprecated');
            }
            return this._constructNode(wrapperNode, this._createLabelNode(item.label), !!item.type, item.type, orderedTypes, item.icon);
        }
        /**
         * Create a documentation node for documentation panel.
         */
        createDocumentationNode(activeItem) {
            const host = document.createElement('div');
            host.classList.add('jp-RenderedText');
            const sanitizer = this.sanitizer;
            const source = activeItem.documentation || '';
            (0,rendermime_lib_index_js_.renderText)({ host, sanitizer, source }).catch(console.error);
            return host;
        }
        /**
         * Get a heuristic for the width of an item.
         */
        itemWidthHeuristic(item) {
            var _a;
            // Get the label text without HTML markup (`<mark>` is the only markup
            // that is allowed in processed items, everything else gets escaped).
            const labelText = item.label.replace(/<(\/)?mark>/g, '');
            return labelText.length + (((_a = item.type) === null || _a === void 0 ? void 0 : _a.length) || 0);
        }
        /**
         * Create a loading bar for the documentation panel.
         */
        createLoadingDocsIndicator() {
            const loadingContainer = document.createElement('div');
            loadingContainer.classList.add('jp-Completer-loading-bar-container');
            const loadingBar = document.createElement('div');
            loadingBar.classList.add('jp-Completer-loading-bar');
            loadingContainer.append(loadingBar);
            return loadingContainer;
        }
        /**
         * Create base node with the value to be inserted.
         */
        _createWrapperNode(value) {
            const li = document.createElement('li');
            li.className = ITEM_CLASS;
            // Set the raw, un-marked up value as a data attribute.
            li.setAttribute('data-value', value);
            return li;
        }
        /**
         * Create match node to highlight potential prefix match within result.
         */
        _createLabelNode(result) {
            const matchNode = document.createElement('code');
            matchNode.className = 'jp-Completer-match';
            // Use innerHTML because search results include <mark> tags.
            matchNode.innerHTML = result;
            return matchNode;
        }
        /**
         * Attaches type and match nodes to base node.
         */
        _constructNode(li, matchNode, typesExist, type, orderedTypes, icon) {
            // Add the icon or type monogram
            if (icon) {
                const iconNode = icon.element({
                    className: 'jp-Completer-type jp-Completer-icon'
                });
                li.appendChild(iconNode);
            }
            else if (typesExist) {
                const typeNode = document.createElement('span');
                typeNode.textContent = (type[0] || '').toLowerCase();
                const colorIndex = (orderedTypes.indexOf(type) % N_COLORS) + 1;
                typeNode.className = 'jp-Completer-type jp-Completer-monogram';
                typeNode.setAttribute(`data-color-index`, colorIndex.toString());
                li.appendChild(typeNode);
            }
            else {
                // Create empty span to ensure consistent list styling.
                // Otherwise, in a list of two items,
                // if one item has an icon, but the other has type,
                // the icon grows out of its bounds.
                const dummyNode = document.createElement('span');
                dummyNode.className = 'jp-Completer-monogram';
                li.appendChild(dummyNode);
            }
            li.appendChild(matchNode);
            // If there is a type, add the type extension and title
            if (typesExist) {
                li.title = type;
                const typeExtendedNode = document.createElement('code');
                typeExtendedNode.className = 'jp-Completer-typeExtended';
                typeExtendedNode.textContent = type.toLocaleLowerCase();
                li.appendChild(typeExtendedNode);
            }
            else {
                // If no type is present on the right,
                // the highlighting of the completion item
                // doesn't cover the entire row.
                const dummyTypeExtendedNode = document.createElement('span');
                dummyTypeExtendedNode.className = 'jp-Completer-typeExtended';
                li.appendChild(dummyTypeExtendedNode);
            }
            return li;
        }
    }
    Completer.Renderer = Renderer;
    /**
     * Default renderer
     */
    let _defaultRenderer;
    /**
     * The default `IRenderer` instance.
     */
    function getDefaultRenderer(sanitizer) {
        if (!_defaultRenderer ||
            (sanitizer && _defaultRenderer.sanitizer !== sanitizer)) {
            _defaultRenderer = new Renderer({ sanitizer: sanitizer });
        }
        return _defaultRenderer;
    }
    Completer.getDefaultRenderer = getDefaultRenderer;
})(Completer || (Completer = {}));
/**
 * A namespace for completer widget private data.
 */
var widget_Private;
(function (Private) {
    /**
     * Mapping from keyCodes to scrollTypes.
     */
    Private.keyCodeMap = {
        38: 'up',
        40: 'down',
        33: 'pageUp',
        34: 'pageDown'
    };
    /**
     * Returns the common subset string that a list of strings shares.
     */
    function commonSubset(values) {
        const len = values.length;
        let subset = '';
        if (len < 2) {
            return subset;
        }
        const strlen = values[0].length;
        for (let i = 0; i < strlen; i++) {
            const ch = values[0][i];
            for (let j = 1; j < len; j++) {
                if (values[j][i] !== ch) {
                    return subset;
                }
            }
            subset += ch;
        }
        return subset;
    }
    Private.commonSubset = commonSubset;
    /**
     * Returns true for any modified click event (i.e., not a left-click).
     */
    function nonstandardClick(event) {
        return (event.button !== 0 ||
            event.altKey ||
            event.ctrlKey ||
            event.shiftKey ||
            event.metaKey);
    }
    Private.nonstandardClick = nonstandardClick;
    /**
     * Measure size of provided HTML element without painting it.
     *
     * #### Notes
     * The provided element has to be detached (not connected to DOM),
     * or a side-effect of detaching it will occur.
     */
    function measureSize(element, display) {
        if (element.isConnected) {
            console.warn('Measuring connected elements with `measureSize` has side-effects');
        }
        element.style.visibility = 'hidden';
        element.style.display = display;
        document.body.appendChild(element);
        const size = element.getBoundingClientRect();
        document.body.removeChild(element);
        element.removeAttribute('style');
        return size;
    }
    Private.measureSize = measureSize;
})(widget_Private || (widget_Private = {}));

;// CONCATENATED MODULE: ../packages/completer/lib/reconciliator.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * The reconciliator which is used to fetch and merge responses from multiple completion providers.
 */
class ProviderReconciliator {
    /**
     * Creates an instance of ProviderReconciliator.
     */
    constructor(options) {
        this._resolveFactory = (provider, el) => provider.resolve
            ? (patch) => provider.resolve(el, this._context, patch)
            : undefined;
        /**
         * Counter to reject current provider response if a new fetch request is created.
         */
        this._fetching = 0;
        this._providers = options.providers;
        this._context = options.context;
        this._timeout = options.timeout;
    }
    /**
     * Check for the providers which are applicable with the current context
     *
     * @return  List of applicable providers
     */
    async applicableProviders() {
        const isApplicablePromises = this._providers.map(p => p.isApplicable(this._context));
        const applicableProviders = await Promise.all(isApplicablePromises);
        return this._providers.filter((_, idx) => applicableProviders[idx]);
    }
    /**
     * Fetch response from multiple providers, If a provider can not return
     * the response for a completer request before timeout,
     * the result of this provider will be ignored.
     *
     * @param {CompletionHandler.IRequest} request - The completion request.
     */
    async fetch(request, trigger) {
        const current = ++this._fetching;
        let promises = [];
        const applicableProviders = await this.applicableProviders();
        for (const provider of applicableProviders) {
            let promise;
            promise = provider.fetch(request, this._context, trigger).then(reply => {
                if (current !== this._fetching) {
                    return Promise.reject(void 0);
                }
                const items = reply.items.map(el => ({
                    ...el,
                    resolve: this._resolveFactory(provider, el)
                }));
                return { ...reply, items };
            });
            const timeoutPromise = new Promise(resolve => {
                return setTimeout(() => resolve(null), this._timeout);
            });
            promise = Promise.race([promise, timeoutPromise]);
            // Wrap promise and return error in case of failure.
            promises.push(promise.catch(p => p));
        }
        // TODO: maybe use `Promise.allSettled` once library is at es2020 instead of adding a catch.
        const combinedPromise = Promise.all(promises);
        return this._mergeCompletions(combinedPromise);
    }
    /**
     * Check if completer should make request to fetch completion responses
     * on user typing. If the provider with highest rank does not have
     * `shouldShowContinuousHint` method, a default one will be used.
     *
     * @param completerIsVisible - The visible status of completer widget.
     * @param changed - CodeMirror changed argument.
     */
    async shouldShowContinuousHint(completerIsVisible, changed) {
        const applicableProviders = await this.applicableProviders();
        if (applicableProviders.length === 0) {
            return false;
        }
        if (applicableProviders[0].shouldShowContinuousHint) {
            return applicableProviders[0].shouldShowContinuousHint(completerIsVisible, changed, this._context);
        }
        return this._defaultShouldShowContinuousHint(completerIsVisible, changed);
    }
    _alignPrefixes(replies, minStart, maxStart) {
        if (minStart != maxStart) {
            const editor = this._context.editor;
            if (!editor) {
                return replies;
            }
            const cursor = editor.getCursorPosition();
            const line = editor.getLine(cursor.line);
            if (!line) {
                return replies;
            }
            return replies.map(reply => {
                // No prefix to strip, return as-is.
                if (reply.start == maxStart) {
                    return reply;
                }
                let prefix = line.substring(reply.start, maxStart);
                return {
                    ...reply,
                    items: reply.items.map(item => {
                        let insertText = item.insertText || item.label;
                        item.insertText = insertText.startsWith(prefix)
                            ? insertText.slice(prefix.length)
                            : insertText;
                        return item;
                    })
                };
            });
        }
        return replies;
    }
    async _mergeCompletions(promises) {
        let replies = (await promises).filter(reply => {
            // Ignore it errors out.
            if (!reply || reply instanceof Error) {
                return false;
            }
            // Ignore if no matches.
            if (!reply.items.length) {
                return false;
            }
            // Otherwise keep.
            return true;
        });
        // Fast path for a single reply or no replies.
        if (replies.length == 0) {
            return null;
        }
        else if (replies.length == 1) {
            return replies[0];
        }
        const minEnd = Math.min(...replies.map(reply => reply.end));
        // If any of the replies uses a wider range, we need to align them
        // so that all responses use the same range.
        const starts = replies.map(reply => reply.start);
        const minStart = Math.min(...starts);
        const maxStart = Math.max(...starts);
        replies = this._alignPrefixes(replies, minStart, maxStart);
        const insertTextSet = new Set();
        const mergedItems = new Array();
        for (const reply of replies) {
            reply.items.forEach(item => {
                // IPython returns 'import' and 'import '; while the latter is more useful,
                // user should not see two suggestions with identical labels and nearly-identical
                // behaviour as they could not distinguish the two either way.
                let text = (item.insertText || item.label).trim();
                if (insertTextSet.has(text)) {
                    return;
                }
                insertTextSet.add(text);
                mergedItems.push(item);
            });
        }
        return {
            start: maxStart,
            end: minEnd,
            items: mergedItems
        };
    }
    _defaultShouldShowContinuousHint(completerIsVisible, changed) {
        return (!completerIsVisible &&
            (changed.sourceChange == null ||
                changed.sourceChange.some(delta => delta.insert != null && delta.insert.length > 0)));
    }
}

;// CONCATENATED MODULE: ../packages/completer/lib/default/contextprovider.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
const CONTEXT_PROVIDER_ID = 'CompletionProvider:context';
/**
 * A context connector for completion handlers.
 */
class ContextCompleterProvider {
    constructor() {
        this.identifier = CONTEXT_PROVIDER_ID;
        this.rank = 500;
        this.renderer = null;
    }
    /**
     * The context completion provider is applicable on all cases.
     * @param context - additional information about context of completion request
     */
    async isApplicable(context) {
        return true;
    }
    /**
     * Fetch completion requests.
     *
     * @param request - The completion request text and details.
     */
    fetch(request, context) {
        const editor = context.editor;
        if (!editor) {
            return Promise.reject('No editor');
        }
        return new Promise(resolve => {
            resolve(contextprovider_Private.contextHint(editor));
        });
    }
}
/**
 * A namespace for Private functionality.
 */
var contextprovider_Private;
(function (Private) {
    /**
     * Get a list of completion hints from a tokenization
     * of the editor.
     */
    function contextHint(editor) {
        // Find the token at the cursor
        const token = editor.getTokenAtCursor();
        // Get the list of matching tokens.
        const tokenList = getCompletionTokens(token, editor);
        // Only choose the ones that have a non-empty type
        // field, which are likely to be of interest.
        const completionList = tokenList.filter(t => t.type).map(t => t.value);
        // Remove duplicate completions from the list
        const matches = new Set(completionList);
        const items = new Array();
        matches.forEach(label => items.push({ label }));
        return {
            start: token.offset,
            end: token.offset + token.value.length,
            items
        };
    }
    Private.contextHint = contextHint;
    /**
     * Get a list of tokens that match the completion request,
     * but are not identical to the completion request.
     */
    function getCompletionTokens(token, editor) {
        const candidates = editor.getTokens();
        // Only get the tokens that have a common start, but
        // are not identical.
        return candidates.filter(t => t.value.indexOf(token.value) === 0 && t.value !== token.value);
    }
})(contextprovider_Private || (contextprovider_Private = {}));

;// CONCATENATED MODULE: ../packages/completer/lib/default/kernelprovider.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

const KERNEL_PROVIDER_ID = 'CompletionProvider:kernel';
/**
 * A kernel connector for completion handlers.
 */
class KernelCompleterProvider {
    constructor() {
        this.identifier = KERNEL_PROVIDER_ID;
        this.rank = 550;
        this.renderer = null;
    }
    /**
     * The kernel completion provider is applicable only if the kernel is available.
     * @param context - additional information about context of completion request
     */
    async isApplicable(context) {
        var _a;
        const hasKernel = (_a = context.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!hasKernel) {
            return false;
        }
        return true;
    }
    /**
     * Fetch completion requests.
     *
     * @param request - The completion request text and details.
     */
    async fetch(request, context) {
        var _a;
        const kernel = (_a = context.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel) {
            throw new Error('No kernel for completion request.');
        }
        const contents = {
            code: request.text,
            cursor_pos: request.offset
        };
        const msg = await kernel.requestComplete(contents);
        const response = msg.content;
        if (response.status !== 'ok') {
            throw new Error('Completion fetch failed to return successfully.');
        }
        const items = new Array();
        const metadata = response.metadata._jupyter_types_experimental;
        response.matches.forEach((label, index) => {
            if (metadata && metadata[index]) {
                items.push({
                    label,
                    type: metadata[index].type,
                    insertText: metadata[index].text
                });
            }
            else {
                items.push({ label });
            }
        });
        return {
            start: response.cursor_start,
            end: response.cursor_end,
            items
        };
    }
    /**
     * Kernel provider will use the inspect request to lazy-load the content
     * for document panel.
     */
    async resolve(item, context, patch) {
        const { editor, session } = context;
        if (session && editor) {
            let code = editor.model.sharedModel.getSource();
            const position = editor.getCursorPosition();
            let offset = index_js_.Text.jsIndexToCharIndex(editor.getOffsetAt(position), code);
            const kernel = session.kernel;
            if (!code || !kernel) {
                return Promise.resolve(item);
            }
            if (patch) {
                const { start, value } = patch;
                code = code.substring(0, start) + value;
                offset = offset + value.length;
            }
            const contents = {
                code,
                cursor_pos: offset,
                detail_level: 0
            };
            const msg = await kernel.requestInspect(contents);
            const value = msg.content;
            if (value.status !== 'ok' || !value.found) {
                return item;
            }
            item.documentation = value.data['text/plain'];
            return item;
        }
        return item;
    }
    /**
     * Kernel provider will activate the completer in continuous mode after
     * the `.` character.
     */
    shouldShowContinuousHint(visible, changed) {
        const sourceChange = changed.sourceChange;
        if (sourceChange == null) {
            return true;
        }
        if (sourceChange.some(delta => delta.delete != null)) {
            return false;
        }
        return sourceChange.some(delta => delta.insert != null &&
            (delta.insert === '.' || (!visible && delta.insert.trim().length > 0)));
    }
}

;// CONCATENATED MODULE: ../packages/completer/lib/manager.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








/**
 * A manager for completer provider.
 */
class CompletionProviderManager {
    /**
     * Construct a new completer manager.
     */
    constructor() {
        /**
         * The set of activated providers
         */
        this._activeProviders = new Set([KERNEL_PROVIDER_ID, CONTEXT_PROVIDER_ID]);
        this._providers = new Map();
        this._panelHandlers = new Map();
        this._mostRecentContext = new Map();
        this._activeProvidersChanged = new dist_index_es6_js_.Signal(this);
    }
    /**
     * Signal emitted when active providers list is changed.
     */
    get activeProvidersChanged() {
        return this._activeProvidersChanged;
    }
    /**
     * Set provider timeout.
     *
     * @param {number} timeout - value of timeout in millisecond.
     */
    setTimeout(timeout) {
        this._timeout = timeout;
    }
    /**
     * Enable/disable the document panel.
     */
    setShowDocumentationPanel(showDoc) {
        this._panelHandlers.forEach(handler => (handler.completer.showDocsPanel = showDoc));
        this._showDoc = showDoc;
    }
    /**
     * Enable/disable continuous hinting mode.
     */
    setContinuousHinting(value) {
        this._panelHandlers.forEach(handler => (handler.autoCompletion = value));
        this._autoCompletion = value;
    }
    /**
     * Register a completer provider with the manager.
     *
     * @param {ICompletionProvider} provider - the provider to be registered.
     */
    registerProvider(provider) {
        const identifier = provider.identifier;
        if (this._providers.has(identifier)) {
            console.warn(`Completion service with identifier ${identifier} is already registered`);
        }
        else {
            this._providers.set(identifier, provider);
            this._panelHandlers.forEach((handler, id) => {
                void this.updateCompleter(this._mostRecentContext.get(id));
            });
        }
    }
    /**
     *
     * Return the map of providers.
     */
    getProviders() {
        return this._providers;
    }
    /**
     * Activate the providers by id, the list of ids is populated from user setting.
     * The non-existing providers will be discarded.
     *
     * @param {Array<string>} providerIds - Array of strings with ids of provider
     */
    activateProvider(providerIds) {
        this._activeProviders = new Set([]);
        providerIds.forEach(providerId => {
            if (this._providers.has(providerId)) {
                this._activeProviders.add(providerId);
            }
        });
        if (this._activeProviders.size === 0) {
            this._activeProviders.add(KERNEL_PROVIDER_ID);
            this._activeProviders.add(CONTEXT_PROVIDER_ID);
        }
        this._activeProvidersChanged.emit();
    }
    /**
     * Create or update completer handler of a widget with new context.
     *
     * @param newCompleterContext - The completion context.
     */
    async updateCompleter(newCompleterContext) {
        var _a, _b;
        const { widget, editor, sanitizer } = newCompleterContext;
        const id = widget.id;
        const handler = this._panelHandlers.get(id);
        const firstProvider = [...this._activeProviders][0];
        const provider = this._providers.get(firstProvider);
        let renderer = (_a = provider === null || provider === void 0 ? void 0 : provider.renderer) !== null && _a !== void 0 ? _a : Completer.getDefaultRenderer(sanitizer);
        const modelFactory = provider === null || provider === void 0 ? void 0 : provider.modelFactory;
        let model;
        if (modelFactory) {
            model = await modelFactory.call(provider, newCompleterContext);
        }
        else {
            model = new CompleterModel();
        }
        this._mostRecentContext.set(widget.id, newCompleterContext);
        const options = {
            model,
            renderer,
            sanitizer,
            showDoc: this._showDoc
        };
        if (!handler) {
            // Create a new handler.
            const handler = await this._generateHandler(newCompleterContext, options);
            this._panelHandlers.set(widget.id, handler);
            widget.disposed.connect(old => {
                this.disposeHandler(old.id, handler);
                this._mostRecentContext.delete(id);
            });
        }
        else {
            // Update existing completer.
            const completer = handler.completer;
            (_b = completer.model) === null || _b === void 0 ? void 0 : _b.dispose();
            completer.model = options.model;
            completer.renderer = options.renderer;
            completer.showDocsPanel = options.showDoc;
            // Update other handler attributes.
            handler.autoCompletion = this._autoCompletion;
            if (editor) {
                handler.editor = editor;
                handler.reconciliator = await this.generateReconciliator(newCompleterContext);
            }
        }
    }
    /**
     * Invoke the completer in the widget with provided id.
     *
     * @param id - the id of notebook panel, console panel or code editor.
     */
    invoke(id) {
        const handler = this._panelHandlers.get(id);
        if (handler) {
            handler.invoke();
        }
    }
    /**
     * Activate `select` command in the widget with provided id.
     *
     * @param {string} id - the id of notebook panel, console panel or code editor.
     */
    select(id) {
        const handler = this._panelHandlers.get(id);
        if (handler) {
            handler.completer.selectActive();
        }
    }
    /**
     * Helper function to generate a `ProviderReconciliator` with provided context.
     * The `isApplicable` method of provider is used to filter out the providers
     * which can not be used with provided context.
     *
     * @param {ICompletionContext} completerContext - the current completer context
     */
    async generateReconciliator(completerContext) {
        const providers = [];
        //TODO Update list with rank
        for (const id of this._activeProviders) {
            const provider = this._providers.get(id);
            if (provider) {
                providers.push(provider);
            }
        }
        return new ProviderReconciliator({
            context: completerContext,
            providers,
            timeout: this._timeout
        });
    }
    /**
     * Helper to dispose the completer handler on widget disposed event.
     *
     * @param {string} id - id of the widget
     * @param {CompletionHandler} handler - the handler to be disposed.
     */
    disposeHandler(id, handler) {
        var _a;
        (_a = handler.completer.model) === null || _a === void 0 ? void 0 : _a.dispose();
        handler.completer.dispose();
        handler.dispose();
        this._panelHandlers.delete(id);
    }
    /**
     * Helper to generate a completer handler from provided context.
     */
    async _generateHandler(completerContext, options) {
        const completer = new Completer(options);
        completer.hide();
        widgets_dist_index_es6_js_.Widget.attach(completer, document.body);
        const reconciliator = await this.generateReconciliator(completerContext);
        const handler = new CompletionHandler({
            completer,
            reconciliator: reconciliator
        });
        handler.editor = completerContext.editor;
        return handler;
    }
}

;// CONCATENATED MODULE: ../packages/completer/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module completer
 */










/***/ })

}]);
//# sourceMappingURL=7748.67c05006644aa0f720b5.js.map?v=67c05006644aa0f720b5