(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[3189],{

/***/ 8872:
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

/**
 * lodash (Custom Build) <https://lodash.com/>
 * Build: `lodash modularize exports="npm" -o ./`
 * Copyright jQuery Foundation and other contributors <https://jquery.org/>
 * Released under MIT license <https://lodash.com/license>
 * Based on Underscore.js 1.8.3 <http://underscorejs.org/LICENSE>
 * Copyright Jeremy Ashkenas, DocumentCloud and Investigative Reporters & Editors
 */

/** Used as references for various `Number` constants. */
var INFINITY = 1 / 0;

/** `Object#toString` result references. */
var symbolTag = '[object Symbol]';

/** Used to match HTML entities and HTML characters. */
var reUnescapedHtml = /[&<>"'`]/g,
    reHasUnescapedHtml = RegExp(reUnescapedHtml.source);

/** Used to map characters to HTML entities. */
var htmlEscapes = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#39;',
  '`': '&#96;'
};

/** Detect free variable `global` from Node.js. */
var freeGlobal = typeof __webpack_require__.g == 'object' && __webpack_require__.g && __webpack_require__.g.Object === Object && __webpack_require__.g;

/** Detect free variable `self`. */
var freeSelf = typeof self == 'object' && self && self.Object === Object && self;

/** Used as a reference to the global object. */
var root = freeGlobal || freeSelf || Function('return this')();

/**
 * The base implementation of `_.propertyOf` without support for deep paths.
 *
 * @private
 * @param {Object} object The object to query.
 * @returns {Function} Returns the new accessor function.
 */
function basePropertyOf(object) {
  return function(key) {
    return object == null ? undefined : object[key];
  };
}

/**
 * Used by `_.escape` to convert characters to HTML entities.
 *
 * @private
 * @param {string} chr The matched character to escape.
 * @returns {string} Returns the escaped character.
 */
var escapeHtmlChar = basePropertyOf(htmlEscapes);

/** Used for built-in method references. */
var objectProto = Object.prototype;

/**
 * Used to resolve the
 * [`toStringTag`](http://ecma-international.org/ecma-262/6.0/#sec-object.prototype.tostring)
 * of values.
 */
var objectToString = objectProto.toString;

/** Built-in value references. */
var Symbol = root.Symbol;

/** Used to convert symbols to primitives and strings. */
var symbolProto = Symbol ? Symbol.prototype : undefined,
    symbolToString = symbolProto ? symbolProto.toString : undefined;

/**
 * The base implementation of `_.toString` which doesn't convert nullish
 * values to empty strings.
 *
 * @private
 * @param {*} value The value to process.
 * @returns {string} Returns the string.
 */
function baseToString(value) {
  // Exit early for strings to avoid a performance hit in some environments.
  if (typeof value == 'string') {
    return value;
  }
  if (isSymbol(value)) {
    return symbolToString ? symbolToString.call(value) : '';
  }
  var result = (value + '');
  return (result == '0' && (1 / value) == -INFINITY) ? '-0' : result;
}

/**
 * Checks if `value` is object-like. A value is object-like if it's not `null`
 * and has a `typeof` result of "object".
 *
 * @static
 * @memberOf _
 * @since 4.0.0
 * @category Lang
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is object-like, else `false`.
 * @example
 *
 * _.isObjectLike({});
 * // => true
 *
 * _.isObjectLike([1, 2, 3]);
 * // => true
 *
 * _.isObjectLike(_.noop);
 * // => false
 *
 * _.isObjectLike(null);
 * // => false
 */
function isObjectLike(value) {
  return !!value && typeof value == 'object';
}

/**
 * Checks if `value` is classified as a `Symbol` primitive or object.
 *
 * @static
 * @memberOf _
 * @since 4.0.0
 * @category Lang
 * @param {*} value The value to check.
 * @returns {boolean} Returns `true` if `value` is a symbol, else `false`.
 * @example
 *
 * _.isSymbol(Symbol.iterator);
 * // => true
 *
 * _.isSymbol('abc');
 * // => false
 */
function isSymbol(value) {
  return typeof value == 'symbol' ||
    (isObjectLike(value) && objectToString.call(value) == symbolTag);
}

/**
 * Converts `value` to a string. An empty string is returned for `null`
 * and `undefined` values. The sign of `-0` is preserved.
 *
 * @static
 * @memberOf _
 * @since 4.0.0
 * @category Lang
 * @param {*} value The value to process.
 * @returns {string} Returns the string.
 * @example
 *
 * _.toString(null);
 * // => ''
 *
 * _.toString(-0);
 * // => '-0'
 *
 * _.toString([1, 2, 3]);
 * // => '1,2,3'
 */
function toString(value) {
  return value == null ? '' : baseToString(value);
}

/**
 * Converts the characters "&", "<", ">", '"', "'", and "\`" in `string` to
 * their corresponding HTML entities.
 *
 * **Note:** No other characters are escaped. To escape additional
 * characters use a third-party library like [_he_](https://mths.be/he).
 *
 * Though the ">" character is escaped for symmetry, characters like
 * ">" and "/" don't need escaping in HTML and have no special meaning
 * unless they're part of a tag or unquoted attribute value. See
 * [Mathias Bynens's article](https://mathiasbynens.be/notes/ambiguous-ampersands)
 * (under "semi-related fun fact") for more details.
 *
 * Backticks are escaped because in IE < 9, they can break out of
 * attribute values or HTML comments. See [#59](https://html5sec.org/#59),
 * [#102](https://html5sec.org/#102), [#108](https://html5sec.org/#108), and
 * [#133](https://html5sec.org/#133) of the
 * [HTML5 Security Cheatsheet](https://html5sec.org/) for more details.
 *
 * When working with HTML you should always
 * [quote attribute values](http://wonko.com/post/html-escaping) to reduce
 * XSS vectors.
 *
 * @static
 * @since 0.1.0
 * @memberOf _
 * @category String
 * @param {string} [string=''] The string to escape.
 * @returns {string} Returns the escaped string.
 * @example
 *
 * _.escape('fred, barney, & pebbles');
 * // => 'fred, barney, &amp; pebbles'
 */
function escape(string) {
  string = toString(string);
  return (string && reHasUnescapedHtml.test(string))
    ? string.replace(reUnescapedHtml, escapeHtmlChar)
    : string;
}

module.exports = escape;


/***/ }),

/***/ 62602:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "g": () => (/* binding */ AttachmentModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(57090);
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(22100);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(30205);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/



/**
 * The default implementation of a notebook attachment model.
 */
class AttachmentModel {
    /**
     * Construct a new attachment model.
     */
    constructor(options) {
        // All attachments are untrusted
        this.trusted = false;
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._raw = {};
        const data = Private.getData(options.value);
        this._data = new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__.ObservableJSON({ values: data });
        this._rawData = data;
        // Make a copy of the data.
        const value = options.value;
        for (const key in value) {
            // Ignore data and metadata that were stripped.
            switch (key) {
                case 'data':
                    break;
                default:
                    this._raw[key] = Private.extract(value, key);
            }
        }
    }
    /**
     * A signal emitted when the attachment model changes.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Dispose of the resources used by the attachment model.
     */
    dispose() {
        this._data.dispose();
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal.clearData(this);
    }
    /**
     * The data associated with the model.
     */
    get data() {
        return this._rawData;
    }
    /**
     * The metadata associated with the model.
     */
    get metadata() {
        return {};
    }
    /**
     * Set the data associated with the model.
     *
     * #### Notes
     * Depending on the implementation of the mime model,
     * this call may or may not have deferred effects,
     */
    setData(options) {
        if (options.data) {
            this._updateObservable(this._data, options.data);
            this._rawData = options.data;
        }
        this._changed.emit(void 0);
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        const attachment = {};
        for (const key in this._raw) {
            attachment[key] = Private.extract(this._raw, key);
        }
        return attachment;
    }
    /**
     * Update an observable JSON object using a readonly JSON object.
     */
    _updateObservable(observable, data) {
        const oldKeys = observable.keys();
        const newKeys = Object.keys(data);
        // Handle removed keys.
        for (const key of oldKeys) {
            if (newKeys.indexOf(key) === -1) {
                observable.delete(key);
            }
        }
        // Handle changed data.
        for (const key of newKeys) {
            const oldValue = observable.get(key);
            const newValue = data[key];
            if (oldValue !== newValue) {
                observable.set(key, newValue);
            }
        }
    }
}
/**
 * The namespace for AttachmentModel statics.
 */
(function (AttachmentModel) {
    /**
     * Get the data for an attachment.
     *
     * @param bundle - A kernel attachment MIME bundle.
     *
     * @returns - The data for the payload.
     */
    function getData(bundle) {
        return Private.getData(bundle);
    }
    AttachmentModel.getData = getData;
})(AttachmentModel || (AttachmentModel = {}));
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * Get the data from a notebook attachment.
     */
    function getData(bundle) {
        return convertBundle(bundle);
    }
    Private.getData = getData;
    /**
     * Get the bundle options given attachment model options.
     */
    function getBundleOptions(options) {
        const data = getData(options.value);
        return { data };
    }
    Private.getBundleOptions = getBundleOptions;
    /**
     * Extract a value from a JSONObject.
     */
    function extract(value, key) {
        const item = value[key];
        if (item === undefined || _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.isPrimitive(item)) {
            return item;
        }
        return _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(item);
    }
    Private.extract = extract;
    /**
     * Convert a mime bundle to mime data.
     */
    function convertBundle(bundle) {
        const map = Object.create(null);
        for (const mimeType in bundle) {
            map[mimeType] = extract(bundle, mimeType);
        }
        return map;
    }
})(Private || (Private = {}));


/***/ }),

/***/ 56159:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BJ": () => (/* binding */ textRendererFactory),
/* harmony export */   "F": () => (/* binding */ svgRendererFactory),
/* harmony export */   "Lz": () => (/* binding */ imageRendererFactory),
/* harmony export */   "Nf": () => (/* binding */ standardRendererFactories),
/* harmony export */   "hJ": () => (/* binding */ latexRendererFactory),
/* harmony export */   "nF": () => (/* binding */ javaScriptRendererFactory),
/* harmony export */   "vy": () => (/* binding */ htmlRendererFactory),
/* harmony export */   "xr": () => (/* binding */ markdownRendererFactory)
/* harmony export */ });
/* harmony import */ var _widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(86580);

