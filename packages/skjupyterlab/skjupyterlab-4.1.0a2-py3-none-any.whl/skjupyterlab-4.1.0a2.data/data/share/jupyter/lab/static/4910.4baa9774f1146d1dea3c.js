"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[4910],{

/***/ 4910:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "CodeMirrorEditor": () => (/* reexport */ CodeMirrorEditor),
  "CodeMirrorEditorFactory": () => (/* reexport */ CodeMirrorEditorFactory),
  "CodeMirrorMimeTypeService": () => (/* reexport */ CodeMirrorMimeTypeService),
  "CodeMirrorSearchHighlighter": () => (/* reexport */ CodeMirrorSearchHighlighter),
  "EditorExtensionRegistry": () => (/* reexport */ EditorExtensionRegistry),
  "EditorLanguageRegistry": () => (/* reexport */ EditorLanguageRegistry),
  "EditorSearchProvider": () => (/* reexport */ EditorSearchProvider),
  "EditorThemeRegistry": () => (/* reexport */ EditorThemeRegistry),
  "ExtensionsHandler": () => (/* reexport */ ExtensionsHandler),
  "IEditorExtensionRegistry": () => (/* reexport */ IEditorExtensionRegistry),
  "IEditorLanguageRegistry": () => (/* reexport */ IEditorLanguageRegistry),
  "IEditorThemeRegistry": () => (/* reexport */ IEditorThemeRegistry),
  "StateCommands": () => (/* reexport */ StateCommands),
  "YRange": () => (/* reexport */ YRange),
  "YSyncConfig": () => (/* reexport */ YSyncConfig),
  "customTheme": () => (/* reexport */ customTheme),
  "jupyterEditorTheme": () => (/* reexport */ jupyterEditorTheme),
  "jupyterHighlightStyle": () => (/* reexport */ jupyterHighlightStyle),
  "jupyterTheme": () => (/* reexport */ jupyterTheme),
  "parseMathIPython": () => (/* reexport */ parseMathIPython),
  "rulers": () => (/* reexport */ rulers),
  "ySync": () => (/* reexport */ ySync),
  "ySyncAnnotation": () => (/* reexport */ ySyncAnnotation),
  "ySyncFacet": () => (/* reexport */ ySyncFacet),
  "ybinding": () => (/* reexport */ ybinding)
});

// EXTERNAL MODULE: consume shared module (default) @codemirror/commands@^6.2.3 (strict) (fallback: ../node_modules/@codemirror/commands/dist/index.js)
var index_js_ = __webpack_require__(83861);
;// CONCATENATED MODULE: ../packages/codemirror/lib/commands.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

/**
 * CodeMirror commands namespace
 */
var StateCommands;
(function (StateCommands) {
    /**
     * Indent or insert a tab as appropriate.
     */
    function indentMoreOrInsertTab(target) {
        const arg = { state: target.state, dispatch: target.dispatch };
        const from = target.state.selection.main.from;
        const to = target.state.selection.main.to;
        if (from != to) {
            return (0,index_js_.indentMore)(arg);
        }
        const line = target.state.doc.lineAt(from);
        const before = target.state.doc.slice(line.from, from).toString();
        if (/^\s*$/.test(before)) {
            return (0,index_js_.indentMore)(arg);
        }
        else {
            return (0,index_js_.insertTab)(arg);
        }
    }
    StateCommands.indentMoreOrInsertTab = indentMoreOrInsertTab;
})(StateCommands || (StateCommands = {}));

// EXTERNAL MODULE: consume shared module (default) @codemirror/language@^6.0.0 (singleton) (fallback: ../node_modules/@codemirror/language/dist/index.js)
var dist_index_js_ = __webpack_require__(25025);
// EXTERNAL MODULE: consume shared module (default) @codemirror/state@^6.2.0 (singleton) (fallback: ../node_modules/@codemirror/state/dist/index.js)
var state_dist_index_js_ = __webpack_require__(42904);
// EXTERNAL MODULE: consume shared module (default) @codemirror/view@^6.9.6 (singleton) (fallback: ../node_modules/@codemirror/view/dist/index.js)
var view_dist_index_js_ = __webpack_require__(87801);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var coreutils_dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(30205);
// EXTERNAL MODULE: ../node_modules/@codemirror/autocomplete/dist/index.js
var dist = __webpack_require__(56318);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var lib_index_js_ = __webpack_require__(41948);
;// CONCATENATED MODULE: ../packages/codemirror/lib/extensions/customStyle.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */


/**
 * Custom theme configuration
 *
 * The first non-null value takes precedence
 */
const customThemeConfig = state_dist_index_js_.Facet.define({
    combine(configs) {
        return (0,state_dist_index_js_.combineConfig)(configs, {
            fontFamily: null,
            fontSize: null,
            lineHeight: null
        }, {
            fontFamily: (a, b) => a !== null && a !== void 0 ? a : b,
            fontSize: (a, b) => a !== null && a !== void 0 ? a : b,
            lineHeight: (a, b) => a !== null && a !== void 0 ? a : b
        });
    }
});
function setEditorStyle(view) {
    const { fontFamily, fontSize, lineHeight } = view.state.facet(customThemeConfig);
    let style = '';
    if (fontSize) {
        style += `font-size: ${fontSize}px !important;`;
    }
    if (fontFamily) {
        style += `font-family: ${fontFamily} !important;`;
    }
    if (lineHeight) {
        style += `line-height: ${lineHeight.toString()} !important`;
    }
    return { style: style };
}
/**
 * Get the extension to customize an editor theme.
 *
 * @param config Theme customization
 * @returns Editor extension
 */
function customTheme(config) {
    return [
        customThemeConfig.of(config),
        view_dist_index_js_.EditorView.editorAttributes.of(setEditorStyle)
    ];
}

// EXTERNAL MODULE: consume shared module (default) @lezer/common@^1.0.0 (singleton) (fallback: ../node_modules/@lezer/common/dist/index.js)
var common_dist_index_js_ = __webpack_require__(54192);
// EXTERNAL MODULE: consume shared module (default) @lezer/highlight@^1.0.0 (singleton) (fallback: ../node_modules/@lezer/highlight/dist/index.js)
var highlight_dist_index_js_ = __webpack_require__(25460);
;// CONCATENATED MODULE: ../packages/codemirror/lib/extensions/ipython-md.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


// Mathematical expression delimiters
const INLINE_MATH_DOLLAR = 'InlineMathDollar';
const INLINE_MATH_BRACKET = 'InlineMathBracket';
const BLOCK_MATH_DOLLAR = 'BlockMathDollar';
const BLOCK_MATH_BRACKET = 'BlockMathBracket';
/**
 * Lengh of the delimiter for a math expression
 */
const DELIMITER_LENGTH = {
    [INLINE_MATH_DOLLAR]: 1,
    [INLINE_MATH_BRACKET]: 3,
    [BLOCK_MATH_DOLLAR]: 2,
    [BLOCK_MATH_BRACKET]: 3
};
/**
 * Delimiters for math expressions
 */
// Delimiters must be defined as constant because they are used in object match tests
const DELIMITERS = Object.keys(DELIMITER_LENGTH).reduce((agg, name) => {
    agg[name] = { mark: `${name}Mark`, resolve: name };
    return agg;
}, {});
/**
 * Define an IPython mathematical expression parser for Markdown.
 *
 * @param latexParser CodeMirror {@link Parser} for LaTeX mathematical expression
 * @returns Markdown extension
 */
function parseMathIPython(latexParser) {
    const defineNodes = new Array();
    Object.keys(DELIMITER_LENGTH).forEach(name => {
        defineNodes.push({
            name,
            style: highlight_dist_index_js_.tags.emphasis
        }, { name: `${name}Mark`, style: highlight_dist_index_js_.tags.processingInstruction });
    });
    return {
        defineNodes,
        parseInline: [
            {
                name: BLOCK_MATH_DOLLAR,
                parse(cx, next, pos) {
                    if (next != 36 /* '$' */ || cx.char(pos + 1) != 36) {
                        return -1;
                    }
                    return cx.addDelimiter(DELIMITERS[BLOCK_MATH_DOLLAR], pos, pos + DELIMITER_LENGTH[BLOCK_MATH_DOLLAR], true, true);
                }
            },
            {
                name: INLINE_MATH_DOLLAR,
                parse(cx, next, pos) {
                    if (next != 36 /* '$' */ || cx.char(pos + 1) == 36) {
                        return -1;
                    }
                    return cx.addDelimiter(DELIMITERS[INLINE_MATH_DOLLAR], pos, pos + DELIMITER_LENGTH[INLINE_MATH_DOLLAR], true, true);
                }
            },
            // Inline expression wrapped in \\( ... \\)
            {
                name: INLINE_MATH_BRACKET,
                before: 'Escape',
                parse(cx, next, pos) {
                    if (next != 92 /* '\' */ ||
                        cx.char(pos + 1) != 92 ||
                        ![40 /* '(' */, 41 /* ')' */].includes(cx.char(pos + 2))) {
                        return -1;
                    }
                    return cx.addDelimiter(DELIMITERS[INLINE_MATH_BRACKET], pos, pos + DELIMITER_LENGTH[INLINE_MATH_BRACKET], cx.char(pos + 2) == 40, cx.char(pos + 2) == 41);
                }
            },
            // Block expression wrapped in \\[ ... \\]
            {
                name: BLOCK_MATH_BRACKET,
                before: 'Escape',
                parse(cx, next, pos) {
                    if (next != 92 /* '\' */ ||
                        cx.char(pos + 1) != 92 ||
                        ![91 /* '[' */, 93 /* ']' */].includes(cx.char(pos + 2))) {
                        return -1;
                    }
                    return cx.addDelimiter(DELIMITERS[BLOCK_MATH_BRACKET], pos, pos + DELIMITER_LENGTH[BLOCK_MATH_BRACKET], cx.char(pos + 2) == 91, cx.char(pos + 2) == 93);
                }
            }
        ],
        wrap: latexParser
            ? (0,common_dist_index_js_.parseMixed)((node, input) => {
                // Test if the node type is one of the math expression
                const delimiterLength = DELIMITER_LENGTH[node.type.name];
                if (delimiterLength) {
                    return {
                        parser: latexParser,
                        // Remove delimiter from LaTeX parser otherwise it won't be highlighted
                        overlay: [
                            {
                                from: node.from + delimiterLength,
                                to: node.to - delimiterLength
                            }
                        ]
                    };
                }
                return null;
            })
            : undefined
    };
}

;// CONCATENATED MODULE: ../packages/codemirror/lib/extensions/rulers.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */
// Inspired by https://discuss.codemirror.net/t/how-to-implement-ruler/4616/



const RULERS_CLASSNAME = 'cm-rulers';
/**
 * Rulers style
 */
const baseTheme = view_dist_index_js_.EditorView.baseTheme({
    [`.${RULERS_CLASSNAME}`]: { borderRight: '1px dotted gray', opacity: 0.7 }
});
/**
 * Rulers facet
 */
const rulerConfig = state_dist_index_js_.Facet.define({
    // Merge all unique values
    combine(value) {
        const final = value.reduce((agg, arr) => agg.concat(
        // Check value is not in aggregate nor multiple time in the array.
        arr.filter((v, idx) => !agg.includes(v) && idx == arr.lastIndexOf(v))), []);
        return final;
    }
});
/**
 * View plugin displaying the rulers
 */
const rulers_plugin = view_dist_index_js_.ViewPlugin.fromClass(class {
    constructor(view) {
        this.rulersContainer = view.dom.appendChild(document.createElement('div'));
        this.rulersContainer.style.cssText = `
                position: absolute;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                overflow: hidden;
            `;
        const defaultCharacterWidth = view.defaultCharacterWidth;
        const widths = view.state.facet(rulerConfig);
        this.rulers = widths.map(width => {
            const ruler = this.rulersContainer.appendChild(document.createElement('div'));
            ruler.classList.add(RULERS_CLASSNAME);
            ruler.style.cssText = `
                position: absolute;
                left: ${width * defaultCharacterWidth}px;
                height: 100%;
            `;
            // FIXME: This should be equal to the amount of padding on a line.
            // This value should be extracted from CodeMirror rather than hardcoded.
            ruler.style.width = '6px';
            return ruler;
        });
    }
    update(update) {
        const widths = update.view.state.facet(rulerConfig);
        if (update.viewportChanged ||
            !coreutils_dist_index_js_.JSONExt.deepEqual(widths, update.startState.facet(rulerConfig))) {
            const defaultCharacterWidth = update.view.defaultCharacterWidth;
            this.rulers.forEach((ruler, rulerIdx) => {
                ruler.style.left = `${widths[rulerIdx] * defaultCharacterWidth}px`;
            });
        }
    }
    destroy() {
        this.rulers.forEach(ruler => {
            ruler.remove();
        });
        this.rulersContainer.remove();
    }
});
/**
 * Extension for CodeMirror 6 displaying rulers.
 *
 * @param value Rulers position
 * @returns CodeMirror 6 extension
 */
function rulers(value) {
    return [baseTheme, rulerConfig.of(value), rulers_plugin];
}

// EXTERNAL MODULE: consume shared module (default) yjs@^13.5.40 (singleton) (fallback: ../node_modules/yjs/dist/yjs.mjs)
var yjs_mjs_ = __webpack_require__(36783);
;// CONCATENATED MODULE: ../packages/codemirror/lib/extensions/ybinding.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 *
 * Binding for yjs and codemirror
 *
 * It is a simplification of https://github.com/yjs/y-codemirror.next
 * licensed under MIT License by Kevin Jahns
 */



/**
 * Defines a range on text using relative positions that can be transformed back to
 * absolute positions. (https://docs.yjs.dev/api/relative-positions)
 */
class YRange {
    /**
     * @param yanchor
     * @param yhead
     */
    constructor(yanchor, yhead) {
        this.yanchor = yanchor;
        this.yhead = yhead;
    }
    /**
     * Convert the position to JSON
     */
    toJSON() {
        return {
            yanchor: (0,yjs_mjs_.relativePositionToJSON)(this.yanchor),
            yhead: (0,yjs_mjs_.relativePositionToJSON)(this.yhead)
        };
    }
    /**
     * Convert a JSON range to a YRange
     * @param json Range to convert
     * @return The range as YRange
     */
    static fromJSON(json) {
        return new YRange((0,yjs_mjs_.createRelativePositionFromJSON)(json.yanchor), (0,yjs_mjs_.createRelativePositionFromJSON)(json.yhead));
    }
}
/**
 * Yjs binding configuration
 */
class YSyncConfig {
    /**
     * Create a new binding configuration
     *
     * @param ytext Yjs text to synchronize
     */
    constructor(ytext) {
        this.ytext = ytext;
    }
    /**
     * Helper function to transform an absolute index position to a Yjs-based relative position
     * (https://docs.yjs.dev/api/relative-positions).
     *
     * A relative position can be transformed back to an absolute position even after the document has changed. The position is
     * automatically adapted. This does not require any position transformations. Relative positions are computed based on
     * the internal Yjs document model. Peers that share content through Yjs are guaranteed that their positions will always
     * synced up when using relative positions.
     *
     * ```js
     * import { ySyncFacet } from 'y-codemirror'
     *
     * ..
     * const ysync = view.state.facet(ySyncFacet)
     * // transform an absolute index position to a ypos
     * const ypos = ysync.getYPos(3)
     * // transform the ypos back to an absolute position
     * ysync.fromYPos(ypos) // => 3
     * ```
     *
     * It cannot be guaranteed that absolute index positions can be synced up between peers.
     * This might lead to undesired behavior when implementing features that require that all peers see the
     * same marked range (e.g. a comment plugin).
     *
     * @param pos
     * @param assoc
     */
    toYPos(pos, assoc = 0) {
        return (0,yjs_mjs_.createRelativePositionFromTypeIndex)(this.ytext, pos, assoc);
    }
    /**
     * @param rpos
     */
    fromYPos(rpos) {
        const pos = (0,yjs_mjs_.createAbsolutePositionFromRelativePosition)((0,yjs_mjs_.createRelativePositionFromJSON)(rpos), this.ytext.doc);
        if (pos == null || pos.type !== this.ytext) {
            throw new Error('[y-codemirror] The position you want to retrieve was created by a different document');
        }
        return {
            pos: pos.index,
            assoc: pos.assoc
        };
    }
    /**
     * @param range
     * @return
     */
    toYRange(range) {
        const assoc = range.assoc;
        const yanchor = this.toYPos(range.anchor, assoc);
        const yhead = this.toYPos(range.head, assoc);
        return new YRange(yanchor, yhead);
    }
    /**
     * @param yrange
     */
    fromYRange(yrange) {
        const anchor = this.fromYPos(yrange.yanchor);
        const head = this.fromYPos(yrange.yhead);
        if (anchor.pos === head.pos) {
            return state_dist_index_js_.EditorSelection.cursor(head.pos, head.assoc);
        }
        return state_dist_index_js_.EditorSelection.range(anchor.pos, head.pos);
    }
}
/**
 * Yjs binding facet
 */
const ySyncFacet = state_dist_index_js_.Facet.define({
    combine(inputs) {
        return inputs[inputs.length - 1];
    }
});
/**
 * Yjs binding annotation
 *
 * It is used to track the origin of the document changes
 */
const ySyncAnnotation = state_dist_index_js_.Annotation.define();
/**
 * Yjs binding view plugin to synchronize the
 * editor state with the Yjs document.
 */
