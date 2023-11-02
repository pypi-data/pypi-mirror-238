"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[666],{

/***/ 37634:
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

var __webpack_unused_export__;


var m = __webpack_require__(40510);
if (true) {
  exports.s = m.createRoot;
  __webpack_unused_export__ = m.hydrateRoot;
} else { var i; }


/***/ }),

/***/ 80666:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MIME_TYPE": () => (/* binding */ MIME_TYPE),
/* harmony export */   "MIME_TYPES_JSONL": () => (/* binding */ MIME_TYPES_JSONL),
/* harmony export */   "RenderedJSON": () => (/* binding */ RenderedJSON),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "rendererFactory": () => (/* binding */ rendererFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(82545);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(72234);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(52850);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var react_dom_client__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(37634);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module json-extension
 */





/**
 * The CSS class to add to the JSON Widget.
 */
const CSS_CLASS = 'jp-RenderedJSON';
/**
 * The MIME type for JSON.
 */
const MIME_TYPE = 'application/json';
// NOTE: not standardized yet
const MIME_TYPES_JSONL = [
    'text/jsonl',
    'application/jsonl',
    'application/json-lines'
];
/**
 * A renderer for JSON data.
 */
class RenderedJSON extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget {
    /**
     * Create a new widget for rendering JSON.
     */
    constructor(options) {
        super();
        this._rootDOM = null;
        this.addClass(CSS_CLASS);
        this.addClass('CodeMirror');
        this._mimeType = options.mimeType;
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
    }
    [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Printing.symbol]() {
        return () => _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Printing.printWidget(this);
    }
    /**
     * Render JSON into this widget's node.
     */
    async renderModel(model) {
        const { Component } = await Promise.all(/* import() */[__webpack_require__.e(2100), __webpack_require__.e(6351), __webpack_require__.e(9239), __webpack_require__.e(5460), __webpack_require__.e(2111), __webpack_require__.e(547)]).then(__webpack_require__.bind(__webpack_require__, 10547));
        let data;
        // handle if json-lines format
        if (MIME_TYPES_JSONL.indexOf(this._mimeType) >= 0) {
            // convert into proper json
            const lines = (model.data[this._mimeType] || '')
                .trim()
                .split(/\n/);
            data = JSON.parse(`[${lines.join(',')}]`);
        }
        else {
            data = (model.data[this._mimeType] || {});
        }
        const metadata = (model.metadata[this._mimeType] || {});
        if (this._rootDOM === null) {
            this._rootDOM = (0,react_dom_client__WEBPACK_IMPORTED_MODULE_4__/* .createRoot */ .s)(this.node);
        }
        return new Promise((resolve, reject) => {
            this._rootDOM.render(react__WEBPACK_IMPORTED_MODULE_3__.createElement(Component, { data: data, metadata: metadata, translator: this.translator, forwardedRef: () => resolve() }));
        });
    }
    /**
     * Called before the widget is detached from the DOM.
     */
    onBeforeDetach(msg) {
        // Unmount the component so it can tear down.
        if (this._rootDOM) {
            this._rootDOM.unmount();
            this._rootDOM = null;
        }
    }
}
/**
 * A mime renderer factory for JSON data.
 */
const rendererFactory = {
    safe: true,
    mimeTypes: [MIME_TYPE, ...MIME_TYPES_JSONL],
    createRenderer: options => new RenderedJSON(options)
};
const extensions = [
    {
        id: '@jupyterlab/json-extension:factory',
        description: 'Adds renderer for JSON content.',
        rendererFactory,
        rank: 0,
        dataType: 'json',
        documentWidgetFactoryOptions: {
            name: 'JSON',
            // TODO: how to translate label of the factory?
            primaryFileType: 'json',
            fileTypes: ['json', 'notebook', 'geojson'],
            defaultFor: ['json']
        }
    },
    {
        id: '@jupyterlab/json-lines-extension:factory',
        description: 'Adds renderer for JSONLines content.',
        rendererFactory,
        rank: 0,
        dataType: 'string',
        documentWidgetFactoryOptions: {
            name: 'JSONLines',
            primaryFileType: 'jsonl',
            fileTypes: ['jsonl', 'ndjson'],
            defaultFor: ['jsonl', 'ndjson']
        }
    }
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extensions);


/***/ })

}]);
//# sourceMappingURL=666.dd1c1834d3d780d953a9.js.map?v=dd1c1834d3d780d953a9