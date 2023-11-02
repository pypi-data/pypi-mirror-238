"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[9465],{

/***/ 29465:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "OutputArea": () => (/* reexport */ OutputArea),
  "OutputAreaModel": () => (/* reexport */ OutputAreaModel),
  "OutputPrompt": () => (/* reexport */ OutputPrompt),
  "SimplifiedOutputArea": () => (/* reexport */ SimplifiedOutputArea),
  "Stdin": () => (/* reexport */ Stdin)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/nbformat@~4.1.0-alpha.2 (strict) (fallback: ../packages/nbformat/lib/index.js)
var index_js_ = __webpack_require__(64571);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/observables@~5.1.0-alpha.2 (strict) (fallback: ../packages/observables/lib/index.js)
var lib_index_js_ = __webpack_require__(57090);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/rendermime@~4.1.0-alpha.2 (singleton) (fallback: ../packages/rendermime/lib/index.js)
var rendermime_lib_index_js_ = __webpack_require__(66866);
// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(16415);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(30205);
;// CONCATENATED MODULE: ../packages/outputarea/lib/model.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






/**
 * The default implementation of the IOutputAreaModel.
 */
class OutputAreaModel {
    /**
     * Construct a new observable outputs instance.
     */
    constructor(options = {}) {
        /**
         * A flag that is set when we want to clear the output area
         * *after* the next addition to it.
         */
        this.clearNext = false;
        this._lastStream = '';
        this._trusted = false;
        this._isDisposed = false;
        this._stateChanged = new dist_index_es6_js_.Signal(this);
        this._changed = new dist_index_es6_js_.Signal(this);
        this._trusted = !!options.trusted;
        this.contentFactory =
            options.contentFactory || OutputAreaModel.defaultContentFactory;
        this.list = new lib_index_js_.ObservableList();
        if (options.values) {
            for (const value of options.values) {
                const index = this._add(value) - 1;
                const item = this.list.get(index);
                item.changed.connect(this._onGenericChange, this);
            }
        }
        this.list.changed.connect(this._onListChanged, this);
    }
    /**
     * A signal emitted when an item changes.
     */
    get stateChanged() {
        return this._stateChanged;
    }
    /**
     * A signal emitted when the list of items changes.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Get the length of the items in the model.
     */
    get length() {
        return this.list ? this.list.length : 0;
    }
    /**
     * Get whether the model is trusted.
     */
    get trusted() {
        return this._trusted;
    }
    /**
     * Set whether the model is trusted.
     *
     * #### Notes
     * Changing the value will cause all of the models to re-set.
     */
    set trusted(value) {
        if (value === this._trusted) {
            return;
        }
        const trusted = (this._trusted = value);
        for (let i = 0; i < this.list.length; i++) {
            const oldItem = this.list.get(i);
            const value = oldItem.toJSON();
            const item = this._createItem({ value, trusted });
            this.list.set(i, item);
            oldItem.dispose();
        }
    }
    /**
     * Test whether the model is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources used by the model.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this.list.dispose();
        dist_index_es6_js_.Signal.clearData(this);
    }
    /**
     * Get an item at the specified index.
     */
    get(index) {
        return this.list.get(index);
    }
    /**
     * Set the value at the specified index.
     */
    set(index, value) {
        value = dist_index_js_.JSONExt.deepCopy(value);
        // Normalize stream data.
        Private.normalize(value);
        const item = this._createItem({ value, trusted: this._trusted });
        this.list.set(index, item);
    }
    /**
     * Add an output, which may be combined with previous output.
     *
     * @returns The total number of outputs.
     *
     * #### Notes
     * The output bundle is copied.
     * Contiguous stream outputs of the same `name` are combined.
     */
    add(output) {
        // If we received a delayed clear message, then clear now.
        if (this.clearNext) {
            this.clear();
            this.clearNext = false;
        }
        return this._add(output);
    }
    /**
     * Clear all of the output.
     *
     * @param wait Delay clearing the output until the next message is added.
     */
    clear(wait = false) {
        this._lastStream = '';
        if (wait) {
            this.clearNext = true;
            return;
        }
        for (const item of this.list) {
            item.dispose();
        }
        this.list.clear();
    }
    /**
     * Deserialize the model from JSON.
     *
     * #### Notes
     * This will clear any existing data.
     */
    fromJSON(values) {
        this.clear();
        for (const value of values) {
            this._add(value);
        }
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        return Array.from((0,index_es6_js_.map)(this.list, (output) => output.toJSON()));
    }
    /**
     * Add a copy of the item to the list.
     *
     * @returns The list length
     */
    _add(value) {
        const trusted = this._trusted;
        value = dist_index_js_.JSONExt.deepCopy(value);
        // Normalize the value.
        Private.normalize(value);
        // Consolidate outputs if they are stream outputs of the same kind.
        if (index_js_.isStream(value) &&
            this._lastStream &&
            value.name === this._lastName &&
            this.shouldCombine({
                value,
                lastModel: this.list.get(this.length - 1)
            })) {
            // In order to get a list change event, we add the previous
            // text to the current item and replace the previous item.
            // This also replaces the metadata of the last item.
            this._lastStream += value.text;
            this._lastStream = Private.removeOverwrittenChars(this._lastStream);
            value.text = this._lastStream;
            const item = this._createItem({ value, trusted });
            const index = this.length - 1;
            const prev = this.list.get(index);
            this.list.set(index, item);
            prev.dispose();
            return this.length;
        }
        if (index_js_.isStream(value)) {
            value.text = Private.removeOverwrittenChars(value.text);
        }
        // Create the new item.
        const item = this._createItem({ value, trusted });
        // Update the stream information.
        if (index_js_.isStream(value)) {
            this._lastStream = value.text;
            this._lastName = value.name;
        }
        else {
            this._lastStream = '';
        }
        // Add the item to our list and return the new length.
        return this.list.push(item);
    }
    /**
     * Whether a new value should be consolidated with the previous output.
     *
     * This will only be called if the minimal criteria of both being stream
     * messages of the same type.
     */
    shouldCombine(options) {
        return true;
    }
    /**
     * Create an output item and hook up its signals.
     */
    _createItem(options) {
        const factory = this.contentFactory;
        const item = factory.createOutputModel(options);
        return item;
    }
    /**
     * Handle a change to the list.
     */
    _onListChanged(sender, args) {
        switch (args.type) {
            case 'add':
                args.newValues.forEach(item => {
                    item.changed.connect(this._onGenericChange, this);
                });
                break;
            case 'remove':
                args.oldValues.forEach(item => {
                    item.changed.disconnect(this._onGenericChange, this);
                });
                break;
            case 'set':
                args.newValues.forEach(item => {
                    item.changed.connect(this._onGenericChange, this);
                });
                args.oldValues.forEach(item => {
                    item.changed.disconnect(this._onGenericChange, this);
                });
                break;
        }
        this._changed.emit(args);
    }
    /**
     * Handle a change to an item.
     */
    _onGenericChange(itemModel) {
        let idx;
        let item = null;
        for (idx = 0; idx < this.list.length; idx++) {
            item = this.list.get(idx);
            if (item === itemModel) {
                break;
            }
        }
        if (item != null) {
            this._stateChanged.emit(idx);
            this._changed.emit({
                type: 'set',
                newIndex: idx,
                oldIndex: idx,
                oldValues: [item],
                newValues: [item]
            });
        }
    }
}
/**
 * The namespace for OutputAreaModel class statics.
 */
