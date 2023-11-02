"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[3309,1564],{

/***/ 3309:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "HTMLViewer": () => (/* reexport */ HTMLViewer),
  "HTMLViewerFactory": () => (/* reexport */ HTMLViewerFactory),
  "IHTMLViewerTracker": () => (/* reexport */ IHTMLViewerTracker),
  "ToolbarItems": () => (/* reexport */ ToolbarItems)
});

// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var index_js_ = __webpack_require__(22100);
;// CONCATENATED MODULE: ../packages/htmlviewer/lib/tokens.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

/**
 * The HTML viewer tracker token.
 */
const IHTMLViewerTracker = new index_js_.Token('@jupyterlab/htmlviewer:IHTMLViewerTracker', `A widget tracker for rendered HTML documents.
  Use this if you want to be able to iterate over and interact with HTML documents
  viewed by the application.`);

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var lib_index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/docregistry@~4.1.0-alpha.2 (strict) (fallback: ../packages/docregistry/lib/index.js)
var docregistry_lib_index_js_ = __webpack_require__(16564);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(30205);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
;// CONCATENATED MODULE: ../packages/htmlviewer/lib/widget.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/






/**
 * The timeout to wait for change activity to have ceased before rendering.
 */
const RENDER_TIMEOUT = 1000;
/**
 * The CSS class to add to the HTMLViewer Widget.
 */
const CSS_CLASS = 'jp-HTMLViewer';
const UNTRUSTED_LINK_STYLE = (options) => `<style>
a[target="_blank"],
area[target="_blank"],
form[target="_blank"],
button[formtarget="_blank"],
input[formtarget="_blank"][type="image"],
input[formtarget="_blank"][type="submit"] {
  cursor: not-allowed !important;
}
a[target="_blank"]:hover::after,
area[target="_blank"]:hover::after,
form[target="_blank"]:hover::after,
button[formtarget="_blank"]:hover::after,
input[formtarget="_blank"][type="image"]:hover::after,
input[formtarget="_blank"][type="submit"]:hover::after {
  content: "${options.warning}";
  box-sizing: border-box;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  border: 2px solid #e65100;
  background-color: #ffb74d;
  color: black;
  font-family: system-ui, -apple-system, blinkmacsystemfont, 'Segoe UI', helvetica, arial, sans-serif;
  text-align: center;
}
</style>`;
/**
 * A viewer widget for HTML documents.
 *
 * #### Notes
 * The iframed HTML document can pose a potential security risk,
 * since it can execute Javascript, and make same-origin requests
 * to the server, thereby executing arbitrary Javascript.
 *
 * Here, we sandbox the iframe so that it can't execute Javascript
 * or launch any popups. We allow one exception: 'allow-same-origin'
 * requests, so that local HTML documents can access CSS, images,
 * etc from the files system.
 */
class HTMLViewer extends docregistry_lib_index_js_.DocumentWidget {
    /**
     * Create a new widget for rendering HTML.
     */
    constructor(options) {
        super({
            ...options,
            content: new ui_components_lib_index_js_.IFrame({ sandbox: ['allow-same-origin'] })
        });
        this._renderPending = false;
        this._parser = new DOMParser();
        this._monitor = null;
        this._objectUrl = '';
        this._trustedChanged = new index_es6_js_.Signal(this);
        this.translator = options.translator || translation_lib_index_js_.nullTranslator;
        this.content.addClass(CSS_CLASS);
        void this.context.ready.then(() => {
            this.update();
            // Throttle the rendering rate of the widget.
            this._monitor = new lib_index_js_.ActivityMonitor({
                signal: this.context.model.contentChanged,
                timeout: RENDER_TIMEOUT
            });
            this._monitor.activityStopped.connect(this.update, this);
        });
    }
    /**
     * Whether the HTML document is trusted. If trusted,
     * it can execute Javascript in the iframe sandbox.
     */
    get trusted() {
        return this.content.sandbox.indexOf('allow-scripts') !== -1;
    }
    set trusted(value) {
        if (this.trusted === value) {
            return;
        }
        if (value) {
            this.content.sandbox = Private.trusted;
        }
        else {
            this.content.sandbox = Private.untrusted;
        }
        this.update(); // Force a refresh.
        this._trustedChanged.emit(value);
    }
    /**
     * Emitted when the trust state of the document changes.
     */
    get trustedChanged() {
        return this._trustedChanged;
    }
    /**
     * Dispose of resources held by the html viewer.
     */
    dispose() {
        if (this._objectUrl) {
            try {
                URL.revokeObjectURL(this._objectUrl);
            }
            catch (error) {
                /* no-op */
            }
        }
        super.dispose();
    }
    /**
     * Handle and update request.
     */
    onUpdateRequest() {
        if (this._renderPending) {
            return;
        }
        this._renderPending = true;
        void this._renderModel().then(() => (this._renderPending = false));
    }
    /**
     * Render HTML in IFrame into this widget's node.
     */
    async _renderModel() {
        let data = this.context.model.toString();
        data = await this._setupDocument(data);
        // Set the new iframe url.
        const blob = new Blob([data], { type: 'text/html' });
        const oldUrl = this._objectUrl;
        this._objectUrl = URL.createObjectURL(blob);
        this.content.url = this._objectUrl;
        // Release reference to any previous object url.
        if (oldUrl) {
            try {
                URL.revokeObjectURL(oldUrl);
            }
            catch (error) {
                /* no-op */
            }
        }
        return;
    }
    /**
     * Set a <base> element in the HTML string so that the iframe
     * can correctly dereference relative links.
     */
    async _setupDocument(data) {
        const doc = this._parser.parseFromString(data, 'text/html');
        let base = doc.querySelector('base');
        if (!base) {
            base = doc.createElement('base');
            doc.head.insertBefore(base, doc.head.firstChild);
        }
        const path = this.context.path;
        const baseUrl = await this.context.urlResolver.getDownloadUrl(path);
        // Set the base href, plus a fake name for the url of this
        // document. The fake name doesn't really matter, as long
        // as the document can dereference relative links to resources
        // (e.g. CSS and scripts).
        base.href = baseUrl;
        base.target = '_self';
        // Inject dynamic style for links if the document is not trusted
        if (!this.trusted) {
            const trans = this.translator.load('jupyterlab');
            const warning = trans.__('Action disabled as the file is not trusted.');
            doc.body.insertAdjacentHTML('beforeend', UNTRUSTED_LINK_STYLE({ warning }));
        }
        return doc.documentElement.innerHTML;
    }
}
/**
 * A widget factory for HTMLViewers.
 */