/**
 * A mime renderer factory for raw html.
 */
const htmlRendererFactory = {
    safe: true,
    mimeTypes: ['text/html'],
    defaultRank: 50,
    createRenderer: options => new _widgets__WEBPACK_IMPORTED_MODULE_0__/* .RenderedHTML */ .oI(options)
};
/**
 * A mime renderer factory for images.
 */
const imageRendererFactory = {
    safe: true,
    mimeTypes: [
        'image/bmp',
        'image/png',
        'image/jpeg',
        'image/gif',
        'image/webp'
    ],
    defaultRank: 90,
    createRenderer: options => new _widgets__WEBPACK_IMPORTED_MODULE_0__/* .RenderedImage */ .UH(options)
};
/**
 * A mime renderer factory for LaTeX.
 */
const latexRendererFactory = {
    safe: true,
    mimeTypes: ['text/latex'],
    defaultRank: 70,
    createRenderer: options => new _widgets__WEBPACK_IMPORTED_MODULE_0__/* .RenderedLatex */ .FK(options)
};
/**
 * A mime renderer factory for Markdown.
 */
const markdownRendererFactory = {
    safe: true,
    mimeTypes: ['text/markdown'],
    defaultRank: 60,
    createRenderer: options => new _widgets__WEBPACK_IMPORTED_MODULE_0__/* .RenderedMarkdown */ .cw(options)
};
/**
 * A mime renderer factory for svg.
 */
const svgRendererFactory = {
    safe: false,
    mimeTypes: ['image/svg+xml'],
    defaultRank: 80,
    createRenderer: options => new _widgets__WEBPACK_IMPORTED_MODULE_0__/* .RenderedSVG */ .zt(options)
};
/**
 * A mime renderer factory for plain and jupyter console text data.
 */
const textRendererFactory = {
    safe: true,
    mimeTypes: [
        'text/plain',
        'application/vnd.jupyter.stdout',
        'application/vnd.jupyter.stderr'
    ],
    defaultRank: 120,
    createRenderer: options => new _widgets__WEBPACK_IMPORTED_MODULE_0__/* .RenderedText */ .lH(options)
};
/**
 * A placeholder factory for rendered JavaScript.
 */
const javaScriptRendererFactory = {
    safe: false,
    mimeTypes: ['text/javascript', 'application/javascript'],
    defaultRank: 110,
    createRenderer: options => new _widgets__WEBPACK_IMPORTED_MODULE_0__/* .RenderedJavaScript */ .ND(options)
};
/**
 * The standard factories provided by the rendermime package.
 */
const standardRendererFactories = [
    htmlRendererFactory,
    markdownRendererFactory,
    latexRendererFactory,
    svgRendererFactory,
    imageRendererFactory,
    javaScriptRendererFactory,
    textRendererFactory
];


/***/ }),

/***/ 73189:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AttachmentModel": () => (/* reexport safe */ _attachmentmodel__WEBPACK_IMPORTED_MODULE_1__.g),
/* harmony export */   "ILatexTypesetter": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_8__._y),
/* harmony export */   "IMarkdownParser": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_8__.sc),
/* harmony export */   "IRenderMimeRegistry": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_8__.ZD),
/* harmony export */   "MimeModel": () => (/* reexport safe */ _mimemodel__WEBPACK_IMPORTED_MODULE_4__.a),
/* harmony export */   "OutputModel": () => (/* reexport safe */ _outputmodel__WEBPACK_IMPORTED_MODULE_5__.M),
/* harmony export */   "RenderMimeRegistry": () => (/* reexport safe */ _registry__WEBPACK_IMPORTED_MODULE_6__.D),
/* harmony export */   "RenderedCommon": () => (/* reexport safe */ _widgets__WEBPACK_IMPORTED_MODULE_9__.pY),
/* harmony export */   "RenderedHTML": () => (/* reexport safe */ _widgets__WEBPACK_IMPORTED_MODULE_9__.oI),
/* harmony export */   "RenderedHTMLCommon": () => (/* reexport safe */ _widgets__WEBPACK_IMPORTED_MODULE_9__.BP),
/* harmony export */   "RenderedImage": () => (/* reexport safe */ _widgets__WEBPACK_IMPORTED_MODULE_9__.UH),
/* harmony export */   "RenderedJavaScript": () => (/* reexport safe */ _widgets__WEBPACK_IMPORTED_MODULE_9__.ND),
/* harmony export */   "RenderedLatex": () => (/* reexport safe */ _widgets__WEBPACK_IMPORTED_MODULE_9__.FK),
/* harmony export */   "RenderedMarkdown": () => (/* reexport safe */ _widgets__WEBPACK_IMPORTED_MODULE_9__.cw),
/* harmony export */   "RenderedSVG": () => (/* reexport safe */ _widgets__WEBPACK_IMPORTED_MODULE_9__.zt),
/* harmony export */   "RenderedText": () => (/* reexport safe */ _widgets__WEBPACK_IMPORTED_MODULE_9__.lH),
/* harmony export */   "htmlRendererFactory": () => (/* reexport safe */ _factories__WEBPACK_IMPORTED_MODULE_2__.vy),
/* harmony export */   "imageRendererFactory": () => (/* reexport safe */ _factories__WEBPACK_IMPORTED_MODULE_2__.Lz),
/* harmony export */   "javaScriptRendererFactory": () => (/* reexport safe */ _factories__WEBPACK_IMPORTED_MODULE_2__.nF),
/* harmony export */   "latexRendererFactory": () => (/* reexport safe */ _factories__WEBPACK_IMPORTED_MODULE_2__.hJ),
/* harmony export */   "markdownRendererFactory": () => (/* reexport safe */ _factories__WEBPACK_IMPORTED_MODULE_2__.xr),
/* harmony export */   "removeMath": () => (/* reexport safe */ _latex__WEBPACK_IMPORTED_MODULE_3__.D),
/* harmony export */   "renderHTML": () => (/* reexport safe */ _renderers__WEBPACK_IMPORTED_MODULE_7__.NN),
/* harmony export */   "renderImage": () => (/* reexport safe */ _renderers__WEBPACK_IMPORTED_MODULE_7__.co),
/* harmony export */   "renderLatex": () => (/* reexport safe */ _renderers__WEBPACK_IMPORTED_MODULE_7__.K3),
/* harmony export */   "renderMarkdown": () => (/* reexport safe */ _renderers__WEBPACK_IMPORTED_MODULE_7__.ap),
/* harmony export */   "renderSVG": () => (/* reexport safe */ _renderers__WEBPACK_IMPORTED_MODULE_7__.KB),
/* harmony export */   "renderText": () => (/* reexport safe */ _renderers__WEBPACK_IMPORTED_MODULE_7__.IY),
/* harmony export */   "replaceMath": () => (/* reexport safe */ _latex__WEBPACK_IMPORTED_MODULE_3__.b),
/* harmony export */   "standardRendererFactories": () => (/* reexport safe */ _factories__WEBPACK_IMPORTED_MODULE_2__.Nf),
/* harmony export */   "svgRendererFactory": () => (/* reexport safe */ _factories__WEBPACK_IMPORTED_MODULE_2__.F),
/* harmony export */   "textRendererFactory": () => (/* reexport safe */ _factories__WEBPACK_IMPORTED_MODULE_2__.BJ)
/* harmony export */ });
/* harmony import */ var _jupyterlab_rendermime_interfaces__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(68213);
/* harmony import */ var _jupyterlab_rendermime_interfaces__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime_interfaces__WEBPACK_IMPORTED_MODULE_0__);
/* harmony reexport (unknown) */ var __WEBPACK_REEXPORT_OBJECT__ = {};
/* harmony reexport (unknown) */ for(const __WEBPACK_IMPORT_KEY__ in _jupyterlab_rendermime_interfaces__WEBPACK_IMPORTED_MODULE_0__) if(__WEBPACK_IMPORT_KEY__ !== "default") __WEBPACK_REEXPORT_OBJECT__[__WEBPACK_IMPORT_KEY__] = () => _jupyterlab_rendermime_interfaces__WEBPACK_IMPORTED_MODULE_0__[__WEBPACK_IMPORT_KEY__]
/* harmony reexport (unknown) */ __webpack_require__.d(__webpack_exports__, __WEBPACK_REEXPORT_OBJECT__);
/* harmony import */ var _attachmentmodel__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(62602);
/* harmony import */ var _factories__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(56159);
/* harmony import */ var _latex__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(74344);
/* harmony import */ var _mimemodel__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(30811);
/* harmony import */ var _outputmodel__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(50440);
/* harmony import */ var _registry__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(69120);
/* harmony import */ var _renderers__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(14769);
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(175);
/* harmony import */ var _widgets__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(86580);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module rendermime
 */












/***/ }),

/***/ 74344:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "D": () => (/* binding */ removeMath),
/* harmony export */   "b": () => (/* binding */ replaceMath)
/* harmony export */ });
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
// Some magic for deferring mathematical expressions to MathJax
// by hiding them from the Markdown parser.
// Some of the code here is adapted with permission from Davide Cervone
// under the terms of the Apache2 license governing the MathJax project.
// Other minor modifications are also due to StackExchange and are used with
// permission.
const inline = '$'; // the inline math delimiter
// MATHSPLIT contains the pattern for math delimiters and special symbols
// needed for searching for math in the text input.
const MATHSPLIT = /(\$\$?|\\(?:begin|end)\{[a-z]*\*?\}|\\[{}$]|[{}]|(?:\n\s*)+|@@\d+@@|\\\\(?:\(|\)|\[|\]))/i;
/**
 *  Break up the text into its component parts and search
 *    through them for math delimiters, braces, linebreaks, etc.
 *  Math delimiters must match and braces must balance.
 *  Don't allow math to pass through a double linebreak
 *    (which will be a paragraph).
 */