(function (OutputAreaModel) {
    /**
     * The default implementation of a `IModelOutputFactory`.
     */
    class ContentFactory {
        /**
         * Create an output model.
         */
        createOutputModel(options) {
            return new rendermime_lib_index_js_.OutputModel(options);
        }
    }
    OutputAreaModel.ContentFactory = ContentFactory;
    /**
     * The default output model factory.
     */
    OutputAreaModel.defaultContentFactory = new ContentFactory();
})(OutputAreaModel || (OutputAreaModel = {}));
/**
 * A namespace for module-private functionality.
 */
var Private;
(function (Private) {
    /**
     * Normalize an output.
     */
    function normalize(value) {
        if (index_js_.isStream(value)) {
            if (Array.isArray(value.text)) {
                value.text = value.text.join('\n');
            }
        }
    }
    Private.normalize = normalize;
    /**
     * Remove characters that are overridden by backspace characters.
     */
    function fixBackspace(txt) {
        let tmp = txt;
        do {
            txt = tmp;
            // Cancel out anything-but-newline followed by backspace
            tmp = txt.replace(/[^\n]\x08/gm, ''); // eslint-disable-line no-control-regex
        } while (tmp.length < txt.length);
        return txt;
    }
    /**
     * Remove chunks that should be overridden by the effect of
     * carriage return characters.
     */
    function fixCarriageReturn(txt) {
        txt = txt.replace(/\r+\n/gm, '\n'); // \r followed by \n --> newline
        while (txt.search(/\r[^$]/g) > -1) {
            const base = txt.match(/^(.*)\r+/m)[1];
            let insert = txt.match(/\r+(.*)$/m)[1];
            insert = insert + base.slice(insert.length, base.length);
            txt = txt.replace(/\r+.*$/m, '\r').replace(/^.*\r/m, insert);
        }
        return txt;
    }
    /*
     * Remove characters overridden by backspaces and carriage returns
     */
    function removeOverwrittenChars(text) {
        return fixCarriageReturn(fixBackspace(text));
    }
    Private.removeOverwrittenChars = removeOverwrittenChars;
})(Private || (Private = {}));

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var apputils_lib_index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/services@~7.1.0-alpha.2 (singleton) (fallback: ../packages/services/lib/index.js)
var services_lib_index_js_ = __webpack_require__(43411);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @lumino/properties@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/properties/dist/index.es6.js)
var properties_dist_index_es6_js_ = __webpack_require__(64260);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var widgets_dist_index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/outputarea/lib/widget.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/**
 * The class name added to an output area widget.
 */
const OUTPUT_AREA_CLASS = 'jp-OutputArea';
/**
 * The class name added to the direction children of OutputArea
 */
const OUTPUT_AREA_ITEM_CLASS = 'jp-OutputArea-child';
/**
 * The class name added to actual outputs
 */
const OUTPUT_AREA_OUTPUT_CLASS = 'jp-OutputArea-output';
/**
 * The class name added to prompt children of OutputArea.
 */
const OUTPUT_AREA_PROMPT_CLASS = 'jp-OutputArea-prompt';
/**
 * The class name added to OutputPrompt.
 */
const OUTPUT_PROMPT_CLASS = 'jp-OutputPrompt';
/**
 * The class name added to an execution result.
 */
