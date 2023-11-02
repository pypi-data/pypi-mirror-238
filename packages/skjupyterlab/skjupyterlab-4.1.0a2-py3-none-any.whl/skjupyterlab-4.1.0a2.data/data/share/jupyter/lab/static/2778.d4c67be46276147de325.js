"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[2778],{

/***/ 82778:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "FOUND_CLASSES": () => (/* reexport */ FOUND_CLASSES),
  "GenericSearchProvider": () => (/* reexport */ GenericSearchProvider),
  "HTMLSearchEngine": () => (/* reexport */ HTMLSearchEngine),
  "ISearchProviderRegistry": () => (/* reexport */ ISearchProviderRegistry),
  "SearchDocumentModel": () => (/* reexport */ SearchDocumentModel),
  "SearchDocumentView": () => (/* reexport */ SearchDocumentView),
  "SearchProvider": () => (/* reexport */ SearchProvider),
  "SearchProviderRegistry": () => (/* reexport */ SearchProviderRegistry),
  "TextSearchEngine": () => (/* reexport */ TextSearchEngine)
});

// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(72234);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(30205);
;// CONCATENATED MODULE: ../packages/documentsearch/lib/searchprovider.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * Abstract class implementing the search provider interface.
 */
class SearchProvider {
    /**
     * Constructor
     *
     * @param widget The widget to search in
     */
    constructor(widget) {
        this.widget = widget;
        this._stateChanged = new dist_index_es6_js_.Signal(this);
        this._filtersChanged = new dist_index_es6_js_.Signal(this);
        this._disposed = false;
    }
    /**
     * Signal indicating that something in the search has changed, so the UI should update
     */
    get stateChanged() {
        return this._stateChanged;
    }
    /**
     * Signal indicating that filter definition changed.
     */
    get filtersChanged() {
        return this._filtersChanged;
    }
    /**
     * The current index of the selected match.
     */
    get currentMatchIndex() {
        return null;
    }
    /**
     * Whether the search provider is disposed or not.
     */
    get isDisposed() {
        return this._disposed;
    }
    /**
     * The number of matches.
     */
    get matchesCount() {
        return null;
    }
    /**
     * Dispose of the resources held by the search provider.
     *
     * #### Notes
     * If the object's `dispose` method is called more than once, all
     * calls made after the first will be a no-op.
     *
     * #### Undefined Behavior
     * It is undefined behavior to use any functionality of the object
     * after it has been disposed unless otherwise explicitly noted.
     */
    dispose() {
        if (this._disposed) {
            return;
        }
        this._disposed = true;
        dist_index_es6_js_.Signal.clearData(this);
    }
    /**
     * Get an initial query value if applicable so that it can be entered
     * into the search box as an initial query
     *
     * @returns Initial value used to populate the search box.
     */
    getInitialQuery() {
        return '';
    }
    /**
     * Get the filters for the given provider.
     *
     * @returns The filters.
     *
     * ### Notes
     * TODO For now it only supports boolean filters (represented with checkboxes)
     */
    getFilters() {
        return {};
    }
    /**
     * Utility for copying the letter case from old to new text.
     */
    static preserveCase(oldText, newText) {
        if (oldText.toUpperCase() === oldText) {
            return newText.toUpperCase();
        }
        if (oldText.toLowerCase() === oldText) {
            return newText.toLowerCase();
        }
        if (toSentenceCase(oldText) === oldText) {
            return toSentenceCase(newText);
        }
        return newText;
    }
}
/**
 * Capitalise first letter of provided word.
 */
function toSentenceCase([first = '', ...suffix]) {
    return first.toUpperCase() + '' + suffix.join('').toLowerCase();
}

;// CONCATENATED MODULE: ../packages/documentsearch/lib/providers/genericsearchprovider.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


const FOUND_CLASSES = ['cm-string', 'cm-overlay', 'cm-searching'];
const SELECTED_CLASSES = ['CodeMirror-selectedtext'];
/**
 * HTML search engine
 */
class HTMLSearchEngine {
    /**
     * Search for a `query` in a DOM tree.
     *
     * @param query Regular expression to search
     * @param rootNode DOM root node to search in
     * @returns The list of matches
     */
    static search(query, rootNode) {
        if (!(rootNode instanceof Node)) {
            console.warn('Unable to search with HTMLSearchEngine the provided object.', rootNode);
            return Promise.resolve([]);
        }
        if (!query.global) {
            query = new RegExp(query.source, query.flags + 'g');
        }
        const matches = [];
        const walker = document.createTreeWalker(rootNode, NodeFilter.SHOW_TEXT, {
            acceptNode: node => {
                // Filter subtrees of UNSUPPORTED_ELEMENTS and nodes that
                // do not contain our search text
                let parentElement = node.parentElement;
                while (parentElement !== rootNode) {
                    if (parentElement.nodeName in HTMLSearchEngine.UNSUPPORTED_ELEMENTS) {
                        return NodeFilter.FILTER_REJECT;
                    }
                    parentElement = parentElement.parentElement;
                }
                return query.test(node.textContent)
                    ? NodeFilter.FILTER_ACCEPT
                    : NodeFilter.FILTER_REJECT;
            }
        });
        let node = null;
        while ((node = walker.nextNode()) !== null) {
            // Reset query index
            query.lastIndex = 0;
            let match = null;
            while ((match = query.exec(node.textContent)) !== null) {
                matches.push({
                    text: match[0],
                    position: match.index,
                    node: node
                });
            }
        }
        return Promise.resolve(matches);
    }
}
/**
 * We choose opt out as most node types should be searched (e.g. script).
 * Even nodes like <data>, could have textContent we care about.
 *
 * Note: nodeName is capitalized, so we do the same here
 */
