"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[6631,2222],{

/***/ 22222:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "IImageTracker": () => (/* reexport */ IImageTracker),
  "ImageViewer": () => (/* reexport */ ImageViewer),
  "ImageViewerFactory": () => (/* reexport */ ImageViewerFactory)
});

// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var index_js_ = __webpack_require__(22100);
;// CONCATENATED MODULE: ../packages/imageviewer/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The image tracker token.
 */
const IImageTracker = new index_js_.Token('@jupyterlab/imageviewer:IImageTracker', `A widget tracker for images.
  Use this if you want to be able to iterate over and interact with images
  viewed by the application.`);

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var lib_index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var apputils_lib_index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/docregistry@~4.1.0-alpha.2 (strict) (fallback: ../packages/docregistry/lib/index.js)
var docregistry_lib_index_js_ = __webpack_require__(16564);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/imageviewer/lib/widget.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * The class name added to a imageviewer.
 */
const IMAGE_CLASS = 'jp-ImageViewer';
/**
 * A widget for images.
 */
class ImageViewer extends index_es6_js_.Widget {
    /**
     * Construct a new image widget.
     */
    constructor(context) {
        super();
        this._scale = 1;
        this._matrix = [1, 0, 0, 1];
        this._colorinversion = 0;
        this._ready = new index_js_.PromiseDelegate();
        this.context = context;
        this.node.tabIndex = 0;
        this.addClass(IMAGE_CLASS);
        this._img = document.createElement('img');
        this.node.appendChild(this._img);
        this._onTitleChanged();
        context.pathChanged.connect(this._onTitleChanged, this);
        void context.ready.then(() => {
            if (this.isDisposed) {
                return;
            }
            const contents = context.contentsModel;
            this._mimeType = contents.mimetype;
            this._render();
            context.model.contentChanged.connect(this.update, this);
            context.fileChanged.connect(this.update, this);
            this._ready.resolve(void 0);
        });
    }
    /**
     * Print in iframe.
     */
    [apputils_lib_index_js_.Printing.symbol]() {
        return () => apputils_lib_index_js_.Printing.printWidget(this);
    }
    /**
     * A promise that resolves when the image viewer is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * The scale factor for the image.
     */
    get scale() {
        return this._scale;
    }
    set scale(value) {
        if (value === this._scale) {
            return;
        }
        this._scale = value;
        this._updateStyle();
    }
    /**
     * The color inversion of the image.
     */
    get colorinversion() {
        return this._colorinversion;
    }
    set colorinversion(value) {
        if (value === this._colorinversion) {
            return;
        }
        this._colorinversion = value;
        this._updateStyle();
    }
    /**
     * Dispose of resources held by the image viewer.
     */
    dispose() {
        if (this._img.src) {
            URL.revokeObjectURL(this._img.src || '');
        }
        super.dispose();
    }
    /**
     * Reset rotation and flip transformations.
     */
    resetRotationFlip() {
        this._matrix = [1, 0, 0, 1];
        this._updateStyle();
    }
    /**
     * Rotate the image counter-clockwise (left).
     */
    rotateCounterclockwise() {
        this._matrix = Private.prod(this._matrix, Private.rotateCounterclockwiseMatrix);
        this._updateStyle();
    }
    /**
     * Rotate the image clockwise (right).
     */
    rotateClockwise() {
        this._matrix = Private.prod(this._matrix, Private.rotateClockwiseMatrix);
        this._updateStyle();
    }
    /**
     * Flip the image horizontally.
     */
    flipHorizontal() {
        this._matrix = Private.prod(this._matrix, Private.flipHMatrix);
        this._updateStyle();
    }
    /**
     * Flip the image vertically.
     */
    flipVertical() {
        this._matrix = Private.prod(this._matrix, Private.flipVMatrix);
        this._updateStyle();
    }
    /**
     * Handle `update-request` messages for the widget.
     */
    onUpdateRequest(msg) {
        if (this.isDisposed || !this.context.isReady) {
            return;
        }
        this._render();
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        this.node.focus();
    }
    /**
     * Handle a change to the title.
     */
    _onTitleChanged() {
        this.title.label = lib_index_js_.PathExt.basename(this.context.localPath);
    }
    /**
     * Render the widget content.
     */
    _render() {
        const context = this.context;
        const cm = context.contentsModel;
        if (!cm) {
            return;
        }
        const oldurl = this._img.src || '';
        let content = context.model.toString();
        if (cm.format === 'base64') {
            this._img.src = `data:${this._mimeType};base64,${content}`;
        }
        else {
            const a = new Blob([content], { type: this._mimeType });
            this._img.src = URL.createObjectURL(a);
        }
        URL.revokeObjectURL(oldurl);
    }
    /**
     * Update the image CSS style, including the transform and filter.
     */
    _updateStyle() {
        const [a, b, c, d] = this._matrix;
        const [tX, tY] = Private.prodVec(this._matrix, [1, 1]);
        const transform = `matrix(${a}, ${b}, ${c}, ${d}, 0, 0) translate(${tX < 0 ? -100 : 0}%, ${tY < 0 ? -100 : 0}%) `;
        this._img.style.transform = `scale(${this._scale}) ${transform}`;
        this._img.style.filter = `invert(${this._colorinversion})`;
    }
}
/**
 * A widget factory for images.
 */
class ImageViewerFactory extends docregistry_lib_index_js_.ABCWidgetFactory {
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        const content = new ImageViewer(context);
        const widget = new docregistry_lib_index_js_.DocumentWidget({ content, context });
        return widget;
    }
}
/**
 * A namespace for image widget private data.
 */
var Private;
(function (Private) {
    /**
     * Multiply 2x2 matrices.
     */
    function prod([a11, a12, a21, a22], [b11, b12, b21, b22]) {
        return [
            a11 * b11 + a12 * b21,
            a11 * b12 + a12 * b22,
            a21 * b11 + a22 * b21,
            a21 * b12 + a22 * b22
        ];
    }
    Private.prod = prod;
    /**
     * Multiply a 2x2 matrix and a 2x1 vector.
     */
    function prodVec([a11, a12, a21, a22], [b1, b2]) {
        return [a11 * b1 + a12 * b2, a21 * b1 + a22 * b2];
    }
    Private.prodVec = prodVec;
    /**
     * Clockwise rotation transformation matrix.
     */
    Private.rotateClockwiseMatrix = [0, 1, -1, 0];
    /**
     * Counter-clockwise rotation transformation matrix.
     */
    Private.rotateCounterclockwiseMatrix = [0, -1, 1, 0];
    /**
     * Horizontal flip transformation matrix.
     */
    Private.flipHMatrix = [-1, 0, 0, 1];
    /**
     * Vertical flip transformation matrix.
     */
    Private.flipVMatrix = [1, 0, 0, -1];
})(Private || (Private = {}));

;// CONCATENATED MODULE: ../packages/imageviewer/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module imageviewer
 */




/***/ })

}]);
//# sourceMappingURL=6631.5dd5b9e820a7a9a1d53a.js.map?v=5dd5b9e820a7a9a1d53a