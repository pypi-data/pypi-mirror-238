"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[3410],{

/***/ 93410:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(82545);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(7280);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(66866);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module rendermime-extension
 */




var CommandIDs;
(function (CommandIDs) {
    CommandIDs.handleLink = 'rendermime:handle-local-link';
})(CommandIDs || (CommandIDs = {}));
/**
 * A plugin providing a rendermime registry.
 */
const plugin = {
    id: '@jupyterlab/rendermime-extension:plugin',
    description: 'Provides the render mime registry.',
    optional: [
        _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__.IDocumentManager,
        _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.ILatexTypesetter,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ISanitizer,
        _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.IMarkdownParser,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator
    ],
    provides: _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.IRenderMimeRegistry,
    activate: activate,
    autoStart: true
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * Activate the rendermine plugin.
 */
function activate(app, docManager, latexTypesetter, sanitizer, markdownParser, translator) {
    const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator).load('jupyterlab');
    if (docManager) {
        app.commands.addCommand(CommandIDs.handleLink, {
            label: trans.__('Handle Local Link'),
            execute: args => {
                const path = args['path'];
                const id = args['id'];
                if (!path) {
                    return;
                }
                // First check if the path exists on the server.
                return docManager.services.contents
                    .get(path, { content: false })
                    .then(() => {
                    // Open the link with the default rendered widget factory,
                    // if applicable.
                    const factory = docManager.registry.defaultRenderedWidgetFactory(path);
                    const widget = docManager.openOrReveal(path, factory.name);
                    // Handle the hash if one has been provided.
                    if (widget && id) {
                        widget.setFragment(id);
                    }
                });
            }
        });
    }
    return new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.RenderMimeRegistry({
        initialFactories: _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.standardRendererFactories,
        linkHandler: !docManager
            ? undefined
            : {
                handleLink: (node, path, id) => {
                    // If node has the download attribute explicitly set, use the
                    // default browser downloading behavior.
                    if (node.tagName === 'A' && node.hasAttribute('download')) {
                        return;
                    }
                    app.commandLinker.connectNode(node, CommandIDs.handleLink, {
                        path,
                        id
                    });
                }
            },
        latexTypesetter: latexTypesetter !== null && latexTypesetter !== void 0 ? latexTypesetter : undefined,
        markdownParser: markdownParser !== null && markdownParser !== void 0 ? markdownParser : undefined,
        translator: translator !== null && translator !== void 0 ? translator : undefined,
        sanitizer: sanitizer !== null && sanitizer !== void 0 ? sanitizer : undefined
    });
}


/***/ })

}]);
//# sourceMappingURL=3410.f153d38c6454e085583e.js.map?v=f153d38c6454e085583e