HTMLSearchEngine.UNSUPPORTED_ELEMENTS = {
    // https://developer.mozilla.org/en-US/docs/Web/HTML/Element#Document_metadata
    BASE: true,
    HEAD: true,
    LINK: true,
    META: true,
    STYLE: true,
    TITLE: true,
    // https://developer.mozilla.org/en-US/docs/Web/HTML/Element#Sectioning_root
    BODY: true,
    // https://developer.mozilla.org/en-US/docs/Web/HTML/Element#Content_sectioning
    // https://developer.mozilla.org/en-US/docs/Web/HTML/Element#Text_content
    // https://developer.mozilla.org/en-US/docs/Web/HTML/Element#Inline_text_semantics
    // Above is searched
    // https://developer.mozilla.org/en-US/docs/Web/HTML/Element#Image_and_multimedia
    AREA: true,
    AUDIO: true,
    IMG: true,
    MAP: true,
    TRACK: true,
    VIDEO: true,
    // https://developer.mozilla.org/en-US/docs/Web/HTML/Element#Embedded_content
    APPLET: true,
    EMBED: true,
    IFRAME: true,
    NOEMBED: true,
    OBJECT: true,
    PARAM: true,
    PICTURE: true,
    SOURCE: true,
    // https://developer.mozilla.org/en-US/docs/Web/HTML/Element#Scripting
    CANVAS: true,
    NOSCRIPT: true,
    SCRIPT: true,
    // https://developer.mozilla.org/en-US/docs/Web/HTML/Element#Demarcating_edits
    // https://developer.mozilla.org/en-US/docs/Web/HTML/Element#Table_content
    // https://developer.mozilla.org/en-US/docs/Web/HTML/Element#Forms
    // https://developer.mozilla.org/en-US/docs/Web/HTML/Element#Interactive_elements
    // https://developer.mozilla.org/en-US/docs/Web/HTML/Element#Web_Components
    // Above is searched
    // Other:
    SVG: true
};

/**
 * Generic DOM tree search provider.
 */
class GenericSearchProvider extends SearchProvider {
    constructor() {
        super(...arguments);
        /**
         * Set to true if the widget under search is read-only, false
         * if it is editable.  Will be used to determine whether to show
         * the replace option.
         */
        this.isReadOnly = true;
        this._matches = [];
        this._mutationObserver = new MutationObserver(this._onWidgetChanged.bind(this));
        this._markNodes = new Array();
    }
    /**
     * Report whether or not this provider has the ability to search on the given object
     */
    static isApplicable(domain) {
        return domain instanceof index_es6_js_.Widget;
    }
    /**
     * Instantiate a generic search provider for the widget.
     *
     * #### Notes
     * The widget provided is always checked using `isApplicable` before calling
     * this factory.
     *
     * @param widget The widget to search on
     * @param registry The search provider registry
     * @param translator [optional] The translator object
     *
     * @returns The search provider on the widget
     */
    static createNew(widget, registry, translator) {
        return new GenericSearchProvider(widget);
    }
    /**
     * The current index of the selected match.
     */
    get currentMatchIndex() {
        return this._currentMatchIndex >= 0 ? this._currentMatchIndex : null;
    }
    /**
     * The current match
     */
    get currentMatch() {
        var _a;
        return (_a = this._matches[this._currentMatchIndex]) !== null && _a !== void 0 ? _a : null;
    }
    /**
     * The current matches
     */
    get matches() {
        // Ensure that no other fn can overwrite matches index property
        // We shallow clone each node
        return this._matches
            ? this._matches.map(m => Object.assign({}, m))
            : this._matches;
    }
    /**
     * The number of matches.
     */
    get matchesCount() {
        return this._matches.length;
    }
    /**
     * Clear currently highlighted match.
     */
    clearHighlight() {
        if (this._currentMatchIndex >= 0) {
            const hit = this._markNodes[this._currentMatchIndex];
            hit.classList.remove(...SELECTED_CLASSES);
        }
        this._currentMatchIndex = -1;
        return Promise.resolve();
    }
    /**
     * Dispose of the resources held by the search provider.
     *
     * #### Notes
     * If the object's `dispose` method is called more than once, all
     * calls made after the first will be a no-op.
     *
     * #### Undefined Behavior
     * It is undefined behavior to use any functionality of the object
     * after it has been disposed unless otherwise explicitly noted.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.endQuery().catch(reason => {
            console.error(`Failed to end search query.`, reason);
        });
        super.dispose();
    }
    /**
     * Move the current match indicator to the next match.
     *
     * @param loop Whether to loop within the matches list.
     *
     * @returns A promise that resolves once the action has completed.
     */
    async highlightNext(loop) {
        var _a;
        return (_a = this._highlightNext(false, loop !== null && loop !== void 0 ? loop : true)) !== null && _a !== void 0 ? _a : undefined;
    }
    /**
     * Move the current match indicator to the previous match.
     *
     * @param loop Whether to loop within the matches list.
     *
     * @returns A promise that resolves once the action has completed.
     */
    async highlightPrevious(loop) {
        var _a;
        return (_a = this._highlightNext(true, loop !== null && loop !== void 0 ? loop : true)) !== null && _a !== void 0 ? _a : undefined;
    }
    /**
     * Replace the currently selected match with the provided text
     *
     * @param newText The replacement text
     * @param loop Whether to loop within the matches list.
     *
     * @returns A promise that resolves with a boolean indicating whether a replace occurred.
     */
    async replaceCurrentMatch(newText, loop) {
        return Promise.resolve(false);
    }
    /**
     * Replace all matches in the notebook with the provided text
     *
     * @param newText The replacement text
     *
     * @returns A promise that resolves with a boolean indicating whether a replace occurred.
     */
    async replaceAllMatches(newText) {
        // This is read only, but we could loosen this in theory for input boxes...
        return Promise.resolve(false);
    }
    /**
     * Initialize the search using the provided options.  Should update the UI
     * to highlight all matches and "select" whatever the first match should be.
     *
     * @param query A RegExp to be use to perform the search
     * @param filters Filter parameters to pass to provider
     */
    async startQuery(query, filters = {}) {
        await this.endQuery();
        this._query = query;
        if (query === null) {
            return Promise.resolve();
        }
        const matches = await HTMLSearchEngine.search(query, this.widget.node);
        // Transform the DOM
        let nodeIdx = 0;
        while (nodeIdx < matches.length) {
            let activeNode = matches[nodeIdx].node;
            let parent = activeNode.parentNode;
            let subMatches = [matches[nodeIdx]];
            while (++nodeIdx < matches.length &&
                matches[nodeIdx].node === activeNode) {
                subMatches.unshift(matches[nodeIdx]);
            }
            const markedNodes = subMatches.map(match => {
                // TODO: support tspan for svg when svg support is added
                const markedNode = document.createElement('mark');
                markedNode.classList.add(...FOUND_CLASSES);
                markedNode.textContent = match.text;
                const newNode = activeNode.splitText(match.position);
                newNode.textContent = newNode.textContent.slice(match.text.length);
                parent.insertBefore(markedNode, newNode);
                return markedNode;
            });
            // Insert node in reverse order as we replace from last to first
            // to maintain match position.
            for (let i = markedNodes.length - 1; i >= 0; i--) {
                this._markNodes.push(markedNodes[i]);
            }
        }
        // Watch for future changes:
        this._mutationObserver.observe(this.widget.node, 
        // https://developer.mozilla.org/en-US/docs/Web/API/MutationObserverInit
        {
            attributes: false,
            characterData: true,
            childList: true,
            subtree: true
        });
        this._matches = matches;
    }
    /**
     * Clear the highlighted matches and any internal state.
     */
    async endQuery() {
        this._mutationObserver.disconnect();
        this._markNodes.forEach(el => {
            const parent = el.parentNode;
            parent.replaceChild(document.createTextNode(el.textContent), el);
            parent.normalize();
        });
        this._markNodes = [];
        this._matches = [];
        this._currentMatchIndex = -1;
    }
    _highlightNext(reverse, loop) {
        if (this._matches.length === 0) {
            return null;
        }
        if (this._currentMatchIndex === -1) {
            this._currentMatchIndex = reverse ? this.matches.length - 1 : 0;
        }
        else {
            const hit = this._markNodes[this._currentMatchIndex];
            hit.classList.remove(...SELECTED_CLASSES);
            this._currentMatchIndex = reverse
                ? this._currentMatchIndex - 1
                : this._currentMatchIndex + 1;
            if (loop &&
                (this._currentMatchIndex < 0 ||
                    this._currentMatchIndex >= this._matches.length)) {
                // Cheap way to make this a circular buffer
                this._currentMatchIndex =
                    (this._currentMatchIndex + this._matches.length) %
                        this._matches.length;
            }
        }
        if (this._currentMatchIndex >= 0 &&
            this._currentMatchIndex < this._matches.length) {
            const hit = this._markNodes[this._currentMatchIndex];
            hit.classList.add(...SELECTED_CLASSES);
            // If not in view, scroll just enough to see it
            if (!elementInViewport(hit)) {
                hit.scrollIntoView(reverse);
            }
            hit.focus();
            return this._matches[this._currentMatchIndex];
        }
        else {
            this._currentMatchIndex = -1;
            return null;
        }
    }
    async _onWidgetChanged(mutations, observer) {
        this._currentMatchIndex = -1;
        // This is typically cheap, but we do not control the rate of change or size of the output
        await this.startQuery(this._query);
        this._stateChanged.emit();
    }
}
function elementInViewport(el) {
    const boundingClientRect = el.getBoundingClientRect();
    return (boundingClientRect.top >= 0 &&
        boundingClientRect.bottom <=
            (window.innerHeight || document.documentElement.clientHeight) &&
        boundingClientRect.left >= 0 &&
        boundingClientRect.right <=
            (window.innerWidth || document.documentElement.clientWidth));
}

