"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[1940],{

/***/ 1940:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "DETAILS_CLASS": () => (/* reexport */ DETAILS_CLASS),
  "IMermaidManager": () => (/* reexport */ IMermaidManager),
  "IMermaidMarkdown": () => (/* reexport */ IMermaidMarkdown),
  "MERMAID_CLASS": () => (/* reexport */ MERMAID_CLASS),
  "MERMAID_CODE_CLASS": () => (/* reexport */ MERMAID_CODE_CLASS),
  "MERMAID_DARK_THEME": () => (/* reexport */ MERMAID_DARK_THEME),
  "MERMAID_DEFAULT_THEME": () => (/* reexport */ MERMAID_DEFAULT_THEME),
  "MERMAID_FILE_EXTENSIONS": () => (/* reexport */ MERMAID_FILE_EXTENSIONS),
  "MERMAID_MIME_TYPE": () => (/* reexport */ MERMAID_MIME_TYPE),
  "MermaidManager": () => (/* reexport */ MermaidManager),
  "MermaidMarkdown": () => (/* reexport */ MermaidMarkdown),
  "RenderedMermaid": () => (/* reexport */ RenderedMermaid),
  "SUMMARY_CLASS": () => (/* reexport */ SUMMARY_CLASS),
  "WARNING_CLASS": () => (/* reexport */ WARNING_CLASS),
  "rendererFactory": () => (/* reexport */ rendererFactory)
});

// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var lib_index_js_ = __webpack_require__(78254);
;// CONCATENATED MODULE: ../packages/mermaid/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

// documented upstream constants
const MERMAID_MIME_TYPE = 'text/vnd.mermaid';
const MERMAID_FILE_EXTENSIONS = ['.mmd', '.mermaid'];
// mermaid themes
const MERMAID_DEFAULT_THEME = 'default';
const MERMAID_DARK_THEME = 'dark';
// DOM
const MERMAID_CLASS = 'jp-RenderedMermaid';
const MERMAID_CODE_CLASS = 'mermaid';
const WARNING_CLASS = 'jp-mod-warning';
const DETAILS_CLASS = 'jp-RenderedMermaid-Details';
const SUMMARY_CLASS = 'jp-RenderedMermaid-Summary';
/**
 * The exported token for a mermaid manager
 */
const IMermaidManager = new index_js_.Token('@jupyterlab/mermaid:IMermaidManager', `a manager for rendering mermaid text-based diagrams`);
/**
 * The exported token for a mermaid manager
 */
const IMermaidMarkdown = new index_js_.Token('@jupyterlab/mermaid:IMermaidMarkdown', `a manager for rendering mermaid text-based diagrams in markdown fenced code blocks`);

;// CONCATENATED MODULE: ../packages/mermaid/lib/manager.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * A mermaid diagram manager with cache.
 */
