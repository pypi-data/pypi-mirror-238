"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[5051],{

/***/ 55051:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "ExtensionsPanel": () => (/* reexport */ ExtensionsPanel),
  "ListModel": () => (/* reexport */ ListModel)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var lib_index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/services@~7.1.0-alpha.2 (singleton) (fallback: ../packages/services/lib/index.js)
var services_lib_index_js_ = __webpack_require__(43411);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/polling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/polling/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(81967);
// EXTERNAL MODULE: ../node_modules/semver/index.js
var semver = __webpack_require__(38873);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
;// CONCATENATED MODULE: ../packages/extensionmanager/lib/dialog.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * Show a dialog box reporting an error during installation of an extension.
 *
 * @param name The name of the extension
 * @param errorMessage Any error message giving details about the failure.
 */
function reportInstallError(name, errorMessage, translator) {
    translator = translator || translation_lib_index_js_.nullTranslator;
    const trans = translator.load('jupyterlab');
    const entries = [];
    entries.push(react_index_js_.createElement("p", null, trans.__(`An error occurred installing "${name}".`)));
    if (errorMessage) {
        entries.push(react_index_js_.createElement("p", null,
            react_index_js_.createElement("span", { className: "jp-extensionmanager-dialog-subheader" }, trans.__('Error message:'))), react_index_js_.createElement("pre", null, errorMessage.trim()));
    }
    const body = react_index_js_.createElement("div", { className: "jp-extensionmanager-dialog" }, entries);
    void (0,index_js_.showDialog)({
        title: trans.__('Extension Installation Error'),
        body,
        buttons: [index_js_.Dialog.warnButton({ label: trans.__('Ok') })]
    });
}

;// CONCATENATED MODULE: ../packages/extensionmanager/lib/model.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/* global RequestInit */








/**
 * The server API path for querying/modifying installed extensions.
 */
const EXTENSION_API_PATH = 'lab/api/extensions';
/**
 * Model for an extension list.
 */
