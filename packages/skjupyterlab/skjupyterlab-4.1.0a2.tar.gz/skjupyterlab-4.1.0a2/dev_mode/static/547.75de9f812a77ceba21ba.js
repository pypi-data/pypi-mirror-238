"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[547],{

/***/ 10547:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Component": () => (/* binding */ Component)
/* harmony export */ });
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(29239);
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(76351);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lezer_highlight__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(25460);
/* harmony import */ var _lezer_highlight__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lezer_highlight__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(22100);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(52850);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var react_highlight_words__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(16934);
/* harmony import */ var react_highlight_words__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(react_highlight_words__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var react_json_tree__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(55807);
/* harmony import */ var react_json_tree__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(react_json_tree__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var style_mod__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(22111);
/* harmony import */ var style_mod__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(style_mod__WEBPACK_IMPORTED_MODULE_8__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.









/**
 * Get the CodeMirror style for a given tag.
 */
function getStyle(tag) {
    var _a;
    return (_a = _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_0__.jupyterHighlightStyle.style([tag])) !== null && _a !== void 0 ? _a : '';
}
/**
 * A component that renders JSON data as a collapsible tree.
 */
class Component extends react__WEBPACK_IMPORTED_MODULE_5__.Component {
    constructor() {
        super(...arguments);
        this.state = { filter: '', value: '' };
        this.timer = 0;
        this.handleChange = (event) => {
            const { value } = event.target;
            this.setState({ value });
            window.clearTimeout(this.timer);
            this.timer = window.setTimeout(() => {
                this.setState({ filter: value });
            }, 300);
        };
    }
    componentDidMount() {
        style_mod__WEBPACK_IMPORTED_MODULE_8__.StyleModule.mount(document, _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_0__.jupyterHighlightStyle.module);
    }
    render() {
        const translator = this.props.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        const trans = translator.load('jupyterlab');
        const { data, metadata, forwardedRef } = this.props;
        const root = metadata && metadata.root ? metadata.root : 'root';
        const keyPaths = this.state.filter
            ? filterPaths(data, this.state.filter, [root])
            : [root];
        return (react__WEBPACK_IMPORTED_MODULE_5__.createElement("div", { className: "container", ref: forwardedRef },
            react__WEBPACK_IMPORTED_MODULE_5__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.InputGroup, { className: "filter", type: "text", placeholder: trans.__('Filter…'), onChange: this.handleChange, value: this.state.value, rightIcon: "ui-components:search" }),
            react__WEBPACK_IMPORTED_MODULE_5__.createElement(react_json_tree__WEBPACK_IMPORTED_MODULE_7__.JSONTree, { data: data, collectionLimit: 100, theme: {
                    extend: theme,
                    valueLabel: getStyle(_lezer_highlight__WEBPACK_IMPORTED_MODULE_3__.tags.variableName),
                    valueText: getStyle(_lezer_highlight__WEBPACK_IMPORTED_MODULE_3__.tags.string),
                    nestedNodeItemString: getStyle(_lezer_highlight__WEBPACK_IMPORTED_MODULE_3__.tags.comment)
                }, invertTheme: false, keyPath: [root], getItemString: (type, data, itemType, itemString) => Array.isArray(data) ? (
                // Always display array type and the number of items i.e. "[] 2 items".
                react__WEBPACK_IMPORTED_MODULE_5__.createElement("span", null,
                    itemType,
                    " ",
                    itemString)) : Object.keys(data).length === 0 ? (
                // Only display object type when it's empty i.e. "{}".
                react__WEBPACK_IMPORTED_MODULE_5__.createElement("span", null, itemType)) : (null // Upstream typings don't accept null, but it should be ok
                ), labelRenderer: ([label, type]) => {
                    return (react__WEBPACK_IMPORTED_MODULE_5__.createElement("span", { className: getStyle(_lezer_highlight__WEBPACK_IMPORTED_MODULE_3__.tags.keyword) },
                        react__WEBPACK_IMPORTED_MODULE_5__.createElement((react_highlight_words__WEBPACK_IMPORTED_MODULE_6___default()), { searchWords: [this.state.filter], textToHighlight: `${label}`, highlightClassName: "jp-mod-selected" })));
                }, valueRenderer: raw => {
                    let className = getStyle(_lezer_highlight__WEBPACK_IMPORTED_MODULE_3__.tags.string);
                    if (typeof raw === 'number') {
                        className = getStyle(_lezer_highlight__WEBPACK_IMPORTED_MODULE_3__.tags.number);
                    }
                    if (raw === 'true' || raw === 'false') {
                        className = getStyle(_lezer_highlight__WEBPACK_IMPORTED_MODULE_3__.tags.keyword);
                    }
                    return (react__WEBPACK_IMPORTED_MODULE_5__.createElement("span", { className: className },
                        react__WEBPACK_IMPORTED_MODULE_5__.createElement((react_highlight_words__WEBPACK_IMPORTED_MODULE_6___default()), { searchWords: [this.state.filter], textToHighlight: `${raw}`, highlightClassName: "jp-mod-selected" })));
                }, shouldExpandNodeInitially: (keyPath, data, level) => metadata && metadata.expanded
                    ? true
                    : keyPaths.join(',').includes(keyPath.join(',')) })));
    }
}
// Provide an invalid theme object (this is on purpose!) to invalidate the
// react-json-tree's inline styles that override CodeMirror CSS classes
const theme = {
    scheme: 'jupyter',
    base00: 'invalid',
    base01: 'invalid',
    base02: 'invalid',
    base03: 'invalid',
    base04: 'invalid',
    base05: 'invalid',
    base06: 'invalid',
    base07: 'invalid',
    base08: 'invalid',
    base09: 'invalid',
    base0A: 'invalid',
    base0B: 'invalid',
    base0C: 'invalid',
    base0D: 'invalid',
    base0E: 'invalid',
    base0F: 'invalid',
    author: 'invalid'
};
function objectIncludes(data, query) {
    return JSON.stringify(data).includes(query);
}
function filterPaths(data, query, parent = ['root']) {
    if (_lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.JSONExt.isArray(data)) {
        return data.reduce((result, item, index) => {
            if (item && typeof item === 'object' && objectIncludes(item, query)) {
                return [
                    ...result,
                    [index, ...parent].join(','),
                    ...filterPaths(item, query, [index, ...parent])
                ];
            }
            return result;
        }, []);
    }
    if (_lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.JSONExt.isObject(data)) {
        return Object.keys(data).reduce((result, key) => {
            const item = data[key];
            if (item &&
                typeof item === 'object' &&
                (key.includes(query) || objectIncludes(item, query))) {
                return [
                    ...result,
                    [key, ...parent].join(','),
                    ...filterPaths(item, query, [key, ...parent])
                ];
            }
            return result;
        }, []);
    }
    return [];
}


/***/ })

}]);
//# sourceMappingURL=547.75de9f812a77ceba21ba.js.map?v=75de9f812a77ceba21ba