const ySync = view_dist_index_js_.ViewPlugin.fromClass(class {
    constructor(view) {
        this.conf = view.state.facet(ySyncFacet);
        this._observer = (event, tr) => {
            var _a;
            if (tr.origin !== this.conf) {
                const delta = event.delta;
                const changes = [];
                let pos = 0;
                for (let i = 0; i < delta.length; i++) {
                    const d = delta[i];
                    if (d.insert != null) {
                        changes.push({ from: pos, to: pos, insert: d.insert });
                    }
                    else if (d.delete != null) {
                        changes.push({ from: pos, to: pos + d.delete, insert: '' });
                        pos += d.delete;
                    }
                    else {
                        pos += (_a = d.retain) !== null && _a !== void 0 ? _a : 0;
                    }
                }
                view.dispatch({
                    changes,
                    // Specified the changes origin to not loop when synchronizing
                    annotations: [ySyncAnnotation.of(this.conf)]
                });
            }
        };
        this._ytext = this.conf.ytext;
        this._ytext.observe(this._observer);
    }
    update(update) {
        if (!update.docChanged ||
            (update.transactions.length > 0 &&
                update.transactions[0].annotation(ySyncAnnotation) === this.conf)) {
            return;
        }
        const ytext = this.conf.ytext;
        ytext.doc.transact(() => {
            /**
             * This variable adjusts the fromA position to the current position in the Y.Text type.
             */
            let adj = 0;
            update.changes.iterChanges((fromA, toA, fromB, toB, insert) => {
                const insertText = insert.sliceString(0, insert.length, '\n');
                if (fromA !== toA) {
                    ytext.delete(fromA + adj, toA - fromA);
                }
                if (insertText.length > 0) {
                    ytext.insert(fromA + adj, insertText);
                }
                adj += insertText.length - (toA - fromA);
            });
            // Set the configuration as origin to not loop when synchronizing
        }, this.conf);
    }
    destroy() {
        this._ytext.unobserve(this._observer);
    }
});
/**
 * Extension for CodeMirror 6 binding the Yjs text (source of truth)
 * and the editor state.
 *
 * @param ytext Yjs text to bind
 * @param undoManager Yjs text undo manager
 * @returns CodeMirror 6 extension
 */
function ybinding({ ytext, undoManager }) {
    const ySyncConfig = new YSyncConfig(ytext);
    // We don't need the undo manager extension as in y-codemirror.next
    // because we deal with undo/redo with our own keyboard shortcut mechanism.
    return [
        ySyncFacet.of(ySyncConfig),
        ySync,
        // We need to add a new origin to the undo manager to ensure text updates
        // are tracked.
        undoManager
            ? view_dist_index_js_.ViewPlugin.define(() => {
                undoManager.addTrackedOrigin(ySyncConfig);
                return {
                    destroy: () => {
                        undoManager.removeTrackedOrigin(ySyncConfig);
                    }
                };
            })
            : []
    ];
}

;// CONCATENATED MODULE: ../packages/codemirror/lib/extensions/index.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */





;// CONCATENATED MODULE: ../packages/codemirror/lib/extension.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.










/**
 * The class name added to read only editor widgets.
 */
const READ_ONLY_CLASS = 'jp-mod-readOnly';
/**
 * Editor configuration handler
 *
 * It stores the editor configuration and the editor extensions.
 * It also allows to inject new extensions into an editor.
 */
class ExtensionsHandler {
    constructor({ baseConfiguration, config, defaultExtensions } = {}) {
        this._configChanged = new index_es6_js_.Signal(this);
        this._disposed = new index_es6_js_.Signal(this);
        this._isDisposed = false;
        this._immutables = new Set();
        this._baseConfig = baseConfiguration !== null && baseConfiguration !== void 0 ? baseConfiguration : {};
        this._config = config !== null && config !== void 0 ? config : {};
        this._configurableBuilderMap = new Map(defaultExtensions);
        const configurables = Object.keys(this._config).concat(Object.keys(this._baseConfig));
        this._immutables = new Set([...this._configurableBuilderMap.keys()].filter(key => !configurables.includes(key)));
    }
    /**
     * Signal triggered when the editor configuration changes.
     * It provides the mapping of the new configuration (only those that changed).
     *
     * It should result in a call to `IExtensionsHandler.reconfigureExtensions`.
     */
    get configChanged() {
        return this._configChanged;
    }
    /**
     * A signal emitted when the object is disposed.
     */
    get disposed() {
        return this._disposed;
    }
    /**
     * Tests whether the object is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the object.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._disposed.emit();
        index_es6_js_.Signal.clearData(this);
    }
    /**
     * Get a config option for the editor.
     */
    getOption(option) {
        var _a;
        return (_a = this._config[option]) !== null && _a !== void 0 ? _a : this._baseConfig[option];
    }
    /**
     * Whether the option exists or not.
     */
    hasOption(option) {
        return (Object.keys(this._config).includes(option) ||
            Object.keys(this._baseConfig).includes(option));
    }
    /**
     * Set a config option for the editor.
     *
     * You will need to reconfigure the editor extensions by listening
     * to `IExtensionsHandler.configChanged`.
     */
    setOption(option, value) {
        // Don't bother setting the option if it is already the same.
        if (this._config[option] !== value) {
            this._config[option] = value;
            this._configChanged.emit({ [option]: value });
        }
    }
    /**
     * Set a base config option for the editor.
     *
     * You will need to reconfigure the editor extensions by listening
     * to `IExtensionsHandler.configChanged`.
     */
    setBaseOptions(options) {
        const changed = this._getChangedOptions(options, this._baseConfig);
        if (changed.length > 0) {
            this._baseConfig = options;
            const customizedKeys = Object.keys(this._config);
            const notOverridden = changed.filter(k => !customizedKeys.includes(k));
            if (notOverridden.length > 0) {
                this._configChanged.emit(notOverridden.reduce((agg, key) => {
                    agg[key] = this._baseConfig[key];
                    return agg;
                }, {}));
            }
        }
    }
    /**
     * Set config options for the editor.
     *
     * You will need to reconfigure the editor extensions by listening
     * to `EditorHandler.configChanged`.
     *
     * This method is preferred when setting several options. The
     * options are set within an operation, which only performs
     * the costly update at the end, and not after every option
     * is set.
     */
    setOptions(options) {
        const changed = this._getChangedOptions(options, this._config);
        if (changed.length > 0) {
            this._config = { ...options };
            this._configChanged.emit(changed.reduce((agg, key) => {
                var _a;
                agg[key] = (_a = this._config[key]) !== null && _a !== void 0 ? _a : this._baseConfig[key];
                return agg;
            }, {}));
        }
    }
    /**
     * Reconfigures the extension mapped with key with the provided value.
     *
     * @param view Editor view
     * @param key Parameter unique key
     * @param value Parameter value to be applied
     */
    reconfigureExtension(view, key, value) {
        const effect = this.getEffect(view.state, key, value);
        if (effect) {
            view.dispatch({
                effects: [effect]
            });
        }
    }
    /**
     * Reconfigures all the extensions mapped with the options from the
     * provided partial configuration.
     *
     * @param view Editor view
     * @param configuration Editor configuration
     */
    reconfigureExtensions(view, configuration) {
        const effects = Object.keys(configuration)
            .filter(key => this.has(key))
            .map(key => this.getEffect(view.state, key, configuration[key]));
        view.dispatch({
            effects: effects.filter(effect => effect !== null)
        });
    }
    /**
     * Appends extensions to the top-level configuration of the
     * editor.
     *
     * Injected extension cannot be removed.
     *
     * ### Notes
     * You should prefer registering a IEditorExtensionFactory instead
     * of this feature.
     *
     * @alpha
     * @param view Editor view
     * @param extension Editor extension to inject
     */
    injectExtension(view, extension) {
        view.dispatch({
            effects: state_dist_index_js_.StateEffect.appendConfig.of(extension)
        });
    }
    /**
     * Returns the list of initial extensions of an editor
     * based on the configuration.
     *
     * @returns The initial editor extensions
     */
    getInitialExtensions() {
        const configuration = { ...this._baseConfig, ...this._config };
        const extensions = [...this._immutables]
            .map(key => { var _a; return (_a = this.get(key)) === null || _a === void 0 ? void 0 : _a.instance(undefined); })
            .filter(ext => ext);
        for (const k of Object.keys(configuration)) {
            const builder = this.get(k);
            if (builder) {
                const value = configuration[k];
                extensions.push(builder.instance(value));
            }
        }
        return extensions;
    }
    /**
     * Get a extension builder
     * @param key Extension unique identifier
     * @returns The extension builder
     */
    get(key) {
        return this._configurableBuilderMap.get(key);
    }
    /**
     * Whether the editor has an extension for the identifier.
     *
     * @param key Extension unique identifier
     * @returns Extension existence
     */
    has(key) {
        return this._configurableBuilderMap.has(key);
    }
    getEffect(state, key, value) {
        var _a;
        const builder = this.get(key);
        return (_a = builder === null || builder === void 0 ? void 0 : builder.reconfigure(value)) !== null && _a !== void 0 ? _a : null;
    }
    _getChangedOptions(newConfig, oldConfig) {
        const changed = new Array();
        const newKeys = new Array();
        for (const [key, value] of Object.entries(newConfig)) {
            newKeys.push(key);
            if (oldConfig[key] !== value) {
                changed.push(key);
            }
        }
        // Add removed old keys
        changed.push(...Object.keys(oldConfig).filter(k => !newKeys.includes(k)));
        return changed;
    }
}
/**
 * CodeMirror extensions registry
 */
class EditorExtensionRegistry {
    constructor() {
        this.configurationBuilder = new Map();
        this.configurationSchema = {};
        this.defaultOptions = {};
        this.handlers = new Set();
        this.immutableExtensions = new Set();
        this._baseConfiguration = {};
    }
    /**
     * Base editor configuration
     *
     * This is the default configuration optionally modified by the user;
     * e.g. through user settings.
     */
    get baseConfiguration() {
        return { ...this.defaultOptions, ...this._baseConfiguration };
    }
    set baseConfiguration(v) {
        if (!coreutils_dist_index_js_.JSONExt.deepEqual(v, this._baseConfiguration)) {
            this._baseConfiguration = v;
            for (const handler of this.handlers) {
                handler.setBaseOptions(this.baseConfiguration);
            }
        }
    }
    /**
     * Default editor configuration
     *
     * This is the default configuration as defined when extensions
     * are registered.
     */
    get defaultConfiguration() {
        // Only options with schema should be JSON serializable
        // So we cannot use `JSONExt.deepCopy` on the default options.
        return Object.freeze({ ...this.defaultOptions });
    }
    /**
     * Editor configuration JSON schema
     */
    get settingsSchema() {
        return Object.freeze(coreutils_dist_index_js_.JSONExt.deepCopy(this.configurationSchema));
    }
    /**
     * Add a default editor extension
     *
     * @template T Extension parameter type
     * @param factory Extension factory
     */
    addExtension(factory) {
        var _a;
        if (this.configurationBuilder.has(factory.name)) {
            throw new Error(`Extension named ${factory.name} is already registered.`);
        }
        this.configurationBuilder.set(factory.name, factory);
        if (typeof factory.default != 'undefined') {
            this.defaultOptions[factory.name] = factory.default;
        }
        if (factory.schema) {
            this.configurationSchema[factory.name] = {
                default: (_a = factory.default) !== null && _a !== void 0 ? _a : null,
                ...factory.schema
            };
            this.defaultOptions[factory.name] =
                this.configurationSchema[factory.name].default;
        }
    }
    /**
     * Create a new extensions handler for an editor
     *
     * @param options Extensions options and initial editor configuration
     */
    createNew(options) {
        const configuration = new Array();
        for (const [key, builder] of this.configurationBuilder.entries()) {
            const extension = builder.factory(options);
            if (extension) {
                configuration.push([key, extension]);
            }
        }
        const handler = new ExtensionsHandler({
            baseConfiguration: this.baseConfiguration,
            config: options.config,
            defaultExtensions: configuration
        });
        this.handlers.add(handler);
        handler.disposed.connect(() => {
            this.handlers.delete(handler);
        });
        return handler;
    }
}
/**
 * Editor extension registry namespace
 */