class ListModel extends ui_components_lib_index_js_.VDomModel {
    constructor(serviceManager, translator) {
        super();
        this.actionError = null;
        /**
         * Contains an error message if an error occurred when querying installed extensions.
         */
        this.installedError = null;
        /**
         * Contains an error message if an error occurred when searching for extensions.
         */
        this.searchError = null;
        /**
         * Whether a reload should be considered due to actions taken.
         */
        this.promptReload = false;
        this._isDisclaimed = false;
        this._isEnabled = false;
        this._isLoadingInstalledExtensions = false;
        this._isSearching = false;
        this._query = '';
        this._page = 1;
        this._pagination = 30;
        this._lastPage = 1;
        this._pendingActions = [];
        const metadata = JSON.parse(
        // The page config option may not be defined; e.g. in the federated example
        lib_index_js_.PageConfig.getOption('extensionManager') || '{}');
        this.name = metadata.name;
        this.canInstall = metadata.can_install;
        this.installPath = metadata.install_path;
        this.translator = translator || translation_lib_index_js_.nullTranslator;
        this._installed = [];
        this._lastSearchResult = [];
        this.serviceManager = serviceManager;
        this._debouncedSearch = new index_es6_js_.Debouncer(this.search.bind(this), 1000);
    }
    /**
     * A readonly array of the installed extensions.
     */
    get installed() {
        return this._installed;
    }
    /**
     * Whether the warning is disclaimed or not.
     */
    get isDisclaimed() {
        return this._isDisclaimed;
    }
    set isDisclaimed(v) {
        if (v !== this._isDisclaimed) {
            this._isDisclaimed = v;
            this.stateChanged.emit();
            void this._debouncedSearch.invoke();
        }
    }
    /**
     * Whether the extension manager is enabled or not.
     */
    get isEnabled() {
        return this._isEnabled;
    }
    set isEnabled(v) {
        if (v !== this._isEnabled) {
            this._isEnabled = v;
            this.stateChanged.emit();
        }
    }
    get isLoadingInstalledExtensions() {
        return this._isLoadingInstalledExtensions;
    }
    get isSearching() {
        return this._isSearching;
    }
    /**
     * A readonly array containing the latest search result
     */
    get searchResult() {
        return this._lastSearchResult;
    }
    /**
     * The search query.
     *
     * Setting its value triggers a new search.
     */
    get query() {
        return this._query;
    }
    set query(value) {
        if (this._query !== value) {
            this._query = value;
            this._page = 1;
            void this._debouncedSearch.invoke();
        }
    }
    /**
     * The current search page.
     *
     * Setting its value triggers a new search.
     *
     * ### Note
     * First page is 1.
     */
    get page() {
        return this._page;
    }
    set page(value) {
        if (this._page !== value) {
            this._page = value;
            void this._debouncedSearch.invoke();
        }
    }
    /**
     * The search pagination.
     *
     * Setting its value triggers a new search.
     */
    get pagination() {
        return this._pagination;
    }
    set pagination(value) {
        if (this._pagination !== value) {
            this._pagination = value;
            void this._debouncedSearch.invoke();
        }
    }
    /**
     * The last page of results in the current search.
     */
    get lastPage() {
        return this._lastPage;
    }
    /**
     * Dispose the extensions list model.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._debouncedSearch.dispose();
        super.dispose();
    }
    /**
     * Whether there are currently any actions pending.
     */
    hasPendingActions() {
        return this._pendingActions.length > 0;
    }
    /**
     * Install an extension.
     *
     * @param entry An entry indicating which extension to install.
     */
    async install(entry) {
        await this.performAction('install', entry).then(data => {
            if (data.status !== 'ok') {
                reportInstallError(entry.name, data.message, this.translator);
            }
            return this.update(true);
        });
    }
    /**
     * Uninstall an extension.
     *
     * @param entry An entry indicating which extension to uninstall.
     */
    async uninstall(entry) {
        if (!entry.installed) {
            throw new Error(`Not installed, cannot uninstall: ${entry.name}`);
        }
        await this.performAction('uninstall', entry);
        return this.update(true);
    }
    /**
     * Enable an extension.
     *
     * @param entry An entry indicating which extension to enable.
     */
    async enable(entry) {
        if (entry.enabled) {
            throw new Error(`Already enabled: ${entry.name}`);
        }
        await this.performAction('enable', entry);
        await this.refreshInstalled(true);
    }
    /**
     * Disable an extension.
     *
     * @param entry An entry indicating which extension to disable.
     */
    async disable(entry) {
        if (!entry.enabled) {
            throw new Error(`Already disabled: ${entry.name}`);
        }
        await this.performAction('disable', entry);
        await this.refreshInstalled(true);
    }
    /**
     * Refresh installed packages
     *
     * @param force Force refreshing the list of installed packages
     */
    async refreshInstalled(force = false) {
        this.installedError = null;
        this._isLoadingInstalledExtensions = true;
        this.stateChanged.emit();
        try {
            const [extensions] = await Private.requestAPI({
                refresh: force ? 1 : 0
            });
            this._installed = extensions.sort(Private.comparator);
        }
        catch (reason) {
            this.installedError = reason.toString();
        }
        finally {
            this._isLoadingInstalledExtensions = false;
            this.stateChanged.emit();
        }
    }
    /**
     * Search with current query.
     *
     * Sets searchError and totalEntries as appropriate.
     *
     * @returns The extensions matching the current query.
     */
    async search(force = false) {
        var _a, _b;
        if (!this.isDisclaimed) {
            return Promise.reject('Installation warning is not disclaimed.');
        }
        this.searchError = null;
        this._isSearching = true;
        this.stateChanged.emit();
        try {
            const [extensions, links] = await Private.requestAPI({
                query: (_a = this.query) !== null && _a !== void 0 ? _a : '',
                page: this.page,
                per_page: this.pagination,
                refresh: force ? 1 : 0
            });
            const lastURL = links['last'];
            if (lastURL) {
                const lastPage = lib_index_js_.URLExt.queryStringToObject((_b = lib_index_js_.URLExt.parse(lastURL).search) !== null && _b !== void 0 ? _b : '')['page'];
                if (lastPage) {
                    this._lastPage = parseInt(lastPage, 10);
                }
            }
            const installedNames = this._installed.map(pkg => pkg.name);
            this._lastSearchResult = extensions
                .filter(pkg => !installedNames.includes(pkg.name))
                .sort(Private.comparator);
        }
        catch (reason) {
            this.searchError = reason.toString();
        }
        finally {
            this._isSearching = false;
            this.stateChanged.emit();
        }
    }
    /**
     * Update the current model.
     *
     * This will query the packages repository, and the notebook server.
     *
     * Emits the `stateChanged` signal on successful completion.
     */
    async update(force = false) {
        if (this.isDisclaimed) {
            // First refresh the installed list - so the search results are correctly filtered
            await this.refreshInstalled(force);
            await this.search();
        }
    }
    /**
     * Send a request to the server to perform an action on an extension.
     *
     * @param action A valid action to perform.
     * @param entry The extension to perform the action on.
     */
    performAction(action, entry) {
        const actionRequest = Private.requestAPI({}, {
            method: 'POST',
            body: JSON.stringify({
                cmd: action,
                extension_name: entry.name
            })
        });
        actionRequest.then(([reply]) => {
            const trans = this.translator.load('jupyterlab');
            if (reply.needs_restart.includes('server')) {
                void (0,index_js_.showDialog)({
                    title: trans.__('Information'),
                    body: trans.__('You will need to restart JupyterLab to apply the changes.'),
                    buttons: [index_js_.Dialog.okButton({ label: trans.__('Ok') })]
                });
            }
            else {
                const followUps = [];
                if (reply.needs_restart.includes('frontend')) {
                    followUps.push(
                    // @ts-expect-error isElectron is not a standard attribute
                    window.isElectron
                        ? trans.__('reload JupyterLab')
                        : trans.__('refresh the web page'));
                }
                if (reply.needs_restart.includes('kernel')) {
                    followUps.push(trans.__('install the extension in all kernels and restart them'));
                }
                void (0,index_js_.showDialog)({
                    title: trans.__('Information'),
                    body: trans.__('You will need to %1 to apply the changes.', followUps.join(trans.__(' and '))),
                    buttons: [index_js_.Dialog.okButton({ label: trans.__('Ok') })]
                });
            }
            this.actionError = null;
        }, reason => {
            this.actionError = reason.toString();
        });
        this.addPendingAction(actionRequest);
        return actionRequest.then(([reply]) => reply);
    }
    /**
     * Add a pending action.
     *
     * @param pending A promise that resolves when the action is completed.
     */
    addPendingAction(pending) {
        // Add to pending actions collection
        this._pendingActions.push(pending);
        // Ensure action is removed when resolved
        const remove = () => {
            const i = this._pendingActions.indexOf(pending);
            this._pendingActions.splice(i, 1);
            this.stateChanged.emit(undefined);
        };
        pending.then(remove, remove);
        // Signal changed state
        this.stateChanged.emit(undefined);
    }
}
/**
 * ListModel statics.
 */
