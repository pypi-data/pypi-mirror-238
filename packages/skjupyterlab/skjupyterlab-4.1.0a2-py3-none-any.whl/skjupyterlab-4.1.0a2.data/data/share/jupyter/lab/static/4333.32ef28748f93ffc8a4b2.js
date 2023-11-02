"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[4333],{

/***/ 74333:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "ITableOfContentsRegistry": () => (/* reexport */ ITableOfContentsRegistry),
  "ITableOfContentsTracker": () => (/* reexport */ ITableOfContentsTracker),
  "TableOfContents": () => (/* reexport */ TableOfContents),
  "TableOfContentsFactory": () => (/* reexport */ TableOfContentsFactory),
  "TableOfContentsItem": () => (/* reexport */ TableOfContentsItem),
  "TableOfContentsModel": () => (/* reexport */ TableOfContentsModel),
  "TableOfContentsPanel": () => (/* reexport */ TableOfContentsPanel),
  "TableOfContentsRegistry": () => (/* reexport */ TableOfContentsRegistry),
  "TableOfContentsTracker": () => (/* reexport */ TableOfContentsTracker),
  "TableOfContentsTree": () => (/* reexport */ TableOfContentsTree),
  "TableOfContentsUtils": () => (/* reexport */ utils_namespaceObject),
  "TableOfContentsWidget": () => (/* reexport */ TableOfContentsWidget)
});

// NAMESPACE OBJECT: ../packages/toc/lib/utils/markdown.js
var markdown_namespaceObject = {};
__webpack_require__.r(markdown_namespaceObject);
__webpack_require__.d(markdown_namespaceObject, {
  "getHeadingId": () => (getHeadingId),
  "getHeadings": () => (getHeadings),
  "isMarkdown": () => (isMarkdown)
});

