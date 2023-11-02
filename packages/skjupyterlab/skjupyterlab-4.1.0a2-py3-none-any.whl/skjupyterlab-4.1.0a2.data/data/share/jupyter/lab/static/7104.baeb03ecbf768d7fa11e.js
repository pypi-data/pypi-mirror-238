"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[7104,8207],{

/***/ 78207:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "ITooltipManager": () => (/* reexport */ ITooltipManager),
  "Tooltip": () => (/* reexport */ Tooltip)
});

// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var index_js_ = __webpack_require__(22100);
;// CONCATENATED MODULE: ../packages/tooltip/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The tooltip manager token.
 */
const ITooltipManager = new index_js_.Token('@jupyterlab/tooltip:ITooltipManager', 'A service for the tooltip manager for the application. Use this to allow your extension to invoke a tooltip.');

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/rendermime@~4.1.0-alpha.2 (singleton) (fallback: ../packages/rendermime/lib/index.js)
var rendermime_lib_index_js_ = __webpack_require__(66866);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/tooltip/lib/widget.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * The class name added to each tooltip.
 */
const TOOLTIP_CLASS = 'jp-Tooltip';
/**
 * The class name added to the tooltip content.
 */
const CONTENT_CLASS = 'jp-Tooltip-content';
/**
 * The class added to the body when a tooltip exists on the page.
 */
const BODY_CLASS = 'jp-mod-tooltip';
/**
 * The minimum height of a tooltip widget.
 */
const MIN_HEIGHT = 20;
/**
 * The maximum height of a tooltip widget.
 */
const MAX_HEIGHT = 250;
/**
 * A flag to indicate that event handlers are caught in the capture phase.
 */
const USE_CAPTURE = true;
/**
 * A tooltip widget.
 */
class Tooltip extends index_es6_js_.Widget {
    /**
     * Instantiate a tooltip.
     */
    constructor(options) {
        super();
        this._content = null;
        const layout = (this.layout = new index_es6_js_.PanelLayout());
        const model = new rendermime_lib_index_js_.MimeModel({ data: options.bundle });
        this.anchor = options.anchor;
        this.addClass(TOOLTIP_CLASS);
        this.hide();
        this._editor = options.editor;
        this._position = options.position;
        this._rendermime = options.rendermime;
        const mimeType = this._rendermime.preferredMimeType(options.bundle, 'any');
        if (!mimeType) {
            return;
        }
        this._content = this._rendermime.createRenderer(mimeType);
        this._content
            .renderModel(model)
            .then(() => this._setGeometry())
            .catch(error => console.error('tooltip rendering failed', error));
        this._content.addClass(CONTENT_CLASS);
        layout.addWidget(this._content);
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this._content) {
            this._content.dispose();
            this._content = null;
        }
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
        if (this.isHidden || this.isDisposed) {
            return;
        }
        const { node } = this;
        const target = event.target;
        switch (event.type) {
            case 'keydown':
                if (node.contains(target)) {
                    return;
                }
                this.dispose();
                break;
            case 'mousedown':
                if (node.contains(target)) {
                    this.activate();
                    return;
                }
                this.dispose();
                break;
            case 'scroll':
                this._evtScroll(event);
                break;
            default:
                break;
        }
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        this.node.tabIndex = 0;
        this.node.focus();
    }
    /**
     * Handle `'after-attach'` messages.
     */
    onAfterAttach(msg) {
        document.body.classList.add(BODY_CLASS);
        document.addEventListener('keydown', this, USE_CAPTURE);
        document.addEventListener('mousedown', this, USE_CAPTURE);
        this.anchor.node.addEventListener('scroll', this, USE_CAPTURE);
        this.update();
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        document.body.classList.remove(BODY_CLASS);
        document.removeEventListener('keydown', this, USE_CAPTURE);
        document.removeEventListener('mousedown', this, USE_CAPTURE);
        this.anchor.node.removeEventListener('scroll', this, USE_CAPTURE);
    }
    /**
     * Handle `'update-request'` messages.
     */
    onUpdateRequest(msg) {
        if (this.isHidden) {
            this.show();
        }
        this._setGeometry();
        super.onUpdateRequest(msg);
    }
    /**
     * Handle scroll events for the widget
     */
    _evtScroll(event) {
        // All scrolls except scrolls in the actual hover box node may cause the
        // referent editor that anchors the node to move, so the only scroll events
        // that can safely be ignored are ones that happen inside the hovering node.
        if (this.node.contains(event.target)) {
            return;
        }
        this.update();
    }
    /**
     * Find the position of the first character of the current token.
     */
    _getTokenPosition() {
        const editor = this._editor;
        const cursor = editor.getCursorPosition();
        const end = editor.getOffsetAt(cursor);
        const line = editor.getLine(cursor.line);
        if (!line) {
            return;
        }
        const tokens = line.substring(0, end).split(/\W+/);
        const last = tokens[tokens.length - 1];
        const start = last ? end - last.length : end;
        return editor.getPositionAt(start);
    }
    /**
     * Set the geometry of the tooltip widget.
     */
    _setGeometry() {
        // determine position for hover box placement
        const position = this._position ? this._position : this._getTokenPosition();
        if (!position) {
            return;
        }
        const editor = this._editor;
        const anchor = editor.getCoordinateForPosition(position);
        const style = window.getComputedStyle(this.node);
        const paddingLeft = parseInt(style.paddingLeft, 10) || 0;
        const host = editor.host.closest('.jp-MainAreaWidget > .lm-Widget') ||
            editor.host;
        // Calculate the geometry of the tooltip.
        lib_index_js_.HoverBox.setGeometry({
            anchor,
            host,
            maxHeight: MAX_HEIGHT,
            minHeight: MIN_HEIGHT,
            node: this.node,
            offset: { horizontal: -1 * paddingLeft },
            privilege: 'below',
            outOfViewDisplay: {
                top: 'stick-inside',
                bottom: 'stick-inside'
            },
            style: style
        });
    }
}

;// CONCATENATED MODULE: ../packages/tooltip/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module tooltip
 */




/***/ })

}]);
//# sourceMappingURL=7104.baeb03ecbf768d7fa11e.js.map?v=baeb03ecbf768d7fa11e