"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[7984],{

/***/ 87984:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MathJaxTypesetter": () => (/* binding */ MathJaxTypesetter),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(22100);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(66866);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module mathjax-extension
 */


var CommandIDs;
(function (CommandIDs) {
    /**
     * Copy raw LaTeX to clipboard.
     */
    CommandIDs.copy = 'mathjax:clipboard';
    /**
     * Scale MathJax elements.
     */
    CommandIDs.scale = 'mathjax:scale';
})(CommandIDs || (CommandIDs = {}));
/**
 * The MathJax Typesetter.
 */
class MathJaxTypesetter {
    constructor() {
        this._initialized = false;
    }
    async _ensureInitialized() {
        if (!this._initialized) {
            this._mathDocument = await Private.ensureMathDocument();
            this._initialized = true;
        }
    }
    /**
     * Get an instance of the MathDocument object.
     */
    async mathDocument() {
        await this._ensureInitialized();
        return this._mathDocument;
    }
    /**
     * Typeset the math in a node.
     */
    async typeset(node) {
        try {
            await this._ensureInitialized();
        }
        catch (e) {
            console.error(e);
            return;
        }
        this._mathDocument.options.elements = [node];
        this._mathDocument.clear().render();
        delete this._mathDocument.options.elements;
    }
}
/**
 * The MathJax extension.
 */
const mathJaxPlugin = {
    id: '@jupyterlab/mathjax-extension:plugin',
    description: 'Provides the LaTeX mathematical expression interpreter.',
    provides: _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__.ILatexTypesetter,
    activate: (app) => {
        const typesetter = new MathJaxTypesetter();
        app.commands.addCommand(CommandIDs.copy, {
            execute: async () => {
                const md = await typesetter.mathDocument();
                const oJax = md.outputJax;
                await navigator.clipboard.writeText(oJax.math.math);
            },
            label: 'MathJax Copy Latex'
        });
        app.commands.addCommand(CommandIDs.scale, {
            execute: async (args) => {
                const md = await typesetter.mathDocument();
                const scale = args['scale'] || 1.0;
                md.outputJax.options.scale = scale;
                md.rerender();
            },
            label: args => 'Mathjax Scale ' + (args['scale'] ? `x${args['scale']}` : 'Reset')
        });
        return typesetter;
    },
    autoStart: true
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (mathJaxPlugin);
/**
 * A namespace for module-private functionality.
 */
var Private;
(function (Private) {
    let _loading = null;
    async function ensureMathDocument() {
        if (!_loading) {
            _loading = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.PromiseDelegate();
            void Promise.all(/* import() */[__webpack_require__.e(7969), __webpack_require__.e(5115), __webpack_require__.e(792)]).then(__webpack_require__.t.bind(__webpack_require__, 20792, 23));
            const [{ mathjax }, { CHTML }, { TeX }, { TeXFont }, { AllPackages }, { SafeHandler }, { HTMLHandler }, { browserAdaptor }, { AssistiveMmlHandler }] = await Promise.all([
                __webpack_require__.e(/* import() */ 4971).then(__webpack_require__.bind(__webpack_require__, 44971)),
                Promise.all(/* import() */[__webpack_require__.e(7969), __webpack_require__.e(28), __webpack_require__.e(2065), __webpack_require__.e(7369)]).then(__webpack_require__.t.bind(__webpack_require__, 57369, 23)),
                Promise.all(/* import() */[__webpack_require__.e(7969), __webpack_require__.e(5115), __webpack_require__.e(7154), __webpack_require__.e(7582)]).then(__webpack_require__.t.bind(__webpack_require__, 27582, 23)),
                Promise.all(/* import() */[__webpack_require__.e(2065), __webpack_require__.e(4498)]).then(__webpack_require__.t.bind(__webpack_require__, 42065, 23)),
                Promise.all(/* import() */[__webpack_require__.e(7969), __webpack_require__.e(5115), __webpack_require__.e(7154), __webpack_require__.e(8845)]).then(__webpack_require__.bind(__webpack_require__, 78845)),
                __webpack_require__.e(/* import() */ 8285).then(__webpack_require__.t.bind(__webpack_require__, 78285, 23)),
                Promise.all(/* import() */[__webpack_require__.e(7969), __webpack_require__.e(28), __webpack_require__.e(2666), __webpack_require__.e(7471)]).then(__webpack_require__.t.bind(__webpack_require__, 97471, 23)),
                __webpack_require__.e(/* import() */ 7713).then(__webpack_require__.bind(__webpack_require__, 90270)),
                Promise.all(/* import() */[__webpack_require__.e(7969), __webpack_require__.e(28), __webpack_require__.e(2666), __webpack_require__.e(4105)]).then(__webpack_require__.t.bind(__webpack_require__, 74105, 23))
            ]);
            mathjax.handlers.register(AssistiveMmlHandler(SafeHandler(new HTMLHandler(browserAdaptor()))));
            class EmptyFont extends TeXFont {
            }
            EmptyFont.defaultFonts = {};
            const chtml = new CHTML({
                // Override dynamically generated fonts in favor of our font css
                font: new EmptyFont()
            });
            const tex = new TeX({
                packages: AllPackages.concat('require'),
                inlineMath: [
                    ['$', '$'],
                    ['\\(', '\\)']
                ],
                displayMath: [
                    ['$$', '$$'],
                    ['\\[', '\\]']
                ],
                processEscapes: true,
                processEnvironments: true
            });
            const mathDocument = mathjax.document(window.document, {
                InputJax: tex,
                OutputJax: chtml
            });
            _loading.resolve(mathDocument);
        }
        return _loading.promise;
    }
    Private.ensureMathDocument = ensureMathDocument;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=7984.35ee462829f70ddf5842.js.map?v=35ee462829f70ddf5842