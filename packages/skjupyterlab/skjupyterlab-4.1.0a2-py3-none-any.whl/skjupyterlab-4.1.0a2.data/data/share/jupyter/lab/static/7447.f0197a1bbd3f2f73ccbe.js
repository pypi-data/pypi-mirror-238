"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[7447,7356],{

/***/ 57447:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "IInspector": () => (/* reexport */ IInspector),
  "InspectionHandler": () => (/* reexport */ InspectionHandler),
  "InspectorPanel": () => (/* reexport */ InspectorPanel),
  "KernelConnector": () => (/* reexport */ KernelConnector)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/rendermime@~4.1.0-alpha.2 (singleton) (fallback: ../packages/rendermime/lib/index.js)
var lib_index_js_ = __webpack_require__(66866);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @lumino/polling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/polling/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(81967);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(30205);
;// CONCATENATED MODULE: ../packages/inspector/lib/handler.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * An object that handles code inspection.
 */
class InspectionHandler {
    /**
     * Construct a new inspection handler for a widget.
     */
    constructor(options) {
        this._cleared = new dist_index_es6_js_.Signal(this);
        this._disposed = new dist_index_es6_js_.Signal(this);
        this._editor = null;
        this._inspected = new dist_index_es6_js_.Signal(this);
        this._isDisposed = false;
        this._pending = 0;
        this._standby = true;
        this._lastInspectedReply = null;
        this._connector = options.connector;
        this._rendermime = options.rendermime;
        this._debouncer = new index_es6_js_.Debouncer(this.onEditorChange.bind(this), 250);
    }
    /**
     * A signal emitted when the inspector should clear all items.
     */
    get cleared() {
        return this._cleared;
    }
    /**
     * A signal emitted when the handler is disposed.
     */
    get disposed() {
        return this._disposed;
    }
    /**
     * A signal emitted when an inspector value is generated.
     */
    get inspected() {
        return this._inspected;
    }
    /**
     * The editor widget used by the inspection handler.
     */
    get editor() {
        return this._editor;
    }
    set editor(newValue) {
        if (newValue === this._editor) {
            return;
        }
        // Remove all of our listeners.
        dist_index_es6_js_.Signal.disconnectReceiver(this);
        const editor = (this._editor = newValue);
        if (editor) {
            // Clear the inspector in preparation for a new editor.
            this._cleared.emit(void 0);
            // Call onEditorChange to cover the case where the user changes
            // the active cell
            this.onEditorChange();
            editor.model.selections.changed.connect(this._onChange, this);
            editor.model.sharedModel.changed.connect(this._onChange, this);
        }
    }
    /**
     * Indicates whether the handler makes API inspection requests or stands by.
     *
     * #### Notes
     * The use case for this attribute is to limit the API traffic when no
     * inspector is visible.
     */
    get standby() {
        return this._standby;
    }
    set standby(value) {
        this._standby = value;
    }
    /**
     * Get whether the inspection handler is disposed.
     *
     * #### Notes
     * This is a read-only property.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources used by the handler.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._debouncer.dispose();
        this._disposed.emit(void 0);
        dist_index_es6_js_.Signal.clearData(this);
    }
    /**
     * Handle a text changed signal from an editor.
     *
     * #### Notes
     * Update the hints inspector based on a text change.
     */
    onEditorChange(customText) {
        // If the handler is in standby mode, bail.
        if (this._standby) {
            return;
        }
        const editor = this.editor;
        if (!editor) {
            return;
        }
        const text = customText ? customText : editor.model.sharedModel.getSource();
        const position = editor.getCursorPosition();
        const offset = index_js_.Text.jsIndexToCharIndex(editor.getOffsetAt(position), text);
        const update = { content: null };
        const pending = ++this._pending;
        void this._connector
            .fetch({ offset, text })
            .then(reply => {
            // If handler has been disposed or a newer request is pending, bail.
            if (!reply || this.isDisposed || pending !== this._pending) {
                this._lastInspectedReply = null;
                this._inspected.emit(update);
                return;
            }
            const { data } = reply;
            // Do not update if there would be no change.
            if (this._lastInspectedReply &&
                dist_index_js_.JSONExt.deepEqual(this._lastInspectedReply, data)) {
                return;
            }
            const mimeType = this._rendermime.preferredMimeType(data);
            if (mimeType) {
                const widget = this._rendermime.createRenderer(mimeType);
                const model = new lib_index_js_.MimeModel({ data });
                void widget.renderModel(model);
                update.content = widget;
            }
            this._lastInspectedReply = reply.data;
            this._inspected.emit(update);
        })
            .catch(reason => {
            // Since almost all failures are benign, fail silently.
            this._lastInspectedReply = null;
            this._inspected.emit(update);
        });
    }
    /**
     * Handle changes to the editor state, debouncing.
     */
    _onChange() {
        void this._debouncer.invoke();
    }
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var apputils_lib_index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var widgets_dist_index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/inspector/lib/inspector.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * The class name added to inspector panels.
 */
const PANEL_CLASS = 'jp-Inspector';
/**
 * The class name added to inspector content.
 */
const CONTENT_CLASS = 'jp-Inspector-content';
/**
 * The class name added to default inspector content.
 */
const DEFAULT_CONTENT_CLASS = 'jp-Inspector-default-content';
/**
 * A panel which contains a set of inspectors.
 */
class InspectorPanel extends widgets_dist_index_es6_js_.Panel {
    /**
     * Construct an inspector.
     */
    constructor(options = {}) {
        super();
        this._source = null;
        this.translator = options.translator || translation_lib_index_js_.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        if (options.initialContent instanceof widgets_dist_index_es6_js_.Widget) {
            this._content = options.initialContent;
        }
        else if (typeof options.initialContent === 'string') {
            this._content = InspectorPanel._generateContentWidget(`<p>${options.initialContent}</p>`);
        }
        else {
            this._content = InspectorPanel._generateContentWidget('<p>' +
                this._trans.__('Click on a function to see documentation.') +
                '</p>');
        }
        this.addClass(PANEL_CLASS);
        this.layout.addWidget(this._content);
    }
    /**
     * Print in iframe
     */
    [apputils_lib_index_js_.Printing.symbol]() {
        return () => apputils_lib_index_js_.Printing.printWidget(this);
    }
    /**
     * The source of events the inspector panel listens for.
     */
    get source() {
        return this._source;
    }
    set source(source) {
        if (this._source === source) {
            return;
        }
        // Disconnect old signal handler.
        if (this._source) {
            this._source.standby = true;
            this._source.inspected.disconnect(this.onInspectorUpdate, this);
            this._source.disposed.disconnect(this.onSourceDisposed, this);
        }
        // Reject a source that is already disposed.
        if (source && source.isDisposed) {
            source = null;
        }
        // Update source.
        this._source = source;
        // Connect new signal handler.
        if (this._source) {
            this._source.standby = false;
            this._source.inspected.connect(this.onInspectorUpdate, this);
            this._source.disposed.connect(this.onSourceDisposed, this);
        }
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.source = null;
        super.dispose();
    }
    /**
     * Handle inspector update signals.
     */
    onInspectorUpdate(sender, args) {
        const { content } = args;
        // Update the content of the inspector widget.
        if (!content || content === this._content) {
            return;
        }
        this._content.dispose();
        this._content = content;
        content.addClass(CONTENT_CLASS);
        this.layout.addWidget(content);
    }
    /**
     * Handle source disposed signals.
     */
    onSourceDisposed(sender, args) {
        this.source = null;
    }
    /**
     * Generate content widget from string
     */
    static _generateContentWidget(message) {
        const widget = new widgets_dist_index_es6_js_.Widget();
        widget.node.innerHTML = message;
        widget.addClass(CONTENT_CLASS);
        widget.addClass(DEFAULT_CONTENT_CLASS);
        return widget;
    }
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/statedb@~4.1.0-alpha.2 (singleton) (fallback: ../packages/statedb/lib/index.js)
var statedb_lib_index_js_ = __webpack_require__(1458);
;// CONCATENATED MODULE: ../packages/inspector/lib/kernelconnector.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The default connector for making inspection requests from the Jupyter API.
 */
class KernelConnector extends statedb_lib_index_js_.DataConnector {
    /**
     * Create a new kernel connector for inspection requests.
     *
     * @param options - The instantiation options for the kernel connector.
     */
    constructor(options) {
        super();
        this._sessionContext = options.sessionContext;
    }
    /**
     * Fetch inspection requests.
     *
     * @param request - The inspection request text and details.
     */
    fetch(request) {
        var _a;
        const kernel = (_a = this._sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel) {
            return Promise.reject(new Error('Inspection fetch requires a kernel.'));
        }
        const contents = {
            code: request.text,
            cursor_pos: request.offset,
            detail_level: 1
        };
        return kernel.requestInspect(contents).then(msg => {
            const response = msg.content;
            if (response.status !== 'ok' || !response.found) {
                throw new Error('Inspection fetch failed to return successfully.');
            }
            return { data: response.data, metadata: response.metadata };
        });
    }
}

;// CONCATENATED MODULE: ../packages/inspector/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The inspector panel token.
 */
const IInspector = new dist_index_js_.Token('@jupyterlab/inspector:IInspector', `A service for adding contextual help to widgets (visible using "Show Contextual Help" from the Help menu).
  Use this to hook into the contextual help system in your extension.`);

;// CONCATENATED MODULE: ../packages/inspector/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module inspector
 */






/***/ })

}]);
//# sourceMappingURL=7447.f0197a1bbd3f2f73ccbe.js.map?v=f0197a1bbd3f2f73ccbe