(function (EditorExtensionRegistry) {
    /**
     * Dynamically configurable editor extension.
     */
    class ConfigurableExtension {
        /**
         * Create a dynamic editor extension.
         *
         * @param builder Extension builder
         */
        constructor(builder) {
            this._compartment = new state_dist_index_js_.Compartment();
            this._builder = builder;
        }
        /**
         * Create an editor extension for the provided value.
         *
         * @param value Editor extension parameter value
         * @returns The editor extension
         */
        instance(value) {
            return this._compartment.of(this._builder(value));
        }
        /**
         * Reconfigure an editor extension.
         *
         * @param value Editor extension value
         * @returns Editor state effect
         */
        reconfigure(value) {
            return this._compartment.reconfigure(this._builder(value));
        }
    }
    /**
     * Immutable editor extension class
     */
    class ImmutableExtension {
        /**
         * Create an immutable editor extension.
         *
         * @param extension Extension
         */
        constructor(extension) {
            this._extension = extension;
        }
        /**
         * Create an editor extension.
         *
         * @returns The editor extension
         */
        instance() {
            return this._extension;
        }
        /**
         * Reconfigure an editor extension.
         *
         * This is a no-op
         */
        reconfigure() {
            // This is a no-op
            return null;
        }
    }
    /**
     * Creates a dynamically configurable editor extension.
     *
     * @param builder Extension builder
     * @return The extension
     */
    function createConfigurableExtension(builder) {
        return new ConfigurableExtension(builder);
    }
    EditorExtensionRegistry.createConfigurableExtension = createConfigurableExtension;
    /**
     * Creates a configurable extension returning
     * one of two extensions depending on a boolean value.
     *
     * @param truthy Extension to apply when the parameter is true
     * @param falsy Extension to apply when the parameter is false
     * @return The extension
     */
    function createConditionalExtension(truthy, falsy = []) {
        return new ConfigurableExtension(value => value ? truthy : falsy);
    }
    EditorExtensionRegistry.createConditionalExtension = createConditionalExtension;
    /**
     * Creates an immutable extension.
     *
     * @param extension Immutable extension
     * @return The extension
     */
    function createImmutableExtension(extension) {
        return new ImmutableExtension(extension);
    }
    EditorExtensionRegistry.createImmutableExtension = createImmutableExtension;
    /**
     * Get the default editor extensions.
     *
     * @returns CodeMirror 6 extension factories
     */
    function getDefaultExtensions(options = {}) {
        const { themes, translator } = options;
        const trans = (translator !== null && translator !== void 0 ? translator : lib_index_js_.nullTranslator).load('jupyterlab');
        const extensions = [
            Object.freeze({
                name: 'autoClosingBrackets',
                default: false,
                factory: () => createConditionalExtension((0,dist/* closeBrackets */.vQ)()),
                schema: {
                    type: 'boolean',
                    title: trans.__('Auto Closing Brackets')
                }
            }),
            Object.freeze({
                name: 'codeFolding',
                default: false,
                factory: () => createConditionalExtension((0,dist_index_js_.foldGutter)()),
                schema: {
                    type: 'boolean',
                    title: trans.__('Code Folding')
                }
            }),
            Object.freeze({
                name: 'cursorBlinkRate',
                default: 1200,
                factory: () => createConfigurableExtension((value) => (0,view_dist_index_js_.drawSelection)({ cursorBlinkRate: value })),
                schema: {
                    type: 'number',
                    title: trans.__('Cursor blinking rate'),
                    description: trans.__('Half-period in milliseconds used for cursor blinking. The default blink rate is 1200ms. By setting this to zero, blinking can be disabled.')
                }
            }),
            Object.freeze({
                name: 'highlightActiveLine',
                default: false,
                factory: () => createConditionalExtension((0,view_dist_index_js_.highlightActiveLine)()),
                schema: {
                    type: 'boolean',
                    title: trans.__('Highlight the active line')
                }
            }),
            Object.freeze({
                name: 'highlightTrailingWhitespace',
                default: false,
                factory: () => createConditionalExtension((0,view_dist_index_js_.highlightTrailingWhitespace)()),
                schema: {
                    type: 'boolean',
                    title: trans.__('Highlight trailing white spaces')
                }
            }),
            Object.freeze({
                name: 'highlightWhitespace',
                default: false,
                factory: () => createConditionalExtension((0,view_dist_index_js_.highlightWhitespace)()),
                schema: {
                    type: 'boolean',
                    title: trans.__('Highlight white spaces')
                }
            }),
            Object.freeze({
                name: 'indentUnit',
                default: '4',
                factory: () => createConfigurableExtension((value) => value == 'Tab'
                    ? dist_index_js_.indentUnit.of('\t')
                    : dist_index_js_.indentUnit.of(' '.repeat(parseInt(value, 10)))),
                schema: {
                    type: 'string',
                    title: trans.__('Indentation unit'),
                    description: trans.__('The indentation is a `Tab` or the number of spaces. This defaults to 4 spaces.'),
                    enum: ['Tab', '1', '2', '4', '8']
                }
            }),
            // Default keyboard shortcuts
            // TODO at some point we may want to get this configurable
            Object.freeze({
                name: 'keymap',
                default: [
                    ...index_js_.defaultKeymap,
                    {
                        key: 'Tab',
                        run: StateCommands.indentMoreOrInsertTab,
                        shift: index_js_.indentLess
                    }
                ],
                factory: () => createConfigurableExtension(value => view_dist_index_js_.keymap.of(value))
            }),
            Object.freeze({
                name: 'lineNumbers',
                default: true,
                factory: () => createConditionalExtension((0,view_dist_index_js_.lineNumbers)()),
                schema: {
                    type: 'boolean',
                    title: trans.__('Line Numbers')
                }
            }),
            Object.freeze({
                name: 'lineWrap',
                factory: () => createConditionalExtension(view_dist_index_js_.EditorView.lineWrapping),
                default: true,
                schema: {
                    type: 'boolean',
                    title: trans.__('Line Wrap')
                }
            }),
            Object.freeze({
                name: 'matchBrackets',
                default: true,
                factory: () => createConditionalExtension((0,dist_index_js_.bracketMatching)()),
                schema: {
                    type: 'boolean',
                    title: trans.__('Match Brackets')
                }
            }),
            Object.freeze({
                name: 'rectangularSelection',
                default: true,
                factory: () => createConditionalExtension([
                    (0,view_dist_index_js_.rectangularSelection)(),
                    (0,view_dist_index_js_.crosshairCursor)()
                ]),
                schema: {
                    type: 'boolean',
                    title: trans.__('Rectangular selection'),
                    description: trans.__('Rectangular (block) selection can be created by dragging the mouse pointer while holding the left mouse button and the Alt key. When the Alt key is pressed, a crosshair cursor will appear, indicating that the rectangular selection mode is active.')
                }
            }),
            Object.freeze({
                name: 'readOnly',
                default: false,
                factory: () => createConfigurableExtension((value) => [
                    state_dist_index_js_.EditorState.readOnly.of(value),
                    value
                        ? view_dist_index_js_.EditorView.editorAttributes.of({ class: READ_ONLY_CLASS })
                        : []
                ])
            }),
            Object.freeze({
                name: 'rulers',
                default: [],
                factory: () => createConfigurableExtension((value) => value.length > 0 ? rulers(value) : []),
                schema: {
                    type: 'array',
                    title: trans.__('Rulers'),
                    items: {
                        type: 'number',
                        minimum: 0
                    }
                }
            }),
            Object.freeze({
                name: 'scrollPastEnd',
                default: false,
                factory: (options) => options.inline ? null : createConditionalExtension((0,view_dist_index_js_.scrollPastEnd)())
            }),
            Object.freeze({
                name: 'smartIndent',
                default: true,
                factory: () => createConditionalExtension((0,dist_index_js_.indentOnInput)()),
                schema: {
                    type: 'boolean',
                    title: trans.__('Smart Indentation')
                }
            }),
            Object.freeze({
                name: 'tabSize',
                default: 4,
                factory: () => createConfigurableExtension((value) => state_dist_index_js_.EditorState.tabSize.of(value)),
                schema: {
                    type: 'number',
                    title: trans.__('Tab size')
                }
            }),
            Object.freeze({
                name: 'tooltips',
                factory: () => 
                // we need `absolute` due to use of `contain: layout` in lumino;
                // we attach to body to ensure cursor collaboration tooltip is
                // visible in first line of the editor.
                createImmutableExtension((0,view_dist_index_js_.tooltips)({
                    position: 'absolute',
                    parent: document.body
                }))
            }),
            Object.freeze({
                name: 'allowMultipleSelections',
                default: true,
                factory: () => createConfigurableExtension((value) => state_dist_index_js_.EditorState.allowMultipleSelections.of(value)),
                schema: {
                    type: 'boolean',
                    title: trans.__('Multiple selections')
                }
            }),
            Object.freeze({
                name: 'customStyles',
                factory: () => createConfigurableExtension(config => customTheme(config)),
                default: {
                    fontFamily: null,
                    fontSize: null,
                    lineHeight: null
                },
                schema: {
                    title: trans.__('Custom editor styles'),
                    type: 'object',
                    properties: {
                        fontFamily: {
                            type: ['string', 'null'],
                            title: trans.__('Font Family')
                        },
                        fontSize: {
                            type: ['number', 'null'],
                            minimum: 1,
                            maximum: 100,
                            title: trans.__('Font Size')
                        },
                        lineHeight: {
                            type: ['number', 'null'],
                            title: trans.__('Line Height')
                        }
                    },
                    additionalProperties: false
                }
            })
        ];
        if (themes) {
            extensions.push(Object.freeze({
                name: 'theme',
                default: 'jupyter',
                factory: () => createConfigurableExtension(value => themes.getTheme(value)),
                schema: {
                    type: 'string',
                    title: trans.__('Theme'),
                    description: trans.__('CodeMirror theme')
                }
            }));
        }
        if (translator) {
            extensions.push(Object.freeze({
                name: 'translation',
                // The list of internal strings is available at https://codemirror.net/examples/translate/
                default: {
                    // @codemirror/view
                    'Control character': trans.__('Control character'),
                    // @codemirror/commands
                    'Selection deleted': trans.__('Selection deleted'),
                    // @codemirror/language
                    'Folded lines': trans.__('Folded lines'),
                    'Unfolded lines': trans.__('Unfolded lines'),
                    to: trans.__('to'),
                    'folded code': trans.__('folded code'),
                    unfold: trans.__('unfold'),
                    'Fold line': trans.__('Fold line'),
                    'Unfold line': trans.__('Unfold line'),
                    // @codemirror/search
                    'Go to line': trans.__('Go to line'),
                    go: trans.__('go'),
                    Find: trans.__('Find'),
                    Replace: trans.__('Replace'),
                    next: trans.__('next'),
                    previous: trans.__('previous'),
                    all: trans.__('all'),
                    'match case': trans.__('match case'),
                    replace: trans.__('replace'),
                    'replace all': trans.__('replace all'),
                    close: trans.__('close'),
                    'current match': trans.__('current match'),
                    'replaced $ matches': trans.__('replaced $ matches'),
                    'replaced match on line $': trans.__('replaced match on line $'),
                    'on line': trans.__('on line'),
                    // @codemirror/autocomplete
                    Completions: trans.__('Completions'),
                    // @codemirror/lint
                    Diagnostics: trans.__('Diagnostics'),
                    'No diagnostics': trans.__('No diagnostics')
                },
                factory: () => createConfigurableExtension(value => state_dist_index_js_.EditorState.phrases.of(value))
            }));
        }
        return extensions;
    }
    EditorExtensionRegistry.getDefaultExtensions = getDefaultExtensions;
})(EditorExtensionRegistry || (EditorExtensionRegistry = {}));

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/codeeditor@~4.1.0-alpha.2 (singleton) (fallback: ../packages/codeeditor/lib/index.js)
var codeeditor_lib_index_js_ = __webpack_require__(40200);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var coreutils_lib_index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: ../node_modules/@lezer/generator/dist/index.js
var generator_dist = __webpack_require__(50306);
;// CONCATENATED MODULE: ../packages/codemirror/lib/theme.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




const jupyterEditorTheme = view_dist_index_js_.EditorView.theme({
    /**
     * CodeMirror themes are handling the background/color in this way. This works
     * fine for CodeMirror editors outside the notebook, but the notebook styles
     * these things differently.
     */
    '&': {
        background: 'var(--jp-layout-color0)',
        color: 'var(--jp-content-font-color1)'
    },
    /* In the notebook, we want this styling to be handled by its container */
    '.jp-CodeConsole &, .jp-Notebook &': {
        background: 'transparent'
    },
    '.cm-content': {
        caretColor: 'var(--jp-editor-cursor-color)'
    },
    /* Inherit font family from .cm-editor */
    '.cm-scroller': {
        fontFamily: 'inherit'
    },
    '.cm-cursor, .cm-dropCursor': {
        borderLeft: 'var(--jp-code-cursor-width0) solid var(--jp-editor-cursor-color)'
    },
    '.cm-selectionBackground, .cm-content ::selection': {
        backgroundColor: 'var(--jp-editor-selected-background)'
    },
    '&.cm-focused > .cm-scroller > .cm-selectionLayer .cm-selectionBackground': {
        backgroundColor: 'var(--jp-editor-selected-focused-background)'
    },
    '.cm-gutters': {
        borderRight: '1px solid var(--jp-border-color2)',
        backgroundColor: 'var(--jp-layout-color2)'
    },
    '.cm-gutter': {
        backgroundColor: 'var(--jp-layout-color2)'
    },
    '.cm-activeLine': {
        backgroundColor: 'color-mix(in srgb, var(--jp-layout-color3) 25%, transparent)'
    },
    '.cm-lineNumbers': {
        color: 'var(--jp-ui-font-color2)'
    },
    '.cm-searchMatch': {
        backgroundColor: 'var(--jp-search-unselected-match-background-color)',
        color: 'var(--jp-search-unselected-match-color)'
    },
    '.cm-searchMatch.cm-searchMatch-selected': {
        backgroundColor: 'var(--jp-search-selected-match-background-color) !important',
        color: 'var(--jp-search-selected-match-color) !important'
    },
    '.cm-tooltip': {
        backgroundColor: 'var(--jp-layout-color1)'
    }
});
// The list of available tags for syntax highlighting is available at
// https://lezer.codemirror.net/docs/ref/#highlight.tags
const jupyterHighlightStyle = dist_index_js_.HighlightStyle.define([
    // Order matters - a rule will override the previous ones; important for example for in headings styles.
    { tag: highlight_dist_index_js_.tags.meta, color: 'var(--jp-mirror-editor-meta-color)' },
    { tag: highlight_dist_index_js_.tags.heading, color: 'var(--jp-mirror-editor-header-color)' },
    {
        tag: [highlight_dist_index_js_.tags.heading1, highlight_dist_index_js_.tags.heading2, highlight_dist_index_js_.tags.heading3, highlight_dist_index_js_.tags.heading4],
        color: 'var(--jp-mirror-editor-header-color)',
        fontWeight: 'bold'
    },
    {
        tag: highlight_dist_index_js_.tags.keyword,
        color: 'var(--jp-mirror-editor-keyword-color)',
        fontWeight: 'bold'
    },
    { tag: highlight_dist_index_js_.tags.atom, color: 'var(--jp-mirror-editor-atom-color)' },
    { tag: highlight_dist_index_js_.tags.number, color: 'var(--jp-mirror-editor-number-color)' },
    {
        tag: [highlight_dist_index_js_.tags.definition(highlight_dist_index_js_.tags.name), highlight_dist_index_js_.tags["function"](highlight_dist_index_js_.tags.definition(highlight_dist_index_js_.tags.variableName))],
        color: 'var(--jp-mirror-editor-def-color)'
    },
    {
        tag: highlight_dist_index_js_.tags.standard(highlight_dist_index_js_.tags.variableName),
        color: 'var(--jp-mirror-editor-builtin-color)'
    },
    {
        tag: [highlight_dist_index_js_.tags.special(highlight_dist_index_js_.tags.variableName), highlight_dist_index_js_.tags.self],
        color: 'var(--jp-mirror-editor-variable-2-color)'
    },
    { tag: highlight_dist_index_js_.tags.punctuation, color: 'var(--jp-mirror-editor-punctuation-color)' },
    { tag: highlight_dist_index_js_.tags.propertyName, color: 'var(--jp-mirror-editor-property-color)' },
    {
        tag: highlight_dist_index_js_.tags.operator,
        color: 'var(--jp-mirror-editor-operator-color)',
        fontWeight: 'bold'
    },
    {
        tag: highlight_dist_index_js_.tags.comment,
        color: 'var(--jp-mirror-editor-comment-color)',
        fontStyle: 'italic'
    },
    { tag: highlight_dist_index_js_.tags.string, color: 'var(--jp-mirror-editor-string-color)' },
    {
        tag: [highlight_dist_index_js_.tags.labelName, highlight_dist_index_js_.tags.monospace, highlight_dist_index_js_.tags.special(highlight_dist_index_js_.tags.string)],
        color: 'var(--jp-mirror-editor-string-2-color)'
    },
    { tag: highlight_dist_index_js_.tags.bracket, color: 'var(--jp-mirror-editor-bracket-color)' },
    { tag: highlight_dist_index_js_.tags.tagName, color: 'var(--jp-mirror-editor-tag-color)' },
    { tag: highlight_dist_index_js_.tags.attributeName, color: 'var(--jp-mirror-editor-attribute-color)' },
    { tag: highlight_dist_index_js_.tags.quote, color: 'var(--jp-mirror-editor-quote-color)' },
    {
        tag: highlight_dist_index_js_.tags.link,
        color: 'var(--jp-mirror-editor-link-color)',
        textDecoration: 'underline'
    },
    { tag: [highlight_dist_index_js_.tags.separator, highlight_dist_index_js_.tags.derefOperator, highlight_dist_index_js_.tags.paren], color: '' },
    { tag: highlight_dist_index_js_.tags.strong, fontWeight: 'bold' },
    { tag: highlight_dist_index_js_.tags.emphasis, fontStyle: 'italic' },
    { tag: highlight_dist_index_js_.tags.strikethrough, textDecoration: 'line-through' },
    {
        tag: highlight_dist_index_js_.tags.bool,
        color: 'var(--jp-mirror-editor-keyword-color)',
        fontWeight: 'bold'
    }
]);
/**
 * JupyterLab CodeMirror 6 theme
 */
const jupyterTheme = [
    jupyterEditorTheme,
    (0,dist_index_js_.syntaxHighlighting)(jupyterHighlightStyle)
];
/**
 * CodeMirror 6 theme registry
 */
class EditorThemeRegistry {
    constructor() {
        /**
         * CodeMirror 6 themes
         */
        this._themeMap = new Map([
            ['jupyter', Object.freeze({ name: 'jupyter', theme: jupyterTheme })]
        ]);
    }
    /**
     * Get all themes
     */
    get themes() {
        return Array.from(this._themeMap.values());
    }
    /**
     * Get the default CodeMirror 6 theme for JupyterLab
     *
     * @returns Default theme
     */
    defaultTheme() {
        return this._themeMap.get('jupyter').theme;
    }
    /**
     * Register a new theme.
     *
     * @param theme Codemirror 6 theme
     */
    addTheme(theme) {
        if (this._themeMap.has(theme.name)) {
            throw new Error(`A theme named '${theme.name}' is already registered.`);
        }
        this._themeMap.set(theme.name, { displayName: theme.name, ...theme });
    }
    /**
     * Get a theme.
     *
     * #### Notes
     * It falls back to the default theme
     *
     * @param name Theme name
     * @returns Theme extension
     */
    getTheme(name) {
        var _a;
        const ext = (_a = this._themeMap.get(name)) === null || _a === void 0 ? void 0 : _a.theme;
        return ext !== null && ext !== void 0 ? ext : this.defaultTheme();
    }
}
/**
 * EditorThemeRegistry namespace
 */
(function (EditorThemeRegistry) {
    /**
     * Get the default editor themes.
     *
     * @param translator Application translator
     * @returns Default CodeMirror 6 themes
     */
    function getDefaultThemes(translator) {
        const trans = (translator !== null && translator !== void 0 ? translator : lib_index_js_.nullTranslator).load('jupyterlab');
        return [
            Object.freeze({
                name: 'codemirror',
                displayName: trans.__('codemirror'),
                theme: [
                    view_dist_index_js_.EditorView.baseTheme({}),
                    (0,dist_index_js_.syntaxHighlighting)(dist_index_js_.defaultHighlightStyle)
                ]
            })
        ];
    }
    EditorThemeRegistry.getDefaultThemes = getDefaultThemes;
})(EditorThemeRegistry || (EditorThemeRegistry = {}));

;// CONCATENATED MODULE: ../packages/codemirror/lib/language.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/**
 * CodeMirror language registry
 */