class MermaidManager {
    constructor(options = {}) {
        this._diagrams = new lib_index_js_.LruCache({ maxSize: options.maxCacheSize || null });
        // handle reacting to themes
        if (options.themes) {
            Private.initThemes(options.themes || null);
            options.themes.themeChanged.connect(this.initialize, this);
        }
    }
    /**
     * Handle (re)-initializing mermaid based on external values.
     */
    initialize() {
        this._diagrams.clear();
        Private.initMermaid();
    }
    /**
     * Get the underlying, potentially un-initialized mermaid module.
     */
    async getMermaid() {
        return await Private.ensureMermaid();
    }
    /**
     * Get the version of the currently-loaded mermaid module
     */
    getMermaidVersion() {
        return Private.version();
    }
    /**
     * Get a pre-cached mermaid figure.
     *
     * This primarily exists for the needs of `marked`, which supports async node
     * visitors, but not async rendering.
     */
    getCachedFigure(text) {
        return this._diagrams.get(text);
    }
    /**
     * Attempt a raw rendering of mermaid to an SVG string, extracting some metadata.
     */
    async renderSvg(text) {
        const _mermaid = await this.getMermaid();
        const id = `jp-mermaid-${Private.nextMermaidId()}`;
        // create temporary element into which to render
        const el = document.createElement('div');
        document.body.appendChild(el);
        try {
            const { svg } = await _mermaid.render(id, text, el);
            const parser = new DOMParser();
            const doc = parser.parseFromString(svg, 'image/svg+xml');
            const info = { text, svg };
            const svgEl = doc.querySelector('svg');
            const { maxWidth } = (svgEl === null || svgEl === void 0 ? void 0 : svgEl.style) || {};
            info.width = maxWidth ? parseFloat(maxWidth) : null;
            const firstTitle = doc.querySelector('title');
            const firstDesc = doc.querySelector('desc');
            if (firstTitle) {
                info.accessibleTitle = firstTitle.textContent;
            }
            if (firstDesc) {
                info.accessibleDescription = firstDesc.textContent;
            }
            return info;
        }
        finally {
            el.remove();
        }
    }
    /**
     * Provide and cache a fully-rendered element, checking the cache first.
     */
    async renderFigure(text) {
        // bail if already cached
        let output = this._diagrams.get(text);
        if (output != null) {
            return output;
        }
        let className = MERMAID_CLASS;
        let result = null;
        // the element that will be returned
        output = document.createElement('div');
        output.className = className;
        try {
            const response = await this.renderSvg(text);
            result = this.makeMermaidFigure(response);
        }
        catch (err) {
            output.classList.add(WARNING_CLASS);
            result = await this.makeMermaidError(text);
        }
        let version = this.getMermaidVersion();
        if (version) {
            result.dataset.jpMermaidVersion = version;
        }
        output.appendChild(result);
        // update the cache for use when rendering synchronously
        this._diagrams.set(text, output);
        return output;
    }
    /**
     * Provide a code block with the mermaid source.
     */
    makeMermaidCode(text) {
        // append the source
        const pre = document.createElement('pre');
        const code = document.createElement('code');
        code.innerText = text;
        pre.appendChild(code);
        code.className = MERMAID_CODE_CLASS;
        code.textContent = text;
        return pre;
    }
    /**
     * Get the parser message element from a failed parse.
     *
     * This doesn't do much of anything if the text is successfully parsed.
     */
    async makeMermaidError(text) {
        const _mermaid = await this.getMermaid();
        let errorMessage = '';
        try {
            await _mermaid.parse(text);
        }
        catch (err) {
            errorMessage = `${err}`;
        }
        const result = document.createElement('details');
        result.className = DETAILS_CLASS;
        const summary = document.createElement('summary');
        summary.className = SUMMARY_CLASS;
        summary.appendChild(this.makeMermaidCode(text));
        result.appendChild(summary);
        const warning = document.createElement('pre');
        warning.innerText = errorMessage;
        result.appendChild(warning);
        return result;
    }
    /**
     * Extract extra attributes to add to a generated figure.
     */
    makeMermaidFigure(info) {
        const figure = document.createElement('figure');
        const img = document.createElement('img');
        figure.appendChild(img);
        img.setAttribute('src', `data:image/svg+xml,${encodeURIComponent(info.svg)}`);
        // add dimension information
        if (info.width) {
            img.width = info.width;
        }
        // add accessible alt title
        if (info.accessibleTitle) {
            img.setAttribute('alt', info.accessibleTitle);
        }
        figure.appendChild(this.makeMermaidCode(info.text));
        // add accessible caption, with fallback to raw mermaid source
        if (info.accessibleDescription) {
            const caption = document.createElement('figcaption');
            caption.className = 'sr-only';
            caption.textContent = info.accessibleDescription;
            figure.appendChild(caption);
        }
        return figure;
    }
}
/**
 * A namespace for global, private mermaid data.
 */
var Private;
(function (Private) {
    let _themes = null;
    let _mermaid = null;
    let _loading = null;
    let _nextMermaidId = 0;
    let _version = null;
    /**
     * Cache a reference to the theme manager.
     */
    function initThemes(themes) {
        _themes = themes;
    }
    Private.initThemes = initThemes;
    /**
     * Get the version of mermaid used for rendering.
     */
    function version() {
        return _version;
    }
    Private.version = version;
    /**
     * (Re-)initialize mermaid with lab-specific theme information
     */
    function initMermaid() {
        if (!_mermaid) {
            return false;
        }
        let theme = MERMAID_DEFAULT_THEME;
        if (_themes) {
            const jpTheme = _themes.theme;
            theme =
                jpTheme && _themes.isLight(jpTheme)
                    ? MERMAID_DEFAULT_THEME
                    : MERMAID_DARK_THEME;
        }
        const fontFamily = window
            .getComputedStyle(document.body)
            .getPropertyValue('--jp-ui-font-family');
        _mermaid.mermaidAPI.globalReset();
        _mermaid.mermaidAPI.initialize({
            theme,
            fontFamily,
            maxTextSize: 100000,
            startOnLoad: false
        });
        return true;
    }
    Private.initMermaid = initMermaid;
    /**
     * Determine whether mermaid has been loaded yet.
     */
    function getMermaid() {
        return _mermaid;
    }
    Private.getMermaid = getMermaid;
    /**
     * Provide a globally-unique, but unstable, ID for disambiguation.
     */
    function nextMermaidId() {
        return _nextMermaidId++;
    }
    Private.nextMermaidId = nextMermaidId;
    /**
     * Ensure mermaid has been lazily loaded once, initialized, and cached.
     */
    async function ensureMermaid() {
        if (_mermaid != null) {
            return _mermaid;
        }
        if (_loading) {
            return _loading.promise;
        }
        _loading = new index_js_.PromiseDelegate();
        _version = (await __webpack_require__.e(/* import() */ 1169).then(__webpack_require__.t.bind(__webpack_require__, 21169, 19))).version;
        _mermaid = (await Promise.all(/* import() */[__webpack_require__.e(750), __webpack_require__.e(7764), __webpack_require__.e(4630)]).then(__webpack_require__.bind(__webpack_require__, 84630))).default;
        initMermaid();
        _loading.resolve(_mermaid);
        return _mermaid;
    }
    Private.ensureMermaid = ensureMermaid;
})(Private || (Private = {}));