class HTMLViewerFactory extends docregistry_lib_index_js_.ABCWidgetFactory {
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        return new HTMLViewer({ context });
    }
    /**
     * Default factory for toolbar items to be added after the widget is created.
     */
    defaultToolbarFactory(widget) {
        return [
            // Make a refresh button for the toolbar.
            {
                name: 'refresh',
                widget: ToolbarItems.createRefreshButton(widget, this.translator)
            },
            // Make a trust button for the toolbar.
            {
                name: 'trust',
                widget: ToolbarItems.createTrustButton(widget, this.translator)
            }
        ];
    }
}
/**
 * A namespace for toolbar items generator
 */
var ToolbarItems;
(function (ToolbarItems) {
    /**
     * Create the refresh button
     *
     * @param widget HTML viewer widget
     * @param translator Application translator object
     * @returns Toolbar item button
     */
    function createRefreshButton(widget, translator) {
        const trans = (translator !== null && translator !== void 0 ? translator : translation_lib_index_js_.nullTranslator).load('jupyterlab');
        return new ui_components_lib_index_js_.ToolbarButton({
            icon: ui_components_lib_index_js_.refreshIcon,
            onClick: async () => {
                if (!widget.context.model.dirty) {
                    await widget.context.revert();
                    widget.update();
                }
            },
            tooltip: trans.__('Rerender HTML Document')
        });
    }
    ToolbarItems.createRefreshButton = createRefreshButton;
    /**
     * Create the trust button
     *
     * @param document HTML viewer widget
     * @param translator Application translator object
     * @returns Toolbar item button
     */
    function createTrustButton(document, translator) {
        return ui_components_lib_index_js_.ReactWidget.create(react_index_js_.createElement(Private.TrustButtonComponent, { htmlDocument: document, translator: translator }));
    }
    ToolbarItems.createTrustButton = createTrustButton;
})(ToolbarItems || (ToolbarItems = {}));
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * Sandbox exceptions for untrusted HTML.
     */
    Private.untrusted = [];
    /**
     * Sandbox exceptions for trusted HTML.
     */
    Private.trusted = [
        'allow-scripts',
        'allow-popups'
    ];
    /**
     * React component for a trusted button.
     *
     * This wraps the ToolbarButtonComponent and watches for trust changes.
     */
    function TrustButtonComponent(props) {
        const translator = props.translator || translation_lib_index_js_.nullTranslator;
        const trans = translator.load('jupyterlab');
        return (react_index_js_.createElement(ui_components_lib_index_js_.UseSignal, { signal: props.htmlDocument.trustedChanged, initialSender: props.htmlDocument }, () => (react_index_js_.createElement(ui_components_lib_index_js_.ToolbarButtonComponent, { className: "", onClick: () => (props.htmlDocument.trusted = !props.htmlDocument.trusted), tooltip: trans.__(`Whether the HTML file is trusted.
Trusting the file allows opening pop-ups and running scripts
which may result in security risks.
Only enable for files you trust.`), label: props.htmlDocument.trusted
                ? trans.__('Distrust HTML')
                : trans.__('Trust HTML') }))));
    }
    Private.TrustButtonComponent = TrustButtonComponent;
})(Private || (Private = {}));

;// CONCATENATED MODULE: ../packages/htmlviewer/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module htmlviewer
 */




/***/ })

}]);
//# sourceMappingURL=3309.4e25eb28b1dc85e807f6.js.map?v=4e25eb28b1dc85e807f6