class EditorLanguageRegistry {
    constructor() {
        this._modeList = [];
        // Add default language text/plain -> No expressions to parse
        this.addLanguage({
            name: 'none',
            mime: 'text/plain',
            support: new dist_index_js_.LanguageSupport(
            // Create a dummy parser that as no expression to parse
            dist_index_js_.LRLanguage.define({ parser: (0,generator_dist/* buildParser */.pV)('@top Program { }') }))
        });
    }
    /**
     * Register a new language for CodeMirror
     *
     * @param language Language to register
     */
    addLanguage(language) {
        var _a;
        const info = (_a = this.findByName(language.name)) !== null && _a !== void 0 ? _a : this.findByMIME(language.mime, true);
        if (info) {
            throw new Error(`${language.mime} already registered`);
        }
        this._modeList.push(this.makeSpec(language));
    }
    /**
     * Ensure a codemirror mode is available by name or Codemirror spec.
     *
     * @param language - The mode to ensure.  If it is a string, uses [findBest]
     *   to get the appropriate spec.
     *
     * @returns A promise that resolves when the mode is available.
     */
    async getLanguage(language) {
        const spec = this.findBest(language);
        if (spec && !spec.support) {
            spec.support = await spec.load();
        }
        return spec;
    }
    /**
     * Get the raw list of available modes specs.
     *
     * @returns The available modes
     */
    getLanguages() {
        return [...this._modeList];
    }
    /**
     * Find a codemirror mode by MIME.
     *
     * @param mime Mime type to look for
     * @param strict Whether xml and json should be assimilated to the generic mimetype
     * @returns The mode or null
     */
    findByMIME(mime, strict = false) {
        if (Array.isArray(mime)) {
            for (let i = 0; i < mime.length; i++) {
                const spec = this.findByMIME(mime[i]);
                if (spec)
                    return spec;
            }
            return null;
        }
        mime = mime.toLowerCase();
        for (let i = 0; i < this._modeList.length; i++) {
            let info = this._modeList[i];
            if (Array.isArray(info.mime)) {
                for (let j = 0; j < info.mime.length; j++) {
                    if (info.mime[j] == mime) {
                        return info;
                    }
                }
            }
            else if (info.mime == mime) {
                return info;
            }
        }
        if (!strict) {
            if (/\+xml$/.test(mime))
                return this.findByMIME('application/xml');
            if (/\+json$/.test(mime))
                return this.findByMIME('application/json');
        }
        return null;
    }
    /**
     * Find a codemirror mode by name.
     *
     * @param name The mode name
     * @returns The mode or null
     */
    findByName(name) {
        name = name.toLowerCase();
        for (let i = 0; i < this._modeList.length; i++) {
            let info = this._modeList[i];
            if (info.name.toLowerCase() == name)
                return info;
            if (info.alias) {
                for (let j = 0; j < info.alias.length; j++) {
                    if (info.alias[j].toLowerCase() == name) {
                        return info;
                    }
                }
            }
        }
        return null;
    }
    /**
     * Find a codemirror mode by extension.
     *
     * @param ext The extension name
     * @returns The mode or null
     */
    findByExtension(ext) {
        if (Array.isArray(ext)) {
            for (let i = 0; i < ext.length; i++) {
                const spec = this.findByExtension(ext[i]);
                if (spec)
                    return spec;
            }
            return null;
        }
        ext = ext.toLowerCase();
        for (let i = 0; i < this._modeList.length; i++) {
            let info = this._modeList[i];
            for (let j = 0; j < info.extensions.length; j++) {
                if (info.extensions[j].toLowerCase() == ext) {
                    return info;
                }
            }
        }
        return null;
    }
    /**
     * Find a codemirror mode by filename.
     *
     * @param name File name
     * @returns The mode or null
     */
    findByFileName(name) {
        const basename = coreutils_lib_index_js_.PathExt.basename(name);
        for (let i = 0; i < this._modeList.length; i++) {
            let info = this._modeList[i];
            if (info.filename && info.filename.test(basename)) {
                return info;
            }
        }
        let dot = basename.lastIndexOf('.');
        let ext = dot > -1 && basename.substring(dot + 1, basename.length);
        if (ext) {
            return this.findByExtension(ext);
        }
        return null;
    }
    /**
     * Find a codemirror mode by name or CodeMirror spec.
     *
     * @param language The CodeMirror mode
     * @param fallback Whether to fallback to default mimetype spec or not
     * @returns The mode or null
     */
    findBest(language, fallback = true) {
        var _a, _b, _c, _d;
        const modename = typeof language === 'string' ? language : language.name;
        const mimetype = typeof language !== 'string' ? language.mime : modename;
        const ext = typeof language !== 'string' ? (_a = language.extensions) !== null && _a !== void 0 ? _a : [] : [];
        return ((_d = (_c = (_b = (modename ? this.findByName(modename) : null)) !== null && _b !== void 0 ? _b : (mimetype ? this.findByMIME(mimetype) : null)) !== null && _c !== void 0 ? _c : this.findByExtension(ext)) !== null && _d !== void 0 ? _d : (fallback
            ? this.findByMIME(codeeditor_lib_index_js_.IEditorMimeTypeService.defaultMimeType)
            : null));
    }
    /**
     * Parse and style a string.
     *
     * @param code Code to highlight
     * @param language Code language
     * @param el HTML element into which the highlighted code will be inserted
     */
    async highlight(code, language, el) {
        var _a;
        if (language) {
            await this.getLanguage(language);
        }
        const language_ = (_a = language === null || language === void 0 ? void 0 : language.support) === null || _a === void 0 ? void 0 : _a.language;
        if (!language_) {
            el.appendChild(document.createTextNode(code));
            return;
        }
        const tree = language_.parser.parse(code);
        // position state required because unstyled tokens are not emitted
        // in highlightTree
        let pos = 0;
        (0,highlight_dist_index_js_.highlightTree)(tree, jupyterHighlightStyle, (from, to, classes) => {
            if (from > pos) {
                // No style applied to the token between pos and from
                el.appendChild(document.createTextNode(code.slice(pos, from)));
            }
            const sp = el.appendChild(document.createElement('span'));
            sp.className = classes;
            sp.appendChild(document.createTextNode(code.slice(from, to)));
            pos = to;
        });
        if (pos < tree.length - 1) {
            // No style applied on the trailing text
            el.appendChild(document.createTextNode(code.slice(pos, tree.length)));
        }
    }
    // Code mirror uses two similar structures, a plain object with optional fields,
    // and a class with the same fields but all mandatory. Maybe adopting the same
    // pattern would be less confusing (although far more verbose)
    makeSpec(spec) {
        let res = dist_index_js_.LanguageDescription.of(spec);
        // CodeMirror does not store/use mime type of a language
        res.mime = spec.mime;
        res.displayName = spec.displayName;
        return res;
    }
}
/**
 * EditorLanguageRegistry namespace
 */
