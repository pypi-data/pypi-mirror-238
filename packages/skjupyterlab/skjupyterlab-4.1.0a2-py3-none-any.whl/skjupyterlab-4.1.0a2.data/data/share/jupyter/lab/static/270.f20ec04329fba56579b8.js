"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[270],{

/***/ 70270:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(89397);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(29400);
/* harmony import */ var _jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(82545);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module cell-toolbar-extension
 */




const cellToolbar = {
    id: '@jupyterlab/cell-toolbar-extension:plugin',
    description: 'Add the cells toolbar.',
    autoStart: true,
    activate: async (app, settingRegistry, toolbarRegistry, translator) => {
        const toolbarItems = settingRegistry && toolbarRegistry
            ? (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.createToolbarFactory)(toolbarRegistry, settingRegistry, _jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_1__.CellBarExtension.FACTORY_NAME, cellToolbar.id, translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator)
            : undefined;
        app.docRegistry.addWidgetExtension('Notebook', new _jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_1__.CellBarExtension(app.commands, toolbarItems));
    },
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.IToolbarWidgetRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator]
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (cellToolbar);


/***/ })

}]);
//# sourceMappingURL=270.f20ec04329fba56579b8.js.map?v=f20ec04329fba56579b8