function removeMath(text) {
    const math = []; // stores math strings for later
    let start = null;
    let end = null;
    let last = null;
    let braces = 0;
    let deTilde;
    // Except for extreme edge cases, this should catch precisely those pieces of the markdown
    // source that will later be turned into code spans. While MathJax will not TeXify code spans,
    // we still have to consider them at this point; the following issue has happened several times:
    //
    //     `$foo` and `$bar` are variables.  -->  <code>$foo ` and `$bar</code> are variables.
    const hasCodeSpans = text.includes('`') || text.includes('~~~');
    if (hasCodeSpans) {
        text = text
            .replace(/~/g, '~T')
            // note: the `fence` (three or more consecutive tildes or backticks)
            // can be followed by an `info string` but this cannot include backticks,
            // see specification: https://spec.commonmark.org/0.30/#info-string
            .replace(/^(?<fence>`{3,}|(~T){3,})[^`\n]*\n([\s\S]*?)^\k<fence>`*$/gm, wholematch => wholematch.replace(/\$/g, '~D'))
            .replace(/(^|[^\\])(`+)([^\n]*?[^`\n])\2(?!`)/gm, wholematch => wholematch.replace(/\$/g, '~D'));
        deTilde = (text) => {
            return text.replace(/~([TD])/g, (wholematch, character) => character === 'T' ? '~' : inline);
        };
    }
    else {
        deTilde = (text) => {
            return text;
        };
    }
    let blocks = text.replace(/\r\n?/g, '\n').split(MATHSPLIT);
    for (let i = 1, m = blocks.length; i < m; i += 2) {
        const block = blocks[i];
        if (block.charAt(0) === '@') {
            //
            //  Things that look like our math markers will get
            //  stored and then retrieved along with the math.
            //
            blocks[i] = '@@' + math.length + '@@';
            math.push(block);
        }
        else if (start !== null) {
            //
            //  If we are in math, look for the end delimiter,
            //    but don't go past double line breaks, and
            //    and balance braces within the math.
            //
            if (block === end) {
                if (braces) {
                    last = i;
                }
                else {
                    blocks = processMath(start, i, deTilde, math, blocks);
                    start = null;
                    end = null;
                    last = null;
                }
            }
            else if (block.match(/\n.*\n/)) {
                if (last !== null) {
                    i = last;
                    blocks = processMath(start, i, deTilde, math, blocks);
                }
                start = null;
                end = null;
                last = null;
                braces = 0;
            }
            else if (block === '{') {
                braces++;
            }
            else if (block === '}' && braces) {
                braces--;
            }
        }
        else {
            //
            //  Look for math start delimiters and when
            //    found, set up the end delimiter.
            //
            if (block === inline || block === '$$') {
                start = i;
                end = block;
                braces = 0;
            }
            else if (block === '\\\\(' || block === '\\\\[') {
                start = i;
                end = block.slice(-1) === '(' ? '\\\\)' : '\\\\]';
                braces = 0;
            }
            else if (block.substr(1, 5) === 'begin') {
                start = i;
                end = '\\end' + block.substr(6);
                braces = 0;
            }
        }
    }
    if (start !== null && last !== null) {
        blocks = processMath(start, last, deTilde, math, blocks);
        start = null;
        end = null;
        last = null;
    }
    return { text: deTilde(blocks.join('')), math };
}
/**
 * Put back the math strings that were saved,
 * and clear the math array (no need to keep it around).
 */
function replaceMath(text, math) {
    /**
     * Replace a math placeholder with its corresponding group.
     * The math delimiters "\\(", "\\[", "\\)" and "\\]" are replaced
     * removing one backslash in order to be interpreted correctly by MathJax.
     */
    const process = (match, n) => {
        let group = math[n];
        if (group.substr(0, 3) === '\\\\(' &&
            group.substr(group.length - 3) === '\\\\)') {
            group = '\\(' + group.substring(3, group.length - 3) + '\\)';
        }
        else if (group.substr(0, 3) === '\\\\[' &&
            group.substr(group.length - 3) === '\\\\]') {
            group = '\\[' + group.substring(3, group.length - 3) + '\\]';
        }
        return group;
    };
    // Replace all the math group placeholders in the text
    // with the saved strings.
    return text.replace(/@@(\d+)@@/g, process);
}
/**
 * Process math blocks.
 *
 * The math is in blocks i through j, so
 *   collect it into one block and clear the others.
 *  Replace &, <, and > by named entities.
 *  For IE, put <br> at the ends of comments since IE removes \n.
 *  Clear the current math positions and store the index of the
 *   math, then push the math string onto the storage array.
 *  The preProcess function is called on all blocks if it has been passed in
 */
function processMath(i, j, preProcess, math, blocks) {
    let block = blocks
        .slice(i, j + 1)
        .join('')
        .replace(/&/g, '&amp;') // use HTML entity for &
        .replace(/</g, '&lt;') // use HTML entity for <
        .replace(/>/g, '&gt;'); // use HTML entity for >
    if (navigator && navigator.appName === 'Microsoft Internet Explorer') {
        block = block.replace(/(%[^\n]*)\n/g, '$1<br/>\n');
    }
    while (j > i) {
        blocks[j] = '';
        j--;
    }
    blocks[i] = '@@' + math.length + '@@'; // replace the current block text with a unique tag to find later
    if (preProcess) {
        block = preProcess(block);
    }
    math.push(block);
    return blocks;
}


/***/ }),

/***/ 30811:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "a": () => (/* binding */ MimeModel)
/* harmony export */ });
/**
 * The default mime model implementation.
 */
class MimeModel {
    /**
     * Construct a new mime model.
     */
    constructor(options = {}) {
        this.trusted = !!options.trusted;
        this._data = options.data || {};
        this._metadata = options.metadata || {};
        this._callback = options.callback || Private.noOp;
    }
    /**
     * The data associated with the model.
     */
    get data() {
        return this._data;
    }
    /**
     * The metadata associated with the model.
     */
    get metadata() {
        return this._metadata;
    }
    /**
     * Set the data associated with the model.
     *
     * #### Notes
     * Depending on the implementation of the mime model,
     * this call may or may not have deferred effects,
     */
    setData(options) {
        this._data = options.data || this._data;
        this._metadata = options.metadata || this._metadata;
        this._callback(options);
    }
}
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * A no-op callback function.
     */
    function noOp() {
        /* no-op */
    }
    Private.noOp = noOp;
})(Private || (Private = {}));


/***/ }),

/***/ 50440:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "M": () => (/* binding */ OutputModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(64571);
/* harmony import */ var _jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(57090);
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(22100);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(30205);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/




/**
 * The default implementation of a notebook output model.
 */
class OutputModel {
    /**
     * Construct a new output model.
     */
    constructor(options) {
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this._raw = {};
        const { data, metadata, trusted } = Private.getBundleOptions(options);
        this._data = new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1__.ObservableJSON({ values: data });
        this._rawData = data;
        this._metadata = new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1__.ObservableJSON({ values: metadata });
        this._rawMetadata = metadata;
        this.trusted = trusted;
        // Make a copy of the data.
        const value = options.value;
        for (const key in value) {
            // Ignore data and metadata that were stripped.
            switch (key) {
                case 'data':
                case 'metadata':
                    break;
                default:
                    this._raw[key] = Private.extract(value, key);
            }
        }
        this.type = value.output_type;
        if (_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__.isExecuteResult(value)) {
            this.executionCount = value.execution_count;
        }
        else {
            this.executionCount = null;
        }
    }
    /**
     * A signal emitted when the output model changes.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Dispose of the resources used by the output model.
     */
    dispose() {
        this._data.dispose();
        this._metadata.dispose();
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal.clearData(this);
    }
    /**
     * The data associated with the model.
     */
    get data() {
        return this._rawData;
    }
    /**
     * The metadata associated with the model.
     */
    get metadata() {
        return this._rawMetadata;
    }
    /**
     * Set the data associated with the model.
     *
     * #### Notes
     * Depending on the implementation of the mime model,
     * this call may or may not have deferred effects,
     */
    setData(options) {
        if (options.data) {
            this._updateObservable(this._data, options.data);
            this._rawData = options.data;
        }
        if (options.metadata) {
            this._updateObservable(this._metadata, options.metadata);
            this._rawMetadata = options.metadata;
        }
        this._changed.emit();
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        const output = {};
        for (const key in this._raw) {
            output[key] = Private.extract(this._raw, key);
        }
        switch (this.type) {
            case 'display_data':
            case 'execute_result':
            case 'update_display_data':
                output['data'] = this.data;
                output['metadata'] = this.metadata;
                break;
            default:
                break;
        }
        // Remove transient data.
        delete output['transient'];
        return output;
    }
    /**
     * Update an observable JSON object using a readonly JSON object.
     */
    _updateObservable(observable, data) {
        const oldKeys = observable.keys();
        const newKeys = Object.keys(data);
        // Handle removed keys.
        for (const key of oldKeys) {
            if (newKeys.indexOf(key) === -1) {
                observable.delete(key);
            }
        }
        // Handle changed data.
        for (const key of newKeys) {
            const oldValue = observable.get(key);
            const newValue = data[key];
            if (oldValue !== newValue) {
                observable.set(key, newValue);
            }
        }
    }
}
/**
 * The namespace for OutputModel statics.
 */
(function (OutputModel) {
    /**
     * Get the data for an output.
     *
     * @param output - A kernel output message payload.
     *
     * @returns - The data for the payload.
     */
    function getData(output) {
        return Private.getData(output);
    }
    OutputModel.getData = getData;
    /**
     * Get the metadata from an output message.
     *
     * @param output - A kernel output message payload.
     *
     * @returns - The metadata for the payload.
     */
    function getMetadata(output) {
        return Private.getMetadata(output);
    }
    OutputModel.getMetadata = getMetadata;
})(OutputModel || (OutputModel = {}));
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * Get the data from a notebook output.
     */
    function getData(output) {
        let bundle = {};
        if (_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__.isExecuteResult(output) ||
            _jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__.isDisplayData(output) ||
            _jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__.isDisplayUpdate(output)) {
            bundle = output.data;
        }
        else if (_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__.isStream(output)) {
            if (output.name === 'stderr') {
                bundle['application/vnd.jupyter.stderr'] = output.text;
            }
            else {
                bundle['application/vnd.jupyter.stdout'] = output.text;
            }
        }
        else if (_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__.isError(output)) {
            bundle['application/vnd.jupyter.error'] = output;
            const traceback = output.traceback.join('\n');
            bundle['application/vnd.jupyter.stderr'] =
                traceback || `${output.ename}: ${output.evalue}`;
        }
        return convertBundle(bundle);
    }
    Private.getData = getData;
    /**
     * Get the metadata from an output message.
     */
    function getMetadata(output) {
        const value = Object.create(null);
        if (_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__.isExecuteResult(output) || _jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__.isDisplayData(output)) {
            for (const key in output.metadata) {
                value[key] = extract(output.metadata, key);
            }
        }
        return value;
    }
    Private.getMetadata = getMetadata;
    /**
     * Get the bundle options given output model options.
     */
    function getBundleOptions(options) {
        const data = getData(options.value);
        const metadata = getMetadata(options.value);
        const trusted = !!options.trusted;
        return { data, metadata, trusted };
    }
    Private.getBundleOptions = getBundleOptions;
    /**
     * Extract a value from a JSONObject.
     */
    function extract(value, key) {
        const item = value[key];
        if (item === undefined || _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.isPrimitive(item)) {
            return item;
        }
        return JSON.parse(JSON.stringify(item));
    }
    Private.extract = extract;
    /**
     * Convert a mime bundle to mime data.
     */
    function convertBundle(bundle) {
        const map = Object.create(null);
        for (const mimeType in bundle) {
            map[mimeType] = extract(bundle, mimeType);
        }
        return map;
    }
})(Private || (Private = {}));