(function (ListModel) {
    /**
     * Utility function to check whether an entry can be updated.
     *
     * @param entry The entry to check.
     */
    function entryHasUpdate(entry) {
        if (!entry.installed || !entry.latest_version) {
            return false;
        }
        return semver.lt(entry.installed_version, entry.latest_version);
    }
    ListModel.entryHasUpdate = entryHasUpdate;
})(ListModel || (ListModel = {}));
/**
 * A namespace for private functionality.
 */
var Private;
(function (Private) {
    /**
     * A comparator function that sorts allowedExtensions orgs to the top.
     */
    function comparator(a, b) {
        if (a.name === b.name) {
            return 0;
        }
        else {
            return a.name > b.name ? 1 : -1;
        }
    }
    Private.comparator = comparator;
    const LINK_PARSER = /<([^>]+)>; rel="([^"]+)",?/g;
    /**
     * Call the API extension
     *
     * @param queryArgs Query arguments
     * @param init Initial values for the request
     * @returns The response body interpreted as JSON and the response link header
     */
    async function requestAPI(queryArgs = {}, init = {}) {
        var _a;
        // Make request to Jupyter API
        const settings = services_lib_index_js_.ServerConnection.makeSettings();
        const requestUrl = lib_index_js_.URLExt.join(settings.baseUrl, EXTENSION_API_PATH // API Namespace
        );
        let response;
        try {
            response = await services_lib_index_js_.ServerConnection.makeRequest(requestUrl + lib_index_js_.URLExt.objectToQueryString(queryArgs), init, settings);
        }
        catch (error) {
            throw new services_lib_index_js_.ServerConnection.NetworkError(error);
        }
        let data = await response.text();
        if (data.length > 0) {
            try {
                data = JSON.parse(data);
            }
            catch (error) {
                console.log('Not a JSON response body.', response);
            }
        }
        if (!response.ok) {
            throw new services_lib_index_js_.ServerConnection.ResponseError(response, data.message || data);
        }
        const link = (_a = response.headers.get('Link')) !== null && _a !== void 0 ? _a : '';
        const links = {};
        let match = null;
        while ((match = LINK_PARSER.exec(link)) !== null) {
            links[match[2]] = match[1];
        }
        return [data, links];
    }
    Private.requestAPI = requestAPI;
})(Private || (Private = {}));