const EXECUTE_CLASS = 'jp-OutputArea-executeResult';
/**
 * The class name added stdin items of OutputArea
 */
const OUTPUT_AREA_STDIN_ITEM_CLASS = 'jp-OutputArea-stdin-item';
/**
 * The class name added to stdin widgets.
 */
const STDIN_CLASS = 'jp-Stdin';
/**
 * The class name added to stdin data prompt nodes.
 */
const STDIN_PROMPT_CLASS = 'jp-Stdin-prompt';
/**
 * The class name added to stdin data input nodes.
 */
const STDIN_INPUT_CLASS = 'jp-Stdin-input';
/**
 * The overlay that can be clicked to switch between output scrolling modes.
 */
const OUTPUT_PROMPT_OVERLAY = 'jp-OutputArea-promptOverlay';
/** ****************************************************************************
 * OutputArea
 ******************************************************************************/
/**
 * An output area widget.
 *
 * #### Notes
 * The widget model must be set separately and can be changed
 * at any time.  Consumers of the widget must account for a
 * `null` model, and may want to listen to the `modelChanged`
 * signal.
 */
class OutputArea extends widgets_dist_index_es6_js_.Widget {
    /**
     * Construct an output area widget.
     */
    constructor(options) {
        var _a, _b, _c, _d;
        super();
        /**
         * A public signal used to indicate the number of displayed outputs has changed.
         *
         * #### Notes
         * This is useful for parents who want to apply styling based on the number
         * of outputs. Emits the current number of outputs.
         */
        this.outputLengthChanged = new dist_index_es6_js_.Signal(this);
        /**
         * Handle an iopub message.
         */
        this._onIOPub = (msg) => {
            const model = this.model;
            const msgType = msg.header.msg_type;
            let output;
            const transient = (msg.content.transient || {});
            const displayId = transient['display_id'];
            let targets;
            switch (msgType) {
                case 'execute_result':
                case 'display_data':
                case 'stream':
                case 'error':
                    output = { ...msg.content, output_type: msgType };
                    model.add(output);
                    break;
                case 'clear_output': {
                    const wait = msg.content.wait;
                    model.clear(wait);
                    break;
                }
                case 'update_display_data':
                    output = { ...msg.content, output_type: 'display_data' };
                    targets = this._displayIdMap.get(displayId);
                    if (targets) {
                        for (const index of targets) {
                            model.set(index, output);
                        }
                    }
                    break;
                default:
                    break;
            }
            if (displayId && msgType === 'display_data') {
                targets = this._displayIdMap.get(displayId) || [];
                targets.push(model.length - 1);
                this._displayIdMap.set(displayId, targets);
            }
        };
        /**
         * Handle an execute reply message.
         */
        this._onExecuteReply = (msg) => {
            // API responses that contain a pager are special cased and their type
            // is overridden from 'execute_reply' to 'display_data' in order to
            // render output.
            const model = this.model;
            const content = msg.content;
            if (content.status !== 'ok') {
                return;
            }
            const payload = content && content.payload;
            if (!payload || !payload.length) {
                return;
            }
            const pages = payload.filter((i) => i.source === 'page');
            if (!pages.length) {
                return;
            }
            const page = JSON.parse(JSON.stringify(pages[0]));
            const output = {
                output_type: 'display_data',
                data: page.data,
                metadata: {}
            };
            model.add(output);
        };
        this._displayIdMap = new Map();
        this._minHeightTimeout = null;
        this._inputRequested = new dist_index_es6_js_.Signal(this);
        this._toggleScrolling = new dist_index_es6_js_.Signal(this);
        this._initialize = new dist_index_es6_js_.Signal(this);
        this._outputTracker = new apputils_lib_index_js_.WidgetTracker({
            namespace: dist_index_js_.UUID.uuid4()
        });
        this._inputHistoryScope = 'global';
        super.layout = new widgets_dist_index_es6_js_.PanelLayout();
        this.addClass(OUTPUT_AREA_CLASS);
        this.contentFactory =
            (_a = options.contentFactory) !== null && _a !== void 0 ? _a : OutputArea.defaultContentFactory;
        this.rendermime = options.rendermime;
        this._maxNumberOutputs = (_b = options.maxNumberOutputs) !== null && _b !== void 0 ? _b : Infinity;
        this._translator = (_c = options.translator) !== null && _c !== void 0 ? _c : translation_lib_index_js_.nullTranslator;
        this._inputHistoryScope = (_d = options.inputHistoryScope) !== null && _d !== void 0 ? _d : 'global';
        const model = (this.model = options.model);
        for (let i = 0; i < Math.min(model.length, this._maxNumberOutputs + 1); i++) {
            const output = model.get(i);
            this._insertOutput(i, output);
        }
        model.changed.connect(this.onModelChanged, this);
        model.stateChanged.connect(this.onStateChanged, this);
        if (options.promptOverlay) {
            this._addPromptOverlay();
        }
    }
    /**
     * Narrow the type of OutputArea's layout prop
     */
    get layout() {
        return super.layout;
    }
    /**
     * A read-only sequence of the children widgets in the output area.
     */
    get widgets() {
        return this.layout.widgets;
    }
    /**
     * The kernel future associated with the output area.
     */
    get future() {
        return this._future;
    }
    set future(value) {
        // Bail if the model is disposed.
        if (this.model.isDisposed) {
            throw Error('Model is disposed');
        }
        if (this._future === value) {
            return;
        }
        if (this._future) {
            this._future.dispose();
        }
        this._future = value;
        this.model.clear();
        // Make sure there were no input widgets.
        if (this.widgets.length) {
            this._clear();
            this.outputLengthChanged.emit(Math.min(this.model.length, this._maxNumberOutputs));
        }
        // Handle published messages.
        value.onIOPub = this._onIOPub;
        // Handle the execute reply.
        value.onReply = this._onExecuteReply;
        // Handle stdin.
        value.onStdin = msg => {
            if (services_lib_index_js_.KernelMessage.isInputRequestMsg(msg)) {
                this.onInputRequest(msg, value);
            }
        };
    }
    /**
     * Signal emitted when an output area is requesting an input.
     */
    get inputRequested() {
        return this._inputRequested;
    }
    /**
     * The maximum number of output items to display on top and bottom of cell output.
     *
     * ### Notes
     * It is set to Infinity if no trim is applied.
     */
    get maxNumberOutputs() {
        return this._maxNumberOutputs;
    }
    set maxNumberOutputs(limit) {
        if (limit <= 0) {
            console.warn(`OutputArea.maxNumberOutputs must be strictly positive.`);
            return;
        }
        const lastShown = this._maxNumberOutputs;
        this._maxNumberOutputs = limit;
        if (lastShown < limit) {
            this._showTrimmedOutputs(lastShown);
        }
    }
    /**
     * Dispose of the resources used by the output area.
     */
    dispose() {
        if (this._future) {
            this._future.dispose();
            this._future = null;
        }
        this._displayIdMap.clear();
        this._outputTracker.dispose();
        super.dispose();
    }
    /**
     * Follow changes on the model state.
     */
    onModelChanged(sender, args) {
        switch (args.type) {
            case 'add':
                this._insertOutput(args.newIndex, args.newValues[0]);
                break;
            case 'remove':
                if (this.widgets.length) {
                    // all items removed from model
                    if (this.model.length === 0) {
                        this._clear();
                    }
                    else {
                        // range of items removed from model
                        // remove widgets corresponding to removed model items
                        const startIndex = args.oldIndex;
                        for (let i = 0; i < args.oldValues.length && startIndex < this.widgets.length; ++i) {
                            const widget = this.widgets[startIndex];
                            widget.parent = null;
                            widget.dispose();
                        }
                        // apply item offset to target model item indices in _displayIdMap
                        this._moveDisplayIdIndices(startIndex, args.oldValues.length);
                        // prevent jitter caused by immediate height change
                        this._preventHeightChangeJitter();
                    }
                }
                break;
            case 'set':
                this._setOutput(args.newIndex, args.newValues[0]);
                break;
            default:
                break;
        }
        this.outputLengthChanged.emit(Math.min(this.model.length, this._maxNumberOutputs));
    }
    /**
     * Emitted when user requests toggling of the output scrolling mode.
     */
    get toggleScrolling() {
        return this._toggleScrolling;
    }
    get initialize() {
        return this._initialize;
    }
    /**
     * Add overlay allowing to toggle scrolling.
     */
    _addPromptOverlay() {
        const overlay = document.createElement('div');
        overlay.className = OUTPUT_PROMPT_OVERLAY;
        overlay.addEventListener('click', () => {
            this._toggleScrolling.emit();
        });
        this.node.appendChild(overlay);
        requestAnimationFrame(() => {
            this._initialize.emit();
        });
    }
    /**
     * Update indices in _displayIdMap in response to element remove from model items
     *
     * @param startIndex - The index of first element removed
     *
     * @param count - The number of elements removed from model items
     *
     */
    _moveDisplayIdIndices(startIndex, count) {
        this._displayIdMap.forEach((indices) => {
            const rangeEnd = startIndex + count;
            const numIndices = indices.length;
            // reverse loop in order to prevent removing element affecting the index
            for (let i = numIndices - 1; i >= 0; --i) {
                const index = indices[i];
                // remove model item indices in removed range
                if (index >= startIndex && index < rangeEnd) {
                    indices.splice(i, 1);
                }
                else if (index >= rangeEnd) {
                    // move model item indices that were larger than range end
                    indices[i] -= count;
                }
            }
        });
    }
    /**
     * Follow changes on the output model state.
     */
    onStateChanged(sender, change) {
        const outputLength = Math.min(this.model.length, this._maxNumberOutputs);
        if (change) {
            if (change >= this._maxNumberOutputs) {
                // Bail early
                return;
            }
            this._setOutput(change, this.model.get(change));
        }
        else {
            for (let i = 0; i < outputLength; i++) {
                this._setOutput(i, this.model.get(i));
            }
        }
        this.outputLengthChanged.emit(outputLength);
    }
    /**
     * Clear the widget outputs.
     */
    _clear() {
        // Bail if there is no work to do.
        if (!this.widgets.length) {
            return;
        }
        // Remove all of our widgets.
        const length = this.widgets.length;
        for (let i = 0; i < length; i++) {
            const widget = this.widgets[0];
            widget.parent = null;
            widget.dispose();
        }
        // Clear the display id map.
        this._displayIdMap.clear();
        // prevent jitter caused by immediate height change
        this._preventHeightChangeJitter();
    }
    _preventHeightChangeJitter() {
        // When an output area is cleared and then quickly replaced with new
        // content (as happens with @interact in widgets, for example), the
        // quickly changing height can make the page jitter.
        // We introduce a small delay in the minimum height
        // to prevent this jitter.
        const rect = this.node.getBoundingClientRect();
        this.node.style.minHeight = `${rect.height}px`;
        if (this._minHeightTimeout) {
            window.clearTimeout(this._minHeightTimeout);
        }
        this._minHeightTimeout = window.setTimeout(() => {
            if (this.isDisposed) {
                return;
            }
            this.node.style.minHeight = '';
        }, 50);
    }
    /**
     * Handle an input request from a kernel.
     */
    onInputRequest(msg, future) {
        // Add an output widget to the end.
        const factory = this.contentFactory;
        const stdinPrompt = msg.content.prompt;
        const password = msg.content.password;
        const panel = new widgets_dist_index_es6_js_.Panel();
        panel.addClass(OUTPUT_AREA_ITEM_CLASS);
        panel.addClass(OUTPUT_AREA_STDIN_ITEM_CLASS);
        const prompt = factory.createOutputPrompt();
        prompt.addClass(OUTPUT_AREA_PROMPT_CLASS);
        panel.addWidget(prompt);
        const input = factory.createStdin({
            parent_header: msg.header,
            prompt: stdinPrompt,
            password,
            future,
            translator: this._translator,
            inputHistoryScope: this._inputHistoryScope
        });
        input.addClass(OUTPUT_AREA_OUTPUT_CLASS);
        panel.addWidget(input);
        // Increase number of outputs to display the result up to the input request.
        if (this.model.length >= this.maxNumberOutputs) {
            this.maxNumberOutputs = this.model.length;
        }
        this.layout.addWidget(panel);
        this._inputRequested.emit();
        /**
         * Wait for the stdin to complete, add it to the model (so it persists)
         * and remove the stdin widget.
         */
        void input.value.then(value => {
            // Increase number of outputs to display the result of stdin if needed.
            if (this.model.length >= this.maxNumberOutputs) {
                this.maxNumberOutputs = this.model.length + 1;
            }
            // Use stdin as the stream so it does not get combined with stdout.
            this.model.add({
                output_type: 'stream',
                name: 'stdin',
                text: value + '\n'
            });
            panel.dispose();
        });
    }
    /**
     * Update an output in the layout in place.
     */
    _setOutput(index, model) {
        if (index >= this._maxNumberOutputs) {
            return;
        }
        const panel = this.layout.widgets[index];
        const renderer = (panel.widgets ? panel.widgets[1] : panel);
        // Check whether it is safe to reuse renderer:
        // - Preferred mime type has not changed
        // - Isolation has not changed
        const mimeType = this.rendermime.preferredMimeType(model.data, model.trusted ? 'any' : 'ensure');
        if (widget_Private.currentPreferredMimetype.get(renderer) === mimeType &&
            OutputArea.isIsolated(mimeType, model.metadata) ===
                renderer instanceof widget_Private.IsolatedRenderer) {
            void renderer.renderModel(model);
        }
        else {
            this.layout.widgets[index].dispose();
            this._insertOutput(index, model);
        }
    }
    /**
     * Render and insert a single output into the layout.
     *
     * @param index - The index of the output to be inserted.
     * @param model - The model of the output to be inserted.
     */
    _insertOutput(index, model) {
        if (index > this._maxNumberOutputs) {
            return;
        }
        const layout = this.layout;
        if (index === this._maxNumberOutputs) {
            const warning = new widget_Private.TrimmedOutputs(this._maxNumberOutputs, () => {
                const lastShown = this._maxNumberOutputs;
                this._maxNumberOutputs = Infinity;
                this._showTrimmedOutputs(lastShown);
            });
            layout.insertWidget(index, this._wrappedOutput(warning));
        }
        else {
            let output = this.createOutputItem(model);
            if (output) {
                output.toggleClass(EXECUTE_CLASS, model.executionCount !== null);
            }
            else {
                output = new widgets_dist_index_es6_js_.Widget();
            }
            if (!this._outputTracker.has(output)) {
                void this._outputTracker.add(output);
            }
            layout.insertWidget(index, output);
        }
    }
    /**
     * A widget tracker for individual output widgets in the output area.
     */
    get outputTracker() {
        return this._outputTracker;
    }
    /**
     * Dispose information message and show output models from the given
     * index to maxNumberOutputs
     *
     * @param lastShown Starting model index to insert.
     */
    _showTrimmedOutputs(lastShown) {
        // Dispose information widget
        this.widgets[lastShown].dispose();
        for (let idx = lastShown; idx < this.model.length; idx++) {
            this._insertOutput(idx, this.model.get(idx));
        }
        this.outputLengthChanged.emit(Math.min(this.model.length, this._maxNumberOutputs));
    }
    /**
     * Create an output item with a prompt and actual output
     *
     * @returns a rendered widget, or null if we cannot render
     * #### Notes
     */
    createOutputItem(model) {
        const output = this.createRenderedMimetype(model);
        if (!output) {
            return null;
        }
        return this._wrappedOutput(output, model.executionCount);
    }
    /**
     * Render a mimetype
     */
    createRenderedMimetype(model) {
        const mimeType = this.rendermime.preferredMimeType(model.data, model.trusted ? 'any' : 'ensure');
        if (!mimeType) {
            return null;
        }
        let output = this.rendermime.createRenderer(mimeType);
        const isolated = OutputArea.isIsolated(mimeType, model.metadata);
        if (isolated === true) {
            output = new widget_Private.IsolatedRenderer(output);
        }
        widget_Private.currentPreferredMimetype.set(output, mimeType);
        output.renderModel(model).catch(error => {
            // Manually append error message to output
            const pre = document.createElement('pre');
            const trans = this._translator.load('jupyterlab');
            pre.textContent = trans.__('Javascript Error: %1', error.message);
            output.node.appendChild(pre);
            // Remove mime-type-specific CSS classes
            output.node.className = 'lm-Widget jp-RenderedText';
            output.node.setAttribute('data-mime-type', 'application/vnd.jupyter.stderr');
        });
        return output;
    }
    /**
     * Wrap a output widget within a output panel
     *
     * @param output Output widget to wrap
     * @param executionCount Execution count
     * @returns The output panel
     */
    _wrappedOutput(output, executionCount = null) {
        const panel = new widget_Private.OutputPanel();
        panel.addClass(OUTPUT_AREA_ITEM_CLASS);
        const prompt = this.contentFactory.createOutputPrompt();
        prompt.executionCount = executionCount;
        prompt.addClass(OUTPUT_AREA_PROMPT_CLASS);
        panel.addWidget(prompt);
        output.addClass(OUTPUT_AREA_OUTPUT_CLASS);
        panel.addWidget(output);
        return panel;
    }
}
class SimplifiedOutputArea extends OutputArea {
    /**
     * Handle an input request from a kernel by doing nothing.
     */
    onInputRequest(msg, future) {
        return;
    }
    /**
     * Create an output item without a prompt, just the output widgets
     */
    createOutputItem(model) {
        const output = this.createRenderedMimetype(model);
        if (!output) {
            return null;
        }
        const panel = new widget_Private.OutputPanel();
        panel.addClass(OUTPUT_AREA_ITEM_CLASS);
        output.addClass(OUTPUT_AREA_OUTPUT_CLASS);
        panel.addWidget(output);
        return panel;
    }
}
/**
 * A namespace for OutputArea statics.
 */