/***/ }),

/***/ 69120:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "D": () => (/* binding */ RenderMimeRegistry)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(82545);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(78254);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _mimemodel__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(30811);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/




/**
 * An object which manages mime renderer factories.
 *
 * This object is used to render mime models using registered mime
 * renderers, selecting the preferred mime renderer to render the
 * model into a widget.
 *
 * #### Notes
 * This class is not intended to be subclassed.
 */
class RenderMimeRegistry {
    /**
     * Construct a new rendermime.
     *
     * @param options - The options for initializing the instance.
     */
    constructor(options = {}) {
        var _a, _b, _c, _d, _e, _f;
        this._id = 0;
        this._ranks = {};
        this._types = null;
        this._factories = {};
        // Parse the options.
        this.translator = (_a = options.translator) !== null && _a !== void 0 ? _a : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        this.resolver = (_b = options.resolver) !== null && _b !== void 0 ? _b : null;
        this.linkHandler = (_c = options.linkHandler) !== null && _c !== void 0 ? _c : null;
        this.latexTypesetter = (_d = options.latexTypesetter) !== null && _d !== void 0 ? _d : null;
        this.markdownParser = (_e = options.markdownParser) !== null && _e !== void 0 ? _e : null;
        this.sanitizer = (_f = options.sanitizer) !== null && _f !== void 0 ? _f : new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Sanitizer();
        // Add the initial factories.
        if (options.initialFactories) {
            for (const factory of options.initialFactories) {
                this.addFactory(factory);
            }
        }
    }
    /**
     * The ordered list of mimeTypes.
     */
    get mimeTypes() {
        return this._types || (this._types = Private.sortedTypes(this._ranks));
    }
    /**
     * Find the preferred mime type for a mime bundle.
     *
     * @param bundle - The bundle of mime data.
     *
     * @param safe - How to consider safe/unsafe factories. If 'ensure',
     *   it will only consider safe factories. If 'any', any factory will be
     *   considered. If 'prefer', unsafe factories will be considered, but
     *   only after the safe options have been exhausted.
     *
     * @returns The preferred mime type from the available factories,
     *   or `undefined` if the mime type cannot be rendered.
     */
    preferredMimeType(bundle, safe = 'ensure') {
        // Try to find a safe factory first, if preferred.
        if (safe === 'ensure' || safe === 'prefer') {
            for (const mt of this.mimeTypes) {
                if (mt in bundle && this._factories[mt].safe) {
                    return mt;
                }
            }
        }
        if (safe !== 'ensure') {
            // Otherwise, search for the best factory among all factories.
            for (const mt of this.mimeTypes) {
                if (mt in bundle) {
                    return mt;
                }
            }
        }
        // Otherwise, no matching mime type exists.
        return undefined;
    }
    /**
     * Create a renderer for a mime type.
     *
     * @param mimeType - The mime type of interest.
     *
     * @returns A new renderer for the given mime type.
     *
     * @throws An error if no factory exists for the mime type.
     */
    createRenderer(mimeType) {
        // Throw an error if no factory exists for the mime type.
        if (!(mimeType in this._factories)) {
            throw new Error(`No factory for mime type: '${mimeType}'`);
        }
        // Invoke the best factory for the given mime type.
        return this._factories[mimeType].createRenderer({
            mimeType,
            resolver: this.resolver,
            sanitizer: this.sanitizer,
            linkHandler: this.linkHandler,
            latexTypesetter: this.latexTypesetter,
            markdownParser: this.markdownParser,
            translator: this.translator
        });
    }
    /**
     * Create a new mime model.  This is a convenience method.
     *
     * @options - The options used to create the model.
     *
     * @returns A new mime model.
     */
    createModel(options = {}) {
        return new _mimemodel__WEBPACK_IMPORTED_MODULE_3__/* .MimeModel */ .a(options);
    }
    /**
     * Create a clone of this rendermime instance.
     *
     * @param options - The options for configuring the clone.
     *
     * @returns A new independent clone of the rendermime.
     */
    clone(options = {}) {
        var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k;
        // Create the clone.
        const clone = new RenderMimeRegistry({
            resolver: (_b = (_a = options.resolver) !== null && _a !== void 0 ? _a : this.resolver) !== null && _b !== void 0 ? _b : undefined,
            sanitizer: (_d = (_c = options.sanitizer) !== null && _c !== void 0 ? _c : this.sanitizer) !== null && _d !== void 0 ? _d : undefined,
            linkHandler: (_f = (_e = options.linkHandler) !== null && _e !== void 0 ? _e : this.linkHandler) !== null && _f !== void 0 ? _f : undefined,
            latexTypesetter: (_h = (_g = options.latexTypesetter) !== null && _g !== void 0 ? _g : this.latexTypesetter) !== null && _h !== void 0 ? _h : undefined,
            markdownParser: (_k = (_j = options.markdownParser) !== null && _j !== void 0 ? _j : this.markdownParser) !== null && _k !== void 0 ? _k : undefined,
            translator: this.translator
        });
        // Clone the internal state.
        clone._factories = { ...this._factories };
        clone._ranks = { ...this._ranks };
        clone._id = this._id;
        // Return the cloned object.
        return clone;
    }
    /**
     * Get the renderer factory registered for a mime type.
     *
     * @param mimeType - The mime type of interest.
     *
     * @returns The factory for the mime type, or `undefined`.
     */
    getFactory(mimeType) {
        return this._factories[mimeType];
    }
    /**
     * Add a renderer factory to the rendermime.
     *
     * @param factory - The renderer factory of interest.
     *
     * @param rank - The rank of the renderer. A lower rank indicates
     *   a higher priority for rendering. If not given, the rank will
     *   defer to the `defaultRank` of the factory.  If no `defaultRank`
     *   is given, it will default to 100.
     *
     * #### Notes
     * The renderer will replace an existing renderer for the given
     * mimeType.
     */
    addFactory(factory, rank) {
        if (rank === undefined) {
            rank = factory.defaultRank;
            if (rank === undefined) {
                rank = 100;
            }
        }
        for (const mt of factory.mimeTypes) {
            this._factories[mt] = factory;
            this._ranks[mt] = { rank, id: this._id++ };
        }
        this._types = null;
    }
    /**
     * Remove a mime type.
     *
     * @param mimeType - The mime type of interest.
     */
    removeMimeType(mimeType) {
        delete this._factories[mimeType];
        delete this._ranks[mimeType];
        this._types = null;
    }
    /**
     * Get the rank for a given mime type.
     *
     * @param mimeType - The mime type of interest.
     *
     * @returns The rank of the mime type or undefined.
     */
    getRank(mimeType) {
        const rank = this._ranks[mimeType];
        return rank && rank.rank;
    }
    /**
     * Set the rank of a given mime type.
     *
     * @param mimeType - The mime type of interest.
     *
     * @param rank - The new rank to assign.
     *
     * #### Notes
     * This is a no-op if the mime type is not registered.
     */
    setRank(mimeType, rank) {
        if (!this._ranks[mimeType]) {
            return;
        }
        const id = this._id++;
        this._ranks[mimeType] = { rank, id };
        this._types = null;
    }
}
/**
 * The namespace for `RenderMimeRegistry` class statics.
 */
(function (RenderMimeRegistry) {
    /**
     * A default resolver that uses a given reference path and a contents manager.
     */
    class UrlResolver {
        /**
         * Create a new url resolver.
         */
        constructor(options) {
            this._path = options.path;
            this._contents = options.contents;
        }
        /**
         * The path of the object, from which local urls can be derived.
         */
        get path() {
            return this._path;
        }
        set path(value) {
            this._path = value;
        }
        /**
         * Resolve a relative url to an absolute url path.
         */
        async resolveUrl(url) {
            if (this.isLocal(url)) {
                const cwd = encodeURI(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.dirname(this.path));
                url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.resolve(cwd, url);
            }
            return url;
        }
        /**
         * Get the download url of a given absolute url path.
         *
         * #### Notes
         * The returned URL may include a query parameter.
         */
        async getDownloadUrl(urlPath) {
            if (this.isLocal(urlPath)) {
                // decode url->path before passing to contents api
                return this._contents.getDownloadUrl(decodeURIComponent(urlPath));
            }
            return urlPath;
        }
        /**
         * Whether the URL should be handled by the resolver
         * or not.
         *
         * #### Notes
         * This is similar to the `isLocal` check in `URLExt`,
         * but it also checks whether the path points to any
         * of the `IDrive`s that may be registered with the contents
         * manager.
         */
        isLocal(url) {
            if (this.isMalformed(url)) {
                return false;
            }
            return _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.isLocal(url) || !!this._contents.driveName(decodeURI(url));
        }
        /**
         * Whether the URL can be decoded using `decodeURI`.
         */
        isMalformed(url) {
            try {
                decodeURI(url);
                return false;
            }
            catch (error) {
                if (error instanceof URIError) {
                    return true;
                }
                throw error;
            }
        }
    }
    RenderMimeRegistry.UrlResolver = UrlResolver;
})(RenderMimeRegistry || (RenderMimeRegistry = {}));
/**
 * The namespace for the module implementation details.
 */