// EXTERNAL MODULE: ../node_modules/react-paginate/dist/react-paginate.js
var react_paginate = __webpack_require__(96389);
var react_paginate_default = /*#__PURE__*/__webpack_require__.n(react_paginate);
;// CONCATENATED MODULE: ../packages/extensionmanager/lib/widget.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




const BADGE_SIZE = 32;
const BADGE_QUERY_SIZE = Math.floor(devicePixelRatio * BADGE_SIZE);
function getExtensionGitHubUser(entry) {
    if (entry.homepage_url &&
        entry.homepage_url.startsWith('https://github.com/')) {
        return entry.homepage_url.split('/')[3];
    }
    else if (entry.repository_url &&
        entry.repository_url.startsWith('https://github.com/')) {
        return entry.repository_url.split('/')[3];
    }
    return null;
}
/**
 * VDOM for visualizing an extension entry.
 */
function ListEntry(props) {
    const { canFetch, entry, supportInstallation, trans } = props;
    const flagClasses = [];
    if (entry.status && ['ok', 'warning', 'error'].indexOf(entry.status) !== -1) {
        flagClasses.push(`jp-extensionmanager-entry-${entry.status}`);
    }
    const githubUser = canFetch ? getExtensionGitHubUser(entry) : null;
    if (!entry.allowed) {
        flagClasses.push(`jp-extensionmanager-entry-should-be-uninstalled`);
    }
    return (react_index_js_.createElement("li", { className: `jp-extensionmanager-entry ${flagClasses.join(' ')}`, style: { display: 'flex' } },
        react_index_js_.createElement("div", { style: { marginRight: '8px' } }, githubUser ? (react_index_js_.createElement("img", { src: `https://github.com/${githubUser}.png?size=${BADGE_QUERY_SIZE}`, style: { width: '32px', height: '32px' } })) : (react_index_js_.createElement("div", { style: { width: `${BADGE_SIZE}px`, height: `${BADGE_SIZE}px` } }))),
        react_index_js_.createElement("div", { className: "jp-extensionmanager-entry-description" },
            react_index_js_.createElement("div", { className: "jp-extensionmanager-entry-title" },
                react_index_js_.createElement("div", { className: "jp-extensionmanager-entry-name" }, entry.homepage_url ? (react_index_js_.createElement("a", { href: entry.homepage_url, target: "_blank", rel: "noopener noreferrer", title: trans.__('%1 extension home page', entry.name) }, entry.name)) : (react_index_js_.createElement("div", null, entry.name))),
                react_index_js_.createElement("div", { className: "jp-extensionmanager-entry-version" },
                    react_index_js_.createElement("div", { title: trans.__('Version: %1', entry.installed_version) }, entry.installed_version)),
                entry.installed && !entry.allowed && (react_index_js_.createElement(ui_components_lib_index_js_.ToolbarButtonComponent, { icon: ui_components_lib_index_js_.infoIcon, iconLabel: trans.__('%1 extension is not allowed anymore. Please uninstall it immediately or contact your administrator.', entry.name), onClick: () => window.open('https://jupyterlab.readthedocs.io/en/latest/user/extensions.html') })),
                entry.approved && (react_index_js_.createElement(ui_components_lib_index_js_.jupyterIcon.react, { className: "jp-extensionmanager-is-approved", top: "1px", height: "auto", width: "1em", title: trans.__('This extension is approved by your security team.') }))),
            react_index_js_.createElement("div", { className: "jp-extensionmanager-entry-content" },
                react_index_js_.createElement("div", { className: "jp-extensionmanager-entry-description" }, entry.description),
                props.performAction && (react_index_js_.createElement("div", { className: "jp-extensionmanager-entry-buttons" }, entry.installed ? (react_index_js_.createElement(react_index_js_.Fragment, null,
                    supportInstallation && (react_index_js_.createElement(react_index_js_.Fragment, null,
                        ListModel.entryHasUpdate(entry) && (react_index_js_.createElement(ui_components_lib_index_js_.Button, { onClick: () => props.performAction('install', entry), title: trans.__('Update "%1" to "%2"', entry.name, entry.latest_version), minimal: true, small: true }, trans.__('Update to %1', entry.latest_version))),
                        react_index_js_.createElement(ui_components_lib_index_js_.Button, { onClick: () => props.performAction('uninstall', entry), title: trans.__('Uninstall "%1"', entry.name), minimal: true, small: true }, trans.__('Uninstall')))),
                    entry.enabled ? (react_index_js_.createElement(ui_components_lib_index_js_.Button, { onClick: () => props.performAction('disable', entry), title: trans.__('Disable "%1"', entry.name), minimal: true, small: true }, trans.__('Disable'))) : (react_index_js_.createElement(ui_components_lib_index_js_.Button, { onClick: () => props.performAction('enable', entry), title: trans.__('Enable "%1"', entry.name), minimal: true, small: true }, trans.__('Enable'))))) : (supportInstallation && (react_index_js_.createElement(ui_components_lib_index_js_.Button, { onClick: () => props.performAction('install', entry), title: trans.__('Install "%1"', entry.name), minimal: true, small: true }, trans.__('Install'))))))))));
}
/**
 * List view widget for extensions
 */