(function (OutputArea) {
    /**
     * Execute code on an output area.
     */
    async function execute(code, output, sessionContext, metadata) {
        var _a;
        // Override the default for `stop_on_error`.
        let stopOnError = true;
        if (metadata &&
            Array.isArray(metadata.tags) &&
            metadata.tags.indexOf('raises-exception') !== -1) {
            stopOnError = false;
        }
        const content = {
            code,
            stop_on_error: stopOnError
        };
        const kernel = (_a = sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel) {
            throw new Error('Session has no kernel.');
        }
        const future = kernel.requestExecute(content, false, metadata);
        output.future = future;
        return future.done;
    }
    OutputArea.execute = execute;
    function isIsolated(mimeType, metadata) {
        const mimeMd = metadata[mimeType];
        // mime-specific higher priority
        if (mimeMd && mimeMd['isolated'] !== undefined) {
            return !!mimeMd['isolated'];
        }
        else {
            // fallback on global
            return !!metadata['isolated'];
        }
    }
    OutputArea.isIsolated = isIsolated;
    /**
     * The default implementation of `IContentFactory`.
     */
    class ContentFactory {
        /**
         * Create the output prompt for the widget.
         */
        createOutputPrompt() {
            return new OutputPrompt();
        }
        /**
         * Create an stdin widget.
         */
        createStdin(options) {
            return new Stdin(options);
        }
    }
    OutputArea.ContentFactory = ContentFactory;
    /**
     * The default `ContentFactory` instance.
     */
    OutputArea.defaultContentFactory = new ContentFactory();
})(OutputArea || (OutputArea = {}));
/**
 * The default output prompt implementation
 */