;// CONCATENATED MODULE: ../packages/documentsearch/lib/providers/textprovider.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * Search provider for text/plain
 */
const TextSearchEngine = {
    /**
     * Search for regular expression matches in a string.
     *
     * @param query Query regular expression
     * @param data String to look into
     * @returns List of matches
     */
    search(query, data) {
        // If data is not a string, try to JSON serialize the data.
        if (typeof data !== 'string') {
            try {
                data = JSON.stringify(data);
            }
            catch (reason) {
                console.warn('Unable to search with TextSearchEngine non-JSON serializable object.', reason, data);
                return Promise.resolve([]);
            }
        }
        if (!query.global) {
            query = new RegExp(query.source, query.flags + 'g');
        }
        const matches = new Array();
        let match = null;
        while ((match = query.exec(data)) !== null) {
            matches.push({
                text: match[0],
                position: match.index
            });
        }
        return Promise.resolve(matches);
    }
};

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/polling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/polling/dist/index.es6.js)
var polling_dist_index_es6_js_ = __webpack_require__(81967);
;// CONCATENATED MODULE: ../packages/documentsearch/lib/searchmodel.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * Search in a document model.
 */
class SearchDocumentModel extends index_js_.VDomModel {
    /**
     * Search document model
     * @param searchProvider Provider for the current document
     * @param searchDebounceTime Debounce search time
     */
    constructor(searchProvider, searchDebounceTime) {
        super();
        this.searchProvider = searchProvider;
        this._caseSensitive = false;
        this._disposed = new dist_index_es6_js_.Signal(this);
        this._parsingError = '';
        this._preserveCase = false;
        this._initialQuery = '';
        this._filters = {};
        this._replaceText = '';
        this._searchExpression = '';
        this._useRegex = false;
        this._wholeWords = false;
        this._filters = {};
        if (this.searchProvider.getFilters) {
            const filters = this.searchProvider.getFilters();
            for (const filter in filters) {
                this._filters[filter] = filters[filter].default;
            }
        }
        searchProvider.stateChanged.connect(this.refresh, this);
        this._searchDebouncer = new polling_dist_index_es6_js_.Debouncer(() => {
            this._updateSearch().catch(reason => {
                console.error('Failed to update search on document.', reason);
            });
        }, searchDebounceTime);
    }
    /**
     * Whether the search is case sensitive or not.
     */
    get caseSensitive() {
        return this._caseSensitive;
    }
    set caseSensitive(v) {
        if (this._caseSensitive !== v) {
            this._caseSensitive = v;
            this.stateChanged.emit();
            this.refresh();
        }
    }
    /**
     * Current highlighted match index.
     */
    get currentIndex() {
        return this.searchProvider.currentMatchIndex;
    }
    /**
     * A signal emitted when the object is disposed.
     */
    get disposed() {
        return this._disposed;
    }
    /**
     * Filter values.
     */
    get filters() {
        return this._filters;
    }
    /**
     * Filter definitions for the current provider.
     */
    get filtersDefinition() {
        var _a, _b, _c;
        return (_c = (_b = (_a = this.searchProvider).getFilters) === null || _b === void 0 ? void 0 : _b.call(_a)) !== null && _c !== void 0 ? _c : {};
    }
    /**
     * Filter definitions changed.
     */
    get filtersDefinitionChanged() {
        return this.searchProvider.filtersChanged || null;
    }
    /**
     * The initial query string.
     */
    get initialQuery() {
        return this._initialQuery;
    }
    set initialQuery(v) {
        if (v) {
            // Usually the value comes from user selection (set by search provider).
            this._initialQuery = v;
        }
        else {
            // If user selection is empty, we fall back to most recent value (if any).
            this._initialQuery = this._searchExpression;
        }
    }
    /**
     * Initial query as suggested by provider.
     *
     * A common choice is the text currently selected by the user.
     */
    get suggestedInitialQuery() {
        return this.searchProvider.getInitialQuery();
    }
    /**
     * Whether the selection includes a single item or multiple items;
     * this is used by the heuristic auto-enabling "search in selection" mode.
     *
     * Returns `undefined` if the provider does not expose this information.
     */
    get selectionState() {
        return this.searchProvider.getSelectionState
            ? this.searchProvider.getSelectionState()
            : undefined;
    }
    /**
     * Whether the document is read-only or not.
     */
    get isReadOnly() {
        return this.searchProvider.isReadOnly;
    }
    /**
     * Replace options support.
     */
    get replaceOptionsSupport() {
        return this.searchProvider.replaceOptionsSupport;
    }
    /**
     * Parsing regular expression error message.
     */
    get parsingError() {
        return this._parsingError;
    }
    /**
     * Whether to preserve case when replacing.
     */
    get preserveCase() {
        return this._preserveCase;
    }
    set preserveCase(v) {
        if (this._preserveCase !== v) {
            this._preserveCase = v;
            this.stateChanged.emit();
            this.refresh();
        }
    }
    /**
     * Replacement expression
     */
    get replaceText() {
        return this._replaceText;
    }
    set replaceText(v) {
        if (this._replaceText !== v) {
            this._replaceText = v;
            this.stateChanged.emit();
        }
    }
    /**
     * Search expression
     */
    get searchExpression() {
        return this._searchExpression;
    }
    set searchExpression(v) {
        if (this._searchExpression !== v) {
            this._searchExpression = v;
            this.stateChanged.emit();
            this.refresh();
        }
    }
    /**
     * Total number of matches.
     */
    get totalMatches() {
        return this.searchProvider.matchesCount;
    }
    /**
     * Whether to use regular expression or not.
     */
    get useRegex() {
        return this._useRegex;
    }
    set useRegex(v) {
        if (this._useRegex !== v) {
            this._useRegex = v;
            this.stateChanged.emit();
            this.refresh();
        }
    }
    /**
     * Whether to match whole words or not.
     */
    get wholeWords() {
        return this._wholeWords;
    }
    set wholeWords(v) {
        if (this._wholeWords !== v) {
            this._wholeWords = v;
            this.stateChanged.emit();
            this.refresh();
        }
    }
    /**
     * Dispose the model.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        if (this._searchExpression) {
            this.endQuery().catch(reason => {
                console.error(`Failed to end query '${this._searchExpression}.`, reason);
            });
        }
        this.searchProvider.stateChanged.disconnect(this.refresh, this);
        this._searchDebouncer.dispose();
        super.dispose();
    }
    /**
     * End the query.
     */
    async endQuery() {
        await this.searchProvider.endQuery();
        this.stateChanged.emit();
    }
    /**
     * Highlight the next match.
     */
    async highlightNext() {
        await this.searchProvider.highlightNext();
        // Emit state change as the index needs to be updated
        this.stateChanged.emit();
    }
    /**
     * Highlight the previous match
     */
    async highlightPrevious() {
        await this.searchProvider.highlightPrevious();
        // Emit state change as the index needs to be updated
        this.stateChanged.emit();
    }
    /**
     * Refresh search
     */
    refresh() {
        this._searchDebouncer.invoke().catch(reason => {
            console.error('Failed to invoke search document debouncer.', reason);
        });
    }
    /**
     * Replace all matches.
     */
    async replaceAllMatches() {
        await this.searchProvider.replaceAllMatches(this._replaceText, {
            preserveCase: this.preserveCase,
            regularExpression: this.useRegex
        });
        // Emit state change as the index needs to be updated
        this.stateChanged.emit();
    }
    /**
     * Replace the current match.
     */
    async replaceCurrentMatch() {
        await this.searchProvider.replaceCurrentMatch(this._replaceText, true, {
            preserveCase: this.preserveCase,
            regularExpression: this.useRegex
        });
        // Emit state change as the index needs to be updated
        this.stateChanged.emit();
    }
    /**
     * Set the value of a given filter.
     *
     * @param name Filter name
     * @param v Filter value
     */
    async setFilter(name, v) {
        if (this._filters[name] !== v) {
            if (this.searchProvider.validateFilter) {
                this._filters[name] = await this.searchProvider.validateFilter(name, v);
                // If the value was changed
                if (this._filters[name] === v) {
                    this.stateChanged.emit();
                    this.refresh();
                }
            }
            else {
                this._filters[name] = v;
                this.stateChanged.emit();
                this.refresh();
            }
        }
    }
    async _updateSearch() {
        if (this._parsingError) {
            this._parsingError = '';
            this.stateChanged.emit();
        }
        try {
            const query = this.searchExpression
                ? Private.parseQuery(this.searchExpression, this.caseSensitive, this.useRegex, this.wholeWords)
                : null;
            if (query) {
                await this.searchProvider.startQuery(query, this._filters);
                // Emit state change as the index needs to be updated
                this.stateChanged.emit();
            }
        }
        catch (reason) {
            this._parsingError = reason.toString();
            this.stateChanged.emit();
            console.error(`Failed to parse expression ${this.searchExpression}`, reason);
        }
    }
}
var Private;
(function (Private) {
    /**
     * Build the regular expression to use for searching.
     *
     * @param queryString Query string
     * @param caseSensitive Whether the search is case sensitive or not
     * @param regex Whether the expression is a regular expression
     * @returns The regular expression to use
     */
    function parseQuery(queryString, caseSensitive, regex, wholeWords) {
        const flag = caseSensitive ? 'gm' : 'gim';
        // escape regex characters in query if its a string search
        let queryText = regex
            ? queryString
            : queryString.replace(/[-[\]/{}()*+?.\\^$|]/g, '\\$&');
        if (wholeWords) {
            queryText = '\\b' + queryText + '\\b';
        }
        const ret = new RegExp(queryText, flag);
        // If the empty string is hit, the search logic will freeze the browser tab
        //  Trying /^/ or /$/ on the codemirror search demo, does not find anything.
        //  So this is a limitation of the editor.
        if (ret.test('')) {
            return null;
        }
        return ret;
    }
    Private.parseQuery = parseQuery;
})(Private || (Private = {}));

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @lumino/commands@^2.0.1 (singleton) (fallback: ../node_modules/@lumino/commands/dist/index.es6.js)
var commands_dist_index_es6_js_ = __webpack_require__(18955);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var apputils_lib_index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
;// CONCATENATED MODULE: ../packages/documentsearch/lib/searchview.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