(function (EditorLanguageRegistry) {
    /**
     * Convert an CodeMirror 5 language parser to CodeMirror 6
     *
     * @param parser Legacy parser
     * @returns Language object
     */
    function legacy(parser) {
        return new dist_index_js_.LanguageSupport(dist_index_js_.StreamLanguage.define(parser));
    }
    EditorLanguageRegistry.legacy = legacy;
    /**
     * Create a dialect of SQL
     *
     * @param dialectName SQL dialect
     * @returns Language object
     */
    async function sql(dialectName) {
        const m = await __webpack_require__.e(/* import() */ 5828).then(__webpack_require__.bind(__webpack_require__, 25828));
        return m.sql({ dialect: m[dialectName] });
    }
    /**
     * Get the default editor languages
     *
     * @param translator Application translator
     * @returns Default CodeMirror 6 languages
     */
    function getDefaultLanguages(translator) {
        const trans = (translator !== null && translator !== void 0 ? translator : lib_index_js_.nullTranslator).load('jupyterlab');
        return [
            {
                name: 'C',
                displayName: trans.__('C'),
                mime: 'text/x-csrc',
                extensions: ['c', 'h', 'ino'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 8578).then(__webpack_require__.bind(__webpack_require__, 8578));
                    return m.cpp();
                }
            },
            {
                name: 'C++',
                displayName: trans.__('C++'),
                mime: 'text/x-c++src',
                extensions: ['cpp', 'c++', 'cc', 'cxx', 'hpp', 'h++', 'hh', 'hxx'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 8578).then(__webpack_require__.bind(__webpack_require__, 8578));
                    return m.cpp();
                }
            },
            {
                name: 'CQL',
                displayName: trans.__('CQL'),
                mime: 'text/x-cassandra',
                extensions: ['cql'],
                load() {
                    return sql('Cassandra');
                }
            },
            {
                name: 'CSS',
                displayName: trans.__('CSS'),
                mime: 'text/css',
                extensions: ['css'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 4205).then(__webpack_require__.bind(__webpack_require__, 64205));
                    return m.css();
                }
            },
            {
                name: 'HTML',
                displayName: trans.__('HTML'),
                alias: ['xhtml'],
                mime: 'text/html',
                extensions: ['html', 'htm', 'handlebars', 'hbs'],
                async load() {
                    const m = await Promise.all(/* import() */[__webpack_require__.e(2979), __webpack_require__.e(4205), __webpack_require__.e(4785)]).then(__webpack_require__.bind(__webpack_require__, 4785));
                    return m.html();
                }
            },
            {
                name: 'Java',
                displayName: trans.__('Java'),
                mime: 'text/x-java',
                extensions: ['java'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 162).then(__webpack_require__.bind(__webpack_require__, 20162));
                    return m.java();
                }
            },
            {
                name: 'Javascript',
                displayName: trans.__('Javascript'),
                alias: ['ecmascript', 'js', 'node'],
                mime: [
                    'text/javascript',
                    'text/ecmascript',
                    'application/javascript',
                    'application/x-javascript',
                    'application/ecmascript'
                ],
                extensions: ['js', 'mjs', 'cjs'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 2979).then(__webpack_require__.bind(__webpack_require__, 52979));
                    return m.javascript();
                }
            },
            {
                name: 'JSON',
                displayName: trans.__('JSON'),
                alias: ['json5'],
                mime: ['application/json', 'application/x-json'],
                extensions: ['json', 'map'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 7439).then(__webpack_require__.bind(__webpack_require__, 57439));
                    return m.json();
                }
            },
            {
                name: 'JSX',
                displayName: trans.__('JSX'),
                mime: 'text/jsx',
                extensions: ['jsx'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 2979).then(__webpack_require__.bind(__webpack_require__, 52979));
                    return m.javascript({ jsx: true });
                }
            },
            {
                name: 'MariaDB SQL',
                displayName: trans.__('MariaDB SQL'),
                mime: 'text/x-mariadb',
                load() {
                    return sql('MariaSQL');
                }
            },
            {
                name: 'Markdown',
                displayName: trans.__('Markdown'),
                mime: 'text/x-markdown',
                extensions: ['md', 'markdown', 'mkd'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 252).then(__webpack_require__.t.bind(__webpack_require__, 252, 23));
                    return m.markdown({ codeLanguages: this._modeList });
                }
            },
            {
                name: 'MS SQL',
                displayName: trans.__('MS SQL'),
                mime: 'text/x-mssql',
                load() {
                    return sql('MSSQL');
                }
            },
            {
                name: 'MySQL',
                displayName: trans.__('MySQL'),
                mime: 'text/x-mysql',
                load() {
                    return sql('MySQL');
                }
            },
            {
                name: 'PHP',
                displayName: trans.__('PHP'),
                mime: [
                    'text/x-php',
                    'application/x-httpd-php',
                    'application/x-httpd-php-open'
                ],
                extensions: ['php', 'php3', 'php4', 'php5', 'php7', 'phtml'],
                async load() {
                    const m = await Promise.all(/* import() */[__webpack_require__.e(2979), __webpack_require__.e(4205), __webpack_require__.e(4785), __webpack_require__.e(8010)]).then(__webpack_require__.bind(__webpack_require__, 78010));
                    return m.php();
                }
            },
            {
                name: 'PLSQL',
                displayName: trans.__('PLSQL'),
                mime: 'text/x-plsql',
                extensions: ['pls'],
                load() {
                    return sql('PLSQL');
                }
            },
            {
                name: 'PostgreSQL',
                displayName: trans.__('PostgreSQL'),
                mime: 'text/x-pgsql',
                load() {
                    return sql('PostgreSQL');
                }
            },
            {
                name: 'Python',
                displayName: trans.__('Python'),
                mime: 'text/x-python',
                extensions: ['BUILD', 'bzl', 'py', 'pyw'],
                filename: /^(BUCK|BUILD)$/,
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 8136).then(__webpack_require__.bind(__webpack_require__, 8136));
                    return m.python();
                }
            },
            {
                name: 'ipython',
                displayName: trans.__('ipython'),
                mime: 'text/x-ipython',
                async load() {
                    // FIXME Restore '?' operator - using the default python LanguageSupport allows
                    // to activate feature such as code folding.
                    // return Promise.resolve(legacy(mkPython({ singleOperators: /\?/ })));
                    const m = await __webpack_require__.e(/* import() */ 8136).then(__webpack_require__.bind(__webpack_require__, 8136));
                    return m.python();
                }
            },
            {
                name: 'Rust',
                displayName: trans.__('Rust'),
                mime: 'text/x-rustsrc',
                extensions: ['rs'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 2251).then(__webpack_require__.bind(__webpack_require__, 85765));
                    return m.rust();
                }
            },
            {
                name: 'SQL',
                displayName: trans.__('SQL'),
                mime: ['application/sql', 'text/x-sql'],
                extensions: ['sql'],
                load() {
                    return sql('StandardSQL');
                }
            },
            {
                name: 'SQLite',
                displayName: trans.__('SQLite'),
                mime: 'text/x-sqlite',
                load() {
                    return sql('SQLite');
                }
            },
            {
                name: 'TSX',
                displayName: trans.__('TSX'),
                alias: ['TypeScript-JSX'],
                mime: 'text/typescript-jsx',
                extensions: ['tsx'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 2979).then(__webpack_require__.bind(__webpack_require__, 52979));
                    return m.javascript({ jsx: true, typescript: true });
                }
            },
            {
                name: 'TypeScript',
                displayName: trans.__('TypeScript'),
                alias: ['ts'],
                mime: 'application/typescript',
                extensions: ['ts'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 2979).then(__webpack_require__.bind(__webpack_require__, 52979));
                    return m.javascript({ typescript: true });
                }
            },
            {
                name: 'WebAssembly',
                displayName: trans.__('WebAssembly'),
                mime: 'text/webassembly',
                extensions: ['wat', 'wast'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 4810).then(__webpack_require__.bind(__webpack_require__, 14810));
                    return m.wast();
                }
            },
            {
                name: 'XML',
                displayName: trans.__('XML'),
                alias: ['rss', 'wsdl', 'xsd'],
                mime: ['application/xml', 'text/xml'],
                extensions: ['xml', 'xsl', 'xsd', 'svg'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 5016).then(__webpack_require__.bind(__webpack_require__, 65016));
                    return m.xml();
                }
            },
            // Legacy modes ported from CodeMirror 5
            {
                name: 'APL',
                displayName: trans.__('APL'),
                mime: 'text/apl',
                extensions: ['dyalog', 'apl'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 563).then(__webpack_require__.bind(__webpack_require__, 10563));
                    return legacy(m.apl);
                }
            },
            {
                name: 'PGP',
                displayName: trans.__('PGP'),
                alias: ['asciiarmor'],
                mime: [
                    'application/pgp',
                    'application/pgp-encrypted',
                    'application/pgp-keys',
                    'application/pgp-signature'
                ],
                extensions: ['asc', 'pgp', 'sig'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 8983).then(__webpack_require__.bind(__webpack_require__, 98983));
                    return legacy(m.asciiArmor);
                }
            },
            {
                name: 'ASN.1',
                displayName: trans.__('ASN.1'),
                mime: 'text/x-ttcn-asn',
                extensions: ['asn', 'asn1'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 7534).then(__webpack_require__.bind(__webpack_require__, 97534));
                    return legacy(m.asn1({}));
                }
            },
            {
                name: 'Asterisk',
                displayName: trans.__('Asterisk'),
                mime: 'text/x-asterisk',
                filename: /^extensions\.conf$/i,
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 403).then(__webpack_require__.bind(__webpack_require__, 70403));
                    return legacy(m.asterisk);
                }
            },
            {
                name: 'Brainfuck',
                displayName: trans.__('Brainfuck'),
                mime: 'text/x-brainfuck',
                extensions: ['b', 'bf'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 2702).then(__webpack_require__.bind(__webpack_require__, 12702));
                    return legacy(m.brainfuck);
                }
            },
            {
                name: 'Cobol',
                displayName: trans.__('Cobol'),
                mime: 'text/x-cobol',
                extensions: ['cob', 'cpy'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 8979).then(__webpack_require__.bind(__webpack_require__, 38979));
                    return legacy(m.cobol);
                }
            },
            {
                name: 'C#',
                displayName: trans.__('C#'),
                alias: ['csharp', 'cs'],
                mime: 'text/x-csharp',
                extensions: ['cs'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 9425).then(__webpack_require__.bind(__webpack_require__, 49425));
                    return legacy(m.csharp);
                }
            },
            {
                name: 'Clojure',
                displayName: trans.__('Clojure'),
                mime: 'text/x-clojure',
                extensions: ['clj', 'cljc', 'cljx'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 4002).then(__webpack_require__.bind(__webpack_require__, 54002));
                    return legacy(m.clojure);
                }
            },
            {
                name: 'ClojureScript',
                displayName: trans.__('ClojureScript'),
                mime: 'text/x-clojurescript',
                extensions: ['cljs'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 4002).then(__webpack_require__.bind(__webpack_require__, 54002));
                    return legacy(m.clojure);
                }
            },
            {
                name: 'Closure Stylesheets (GSS)',
                displayName: trans.__('Closure Stylesheets (GSS)'),
                mime: 'text/x-gss',
                extensions: ['gss'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 5019).then(__webpack_require__.bind(__webpack_require__, 85019));
                    return legacy(m.gss);
                }
            },
            {
                name: 'CMake',
                displayName: trans.__('CMake'),
                mime: 'text/x-cmake',
                extensions: ['cmake', 'cmake.in'],
                filename: /^CMakeLists\.txt$/,
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 1941).then(__webpack_require__.bind(__webpack_require__, 41941));
                    return legacy(m.cmake);
                }
            },
            {
                name: 'CoffeeScript',
                displayName: trans.__('CoffeeScript'),
                alias: ['coffee', 'coffee-script'],
                mime: [
                    'application/vnd.coffeescript',
                    'text/coffeescript',
                    'text/x-coffeescript'
                ],
                extensions: ['coffee'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 3449).then(__webpack_require__.bind(__webpack_require__, 83449));
                    return legacy(m.coffeeScript);
                }
            },
            {
                name: 'Common Lisp',
                displayName: trans.__('Common Lisp'),
                alias: ['lisp'],
                mime: 'text/x-common-lisp',
                extensions: ['cl', 'lisp', 'el'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 3370).then(__webpack_require__.bind(__webpack_require__, 43370));
                    return legacy(m.commonLisp);
                }
            },
            {
                name: 'Cypher',
                displayName: trans.__('Cypher'),
                mime: 'application/x-cypher-query',
                extensions: ['cyp', 'cypher'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 4387).then(__webpack_require__.bind(__webpack_require__, 24387));
                    return legacy(m.cypher);
                }
            },
            {
                name: 'Cython',
                displayName: trans.__('Cython'),
                mime: 'text/x-cython',
                extensions: ['pyx', 'pxd', 'pxi'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 2871).then(__webpack_require__.bind(__webpack_require__, 72871));
                    return legacy(m.cython);
                }
            },
            {
                name: 'Crystal',
                displayName: trans.__('Crystal'),
                mime: 'text/x-crystal',
                extensions: ['cr'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 3420).then(__webpack_require__.bind(__webpack_require__, 13420));
                    return legacy(m.crystal);
                }
            },
            {
                name: 'D',
                displayName: trans.__('D'),
                mime: 'text/x-d',
                extensions: ['d'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 3501).then(__webpack_require__.bind(__webpack_require__, 73501));
                    return legacy(m.d);
                }
            },
            {
                name: 'Dart',
                displayName: trans.__('Dart'),
                mime: ['application/dart', 'text/x-dart'],
                extensions: ['dart'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 9425).then(__webpack_require__.bind(__webpack_require__, 49425));
                    return legacy(m.dart);
                }
            },
            {
                name: 'diff',
                displayName: trans.__('diff'),
                mime: 'text/x-diff',
                extensions: ['diff', 'patch'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 9116).then(__webpack_require__.bind(__webpack_require__, 39116));
                    return legacy(m.diff);
                }
            },
            {
                name: 'Dockerfile',
                displayName: trans.__('Dockerfile'),
                mime: 'text/x-dockerfile',
                filename: /^Dockerfile$/,
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 2343).then(__webpack_require__.bind(__webpack_require__, 22343));
                    return legacy(m.dockerFile);
                }
            },
            {
                name: 'DTD',
                displayName: trans.__('DTD'),
                mime: 'application/xml-dtd',
                extensions: ['dtd'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 221).then(__webpack_require__.bind(__webpack_require__, 30221));
                    return legacy(m.dtd);
                }
            },
            {
                name: 'Dylan',
                displayName: trans.__('Dylan'),
                mime: 'text/x-dylan',
                extensions: ['dylan', 'dyl', 'intr'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 9331).then(__webpack_require__.bind(__webpack_require__, 69331));
                    return legacy(m.dylan);
                }
            },
            {
                name: 'EBNF',
                displayName: trans.__('EBNF'),
                mime: 'text/x-ebnf',
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 647).then(__webpack_require__.bind(__webpack_require__, 90647));
                    return legacy(m.ebnf);
                }
            },
            {
                name: 'ECL',
                displayName: trans.__('ECL'),
                mime: 'text/x-ecl',
                extensions: ['ecl'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 5061).then(__webpack_require__.bind(__webpack_require__, 75061));
                    return legacy(m.ecl);
                }
            },
            {
                name: 'edn',
                displayName: trans.__('edn'),
                mime: 'application/edn',
                extensions: ['edn'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 4002).then(__webpack_require__.bind(__webpack_require__, 54002));
                    return legacy(m.clojure);
                }
            },
            {
                name: 'Eiffel',
                displayName: trans.__('Eiffel'),
                mime: 'text/x-eiffel',
                extensions: ['e'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 7264).then(__webpack_require__.bind(__webpack_require__, 57264));
                    return legacy(m.eiffel);
                }
            },
            {
                name: 'Elm',
                displayName: trans.__('Elm'),
                mime: 'text/x-elm',
                extensions: ['elm'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 1558).then(__webpack_require__.bind(__webpack_require__, 21558));
                    return legacy(m.elm);
                }
            },
            {
                name: 'Erlang',
                displayName: trans.__('Erlang'),
                mime: 'text/x-erlang',
                extensions: ['erl'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 883).then(__webpack_require__.bind(__webpack_require__, 20883));
                    return legacy(m.erlang);
                }
            },
            {
                name: 'Esper',
                displayName: trans.__('Esper'),
                mime: 'text/x-esper',
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 8479).then(__webpack_require__.bind(__webpack_require__, 48479));
                    return legacy(m.esper);
                }
            },
            {
                name: 'Factor',
                displayName: trans.__('Factor'),
                mime: 'text/x-factor',
                extensions: ['factor'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 9037).then(__webpack_require__.bind(__webpack_require__, 59037));
                    return legacy(m.factor);
                }
            },
            {
                name: 'FCL',
                displayName: trans.__('FCL'),
                mime: 'text/x-fcl',
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 4521).then(__webpack_require__.bind(__webpack_require__, 74521));
                    return legacy(m.fcl);
                }
            },
            {
                name: 'Forth',
                displayName: trans.__('Forth'),
                mime: 'text/x-forth',
                extensions: ['forth', 'fth', '4th'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 7817).then(__webpack_require__.bind(__webpack_require__, 77817));
                    return legacy(m.forth);
                }
            },
            {
                name: 'Fortran',
                displayName: trans.__('Fortran'),
                mime: 'text/x-fortran',
                extensions: ['f', 'for', 'f77', 'f90', 'f95'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 3562).then(__webpack_require__.bind(__webpack_require__, 33562));
                    return legacy(m.fortran);
                }
            },
            {
                name: 'F#',
                displayName: trans.__('F#'),
                alias: ['fsharp'],
                mime: 'text/x-fsharp',
                extensions: ['fs'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 7022).then(__webpack_require__.bind(__webpack_require__, 47022));
                    return legacy(m.fSharp);
                }
            },
            {
                name: 'Gas',
                displayName: trans.__('Gas'),
                mime: 'text/x-gas',
                extensions: ['s'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 5972).then(__webpack_require__.bind(__webpack_require__, 15972));
                    return legacy(m.gas);
                }
            },
            {
                name: 'Gherkin',
                displayName: trans.__('Gherkin'),
                mime: 'text/x-feature',
                extensions: ['feature'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 906).then(__webpack_require__.bind(__webpack_require__, 10906));
                    return legacy(m.gherkin);
                }
            },
            {
                name: 'Go',
                displayName: trans.__('Go'),
                mime: 'text/x-go',
                extensions: ['go'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 9022).then(__webpack_require__.bind(__webpack_require__, 89022));
                    return legacy(m.go);
                }
            },
            {
                name: 'Groovy',
                displayName: trans.__('Groovy'),
                mime: 'text/x-groovy',
                extensions: ['groovy', 'gradle'],
                filename: /^Jenkinsfile$/,
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 7360).then(__webpack_require__.bind(__webpack_require__, 7360));
                    return legacy(m.groovy);
                }
            },
            {
                name: 'Haskell',
                displayName: trans.__('Haskell'),
                mime: 'text/x-haskell',
                extensions: ['hs'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 3111).then(__webpack_require__.bind(__webpack_require__, 63111));
                    return legacy(m.haskell);
                }
            },
            {
                name: 'Haxe',
                displayName: trans.__('Haxe'),
                mime: 'text/x-haxe',
                extensions: ['hx'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 4039).then(__webpack_require__.bind(__webpack_require__, 84039));
                    return legacy(m.haxe);
                }
            },
            {
                name: 'HXML',
                displayName: trans.__('HXML'),
                mime: 'text/x-hxml',
                extensions: ['hxml'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 4039).then(__webpack_require__.bind(__webpack_require__, 84039));
                    return legacy(m.hxml);
                }
            },
            {
                name: 'HTTP',
                displayName: trans.__('HTTP'),
                mime: 'message/http',
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 9060).then(__webpack_require__.bind(__webpack_require__, 19060));
                    return legacy(m.http);
                }
            },
            {
                name: 'IDL',
                displayName: trans.__('IDL'),
                mime: 'text/x-idl',
                extensions: ['pro'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 9250).then(__webpack_require__.bind(__webpack_require__, 89250));
                    return legacy(m.idl);
                }
            },
            {
                name: 'JSON-LD',
                displayName: trans.__('JSON-LD'),
                alias: ['jsonld'],
                mime: 'application/ld+json',
                extensions: ['jsonld'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 661).then(__webpack_require__.bind(__webpack_require__, 70661));
                    return legacy(m.jsonld);
                }
            },
            {
                name: 'Jinja2',
                displayName: trans.__('Jinja2'),
                mime: 'text/jinja2',
                extensions: ['j2', 'jinja', 'jinja2'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 9558).then(__webpack_require__.bind(__webpack_require__, 79558));
                    return legacy(m.jinja2);
                }
            },
            {
                name: 'Julia',
                displayName: trans.__('Julia'),
                mime: 'text/x-julia',
                extensions: ['jl'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 1837).then(__webpack_require__.bind(__webpack_require__, 81837));
                    return legacy(m.julia);
                }
            },
            {
                name: 'Kotlin',
                displayName: trans.__('Kotlin'),
                mime: 'text/x-kotlin',
                extensions: ['kt'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 9425).then(__webpack_require__.bind(__webpack_require__, 49425));
                    return legacy(m.kotlin);
                }
            },
            {
                name: 'LESS',
                displayName: trans.__('LESS'),
                mime: 'text/x-less',
                extensions: ['less'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 5019).then(__webpack_require__.bind(__webpack_require__, 85019));
                    return legacy(m.less);
                }
            },
            {
                name: 'LiveScript',
                displayName: trans.__('LiveScript'),
                alias: ['ls'],
                mime: 'text/x-livescript',
                extensions: ['ls'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 3211).then(__webpack_require__.bind(__webpack_require__, 3211));
                    return legacy(m.liveScript);
                }
            },
            {
                name: 'Lua',
                displayName: trans.__('Lua'),
                mime: 'text/x-lua',
                extensions: ['lua'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 5494).then(__webpack_require__.bind(__webpack_require__, 25494));
                    return legacy(m.lua);
                }
            },
            {
                name: 'mIRC',
                displayName: trans.__('mIRC'),
                mime: 'text/mirc',
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 8937).then(__webpack_require__.bind(__webpack_require__, 58937));
                    return legacy(m.mirc);
                }
            },
            {
                name: 'Mathematica',
                displayName: trans.__('Mathematica'),
                mime: 'text/x-mathematica',
                extensions: ['m', 'nb', 'wl', 'wls'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 1418).then(__webpack_require__.bind(__webpack_require__, 1418));
                    return legacy(m.mathematica);
                }
            },
            {
                name: 'Modelica',
                displayName: trans.__('Modelica'),
                mime: 'text/x-modelica',
                extensions: ['mo'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 6788).then(__webpack_require__.bind(__webpack_require__, 26788));
                    return legacy(m.modelica);
                }
            },
            {
                name: 'MUMPS',
                displayName: trans.__('MUMPS'),
                mime: 'text/x-mumps',
                extensions: ['mps'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 6139).then(__webpack_require__.bind(__webpack_require__, 66139));
                    return legacy(m.mumps);
                }
            },
            {
                name: 'mbox',
                displayName: trans.__('mbox'),
                mime: 'application/mbox',
                extensions: ['mbox'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 4965).then(__webpack_require__.bind(__webpack_require__, 24965));
                    return legacy(m.mbox);
                }
            },
            {
                name: 'Nginx',
                displayName: trans.__('Nginx'),
                mime: 'text/x-nginx-conf',
                filename: /nginx.*\.conf$/i,
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 67).then(__webpack_require__.bind(__webpack_require__, 80067));
                    return legacy(m.nginx);
                }
            },
            {
                name: 'NSIS',
                displayName: trans.__('NSIS'),
                mime: 'text/x-nsis',
                extensions: ['nsh', 'nsi'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 1091).then(__webpack_require__.bind(__webpack_require__, 61091));
                    return legacy(m.nsis);
                }
            },
            {
                name: 'NTriples',
                displayName: trans.__('NTriples'),
                mime: [
                    'application/n-triples',
                    'application/n-quads',
                    'text/n-triples'
                ],
                extensions: ['nt', 'nq'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 9676).then(__webpack_require__.bind(__webpack_require__, 39676));
                    return legacy(m.ntriples);
                }
            },
            {
                name: 'Objective-C',
                displayName: trans.__('Objective-C'),
                alias: ['objective-c', 'objc'],
                mime: 'text/x-objectivec',
                extensions: ['m'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 9425).then(__webpack_require__.bind(__webpack_require__, 49425));
                    return legacy(m.objectiveC);
                }
            },
            {
                name: 'Objective-C++',
                displayName: trans.__('Objective-C++'),
                alias: ['objective-c++', 'objc++'],
                mime: 'text/x-objectivec++',
                extensions: ['mm'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 9425).then(__webpack_require__.bind(__webpack_require__, 49425));
                    return legacy(m.objectiveCpp);
                }
            },
            {
                name: 'OCaml',
                displayName: trans.__('OCaml'),
                mime: 'text/x-ocaml',
                extensions: ['ml', 'mli', 'mll', 'mly'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 7022).then(__webpack_require__.bind(__webpack_require__, 47022));
                    return legacy(m.oCaml);
                }
            },
            {
                name: 'Octave',
                displayName: trans.__('Octave'),
                mime: 'text/x-octave',
                extensions: ['m'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 3336).then(__webpack_require__.bind(__webpack_require__, 33336));
                    return legacy(m.octave);
                }
            },
            {
                name: 'Oz',
                displayName: trans.__('Oz'),
                mime: 'text/x-oz',
                extensions: ['oz'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 632).then(__webpack_require__.bind(__webpack_require__, 632));
                    return legacy(m.oz);
                }
            },
            {
                name: 'Pascal',
                displayName: trans.__('Pascal'),
                mime: 'text/x-pascal',
                extensions: ['p', 'pas'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 2386).then(__webpack_require__.bind(__webpack_require__, 42386));
                    return legacy(m.pascal);
                }
            },
            {
                name: 'Perl',
                displayName: trans.__('Perl'),
                mime: 'text/x-perl',
                extensions: ['pl', 'pm'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 3322).then(__webpack_require__.bind(__webpack_require__, 53322));
                    return legacy(m.perl);
                }
            },
            {
                name: 'Pig',
                displayName: trans.__('Pig'),
                mime: 'text/x-pig',
                extensions: ['pig'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 8381).then(__webpack_require__.bind(__webpack_require__, 68381));
                    return legacy(m.pig);
                }
            },
            {
                name: 'PowerShell',
                displayName: trans.__('PowerShell'),
                mime: 'application/x-powershell',
                extensions: ['ps1', 'psd1', 'psm1'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 8378).then(__webpack_require__.bind(__webpack_require__, 18378));
                    return legacy(m.powerShell);
                }
            },
            {
                name: 'Properties files',
                displayName: trans.__('Properties files'),
                alias: ['ini', 'properties'],
                mime: 'text/x-properties',
                extensions: ['properties', 'ini', 'in'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 7803).then(__webpack_require__.bind(__webpack_require__, 87803));
                    return legacy(m.properties);
                }
            },
            {
                name: 'ProtoBuf',
                displayName: trans.__('ProtoBuf'),
                mime: 'text/x-protobuf',
                extensions: ['proto'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 114).then(__webpack_require__.bind(__webpack_require__, 40114));
                    return legacy(m.protobuf);
                }
            },
            {
                name: 'Puppet',
                displayName: trans.__('Puppet'),
                mime: 'text/x-puppet',
                extensions: ['pp'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 7005).then(__webpack_require__.bind(__webpack_require__, 57005));
                    return legacy(m.puppet);
                }
            },
            {
                name: 'Q',
                displayName: trans.__('Q'),
                mime: 'text/x-q',
                extensions: ['q'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 1088).then(__webpack_require__.bind(__webpack_require__, 31088));
                    return legacy(m.q);
                }
            },
            {
                name: 'R',
                displayName: trans.__('R'),
                alias: ['rscript'],
                mime: 'text/x-rsrc',
                extensions: ['r', 'R'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 2188).then(__webpack_require__.bind(__webpack_require__, 42188));
                    return legacy(m.r);
                }
            },
            {
                name: 'RPM Changes',
                displayName: trans.__('RPM Changes'),
                mime: 'text/x-rpm-changes',
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 3700).then(__webpack_require__.bind(__webpack_require__, 13700));
                    return legacy(m.rpmChanges);
                }
            },
            {
                name: 'RPM Spec',
                displayName: trans.__('RPM Spec'),
                mime: 'text/x-rpm-spec',
                extensions: ['spec'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 3700).then(__webpack_require__.bind(__webpack_require__, 13700));
                    return legacy(m.rpmSpec);
                }
            },
            {
                name: 'Ruby',
                displayName: trans.__('Ruby'),
                alias: ['jruby', 'macruby', 'rake', 'rb', 'rbx'],
                mime: 'text/x-ruby',
                extensions: ['rb'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 5299).then(__webpack_require__.bind(__webpack_require__, 68433));
                    return legacy(m.ruby);
                }
            },
            {
                name: 'SAS',
                displayName: trans.__('SAS'),
                mime: 'text/x-sas',
                extensions: ['sas'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 4825).then(__webpack_require__.bind(__webpack_require__, 44825));
                    return legacy(m.sas);
                }
            },
            {
                name: 'Scala',
                displayName: trans.__('Scala'),
                mime: 'text/x-scala',
                extensions: ['scala'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 9425).then(__webpack_require__.bind(__webpack_require__, 49425));
                    return legacy(m.scala);
                }
            },
            {
                name: 'Scheme',
                displayName: trans.__('Scheme'),
                mime: 'text/x-scheme',
                extensions: ['scm', 'ss'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 899).then(__webpack_require__.bind(__webpack_require__, 20899));
                    return legacy(m.scheme);
                }
            },
            {
                name: 'SCSS',
                displayName: trans.__('SCSS'),
                mime: 'text/x-scss',
                extensions: ['scss'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 5019).then(__webpack_require__.bind(__webpack_require__, 85019));
                    return legacy(m.sCSS);
                }
            },
            {
                name: 'Shell',
                displayName: trans.__('Shell'),
                alias: ['bash', 'sh', 'zsh'],
                mime: ['text/x-sh', 'application/x-sh'],
                extensions: ['sh', 'ksh', 'bash'],
                filename: /^PKGBUILD$/,
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 7170).then(__webpack_require__.bind(__webpack_require__, 27170));
                    return legacy(m.shell);
                }
            },
            {
                name: 'Sieve',
                displayName: trans.__('Sieve'),
                mime: 'application/sieve',
                extensions: ['siv', 'sieve'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 745).then(__webpack_require__.bind(__webpack_require__, 50745));
                    return legacy(m.sieve);
                }
            },
            {
                name: 'Smalltalk',
                displayName: trans.__('Smalltalk'),
                mime: 'text/x-stsrc',
                extensions: ['st'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 9234).then(__webpack_require__.bind(__webpack_require__, 9234));
                    return legacy(m.smalltalk);
                }
            },
            {
                name: 'Solr',
                displayName: trans.__('Solr'),
                mime: 'text/x-solr',
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 85).then(__webpack_require__.bind(__webpack_require__, 50085));
                    return legacy(m.solr);
                }
            },
            {
                name: 'SML',
                displayName: trans.__('SML'),
                mime: 'text/x-sml',
                extensions: ['sml', 'sig', 'fun', 'smackspec'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 7022).then(__webpack_require__.bind(__webpack_require__, 47022));
                    return legacy(m.sml);
                }
            },
            {
                name: 'SPARQL',
                displayName: trans.__('SPARQL'),
                alias: ['sparul'],
                mime: 'application/sparql-query',
                extensions: ['rq', 'sparql'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 5249).then(__webpack_require__.bind(__webpack_require__, 55249));
                    return legacy(m.sparql);
                }
            },
            {
                name: 'Spreadsheet',
                displayName: trans.__('Spreadsheet'),
                alias: ['excel', 'formula'],
                mime: 'text/x-spreadsheet',
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 69).then(__webpack_require__.bind(__webpack_require__, 70069));
                    return legacy(m.spreadsheet);
                }
            },
            {
                name: 'Squirrel',
                displayName: trans.__('Squirrel'),
                mime: 'text/x-squirrel',
                extensions: ['nut'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 9425).then(__webpack_require__.bind(__webpack_require__, 49425));
                    return legacy(m.squirrel);
                }
            },
            {
                name: 'Stylus',
                displayName: trans.__('Stylus'),
                mime: 'text/x-styl',
                extensions: ['styl'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 6739).then(__webpack_require__.bind(__webpack_require__, 56739));
                    return legacy(m.stylus);
                }
            },
            {
                name: 'Swift',
                displayName: trans.__('Swift'),
                mime: 'text/x-swift',
                extensions: ['swift'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 1618).then(__webpack_require__.bind(__webpack_require__, 51618));
                    return legacy(m.swift);
                }
            },
            {
                name: 'sTeX',
                displayName: trans.__('sTeX'),
                mime: 'text/x-stex',
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 311).then(__webpack_require__.bind(__webpack_require__, 60311));
                    return legacy(m.stex);
                }
            },
            {
                name: 'LaTeX',
                displayName: trans.__('LaTeX'),
                alias: ['tex'],
                mime: 'text/x-latex',
                extensions: ['text', 'ltx', 'tex'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 311).then(__webpack_require__.bind(__webpack_require__, 60311));
                    return legacy(m.stex);
                }
            },
            {
                name: 'SystemVerilog',
                displayName: trans.__('SystemVerilog'),
                mime: 'text/x-systemverilog',
                extensions: ['v', 'sv', 'svh'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 5822).then(__webpack_require__.bind(__webpack_require__, 45822));
                    return legacy(m.verilog);
                }
            },
            {
                name: 'Tcl',
                displayName: trans.__('Tcl'),
                mime: 'text/x-tcl',
                extensions: ['tcl'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 8446).then(__webpack_require__.bind(__webpack_require__, 8446));
                    return legacy(m.tcl);
                }
            },
            {
                name: 'Textile',
                displayName: trans.__('Textile'),
                mime: 'text/x-textile',
                extensions: ['textile'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 4030).then(__webpack_require__.bind(__webpack_require__, 84030));
                    return legacy(m.textile);
                }
            },
            {
                name: 'TiddlyWiki',
                displayName: trans.__('TiddlyWiki'),
                mime: 'text/x-tiddlywiki',
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 7054).then(__webpack_require__.bind(__webpack_require__, 27054));
                    return legacy(m.tiddlyWiki);
                }
            },
            {
                name: 'Tiki wiki',
                displayName: trans.__('Tiki wiki'),
                mime: 'text/tiki',
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 5425).then(__webpack_require__.bind(__webpack_require__, 15425));
                    return legacy(m.tiki);
                }
            },
            {
                name: 'TOML',
                displayName: trans.__('TOML'),
                mime: 'text/x-toml',
                extensions: ['toml'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 2682).then(__webpack_require__.bind(__webpack_require__, 92682));
                    return legacy(m.toml);
                }
            },
            {
                name: 'troff',
                displayName: trans.__('troff'),
                mime: 'text/troff',
                extensions: ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 8433).then(__webpack_require__.bind(__webpack_require__, 28433));
                    return legacy(m.troff);
                }
            },
            {
                name: 'TTCN',
                displayName: trans.__('TTCN'),
                mime: 'text/x-ttcn',
                extensions: ['ttcn', 'ttcn3', 'ttcnpp'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 1122).then(__webpack_require__.bind(__webpack_require__, 21122));
                    return legacy(m.ttcn);
                }
            },
            {
                name: 'TTCN_CFG',
                displayName: trans.__('TTCN_CFG'),
                mime: 'text/x-ttcn-cfg',
                extensions: ['cfg'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 6942).then(__webpack_require__.bind(__webpack_require__, 6942));
                    return legacy(m.ttcnCfg);
                }
            },
            {
                name: 'Turtle',
                displayName: trans.__('Turtle'),
                mime: 'text/turtle',
                extensions: ['ttl'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 9604).then(__webpack_require__.bind(__webpack_require__, 19604));
                    return legacy(m.turtle);
                }
            },
            {
                name: 'Web IDL',
                displayName: trans.__('Web IDL'),
                mime: 'text/x-webidl',
                extensions: ['webidl'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 4148).then(__webpack_require__.bind(__webpack_require__, 64148));
                    return legacy(m.webIDL);
                }
            },
            {
                name: 'VB.NET',
                displayName: trans.__('VB.NET'),
                mime: 'text/x-vb',
                extensions: ['vb'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 5834).then(__webpack_require__.bind(__webpack_require__, 75834));
                    return legacy(m.vb);
                }
            },
            {
                name: 'VBScript',
                displayName: trans.__('VBScript'),
                mime: 'text/vbscript',
                extensions: ['vbs'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 5996).then(__webpack_require__.bind(__webpack_require__, 35996));
                    return legacy(m.vbScript);
                }
            },
            {
                name: 'Velocity',
                displayName: trans.__('Velocity'),
                mime: 'text/velocity',
                extensions: ['vtl'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 431).then(__webpack_require__.bind(__webpack_require__, 431));
                    return legacy(m.velocity);
                }
            },
            {
                name: 'Verilog',
                displayName: trans.__('Verilog'),
                mime: 'text/x-verilog',
                extensions: ['v'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 5822).then(__webpack_require__.bind(__webpack_require__, 45822));
                    return legacy(m.verilog);
                }
            },
            {
                name: 'VHDL',
                displayName: trans.__('VHDL'),
                mime: 'text/x-vhdl',
                extensions: ['vhd', 'vhdl'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 677).then(__webpack_require__.bind(__webpack_require__, 30677));
                    return legacy(m.vhdl);
                }
            },
            {
                name: 'XQuery',
                displayName: trans.__('XQuery'),
                mime: 'application/xquery',
                extensions: ['xy', 'xquery'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 3230).then(__webpack_require__.bind(__webpack_require__, 83230));
                    return legacy(m.xQuery);
                }
            },
            {
                name: 'Yacas',
                displayName: trans.__('Yacas'),
                mime: 'text/x-yacas',
                extensions: ['ys'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 4038).then(__webpack_require__.bind(__webpack_require__, 44038));
                    return legacy(m.yacas);
                }
            },
            {
                name: 'YAML',
                displayName: trans.__('YAML'),
                alias: ['yml'],
                mime: ['text/x-yaml', 'text/yaml'],
                extensions: ['yaml', 'yml'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 9233).then(__webpack_require__.bind(__webpack_require__, 9233));
                    return legacy(m.yaml);
                }
            },
            {
                name: 'Z80',
                displayName: trans.__('Z80'),
                mime: 'text/x-z80',
                extensions: ['z80'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 5698).then(__webpack_require__.bind(__webpack_require__, 75698));
                    return legacy(m.z80);
                }
            },
            {
                name: 'mscgen',
                displayName: trans.__('mscgen'),
                mime: 'text/x-mscgen',
                extensions: ['mscgen', 'mscin', 'msc'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 4843).then(__webpack_require__.bind(__webpack_require__, 64843));
                    return legacy(m.mscgen);
                }
            },
            {
                name: 'xu',
                displayName: trans.__('xu'),
                mime: 'text/x-xu',
                extensions: ['xu'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 4843).then(__webpack_require__.bind(__webpack_require__, 64843));
                    return legacy(m.xu);
                }
            },
            {
                name: 'msgenny',
                displayName: trans.__('msgenny'),
                mime: 'text/x-msgenny',
                extensions: ['msgenny'],
                async load() {
                    const m = await __webpack_require__.e(/* import() */ 4843).then(__webpack_require__.bind(__webpack_require__, 64843));
                    return legacy(m.msgenny);
                }
            }
        ];
    }
    EditorLanguageRegistry.getDefaultLanguages = getDefaultLanguages;
})(EditorLanguageRegistry || (EditorLanguageRegistry = {}));

