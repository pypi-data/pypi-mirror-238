"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[7507,2270],{

/***/ 62270:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "IPropertyInspectorProvider": () => (/* reexport */ IPropertyInspectorProvider),
  "SideBarPropertyInspectorProvider": () => (/* binding */ SideBarPropertyInspectorProvider)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(30205);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(72234);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
;// CONCATENATED MODULE: ../packages/property-inspector/lib/token.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The property inspector provider token.
 */
const IPropertyInspectorProvider = new dist_index_js_.Token('@jupyterlab/property-inspector:IPropertyInspectorProvider', 'A service to registry new widget in the property inspector side panel.');

;// CONCATENATED MODULE: ../packages/property-inspector/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module property-inspector
 */






/**
 * The implementation of the PropertyInspector.
 */
class PropertyInspectorProvider extends dist_index_es6_js_.Widget {
    /**
     * Construct a new Property Inspector.
     */
    constructor() {
        super();
        this._tracker = new dist_index_es6_js_.FocusTracker();
        this._inspectors = new Map();
        this.addClass('jp-PropertyInspector');
        this._tracker = new dist_index_es6_js_.FocusTracker();
        this._tracker.currentChanged.connect(this._onCurrentChanged, this);
    }
    /**
     * Register a widget in the property inspector provider.
     *
     * @param widget The owner widget to register.
     */
    register(widget) {
        if (this._inspectors.has(widget)) {
            throw new Error('Widget is already registered');
        }
        const inspector = new Private.PropertyInspector(widget);
        widget.disposed.connect(this._onWidgetDisposed, this);
        this._inspectors.set(widget, inspector);
        inspector.onAction.connect(this._onInspectorAction, this);
        this._tracker.add(widget);
        return inspector;
    }
    /**
     * The current widget being tracked by the inspector.
     */
    get currentWidget() {
        return this._tracker.currentWidget;
    }
    /**
     * Refresh the content for the current widget.
     */
    refresh() {
        const current = this._tracker.currentWidget;
        if (!current) {
            this.setContent(null);
            return;
        }
        const inspector = this._inspectors.get(current);
        if (inspector) {
            this.setContent(inspector.content);
        }
    }
    /**
     * Handle the disposal of a widget.
     */
    _onWidgetDisposed(sender) {
        const inspector = this._inspectors.get(sender);
        if (inspector) {
            inspector.dispose();
            this._inspectors.delete(sender);
        }
    }
    /**
     * Handle inspector actions.
     */
    _onInspectorAction(sender, action) {
        const owner = sender.owner;
        const current = this._tracker.currentWidget;
        switch (action) {
            case 'content':
                if (current === owner) {
                    this.setContent(sender.content);
                }
                break;
            case 'dispose':
                if (owner) {
                    this._tracker.remove(owner);
                    this._inspectors.delete(owner);
                }
                break;
            case 'show-panel':
                if (current === owner) {
                    this.showPanel();
                }
                break;
            default:
                throw new Error('Unsupported inspector action');
        }
    }
    /**
     * Handle a change to the current widget in the tracker.
     */
    _onCurrentChanged() {
        const current = this._tracker.currentWidget;
        if (current) {
            const inspector = this._inspectors.get(current);
            const content = inspector.content;
            this.setContent(content);
        }
        else {
            this.setContent(null);
        }
    }
}
/**
 * A class that adds a property inspector provider to the
 * JupyterLab sidebar.
 */
class SideBarPropertyInspectorProvider extends PropertyInspectorProvider {
    /**
     * Construct a new Side Bar Property Inspector.
     */
    constructor({ shell, placeholder, translator }) {
        super();
        this._labshell = shell;
        this.translator = translator || index_js_.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        const layout = (this.layout = new dist_index_es6_js_.SingletonLayout());
        if (placeholder) {
            this._placeholder = placeholder;
        }
        else {
            const node = document.createElement('div');
            const content = document.createElement('div');
            content.textContent = this._trans.__('No properties to inspect.');
            content.className = 'jp-PropertyInspector-placeholderContent';
            node.appendChild(content);
            this._placeholder = new dist_index_es6_js_.Widget({ node });
            this._placeholder.addClass('jp-PropertyInspector-placeholder');
        }
        layout.widget = this._placeholder;
        this._labshell.currentChanged.connect(this._onShellCurrentChanged, this);
        this._onShellCurrentChanged();
    }
    /**
     * Set the content of the sidebar panel.
     */
    setContent(content) {
        const layout = this.layout;
        if (layout.widget) {
            layout.widget.removeClass('jp-PropertyInspector-content');
            layout.removeWidget(layout.widget);
        }
        if (!content) {
            content = this._placeholder;
        }
        content.addClass('jp-PropertyInspector-content');
        layout.widget = content;
    }
    /**
     * Show the sidebar panel.
     */
    showPanel() {
        this._labshell.activateById(this.id);
    }
    /**
     * Handle the case when the current widget is not in our tracker.
     */
    _onShellCurrentChanged() {
        const current = this.currentWidget;
        if (!current) {
            this.setContent(null);
            return;
        }
        const currentShell = this._labshell.currentWidget;
        if (currentShell === null || currentShell === void 0 ? void 0 : currentShell.node.contains(current.node)) {
            this.refresh();
        }
        else {
            this.setContent(null);
        }
    }
}
/**
 * A namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * An implementation of the property inspector used by the
     * property inspector provider.
     */
    class PropertyInspector {
        /**
         * Construct a new property inspector.
         */
        constructor(owner) {
            this._isDisposed = false;
            this._content = null;
            this._owner = null;
            this._onAction = new index_es6_js_.Signal(this);
            this._owner = owner;
        }
        /**
         * The owner widget for the property inspector.
         */
        get owner() {
            return this._owner;
        }
        /**
         * The current content for the property inspector.
         */
        get content() {
            return this._content;
        }
        /**
         * Whether the property inspector is disposed.
         */
        get isDisposed() {
            return this._isDisposed;
        }
        /**
         * A signal used for actions related to the property inspector.
         */
        get onAction() {
            return this._onAction;
        }
        /**
         * Show the property inspector panel.
         */
        showPanel() {
            if (this._isDisposed) {
                return;
            }
            this._onAction.emit('show-panel');
        }
        /**
         * Render the property inspector content.
         */
        render(widget) {
            if (this._isDisposed) {
                return;
            }
            if (widget instanceof dist_index_es6_js_.Widget) {
                this._content = widget;
            }
            else {
                this._content = lib_index_js_.ReactWidget.create(widget);
            }
            this._onAction.emit('content');
        }
        /**
         * Dispose of the property inspector.
         */
        dispose() {
            if (this._isDisposed) {
                return;
            }
            this._isDisposed = true;
            this._content = null;
            this._owner = null;
            index_es6_js_.Signal.clearData(this);
        }
    }
    Private.PropertyInspector = PropertyInspector;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=7507.6c88c17541cc2bca6e9c.js.map?v=6c88c17541cc2bca6e9c