;// CONCATENATED MODULE: ../packages/mermaid/lib/markdown.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * An implementation of mermaid fenced code blocks in markdown.
 */
class MermaidMarkdown {
    constructor(options) {
        this.languages = ['mermaid'];
        this.rank = 100;
        this._mermaid = options.mermaid;
    }
    /**
     * Pre-parse and cache the rendered text.
     */
    async walk(text) {
        await this._mermaid.renderFigure(text);
    }
    /**
     * Render the diagram.
     */
    render(text) {
        // handle pre-cached mermaid figures
        let cachedFigure = this._mermaid.getCachedFigure(text);
        if (cachedFigure) {
            return cachedFigure.outerHTML;
        }
        return null;
    }
}

// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/mermaid/lib/mime.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module mermaid-extension
 */



const SVG_MIME = 'image/svg+xml';
/**
 * A widget for rendering mermaid text-based diagrams, for usage with rendermime.
 */
class RenderedMermaid extends index_es6_js_.Widget {
    /**
     * Create a new widget for rendering Vega/Vega-Lite.
     */
    constructor(options) {
        super();
        this._lastRendered = null;
        this._mimeType = options.mimeType;
        this.addClass(MERMAID_CLASS);
    }
    static set manager(manager) {
        if (RenderedMermaid._manager) {
            console.warn('Mermaid manager may only be set once, and is already set.');
            return;
        }
        RenderedMermaid._manager = manager;
        RenderedMermaid._managerReady.resolve(manager);
    }
    /**
     * Render mermaid text-based diagrams into this widget's node.
     */
    async renderModel(model) {
        const manager = await RenderedMermaid._managerReady.promise;
        const text = model.data[this._mimeType];
        if (text == null || text === this._lastRendered) {
            return;
        }
        this._lastRendered = text;
        // get a div containing a figure or parser message
        const figure = await manager.renderFigure(text);
        if (figure.classList.contains(WARNING_CLASS)) {
            this.node.classList.add(WARNING_CLASS);
        }
        else {
            this.node.classList.remove(WARNING_CLASS);
        }
        if (!figure.firstChild) {
            return;
        }
        if (this.node.innerHTML !== figure.innerHTML) {
            this.node.innerHTML = figure.innerHTML;
        }
        // capture the version of mermaid used
        const version = manager.getMermaidVersion();
        const mermaidMetadata = {
            ...(model.metadata[MERMAID_MIME_TYPE] || {}),
            version
        };
        const metadata = {
            ...model.metadata,
            [MERMAID_MIME_TYPE]: mermaidMetadata
        };
        // if available, set the fully-rendered SVG
        const img = figure.querySelector('img');
        if (img) {
            const svg = decodeURIComponent(img.src.split(',')[1]);
            const oldSvg = model.data[SVG_MIME];
            if (svg !== oldSvg) {
                model.setData({
                    data: { ...model.data, [SVG_MIME]: svg },
                    metadata
                });
            }
        }
        else {
            const dataWithoutSvg = { ...model.data };
            delete dataWithoutSvg[SVG_MIME];
            model.setData({ data: dataWithoutSvg, metadata });
        }
    }
}
RenderedMermaid._manager = null;
RenderedMermaid._managerReady = new index_js_.PromiseDelegate();

/**
 * A mime renderer factory for mermaid text-based diagrams.
 */
const rendererFactory = {
    safe: true,
    mimeTypes: [MERMAID_MIME_TYPE],
    createRenderer: options => new RenderedMermaid(options)
};

;// CONCATENATED MODULE: ../packages/mermaid/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module mermaid
 */






/***/ })

}]);
//# sourceMappingURL=1940.0b5c7538d61c717b88a2.js.map?v=0b5c7538d61c717b88a2