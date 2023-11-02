"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[2313],{

/***/ 82313:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(76351);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module ui-components-extension
 */

/**
 * Placeholder for future extension that will provide an icon manager class
 * to assist with overriding/replacing particular sets of icons
 */
const labiconManager = {
    id: '@jupyterlab/ui-components-extension:labicon-manager',
    description: 'Provides the icon manager.',
    provides: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.ILabIconManager,
    autoStart: true,
    activate: (app) => {
        return Object.create(null);
    }
};
/**
 * Sets up the renderer registry to be used by the FormEditor component.
 */
const formRendererRegistryPlugin = {
    id: '@jupyterlab/ui-components-extension:form-renderer-registry',
    description: 'Provides the settings form renderer registry.',
    provides: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.IFormRendererRegistry,
    autoStart: true,
    activate: (app) => {
        const formRendererRegistry = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.FormRendererRegistry();
        return formRendererRegistry;
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([labiconManager, formRendererRegistryPlugin]);


/***/ })

}]);
//# sourceMappingURL=2313.8a08fd0caee2ccce0393.js.map?v=8a08fd0caee2ccce0393