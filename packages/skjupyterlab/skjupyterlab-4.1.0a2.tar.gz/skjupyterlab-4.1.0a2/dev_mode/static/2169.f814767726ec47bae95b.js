"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[2169],{

/***/ 22169:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "IPluginManager": () => (/* reexport */ IPluginManager),
  "PluginListModel": () => (/* reexport */ PluginListModel),
  "Plugins": () => (/* reexport */ Plugins)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var lib_index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/services@~7.1.0-alpha.2 (singleton) (fallback: ../packages/services/lib/index.js)
var services_lib_index_js_ = __webpack_require__(43411);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(30205);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
;// CONCATENATED MODULE: ../packages/pluginmanager/lib/dialogs.js

function PluginRequiredMessage(props) {
    return (react_index_js_.createElement(react_index_js_.Fragment, null,
        props.trans.__('The plugin "%1" cannot be disabled as it is required by other plugins:', props.plugin.id),
        react_index_js_.createElement("ul", null, props.dependants.map(plugin => (react_index_js_.createElement("li", { key: 'dependantsDialog-' + plugin.id }, plugin.id)))),
        props.trans.__('Please disable the dependant plugins first.')));
}
function PluginInUseMessage(props) {
    return (react_index_js_.createElement("div", { className: 'jp-pluginmanager-PluginInUseMessage' },
        props.trans.__('While the plugin "%1" is not required by other enabled plugins, some plugins provide optional features depending on it. These plugins are:', props.plugin.id),
        react_index_js_.createElement("ul", null, props.optionalDependants.map(plugin => (react_index_js_.createElement("li", { key: 'optionalDependantsDialog-' + plugin.id }, plugin.id)))),
        props.trans.__('Do you want to disable it anyway?')));
}

;// CONCATENATED MODULE: ../packages/pluginmanager/lib/model.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */








/**
 * The server API path for querying/modifying available plugins.
 */
const PLUGIN_API_PATH = 'lab/api/plugins';
/**
 * The model representing plugin list.
 */