var Private;
(function (Private) {
    /**
     * Get the mime types in the map, ordered by rank.
     */
    function sortedTypes(map) {
        return Object.keys(map).sort((a, b) => {
            const p1 = map[a];
            const p2 = map[b];
            if (p1.rank !== p2.rank) {
                return p1.rank - p2.rank;
            }
            return p1.id - p2.id;
        });
    }
    Private.sortedTypes = sortedTypes;
})(Private || (Private = {}));


/***/ }),

/***/ 14769:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IY": () => (/* binding */ renderText),
/* harmony export */   "K3": () => (/* binding */ renderLatex),
/* harmony export */   "KB": () => (/* binding */ renderSVG),
/* harmony export */   "NN": () => (/* binding */ renderHTML),
/* harmony export */   "ap": () => (/* binding */ renderMarkdown),
/* harmony export */   "co": () => (/* binding */ renderImage)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(78254);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var lodash_escape__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(8872);
/* harmony import */ var lodash_escape__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(lodash_escape__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _latex__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(74344);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/




/**
 * Render HTML into a host node.
 *
 * @param options - The options for rendering.
 *
 * @returns A promise which resolves when rendering is complete.
 */
function renderHTML(options) {
    // Unpack the options.
    let { host, source, trusted, sanitizer, resolver, linkHandler, shouldTypeset, latexTypesetter, translator } = options;
    translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
    const trans = translator === null || translator === void 0 ? void 0 : translator.load('jupyterlab');
    let originalSource = source;
    // Bail early if the source is empty.
    if (!source) {
        host.textContent = '';
        return Promise.resolve(undefined);
    }
    // Sanitize the source if it is not trusted. This removes all
    // `<script>` tags as well as other potentially harmful HTML.
    if (!trusted) {
        originalSource = `${source}`;
        source = sanitizer.sanitize(source);
    }
    // Set the inner HTML of the host.
    host.innerHTML = source;
    if (host.getElementsByTagName('script').length > 0) {
        // If output it trusted, eval any script tags contained in the HTML.
        // This is not done automatically by the browser when script tags are
        // created by setting `innerHTML`.
        if (trusted) {
            Private.evalInnerHTMLScriptTags(host);
        }
        else {
            const container = document.createElement('div');
            const warning = document.createElement('pre');
            warning.textContent = trans.__('This HTML output contains inline scripts. Are you sure that you want to run arbitrary Javascript within your JupyterLab session?');
            const runButton = document.createElement('button');
            runButton.textContent = trans.__('Run');
            runButton.onclick = event => {
                host.innerHTML = originalSource;
                Private.evalInnerHTMLScriptTags(host);
                if (host.firstChild) {
                    host.removeChild(host.firstChild);
                }
            };
            container.appendChild(warning);
            container.appendChild(runButton);
            host.insertBefore(container, host.firstChild);
        }
    }
    // Handle default behavior of nodes.
    Private.handleDefaults(host, resolver);
    // Patch the urls if a resolver is available.
    let promise;
    if (resolver) {
        promise = Private.handleUrls(host, resolver, linkHandler);
    }
    else {
        promise = Promise.resolve(undefined);
    }
    // Return the final rendered promise.
    return promise.then(() => {
        if (shouldTypeset && latexTypesetter) {
            latexTypesetter.typeset(host);
        }
    });
}
/**
 * Render an image into a host node.
 *
 * @param options - The options for rendering.
 *
 * @returns A promise which resolves when rendering is complete.
 */
function renderImage(options) {
    // Unpack the options.
    const { host, mimeType, source, width, height, needsBackground, unconfined } = options;
    // Clear the content in the host.
    host.textContent = '';
    // Create the image element.
    const img = document.createElement('img');
    // Set the source of the image.
    img.src = `data:${mimeType};base64,${source}`;
    // Set the size of the image if provided.
    if (typeof height === 'number') {
        img.height = height;
    }
    if (typeof width === 'number') {
        img.width = width;
    }
    if (needsBackground === 'light') {
        img.classList.add('jp-needs-light-background');
    }
    else if (needsBackground === 'dark') {
        img.classList.add('jp-needs-dark-background');
    }
    if (unconfined === true) {
        img.classList.add('jp-mod-unconfined');
    }
    // Add the image to the host.
    host.appendChild(img);
    // Return the rendered promise.
    return Promise.resolve(undefined);
}
/**
 * Render LaTeX into a host node.
 *
 * @param options - The options for rendering.
 *
 * @returns A promise which resolves when rendering is complete.
 */
function renderLatex(options) {
    // Unpack the options.
    const { host, source, shouldTypeset, latexTypesetter } = options;
    // Set the source on the node.
    host.textContent = source;
    // Typeset the node if needed.
    if (shouldTypeset && latexTypesetter) {
        latexTypesetter.typeset(host);
    }
    // Return the rendered promise.
    return Promise.resolve(undefined);
}
/**
 * Render Markdown into a host node.
 *
 * @param options - The options for rendering.
 *
 * @returns A promise which resolves when rendering is complete.
 */
async function renderMarkdown(options) {
    // Unpack the options.
    const { host, source, markdownParser, ...others } = options;
    // Clear the content if there is no source.
    if (!source) {
        host.textContent = '';
        return;
    }
    let html = '';
    if (markdownParser) {
        // Separate math from normal markdown text.
        const parts = (0,_latex__WEBPACK_IMPORTED_MODULE_3__/* .removeMath */ .D)(source);
        // Convert the markdown to HTML.
        html = await markdownParser.render(parts['text']);
        // Replace math.
        html = (0,_latex__WEBPACK_IMPORTED_MODULE_3__/* .replaceMath */ .b)(html, parts['math']);
    }
    else {
        // Fallback if the application does not have any markdown parser.
        html = `<pre>${source}</pre>`;
    }
    // Render HTML.
    await renderHTML({
        host,
        source: html,
        ...others
    });
    // Apply ids to the header nodes.
    Private.headerAnchors(host);
}
/**
 * The namespace for the `renderMarkdown` function statics.
 */
(function (renderMarkdown) {
    /**
     * Create a normalized id for a header element.
     *
     * @param header Header element
     * @returns Normalized id
     */
    function createHeaderId(header) {
        var _a;
        return ((_a = header.textContent) !== null && _a !== void 0 ? _a : '').replace(/ /g, '-');
    }
    renderMarkdown.createHeaderId = createHeaderId;
})(renderMarkdown || (renderMarkdown = {}));
/**
 * Render SVG into a host node.
 *
 * @param options - The options for rendering.
 *
 * @returns A promise which resolves when rendering is complete.
 */
function renderSVG(options) {
    // Unpack the options.
    let { host, source, trusted, unconfined } = options;
    // Clear the content if there is no source.
    if (!source) {
        host.textContent = '';
        return Promise.resolve(undefined);
    }
    // Display a message if the source is not trusted.
    if (!trusted) {
        host.textContent =
            'Cannot display an untrusted SVG. Maybe you need to run the cell?';
        return Promise.resolve(undefined);
    }
    // Add missing SVG namespace (if actually missing)
    const patt = '<svg[^>]+xmlns=[^>]+svg';
    if (source.search(patt) < 0) {
        source = source.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"');
    }
    // Render in img so that user can save it easily
    const img = new Image();
    img.src = `data:image/svg+xml,${encodeURIComponent(source)}`;
    host.appendChild(img);
    if (unconfined === true) {
        host.classList.add('jp-mod-unconfined');
    }
    return Promise.resolve();
}
/**
 * Replace URLs with links.
 *
 * @param content - The text content of a node.
 *
 * @returns A list of text nodes and anchor elements.
 */
function autolink(content) {
    // Taken from Visual Studio Code:
    // https://github.com/microsoft/vscode/blob/9f709d170b06e991502153f281ec3c012add2e42/src/vs/workbench/contrib/debug/browser/linkDetector.ts#L17-L18
    const controlCodes = '\\u0000-\\u0020\\u007f-\\u009f';
    const webLinkRegex = new RegExp('(?:[a-zA-Z][a-zA-Z0-9+.-]{2,}:\\/\\/|data:|www\\.)[^\\s' +
        controlCodes +
        '"]{2,}[^\\s' +
        controlCodes +
        '"\'(){}\\[\\],:;.!?]', 'ug');
    const nodes = [];
    let lastIndex = 0;
    let match;
    while (null != (match = webLinkRegex.exec(content))) {
        if (match.index !== lastIndex) {
            nodes.push(document.createTextNode(content.slice(lastIndex, match.index)));
        }
        let url = match[0];
        // Special case when the URL ends with ">" or "<"
        const lastChars = url.slice(-1);
        const endsWithGtLt = ['>', '<'].indexOf(lastChars) !== -1;
        const len = endsWithGtLt ? url.length - 1 : url.length;
        const anchor = document.createElement('a');
        url = url.slice(0, len);
        anchor.href = url.startsWith('www.') ? 'https://' + url : url;
        anchor.rel = 'noopener';
        anchor.target = '_blank';
        anchor.appendChild(document.createTextNode(url.slice(0, len)));
        nodes.push(anchor);
        lastIndex = match.index + len;
    }
    if (lastIndex !== content.length) {
        nodes.push(document.createTextNode(content.slice(lastIndex, content.length)));
    }
    return nodes;
}
/**
 * Split a shallow node (node without nested nodes inside) at a given text content position.
 *
 * @param node the shallow node to be split
 * @param at the position in textContent at which the split should occur
 */
function splitShallowNode(node, at) {
    var _a, _b;
    const pre = node.cloneNode();
    pre.textContent = (_a = node.textContent) === null || _a === void 0 ? void 0 : _a.slice(0, at);
    const post = node.cloneNode();
    post.textContent = (_b = node.textContent) === null || _b === void 0 ? void 0 : _b.slice(at);
    return {
        pre,
        post
    };
}
/**
 * Iterate over some nodes, while tracking cumulative start and end position.
 */
function* nodeIter(nodes) {
    var _a;
    let start = 0;
    let end;
    for (let node of nodes) {
        end = start + (((_a = node.textContent) === null || _a === void 0 ? void 0 : _a.length) || 0);
        yield {
            node,
            start,
            end,
            isText: node.nodeType === Node.TEXT_NODE
        };
        start = end;
    }
}
/**
 * Align two collections of nodes.
 *
 * If a text node in one collections spans an element in the other, yield the spanned elements.
 * Otherwise, split the nodes such that yielded pair start and stop on the same position.
 */
function* alignedNodes(a, b) {
    var _a, _b;
    let iterA = nodeIter(a);
    let iterB = nodeIter(b);
    let nA = iterA.next();
    let nB = iterB.next();
    while (!nA.done && !nB.done) {
        let A = nA.value;
        let B = nB.value;
        if (A.isText && A.start <= B.start && A.end >= B.end) {
            // A is a text element that spans all of B, simply yield B
            yield [null, B.node];
            nB = iterB.next();
        }
        else if (B.isText && B.start <= A.start && B.end >= A.end) {
            // B is a text element that spans all of A, simply yield A
            yield [A.node, null];
            nA = iterA.next();
        }
        else {
            // There is some intersection, split one, unless they match exactly
            if (A.end === B.end && A.start === B.start) {
                yield [A.node, B.node];
                nA = iterA.next();
                nB = iterB.next();
            }
            else if (A.end > B.end) {
                /*
                A |-----[======]---|
                B |--[======]------|
                            | <- Split A here
                        | <- trim B to start from here if needed
                */
                let { pre, post } = splitShallowNode(A.node, B.end - A.start);
                if (B.start < A.start) {
                    // this node should not be yielded anywhere else, so ok to modify in-place
                    B.node.textContent = (_a = B.node.textContent) === null || _a === void 0 ? void 0 : _a.slice(A.start - B.start);
                }
                yield [pre, B.node];
                // Modify iteration result in-place:
                A.node = post;
                A.start = B.end;
                nB = iterB.next();
            }
            else if (B.end > A.end) {
                let { pre, post } = splitShallowNode(B.node, A.end - B.start);
                if (A.start < B.start) {
                    // this node should not be yielded anywhere else, so ok to modify in-place
                    A.node.textContent = (_b = A.node.textContent) === null || _b === void 0 ? void 0 : _b.slice(B.start - A.start);
                }
                yield [A.node, pre];
                // Modify iteration result in-place:
                B.node = post;
                B.start = A.end;
                nA = iterA.next();
            }
            else {
                throw new Error(`Unexpected intersection: ${JSON.stringify(A)} ${JSON.stringify(B)}`);
            }
        }
    }
}
/**
 * Render text into a host node.
 *
 * @param options - The options for rendering.
 *
 * @returns A promise which resolves when rendering is complete.
 */
function renderText(options) {
    var _a, _b;
    // Unpack the options.
    const { host, sanitizer, source } = options;
    // Create the HTML content.
    const content = sanitizer.sanitize(Private.ansiSpan(source), {
        allowedTags: ['span']
    });
    // Set the sanitized content for the host node.
    const ret = document.createElement('pre');
    const pre = document.createElement('pre');
    pre.innerHTML = content;
    const preTextContent = pre.textContent;
    if (preTextContent) {
        // Note: only text nodes and span elements should be present after sanitization in the `<pre>` element.
        const linkedNodes = ((_b = (_a = sanitizer.getAutolink) === null || _a === void 0 ? void 0 : _a.call(sanitizer)) !== null && _b !== void 0 ? _b : true)
            ? autolink(preTextContent)
            : [document.createTextNode(content)];
        let inAnchorElement = false;
        const combinedNodes = [];
        const preNodes = Array.from(pre.childNodes);
        for (let nodes of alignedNodes(preNodes, linkedNodes)) {
            if (!nodes[0]) {
                combinedNodes.push(nodes[1]);
                inAnchorElement = nodes[1].nodeType !== Node.TEXT_NODE;
                continue;
            }
            else if (!nodes[1]) {
                combinedNodes.push(nodes[0]);
                inAnchorElement = false;
                continue;
            }
            let [preNode, linkNode] = nodes;
            const lastCombined = combinedNodes[combinedNodes.length - 1];
            // If we are already in an anchor element and the anchor element did not change,
            // we should insert the node from <pre> which is either Text node or coloured span Element
            // into the anchor content as a child
            if (inAnchorElement &&
                linkNode.href ===
                    lastCombined.href) {
                lastCombined.appendChild(preNode);
            }
            else {
                // the `linkNode` is either Text or AnchorElement;
                const isAnchor = linkNode.nodeType !== Node.TEXT_NODE;
                // if we are NOT about to start an anchor element, just add the pre Node
                if (!isAnchor) {
                    combinedNodes.push(preNode);
                    inAnchorElement = false;
                }
                else {
                    // otherwise start a new anchor; the contents of the `linkNode` and `preNode` should be the same,
                    // so we just put the neatly formatted `preNode` inside the anchor node (`linkNode`)
                    // and append that to combined nodes.
                    linkNode.textContent = '';
                    linkNode.appendChild(preNode);
                    combinedNodes.push(linkNode);
                    inAnchorElement = true;
                }
            }
        }
        // Do not reuse `pre` element. Clearing out previous children is too slow...
        for (const child of combinedNodes) {
            ret.appendChild(child);
        }
    }
    host.appendChild(ret);
    // Return the rendered promise.
    return Promise.resolve(undefined);
}
/**
 * The namespace for module implementation details.
 */
var Private;
(function (Private) {
    /**
     * Eval the script tags contained in a host populated by `innerHTML`.
     *
     * When script tags are created via `innerHTML`, the browser does not
     * evaluate them when they are added to the page. This function works
     * around that by creating new equivalent script nodes manually, and
     * replacing the originals.
     */
    function evalInnerHTMLScriptTags(host) {
        // Create a snapshot of the current script nodes.
        const scripts = Array.from(host.getElementsByTagName('script'));
        // Loop over each script node.
        for (const script of scripts) {
            // Skip any scripts which no longer have a parent.
            if (!script.parentNode) {
                continue;
            }
            // Create a new script node which will be clone.
            const clone = document.createElement('script');
            // Copy the attributes into the clone.
            const attrs = script.attributes;
            for (let i = 0, n = attrs.length; i < n; ++i) {
                const { name, value } = attrs[i];
                clone.setAttribute(name, value);
            }
            // Copy the text content into the clone.
            clone.textContent = script.textContent;
            // Replace the old script in the parent.
            script.parentNode.replaceChild(clone, script);
        }
    }
    Private.evalInnerHTMLScriptTags = evalInnerHTMLScriptTags;
    /**
     * Handle the default behavior of nodes.
     */
    function handleDefaults(node, resolver) {
        // Handle anchor elements.
        const anchors = node.getElementsByTagName('a');
        for (let i = 0; i < anchors.length; i++) {
            const el = anchors[i];
            // skip when processing a elements inside svg
            // which are of type SVGAnimatedString
            if (!(el instanceof HTMLAnchorElement)) {
                continue;
            }
            const path = el.href;
            const isLocal = resolver && resolver.isLocal
                ? resolver.isLocal(path)
                : _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.isLocal(path);
            // set target attribute if not already present
            if (!el.target) {
                el.target = isLocal ? '_self' : '_blank';
            }
            // set rel as 'noopener' for non-local anchors
            if (!isLocal) {
                el.rel = 'noopener';
            }
        }
        // Handle image elements.
        const imgs = node.getElementsByTagName('img');
        for (let i = 0; i < imgs.length; i++) {
            if (!imgs[i].alt) {
                imgs[i].alt = 'Image';
            }
        }
    }
    Private.handleDefaults = handleDefaults;
    /**
     * Resolve the relative urls in element `src` and `href` attributes.
     *
     * @param node - The head html element.
     *
     * @param resolver - A url resolver.
     *
     * @param linkHandler - An optional link handler for nodes.
     *
     * @returns a promise fulfilled when the relative urls have been resolved.
     */
    function handleUrls(node, resolver, linkHandler) {
        // Set up an array to collect promises.
        const promises = [];
        // Handle HTML Elements with src attributes.
        const nodes = node.querySelectorAll('*[src]');
        for (let i = 0; i < nodes.length; i++) {
            promises.push(handleAttr(nodes[i], 'src', resolver));
        }
        // Handle anchor elements.
        const anchors = node.getElementsByTagName('a');
        for (let i = 0; i < anchors.length; i++) {
            promises.push(handleAnchor(anchors[i], resolver, linkHandler));
        }
        // Handle link elements.
        const links = node.getElementsByTagName('link');
        for (let i = 0; i < links.length; i++) {
            promises.push(handleAttr(links[i], 'href', resolver));
        }
        // Wait on all promises.
        return Promise.all(promises).then(() => undefined);
    }
    Private.handleUrls = handleUrls;
    /**
     * Apply ids to headers.
     */
    function headerAnchors(node) {
        const headerNames = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'];
        for (const headerType of headerNames) {
            const headers = node.getElementsByTagName(headerType);
            for (let i = 0; i < headers.length; i++) {
                const header = headers[i];
                header.id = renderMarkdown.createHeaderId(header);
                const anchor = document.createElement('a');
                anchor.target = '_self';
                anchor.textContent = '¶';
                anchor.href = '#' + header.id;
                anchor.classList.add('jp-InternalAnchorLink');
                header.appendChild(anchor);
            }
        }
    }
    Private.headerAnchors = headerAnchors;
    /**
     * Handle a node with a `src` or `href` attribute.
     */
    async function handleAttr(node, name, resolver) {
        const source = node.getAttribute(name) || '';
        const isLocal = resolver.isLocal
            ? resolver.isLocal(source)
            : _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.isLocal(source);
        if (!source || !isLocal) {
            return;
        }
        try {
            const urlPath = await resolver.resolveUrl(source);
            let url = await resolver.getDownloadUrl(urlPath);
            if (_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.parse(url).protocol !== 'data:') {
                // Bust caching for local src attrs.
                // https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/Using_XMLHttpRequest#Bypassing_the_cache
                url += (/\?/.test(url) ? '&' : '?') + new Date().getTime();
            }
            node.setAttribute(name, url);
        }
        catch (err) {
            // If there was an error getting the url,
            // just make it an empty link and report the error.
            node.setAttribute(name, '');
            throw err;
        }
    }
    /**
     * Handle an anchor node.
     */
    function handleAnchor(anchor, resolver, linkHandler) {
        // Get the link path without the location prepended.
        // (e.g. "./foo.md#Header 1" vs "http://localhost:8888/foo.md#Header 1")
        let href = anchor.getAttribute('href') || '';
        const isLocal = resolver.isLocal
            ? resolver.isLocal(href)
            : _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.isLocal(href);
        // Bail if it is not a file-like url.
        if (!href || !isLocal) {
            return Promise.resolve(undefined);
        }
        // Remove the hash until we can handle it.
        const hash = anchor.hash;
        if (hash) {
            // Handle internal link in the file.
            if (hash === href) {
                anchor.target = '_self';
                return Promise.resolve(undefined);
            }
            // For external links, remove the hash until we have hash handling.
            href = href.replace(hash, '');
        }
        // Get the appropriate file path.
        return resolver
            .resolveUrl(href)
            .then(urlPath => {
            // decode encoded url from url to api path
            const path = decodeURIComponent(urlPath);
            // Handle the click override.
            if (linkHandler) {
                linkHandler.handleLink(anchor, path, hash);
            }
            // Get the appropriate file download path.
            return resolver.getDownloadUrl(urlPath);
        })
            .then(url => {
            // Set the visible anchor.
            anchor.href = url + hash;
        })
            .catch(err => {
            // If there was an error getting the url,
            // just make it an empty link.
            anchor.href = '';
        });
    }
    const ANSI_COLORS = [
        'ansi-black',
        'ansi-red',
        'ansi-green',
        'ansi-yellow',
        'ansi-blue',
        'ansi-magenta',
        'ansi-cyan',
        'ansi-white',
        'ansi-black-intense',
        'ansi-red-intense',
        'ansi-green-intense',
        'ansi-yellow-intense',
        'ansi-blue-intense',
        'ansi-magenta-intense',
        'ansi-cyan-intense',
        'ansi-white-intense'
    ];
    /**
     * Create HTML tags for a string with given foreground, background etc. and
     * add them to the `out` array.
     */
    function pushColoredChunk(chunk, fg, bg, bold, underline, inverse, out) {
        if (chunk) {
            const classes = [];
            const styles = [];
            if (bold && typeof fg === 'number' && 0 <= fg && fg < 8) {
                fg += 8; // Bold text uses "intense" colors
            }
            if (inverse) {
                [fg, bg] = [bg, fg];
            }
            if (typeof fg === 'number') {
                classes.push(ANSI_COLORS[fg] + '-fg');
            }
            else if (fg.length) {
                styles.push(`color: rgb(${fg})`);
            }
            else if (inverse) {
                classes.push('ansi-default-inverse-fg');
            }
            if (typeof bg === 'number') {
                classes.push(ANSI_COLORS[bg] + '-bg');
            }
            else if (bg.length) {
                styles.push(`background-color: rgb(${bg})`);
            }
            else if (inverse) {
                classes.push('ansi-default-inverse-bg');
            }
            if (bold) {
                classes.push('ansi-bold');
            }
            if (underline) {
                classes.push('ansi-underline');
            }
            if (classes.length || styles.length) {
                out.push('<span');
                if (classes.length) {
                    out.push(` class="${classes.join(' ')}"`);
                }
                if (styles.length) {
                    out.push(` style="${styles.join('; ')}"`);
                }
                out.push('>');
                out.push(chunk);
                out.push('</span>');
            }
            else {
                out.push(chunk);
            }
        }
    }
    /**
     * Convert ANSI extended colors to R/G/B triple.
     */
    function getExtendedColors(numbers) {
        let r;
        let g;
        let b;
        const n = numbers.shift();
        if (n === 2 && numbers.length >= 3) {
            // 24-bit RGB
            r = numbers.shift();
            g = numbers.shift();
            b = numbers.shift();
            if ([r, g, b].some(c => c < 0 || 255 < c)) {
                throw new RangeError('Invalid range for RGB colors');
            }
        }
        else if (n === 5 && numbers.length >= 1) {
            // 256 colors
            const idx = numbers.shift();
            if (idx < 0) {
                throw new RangeError('Color index must be >= 0');
            }
            else if (idx < 16) {
                // 16 default terminal colors
                return idx;
            }
            else if (idx < 232) {
                // 6x6x6 color cube, see https://stackoverflow.com/a/27165165/500098
                r = Math.floor((idx - 16) / 36);
                r = r > 0 ? 55 + r * 40 : 0;
                g = Math.floor(((idx - 16) % 36) / 6);
                g = g > 0 ? 55 + g * 40 : 0;
                b = (idx - 16) % 6;
                b = b > 0 ? 55 + b * 40 : 0;
            }
            else if (idx < 256) {
                // grayscale, see https://stackoverflow.com/a/27165165/500098
                r = g = b = (idx - 232) * 10 + 8;
            }
            else {
                throw new RangeError('Color index must be < 256');
            }
        }
        else {
            throw new RangeError('Invalid extended color specification');
        }
        return [r, g, b];
    }
    /**
     * Transform ANSI color escape codes into HTML <span> tags with CSS
     * classes such as "ansi-green-intense-fg".
     * The actual colors used are set in the CSS file.
     * This also removes non-color escape sequences.
     * This is supposed to have the same behavior as nbconvert.filters.ansi2html()
     */
    function ansiSpan(str) {
        const ansiRe = /\x1b\[(.*?)([@-~])/g; // eslint-disable-line no-control-regex
        let fg = [];
        let bg = [];
        let bold = false;
        let underline = false;
        let inverse = false;
        let match;
        const out = [];
        const numbers = [];
        let start = 0;
        str = lodash_escape__WEBPACK_IMPORTED_MODULE_2___default()(str);
        str += '\x1b[m'; // Ensure markup for trailing text
        // tslint:disable-next-line
        while ((match = ansiRe.exec(str))) {
            if (match[2] === 'm') {
                const items = match[1].split(';');
                for (let i = 0; i < items.length; i++) {
                    const item = items[i];
                    if (item === '') {
                        numbers.push(0);
                    }
                    else if (item.search(/^\d+$/) !== -1) {
                        numbers.push(parseInt(item, 10));
                    }
                    else {
                        // Ignored: Invalid color specification
                        numbers.length = 0;
                        break;
                    }
                }
            }
            else {
                // Ignored: Not a color code
            }
            const chunk = str.substring(start, match.index);
            pushColoredChunk(chunk, fg, bg, bold, underline, inverse, out);
            start = ansiRe.lastIndex;
            while (numbers.length) {
                const n = numbers.shift();
                switch (n) {
                    case 0:
                        fg = bg = [];
                        bold = false;
                        underline = false;
                        inverse = false;
                        break;
                    case 1:
                    case 5:
                        bold = true;
                        break;
                    case 4:
                        underline = true;
                        break;
                    case 7:
                        inverse = true;
                        break;
                    case 21:
                    case 22:
                        bold = false;
                        break;
                    case 24:
                        underline = false;
                        break;
                    case 27:
                        inverse = false;
                        break;
                    case 30:
                    case 31:
                    case 32:
                    case 33:
                    case 34:
                    case 35:
                    case 36:
                    case 37:
                        fg = n - 30;
                        break;
                    case 38:
                        try {
                            fg = getExtendedColors(numbers);
                        }
                        catch (e) {
                            numbers.length = 0;
                        }
                        break;
                    case 39:
                        fg = [];
                        break;
                    case 40:
                    case 41:
                    case 42:
                    case 43:
                    case 44:
                    case 45:
                    case 46:
                    case 47:
                        bg = n - 40;
                        break;
                    case 48:
                        try {
                            bg = getExtendedColors(numbers);
                        }
                        catch (e) {
                            numbers.length = 0;
                        }
                        break;
                    case 49:
                        bg = [];
                        break;
                    case 90:
                    case 91:
                    case 92:
                    case 93:
                    case 94:
                    case 95:
                    case 96:
                    case 97:
                        fg = n - 90 + 8;
                        break;
                    case 100:
                    case 101:
                    case 102:
                    case 103:
                    case 104:
                    case 105:
                    case 106:
                    case 107:
                        bg = n - 100 + 8;
                        break;
                    default:
                    // Unknown codes are ignored
                }
            }
        }
        return out.join('');
    }
    Private.ansiSpan = ansiSpan;
})(Private || (Private = {}));


/***/ }),

