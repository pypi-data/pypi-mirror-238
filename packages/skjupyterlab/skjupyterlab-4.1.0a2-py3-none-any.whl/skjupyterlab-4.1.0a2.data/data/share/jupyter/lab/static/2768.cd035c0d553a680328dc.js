"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[2768,1123],{

/***/ 91123:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "createMarkdownParser": () => (/* binding */ createMarkdownParser),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(22100);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(78254);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(29239);
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(66866);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(85707);
/* harmony import */ var _jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_4__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module markedparser-extension
 */





// highlight cache key separator
const FENCE = '```~~~';
/**
 * Create a markdown parser
 *
 * @param languages Editor languages
 * @returns Markdown parser
 */
function createMarkdownParser(languages, options) {
    return {
        render: (content) => {
            return Private.render(content, languages, options);
        }
    };
}
/**
 * The markdown parser plugin.
 */
const plugin = {
    id: '@jupyterlab/markedparser-extension:plugin',
    description: 'Provides the Markdown parser.',
    autoStart: true,
    provides: _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__.IMarkdownParser,
    requires: [_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.IEditorLanguageRegistry],
    optional: [_jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_4__.IMermaidMarkdown],
    activate: (app, languages, mermaidMarkdown) => {
        return createMarkdownParser(languages, {
            blocks: mermaidMarkdown ? [mermaidMarkdown] : []
        });
    }
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * A namespace for private marked functions
 */
var Private;
(function (Private) {
    let _initializing = null;
    let _marked = null;
    let _blocks = [];
    let _languages = null;
    let _markedOptions = {};
    let _highlights = new _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.LruCache();
    async function render(content, languages, options) {
        _languages = languages;
        if (!_marked) {
            _marked = await initializeMarked(options);
        }
        return _marked(content, _markedOptions);
    }
    Private.render = render;
    /**
     * Load marked lazily and exactly once.
     */
    async function initializeMarked(options) {
        if (_marked) {
            return _marked;
        }
        if (_initializing) {
            return await _initializing.promise;
        }
        // order blocks by `rank`
        _blocks = (options === null || options === void 0 ? void 0 : options.blocks) || [];
        _blocks = _blocks.sort((a, b) => { var _a, _b; return ((_a = a.rank) !== null && _a !== void 0 ? _a : Infinity) - ((_b = b.rank) !== null && _b !== void 0 ? _b : Infinity); });
        _initializing = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.PromiseDelegate();
        // load marked lazily, and exactly once
        const [{ marked, Renderer }, plugins] = await Promise.all([
            __webpack_require__.e(/* import() */ 2922).then(__webpack_require__.t.bind(__webpack_require__, 72922, 23)),
            loadMarkedPlugins()
        ]);
        // use load marked plugins
        for (const plugin of plugins) {
            marked.use(plugin);
        }
        // finish marked configuration
        _markedOptions = {
            // use the explicit async paradigm for `walkTokens`
            async: true,
            // enable all built-in GitHub-flavored Markdown opinions
            gfm: true,
            // asynchronously prepare for any special tokens, like highlighting and mermaid
            walkTokens,
            // use custom renderer
            renderer: makeRenderer(Renderer)
        };
        // complete initialization
        _marked = marked;
        _initializing.resolve(_marked);
        return _marked;
    }
    Private.initializeMarked = initializeMarked;
    /**
     * Load and use marked plugins.
     *
     * As of writing, both of these features would work without plugins, but emit
     * deprecation warnings.
     */
    async function loadMarkedPlugins() {
        // use loaded marked plugins
        return Promise.all([
            (async () => (await __webpack_require__.e(/* import() */ 4152).then(__webpack_require__.t.bind(__webpack_require__, 24152, 23))).gfmHeadingId())(),
            (async () => (await __webpack_require__.e(/* import() */ 9853).then(__webpack_require__.t.bind(__webpack_require__, 29853, 23))).mangle())()
        ]);
    }
    /**
     * Build a custom marked renderer.
     */
    function makeRenderer(Renderer_) {
        const renderer = new Renderer_();
        const originalCode = renderer.code;
        renderer.code = (code, language) => {
            // handle block renderers
            for (const block of _blocks) {
                if (block.languages.includes(language)) {
                    const rendered = block.render(code);
                    if (rendered != null) {
                        return rendered;
                    }
                }
            }
            // handle known highlighting
            const key = `${language}${FENCE}${code}${FENCE}`;
            const highlight = _highlights.get(key);
            if (highlight != null) {
                return highlight;
            }
            // fall back to calling with the renderer as `this`
            return originalCode.call(renderer, code, language);
        };
        return renderer;
    }
    /**
     * Apply and cache syntax highlighting for code blocks.
     */
    async function highlight(token) {
        const { lang, text } = token;
        if (!lang || !_languages) {
            // no language(s), no highlight
            return;
        }
        const key = `${lang}${FENCE}${text}${FENCE}`;
        if (_highlights.get(key)) {
            // already cached, don't make another DOM element
            return;
        }
        const el = document.createElement('div');
        try {
            await _languages.highlight(text, _languages.findBest(lang), el);
            const html = `<pre><code class="language-${lang}">${el.innerHTML}</code></pre>`;
            _highlights.set(key, html);
        }
        catch (err) {
            console.error(`Failed to highlight ${lang} code`, err);
        }
        finally {
            el.remove();
        }
    }
    /**
     * After parsing, lazily load and render or highlight code blocks
     */
    async function walkTokens(token) {
        switch (token.type) {
            case 'code':
                if (token.lang) {
                    for (const block of _blocks) {
                        if (block.languages.includes(token.lang)) {
                            await block.walk(token.text);
                            return;
                        }
                    }
                }
                await highlight(token);
        }
    }
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=2768.cd035c0d553a680328dc.js.map?v=cd035c0d553a680328dc