function ListView(props) {
    var _a;
    const { canFetch, performAction, supportInstallation, trans } = props;
    return (react_index_js_.createElement("div", { className: "jp-extensionmanager-listview-wrapper" },
        props.entries.length > 0 ? (react_index_js_.createElement("ul", { className: "jp-extensionmanager-listview" }, props.entries.map(entry => (react_index_js_.createElement(ListEntry, { key: entry.name, canFetch: canFetch, entry: entry, performAction: performAction, supportInstallation: supportInstallation, trans: trans }))))) : (react_index_js_.createElement("div", { key: "message", className: "jp-extensionmanager-listview-message" }, trans.__('No entries'))),
        props.numPages > 1 && (react_index_js_.createElement("div", { className: "jp-extensionmanager-pagination" },
            react_index_js_.createElement((react_paginate_default()), { previousLabel: '<', nextLabel: '>', breakLabel: "...", breakClassName: 'break', initialPage: ((_a = props.initialPage) !== null && _a !== void 0 ? _a : 1) - 1, pageCount: props.numPages, marginPagesDisplayed: 2, pageRangeDisplayed: 3, onPageChange: (data) => props.onPage(data.selected + 1), activeClassName: 'active' })))));
}
function ErrorMessage(props) {
    return react_index_js_.createElement("div", { className: "jp-extensionmanager-error" }, props.children);
}
class Header extends ui_components_lib_index_js_.ReactWidget {
    constructor(model, trans, searchInputRef) {
        super();
        this.model = model;
        this.trans = trans;
        this.searchInputRef = searchInputRef;
        model.stateChanged.connect(this.update, this);
        this.addClass('jp-extensionmanager-header');
    }
    render() {
        return (react_index_js_.createElement(react_index_js_.Fragment, null,
            react_index_js_.createElement("div", { className: "jp-extensionmanager-title" },
                react_index_js_.createElement("span", null, this.trans.__('%1 Manager', this.model.name)),
                this.model.installPath && (react_index_js_.createElement(ui_components_lib_index_js_.infoIcon.react, { className: "jp-extensionmanager-path", tag: "span", title: this.trans.__('Extension installation path: %1', this.model.installPath) }))),
            react_index_js_.createElement(ui_components_lib_index_js_.FilterBox, { placeholder: this.trans.__('Search'), disabled: !this.model.isDisclaimed, updateFilter: (fn, query) => {
                    this.model.query = query !== null && query !== void 0 ? query : '';
                }, useFuzzyFilter: false, inputRef: this.searchInputRef }),
            react_index_js_.createElement("div", { className: `jp-extensionmanager-pending ${this.model.hasPendingActions() ? 'jp-mod-hasPending' : ''}` }),
            this.model.actionError && (react_index_js_.createElement(ErrorMessage, null,
                react_index_js_.createElement("p", null, this.trans.__('Error when performing an action.')),
                react_index_js_.createElement("p", null, this.trans.__('Reason given:')),
                react_index_js_.createElement("pre", null, this.model.actionError)))));
    }
}
class Warning extends ui_components_lib_index_js_.ReactWidget {
    constructor(model, trans) {
        super();
        this.model = model;
        this.trans = trans;
        this.addClass('jp-extensionmanager-disclaimer');
        model.stateChanged.connect(this.update, this);
    }
    render() {
        return (react_index_js_.createElement(react_index_js_.Fragment, null,
            react_index_js_.createElement("p", null,
                this.trans
                    .__(`The JupyterLab development team is excited to have a robust
third-party extension community. However, we do not review
third-party extensions, and some extensions may introduce security
risks or contain malicious code that runs on your machine. Moreover in order
to work, this panel needs to fetch data from web services. Do you agree to
activate this feature?`),
                react_index_js_.createElement("br", null),
                react_index_js_.createElement("a", { href: "https://jupyterlab.readthedocs.io/en/latest/privacy_policies.html", target: "_blank", rel: "noreferrer" }, this.trans.__('Please read the privacy policy.'))),
            this.model.isDisclaimed ? (react_index_js_.createElement(ui_components_lib_index_js_.Button, { className: "jp-extensionmanager-disclaimer-disable", onClick: (e) => {
                    this.model.isDisclaimed = false;
                }, title: this.trans.__('This will withdraw your consent.') }, this.trans.__('No'))) : (react_index_js_.createElement("div", null,
                react_index_js_.createElement(ui_components_lib_index_js_.Button, { className: "jp-extensionmanager-disclaimer-enable", onClick: () => {
                        this.model.isDisclaimed = true;
                    } }, this.trans.__('Yes')),
                react_index_js_.createElement(ui_components_lib_index_js_.Button, { className: "jp-extensionmanager-disclaimer-disable", onClick: () => {
                        this.model.isEnabled = false;
                    }, title: this.trans.__('This will disable the extension manager panel; including the listing of installed extension.') }, this.trans.__('No, disable'))))));
    }
}
class InstalledList extends ui_components_lib_index_js_.ReactWidget {
    constructor(model, trans) {
        super();
        this.model = model;
        this.trans = trans;
        model.stateChanged.connect(this.update, this);
    }
    render() {
        return (react_index_js_.createElement(react_index_js_.Fragment, null, this.model.installedError !== null ? (react_index_js_.createElement(ErrorMessage, null, `Error querying installed extensions${this.model.installedError ? `: ${this.model.installedError}` : '.'}`)) : this.model.isLoadingInstalledExtensions ? (react_index_js_.createElement("div", { className: "jp-extensionmanager-loader" }, this.trans.__('Updating extensions list…'))) : (react_index_js_.createElement(ListView, { canFetch: this.model.isDisclaimed, entries: this.model.installed.filter(pkg => new RegExp(this.model.query.toLowerCase()).test(pkg.name)), numPages: 1, trans: this.trans, onPage: value => {
                /* no-op */
            }, performAction: this.model.isDisclaimed ? this.onAction.bind(this) : null, supportInstallation: this.model.canInstall && this.model.isDisclaimed }))));
    }
    /**
     * Callback handler for when the user wants to perform an action on an extension.
     *
     * @param action The action to perform.
     * @param entry The entry to perform the action on.
     */
    onAction(action, entry) {
        switch (action) {
            case 'install':
                return this.model.install(entry);
            case 'uninstall':
                return this.model.uninstall(entry);
            case 'enable':
                return this.model.enable(entry);
            case 'disable':
                return this.model.disable(entry);
            default:
                throw new Error(`Invalid action: ${action}`);
        }
    }
}
class SearchResult extends ui_components_lib_index_js_.ReactWidget {
    constructor(model, trans) {
        super();
        this.model = model;
        this.trans = trans;
        model.stateChanged.connect(this.update, this);
    }
    /**
     * Callback handler for the user changes the page of the search result pagination.
     *
     * @param value The pagination page number.
     */
    onPage(value) {
        this.model.page = value;
    }
    /**
     * Callback handler for when the user wants to perform an action on an extension.
     *
     * @param action The action to perform.
     * @param entry The entry to perform the action on.
     */
    onAction(action, entry) {
        switch (action) {
            case 'install':
                return this.model.install(entry);
            case 'uninstall':
                return this.model.uninstall(entry);
            case 'enable':
                return this.model.enable(entry);
            case 'disable':
                return this.model.disable(entry);
            default:
                throw new Error(`Invalid action: ${action}`);
        }
    }
    render() {
        return (react_index_js_.createElement(react_index_js_.Fragment, null, this.model.searchError !== null ? (react_index_js_.createElement(ErrorMessage, null, `Error searching for extensions${this.model.searchError ? `: ${this.model.searchError}` : '.'}`)) : this.model.isSearching ? (react_index_js_.createElement("div", { className: "jp-extensionmanager-loader" }, this.trans.__('Updating extensions list…'))) : (react_index_js_.createElement(ListView, { canFetch: this.model.isDisclaimed, entries: this.model.searchResult, initialPage: this.model.page, numPages: this.model.lastPage, onPage: value => {
                this.onPage(value);
            }, performAction: this.model.isDisclaimed ? this.onAction.bind(this) : null, supportInstallation: this.model.canInstall && this.model.isDisclaimed, trans: this.trans }))));
    }
    update() {
        this.title.label = this.model.query
            ? this.trans.__('Search Results')
            : this.trans.__('Discover');
        super.update();
    }
}
class ExtensionsPanel extends ui_components_lib_index_js_.SidePanel {
    constructor(options) {
        const { model, translator } = options;
        super({ translator });
        this._wasInitialized = false;
        this._wasDisclaimed = true;
        this.model = model;
        this._searchInputRef = react_index_js_.createRef();
        this.addClass('jp-extensionmanager-view');
        this.trans = translator.load('jupyterlab');
        this.header.addWidget(new Header(model, this.trans, this._searchInputRef));
        const warning = new Warning(model, this.trans);
        warning.title.label = this.trans.__('Warning');
        this.addWidget(warning);
        const installed = new ui_components_lib_index_js_.PanelWithToolbar();
        installed.addClass('jp-extensionmanager-installedlist');
        installed.title.label = this.trans.__('Installed');
        installed.toolbar.addItem('refresh', new ui_components_lib_index_js_.ToolbarButton({
            icon: ui_components_lib_index_js_.refreshIcon,
            onClick: () => {
                model.refreshInstalled(true).catch(reason => {
                    console.error(`Failed to refresh the installed extensions list:\n${reason}`);
                });
            },
            tooltip: this.trans.__('Refresh extensions list')
        }));
        installed.addWidget(new InstalledList(model, this.trans));
        this.addWidget(installed);
        if (this.model.canInstall) {
            const searchResults = new SearchResult(model, this.trans);
            searchResults.addClass('jp-extensionmanager-searchresults');
            this.addWidget(searchResults);
        }
        this._wasDisclaimed = this.model.isDisclaimed;
        if (this.model.isDisclaimed) {
            this.content.collapse(0);
            this.content.layout.setRelativeSizes([0, 1, 1]);
        }
        else {
            // If warning is not disclaimed expand only the warning panel
            this.content.expand(0);
            this.content.collapse(1);
            this.content.collapse(2);
        }
        this.model.stateChanged.connect(this._onStateChanged, this);
    }
    /**
     * Dispose of the widget and its descendant widgets.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.model.stateChanged.disconnect(this._onStateChanged, this);
        super.dispose();
    }
    /**
     * Handle the DOM events for the extension manager search bar.
     *
     * @param event - The DOM event sent to the extension manager search bar.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the search bar's DOM node.
     * It should not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'focus':
            case 'blur':
                this._toggleFocused();
                break;
            default:
                break;
        }
    }
    /**
     * A message handler invoked on a `'before-attach'` message.
     */
    onBeforeAttach(msg) {
        this.node.addEventListener('focus', this, true);
        this.node.addEventListener('blur', this, true);
        super.onBeforeAttach(msg);
    }
    onBeforeShow(msg) {
        if (!this._wasInitialized) {
            this._wasInitialized = true;
            this.model.refreshInstalled().catch(reason => {
                console.log(`Failed to refresh installed extension list:\n${reason}`);
            });
        }
    }
    /**
     * A message handler invoked on an `'after-detach'` message.
     */
    onAfterDetach(msg) {
        super.onAfterDetach(msg);
        this.node.removeEventListener('focus', this, true);
        this.node.removeEventListener('blur', this, true);
    }
    /**
     * A message handler invoked on an `'activate-request'` message.
     */
    onActivateRequest(msg) {
        if (this.isAttached) {
            const input = this._searchInputRef.current;
            if (input) {
                input.focus();
                input.select();
            }
        }
        super.onActivateRequest(msg);
    }
    _onStateChanged() {
        if (!this._wasDisclaimed && this.model.isDisclaimed) {
            this.content.collapse(0);
            this.content.expand(1);
            this.content.expand(2);
        }
        this._wasDisclaimed = this.model.isDisclaimed;
    }
    /**
     * Toggle the focused modifier based on the input node focus state.
     */
    _toggleFocused() {
        const focused = document.activeElement === this._searchInputRef.current;
        this.toggleClass('lm-mod-focused', focused);
    }
}

;// CONCATENATED MODULE: ../packages/extensionmanager/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module extensionmanager
 */




/***/ })

}]);
//# sourceMappingURL=5051.d1846b543e65f1c82c29.js.map?v=d1846b543e65f1c82c29