class PluginListModel extends ui_components_lib_index_js_.VDomModel {
    constructor(options) {
        var _a, _b, _c;
        super();
        /**
         * Contains an error message if an error occurred when querying plugin status.
         */
        this.statusError = null;
        /**
         * Contains an error message if an error occurred when enabling/disabling plugin.
         */
        this.actionError = null;
        this._trackerDataChanged = new index_es6_js_.Signal(this);
        this._isLoading = false;
        this._pendingActions = [];
        this._ready = new dist_index_js_.PromiseDelegate();
        this._pluginData = options.pluginData;
        this._serverSettings =
            options.serverSettings || services_lib_index_js_.ServerConnection.makeSettings();
        this._query = options.query || '';
        this._isDisclaimed = (_a = options.isDisclaimed) !== null && _a !== void 0 ? _a : false;
        this._extraLockedPlugins = (_b = options.extraLockedPlugins) !== null && _b !== void 0 ? _b : [];
        this.refresh()
            .then(() => this._ready.resolve())
            .catch(e => this._ready.reject(e));
        this._trans = ((_c = options.translator) !== null && _c !== void 0 ? _c : translation_lib_index_js_.nullTranslator).load('jupyterlab');
    }
    get available() {
        return [...this._available.values()];
    }
    /**
     * Whether plugin data is still getting loaded.
     */
    get isLoading() {
        return this._isLoading;
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
            this._trackerDataChanged.emit(void 0);
        }
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
            this.stateChanged.emit();
            this._trackerDataChanged.emit(void 0);
        }
    }
    /**
     * A promise that resolves when the trackable data changes
     */
    get trackerDataChanged() {
        return this._trackerDataChanged;
    }
    /**
     * A promise that resolves when the plugins were fetched from the server
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * Enable a plugin.
     *
     * @param entry An entry indicating which plugin to enable.
     */
    async enable(entry) {
        if (!this.isDisclaimed) {
            throw new Error('User has not confirmed the disclaimer');
        }
        await this._performAction('enable', entry);
        entry.enabled = true;
    }
    /**
     * Disable a plugin.
     *
     * @param entry An entry indicating which plugin to disable.
     * @returns Whether the plugin was disabled
     */
    async disable(entry) {
        if (!this.isDisclaimed) {
            throw new Error('User has not confirmed the disclaimer');
        }
        const { dependants, optionalDependants } = this.getDependants(entry);
        if (dependants.length > 0) {
            // We require user to disable plugins one-by-one as each of them may have
            // further dependencies (or optional dependencies) and we want the user to
            // take a pause to think about those.
            void (0,index_js_.showDialog)({
                title: this._trans.__('This plugin is required by other plugins'),
                body: PluginRequiredMessage({
                    plugin: entry,
                    dependants,
                    trans: this._trans
                }),
                buttons: [index_js_.Dialog.okButton()]
            });
            return;
        }
        if (optionalDependants.length > 0) {
            const userConfirmation = await (0,index_js_.showDialog)({
                title: this._trans.__('This plugin is used by other plugins'),
                body: PluginInUseMessage({
                    plugin: entry,
                    optionalDependants,
                    trans: this._trans
                }),
                buttons: [
                    index_js_.Dialog.okButton({ label: this._trans.__('Disable anyway') }),
                    index_js_.Dialog.cancelButton()
                ]
            });
            if (!userConfirmation.button.accept) {
                return;
            }
        }
        await this._performAction('disable', entry);
        if (this.actionError) {
            return;
        }
        entry.enabled = false;
    }
    getDependants(entry) {
        const dependants = [];
        const optionalDependants = [];
        if (entry.provides) {
            const tokenName = entry.provides.name;
            for (const plugin of this._available.values()) {
                if (!plugin.enabled) {
                    continue;
                }
                if (plugin.requires
                    .filter(token => !!token)
                    .some(token => token.name === tokenName)) {
                    dependants.push(plugin);
                }
                if (plugin.optional
                    .filter(token => !!token)
                    .some(token => token.name === tokenName)) {
                    optionalDependants.push(plugin);
                }
            }
        }
        return {
            dependants,
            optionalDependants
        };
    }
    /**
     * Whether there are currently any actions pending.
     */
    hasPendingActions() {
        return this._pendingActions.length > 0;
    }
    /**
     * Send a request to the server to perform an action on a plugin.
     *
     * @param action A valid action to perform.
     * @param entry The plugin to perform the action on.
     */
    _performAction(action, entry) {
        this.actionError = null;
        const actionRequest = this._requestAPI({}, {
            method: 'POST',
            body: JSON.stringify({
                cmd: action,
                plugin_name: entry.id
            })
        });
        actionRequest.catch(reason => {
            this.actionError = reason.toString();
        });
        this._addPendingAction(actionRequest);
        return actionRequest;
    }
    /**
     * Add a pending action.
     *
     * @param pending A promise that resolves when the action is completed.
     */
    _addPendingAction(pending) {
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
    /**
     * Refresh plugin lock statuses
     */
    async refresh() {
        var _a;
        this.statusError = null;
        this._isLoading = true;
        this.stateChanged.emit();
        try {
            // Get the lock status from backend; if backend is not available,
            // we assume that all plugins are locked.
            const fallback = {
                allLocked: true,
                lockRules: []
            };
            const status = (_a = (await this._requestAPI())) !== null && _a !== void 0 ? _a : fallback;
            this._available = new Map(this._pluginData.availablePlugins.map(plugin => {
                let tokenLabel = plugin.provides
                    ? plugin.provides.name.split(':')[1]
                    : undefined;
                if (plugin.provides && !tokenLabel) {
                    tokenLabel = plugin.provides.name;
                }
                return [
                    plugin.id,
                    {
                        ...plugin,
                        locked: this._isLocked(plugin.id, status),
                        tokenLabel
                    }
                ];
            }));
        }
        catch (reason) {
            this.statusError = reason.toString();
        }
        finally {
            this._isLoading = false;
            this.stateChanged.emit();
        }
    }
    _isLocked(pluginId, status) {
        if (status.allLocked) {
            // All plugins are locked.
            return true;
        }
        if (this._extraLockedPlugins.includes(pluginId)) {
            // Plugin is locked on client side.
            return true;
        }
        const extension = pluginId.split(':')[0];
        if (status.lockRules.includes(extension)) {
            // Entire extension is locked.
            return true;
        }
        if (status.lockRules.includes(pluginId)) {
            // This plugin specifically is locked.
            return true;
        }
        return false;
    }
    /**
     * Call the plugin API
     *
     * @param endPoint API REST end point for the plugin
     * @param init Initial values for the request
     * @returns The response body interpreted as JSON
     */
    async _requestAPI(queryArgs = {}, init = {}) {
        // Make request to Jupyter API
        const settings = this._serverSettings;
        const requestUrl = lib_index_js_.URLExt.join(settings.baseUrl, PLUGIN_API_PATH);
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
        return data;
    }
}

// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/pluginmanager/lib/widget.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */




/**
 * Panel with a table of available plugins allowing to enable/disable each.
 */
class Plugins extends dist_index_es6_js_.Panel {
    constructor(options) {
        const { model, translator } = options;
        super();
        this.model = model;
        this.addClass('jp-pluginmanager');
        this.trans = translator.load('jupyterlab');
        this.addWidget(new Disclaimer(model, this.trans));
        const header = new Header(model, this.trans);
        this.addWidget(header);
        const availableList = new AvailableList(model, this.trans);
        this.addWidget(availableList);
    }
}
class AvailableList extends index_js_.VDomRenderer {
    constructor(model, trans) {
        super(model);
        this.trans = trans;
        this.addClass('jp-pluginmanager-AvailableList');
    }
    render() {
        return (react_index_js_.createElement(react_index_js_.Fragment, null, this.model.statusError !== null ? (react_index_js_.createElement(ErrorMessage, null, this.trans.__('Error querying installed extensions%1', this.model.statusError ? `: ${this.model.statusError}` : '.'))) : this.model.isLoading ? (react_index_js_.createElement("div", { className: "jp-pluginmanager-loader" }, this.trans.__('Updating plugin list…'))) : (react_index_js_.createElement(ui_components_lib_index_js_.Table, { blankIndicator: () => {
                return react_index_js_.createElement("div", null, this.trans.__('No entries'));
            }, sortKey: 'plugin-id', rows: this.model.available
                .filter(pkg => {
                const pattern = new RegExp(this.model.query, 'i');
                return (pattern.test(pkg.id) ||
                    pattern.test(pkg.extension) ||
                    (pkg.tokenLabel && pattern.test(pkg.tokenLabel)));
            })
                .map(data => {
                return {
                    data: data,
                    key: data.id
                };
            }), columns: [
                {
                    id: 'plugin-id',
                    label: this.trans.__('Plugin'),
                    renderCell: (row) => (react_index_js_.createElement(react_index_js_.Fragment, null,
                        react_index_js_.createElement("code", null, row.id),
                        react_index_js_.createElement("br", null),
                        row.description)),
                    sort: (a, b) => a.id.localeCompare(b.id)
                },
                {
                    id: 'description',
                    label: this.trans.__('Description'),
                    renderCell: (row) => react_index_js_.createElement(react_index_js_.Fragment, null, row.description),
                    sort: (a, b) => a.description && b.description
                        ? a.description.localeCompare(b.description)
                        : undefined,
                    isHidden: true
                },
                {
                    id: 'autostart',
                    label: this.trans.__('Autostart?'),
                    renderCell: (row) => {
                        switch (row.autoStart) {
                            case 'defer':
                                return this.trans.__('Defer');
                            case true:
                                return this.trans.__('Yes');
                            case false:
                            case undefined: // The default is `false`.
                                return this.trans.__('No');
                            default:
                                const leftover = row.autoStart;
                                throw new Error(`Unknown value: ${leftover}`);
                        }
                    },
                    sort: (a, b) => a.autoStart === b.autoStart ? 0 : a.autoStart ? -1 : 1
                },
                {
                    id: 'requires',
                    label: this.trans.__('Depends on'),
                    renderCell: (row) => (react_index_js_.createElement(react_index_js_.Fragment, null, row.requires.map(v => v.name).join('\n'))),
                    sort: (a, b) => (a.requires || []).length - (b.requires || []).length,
                    isHidden: true
                },
                {
                    id: 'extension',
                    label: this.trans.__('Extension'),
                    renderCell: (row) => react_index_js_.createElement(react_index_js_.Fragment, null, row.extension),
                    sort: (a, b) => a.extension.localeCompare(b.extension)
                },
                {
                    id: 'provides',
                    label: this.trans.__('Provides'),
                    renderCell: (row) => (react_index_js_.createElement(react_index_js_.Fragment, null, row.provides ? (react_index_js_.createElement("code", { title: row.provides.name }, row.tokenLabel)) : ('-'))),
                    sort: (a, b) => (a.tokenLabel || '').localeCompare(b.tokenLabel || '')
                },
                {
                    id: 'enabled',
                    label: this.trans.__('Enabled'),
                    renderCell: (row) => (react_index_js_.createElement(react_index_js_.Fragment, null,
                        react_index_js_.createElement("input", { type: "checkbox", checked: row.enabled, disabled: row.locked || !this.model.isDisclaimed, title: row.locked || !this.model.isDisclaimed
                                ? row.locked
                                    ? this.trans.__('This plugin is locked.')
                                    : this.trans.__('To enable/disable, please acknowledge the disclaimer.')
                                : row.enabled
                                    ? this.trans.__('Disable %1 plugin', row.id)
                                    : this.trans.__('Enable %1 plugin', row.id), onChange: (event) => {
                                if (!this.model.isDisclaimed) {
                                    return;
                                }
                                if (event.target.checked) {
                                    void this.onAction('enable', row);
                                }
                                else {
                                    void this.onAction('disable', row);
                                }
                            } }),
                        row.locked ? (react_index_js_.createElement(ui_components_lib_index_js_.lockIcon.react, { tag: "span", title: this.trans.__('This plugin was locked by system administrator or is a critical dependency and cannot be enabled/disabled.') })) : (''))),
                    sort: (a, b) => +a.enabled - +b.enabled
                }
            ] }))));
    }
    /**
     * Callback handler for when the user wants to perform an action on an extension.
     *
     * @param action The action to perform.
     * @param entry The entry to perform the action on.
     */
    onAction(action, entry) {
        switch (action) {
            case 'enable':
                return this.model.enable(entry);
            case 'disable':
                return this.model.disable(entry);
            default:
                throw new Error(`Invalid action: ${action}`);
        }
    }
}
class Disclaimer extends index_js_.VDomRenderer {
    constructor(model, trans) {
        super(model);
        this.trans = trans;
        this.addClass('jp-pluginmanager-Disclaimer');
    }
    render() {
        return (react_index_js_.createElement("div", null,
            react_index_js_.createElement("div", null, this.trans.__('Customise your experience/improve performance by disabling plugins you do not need. To disable or uninstall an entire extension use the Extension Manager instead. Changes will apply after reloading JupyterLab.')),
            react_index_js_.createElement("label", null,
                react_index_js_.createElement("input", { type: "checkbox", className: "jp-mod-styled jp-pluginmanager-Disclaimer-checkbox", defaultChecked: this.model.isDisclaimed, onChange: event => {
                        this.model.isDisclaimed = event.target.checked;
                    } }),
                this.trans.__('I understand that disabling core application plugins may render features and parts of the user interface unavailable and recovery using `jupyter labextension enable <plugin-name>` command may be required'))));
    }
}
class Header extends index_js_.VDomRenderer {
    constructor(model, trans) {
        super(model);
        this.trans = trans;
        this.addClass('jp-pluginmanager-Header');
    }
    render() {
        return (react_index_js_.createElement(react_index_js_.Fragment, null,
            react_index_js_.createElement(ui_components_lib_index_js_.FilterBox, { placeholder: this.trans.__('Filter'), updateFilter: (fn, query) => {
                    this.model.query = query !== null && query !== void 0 ? query : '';
                }, initialQuery: this.model.query, useFuzzyFilter: false }),
            react_index_js_.createElement("div", { className: `jp-pluginmanager-pending ${this.model.hasPendingActions() ? 'jp-mod-hasPending' : ''}` }),
            this.model.actionError && (react_index_js_.createElement(ErrorMessage, null,
                react_index_js_.createElement("p", null, this.trans.__('Error when performing an action.')),
                react_index_js_.createElement("p", null, this.trans.__('Reason given:')),
                react_index_js_.createElement("pre", null, this.model.actionError)))));
    }
}
function ErrorMessage(props) {
    return react_index_js_.createElement("div", { className: "jp-pluginmanager-error" }, props.children);
}

;// CONCATENATED MODULE: ../packages/pluginmanager/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The plugin manager token.
 */
const IPluginManager = new dist_index_js_.Token('@jupyterlab/pluginmanager:IPluginManager', `A canary for plugin manager presence, with a method to open the plugin manager widget.`);

;// CONCATENATED MODULE: ../packages/pluginmanager/lib/index.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module pluginmanager
 */





/***/ })

}]);
//# sourceMappingURL=2169.f814767726ec47bae95b.js.map?v=f814767726ec47bae95b