;// CONCATENATED MODULE: ../packages/codemirror/lib/editor.js
/* eslint-disable @typescript-eslint/ban-types */
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








/**
 * The class name added to CodeMirrorWidget instances.
 */
const EDITOR_CLASS = 'jp-CodeMirrorEditor';
/**
 * The key code for the up arrow key.
 */
const UP_ARROW = 38;
/**
 * The key code for the down arrow key.
 */
const DOWN_ARROW = 40;
/**
 * CodeMirror editor.
 */
class CodeMirrorEditor {
    /**
     * Construct a CodeMirror editor.
     */
    constructor(options) {
        var _a, _b, _c, _d, _e, _f;
        /**
         * A signal emitted when either the top or bottom edge is requested.
         */
        this.edgeRequested = new index_es6_js_.Signal(this);
        this._isDisposed = false;
        this._language = new state_dist_index_js_.Compartment();
        this._uuid = '';
        this._languages = (_a = options.languages) !== null && _a !== void 0 ? _a : new EditorLanguageRegistry();
        this._configurator =
            (_d = (_b = options.extensionsRegistry) === null || _b === void 0 ? void 0 : _b.createNew({
                ...options,
                inline: (_c = options.inline) !== null && _c !== void 0 ? _c : false
            })) !== null && _d !== void 0 ? _d : new ExtensionsHandler();
        const host = (this.host = options.host);
        host.classList.add(EDITOR_CLASS);
        host.classList.add('jp-Editor');
        host.addEventListener('focus', this, true);
        host.addEventListener('blur', this, true);
        host.addEventListener('scroll', this, true);
        this._uuid = (_e = options.uuid) !== null && _e !== void 0 ? _e : coreutils_dist_index_js_.UUID.uuid4();
        const model = (this._model = options.model);
        // Default keydown handler - it will have low priority
        const onKeyDown = view_dist_index_js_.EditorView.domEventHandlers({
            keydown: (event, view) => {
                return this.onKeydown(event);
            }
        });
        const updateListener = view_dist_index_js_.EditorView.updateListener.of((update) => {
            this._onDocChanged(update);
        });
        this._editor = Private.createEditor(host, this._configurator, [
            // We need to set the order to high, otherwise the keybinding for ArrowUp/ArrowDown
            // will process the event shunting our edge detection code.
            state_dist_index_js_.Prec.high(onKeyDown),
            updateListener,
            // Initialize with empty extension
            this._language.of([]),
            ...((_f = options.extensions) !== null && _f !== void 0 ? _f : [])
        ], model.sharedModel.source);
        this._onMimeTypeChanged();
        this._onCursorActivity();
        this._configurator.configChanged.connect(this.onConfigChanged, this);
        model.mimeTypeChanged.connect(this._onMimeTypeChanged, this);
    }
    /**
     * The uuid of this editor;
     */
    get uuid() {
        return this._uuid;
    }
    set uuid(value) {
        this._uuid = value;
    }
    /**
     * Get the codemirror editor wrapped by the editor.
     */
    get editor() {
        return this._editor;
    }
    /**
     * Get the codemirror doc wrapped by the widget.
     */
    get doc() {
        return this._editor.state.doc;
    }
    /**
     * Get the number of lines in the editor.
     */
    get lineCount() {
        return this.doc.lines;
    }
    /**
     * Returns a model for this editor.
     */
    get model() {
        return this._model;
    }
    /**
     * The height of a line in the editor in pixels.
     */
    get lineHeight() {
        return this._editor.defaultLineHeight;
    }
    /**
     * The widget of a character in the editor in pixels.
     */
    get charWidth() {
        return this._editor.defaultCharacterWidth;
    }
    /**
     * Tests whether the editor is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this.host.removeEventListener('focus', this, true);
        this.host.removeEventListener('blur', this, true);
        this.host.removeEventListener('scroll', this, true);
        this._configurator.dispose();
        index_es6_js_.Signal.clearData(this);
        this.editor.destroy();
    }
    /**
     * Get a config option for the editor.
     */
    getOption(option) {
        return this._configurator.getOption(option);
    }
    /**
     * Whether the option exists or not.
     */
    hasOption(option) {
        return this._configurator.hasOption(option);
    }
    /**
     * Set a config option for the editor.
     */
    setOption(option, value) {
        this._configurator.setOption(option, value);
    }
    /**
     * Set config options for the editor.
     *
     * This method is preferred when setting several options. The
     * options are set within an operation, which only performs
     * the costly update at the end, and not after every option
     * is set.
     */
    setOptions(options) {
        this._configurator.setOptions(options);
    }
    /**
     * Inject an extension into the editor
     *
     * @alpha
     * @experimental
     * @param ext CodeMirror 6 extension
     */
    injectExtension(ext) {
        this._configurator.injectExtension(this._editor, ext);
    }
    /**
     * Returns the content for the given line number.
     */
    getLine(line) {
        // TODO: CM6 remove +1 when CM6 first line number has propagated
        line = line + 1;
        return line <= this.doc.lines ? this.doc.line(line).text : undefined;
    }
    /**
     * Find an offset for the given position.
     */
    getOffsetAt(position) {
        // TODO: CM6 remove +1 when CM6 first line number has propagated
        return this.doc.line(position.line + 1).from + position.column;
    }
    /**
     * Find a position for the given offset.
     */
    getPositionAt(offset) {
        // TODO: CM6 remove -1 when CM6 first line number has propagated
        const line = this.doc.lineAt(offset);
        return { line: line.number - 1, column: offset - line.from };
    }
    /**
     * Undo one edit (if any undo events are stored).
     */
    undo() {
        this.model.sharedModel.undo();
    }
    /**
     * Redo one undone edit.
     */
    redo() {
        this.model.sharedModel.redo();
    }
    /**
     * Clear the undo history.
     */
    clearHistory() {
        this.model.sharedModel.clearUndoHistory();
    }
    /**
     * Brings browser focus to this editor text.
     */
    focus() {
        this._editor.focus();
    }
    /**
     * Test whether the editor has keyboard focus.
     */
    hasFocus() {
        return this._editor.hasFocus;
    }
    /**
     * Explicitly blur the editor.
     */
    blur() {
        this._editor.contentDOM.blur();
    }
    get state() {
        return this._editor.state;
    }
    firstLine() {
        // TODO: return 1 when CM6 first line number has propagated
        return 0;
    }
    lastLine() {
        return this.doc.lines - 1;
    }
    cursorCoords(where, mode) {
        const selection = this.state.selection.main;
        const pos = where ? selection.from : selection.to;
        const rect = this.editor.coordsAtPos(pos);
        return rect;
    }
    getRange(from, to, separator) {
        const fromOffset = this.getOffsetAt(this._toPosition(from));
        const toOffset = this.getOffsetAt(this._toPosition(to));
        return this.state.sliceDoc(fromOffset, toOffset);
    }
    /**
     * Reveal the given position in the editor.
     */
    revealPosition(position) {
        const offset = this.getOffsetAt(position);
        this._editor.dispatch({
            effects: view_dist_index_js_.EditorView.scrollIntoView(offset)
        });
    }
    /**
     * Reveal the given selection in the editor.
     */
    revealSelection(selection) {
        const start = this.getOffsetAt(selection.start);
        const end = this.getOffsetAt(selection.end);
        this._editor.dispatch({
            effects: view_dist_index_js_.EditorView.scrollIntoView(state_dist_index_js_.EditorSelection.range(start, end))
        });
    }
    /**
     * Get the window coordinates given a cursor position.
     */
    getCoordinateForPosition(position) {
        const offset = this.getOffsetAt(position);
        const rect = this.editor.coordsAtPos(offset);
        return rect;
    }
    /**
     * Get the cursor position given window coordinates.
     *
     * @param coordinate - The desired coordinate.
     *
     * @returns The position of the coordinates, or null if not
     *   contained in the editor.
     */
    getPositionForCoordinate(coordinate) {
        const offset = this.editor.posAtCoords({
            x: coordinate.left,
            y: coordinate.top
        });
        return this.getPositionAt(offset) || null;
    }
    /**
     * Returns the primary position of the cursor, never `null`.
     */
    getCursorPosition() {
        const offset = this.state.selection.main.head;
        return this.getPositionAt(offset);
    }
    /**
     * Set the primary position of the cursor.
     *
     * #### Notes
     * This will remove any secondary cursors.
     */
    setCursorPosition(position, options) {
        const offset = this.getOffsetAt(position);
        this.editor.dispatch({
            selection: { anchor: offset },
            scrollIntoView: true
        });
        // If the editor does not have focus, this cursor change
        // will get screened out in _onCursorsChanged(). Make an
        // exception for this method.
        if (!this.editor.hasFocus) {
            this.model.selections.set(this.uuid, this.getSelections());
        }
    }
    /**
     * Returns the primary selection, never `null`.
     */
    getSelection() {
        return this.getSelections()[0];
    }
    /**
     * Set the primary selection. This will remove any secondary cursors.
     */
    setSelection(selection) {
        this.setSelections([selection]);
    }
    /**
     * Gets the selections for all the cursors, never `null` or empty.
     */
    getSelections() {
        const selections = this.state.selection.ranges; //= [{anchor: number, head: number}]
        if (selections.length > 0) {
            const sel = selections.map(r => ({
                anchor: this._toCodeMirrorPosition(this.getPositionAt(r.from)),
                head: this._toCodeMirrorPosition(this.getPositionAt(r.to))
            }));
            return sel.map(selection => this._toSelection(selection));
        }
        const cursor = this._toCodeMirrorPosition(this.getPositionAt(this.state.selection.main.head));
        const selection = this._toSelection({ anchor: cursor, head: cursor });
        return [selection];
    }
    /**
     * Sets the selections for all the cursors, should not be empty.
     * Cursors will be removed or added, as necessary.
     * Passing an empty array resets a cursor position to the start of a document.
     */
    setSelections(selections) {
        const sel = selections.length
            ? selections.map(r => state_dist_index_js_.EditorSelection.range(this.getOffsetAt(r.start), this.getOffsetAt(r.end)))
            : [state_dist_index_js_.EditorSelection.range(0, 0)];
        this.editor.dispatch({ selection: state_dist_index_js_.EditorSelection.create(sel) });
    }
    /**
     * Replaces the current selection with the given text.
     *
     * Behaviour for multiple selections is undefined.
     *
     * @param text The text to be inserted.
     */
    replaceSelection(text) {
        const firstSelection = this.getSelections()[0];
        this.model.sharedModel.updateSource(this.getOffsetAt(firstSelection.start), this.getOffsetAt(firstSelection.end), text);
        const newPosition = this.getPositionAt(this.getOffsetAt(firstSelection.start) + text.length);
        this.setSelection({ start: newPosition, end: newPosition });
    }
    /**
     * Get a list of tokens for the current editor text content.
     */
    getTokens() {
        const tokens = [];
        const tree = (0,dist_index_js_.ensureSyntaxTree)(this.state, this.doc.length);
        if (tree) {
            tree.iterate({
                enter: (ref) => {
                    if (ref.node.firstChild === null) {
                        tokens.push({
                            value: this.state.sliceDoc(ref.from, ref.to),
                            offset: ref.from,
                            type: ref.name
                        });
                    }
                    return true;
                }
            });
        }
        return tokens;
    }
    /**
     * Get the token at a given editor position.
     */
    getTokenAt(offset) {
        const tree = (0,dist_index_js_.ensureSyntaxTree)(this.state, offset);
        let token = null;
        if (tree) {
            tree.iterate({
                enter: (ref) => {
                    // If a token has already been discovered, stop iterating.
                    if (token) {
                        return false;
                    }
                    // If it is not a leaf, keep iterating.
                    if (ref.node.firstChild) {
                        return true;
                    }
                    // If the relevant leaf token has been found, stop iterating.
                    if (offset >= ref.from && offset <= ref.to) {
                        token = {
                            value: this.state.sliceDoc(ref.from, ref.to),
                            offset: ref.from,
                            type: ref.name
                        };
                        return false;
                    }
                    return true;
                }
            });
        }
        return token || { offset, value: '' };
    }
    /**
     * Get the token a the cursor position.
     */
    getTokenAtCursor() {
        return this.getTokenAt(this.state.selection.main.head);
    }
    /**
     * Insert a new indented line at the current cursor position.
     */
    newIndentedLine() {
        (0,index_js_.insertNewlineAndIndent)({
            state: this.state,
            dispatch: this.editor.dispatch
        });
    }
    /**
     * Execute a codemirror command on the editor.
     *
     * @param command - The name of the command to execute.
     */
    execCommand(command) {
        command(this.editor);
    }
    onConfigChanged(configurator, changes) {
        configurator.reconfigureExtensions(this._editor, changes);
    }
    /**
     * Handle keydown events from the editor.
     */
    onKeydown(event) {
        const position = this.state.selection.main.head;
        if (position === 0 && event.keyCode === UP_ARROW) {
            if (!event.shiftKey) {
                this.edgeRequested.emit('top');
            }
            return false;
        }
        const line = this.doc.lineAt(position).number;
        if (line === 1 && event.keyCode === UP_ARROW) {
            if (!event.shiftKey) {
                this.edgeRequested.emit('topLine');
            }
            return false;
        }
        const length = this.doc.length;
        if (position === length && event.keyCode === DOWN_ARROW) {
            if (!event.shiftKey) {
                this.edgeRequested.emit('bottom');
            }
            return false;
        }
        return false;
    }
    /**
     * Handles a mime type change.
     */
    _onMimeTypeChanged() {
        // TODO: should we provide a hook for when the mode is done being set?
        this._languages
            .getLanguage(this._model.mimeType)
            .then(language => {
            var _a;
            this._editor.dispatch({
                effects: this._language.reconfigure((_a = language === null || language === void 0 ? void 0 : language.support) !== null && _a !== void 0 ? _a : [])
            });
        })
            .catch(reason => {
            console.log(`Failed to load language for '${this._model.mimeType}'.`, reason);
            this._editor.dispatch({
                effects: this._language.reconfigure([])
            });
        });
    }
    /**
     * Handles a cursor activity event.
     */
    _onCursorActivity() {
        // Only add selections if the editor has focus. This avoids unwanted
        // triggering of cursor activity due to collaborator actions.
        if (this._editor.hasFocus) {
            const selections = this.getSelections();
            this.model.selections.set(this.uuid, selections);
        }
    }
    /**
     * Converts a code mirror selection to an editor selection.
     */
    _toSelection(selection) {
        return {
            uuid: this.uuid,
            start: this._toPosition(selection.anchor),
            end: this._toPosition(selection.head)
        };
    }
    /**
     * Convert a code mirror position to an editor position.
     */
    _toPosition(position) {
        return {
            line: position.line,
            column: position.ch
        };
    }
    /**
     * Convert an editor position to a code mirror position.
     */
    _toCodeMirrorPosition(position) {
        return {
            line: position.line,
            ch: position.column
        };
    }
    /**
     * Handles document changes.
     */
    _onDocChanged(update) {
        if (update.transactions.length && update.transactions[0].selection) {
            this._onCursorActivity();
        }
    }
    /**
     * Handle the DOM events for the editor.
     *
     * @param event - The DOM event sent to the editor.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the editor's DOM node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'focus':
                this._evtFocus(event);
                break;
            case 'blur':
                this._evtBlur(event);
                break;
            default:
                break;
        }
    }
    /**
     * Handle `focus` events for the editor.
     */
    _evtFocus(event) {
        this.host.classList.add('jp-mod-focused');
        // Update the selections on editor gaining focus because
        // the onCursorActivity function filters usual cursor events
        // based on the editor's focus.
        this._onCursorActivity();
    }
    /**
     * Handle `blur` events for the editor.
     */
    _evtBlur(event) {
        this.host.classList.remove('jp-mod-focused');
    }
}
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    function createEditor(host, editorConfig, additionalExtensions, doc) {
        const extensions = editorConfig.getInitialExtensions();
        extensions.push(...additionalExtensions);
        const view = new view_dist_index_js_.EditorView({
            state: state_dist_index_js_.EditorState.create({
                doc,
                extensions
            }),
            parent: host
        });
        return view;
    }
    Private.createEditor = createEditor;
})(Private || (Private = {}));

