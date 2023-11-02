"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[4525],{

/***/ 24525:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CSVSearchProvider": () => (/* binding */ CSVSearchProvider)
/* harmony export */ });
/* harmony import */ var _jupyterlab_csvviewer__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(25946);
/* harmony import */ var _jupyterlab_csvviewer__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_csvviewer__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(16564);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(80599);
/* harmony import */ var _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * CSV viewer search provider
 */
class CSVSearchProvider extends _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__.SearchProvider {
    constructor() {
        super(...arguments);
        /**
         * Set to true if the widget under search is read-only, false
         * if it is editable.  Will be used to determine whether to show
         * the replace option.
         */
        this.isReadOnly = true;
    }
    /**
     * Instantiate a search provider for the widget.
     *
     * #### Notes
     * The widget provided is always checked using `isApplicable` before calling
     * this factory.
     *
     * @param widget The widget to search on
     * @param translator [optional] The translator object
     *
     * @returns The search provider on the widget
     */
    static createNew(widget, translator) {
        return new CSVSearchProvider(widget);
    }
    /**
     * Report whether or not this provider has the ability to search on the given object
     */
    static isApplicable(domain) {
        // check to see if the CSVSearchProvider can search on the
        // first cell, false indicates another editor is present
        return (domain instanceof _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.DocumentWidget && domain.content instanceof _jupyterlab_csvviewer__WEBPACK_IMPORTED_MODULE_0__.CSVViewer);
    }
    /**
     * Clear currently highlighted match.
     */
    clearHighlight() {
        // no-op
        return Promise.resolve();
    }
    /**
     * Move the current match indicator to the next match.
     *
     * @param loop Whether to loop within the matches list.
     *
     * @returns The match is never returned by this provider
     */
    highlightNext(loop) {
        this.widget.content.searchService.find(this._query);
        return Promise.resolve(undefined);
    }
    /**
     * Move the current match indicator to the previous match.
     *
     * @param loop Whether to loop within the matches list.
     *
     * @returns The match is never returned by this provider
     */
    highlightPrevious(loop) {
        this.widget.content.searchService.find(this._query, true);
        return Promise.resolve(undefined);
    }
    /**
     * Replace the currently selected match with the provided text
     * Not implemented in the CSV viewer as it is read-only.
     *
     * @param newText The replacement text
     * @param loop Whether to loop within the matches list.
     *
     * @returns A promise that resolves once the action has completed.
     */
    replaceCurrentMatch(newText, loop) {
        return Promise.resolve(false);
    }
    /**
     * Replace all matches in the notebook with the provided text
     * Not implemented in the CSV viewer as it is read-only.
     *
     * @param newText The replacement text
     *
     * @returns A promise that resolves once the action has completed.
     */
    replaceAllMatches(newText) {
        return Promise.resolve(false);
    }
    /**
     * Initialize the search using the provided options.  Should update the UI
     * to highlight all matches and "select" whatever the first match should be.
     *
     * @param query A RegExp to be use to perform the search
     */
    startQuery(query) {
        this._query = query;
        this.widget.content.searchService.find(query);
        return Promise.resolve();
    }
    /**
     * Clears state of a search provider to prepare for startQuery to be called
     * in order to start a new query or refresh an existing one.
     */
    endQuery() {
        this.widget.content.searchService.clear();
        return Promise.resolve();
    }
}


/***/ })

}]);
//# sourceMappingURL=4525.326d5ae041194da52267.js.map?v=326d5ae041194da52267