const OVERLAY_CLASS = 'jp-DocumentSearch-overlay';
const OVERLAY_ROW_CLASS = 'jp-DocumentSearch-overlay-row';
const INPUT_CLASS = 'jp-DocumentSearch-input';
const INPUT_WRAPPER_CLASS = 'jp-DocumentSearch-input-wrapper';
const INPUT_BUTTON_CLASS_OFF = 'jp-DocumentSearch-input-button-off';
const INPUT_BUTTON_CLASS_ON = 'jp-DocumentSearch-input-button-on';
const INDEX_COUNTER_CLASS = 'jp-DocumentSearch-index-counter';
const UP_DOWN_BUTTON_WRAPPER_CLASS = 'jp-DocumentSearch-up-down-wrapper';
const UP_DOWN_BUTTON_CLASS = 'jp-DocumentSearch-up-down-button';
const FILTER_BUTTON_CLASS = 'jp-DocumentSearch-filter-button';
const FILTER_BUTTON_ENABLED_CLASS = 'jp-DocumentSearch-filter-button-enabled';
const REGEX_ERROR_CLASS = 'jp-DocumentSearch-regex-error';
const SEARCH_OPTIONS_CLASS = 'jp-DocumentSearch-search-options';
const SEARCH_FILTER_DISABLED_CLASS = 'jp-DocumentSearch-search-filter-disabled';
const SEARCH_FILTER_CLASS = 'jp-DocumentSearch-search-filter';
const REPLACE_BUTTON_CLASS = 'jp-DocumentSearch-replace-button';
const REPLACE_BUTTON_WRAPPER_CLASS = 'jp-DocumentSearch-replace-button-wrapper';
const REPLACE_WRAPPER_CLASS = 'jp-DocumentSearch-replace-wrapper-class';
const REPLACE_TOGGLE_CLASS = 'jp-DocumentSearch-replace-toggle';
const TOGGLE_WRAPPER = 'jp-DocumentSearch-toggle-wrapper';
const TOGGLE_PLACEHOLDER = 'jp-DocumentSearch-toggle-placeholder';
const BUTTON_CONTENT_CLASS = 'jp-DocumentSearch-button-content';
const BUTTON_WRAPPER_CLASS = 'jp-DocumentSearch-button-wrapper';
const SPACER_CLASS = 'jp-DocumentSearch-spacer';
function SearchInput(props) {
    const [rows, setRows] = (0,react_index_js_.useState)(1);
    const updateRows = (0,react_index_js_.useCallback)((event) => {
        var _a;
        const element = event
            ? event.target
            : (_a = props.inputRef) === null || _a === void 0 ? void 0 : _a.current;
        if (element) {
            setRows(element.value.split(/\n/).length);
        }
    }, []);
    (0,react_index_js_.useEffect)(() => {
        var _a, _b;
        // For large part, `focusSearchInput()` is responsible for focusing and
        // selecting the search input, however when `initialValue` changes, this
        // triggers React re-render to update `defaultValue` (implemented via `key`)
        // which means that `focusSearchInput` is no longer effective as it has
        // already fired before the re-render, hence we use this conditional effect.
        (_b = (_a = props.inputRef) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.select();
        // After any change to initial value we also want to update rows in case if
        // multi-line text was selected.
        updateRows();
    }, [props.initialValue]);
    return (react_index_js_.createElement("textarea", { placeholder: props.placeholder, className: INPUT_CLASS, rows: rows, onChange: e => {
            props.onChange(e);
            updateRows(e);
        }, onKeyDown: e => {
            props.onKeyDown(e);
            updateRows(e);
        }, 
        // Setting a key ensures that `defaultValue` will become updated
        // when the initial value changes.
        key: props.autoUpdate ? props.initialValue : null, tabIndex: 0, ref: props.inputRef, title: props.title, defaultValue: props.initialValue, autoFocus: props.autoFocus }));
}
function SearchEntry(props) {
    var _a;
    const trans = ((_a = props.translator) !== null && _a !== void 0 ? _a : lib_index_js_.nullTranslator).load('jupyterlab');
    const caseButtonToggleClass = (0,index_js_.classes)(props.caseSensitive ? INPUT_BUTTON_CLASS_ON : INPUT_BUTTON_CLASS_OFF, BUTTON_CONTENT_CLASS);
    const regexButtonToggleClass = (0,index_js_.classes)(props.useRegex ? INPUT_BUTTON_CLASS_ON : INPUT_BUTTON_CLASS_OFF, BUTTON_CONTENT_CLASS);
    const wordButtonToggleClass = (0,index_js_.classes)(props.wholeWords ? INPUT_BUTTON_CLASS_ON : INPUT_BUTTON_CLASS_OFF, BUTTON_CONTENT_CLASS);
    const wrapperClass = INPUT_WRAPPER_CLASS;
    return (react_index_js_.createElement("div", { className: wrapperClass },
        react_index_js_.createElement(SearchInput, { placeholder: trans.__('Find'), onChange: e => props.onChange(e), onKeyDown: e => props.onKeydown(e), inputRef: props.inputRef, initialValue: props.initialSearchText, title: trans.__('Find'), autoFocus: true, autoUpdate: true }),
        react_index_js_.createElement("button", { className: BUTTON_WRAPPER_CLASS, onClick: () => {
                props.onCaseSensitiveToggled();
            }, tabIndex: 0, title: trans.__('Match Case') },
            react_index_js_.createElement(index_js_.caseSensitiveIcon.react, { className: caseButtonToggleClass, tag: "span" })),
        react_index_js_.createElement("button", { className: BUTTON_WRAPPER_CLASS, onClick: () => props.onWordToggled(), tabIndex: 0, title: trans.__('Match Whole Word') },
            react_index_js_.createElement(index_js_.wordIcon.react, { className: wordButtonToggleClass, tag: "span" })),
        react_index_js_.createElement("button", { className: BUTTON_WRAPPER_CLASS, onClick: () => props.onRegexToggled(), tabIndex: 0, title: trans.__('Use Regular Expression') },
            react_index_js_.createElement(index_js_.regexIcon.react, { className: regexButtonToggleClass, tag: "span" }))));
}
function ReplaceEntry(props) {
    var _a, _b, _c;
    const trans = ((_a = props.translator) !== null && _a !== void 0 ? _a : lib_index_js_.nullTranslator).load('jupyterlab');
    const preserveCaseButtonToggleClass = (0,index_js_.classes)(props.preserveCase ? INPUT_BUTTON_CLASS_ON : INPUT_BUTTON_CLASS_OFF, BUTTON_CONTENT_CLASS);
    return (react_index_js_.createElement("div", { className: REPLACE_WRAPPER_CLASS },
        react_index_js_.createElement("div", { className: INPUT_WRAPPER_CLASS },
            react_index_js_.createElement(SearchInput, { placeholder: trans.__('Replace'), initialValue: (_b = props.replaceText) !== null && _b !== void 0 ? _b : '', onKeyDown: e => props.onReplaceKeydown(e), onChange: e => props.onChange(e), title: trans.__('Replace'), autoFocus: false, autoUpdate: false }),
            ((_c = props.replaceOptionsSupport) === null || _c === void 0 ? void 0 : _c.preserveCase) ? (react_index_js_.createElement("button", { className: BUTTON_WRAPPER_CLASS, onClick: () => props.onPreserveCaseToggled(), tabIndex: 0, title: trans.__('Preserve Case') },
                react_index_js_.createElement(index_js_.caseSensitiveIcon.react, { className: preserveCaseButtonToggleClass, tag: "span" }))) : null),
        react_index_js_.createElement("button", { className: REPLACE_BUTTON_WRAPPER_CLASS, onClick: () => props.onReplaceCurrent(), tabIndex: 0 },
            react_index_js_.createElement("span", { className: `${REPLACE_BUTTON_CLASS} ${BUTTON_CONTENT_CLASS}`, tabIndex: 0 }, trans.__('Replace'))),
        react_index_js_.createElement("button", { className: REPLACE_BUTTON_WRAPPER_CLASS, tabIndex: 0, onClick: () => props.onReplaceAll() },
            react_index_js_.createElement("span", { className: `${REPLACE_BUTTON_CLASS} ${BUTTON_CONTENT_CLASS}`, tabIndex: -1 }, trans.__('Replace All')))));
}
function UpDownButtons(props) {
    var _a, _b;
    const nextBinding = (_a = props.keyBindings) === null || _a === void 0 ? void 0 : _a.next;
    const prevBinding = (_b = props.keyBindings) === null || _b === void 0 ? void 0 : _b.previous;
    const nextKeys = nextBinding
        ? commands_dist_index_es6_js_.CommandRegistry.formatKeystroke(nextBinding.keys)
        : '';
    const prevKeys = prevBinding
        ? commands_dist_index_es6_js_.CommandRegistry.formatKeystroke(prevBinding.keys)
        : '';
    const prevShortcut = prevKeys ? ` (${prevKeys})` : '';
    const nextShortcut = nextKeys ? ` (${nextKeys})` : '';
    return (react_index_js_.createElement("div", { className: UP_DOWN_BUTTON_WRAPPER_CLASS },
        react_index_js_.createElement("button", { className: BUTTON_WRAPPER_CLASS, onClick: () => props.onHighlightPrevious(), tabIndex: 0, title: `${props.trans.__('Previous Match')}${prevShortcut}` },
            react_index_js_.createElement(index_js_.caretUpEmptyThinIcon.react, { className: (0,index_js_.classes)(UP_DOWN_BUTTON_CLASS, BUTTON_CONTENT_CLASS), tag: "span" })),
        react_index_js_.createElement("button", { className: BUTTON_WRAPPER_CLASS, onClick: () => props.onHighlightNext(), tabIndex: 0, title: `${props.trans.__('Next Match')}${nextShortcut}` },
            react_index_js_.createElement(index_js_.caretDownEmptyThinIcon.react, { className: (0,index_js_.classes)(UP_DOWN_BUTTON_CLASS, BUTTON_CONTENT_CLASS), tag: "span" }))));
}
function SearchIndices(props) {
    return (react_index_js_.createElement("div", { className: INDEX_COUNTER_CLASS }, props.totalMatches === 0
        ? '-/-'
        : `${props.currentIndex === null ? '-' : props.currentIndex + 1}/${props.totalMatches}`));
}
function FilterToggle(props) {
    let className = `${FILTER_BUTTON_CLASS} ${BUTTON_CONTENT_CLASS}`;
    if (props.visible) {
        className = `${className} ${FILTER_BUTTON_ENABLED_CLASS}`;
    }
    const icon = props.anyEnabled ? index_js_.filterDotIcon : index_js_.filterIcon;
    return (react_index_js_.createElement("button", { className: BUTTON_WRAPPER_CLASS, onClick: () => props.toggleVisible(), tabIndex: 0, title: props.visible
            ? props.trans.__('Hide Search Filters')
            : props.trans.__('Show Search Filters') },
        react_index_js_.createElement(icon.react, { className: className, tag: "span", height: "20px", width: "20px" })));
}
function FilterSelection(props) {
    return (react_index_js_.createElement("label", { className: props.isEnabled
            ? SEARCH_FILTER_CLASS
            : `${SEARCH_FILTER_CLASS} ${SEARCH_FILTER_DISABLED_CLASS}`, title: props.description },
        react_index_js_.createElement("input", { type: "checkbox", className: "jp-mod-styled", disabled: !props.isEnabled, checked: props.value, onChange: props.onToggle }),
        props.title));
}
class SearchOverlay extends react_index_js_.Component {
    constructor(props) {
        super(props);
        this.translator = props.translator || lib_index_js_.nullTranslator;
    }
    _onSearchChange(event) {
        const searchText = event.target.value;
        this.props.onSearchChanged(searchText);
    }
    _onSearchKeydown(event) {
        if (event.keyCode === 13) {
            // Enter pressed
            event.stopPropagation();
            event.preventDefault();
            if (event.ctrlKey) {
                const textarea = event.target;
                this._insertNewLine(textarea);
                this.props.onSearchChanged(textarea.value);
            }
            else {
                event.shiftKey
                    ? this.props.onHighlightPrevious()
                    : this.props.onHighlightNext();
            }
        }
    }
    _onReplaceKeydown(event) {
        if (event.keyCode === 13) {
            // Enter pressed
            event.stopPropagation();
            event.preventDefault();
            if (event.ctrlKey) {
                this._insertNewLine(event.target);
            }
            else {
                this.props.onReplaceCurrent();
            }
        }
    }
    _insertNewLine(textarea) {
        const [start, end] = [textarea.selectionStart, textarea.selectionEnd];
        textarea.setRangeText('\n', start, end, 'end');
    }
    _onClose() {
        // Clean up and close widget.
        this.props.onClose();
    }
    _onReplaceToggled() {
        // Deactivate invalid replace filters
        if (!this.props.replaceEntryVisible) {
            for (const key in this.props.filtersDefinition) {
                const filter = this.props.filtersDefinition[key];
                if (!filter.supportReplace) {
                    this.props.onFilterChanged(key, false).catch(reason => {
                        console.error(`Fail to update filter value for ${filter.title}:\n${reason}`);
                    });
                }
            }
        }
        this.props.onReplaceEntryShown(!this.props.replaceEntryVisible);
    }
    _toggleFiltersVisibility() {
        this.props.onFiltersVisibilityChanged(!this.props.filtersVisible);
    }
    render() {
        var _a, _b;
        const trans = this.translator.load('jupyterlab');
        const showReplace = !this.props.isReadOnly && this.props.replaceEntryVisible;
        const filters = this.props.filtersDefinition;
        const hasFilters = Object.keys(filters).length > 0;
        const filterToggle = hasFilters ? (react_index_js_.createElement(FilterToggle, { visible: this.props.filtersVisible, anyEnabled: Object.keys(filters).some(name => {
                var _a;
                const filter = filters[name];
                return (_a = this.props.filters[name]) !== null && _a !== void 0 ? _a : filter.default;
            }), toggleVisible: () => this._toggleFiltersVisibility(), trans: trans })) : null;
        const selectionBinding = (_a = this.props.keyBindings) === null || _a === void 0 ? void 0 : _a.toggleSearchInSelection;
        const selectionKeys = selectionBinding
            ? commands_dist_index_es6_js_.CommandRegistry.formatKeystroke(selectionBinding.keys)
            : '';
        const selectionKeyHint = selectionKeys ? ` (${selectionKeys})` : '';
        const filter = hasFilters ? (react_index_js_.createElement("div", { className: SEARCH_OPTIONS_CLASS }, Object.keys(filters).map(name => {
            var _a;
            const filter = filters[name];
            return (react_index_js_.createElement(FilterSelection, { key: name, title: filter.title, description: filter.description +
                    (name == 'selection' ? selectionKeyHint : ''), isEnabled: !showReplace || filter.supportReplace, onToggle: async () => {
                    await this.props.onFilterChanged(name, !this.props.filters[name]);
                }, value: (_a = this.props.filters[name]) !== null && _a !== void 0 ? _a : filter.default }));
        }))) : null;
        const icon = this.props.replaceEntryVisible
            ? index_js_.caretDownIcon
            : index_js_.caretRightIcon;
        // TODO: Error messages from regex are not currently localizable.
        return (react_index_js_.createElement(react_index_js_.Fragment, null,
            react_index_js_.createElement("div", { className: OVERLAY_ROW_CLASS },
                this.props.isReadOnly ? (react_index_js_.createElement("div", { className: TOGGLE_PLACEHOLDER })) : (react_index_js_.createElement("button", { className: TOGGLE_WRAPPER, onClick: () => this._onReplaceToggled(), tabIndex: 0, title: trans.__('Toggle Replace') },
                    react_index_js_.createElement(icon.react, { className: `${REPLACE_TOGGLE_CLASS} ${BUTTON_CONTENT_CLASS}`, tag: "span", elementPosition: "center", height: "20px", width: "20px" }))),
                react_index_js_.createElement(SearchEntry, { inputRef: this.props.searchInputRef, useRegex: this.props.useRegex, caseSensitive: this.props.caseSensitive, wholeWords: this.props.wholeWords, onCaseSensitiveToggled: this.props.onCaseSensitiveToggled, onRegexToggled: this.props.onRegexToggled, onWordToggled: this.props.onWordToggled, onKeydown: (e) => this._onSearchKeydown(e), onChange: (e) => this._onSearchChange(e), initialSearchText: this.props.initialSearchText, translator: this.translator }),
                filterToggle,
                react_index_js_.createElement(SearchIndices, { currentIndex: this.props.currentIndex, totalMatches: (_b = this.props.totalMatches) !== null && _b !== void 0 ? _b : 0 }),
                react_index_js_.createElement(UpDownButtons, { onHighlightPrevious: () => {
                        this.props.onHighlightPrevious();
                    }, onHighlightNext: () => {
                        this.props.onHighlightNext();
                    }, trans: trans, keyBindings: this.props.keyBindings }),
                react_index_js_.createElement("button", { className: BUTTON_WRAPPER_CLASS, onClick: () => this._onClose(), tabIndex: 0 },
                    react_index_js_.createElement(index_js_.closeIcon.react, { className: "jp-icon-hover", elementPosition: "center", height: "16px", width: "16px" }))),
            react_index_js_.createElement("div", { className: OVERLAY_ROW_CLASS }, showReplace ? (react_index_js_.createElement(react_index_js_.Fragment, null,
                react_index_js_.createElement(ReplaceEntry, { onPreserveCaseToggled: this.props.onPreserveCaseToggled, onReplaceKeydown: (e) => this._onReplaceKeydown(e), onChange: (e) => this.props.onReplaceChanged(e.target.value), onReplaceCurrent: () => this.props.onReplaceCurrent(), onReplaceAll: () => this.props.onReplaceAll(), replaceOptionsSupport: this.props.replaceOptionsSupport, replaceText: this.props.replaceText, preserveCase: this.props.preserveCase, translator: this.translator }),
                react_index_js_.createElement("div", { className: SPACER_CLASS }))) : null),
            this.props.filtersVisible ? filter : null,
            !!this.props.errorMessage && (react_index_js_.createElement("div", { className: REGEX_ERROR_CLASS }, this.props.errorMessage))));
    }
}
/**
 * Search document widget
 */
class SearchDocumentView extends index_js_.VDomRenderer {
    /**
     * Search document widget constructor.
     *
     * @param model Search document model
     * @param translator Application translator object
     * @param keyBindings Search keybindings
     *
     */
    constructor(model, translator, keyBindings) {
        super(model);
        this.translator = translator;
        this._showReplace = false;
        this._showFilters = false;
        this._closed = new dist_index_es6_js_.Signal(this);
        this.addClass(OVERLAY_CLASS);
        this._searchInput = react_index_js_.createRef();
        this._keyBindings = keyBindings;
    }
    /**
     * A signal emitted when the widget is closed.
     *
     * Closing the widget detached it from the DOM but does not dispose it.
     */
    get closed() {
        return this._closed;
    }
    /**
     * Focus search input.
     */
    focusSearchInput() {
        var _a;
        (_a = this._searchInput.current) === null || _a === void 0 ? void 0 : _a.select();
    }
    /**
     * Set the initial search text.
     */
    setSearchText(search) {
        this.model.initialQuery = search;
        // Only set the new search text to search expression if there is any
        // to avoid nullifying the one that was remembered from last time.
        if (search) {
            this.model.searchExpression = search;
        }
    }
    /**
     * Set the replace text
     *
     * It does not trigger a view update.
     */
    setReplaceText(replace) {
        this.model.replaceText = replace;
    }
    /**
     * Show the replacement input box.
     */
    showReplace() {
        this.setReplaceInputVisibility(true);
    }
    /**
     * A message handler invoked on a `'close-request'` message.
     *
     * #### Notes
     * On top of the default implementation emit closed signal and end model query.
     */
    onCloseRequest(msg) {
        super.onCloseRequest(msg);
        this._closed.emit();
        void this.model.endQuery();
    }
    setReplaceInputVisibility(v) {
        if (this._showReplace !== v) {
            this._showReplace = v;
            this.update();
        }
    }
    setFiltersVisibility(v) {
        if (this._showFilters !== v) {
            this._showFilters = v;
            this.update();
        }
    }
    render() {
        return this.model.filtersDefinitionChanged ? (react_index_js_.createElement(apputils_lib_index_js_.UseSignal, { signal: this.model.filtersDefinitionChanged }, () => this._renderOverlay())) : (this._renderOverlay());
    }
    _renderOverlay() {
        return (react_index_js_.createElement(SearchOverlay, { caseSensitive: this.model.caseSensitive, currentIndex: this.model.currentIndex, isReadOnly: this.model.isReadOnly, errorMessage: this.model.parsingError, filters: this.model.filters, filtersDefinition: this.model.filtersDefinition, preserveCase: this.model.preserveCase, replaceEntryVisible: this._showReplace, filtersVisible: this._showFilters, replaceOptionsSupport: this.model.replaceOptionsSupport, replaceText: this.model.replaceText, initialSearchText: this.model.initialQuery, searchInputRef: this._searchInput, totalMatches: this.model.totalMatches, translator: this.translator, useRegex: this.model.useRegex, wholeWords: this.model.wholeWords, onCaseSensitiveToggled: () => {
                this.model.caseSensitive = !this.model.caseSensitive;
            }, onRegexToggled: () => {
                this.model.useRegex = !this.model.useRegex;
            }, onWordToggled: () => {
                this.model.wholeWords = !this.model.wholeWords;
            }, onFilterChanged: async (name, value) => {
                await this.model.setFilter(name, value);
            }, onFiltersVisibilityChanged: (v) => {
                this.setFiltersVisibility(v);
            }, onHighlightNext: () => {
                void this.model.highlightNext();
            }, onHighlightPrevious: () => {
                void this.model.highlightPrevious();
            }, onPreserveCaseToggled: () => {
                this.model.preserveCase = !this.model.preserveCase;
            }, onSearchChanged: (q) => {
                this.model.searchExpression = q;
            }, onClose: () => {
                this.close();
            }, onReplaceEntryShown: (v) => {
                this.setReplaceInputVisibility(v);
            }, onReplaceChanged: (q) => {
                this.model.replaceText = q;
            }, onReplaceCurrent: () => {
                void this.model.replaceCurrentMatch();
            }, onReplaceAll: () => {
                void this.model.replaceAllMatches();
            }, keyBindings: this._keyBindings }));
    }
}

// EXTERNAL MODULE: consume shared module (default) @lumino/disposable@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/disposable/dist/index.es6.js)
var disposable_dist_index_es6_js_ = __webpack_require__(78612);
;// CONCATENATED MODULE: ../packages/documentsearch/lib/searchproviderregistry.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * Search provider registry
 */
class SearchProviderRegistry {
    /**
     * Constructor
     *
     * @param translator Application translator object
     */
    constructor(translator = lib_index_js_.nullTranslator) {
        this.translator = translator;
        this._changed = new dist_index_es6_js_.Signal(this);
        this._providerMap = new Map();
    }
    /**
     * Add a provider to the registry.
     *
     * @param key - The provider key.
     * @returns A disposable delegate that, when disposed, deregisters the given search provider
     */
    add(key, provider) {
        this._providerMap.set(key, provider);
        this._changed.emit();
        return new disposable_dist_index_es6_js_.DisposableDelegate(() => {
            this._providerMap.delete(key);
            this._changed.emit();
        });
    }
    /**
     * Returns a matching provider for the widget.
     *
     * @param widget - The widget to search over.
     * @returns the search provider, or undefined if none exists.
     */
    getProvider(widget) {
        // iterate through all providers and ask each one if it can search on the
        // widget.
        for (const P of this._providerMap.values()) {
            if (P.isApplicable(widget)) {
                return P.createNew(widget, this.translator);
            }
        }
        return undefined;
    }
    /**
     * Whether the registry as a matching provider for the widget.
     *
     * @param widget - The widget to search over.
     * @returns Provider existence
     */
    hasProvider(widget) {
        for (const P of this._providerMap.values()) {
            if (P.isApplicable(widget)) {
                return true;
            }
        }
        return false;
    }
    /**
     * Signal that emits when a new search provider has been registered
     * or removed.
     */
    get changed() {
        return this._changed;
    }
}

// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
;// CONCATENATED MODULE: ../packages/documentsearch/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The search provider registry token.
 */
const ISearchProviderRegistry = new dist_index_js_.Token('@jupyterlab/documentsearch:ISearchProviderRegistry', `A service for a registry of search
  providers for the application. Plugins can register their UI elements with this registry
  to provide find/replace support.`);

;// CONCATENATED MODULE: ../packages/documentsearch/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module documentsearch
 */









/***/ })

}]);
//# sourceMappingURL=2778.d4c67be46276147de325.js.map?v=d4c67be46276147de325