class OutputPrompt extends widgets_dist_index_es6_js_.Widget {
    /*
     * Create an output prompt widget.
     */
    constructor() {
        super();
        this._executionCount = null;
        this.addClass(OUTPUT_PROMPT_CLASS);
    }
    /**
     * The execution count for the prompt.
     */
    get executionCount() {
        return this._executionCount;
    }
    set executionCount(value) {
        this._executionCount = value;
        if (value === null) {
            this.node.textContent = '';
        }
        else {
            this.node.textContent = `[${value}]:`;
        }
    }
}
/**
 * The default stdin widget.
 */
class Stdin extends widgets_dist_index_es6_js_.Widget {
    static _historyIx(key, ix) {
        const history = Stdin._history.get(key);
        if (!history) {
            return undefined;
        }
        const len = history.length;
        // wrap nonpositive ix to nonnegative ix
        if (ix <= 0) {
            return len + ix;
        }
    }
    static _historyAt(key, ix) {
        const history = Stdin._history.get(key);
        if (!history) {
            return undefined;
        }
        const len = history.length;
        const ixpos = Stdin._historyIx(key, ix);
        if (ixpos !== undefined && ixpos < len) {
            return history[ixpos];
        }
        // return undefined if ix is out of bounds
    }
    static _historyPush(key, line) {
        const history = Stdin._history.get(key);
        history.push(line);
        if (history.length > 1000) {
            // truncate line history if it's too long
            history.shift();
        }
    }
    static _historySearch(key, pat, ix, reverse = true) {
        const history = Stdin._history.get(key);
        const len = history.length;
        const ixpos = Stdin._historyIx(key, ix);
        const substrFound = (x) => x.search(pat) !== -1;
        if (ixpos === undefined) {
            return;
        }
        if (reverse) {
            if (ixpos === 0) {
                // reverse search fails if already at start of history
                return;
            }
            const ixFound = history.slice(0, ixpos).findLastIndex(substrFound);
            if (ixFound !== -1) {
                // wrap ix to negative
                return ixFound - len;
            }
        }
        else {
            if (ixpos >= len - 1) {
                // forward search fails if already at end of history
                return;
            }
            const ixFound = history.slice(ixpos + 1).findIndex(substrFound);
            if (ixFound !== -1) {
                // wrap ix to negative and adjust for slice
                return ixFound - len + ixpos + 1;
            }
        }
    }
    /**
     * Construct a new input widget.
     */
    constructor(options) {
        var _a;
        super({
            node: widget_Private.createInputWidgetNode(options.prompt, options.password)
        });
        this._promise = new dist_index_js_.PromiseDelegate();
        this.addClass(STDIN_CLASS);
        this._future = options.future;
        this._historyIndex = 0;
        this._historyKey =
            options.inputHistoryScope === 'session'
                ? options.parent_header.session
                : '';
        this._historyPat = '';
        this._parentHeader = options.parent_header;
        this._password = options.password;
        this._trans = ((_a = options.translator) !== null && _a !== void 0 ? _a : translation_lib_index_js_.nullTranslator).load('jupyterlab');
        this._value = options.prompt + ' ';
        this._input = this.node.getElementsByTagName('input')[0];
        // make users aware of the line history feature
        this._input.placeholder = this._trans.__('↑↓ for history. Search history with c-↑/c-↓');
        // initialize line history
        if (!Stdin._history.has(this._historyKey)) {
            Stdin._history.set(this._historyKey, []);
        }
    }
    /**
     * The value of the widget.
     */
    get value() {
        return this._promise.promise.then(() => this._value);
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
        const input = this._input;
        if (event.type === 'keydown') {
            if (event.key === 'Enter') {
                this.resetSearch();
                this._future.sendInputReply({
                    status: 'ok',
                    value: input.value
                }, this._parentHeader);
                if (this._password) {
                    this._value += '········';
                }
                else {
                    this._value += input.value;
                    Stdin._historyPush(this._historyKey, input.value);
                }
                this._promise.resolve(void 0);
            }
            else if (event.key === 'Escape') {
                // currently this gets clobbered by the documentsearch:end command at the notebook level
                this.resetSearch();
                input.blur();
            }
            else if (event.ctrlKey &&
                (event.key === 'ArrowUp' || event.key === 'ArrowDown')) {
                // if _historyPat is blank, use input as search pattern. Otherwise, reuse the current search pattern
                if (this._historyPat === '') {
                    this._historyPat = input.value;
                }
                const reverse = event.key === 'ArrowUp';
                const searchHistoryIx = Stdin._historySearch(this._historyKey, this._historyPat, this._historyIndex, reverse);
                if (searchHistoryIx !== undefined) {
                    const historyLine = Stdin._historyAt(this._historyKey, searchHistoryIx);
                    if (historyLine !== undefined) {
                        if (this._historyIndex === 0) {
                            this._valueCache = input.value;
                        }
                        this._setInputValue(historyLine);
                        this._historyIndex = searchHistoryIx;
                        // The default action for ArrowUp is moving to first character
                        // but we want to keep the cursor at the end.
                        event.preventDefault();
                    }
                }
            }
            else if (event.key === 'ArrowUp') {
                this.resetSearch();
                const historyLine = Stdin._historyAt(this._historyKey, this._historyIndex - 1);
                if (historyLine) {
                    if (this._historyIndex === 0) {
                        this._valueCache = input.value;
                    }
                    this._setInputValue(historyLine);
                    --this._historyIndex;
                    // The default action for ArrowUp is moving to first character
                    // but we want to keep the cursor at the end.
                    event.preventDefault();
                }
            }
            else if (event.key === 'ArrowDown') {
                this.resetSearch();
                if (this._historyIndex === 0) {
                    // do nothing
                }
                else if (this._historyIndex === -1) {
                    this._setInputValue(this._valueCache);
                    ++this._historyIndex;
                }
                else {
                    const historyLine = Stdin._historyAt(this._historyKey, this._historyIndex + 1);
                    if (historyLine) {
                        this._setInputValue(historyLine);
                        ++this._historyIndex;
                    }
                }
            }
        }
    }
    resetSearch() {
        this._historyPat = '';
    }
    /**
     * Handle `after-attach` messages sent to the widget.
     */
    onAfterAttach(msg) {
        this._input.addEventListener('keydown', this);
        this._input.focus();
    }
    /**
     * Handle `before-detach` messages sent to the widget.
     */
    onBeforeDetach(msg) {
        this._input.removeEventListener('keydown', this);
    }
    _setInputValue(value) {
        this._input.value = value;
        // Set cursor at the end; this is usually not necessary when input is
        // focused but having the explicit placement ensures consistency.
        this._input.setSelectionRange(value.length, value.length);
    }
}
Stdin._history = new Map();