/***/ 175:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ZD": () => (/* binding */ IRenderMimeRegistry),
/* harmony export */   "_y": () => (/* binding */ ILatexTypesetter),
/* harmony export */   "sc": () => (/* binding */ IMarkdownParser)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(22100);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/

/**
 * The rendermime token.
 */
const IRenderMimeRegistry = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/rendermime:IRenderMimeRegistry', 'A service for the rendermime registry for the application. Use this to create renderers for various mime-types in your extension. Many times it will be easier to create a "mime renderer extension" rather than using this service directly.');
/**
 * The latex typesetter token.
 */
const ILatexTypesetter = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/rendermime:ILatexTypesetter', 'A service for the LaTeX typesetter for the application. Use this if you want to typeset math in your extension.');
/**
 * The markdown parser token.
 */
const IMarkdownParser = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/rendermime:IMarkdownParser', 'A service for rendering markdown syntax as HTML content.');


/***/ }),

/***/ 86580:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BP": () => (/* binding */ RenderedHTMLCommon),
/* harmony export */   "FK": () => (/* binding */ RenderedLatex),
/* harmony export */   "ND": () => (/* binding */ RenderedJavaScript),
/* harmony export */   "UH": () => (/* binding */ RenderedImage),
/* harmony export */   "cw": () => (/* binding */ RenderedMarkdown),
/* harmony export */   "lH": () => (/* binding */ RenderedText),
/* harmony export */   "oI": () => (/* binding */ RenderedHTML),
/* harmony export */   "pY": () => (/* binding */ RenderedCommon),
/* harmony export */   "zt": () => (/* binding */ RenderedSVG)
/* harmony export */ });
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(72234);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _renderers__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(14769);