// NAMESPACE OBJECT: ../packages/toc/lib/utils/index.js
var utils_namespaceObject = {};
__webpack_require__.r(utils_namespaceObject);
__webpack_require__.d(utils_namespaceObject, {
  "Markdown": () => (markdown_namespaceObject),
  "NUMBERING_CLASS": () => (NUMBERING_CLASS),
  "addPrefix": () => (addPrefix),
  "clearNumbering": () => (clearNumbering),
  "filterHeadings": () => (filterHeadings),
  "getHTMLHeadings": () => (getHTMLHeadings),
  "getPrefix": () => (getPrefix),
  "isHTML": () => (isHTML)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var index_js_ = __webpack_require__(78254);
;// CONCATENATED MODULE: ../packages/toc/lib/factory.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * Timeout for throttling ToC rendering following model changes.
 *
 * @private
 */
const RENDER_TIMEOUT = 1000;
/**
 * Abstract table of contents model factory for IDocumentWidget.
 */
class TableOfContentsFactory {
    /**
     * Constructor
     *
     * @param tracker Widget tracker
     */
    constructor(tracker) {
        this.tracker = tracker;
    }
    /**
     * Whether the factory can handle the widget or not.
     *
     * @param widget - widget
     * @returns boolean indicating a ToC can be generated
     */
    isApplicable(widget) {
        if (!this.tracker.has(widget)) {
            return false;
        }
        return true;
    }
    /**
     * Create a new table of contents model for the widget
     *
     * @param widget - widget
     * @param configuration - Table of contents configuration
     * @returns The table of contents model
     */
    createNew(widget, configuration) {
        const model = this._createNew(widget, configuration);
        const context = widget.context;
        const updateHeadings = () => {
            model.refresh().catch(reason => {
                console.error('Failed to update the table of contents.', reason);
            });
        };
        const monitor = new index_js_.ActivityMonitor({
            signal: context.model.contentChanged,
            timeout: RENDER_TIMEOUT
        });
        monitor.activityStopped.connect(updateHeadings);
        const updateTitle = () => {
            model.title = index_js_.PathExt.basename(context.localPath);
        };
        context.pathChanged.connect(updateTitle);
        context.ready
            .then(() => {
            updateTitle();
            updateHeadings();
        })
            .catch(reason => {
            console.error(`Failed to initiate headings for ${context.localPath}.`);
        });
        widget.disposed.connect(() => {
            monitor.activityStopped.disconnect(updateHeadings);
            context.pathChanged.disconnect(updateTitle);
        });
        return model;
    }
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(30205);
;// CONCATENATED MODULE: ../packages/toc/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * Table of contents registry token.
 */
const ITableOfContentsRegistry = new dist_index_js_.Token('@jupyterlab/toc:ITableOfContentsRegistry', 'A service to register table of content factory.');
/**
 * Table of contents tracker token.
 */
const ITableOfContentsTracker = new dist_index_js_.Token('@jupyterlab/toc:ITableOfContentsTracker', 'A widget tracker for table of contents.');
/**
 * Namespace for table of contents interface
 */
var TableOfContents;
(function (TableOfContents) {
    /**
     * Default table of content configuration
     */
    TableOfContents.defaultConfig = {
        baseNumbering: 1,
        maximalDepth: 4,
        numberingH1: true,
        numberHeaders: false,
        includeOutput: true,
        syncCollapseState: false
    };
})(TableOfContents || (TableOfContents = {}));

;// CONCATENATED MODULE: ../packages/toc/lib/model.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * Abstract table of contents model.
 */
class TableOfContentsModel extends lib_index_js_.VDomModel {
    /**
     * Constructor
     *
     * @param widget The widget to search in
     * @param configuration Default model configuration
     */
    constructor(widget, configuration) {
        super();
        this.widget = widget;
        this._activeHeading = null;
        this._activeHeadingChanged = new index_es6_js_.Signal(this);
        this._collapseChanged = new index_es6_js_.Signal(this);
        this._configuration = configuration !== null && configuration !== void 0 ? configuration : { ...TableOfContents.defaultConfig };
        this._headings = new Array();
        this._headingsChanged = new index_es6_js_.Signal(this);
        this._isActive = false;
        this._isRefreshing = false;
        this._needsRefreshing = false;
    }
    /**
     * Current active entry.
     *
     * @returns table of contents active entry
     */
    get activeHeading() {
        return this._activeHeading;
    }
    /**
     * Signal emitted when the active heading changes.
     */
    get activeHeadingChanged() {
        return this._activeHeadingChanged;
    }
    /**
     * Signal emitted when a table of content section collapse state changes.
     */
    get collapseChanged() {
        return this._collapseChanged;
    }
    /**
     * Model configuration
     */
    get configuration() {
        return this._configuration;
    }
    /**
     * List of headings.
     *
     * @returns table of contents list of headings
     */
    get headings() {
        return this._headings;
    }
    /**
     * Signal emitted when the headings changes.
     */
    get headingsChanged() {
        return this._headingsChanged;
    }
    /**
     * Whether the model is active or not.
     *
     * #### Notes
     * An active model means it is displayed in the table of contents.
     * This can be used by subclass to limit updating the headings.
     */
    get isActive() {
        return this._isActive;
    }
    set isActive(v) {
        this._isActive = v;
        // Refresh on activation expect if it is always active
        //  => a ToC model is always active e.g. when displaying numbering in the document
        if (this._isActive && !this.isAlwaysActive) {
            this.refresh().catch(reason => {
                console.error('Failed to refresh ToC model.', reason);
            });
        }
    }
    /**
     * Whether the model gets updated even if the table of contents panel
     * is hidden or not.
     *
     * #### Notes
     * For example, ToC models use to add title numbering will
     * set this to true.
     */
    get isAlwaysActive() {
        return false;
    }
    /**
     * List of configuration options supported by the model.
     */
    get supportedOptions() {
        return ['maximalDepth'];
    }
    /**
     * Document title
     */
    get title() {
        return this._title;
    }
    set title(v) {
        if (v !== this._title) {
            this._title = v;
            this.stateChanged.emit();
        }
    }
    /**
     * Refresh the headings list.
     */
    async refresh() {
        if (this._isRefreshing) {
            // Schedule a refresh if one is in progress
            this._needsRefreshing = true;
            return Promise.resolve();
        }
        this._isRefreshing = true;
        try {
            const newHeadings = await this.getHeadings();
            if (this._needsRefreshing) {
                this._needsRefreshing = false;
                this._isRefreshing = false;
                return this.refresh();
            }
            if (newHeadings &&
                !Private.areHeadingsEqual(newHeadings, this._headings)) {
                this._headings = newHeadings;
                this.stateChanged.emit();
                this._headingsChanged.emit();
            }
        }
        finally {
            this._isRefreshing = false;
        }
    }
    /**
     * Set a new active heading.
     *
     * @param heading The new active heading
     * @param emitSignal Whether to emit the activeHeadingChanged signal or not.
     */
    setActiveHeading(heading, emitSignal = true) {
        if (this._activeHeading !== heading) {
            this._activeHeading = heading;
            this.stateChanged.emit();
            if (emitSignal) {
                this._activeHeadingChanged.emit(heading);
            }
        }
    }
    /**
     * Model configuration setter.
     *
     * @param c New configuration
     */
    setConfiguration(c) {
        const newConfiguration = { ...this._configuration, ...c };
        if (!dist_index_js_.JSONExt.deepEqual(this._configuration, newConfiguration)) {
            this._configuration = newConfiguration;
            this.refresh().catch(reason => {
                console.error('Failed to update the table of contents.', reason);
            });
        }
    }
    /**
     * Callback on heading collapse.
     *
     * @param options.heading The heading to change state (all headings if not provided)
     * @param options.collapsed The new collapsed status (toggle existing status if not provided)
     */
    toggleCollapse(options) {
        var _a, _b;
        if (options.heading) {
            options.heading.collapsed =
                (_a = options.collapsed) !== null && _a !== void 0 ? _a : !options.heading.collapsed;
            this.stateChanged.emit();
            this._collapseChanged.emit(options.heading);
        }
        else {
            // Use the provided state or collapsed all except if all are collapsed
            const newState = (_b = options.collapsed) !== null && _b !== void 0 ? _b : !this.headings.some(h => { var _a; return !((_a = h.collapsed) !== null && _a !== void 0 ? _a : false); });
            this.headings.forEach(h => (h.collapsed = newState));
            this.stateChanged.emit();
            this._collapseChanged.emit(null);
        }
    }
}
/**
 * Private functions namespace
 */
var Private;
(function (Private) {
    /**
     * Test if two list of headings are equal or not.
     *
     * @param headings1 First list of headings
     * @param headings2 Second list of headings
     * @returns Whether the array are identical or not.
     */
    function areHeadingsEqual(headings1, headings2) {
        if (headings1.length === headings2.length) {
            for (let i = 0; i < headings1.length; i++) {
                if (headings1[i].level !== headings2[i].level ||
                    headings1[i].text !== headings2[i].text ||
                    headings1[i].prefix !== headings2[i].prefix) {
                    return false;
                }
            }
            return true;
        }
        return false;
    }
    Private.areHeadingsEqual = areHeadingsEqual;
})(Private || (Private = {}));

// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(72234);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
;// CONCATENATED MODULE: ../packages/toc/lib/tocitem.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * React component for a table of contents entry.
 */
class TableOfContentsItem extends react_index_js_.PureComponent {
    /**
     * Renders a table of contents entry.
     *
     * @returns rendered entry
     */
    render() {
        const { children, isActive, heading, onCollapse, onMouseDown } = this.props;
        return (react_index_js_.createElement("li", { className: "jp-tocItem" },
            react_index_js_.createElement("div", { className: `jp-tocItem-heading ${isActive ? 'jp-tocItem-active' : ''}`, onMouseDown: (event) => {
                    // React only on deepest item
                    if (!event.defaultPrevented) {
                        event.preventDefault();
                        onMouseDown(heading);
                    }
                } },
                react_index_js_.createElement("button", { className: "jp-tocItem-collapser", onClick: (event) => {
                        event.preventDefault();
                        onCollapse(heading);
                    }, style: { visibility: children ? 'visible' : 'hidden' } }, heading.collapsed ? (react_index_js_.createElement(lib_index_js_.caretRightIcon.react, { tag: "span", width: "20px" })) : (react_index_js_.createElement(lib_index_js_.caretDownIcon.react, { tag: "span", width: "20px" }))),
                react_index_js_.createElement("span", { className: "jp-tocItem-content", title: heading.text, ...heading.dataset },
                    heading.prefix,
                    heading.text)),
            children && !heading.collapsed && react_index_js_.createElement("ol", null, children)));
    }
}

;// CONCATENATED MODULE: ../packages/toc/lib/toctree.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * React component for a table of contents tree.
 */
class TableOfContentsTree extends react_index_js_.PureComponent {
    /**
     * Renders a table of contents tree.
     */
    render() {
        const { documentType } = this.props;
        return (react_index_js_.createElement("ol", { className: "jp-TableOfContents-content", ...{ 'data-document-type': documentType } }, this.buildTree()));
    }
    /**
     * Convert the flat headings list to a nested tree list
     */
    buildTree() {
        if (this.props.headings.length === 0) {
            return [];
        }
        const buildOneTree = (currentIndex) => {
            const items = this.props.headings;
            const children = new Array();
            const current = items[currentIndex];
            let nextCandidateIndex = currentIndex + 1;
            while (nextCandidateIndex < items.length) {
                const candidateItem = items[nextCandidateIndex];
                if (candidateItem.level <= current.level) {
                    break;
                }
                const [child, nextIndex] = buildOneTree(nextCandidateIndex);
                children.push(child);
                nextCandidateIndex = nextIndex;
            }
            const currentTree = (react_index_js_.createElement(TableOfContentsItem, { key: `${current.level}-${currentIndex}-${current.text}`, isActive: !!this.props.activeHeading && current === this.props.activeHeading, heading: current, onMouseDown: this.props.setActiveHeading, onCollapse: this.props.onCollapseChange }, children.length ? children : null));
            return [currentTree, nextCandidateIndex];
        };
        const trees = new Array();
        let currentIndex = 0;
        while (currentIndex < this.props.headings.length) {
            const [tree, nextIndex] = buildOneTree(currentIndex);
            trees.push(tree);
            currentIndex = nextIndex;
        }
        return trees;
    }
}

;// CONCATENATED MODULE: ../packages/toc/lib/treeview.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * Table of contents widget.
 */
class TableOfContentsWidget extends lib_index_js_.VDomRenderer {
    /**
     * Constructor
     *
     * @param options Widget options
     */
    constructor(options) {
        super(options.model);
        this._placeholderHeadline = options.placeholderHeadline;
        this._placeholderText = options.placeholderText;
    }
    /**
     * Render the content of this widget using the virtual DOM.
     *
     * This method will be called anytime the widget needs to be rendered, which
     * includes layout triggered rendering.
     */
    render() {
        if (!this.model || this.model.headings.length === 0) {
            return (react_index_js_.createElement("div", { className: "jp-TableOfContents-placeholder" },
                react_index_js_.createElement("div", { className: "jp-TableOfContents-placeholderContent" },
                    react_index_js_.createElement("h3", null, this._placeholderHeadline),
                    react_index_js_.createElement("p", null, this._placeholderText))));
        }
        return (react_index_js_.createElement(TableOfContentsTree, { activeHeading: this.model.activeHeading, documentType: this.model.documentType, headings: this.model.headings, onCollapseChange: (heading) => {
                this.model.toggleCollapse({ heading });
            }, setActiveHeading: (heading) => {
                this.model.setActiveHeading(heading);
            } }));
    }
}

;// CONCATENATED MODULE: ../packages/toc/lib/panel.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */



/**
 * Table of contents sidebar panel.
 */
class TableOfContentsPanel extends lib_index_js_.SidePanel {
    /**
     * Constructor
     *
     * @param translator - Translator tool
     */
    constructor(translator) {
        super({ content: new dist_index_es6_js_.Panel(), translator });
        this._model = null;
        this.addClass('jp-TableOfContents');
        this._title = new panel_Private.Header(this._trans.__('Table of Contents'));
        this.header.addWidget(this._title);
        this._treeview = new TableOfContentsWidget({
            placeholderHeadline: this._trans.__('No Headings'),
            placeholderText: this._trans.__('The table of contents shows headings in notebooks and supported files.')
        });
        this._treeview.addClass('jp-TableOfContents-tree');
        this.content.addWidget(this._treeview);
    }
    /**
     * Get the current model.
     */
    get model() {
        return this._model;
    }
    set model(newValue) {
        var _a, _b;
        if (this._model !== newValue) {
            (_a = this._model) === null || _a === void 0 ? void 0 : _a.stateChanged.disconnect(this._onTitleChanged, this);
            this._model = newValue;
            if (this._model) {
                this._model.isActive = this.isVisible;
            }
            (_b = this._model) === null || _b === void 0 ? void 0 : _b.stateChanged.connect(this._onTitleChanged, this);
            this._onTitleChanged();
            this._treeview.model = this._model;
        }
    }
    onAfterHide(msg) {
        super.onAfterHide(msg);
        if (this._model) {
            this._model.isActive = false;
        }
    }
    onBeforeShow(msg) {
        super.onBeforeShow(msg);
        if (this._model) {
            this._model.isActive = true;
        }
    }
    _onTitleChanged() {
        var _a, _b;
        this._title.setTitle((_b = (_a = this._model) === null || _a === void 0 ? void 0 : _a.title) !== null && _b !== void 0 ? _b : this._trans.__('Table of Contents'));
    }
}
/**
 * Private helpers namespace
 */
var panel_Private;
(function (Private) {
    /**
     * Panel header
     */
    class Header extends dist_index_es6_js_.Widget {
        /**
         * Constructor
         *
         * @param title - Title text
         */
        constructor(title) {
            const node = document.createElement('h2');
            node.textContent = title;
            node.classList.add('jp-text-truncated');
            super({ node });
            this._title = node;
        }
        /**
         * Set the header title.
         */
        setTitle(title) {
            this._title.textContent = title;
        }
    }
    Private.Header = Header;
})(panel_Private || (panel_Private = {}));

// EXTERNAL MODULE: consume shared module (default) @lumino/disposable@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/disposable/dist/index.es6.js)
var disposable_dist_index_es6_js_ = __webpack_require__(78612);
;// CONCATENATED MODULE: ../packages/toc/lib/registry.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * Class for registering table of contents generators.
 */
class TableOfContentsRegistry {
    constructor() {
        this._generators = new Map();
        this._idCounter = 0;
    }
    /**
     * Finds a table of contents model for a widget.
     *
     * ## Notes
     *
     * -   If unable to find a table of contents model, the method return `undefined`.
     *
     * @param widget - widget
     * @param configuration - Default model configuration
     * @returns Table of contents model
     */
    getModel(widget, configuration) {
        for (const generator of this._generators.values()) {
            if (generator.isApplicable(widget)) {
                return generator.createNew(widget, configuration);
            }
        }
    }
    /**
     * Adds a table of contents generator to the registry.
     *
     * @param generator - table of contents generator
     */
    add(generator) {
        const id = this._idCounter++;
        this._generators.set(id, generator);
        return new disposable_dist_index_es6_js_.DisposableDelegate(() => {
            this._generators.delete(id);
        });
    }
}

;// CONCATENATED MODULE: ../packages/toc/lib/tracker.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * Table of contents tracker
 */
class TableOfContentsTracker {
    /**
     * Constructor
     */
    constructor() {
        this.modelMapping = new WeakMap();
    }
    /**
     * Track a given model.
     *
     * @param widget Widget
     * @param model Table of contents model
     */
    add(widget, model) {
        this.modelMapping.set(widget, model);
    }
    /**
     * Get the table of contents model associated with a given widget.
     *
     * @param widget Widget
     * @returns The table of contents model
     */
    get(widget) {
        const model = this.modelMapping.get(widget);
        return !model || model.isDisposed ? null : model;
    }
}

;// CONCATENATED MODULE: ../packages/toc/lib/utils/common.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * Class used to mark numbering prefix for headings in a document.
 */
const NUMBERING_CLASS = 'numbering-entry';
/**
 * Filter headings for table of contents and compute associated prefix
 *
 * @param headings Headings to process
 * @param options Options
 * @param initialLevels Initial levels for prefix computation
 * @returns Extracted headings
 */
function filterHeadings(headings, options, initialLevels = []) {
    const config = {
        ...TableOfContents.defaultConfig,
        ...options
    };
    const levels = initialLevels;
    let previousLevel = levels.length;
    const filteredHeadings = new Array();
    for (const heading of headings) {
        if (heading.skip) {
            continue;
        }
        const level = heading.level;
        if (level > 0 && level <= config.maximalDepth) {
            const prefix = getPrefix(level, previousLevel, levels, config);
            previousLevel = level;
            filteredHeadings.push({
                ...heading,
                prefix
            });
        }
    }
    return filteredHeadings;
}
/**
 * Returns whether a MIME type corresponds to either HTML.
 *
 * @param mime - MIME type string
 * @returns boolean indicating whether a provided MIME type corresponds to either HTML
 *
 * @example
 * const bool = isHTML('text/html');
 * // returns true
 *
 * @example
 * const bool = isHTML('text/plain');
 * // returns false
 */
function isHTML(mime) {
    return mime === 'text/html';
}
/**
 * Parse a HTML string for headings.
 *
 * ### Notes
 * The html string is not sanitized - use with caution
 *
 * @param html HTML string to parse
 * @param force Whether to ignore HTML headings with class jp-toc-ignore and tocSkip or not
 * @returns Extracted headings
 */
function getHTMLHeadings(html, force = true) {
    var _a;
    const container = document.createElement('div');
    container.innerHTML = html;
    const headings = new Array();
    const headers = container.querySelectorAll('h1, h2, h3, h4, h5, h6');
    for (const h of headers) {
        const level = parseInt(h.tagName[1], 10);
        headings.push({
            text: (_a = h.textContent) !== null && _a !== void 0 ? _a : '',
            level,
            id: h === null || h === void 0 ? void 0 : h.getAttribute('id'),
            skip: h.classList.contains('jp-toc-ignore') || h.classList.contains('tocSkip')
        });
    }
    return headings;
}
/**
 * Add an heading prefix to a HTML node.
 *
 * @param container HTML node containing the heading
 * @param selector Heading selector
 * @param prefix Title prefix to add
 * @returns The modified HTML element
 */
function addPrefix(container, selector, prefix) {
    let element = container.querySelector(selector);
    if (!element) {
        return null;
    }
    if (!element.querySelector(`span.${NUMBERING_CLASS}`)) {
        addNumbering(element, prefix);
    }
    else {
        // There are likely multiple elements with the same selector
        //  => use the first one without prefix
        const allElements = container.querySelectorAll(selector);
        for (const el of allElements) {
            if (!el.querySelector(`span.${NUMBERING_CLASS}`)) {
                element = el;
                addNumbering(el, prefix);
                break;
            }
        }
    }
    return element;
}
/**
 * Update the levels and create the numbering prefix
 *
 * @param level Current level
 * @param previousLevel Previous level
 * @param levels Levels list
 * @param options Options
 * @returns The numbering prefix
 */
function getPrefix(level, previousLevel, levels, options) {
    const { baseNumbering, numberingH1, numberHeaders } = options;
    let prefix = '';
    if (numberHeaders) {
        const highestLevel = numberingH1 ? 1 : 2;
        if (level > previousLevel) {
            // Initialize the new levels
            for (let l = previousLevel; l < level - 1; l++) {
                levels[l] = 0;
            }
            levels[level - 1] = level === highestLevel ? baseNumbering : 1;
        }
        else {
            // Increment the current level
            levels[level - 1] += 1;
            // Drop higher levels
            if (level < previousLevel) {
                levels.splice(level);
            }
        }
        // If the header list skips some level, replace missing elements by 0
        if (numberingH1) {
            prefix = levels.map(level => level !== null && level !== void 0 ? level : 0).join('.') + '. ';
        }
        else {
            if (levels.length > 1) {
                prefix =
                    levels
                        .slice(1)
                        .map(level => level !== null && level !== void 0 ? level : 0)
                        .join('.') + '. ';
            }
        }
    }
    return prefix;
}
/**
 * Add a numbering prefix to a HTML element.
 *
 * @param el HTML element
 * @param numbering Numbering prefix to add
 */
function addNumbering(el, numbering) {
    el.insertAdjacentHTML('afterbegin', `<span class="${NUMBERING_CLASS}">${numbering}</span>`);
}
/**
 * Remove all numbering nodes from element
 * @param element Node to clear
 */
function clearNumbering(element) {
    element === null || element === void 0 ? void 0 : element.querySelectorAll(`span.${NUMBERING_CLASS}`).forEach(el => {
        el.remove();
    });
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/rendermime@~4.1.0-alpha.2 (singleton) (fallback: ../packages/rendermime/lib/index.js)
var rendermime_lib_index_js_ = __webpack_require__(66866);
;// CONCATENATED MODULE: ../packages/toc/lib/utils/markdown.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * Build the heading html id.
 *
 * @param raw Raw markdown heading
 * @param level Heading level
 */
async function getHeadingId(parser, raw, level) {
    try {
        const innerHTML = await parser.render(raw);
        if (!innerHTML) {
            return null;
        }
        const container = document.createElement('div');
        container.innerHTML = innerHTML;
        const header = container.querySelector(`h${level}`);
        if (!header) {
            return null;
        }
        return rendermime_lib_index_js_.renderMarkdown.createHeaderId(header);
    }
    catch (reason) {
        console.error('Failed to parse a heading.', reason);
    }
    return null;
}
/**
 * Parses the provided string and returns a list of headings.
 *
 * @param text - Input text
 * @returns List of headings
 */
function getHeadings(text) {
    // Split the text into lines:
    const lines = text.split('\n');
    // Iterate over the lines to get the header level and text for each line:
    const headings = new Array();
    let isCodeBlock;
    let lineIdx = 0;
    // Don't check for Markdown headings if in a YAML frontmatter block.
    // We can only start a frontmatter block on the first line of the file.
    // At other positions in a markdown file, '---' represents a horizontal rule.
    if (lines[lineIdx] === '---') {
        // Search for another '---' and treat that as the end of the frontmatter.
        // If we don't find one, treat the file as containing no frontmatter.
        for (let frontmatterEndLineIdx = lineIdx + 1; frontmatterEndLineIdx < lines.length; frontmatterEndLineIdx++) {
            if (lines[frontmatterEndLineIdx] === '---') {
                lineIdx = frontmatterEndLineIdx + 1;
                break;
            }
        }
    }
    for (; lineIdx < lines.length; lineIdx++) {
        const line = lines[lineIdx];
        if (line === '') {
            // Bail early
            continue;
        }
        // Don't check for Markdown headings if in a code block
        if (line.startsWith('```')) {
            isCodeBlock = !isCodeBlock;
        }
        if (isCodeBlock) {
            continue;
        }
        const heading = parseHeading(line, lines[lineIdx + 1]); // append the next line to capture alternative style Markdown headings
        if (heading) {
            headings.push({
                ...heading,
                line: lineIdx
            });
        }
    }
    return headings;
}
const MARKDOWN_MIME_TYPE = [
    'text/x-ipythongfm',
    'text/x-markdown',
    'text/x-gfm',
    'text/markdown'
];
/**
 * Returns whether a MIME type corresponds to a Markdown flavor.
 *
 * @param mime - MIME type string
 * @returns boolean indicating whether a provided MIME type corresponds to a Markdown flavor
 *
 * @example
 * const bool = isMarkdown('text/markdown');
 * // returns true
 *
 * @example
 * const bool = isMarkdown('text/plain');
 * // returns false
 */
function isMarkdown(mime) {
    return MARKDOWN_MIME_TYPE.includes(mime);
}
/**
 * Parses a heading, if one exists, from a provided string.
 *
 * ## Notes
 *
 * -   Heading examples:
 *
 *     -   Markdown heading:
 *
 *         ```
 *         # Foo
 *         ```
 *
 *     -   Markdown heading (alternative style):
 *
 *         ```
 *         Foo
 *         ===
 *         ```
 *
 *         ```
 *         Foo
 *         ---
 *         ```
 *
 *     -   HTML heading:
 *
 *         ```
 *         <h3>Foo</h3>
 *         ```
 *
 * @private
 * @param line - Line to parse
 * @param nextLine - The line after the one to parse
 * @returns heading info
 *
 * @example
 * const out = parseHeading('### Foo\n');
 * // returns {'text': 'Foo', 'level': 3}
 *
 * @example
 * const out = parseHeading('Foo\n===\n');
 * // returns {'text': 'Foo', 'level': 1}
 *
 * @example
 * const out = parseHeading('<h4>Foo</h4>\n');
 * // returns {'text': 'Foo', 'level': 4}
 *
 * @example
 * const out = parseHeading('Foo');
 * // returns null
 */
function parseHeading(line, nextLine) {
    // Case: Markdown heading
    let match = line.match(/^([#]{1,6}) (.*)/);
    if (match) {
        return {
            text: cleanTitle(match[2]),
            level: match[1].length,
            raw: line,
            skip: skipHeading.test(match[0])
        };
    }
    // Case: Markdown heading (alternative style)
    if (nextLine) {
        match = nextLine.match(/^ {0,3}([=]{2,}|[-]{2,})\s*$/);
        if (match) {
            return {
                text: cleanTitle(line),
                level: match[1][0] === '=' ? 1 : 2,
                raw: [line, nextLine].join('\n'),
                skip: skipHeading.test(line)
            };
        }
    }
    // Case: HTML heading (WARNING: this is not particularly robust, as HTML headings can span multiple lines)
    match = line.match(/<h([1-6]).*>(.*)<\/h\1>/i);
    if (match) {
        return {
            text: match[2],
            level: parseInt(match[1], 10),
            skip: skipHeading.test(match[0]),
            raw: line
        };
    }
    return null;
}
function cleanTitle(heading) {
    // take special care to parse Markdown links into raw text
    return heading.replace(/\[(.+)\]\(.+\)/g, '$1');
}
/**
 * Ignore title with html tag with a class name equal to `jp-toc-ignore` or `tocSkip`
 */
const skipHeading = /<\w+\s(.*?\s)?class="(.*?\s)?(jp-toc-ignore|tocSkip)(\s.*?)?"(\s.*?)?>/;

;// CONCATENATED MODULE: ../packages/toc/lib/utils/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



;// CONCATENATED MODULE: ../packages/toc/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module toc
 */









// Namespace the utils



/***/ })

}]);
//# sourceMappingURL=4333.32ef28748f93ffc8a4b2.js.map?v=32ef28748f93ffc8a4b2