/** ****************************************************************************
 * Private namespace
 ******************************************************************************/
/**
 * A namespace for private data.
 */
var widget_Private;
(function (Private) {
    /**
     * Create the node for an InputWidget.
     */
    function createInputWidgetNode(prompt, password) {
        const node = document.createElement('div');
        const promptNode = document.createElement('pre');
        promptNode.className = STDIN_PROMPT_CLASS;
        promptNode.textContent = prompt;
        const input = document.createElement('input');
        input.className = STDIN_INPUT_CLASS;
        if (password) {
            input.type = 'password';
        }
        node.appendChild(promptNode);
        promptNode.appendChild(input);
        return node;
    }
    Private.createInputWidgetNode = createInputWidgetNode;
    /**
     * A renderer for IFrame data.
     */
    class IsolatedRenderer extends widgets_dist_index_es6_js_.Widget {
        /**
         * Create an isolated renderer.
         */
        constructor(wrapped) {
            super({ node: document.createElement('iframe') });
            this.addClass('jp-mod-isolated');
            this._wrapped = wrapped;
            // Once the iframe is loaded, the subarea is dynamically inserted
            const iframe = this.node;
            iframe.frameBorder = '0';
            iframe.scrolling = 'auto';
            iframe.addEventListener('load', () => {
                // Workaround needed by Firefox, to properly render svg inside
                // iframes, see https://stackoverflow.com/questions/10177190/
                // svg-dynamically-added-to-iframe-does-not-render-correctly
                iframe.contentDocument.open();
                // Insert the subarea into the iframe
                // We must directly write the html. At this point, subarea doesn't
                // contain any user content.
                iframe.contentDocument.write(this._wrapped.node.innerHTML);
                iframe.contentDocument.close();
                const body = iframe.contentDocument.body;
                // Adjust the iframe height automatically
                iframe.style.height = `${body.scrollHeight}px`;
                iframe.heightChangeObserver = new ResizeObserver(() => {
                    iframe.style.height = `${body.scrollHeight}px`;
                });
                iframe.heightChangeObserver.observe(body);
            });
        }
        /**
         * Render a mime model.
         *
         * @param model - The mime model to render.
         *
         * @returns A promise which resolves when rendering is complete.
         *
         * #### Notes
         * This method may be called multiple times during the lifetime
         * of the widget to update it if and when new data is available.
         */
        renderModel(model) {
            return this._wrapped.renderModel(model);
        }
    }
    Private.IsolatedRenderer = IsolatedRenderer;
    Private.currentPreferredMimetype = new properties_dist_index_es6_js_.AttachedProperty({
        name: 'preferredMimetype',
        create: owner => ''
    });
    /**
     * A `Panel` that's focused by a `contextmenu` event.
     */
    class OutputPanel extends widgets_dist_index_es6_js_.Panel {
        /**
         * Construct a new `OutputPanel` widget.
         */
        constructor(options) {
            super(options);
        }
        /**
         * A callback that focuses on the widget.
         */
        _onContext(_) {
            this.node.focus();
        }
        /**
         * Handle `after-attach` messages sent to the widget.
         */
        onAfterAttach(msg) {
            super.onAfterAttach(msg);
            this.node.addEventListener('contextmenu', this._onContext.bind(this));
        }
        /**
         * Handle `before-detach` messages sent to the widget.
         */
        onBeforeDetach(msg) {
            super.onAfterDetach(msg);
            this.node.removeEventListener('contextmenu', this._onContext.bind(this));
        }
    }
    Private.OutputPanel = OutputPanel;
    /**
     * Trimmed outputs information widget.
     */
    class TrimmedOutputs extends widgets_dist_index_es6_js_.Widget {
        /**
         * Widget constructor
         *
         * ### Notes
         * The widget will be disposed on click after calling the callback.
         *
         * @param maxNumberOutputs Maximal number of outputs to display
         * @param _onClick Callback on click event on the widget
         */
        constructor(maxNumberOutputs, onClick) {
            const node = document.createElement('div');
            const title = `The first ${maxNumberOutputs} are displayed`;
            const msg = 'Show more outputs';
            node.insertAdjacentHTML('afterbegin', `<a title=${title}>
          <pre>${msg}</pre>
        </a>`);
            super({
                node
            });
            this._onClick = onClick;
            this.addClass('jp-TrimmedOutputs');
            this.addClass('jp-RenderedHTMLCommon');
        }
        /**
         * Handle the DOM events for widget.
         *
         * @param event - The DOM event sent to the widget.
         *
         * #### Notes
         * This method implements the DOM `EventListener` interface and is
         * called in response to events on the widget's DOM node. It should
         * not be called directly by user code.
         */
        handleEvent(event) {
            if (event.type === 'click') {
                this._onClick(event);
            }
        }
        /**
         * Handle `after-attach` messages for the widget.
         */
        onAfterAttach(msg) {
            super.onAfterAttach(msg);
            this.node.addEventListener('click', this);
        }
        /**
         * A message handler invoked on a `'before-detach'`
         * message
         */
        onBeforeDetach(msg) {
            super.onBeforeDetach(msg);
            this.node.removeEventListener('click', this);
        }
    }
    Private.TrimmedOutputs = TrimmedOutputs;
})(widget_Private || (widget_Private = {}));

;// CONCATENATED MODULE: ../packages/outputarea/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module outputarea
 */




/***/ })

}]);
//# sourceMappingURL=9465.68987cc053c222bfa8d8.js.map?v=68987cc053c222bfa8d8