/**
 * A common base class for mime renderers.
 */
class RenderedCommon extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    /**
     * Construct a new rendered common widget.
     *
     * @param options - The options for initializing the widget.
     */
    constructor(options) {
        var _a, _b;
        super();
        this.mimeType = options.mimeType;
        this.sanitizer = options.sanitizer;
        this.resolver = options.resolver;
        this.linkHandler = options.linkHandler;
        this.translator = (_a = options.translator) !== null && _a !== void 0 ? _a : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__.nullTranslator;
        this.latexTypesetter = options.latexTypesetter;
        this.markdownParser = (_b = options.markdownParser) !== null && _b !== void 0 ? _b : null;
        this.node.dataset['mimeType'] = this.mimeType;
    }
    /**
     * Render a mime model.
     *
     * @param model - The mime model to render.
     *
     * @param keepExisting - Whether to keep the existing rendering.
     *
     * @returns A promise which resolves when rendering is complete.
     *
     * #### Notes
     * By default, if the DOM node for this widget already has content, it
     * is emptied before rendering. Subclasses that do not want this behavior
     * (if, for instance, they are using DOM diffing), should override this
     * method or call `super.renderModel(model, true)`.
     */
    async renderModel(model, keepExisting) {
        // TODO compare model against old model for early bail?
        // Empty any existing content in the node from previous renders
        if (!keepExisting) {
            while (this.node.firstChild) {
                this.node.removeChild(this.node.firstChild);
            }
        }
        // Toggle the trusted class on the widget.
        this.toggleClass('jp-mod-trusted', model.trusted);
        // Render the actual content.
        await this.render(model);
        // Handle the fragment identifier if given.
        const { fragment } = model.metadata;
        if (fragment) {
            this.setFragment(fragment);
        }
    }
    /**
     * Set the URI fragment identifier.
     *
     * @param fragment - The URI fragment identifier.
     */
    setFragment(fragment) {
        /* no-op */
    }
}
/**
 * A common base class for HTML mime renderers.
 */