// EXTERNAL MODULE: consume shared module (default) @codemirror/search@^6.3.0 (strict) (fallback: ../node_modules/@codemirror/search/dist/index.js)
var search_dist_index_js_ = __webpack_require__(35260);
;// CONCATENATED MODULE: ../packages/codemirror/lib/factory.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






/**
 * CodeMirror editor factory.
 */
class CodeMirrorEditorFactory {
    /**
     * Construct an IEditorFactoryService for CodeMirrorEditors.
     */
    constructor(options = {}) {
        var _a, _b, _c;
        /**
         * Create a new editor for inline code.
         */
        this.newInlineEditor = (options) => {
            var _a;
            options.host.dataset.type = 'inline';
            return this.newEditor({
                ...options,
                config: { ...this.inlineCodeMirrorConfig, ...(options.config || {}) },
                inline: true,
                // FIXME the search keymap should be added in the search plugin
                extensions: [view_dist_index_js_.keymap.of(search_dist_index_js_.searchKeymap)].concat((_a = options.extensions) !== null && _a !== void 0 ? _a : [])
            });
        };
        /**
         * Create a new editor for a full document.
         */
        this.newDocumentEditor = (options) => {
            var _a, _b;
            options.host.dataset.type = 'document';
            return this.newEditor({
                ...options,
                config: { ...this.documentCodeMirrorConfig, ...((_a = options.config) !== null && _a !== void 0 ? _a : {}) },
                inline: false,
                extensions: [
                    view_dist_index_js_.keymap.of([
                        {
                            key: 'Shift-Enter',
                            run: (target) => {
                                return true;
                            }
                        }
                    ])
                ].concat((_b = options.extensions) !== null && _b !== void 0 ? _b : [])
            });
        };
        this.languages = (_a = options.languages) !== null && _a !== void 0 ? _a : new EditorLanguageRegistry();
        this.extensions = (_b = options.extensions) !== null && _b !== void 0 ? _b : new EditorExtensionRegistry();
        this.translator = (_c = options.translator) !== null && _c !== void 0 ? _c : lib_index_js_.nullTranslator;
        this.inlineCodeMirrorConfig = {};
        this.documentCodeMirrorConfig = {
            lineNumbers: true,
            scrollPastEnd: true
        };
    }
    /**
     * Create a new editor
     *
     * @param options Editor options
     * @returns The editor
     */
    newEditor(options) {
        const editor = new CodeMirrorEditor({
            extensionsRegistry: this.extensions,
            languages: this.languages,
            translator: this.translator,
            ...options
        });
        return editor;
    }
}

;// CONCATENATED MODULE: ../packages/codemirror/lib/mimetype.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * The mime type service for CodeMirror.
 */
