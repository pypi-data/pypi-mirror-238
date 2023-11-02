"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[8567,2577],{

/***/ 2577:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "IMarkdownViewerTracker": () => (/* reexport */ IMarkdownViewerTracker),
  "MarkdownDocument": () => (/* reexport */ MarkdownDocument),
  "MarkdownViewer": () => (/* reexport */ MarkdownViewer),
  "MarkdownViewerFactory": () => (/* reexport */ MarkdownViewerFactory),
  "MarkdownViewerTableOfContentsFactory": () => (/* reexport */ MarkdownViewerTableOfContentsFactory),
  "MarkdownViewerTableOfContentsModel": () => (/* reexport */ MarkdownViewerTableOfContentsModel)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/toc@~6.1.0-alpha.2 (singleton) (fallback: ../packages/toc/lib/index.js)
var index_js_ = __webpack_require__(95691);
;// CONCATENATED MODULE: ../packages/markdownviewer/lib/toc.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * Table of content model for Markdown viewer files.
 */
class MarkdownViewerTableOfContentsModel extends index_js_.TableOfContentsModel {
    /**
     * Constructor
     *
     * @param widget The widget to search in
     * @param parser Markdown parser
     * @param configuration Default model configuration
     */
    constructor(widget, parser, configuration) {
        super(widget, configuration);
        this.parser = parser;
    }
    /**
     * Type of document supported by the model.
     *
     * #### Notes
     * A `data-document-type` attribute with this value will be set
     * on the tree view `.jp-TableOfContents-content[data-document-type="..."]`
     */
    get documentType() {
        return 'markdown-viewer';
    }
    /**
     * Whether the model gets updated even if the table of contents panel
     * is hidden or not.
     */
    get isAlwaysActive() {
        return true;
    }
    /**
     * List of configuration options supported by the model.
     */
    get supportedOptions() {
        return ['maximalDepth', 'numberingH1', 'numberHeaders'];
    }
    /**
     * Produce the headings for a document.
     *
     * @returns The list of new headings or `null` if nothing needs to be updated.
     */
    getHeadings() {
        const content = this.widget.context.model.toString();
        const headings = index_js_.TableOfContentsUtils.filterHeadings(index_js_.TableOfContentsUtils.Markdown.getHeadings(content), {
            ...this.configuration,
            // Force base number to be equal to 1
            baseNumbering: 1
        });
        return Promise.resolve(headings);
    }
}
/**
 * Table of content model factory for Markdown viewer files.
 */
class MarkdownViewerTableOfContentsFactory extends index_js_.TableOfContentsFactory {
    /**
     * Constructor
     *
     * @param tracker Widget tracker
     * @param parser Markdown parser
     */
    constructor(tracker, parser) {
        super(tracker);
        this.parser = parser;
    }
    /**
     * Create a new table of contents model for the widget
     *
     * @param widget - widget
     * @param configuration - Table of contents configuration
     * @returns The table of contents model
     */
    _createNew(widget, configuration) {
        const model = new MarkdownViewerTableOfContentsModel(widget, this.parser, configuration);
        let headingToElement = new WeakMap();
        const onActiveHeadingChanged = (model, heading) => {
            if (heading) {
                const el = headingToElement.get(heading);
                if (el) {
                    const widgetBox = widget.content.node.getBoundingClientRect();
                    const elementBox = el.getBoundingClientRect();
                    if (elementBox.top > widgetBox.bottom ||
                        elementBox.bottom < widgetBox.top) {
                        el.scrollIntoView({ block: 'center' });
                    }
                }
                else {
                    console.warn('Heading element not found for heading', heading, 'in widget', widget);
                }
            }
        };
        const onHeadingsChanged = () => {
            if (!this.parser) {
                return;
            }
            // Clear all numbering items
            index_js_.TableOfContentsUtils.clearNumbering(widget.content.node);
            // Create a new mapping
            headingToElement = new WeakMap();
            model.headings.forEach(async (heading) => {
                var _a;
                const elementId = await index_js_.TableOfContentsUtils.Markdown.getHeadingId(this.parser, heading.raw, heading.level);
                if (!elementId) {
                    return;
                }
                const selector = `h${heading.level}[id="${elementId}"]`;
                headingToElement.set(heading, index_js_.TableOfContentsUtils.addPrefix(widget.content.node, selector, (_a = heading.prefix) !== null && _a !== void 0 ? _a : ''));
            });
        };
        void widget.content.ready.then(() => {
            onHeadingsChanged();
            widget.content.rendered.connect(onHeadingsChanged);
            model.activeHeadingChanged.connect(onActiveHeadingChanged);
            model.headingsChanged.connect(onHeadingsChanged);
            widget.disposed.connect(() => {
                widget.content.rendered.disconnect(onHeadingsChanged);
                model.activeHeadingChanged.disconnect(onActiveHeadingChanged);
                model.headingsChanged.disconnect(onHeadingsChanged);
            });
        });
        return model;
    }
}

// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
;// CONCATENATED MODULE: ../packages/markdownviewer/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The markdownviewer tracker token.
 */
const IMarkdownViewerTracker = new dist_index_js_.Token('@jupyterlab/markdownviewer:IMarkdownViewerTracker', `A widget tracker for markdown
  document viewers. Use this if you want to iterate over and interact with rendered markdown documents.`);

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var lib_index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var coreutils_lib_index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/docregistry@~4.1.0-alpha.2 (strict) (fallback: ../packages/docregistry/lib/index.js)
var docregistry_lib_index_js_ = __webpack_require__(16564);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/rendermime@~4.1.0-alpha.2 (singleton) (fallback: ../packages/rendermime/lib/index.js)
var rendermime_lib_index_js_ = __webpack_require__(66866);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(30205);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/markdownviewer/lib/widget.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








/**
 * The class name added to a markdown viewer.
 */
const MARKDOWNVIEWER_CLASS = 'jp-MarkdownViewer';
/**
 * The markdown MIME type.
 */
const MIMETYPE = 'text/markdown';
/**
 * A widget for markdown documents.
 */
class MarkdownViewer extends dist_index_es6_js_.Widget {
    /**
     * Construct a new markdown viewer widget.
     */
    constructor(options) {
        super();
        this._config = { ...MarkdownViewer.defaultConfig };
        this._fragment = '';
        this._ready = new dist_index_js_.PromiseDelegate();
        this._isRendering = false;
        this._renderRequested = false;
        this._rendered = new index_es6_js_.Signal(this);
        this.context = options.context;
        this.translator = options.translator || translation_lib_index_js_.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this.renderer = options.renderer;
        this.node.tabIndex = 0;
        this.addClass(MARKDOWNVIEWER_CLASS);
        const layout = (this.layout = new dist_index_es6_js_.StackedLayout());
        layout.addWidget(this.renderer);
        void this.context.ready.then(async () => {
            await this._render();
            // Throttle the rendering rate of the widget.
            this._monitor = new coreutils_lib_index_js_.ActivityMonitor({
                signal: this.context.model.contentChanged,
                timeout: this._config.renderTimeout
            });
            this._monitor.activityStopped.connect(this.update, this);
            this._ready.resolve(undefined);
        });
    }
    /**
     * A promise that resolves when the markdown viewer is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * Signal emitted when the content has been rendered.
     */
    get rendered() {
        return this._rendered;
    }
    /**
     * Set URI fragment identifier.
     */
    setFragment(fragment) {
        this._fragment = fragment;
        this.update();
    }
    /**
     * Set a config option for the markdown viewer.
     */
    setOption(option, value) {
        if (this._config[option] === value) {
            return;
        }
        this._config[option] = value;
        const { style } = this.renderer.node;
        switch (option) {
            case 'fontFamily':
                style.setProperty('font-family', value);
                break;
            case 'fontSize':
                style.setProperty('font-size', value ? value + 'px' : null);
                break;
            case 'hideFrontMatter':
                this.update();
                break;
            case 'lineHeight':
                style.setProperty('line-height', value ? value.toString() : null);
                break;
            case 'lineWidth': {
                const padding = value ? `calc(50% - ${value / 2}ch)` : null;
                style.setProperty('padding-left', padding);
                style.setProperty('padding-right', padding);
                break;
            }
            case 'renderTimeout':
                if (this._monitor) {
                    this._monitor.timeout = value;
                }
                break;
            default:
                break;
        }
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
        if (this.context.isReady && !this.isDisposed) {
            void this._render();
            this._fragment = '';
        }
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        this.node.focus();
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
        const { context } = this;
        const { model } = context;
        const source = model.toString();
        const data = {};
        // If `hideFrontMatter`is true remove front matter.
        data[MIMETYPE] = this._config.hideFrontMatter
            ? Private.removeFrontMatter(source)
            : source;
        const mimeModel = new rendermime_lib_index_js_.MimeModel({
            data,
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
            else {
                this._rendered.emit();
            }
        }
        catch (reason) {
            // Dispose the document if rendering fails.
            requestAnimationFrame(() => {
                this.dispose();
            });
            void (0,lib_index_js_.showErrorMessage)(this._trans.__('Renderer Failure: %1', context.path), reason);
        }
    }
}
/**
 * The namespace for MarkdownViewer class statics.
 */
(function (MarkdownViewer) {
    /**
     * The default configuration options for an editor.
     */
    MarkdownViewer.defaultConfig = {
        fontFamily: null,
        fontSize: null,
        lineHeight: null,
        lineWidth: null,
        hideFrontMatter: true,
        renderTimeout: 1000
    };
})(MarkdownViewer || (MarkdownViewer = {}));
/**
 * A document widget for markdown content.
 */
class MarkdownDocument extends docregistry_lib_index_js_.DocumentWidget {
    setFragment(fragment) {
        this.content.setFragment(fragment);
    }
}
/**
 * A widget factory for markdown viewers.
 */
class MarkdownViewerFactory extends docregistry_lib_index_js_.ABCWidgetFactory {
    /**
     * Construct a new markdown viewer widget factory.
     */
    constructor(options) {
        super(Private.createRegistryOptions(options));
        this._fileType = options.primaryFileType;
        this._rendermime = options.rendermime;
    }
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        var _a, _b, _c, _d, _e;
        const rendermime = this._rendermime.clone({
            resolver: context.urlResolver
        });
        const renderer = rendermime.createRenderer(MIMETYPE);
        const content = new MarkdownViewer({ context, renderer });
        content.title.icon = (_a = this._fileType) === null || _a === void 0 ? void 0 : _a.icon;
        content.title.iconClass = (_c = (_b = this._fileType) === null || _b === void 0 ? void 0 : _b.iconClass) !== null && _c !== void 0 ? _c : '';
        content.title.iconLabel = (_e = (_d = this._fileType) === null || _d === void 0 ? void 0 : _d.iconLabel) !== null && _e !== void 0 ? _e : '';
        content.title.caption = this.label;
        const widget = new MarkdownDocument({ content, context });
        return widget;
    }
}
/**
 * A namespace for markdown viewer widget private data.
 */
var Private;
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
    /**
     * Remove YAML front matter from source.
     */
    function removeFrontMatter(source) {
        const re = /^---\n[^]*?\n(---|...)\n/;
        const match = source.match(re);
        if (!match) {
            return source;
        }
        const { length } = match[0];
        return source.slice(length);
    }
    Private.removeFrontMatter = removeFrontMatter;
})(Private || (Private = {}));

;// CONCATENATED MODULE: ../packages/markdownviewer/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module markdownviewer
 */





/***/ })

}]);
//# sourceMappingURL=8567.00248d6972c5efd2f96f.js.map?v=00248d6972c5efd2f96f