class RenderedHTMLCommon extends RenderedCommon {
    /**
     * Construct a new rendered HTML common widget.
     *
     * @param options - The options for initializing the widget.
     */
    constructor(options) {
        super(options);
        this.addClass('jp-RenderedHTMLCommon');
    }
    setFragment(fragment) {
        let el;
        try {
            el = this.node.querySelector(fragment.startsWith('#')
                ? `#${CSS.escape(fragment.slice(1))}`
                : fragment);
        }
        catch (error) {
            console.warn('Unable to set URI fragment identifier.', error);
        }
        if (el) {
            el.scrollIntoView();
        }
    }
}
/**
 * A mime renderer for displaying HTML and math.
 */
class RenderedHTML extends RenderedHTMLCommon {
    /**
     * Construct a new rendered HTML widget.
     *
     * @param options - The options for initializing the widget.
     */
    constructor(options) {
        super(options);
        this.addClass('jp-RenderedHTML');
    }
    /**
     * Render a mime model.
     *
     * @param model - The mime model to render.
     *
     * @returns A promise which resolves when rendering is complete.
     */
    render(model) {
        return _renderers__WEBPACK_IMPORTED_MODULE_2__/* .renderHTML */ .NN({
            host: this.node,
            source: String(model.data[this.mimeType]),
            trusted: model.trusted,
            resolver: this.resolver,
            sanitizer: this.sanitizer,
            linkHandler: this.linkHandler,
            shouldTypeset: this.isAttached,
            latexTypesetter: this.latexTypesetter,
            translator: this.translator
        });
    }
    /**
     * A message handler invoked on an `'after-attach'` message.
     */
    onAfterAttach(msg) {
        if (this.latexTypesetter) {
            this.latexTypesetter.typeset(this.node);
        }
    }
}
/**
 * A mime renderer for displaying LaTeX output.
 */
class RenderedLatex extends RenderedCommon {
    /**
     * Construct a new rendered LaTeX widget.
     *
     * @param options - The options for initializing the widget.
     */
    constructor(options) {
        super(options);
        this.addClass('jp-RenderedLatex');
    }
    /**
     * Render a mime model.
     *
     * @param model - The mime model to render.
     *
     * @returns A promise which resolves when rendering is complete.
     */
    render(model) {
        return _renderers__WEBPACK_IMPORTED_MODULE_2__/* .renderLatex */ .K3({
            host: this.node,
            source: String(model.data[this.mimeType]),
            shouldTypeset: this.isAttached,
            latexTypesetter: this.latexTypesetter
        });
    }
    /**
     * A message handler invoked on an `'after-attach'` message.
     */
    onAfterAttach(msg) {
        if (this.latexTypesetter) {
            this.latexTypesetter.typeset(this.node);
        }
    }
}
/**
 * A mime renderer for displaying images.
 */
class RenderedImage extends RenderedCommon {
    /**
     * Construct a new rendered image widget.
     *
     * @param options - The options for initializing the widget.
     */
    constructor(options) {
        super(options);
        this.addClass('jp-RenderedImage');
    }
    /**
     * Render a mime model.
     *
     * @param model - The mime model to render.
     *
     * @returns A promise which resolves when rendering is complete.
     */
    render(model) {
        const metadata = model.metadata[this.mimeType];
        return _renderers__WEBPACK_IMPORTED_MODULE_2__/* .renderImage */ .co({
            host: this.node,
            mimeType: this.mimeType,
            source: String(model.data[this.mimeType]),
            width: metadata && metadata.width,
            height: metadata && metadata.height,
            needsBackground: model.metadata['needs_background'],
            unconfined: metadata && metadata.unconfined
        });
    }
}
/**
 * A mime renderer for displaying Markdown with embedded latex.
 */
class RenderedMarkdown extends RenderedHTMLCommon {
    /**
     * Construct a new rendered markdown widget.
     *
     * @param options - The options for initializing the widget.
     */
    constructor(options) {
        super(options);
        this.addClass('jp-RenderedMarkdown');
    }
    /**
     * Render a mime model.
     *
     * @param model - The mime model to render.
     *
     * @returns A promise which resolves when rendering is complete.
     */
    render(model) {
        return _renderers__WEBPACK_IMPORTED_MODULE_2__/* .renderMarkdown */ .ap({
            host: this.node,
            source: String(model.data[this.mimeType]),
            trusted: model.trusted,
            resolver: this.resolver,
            sanitizer: this.sanitizer,
            linkHandler: this.linkHandler,
            shouldTypeset: this.isAttached,
            latexTypesetter: this.latexTypesetter,
            markdownParser: this.markdownParser,
            translator: this.translator
        });
    }
    /**
     * Render a mime model.
     *
     * @param model - The mime model to render.
     *
     * @returns A promise which resolves when rendering is complete.
     */
    async renderModel(model) {
        await super.renderModel(model, true);
    }
    /**
     * A message handler invoked on an `'after-attach'` message.
     */
    onAfterAttach(msg) {
        if (this.latexTypesetter) {
            this.latexTypesetter.typeset(this.node);
        }
    }
}
/**
 * A widget for displaying SVG content.
 */
class RenderedSVG extends RenderedCommon {
    /**
     * Construct a new rendered SVG widget.
     *
     * @param options - The options for initializing the widget.
     */
    constructor(options) {
        super(options);
        this.addClass('jp-RenderedSVG');
    }
    /**
     * Render a mime model.
     *
     * @param model - The mime model to render.
     *
     * @returns A promise which resolves when rendering is complete.
     */
    render(model) {
        const metadata = model.metadata[this.mimeType];
        return _renderers__WEBPACK_IMPORTED_MODULE_2__/* .renderSVG */ .KB({
            host: this.node,
            source: String(model.data[this.mimeType]),
            trusted: model.trusted,
            unconfined: metadata && metadata.unconfined,
            translator: this.translator
        });
    }
    /**
     * A message handler invoked on an `'after-attach'` message.
     */
    onAfterAttach(msg) {
        if (this.latexTypesetter) {
            this.latexTypesetter.typeset(this.node);
        }
    }
}
/**
 * A widget for displaying plain text and console text.
 */
class RenderedText extends RenderedCommon {
    /**
     * Construct a new rendered text widget.
     *
     * @param options - The options for initializing the widget.
     */
    constructor(options) {
        super(options);
        this.addClass('jp-RenderedText');
    }
    /**
     * Render a mime model.
     *
     * @param model - The mime model to render.
     *
     * @returns A promise which resolves when rendering is complete.
     */
    render(model) {
        return _renderers__WEBPACK_IMPORTED_MODULE_2__/* .renderText */ .IY({
            host: this.node,
            sanitizer: this.sanitizer,
            source: String(model.data[this.mimeType]),
            translator: this.translator
        });
    }
}
/**
 * A widget for displaying JavaScript output.
 */
class RenderedJavaScript extends RenderedCommon {
    /**
     * Construct a new rendered text widget.
     *
     * @param options - The options for initializing the widget.
     */
    constructor(options) {
        super(options);
        this.addClass('jp-RenderedJavaScript');
    }
    /**
     * Render a mime model.
     *
     * @param model - The mime model to render.
     *
     * @returns A promise which resolves when rendering is complete.
     */
    render(model) {
        const trans = this.translator.load('jupyterlab');
        return _renderers__WEBPACK_IMPORTED_MODULE_2__/* .renderText */ .IY({
            host: this.node,
            sanitizer: this.sanitizer,
            source: trans.__('JavaScript output is disabled in JupyterLab'),
            translator: this.translator
        });
    }
}


/***/ })

}]);
//# sourceMappingURL=3189.ed73a4a997c815278b39.js.map?v=ed73a4a997c815278b39