class CodeMirrorMimeTypeService {
    constructor(languages) {
        this.languages = languages;
    }
    /**
     * Returns a mime type for the given language info.
     *
     * #### Notes
     * If a mime type cannot be found returns the default mime type `text/plain`, never `null`.
     * There may be more than one mime type, but only the first one will be returned.
     * To access all mime types, use `IEditorLanguageRegistry` instead.
     */
    getMimeTypeByLanguage(info) {
        var _a;
        const ext = info.file_extension || '';
        const mode = this.languages.findBest(info.codemirror_mode || {
            mimetype: info.mimetype,
            name: info.name,
            ext: [ext.split('.').slice(-1)[0]]
        });
        return mode
            ? Array.isArray(mode.mime)
                ? (_a = mode.mime[0]) !== null && _a !== void 0 ? _a : codeeditor_lib_index_js_.IEditorMimeTypeService.defaultMimeType
                : mode.mime
            : codeeditor_lib_index_js_.IEditorMimeTypeService.defaultMimeType;
    }
    /**
     * Returns a mime type for the given file path.
     *
     * #### Notes
     * If a mime type cannot be found returns the default mime type `text/plain`, never `null`.
     * There may be more than one mime type, but only the first one will be returned.
     * To access all mime types, use `IEditorLanguageRegistry` instead.
     */
    getMimeTypeByFilePath(path) {
        var _a;
        const ext = coreutils_lib_index_js_.PathExt.extname(path);
        if (ext === '.ipy') {
            return 'text/x-python';
        }
        else if (ext === '.md') {
            return 'text/x-ipythongfm';
        }
        const mode = this.languages.findByFileName(path);
        return mode
            ? Array.isArray(mode.mime)
                ? (_a = mode.mime[0]) !== null && _a !== void 0 ? _a : codeeditor_lib_index_js_.IEditorMimeTypeService.defaultMimeType
                : mode.mime
            : codeeditor_lib_index_js_.IEditorMimeTypeService.defaultMimeType;
    }
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/documentsearch@~4.1.0-alpha.2 (singleton) (fallback: ../packages/documentsearch/lib/index.js)
var documentsearch_lib_index_js_ = __webpack_require__(80599);
;// CONCATENATED MODULE: ../packages/codemirror/lib/searchprovider.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * Search provider for editors.
 */
class EditorSearchProvider {
    /**
     * Constructor
     */
    constructor() {
        /**
         * Current match index
         */
        this.currentIndex = null;
        /**
         * Current search query
         */
        this.query = null;
        this._isActive = true;
        this._inSelection = null;
        this._isDisposed = false;
        this._cmHandler = null;
        this.currentIndex = null;
        this._stateChanged = new index_es6_js_.Signal(this);
    }
    /**
     * CodeMirror search highlighter
     */
    get cmHandler() {
        if (!this._cmHandler) {
            this._cmHandler = new CodeMirrorSearchHighlighter(this.editor);
        }
        return this._cmHandler;
    }
    /**
     * Changed signal to be emitted when search matches change.
     */
    get stateChanged() {
        return this._stateChanged;
    }
    /**
     * Current match index
     */
    get currentMatchIndex() {
        return this.isActive ? this.currentIndex : null;
    }
    /**
     * Whether the cell search is active.
     *
     * This is used when applying search only on selected cells.
     */
    get isActive() {
        return this._isActive;
    }
    /**
     * Whether the search provider is disposed or not.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Number of matches in the cell.
     */
    get matchesCount() {
        return this.isActive ? this.cmHandler.matches.length : 0;
    }
    /**
     * Clear currently highlighted match
     */
    clearHighlight() {
        this.currentIndex = null;
        this.cmHandler.clearHighlight();
        return Promise.resolve();
    }
    /**
     * Dispose the search provider
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        index_es6_js_.Signal.clearData(this);
        if (this.isActive) {
            this.endQuery().catch(reason => {
                console.error(`Failed to end search query on cells.`, reason);
            });
        }
    }
    /**
     * Set `isActive` status.
     *
     * #### Notes
     * It will start or end the search
     *
     * @param v New value
     */
    async setIsActive(v) {
        if (this._isActive === v) {
            return;
        }
        this._isActive = v;
        if (this._isActive) {
            if (this.query !== null) {
                await this.startQuery(this.query, this.filters);
            }
        }
        else {
            await this.endQuery();
        }
    }
    /**
     * Set whether search should be limitted to specified text selection.
     */
    async setSearchSelection(selection) {
        if (this._inSelection === selection) {
            return;
        }
        this._inSelection = selection;
        await this.updateCodeMirror(this.model.sharedModel.getSource());
        this._stateChanged.emit();
    }
    /**
     * Set whether user selection should be protected from modifications.
     *
     * If disabled, the selection will be updated on search and on editor focus
     * to cover the current match. We need to protect selection from modifications
     * for both: search in text and search in cells; since `setSearchSelection`
     * is only telling us about search in text, we need to have an additional
     * way to signal that either search in text or in cells is active, or for
     * any other reason selection range should be protected.
     */
    setProtectSelection(v) {
        this.cmHandler.protectSelection = v;
    }
    /**
     * Initialize the search using the provided options. Should update the UI
     * to highlight all matches and "select" the first match.
     *
     * @param query A RegExp to be use to perform the search
     * @param filters Filter parameters to pass to provider
     */
    async startQuery(query, filters) {
        this.query = query;
        this.filters = filters;
        // Search input
        const content = this.model.sharedModel.getSource();
        await this.updateCodeMirror(content);
        this.model.sharedModel.changed.connect(this.onSharedModelChanged, this);
    }
    /**
     * Stop the search and clean any UI elements.
     */
    async endQuery() {
        await this.clearHighlight();
        await this.cmHandler.endQuery();
        this.currentIndex = null;
    }
    /**
     * Highlight the next match.
     *
     * @returns The next match if there is one.
     */
    async highlightNext(loop = true, options) {
        if (this.matchesCount === 0 || !this.isActive) {
            this.currentIndex = null;
        }
        else {
            let match = await this.cmHandler.highlightNext(options);
            if (match) {
                this.currentIndex = this.cmHandler.currentIndex;
            }
            else {
                // Note: the loop logic is only used in single-editor (e.g. file editor)
                // provider sub-classes, notebook has it's own loop logic and ignores
                // `currentIndex` as set here.
                this.currentIndex = loop ? 0 : null;
            }
            return match;
        }
        return Promise.resolve(this.getCurrentMatch());
    }
    /**
     * Highlight the previous match.
     *
     * @returns The previous match if there is one.
     */
    async highlightPrevious(loop = true, options) {
        if (this.matchesCount === 0 || !this.isActive) {
            this.currentIndex = null;
        }
        else {
            let match = await this.cmHandler.highlightPrevious(options);
            if (match) {
                this.currentIndex = this.cmHandler.currentIndex;
            }
            else {
                this.currentIndex = loop ? this.matchesCount - 1 : null;
            }
            return match;
        }
        return Promise.resolve(this.getCurrentMatch());
    }
    /**
     * Replace the currently selected match with the provided text.
     *
     * If no match is selected, it won't do anything.
     *
     * The caller of this method is expected to call `highlightNext` if after
     * calling `replaceCurrentMatch()` attribute `this.currentIndex` is null.
     * It is necesary to let the caller handle highlighting because this
     * method is used in composition pattern (search engine of notebook cells)
     * and highligthing on the composer (notebook) level needs to switch to next
     * engine (cell) with matches.
     *
     * @param newText The replacement text.
     * @returns Whether a replace occurred.
     */
    replaceCurrentMatch(newText, loop, options) {
        if (!this.isActive) {
            return Promise.resolve(false);
        }
        let occurred = false;
        if (this.currentIndex !== null &&
            this.currentIndex < this.cmHandler.matches.length) {
            const match = this.getCurrentMatch();
            // If cursor there is no match selected, highlight the next match
            if (!match) {
                this.currentIndex = null;
            }
            else {
                this.cmHandler.matches.splice(this.currentIndex, 1);
                this.currentIndex =
                    this.currentIndex < this.cmHandler.matches.length
                        ? Math.max(this.currentIndex - 1, 0)
                        : null;
                const substitutedText = (options === null || options === void 0 ? void 0 : options.regularExpression)
                    ? match.text.replace(this.query, newText)
                    : newText;
                const insertText = (options === null || options === void 0 ? void 0 : options.preserveCase)
                    ? documentsearch_lib_index_js_.GenericSearchProvider.preserveCase(match.text, substitutedText)
                    : substitutedText;
                this.model.sharedModel.updateSource(match.position, match.position + match.text.length, insertText);
                occurred = true;
            }
        }
        return Promise.resolve(occurred);
    }
    /**
     * Replace all matches in the cell source with the provided text
     *
     * @param newText The replacement text.
     * @returns Whether a replace occurred.
     */
    replaceAllMatches(newText, options) {
        if (!this.isActive) {
            return Promise.resolve(false);
        }
        let occurred = this.cmHandler.matches.length > 0;
        let src = this.model.sharedModel.getSource();
        let lastEnd = 0;
        const finalSrc = this.cmHandler.matches.reduce((agg, match) => {
            const start = match.position;
            const end = start + match.text.length;
            const substitutedText = (options === null || options === void 0 ? void 0 : options.regularExpression)
                ? match.text.replace(this.query, newText)
                : newText;
            const insertText = (options === null || options === void 0 ? void 0 : options.preserveCase)
                ? documentsearch_lib_index_js_.GenericSearchProvider.preserveCase(match.text, substitutedText)
                : substitutedText;
            const newStep = `${agg}${src.slice(lastEnd, start)}${insertText}`;
            lastEnd = end;
            return newStep;
        }, '');
        if (occurred) {
            this.cmHandler.matches = [];
            this.currentIndex = null;
            this.model.sharedModel.setSource(`${finalSrc}${src.slice(lastEnd)}`);
        }
        return Promise.resolve(occurred);
    }
    /**
     * Get the current match if it exists.
     *
     * @returns The current match
     */
    getCurrentMatch() {
        if (this.currentIndex === null) {
            return undefined;
        }
        else {
            let match = undefined;
            if (this.currentIndex < this.cmHandler.matches.length) {
                match = this.cmHandler.matches[this.currentIndex];
            }
            return match;
        }
    }
    /**
     * Callback on source change
     *
     * @param emitter Source of the change
     * @param changes Source change
     */
    async onSharedModelChanged(emitter, changes) {
        if (changes.sourceChange) {
            await this.updateCodeMirror(emitter.getSource());
            this._stateChanged.emit();
        }
    }
    /**
     * Update matches
     */
    async updateCodeMirror(content) {
        if (this.query !== null && this.isActive) {
            const allMatches = await documentsearch_lib_index_js_.TextSearchEngine.search(this.query, content);
            if (this._inSelection) {
                const editor = this.editor;
                const start = editor.getOffsetAt(this._inSelection.start);
                const end = editor.getOffsetAt(this._inSelection.end);
                this.cmHandler.matches = allMatches.filter(match => match.position >= start && match.position <= end);
                // A special case to always have a current match when in line selection mode.
                if (this.cmHandler.currentIndex === null &&
                    this.cmHandler.matches.length > 0) {
                    await this.cmHandler.highlightNext({
                        from: 'selection',
                        select: false,
                        scroll: false
                    });
                }
                this.currentIndex = this.cmHandler.currentIndex;
            }
            else {
                this.cmHandler.matches = allMatches;
            }
        }
        else {
            this.cmHandler.matches = [];
        }
    }
}
/**
 * Helper class to highlight texts in a code mirror editor.
 *
 * Highlighted texts (aka `matches`) must be provided through
 * the `matches` attributes.
 *
 * **NOTES:**
 * - to retain the selection visibility `drawSelection` extension is needed.
 * - highlighting starts from the cursor (if editor is focused and `from` is set
 *   to `'auto'`, cursor moved, or `from` argument is set to `'selection'` or
 *   `'selection-start'`), or from last "current" match otherwise.
 * - `currentIndex` is the (readonly) source of truth for the current match.
 */
class CodeMirrorSearchHighlighter {
    /**
     * Constructor
     *
     * @param editor The CodeMirror editor
     */
    constructor(editor) {
        this._current = null;
        this._cm = editor;
        this._matches = new Array();
        this._currentIndex = null;
        this._highlightEffect = state_dist_index_js_.StateEffect.define({
            map: (value, mapping) => {
                const transform = (v) => ({
                    text: v.text,
                    position: mapping.mapPos(v.position)
                });
                return {
                    matches: value.matches.map(transform),
                    currentMatch: value.currentMatch
                        ? transform(value.currentMatch)
                        : null
                };
            }
        });
        this._highlightMark = view_dist_index_js_.Decoration.mark({ class: 'cm-searching' });
        this._currentMark = view_dist_index_js_.Decoration.mark({ class: 'jp-current-match' });
        this._highlightField = state_dist_index_js_.StateField.define({
            create: () => {
                return view_dist_index_js_.Decoration.none;
            },
            update: (highlights, transaction) => {
                highlights = highlights.map(transaction.changes);
                for (let ef of transaction.effects) {
                    if (ef.is(this._highlightEffect)) {
                        const e = ef;
                        if (e.value.matches.length) {
                            // Note: nesting will vary; sometimes `.cm-searching` will be
                            // inside `.jp-current-match`, sometime the other way round.
                            highlights = highlights.update({
                                add: e.value.matches.map(m => this._highlightMark.range(m.position, m.position + m.text.length)),
                                // filter out old marks
                                filter: () => false
                            });
                            highlights = highlights.update({
                                add: e.value.currentMatch
                                    ? [
                                        this._currentMark.range(e.value.currentMatch.position, e.value.currentMatch.position +
                                            e.value.currentMatch.text.length)
                                    ]
                                    : []
                            });
                        }
                        else {
                            highlights = view_dist_index_js_.Decoration.none;
                        }
                    }
                }
                return highlights;
            },
            provide: f => view_dist_index_js_.EditorView.decorations.from(f)
        });
        this._domEventHandlers = view_dist_index_js_.EditorView.domEventHandlers({
            focus: () => {
                // Set cursor on active match when editor gets focused.
                this._selectCurrentMatch();
            }
        });
    }
    /**
     * The current index of the selected match.
     */
    get currentIndex() {
        return this._currentIndex;
    }
    /**
     * The list of matches
     */
    get matches() {
        return this._matches;
    }
    set matches(v) {
        this._matches = v;
        if (this._currentIndex !== null &&
            this._currentIndex > this._matches.length) {
            this._currentIndex = this._matches.length > 0 ? 0 : null;
        }
        this._highlightCurrentMatch({ select: false });
    }
    /**
     * Whether the cursor/selection should not be modified.
     */
    get protectSelection() {
        return this._protectSelection;
    }
    set protectSelection(v) {
        this._protectSelection = v;
    }
    /**
     * Clear all highlighted matches
     */
    clearHighlight() {
        this._currentIndex = null;
        this._highlightCurrentMatch();
    }
    /**
     * Clear the highlighted matches.
     */
    endQuery() {
        this._currentIndex = null;
        this._matches = [];
        if (this._cm) {
            this._cm.editor.dispatch({
                effects: this._highlightEffect.of({ matches: [], currentMatch: null })
            });
        }
        return Promise.resolve();
    }
    /**
     * Highlight the next match
     *
     * @returns The next match if available
     */
    highlightNext(options) {
        var _a;
        this._currentIndex = this._findNext(false, (_a = options === null || options === void 0 ? void 0 : options.from) !== null && _a !== void 0 ? _a : 'auto');
        this._highlightCurrentMatch(options);
        return Promise.resolve(this._currentIndex !== null
            ? this._matches[this._currentIndex]
            : undefined);
    }
    /**
     * Highlight the previous match
     *
     * @returns The previous match if available
     */
    highlightPrevious(options) {
        var _a;
        this._currentIndex = this._findNext(true, (_a = options === null || options === void 0 ? void 0 : options.from) !== null && _a !== void 0 ? _a : 'auto');
        this._highlightCurrentMatch(options);
        return Promise.resolve(this._currentIndex !== null
            ? this._matches[this._currentIndex]
            : undefined);
    }
    /**
     * Set the editor
     *
     * @param editor Editor
     */
    setEditor(editor) {
        if (this._cm) {
            throw new Error('CodeMirrorEditor already set.');
        }
        else {
            this._cm = editor;
            if (this._currentIndex !== null) {
                this._highlightCurrentMatch();
            }
            this._cm.editor.dispatch({
                effects: state_dist_index_js_.StateEffect.appendConfig.of(this._domEventHandlers)
            });
            this._refresh();
        }
    }
    _selectCurrentMatch(scroll = true) {
        // This method has two responsibilities:
        // 1) Scroll the current match into the view - useful for long lines,
        //    and file editors with more lines that fit on the screen
        // 2) When user has focus on the editor (not search box) and presses
        //    ctrl + g/ctrl + shift + g to jump to next match they want their
        //    cursor to jump too.
        // We execute (1) and (2) together as CodeMirror has a special code path
        // to handle both in a single dispatch.
        // The (2) case is inapplicable to search in selection mode, as it would
        // invalidate the query selection, so in that case we only execute (1).
        const match = this._current;
        if (!match) {
            return;
        }
        if (!this._cm) {
            return;
        }
        const cursor = {
            anchor: match.position,
            head: match.position + match.text.length
        };
        const selection = this._cm.editor.state.selection.main;
        if ((selection.from === match.position &&
            selection.to === match.position + match.text.length) ||
            this._protectSelection) {
            // Correct selection is already set or search is restricted to selection:
            // scroll without changing the selection.
            if (scroll) {
                this._cm.editor.dispatch({
                    effects: view_dist_index_js_.EditorView.scrollIntoView(state_dist_index_js_.EditorSelection.range(cursor.anchor, cursor.head))
                });
                return;
            }
        }
        else {
            this._cm.editor.dispatch({
                selection: cursor,
                scrollIntoView: scroll
            });
        }
    }
    _highlightCurrentMatch(options) {
        var _a, _b, _c;
        if (!this._cm) {
            // no-op
            return;
        }
        // Highlight the current index
        if (this._currentIndex !== null) {
            const match = this.matches[this._currentIndex];
            this._current = match;
            // We do not change selection nor scroll if:
            // - user is selecting text,
            // - document was modified
            if ((_a = options === null || options === void 0 ? void 0 : options.select) !== null && _a !== void 0 ? _a : true) {
                if (this._cm.hasFocus()) {
                    // If editor is focused we actually set the cursor on the match.
                    this._selectCurrentMatch((_b = options === null || options === void 0 ? void 0 : options.scroll) !== null && _b !== void 0 ? _b : true);
                }
                else if ((_c = options === null || options === void 0 ? void 0 : options.scroll) !== null && _c !== void 0 ? _c : true) {
                    // otherwise we just scroll to preserve the selection.
                    this._cm.editor.dispatch({
                        effects: view_dist_index_js_.EditorView.scrollIntoView(match.position)
                    });
                }
            }
        }
        else {
            this._current = null;
        }
        this._refresh();
    }
    _refresh() {
        if (!this._cm) {
            // no-op
            return;
        }
        let effects = [
            this._highlightEffect.of({
                matches: this.matches,
                currentMatch: this._current
            })
        ];
        if (!this._cm.state.field(this._highlightField, false)) {
            effects.push(state_dist_index_js_.StateEffect.appendConfig.of([this._highlightField]));
        }
        this._cm.editor.dispatch({ effects });
    }
    _findNext(reverse, from = 'auto') {
        if (this._matches.length === 0) {
            // No-op
            return null;
        }
        let lastPosition = 0;
        if ((from === 'auto' && this._cm.hasFocus()) || from === 'selection') {
            const cursor = this._cm.state.selection.main;
            lastPosition = reverse ? cursor.anchor : cursor.head;
        }
        else if (from === 'selection-start') {
            const cursor = this._cm.state.selection.main;
            lastPosition = Math.min(cursor.anchor, cursor.head);
        }
        else if (from === 'start') {
            lastPosition = 0;
        }
        else if (this._current) {
            lastPosition = reverse
                ? this._current.position
                : this._current.position + this._current.text.length;
        }
        if (lastPosition === 0 && reverse && this.currentIndex === null) {
            // The default position is (0, 0) but we want to start from the end in that case
            lastPosition = this._cm.doc.length;
        }
        const position = lastPosition;
        let found = Utils.findNext(this._matches, position, 0, this._matches.length - 1);
        if (found === null) {
            // Don't loop
            return reverse ? this._matches.length - 1 : null;
        }
        if (reverse) {
            found -= 1;
            if (found < 0) {
                // Don't loop
                return null;
            }
        }
        return found;
    }
}
/**
 * Helpers namespace
 */
var Utils;
(function (Utils) {
    /**
     * Find the closest match at `position` just after it.
     *
     * #### Notes
     * Search is done using a binary search algorithm
     *
     * @param matches List of matches
     * @param position Searched position
     * @param lowerBound Lower range index
     * @param higherBound High range index
     * @returns The next match or null if none exists
     */
    function findNext(matches, position, lowerBound = 0, higherBound = Infinity) {
        higherBound = Math.min(matches.length - 1, higherBound);
        while (lowerBound <= higherBound) {
            let middle = Math.floor(0.5 * (lowerBound + higherBound));
            const currentPosition = matches[middle].position;
            if (currentPosition < position) {
                lowerBound = middle + 1;
                if (lowerBound < matches.length &&
                    matches[lowerBound].position > position) {
                    return lowerBound;
                }
            }
            else if (currentPosition > position) {
                higherBound = middle - 1;
                if (higherBound > 0 && matches[higherBound].position < position) {
                    return middle;
                }
            }
            else {
                return middle;
            }
        }
        // Next could be the first item
        const first = lowerBound > 0 ? lowerBound - 1 : 0;
        const match = matches[first];
        return match.position >= position ? first : null;
    }
    Utils.findNext = findNext;
})(Utils || (Utils = {}));

;// CONCATENATED MODULE: ../packages/codemirror/lib/token.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

/**
 * Editor language token.
 */
const IEditorExtensionRegistry = new coreutils_dist_index_js_.Token('@jupyterlab/codemirror:IEditorExtensionRegistry', `A registry for CodeMirror extension factories.`);
/**
 * Editor language token.
 */
const IEditorLanguageRegistry = new coreutils_dist_index_js_.Token('@jupyterlab/codemirror:IEditorLanguageRegistry', 'A registry for CodeMirror languages.');
/**
 * Editor theme token.
 */
const IEditorThemeRegistry = new coreutils_dist_index_js_.Token('@jupyterlab/codemirror:IEditorThemeRegistry', 'A registry for CodeMirror theme.');

;// CONCATENATED MODULE: ../packages/codemirror/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module codemirror
 */












/***/ })

}]);
//# sourceMappingURL=4910.4baa9774f1146d1dea3c.js.map?v=4baa9774f1146d1dea3c