"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[266,1768],{

/***/ 61768:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommandIDs": () => (/* binding */ CommandIDs),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(82545);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(85707);
/* harmony import */ var _jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * A namespace for mermaid text-based diagram commands.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.copySource = 'mermaid:copy-source';
})(CommandIDs || (CommandIDs = {}));
/**
 * A plugin for the core rendering/cachine of mermaid text-based diagrams
 */
const core = {
    id: '@jupyterlab/mermaid-extension:core',
    description: 'Provides the Mermaid manager.',
    autoStart: true,
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IThemeManager],
    provides: _jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.IMermaidManager,
    activate: (app, themes) => {
        const manager = new _jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.MermaidManager({ themes });
        _jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.RenderedMermaid.manager = manager;
        return manager;
    }
};
/**
 * A plugin for rendering mermaid text-based diagrams in markdown fenced code blocks
 */
const markdown = {
    id: '@jupyterlab/mermaid-extension:markdown',
    description: 'Provides the Mermaid markdown renderer.',
    autoStart: true,
    requires: [_jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.IMermaidManager],
    provides: _jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.IMermaidMarkdown,
    activate: (app, mermaid) => {
        return new _jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.MermaidMarkdown({ mermaid });
    }
};
/**
 * Contextual commands for mermaid text-based diagrams.
 */
const contextCommands = {
    id: '@jupyterlab/mermaid-extension:context-commands',
    description: 'Provides context menu commands for mermaid diagrams.',
    autoStart: true,
    requires: [_jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.IMermaidManager],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.ITranslator],
    activate: (app, mermaid, translator) => {
        const isMermaid = (node) => node.classList.contains(_jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.MERMAID_CLASS);
        const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator).load('jupyterlab');
        app.commands.addCommand(CommandIDs.copySource, {
            label: trans.__('Mermaid Copy Diagram Source'),
            execute: async (args) => {
                const node = app.contextMenuHitTest(isMermaid);
                if (!node) {
                    return;
                }
                const code = node.querySelector(`.${_jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.MERMAID_CODE_CLASS}`);
                if (!code || !code.textContent) {
                    return;
                }
                await navigator.clipboard.writeText(code.textContent);
            }
        });
        const options = { selector: `.${_jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.MERMAID_CLASS}`, rank: 13 };
        app.contextMenu.addItem({ command: CommandIDs.copySource, ...options });
        app.contextMenu.addItem({ type: 'separator', ...options });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([core, markdown, contextCommands]);


/***/ })

}]);
//# sourceMappingURL=266.ba08ff0dd001a8d9489c.js.map?v=ba08ff0dd001a8d9489c