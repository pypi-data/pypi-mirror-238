"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[6417],{

/***/ 86417:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "IJSONSettingEditorTracker": () => (/* reexport */ tokens/* IJSONSettingEditorTracker */.g),
  "ISettingEditorTracker": () => (/* reexport */ tokens/* ISettingEditorTracker */.O),
  "JsonSettingEditor": () => (/* reexport */ JsonSettingEditor),
  "SettingsEditor": () => (/* reexport */ SettingsEditor)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(30205);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(72234);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
var react_index_js_default = /*#__PURE__*/__webpack_require__.n(react_index_js_);
// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var algorithm_dist_index_es6_js_ = __webpack_require__(16415);
;// CONCATENATED MODULE: ../packages/settingeditor/lib/pluginlist.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/






/**
 * The JupyterLab plugin schema key for the setting editor
 * icon class of a plugin.
 */
const ICON_KEY = 'jupyter.lab.setting-icon';
/**
 * The JupyterLab plugin schema key for the setting editor
 * icon class of a plugin.
 */
const ICON_CLASS_KEY = 'jupyter.lab.setting-icon-class';
/**
 * The JupyterLab plugin schema key for the setting editor
 * icon label of a plugin.
 */
const ICON_LABEL_KEY = 'jupyter.lab.setting-icon-label';
/**
 * A list of plugins with editable settings.
 */
class PluginList extends index_js_.ReactWidget {
    /**
     * Create a new plugin list.
     */
    constructor(options) {
        var _a;
        super();
        this._changed = new index_es6_js_.Signal(this);
        this._handleSelectSignal = new index_es6_js_.Signal(this);
        this._updateFilterSignal = new index_es6_js_.Signal(this);
        this._allPlugins = [];
        this._settings = {};
        this._scrollTop = 0;
        this._selection = '';
        this.registry = options.registry;
        this.translator = options.translator || lib_index_js_.nullTranslator;
        this.addClass('jp-PluginList');
        this._confirm = options.confirm;
        this.registry.pluginChanged.connect(() => {
            this.update();
        }, this);
        this.mapPlugins = this.mapPlugins.bind(this);
        this.setFilter = this.setFilter.bind(this);
        this.setFilter(options.query ? (0,ui_components_lib_index_js_.updateFilterFunction)(options.query, false, false) : null);
        this.setError = this.setError.bind(this);
        this._evtMousedown = this._evtMousedown.bind(this);
        this._query = (_a = options.query) !== null && _a !== void 0 ? _a : '';
        this._allPlugins = PluginList.sortPlugins(this.registry).filter(plugin => {
            var _a;
            const { schema } = plugin;
            const deprecated = schema['jupyter.lab.setting-deprecated'] === true;
            const editable = Object.keys(schema.properties || {}).length > 0;
            const extensible = schema.additionalProperties !== false;
            // Filters out a couple of plugins that take too long to load in the new settings editor.
            const correctEditor = 
            // If this is the json settings editor, anything is fine
            this._confirm ||
                // If this is the new settings editor, remove context menu / main menu settings.
                (!this._confirm && !((_a = options.toSkip) !== null && _a !== void 0 ? _a : []).includes(plugin.id));
            return !deprecated && correctEditor && (editable || extensible);
        });
        /**
         * Loads all settings and stores them for easy access when displaying search results.
         */
        const loadSettings = async () => {
            for (const plugin of this._allPlugins) {
                const pluginSettings = (await this.registry.load(plugin.id));
                this._settings[plugin.id] = pluginSettings;
            }
            this.update();
        };
        void loadSettings();
        this._errors = {};
    }
    /**
     * A signal emitted when a list user interaction happens.
     */
    get changed() {
        return this._changed;
    }
    /**
     * The selection value of the plugin list.
     */
    get scrollTop() {
        var _a;
        return (_a = this.node.querySelector('ul')) === null || _a === void 0 ? void 0 : _a.scrollTop;
    }
    get hasErrors() {
        for (const id in this._errors) {
            if (this._errors[id]) {
                return true;
            }
        }
        return false;
    }
    get filter() {
        return this._filter;
    }
    /**
     * The selection value of the plugin list.
     */
    get selection() {
        return this._selection;
    }
    set selection(selection) {
        this._selection = selection;
        this.update();
    }
    /**
     * Signal that fires when search filter is updated so that settings panel can filter results.
     */
    get updateFilterSignal() {
        return this._updateFilterSignal;
    }
    get handleSelectSignal() {
        return this._handleSelectSignal;
    }
    /**
     * Handle `'update-request'` messages.
     */
    onUpdateRequest(msg) {
        const ul = this.node.querySelector('ul');
        if (ul && this._scrollTop !== undefined) {
            ul.scrollTop = this._scrollTop;
        }
        super.onUpdateRequest(msg);
    }
    /**
     * Handle the `'mousedown'` event for the plugin list.
     *
     * @param event - The DOM event sent to the widget
     */
    _evtMousedown(event) {
        const target = event.currentTarget;
        const id = target.getAttribute('data-id');
        if (!id) {
            return;
        }
        if (this._confirm) {
            this._confirm(id)
                .then(() => {
                this.selection = id;
                this._changed.emit(undefined);
                this.update();
            })
                .catch(() => {
                /* no op */
            });
        }
        else {
            this._scrollTop = this.scrollTop;
            this._selection = id;
            this._handleSelectSignal.emit(id);
            this._changed.emit(undefined);
            this.update();
        }
    }
    /**
     * Check the plugin for a rendering hint's value.
     *
     * #### Notes
     * The order of priority for overridden hints is as follows, from most
     * important to least:
     * 1. Data set by the end user in a settings file.
     * 2. Data set by the plugin author as a schema default.
     * 3. Data set by the plugin author as a top-level key of the schema.
     */
    getHint(key, registry, plugin) {
        // First, give priority to checking if the hint exists in the user data.
        let hint = plugin.data.user[key];
        // Second, check to see if the hint exists in composite data, which folds
        // in default values from the schema.
        if (!hint) {
            hint = plugin.data.composite[key];
        }
        // Third, check to see if the plugin schema has defined the hint.
        if (!hint) {
            hint = plugin.schema[key];
        }
        // Finally, use the defaults from the registry schema.
        if (!hint) {
            const { properties } = registry.schema;
            hint = properties && properties[key] && properties[key].default;
        }
        return typeof hint === 'string' ? hint : '';
    }
    /**
     * Function to recursively filter properties that match search results.
     * @param filter - Function to filter based on search results
     * @param props - Schema properties being filtered
     * @param definitions - Definitions to use for filling in references in properties
     * @param ref - Reference to a definition
     * @returns - String array of properties that match the search results.
     */
    getFilterString(filter, props, definitions, ref) {
        var _a;
        // If properties given are references, populate properties
        // with corresponding definition.
        if (ref && definitions) {
            ref = ref.replace('#/definitions/', '');
            props = (_a = definitions[ref]) !== null && _a !== void 0 ? _a : {};
        }
        // If given properties are an object, advance into the properties
        // for that object instead.
        if (props.properties) {
            props = props.properties;
            // If given properties are an array, advance into the properties
            // for the items instead.
        }
        else if (props.items) {
            props = props.items;
            // Otherwise, you've reached the base case and don't need to check for matching properties
        }
        else {
            return [];
        }
        // If reference found, recurse
        if (props['$ref']) {
            return this.getFilterString(filter, props, definitions, props['$ref']);
        }
        // Make sure props is non-empty before calling reduce
        if (Object.keys(props).length === 0) {
            return [];
        }
        // Iterate through the properties and check for titles / descriptions that match search.
        return Object.keys(props).reduce((acc, value) => {
            var _a, _b;
            // If this is the base case, check for matching title / description
            const subProps = props[value];
            if (!subProps) {
                if (filter((_a = props.title) !== null && _a !== void 0 ? _a : '')) {
                    return props.title;
                }
                if (filter(value)) {
                    return value;
                }
            }
            // If there are properties in the object, check for title / description
            if (filter((_b = subProps.title) !== null && _b !== void 0 ? _b : '')) {
                acc.push(subProps.title);
            }
            if (filter(value)) {
                acc.push(value);
            }
            // Finally, recurse on the properties left.
            acc.concat(this.getFilterString(filter, subProps, definitions, subProps['$ref']));
            return acc;
        }, []);
    }
    /**
     * Updates the filter when the search bar value changes.
     * @param filter Filter function passed by search bar based on search value.
     */
    setFilter(filter, query) {
        if (filter) {
            this._filter = (plugin) => {
                var _a, _b;
                if (!filter || filter((_a = plugin.schema.title) !== null && _a !== void 0 ? _a : '')) {
                    return null;
                }
                const filtered = this.getFilterString(filter, (_b = plugin.schema) !== null && _b !== void 0 ? _b : {}, plugin.schema.definitions);
                return filtered;
            };
        }
        else {
            this._filter = null;
        }
        this._query = query;
        this._updateFilterSignal.emit(this._filter);
        this.update();
    }
    setError(id, error) {
        if (this._errors[id] !== error) {
            this._errors[id] = error;
            this.update();
        }
        else {
            this._errors[id] = error;
        }
    }
    mapPlugins(plugin) {
        var _a, _b, _c, _d;
        const { id, schema, version } = plugin;
        const trans = this.translator.load('jupyterlab');
        const title = typeof schema.title === 'string' ? trans._p('schema', schema.title) : id;
        const highlightedTitleIndices = algorithm_dist_index_es6_js_.StringExt.matchSumOfSquares(title.toLocaleLowerCase(), (_b = (_a = this._query) === null || _a === void 0 ? void 0 : _a.toLocaleLowerCase()) !== null && _b !== void 0 ? _b : '');
        const hightlightedTitle = algorithm_dist_index_es6_js_.StringExt.highlight(title, (_c = highlightedTitleIndices === null || highlightedTitleIndices === void 0 ? void 0 : highlightedTitleIndices.indices) !== null && _c !== void 0 ? _c : [], chunk => {
            return react_index_js_default().createElement("mark", null, chunk);
        });
        const description = typeof schema.description === 'string'
            ? trans._p('schema', schema.description)
            : '';
        const itemTitle = `${description}\n${id}\n${version}`;
        const icon = this.getHint(ICON_KEY, this.registry, plugin);
        const iconClass = this.getHint(ICON_CLASS_KEY, this.registry, plugin);
        const iconTitle = this.getHint(ICON_LABEL_KEY, this.registry, plugin);
        const filteredProperties = this._filter
            ? (_d = this._filter(plugin)) === null || _d === void 0 ? void 0 : _d.map(fieldValue => {
                var _a, _b, _c;
                const highlightedIndices = algorithm_dist_index_es6_js_.StringExt.matchSumOfSquares(fieldValue.toLocaleLowerCase(), (_b = (_a = this._query) === null || _a === void 0 ? void 0 : _a.toLocaleLowerCase()) !== null && _b !== void 0 ? _b : '');
                const highlighted = algorithm_dist_index_es6_js_.StringExt.highlight(fieldValue, (_c = highlightedIndices === null || highlightedIndices === void 0 ? void 0 : highlightedIndices.indices) !== null && _c !== void 0 ? _c : [], chunk => {
                    return react_index_js_default().createElement("mark", null, chunk);
                });
                return react_index_js_default().createElement("li", { key: `${id}-${fieldValue}` },
                    " ",
                    highlighted,
                    " ");
            })
            : undefined;
        return (react_index_js_default().createElement("div", { onClick: this._evtMousedown, className: `${id === this.selection
                ? 'jp-mod-selected jp-PluginList-entry'
                : 'jp-PluginList-entry'} ${this._errors[id] ? 'jp-ErrorPlugin' : ''}`, "data-id": id, key: id, title: itemTitle },
            react_index_js_default().createElement("div", { className: "jp-PluginList-entry-label", role: "tab" },
                react_index_js_default().createElement("div", { className: "jp-SelectedIndicator" }),
                react_index_js_default().createElement(ui_components_lib_index_js_.LabIcon.resolveReact, { icon: icon || (iconClass ? undefined : ui_components_lib_index_js_.settingsIcon), iconClass: (0,ui_components_lib_index_js_.classes)(iconClass, 'jp-Icon'), title: iconTitle, tag: "span", stylesheet: "settingsEditor" }),
                react_index_js_default().createElement("span", { className: "jp-PluginList-entry-label-text" }, hightlightedTitle)),
            react_index_js_default().createElement("ul", null, filteredProperties)));
    }
    render() {
        const trans = this.translator.load('jupyterlab');
        // Filter all plugins based on search value before displaying list.
        const allPlugins = this._allPlugins.filter(plugin => {
            if (!this._filter) {
                return false;
            }
            const filtered = this._filter(plugin);
            return filtered === null || filtered.length > 0;
        });
        const modifiedPlugins = allPlugins.filter(plugin => {
            var _a;
            return (_a = this._settings[plugin.id]) === null || _a === void 0 ? void 0 : _a.isModified;
        });
        const modifiedItems = modifiedPlugins.map(this.mapPlugins);
        const otherItems = allPlugins
            .filter(plugin => {
            return !modifiedPlugins.includes(plugin);
        })
            .map(this.mapPlugins);
        return (react_index_js_default().createElement("div", { className: "jp-PluginList-wrapper" },
            react_index_js_default().createElement(ui_components_lib_index_js_.FilterBox, { updateFilter: this.setFilter, useFuzzyFilter: false, placeholder: trans.__('Search…'), forceRefresh: false, caseSensitive: false, initialQuery: this._query }),
            modifiedItems.length > 0 && (react_index_js_default().createElement("div", null,
                react_index_js_default().createElement("h1", { className: "jp-PluginList-header" }, trans.__('Modified')),
                react_index_js_default().createElement("ul", null, modifiedItems))),
            otherItems.length > 0 && (react_index_js_default().createElement("div", null,
                react_index_js_default().createElement("h1", { className: "jp-PluginList-header" }, trans.__('Settings')),
                react_index_js_default().createElement("ul", null, otherItems))),
            modifiedItems.length === 0 && otherItems.length === 0 && (react_index_js_default().createElement("p", { className: "jp-PluginList-noResults" }, trans.__('No items match your search.')))));
    }
}
/**
 * A namespace for `PluginList` statics.
 */
(function (PluginList) {
    /**
     * Sort a list of plugins by title and ID.
     */
    function sortPlugins(registry) {
        return Object.keys(registry.plugins)
            .map(plugin => registry.plugins[plugin])
            .sort((a, b) => {
            return (a.schema.title || a.id).localeCompare(b.schema.title || b.id);
        });
    }
    PluginList.sortPlugins = sortPlugins;
})(PluginList || (PluginList = {}));

// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @lumino/polling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/polling/dist/index.es6.js)
var polling_dist_index_es6_js_ = __webpack_require__(81967);
// EXTERNAL MODULE: consume shared module (default) @rjsf/validator-ajv8@^5.1.0 (strict) (fallback: ../node_modules/@rjsf/validator-ajv8/dist/validator-ajv8.esm.js)
var validator_ajv8_esm_js_ = __webpack_require__(89319);
var validator_ajv8_esm_js_default = /*#__PURE__*/__webpack_require__.n(validator_ajv8_esm_js_);
;// CONCATENATED MODULE: ../packages/settingeditor/lib/SettingsFormEditor.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/







/**
 * Indentation to use when saving the settings as JSON document.
 */
const JSON_INDENTATION = 4;
/**
 * A React component that prepares the settings for a
 * given plugin to be rendered in the FormEditor.
 */
class SettingsFormEditor extends (react_index_js_default()).Component {
    constructor(props) {
        super(props);
        /**
         * Handler for the "Restore to defaults" button - clears all
         * modified settings then calls `setFormData` to restore the
         * values.
         */
        this.reset = async (event) => {
            event.stopPropagation();
            for (const field in this.props.settings.user) {
                await this.props.settings.remove(field);
            }
            this._formData = this.props.settings.composite;
            this.setState({ isModified: false });
        };
        this._onChange = (e) => {
            this.props.hasError(e.errors.length !== 0);
            this._formData = e.formData;
            if (e.errors.length === 0) {
                this.props.updateDirtyState(true);
                void this._debouncer.invoke();
            }
            this.props.onSelect(this.props.settings.id);
        };
        const { settings } = props;
        this._formData = settings.composite;
        this.state = {
            isModified: settings.isModified,
            uiSchema: {},
            filteredSchema: this.props.settings.schema,
            formContext: {
                defaultFormData: this.props.settings.default(),
                settings: this.props.settings
            }
        };
        this.handleChange = this.handleChange.bind(this);
        this._debouncer = new polling_dist_index_es6_js_.Debouncer(this.handleChange);
    }
    componentDidMount() {
        this._setUiSchema();
        this._setFilteredSchema();
    }
    componentDidUpdate(prevProps) {
        this._setUiSchema(prevProps.renderers[prevProps.settings.id]);
        this._setFilteredSchema(prevProps.filteredValues);
        if (prevProps.settings !== this.props.settings) {
            this.setState({
                formContext: {
                    settings: this.props.settings,
                    defaultFormData: this.props.settings.default()
                }
            });
        }
    }
    componentWillUnmount() {
        this._debouncer.dispose();
    }
    /**
     * Handler for edits made in the form editor.
     */
    handleChange() {
        // Prevent unnecessary save when opening settings that haven't been modified.
        if (!this.props.settings.isModified &&
            this._formData &&
            this.props.settings.isDefault(this._formData)) {
            this.props.updateDirtyState(false);
            return;
        }
        this.props.settings
            .save(JSON.stringify(this._formData, undefined, JSON_INDENTATION))
            .then(() => {
            this.props.updateDirtyState(false);
            this.setState({ isModified: this.props.settings.isModified });
        })
            .catch((reason) => {
            this.props.updateDirtyState(false);
            const trans = this.props.translator.load('jupyterlab');
            void (0,index_js_.showErrorMessage)(trans.__('Error saving settings.'), reason);
        });
    }
    render() {
        const trans = this.props.translator.load('jupyterlab');
        return (react_index_js_default().createElement((react_index_js_default()).Fragment, null,
            react_index_js_default().createElement("div", { className: "jp-SettingsHeader" },
                react_index_js_default().createElement("h2", { className: "jp-SettingsHeader-title", title: this.props.settings.schema.description }, this.props.settings.schema.title),
                react_index_js_default().createElement("div", { className: "jp-SettingsHeader-buttonbar" }, this.state.isModified && (react_index_js_default().createElement(ui_components_lib_index_js_.Button, { className: "jp-RestoreButton", onClick: this.reset }, trans.__('Restore to Defaults')))),
                react_index_js_default().createElement("div", { className: "jp-SettingsHeader-description" }, this.props.settings.schema.description)),
            react_index_js_default().createElement(ui_components_lib_index_js_.FormComponent, { validator: (validator_ajv8_esm_js_default()), schema: this.state.filteredSchema, formData: this._getFilteredFormData(this.state.filteredSchema), uiSchema: this.state.uiSchema, fields: this.props.renderers[this.props.settings.id], formContext: this.state.formContext, liveValidate: true, idPrefix: `jp-SettingsEditor-${this.props.settings.id}`, onChange: this._onChange, translator: this.props.translator })));
    }
    _setUiSchema(prevRenderers) {
        var _a;
        const renderers = this.props.renderers[this.props.settings.id];
        if (!dist_index_js_.JSONExt.deepEqual(Object.keys(prevRenderers !== null && prevRenderers !== void 0 ? prevRenderers : {}).sort(), Object.keys(renderers !== null && renderers !== void 0 ? renderers : {}).sort())) {
            /**
             * Construct uiSchema to pass any custom renderers to the form editor.
             */
            const uiSchema = {};
            for (const id in this.props.renderers[this.props.settings.id]) {
                if (Object.keys((_a = this.props.settings.schema.properties) !== null && _a !== void 0 ? _a : {}).includes(id)) {
                    uiSchema[id] = {
                        'ui:field': id
                    };
                }
            }
            this.setState({ uiSchema });
        }
    }
    _setFilteredSchema(prevFilteredValues) {
        var _a, _b, _c, _d;
        if (prevFilteredValues === undefined ||
            !dist_index_js_.JSONExt.deepEqual(prevFilteredValues, this.props.filteredValues)) {
            /**
             * Only show fields that match search value.
             */
            const filteredSchema = dist_index_js_.JSONExt.deepCopy(this.props.settings.schema);
            if ((_b = (_a = this.props.filteredValues) === null || _a === void 0 ? void 0 : _a.length) !== null && _b !== void 0 ? _b : 0 > 0) {
                for (const field in filteredSchema.properties) {
                    if (!((_c = this.props.filteredValues) === null || _c === void 0 ? void 0 : _c.includes((_d = filteredSchema.properties[field].title) !== null && _d !== void 0 ? _d : field))) {
                        delete filteredSchema.properties[field];
                    }
                }
            }
            this.setState({ filteredSchema });
        }
    }
    _getFilteredFormData(filteredSchema) {
        if (!(filteredSchema === null || filteredSchema === void 0 ? void 0 : filteredSchema.properties)) {
            return this._formData;
        }
        const filteredFormData = dist_index_js_.JSONExt.deepCopy(this._formData);
        for (const field in filteredFormData) {
            if (!filteredSchema.properties[field]) {
                delete filteredFormData[field];
            }
        }
        return filteredFormData;
    }
}

;// CONCATENATED MODULE: ../packages/settingeditor/lib/InstructionsPlaceholder.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

const SettingsEditorPlaceholder = ({ translator }) => {
    const trans = translator.load('jupyterlab');
    return (react_index_js_default().createElement("div", { className: "jp-SettingsEditor-placeholder" },
        react_index_js_default().createElement("div", { className: "jp-SettingsEditor-placeholderContent" },
            react_index_js_default().createElement("h3", null, trans.__('No Plugin Selected')),
            react_index_js_default().createElement("p", null, trans.__('Select a plugin from the list to view and edit its preferences.')))));
};

;// CONCATENATED MODULE: ../packages/settingeditor/lib/settingspanel.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/



/**
 * React component that displays a list of SettingsFormEditor
 * components.
 */
const SettingsPanel = ({ settings, editorRegistry, onSelect, handleSelectSignal, hasError, updateDirtyState, updateFilterSignal, translator, initialFilter }) => {
    const [activePluginId, setActivePluginId] = (0,react_index_js_.useState)(null);
    const [filterPlugin, setFilter] = (0,react_index_js_.useState)(initialFilter ? () => initialFilter : null);
    const wrapperRef = react_index_js_default().useRef(null);
    const editorDirtyStates = react_index_js_default().useRef({});
    (0,react_index_js_.useEffect)(() => {
        var _a;
        const onFilterUpdate = (list, newFilter) => {
            newFilter ? setFilter(() => newFilter) : setFilter(null);
        };
        // When filter updates, only show plugins that match search.
        updateFilterSignal.connect(onFilterUpdate);
        const onSelectChange = (list, pluginId) => {
            setActivePluginId(pluginId);
        };
        (_a = handleSelectSignal === null || handleSelectSignal === void 0 ? void 0 : handleSelectSignal.connect) === null || _a === void 0 ? void 0 : _a.call(handleSelectSignal, onSelectChange);
        return () => {
            var _a;
            updateFilterSignal.disconnect(onFilterUpdate);
            (_a = handleSelectSignal === null || handleSelectSignal === void 0 ? void 0 : handleSelectSignal.disconnect) === null || _a === void 0 ? void 0 : _a.call(handleSelectSignal, onSelectChange);
        };
    }, []);
    const updateDirtyStates = react_index_js_default().useCallback((id, dirty) => {
        if (editorDirtyStates.current) {
            editorDirtyStates.current[id] = dirty;
            for (const editor in editorDirtyStates.current) {
                if (editorDirtyStates.current[editor]) {
                    updateDirtyState(true);
                    return;
                }
            }
        }
        updateDirtyState(false);
    }, [editorDirtyStates, updateDirtyState]);
    const renderers = react_index_js_default().useMemo(() => Object.entries(editorRegistry.renderers).reduce((agg, [id, renderer]) => {
        const splitPosition = id.lastIndexOf('.');
        const pluginId = id.substring(0, splitPosition);
        const propertyName = id.substring(splitPosition + 1);
        if (!agg[pluginId]) {
            agg[pluginId] = {};
        }
        if (!agg[pluginId][propertyName] && renderer.fieldRenderer) {
            agg[pluginId][propertyName] = renderer.fieldRenderer;
        }
        return agg;
    }, {}), [editorRegistry]);
    if (!activePluginId && !filterPlugin) {
        return react_index_js_default().createElement(SettingsEditorPlaceholder, { translator: translator });
    }
    return (react_index_js_default().createElement("div", { className: "jp-SettingsPanel", ref: wrapperRef }, settings.map(pluginSettings => {
        // Pass filtered results to SettingsFormEditor to only display filtered fields.
        const filtered = filterPlugin
            ? filterPlugin(pluginSettings.plugin)
            : null;
        // If filtered results are an array, only show if the array is non-empty.
        if ((activePluginId && activePluginId !== pluginSettings.id) ||
            (filtered !== null && filtered.length === 0)) {
            return undefined;
        }
        return (react_index_js_default().createElement("div", { className: "jp-SettingsForm", key: `${pluginSettings.id}SettingsEditor` },
            react_index_js_default().createElement(SettingsFormEditor, { filteredValues: filtered, settings: pluginSettings, renderers: renderers, hasError: (error) => {
                    hasError(pluginSettings.id, error);
                }, updateDirtyState: (dirty) => {
                    updateDirtyStates(pluginSettings.id, dirty);
                }, onSelect: onSelect, translator: translator })));
    })));
};

;// CONCATENATED MODULE: ../packages/settingeditor/lib/settingseditor.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */








/**
 * Form based interface for editing settings.
 */
class SettingsEditor extends dist_index_es6_js_.SplitPanel {
    constructor(options) {
        super({
            orientation: 'horizontal',
            renderer: dist_index_es6_js_.SplitPanel.defaultRenderer,
            spacing: 1
        });
        this._clearDirty = null;
        this._dirty = false;
        this._saveStateChange = new index_es6_js_.Signal(this);
        this.translator = options.translator || lib_index_js_.nullTranslator;
        this._status = options.status;
        const list = (this._list = new PluginList({
            registry: options.registry,
            toSkip: options.toSkip,
            translator: this.translator,
            query: options.query
        }));
        this.addWidget(list);
        this.setDirtyState = this.setDirtyState.bind(this);
        /**
         * Initializes the settings panel after loading the schema for all plugins.
         */
        void Promise.all(PluginList.sortPlugins(options.registry)
            .filter(plugin => {
            const { schema } = plugin;
            const deprecated = schema['jupyter.lab.setting-deprecated'] === true;
            const editable = Object.keys(schema.properties || {}).length > 0;
            const extensible = schema.additionalProperties !== false;
            return !deprecated && (editable || extensible);
        })
            .map(async (plugin) => await options.registry.load(plugin.id)))
            .then(settings => {
            const settingsPanel = ui_components_lib_index_js_.ReactWidget.create(react_index_js_default().createElement(SettingsPanel, { settings: settings.filter(pluginSettings => { var _a; return !((_a = options.toSkip) !== null && _a !== void 0 ? _a : []).includes(pluginSettings.id); }), editorRegistry: options.editorRegistry, handleSelectSignal: this._list.handleSelectSignal, onSelect: (id) => (this._list.selection = id), hasError: this._list.setError, updateFilterSignal: this._list.updateFilterSignal, updateDirtyState: this.setDirtyState, translator: this.translator, initialFilter: this._list.filter }));
            this.addWidget(settingsPanel);
        })
            .catch(reason => {
            console.error(`Fail to load the setting plugins:\n${reason}`);
        });
    }
    /**
     * A signal emitted on the start and end of a saving operation.
     */
    get saveStateChanged() {
        return this._saveStateChange;
    }
    /**
     * Set the dirty state status
     *
     * @param dirty New status
     */
    setDirtyState(dirty) {
        this._dirty = dirty;
        if (this._dirty && !this._clearDirty) {
            this._clearDirty = this._status.setDirty();
        }
        else if (!this._dirty && this._clearDirty) {
            this._clearDirty.dispose();
            this._clearDirty = null;
        }
        if (dirty) {
            if (!this.title.className.includes('jp-mod-dirty')) {
                this.title.className += ' jp-mod-dirty';
            }
        }
        else {
            this.title.className = this.title.className.replace('jp-mod-dirty', '');
        }
        this._saveStateChange.emit(dirty ? 'started' : 'completed');
    }
    /**
     * A message handler invoked on a `'close-request'` message.
     *
     * @param msg Widget message
     */
    onCloseRequest(msg) {
        const trans = this.translator.load('jupyterlab');
        if (this._list.hasErrors) {
            void (0,index_js_.showDialog)({
                title: trans.__('Warning'),
                body: trans.__('Unsaved changes due to validation error. Continue without saving?')
            }).then(value => {
                if (value.button.accept) {
                    this.dispose();
                    super.onCloseRequest(msg);
                }
            });
        }
        else if (this._dirty) {
            void (0,index_js_.showDialog)({
                title: trans.__('Warning'),
                body: trans.__('Some changes have not been saved. Continue without saving?')
            }).then(value => {
                if (value.button.accept) {
                    this.dispose();
                    super.onCloseRequest(msg);
                }
            });
        }
        else {
            this.dispose();
            super.onCloseRequest(msg);
        }
    }
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/codeeditor@~4.1.0-alpha.2 (singleton) (fallback: ../packages/codeeditor/lib/index.js)
var codeeditor_lib_index_js_ = __webpack_require__(40200);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/inspector@~4.1.0-alpha.2 (singleton) (fallback: ../packages/inspector/lib/index.js)
var inspector_lib_index_js_ = __webpack_require__(79891);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/rendermime@~4.1.0-alpha.2 (singleton) (fallback: ../packages/rendermime/lib/index.js)
var rendermime_lib_index_js_ = __webpack_require__(66866);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/statedb@~4.1.0-alpha.2 (singleton) (fallback: ../packages/statedb/lib/index.js)
var statedb_lib_index_js_ = __webpack_require__(1458);
;// CONCATENATED MODULE: ../packages/settingeditor/lib/inspector.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/




/**
 * Create a raw editor inspector.
 */
function createInspector(editor, rendermime, translator) {
    translator = translator || lib_index_js_.nullTranslator;
    const trans = translator.load('jupyterlab');
    const connector = new InspectorConnector(editor, translator);
    const inspector = new inspector_lib_index_js_.InspectorPanel({
        initialContent: trans.__('Any errors will be listed here'),
        translator: translator
    });
    const handler = new inspector_lib_index_js_.InspectionHandler({
        connector,
        rendermime: rendermime ||
            new rendermime_lib_index_js_.RenderMimeRegistry({
                initialFactories: rendermime_lib_index_js_.standardRendererFactories,
                translator: translator
            })
    });
    inspector.addClass('jp-SettingsDebug');
    inspector.source = handler;
    handler.editor = editor.source;
    return inspector;
}
/**
 * The data connector used to populate a code inspector.
 *
 * #### Notes
 * This data connector debounces fetch requests to throttle them at no more than
 * one request per 100ms. This means that using the connector to populate
 * multiple client objects can lead to missed fetch responses.
 */
class InspectorConnector extends statedb_lib_index_js_.DataConnector {
    constructor(editor, translator) {
        super();
        this._current = 0;
        this._editor = editor;
        this._trans = (translator !== null && translator !== void 0 ? translator : lib_index_js_.nullTranslator).load('jupyterlab');
    }
    /**
     * Fetch inspection requests.
     */
    fetch(request) {
        return new Promise(resolve => {
            // Debounce requests at a rate of 100ms.
            const current = (this._current = window.setTimeout(() => {
                if (current !== this._current) {
                    return resolve(undefined);
                }
                const errors = this._validate(request.text);
                if (!errors) {
                    return resolve({
                        data: { 'text/markdown': this._trans.__('No errors found') },
                        metadata: {}
                    });
                }
                resolve({ data: this.render(errors), metadata: {} });
            }, 100));
        });
    }
    /**
     * Render validation errors as an HTML string.
     */
    render(errors) {
        return {
            'text/markdown': errors.map(this.renderError.bind(this)).join('')
        };
    }
    /**
     * Render an individual validation error as a markdown string.
     */
    renderError(error) {
        var _a;
        switch (error.keyword) {
            case 'additionalProperties':
                return `**\`[${this._trans.__('additional property error')}]\`**
          ${this._trans.__('`%1` is not a valid property', (_a = error.params) === null || _a === void 0 ? void 0 : _a.additionalProperty)}`;
            case 'syntax':
                return `**\`[${this._trans.__('syntax error')}]\`** *${error.message}*`;
            case 'type':
                return `**\`[${this._trans.__('type error')}]\`**
          \`${error.instancePath}\` ${error.message}`;
            default:
                return `**\`[${this._trans.__('error')}]\`** *${error.message}*`;
        }
    }
    _validate(raw) {
        const editor = this._editor;
        if (!editor.settings) {
            return null;
        }
        const { id, schema, version } = editor.settings;
        const data = { composite: {}, user: {} };
        const validator = editor.registry.validator;
        return validator.validateData({ data, id, raw, schema, version }, false);
    }
}

;// CONCATENATED MODULE: ../packages/settingeditor/lib/raweditor.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






/**
 * A class name added to all raw editors.
 */
const RAW_EDITOR_CLASS = 'jp-SettingsRawEditor';
/**
 * A class name added to the user settings editor.
 */
const USER_CLASS = 'jp-SettingsRawEditor-user';
/**
 * A class name added to the user editor when there are validation errors.
 */
const ERROR_CLASS = 'jp-mod-error';
/**
 * A raw JSON settings editor.
 */
class RawEditor extends dist_index_es6_js_.SplitPanel {
    /**
     * Create a new plugin editor.
     */
    constructor(options) {
        super({
            orientation: 'horizontal',
            renderer: dist_index_es6_js_.SplitPanel.defaultRenderer,
            spacing: 1
        });
        this._canRevert = false;
        this._canSave = false;
        this._commandsChanged = new index_es6_js_.Signal(this);
        this._settings = null;
        this._toolbar = new ui_components_lib_index_js_.Toolbar();
        const { commands, editorFactory, registry, translator } = options;
        this.registry = registry;
        this.translator = translator || lib_index_js_.nullTranslator;
        this._commands = commands;
        // Create read-only defaults editor.
        const defaults = (this._defaults = new codeeditor_lib_index_js_.CodeEditorWrapper({
            editorOptions: {
                config: { readOnly: true }
            },
            model: new codeeditor_lib_index_js_.CodeEditor.Model({ mimeType: 'text/javascript' }),
            factory: editorFactory
        }));
        // Create read-write user settings editor.
        const user = (this._user = new codeeditor_lib_index_js_.CodeEditorWrapper({
            editorOptions: {
                config: { lineNumbers: true }
            },
            model: new codeeditor_lib_index_js_.CodeEditor.Model({ mimeType: 'text/javascript' }),
            factory: editorFactory
        }));
        user.addClass(USER_CLASS);
        user.editor.model.sharedModel.changed.connect(this._onTextChanged, this);
        // Create and set up an inspector.
        this._inspector = createInspector(this, options.rendermime, this.translator);
        this.addClass(RAW_EDITOR_CLASS);
        this._onSaveError = options.onSaveError;
        this.addWidget(Private.defaultsEditor(defaults, this.translator));
        this.addWidget(Private.userEditor(user, this._toolbar, this._inspector, this.translator));
    }
    /**
     * Whether the raw editor revert functionality is enabled.
     */
    get canRevert() {
        return this._canRevert;
    }
    /**
     * Whether the raw editor save functionality is enabled.
     */
    get canSave() {
        return this._canSave;
    }
    /**
     * Emits when the commands passed in at instantiation change.
     */
    get commandsChanged() {
        return this._commandsChanged;
    }
    /**
     * Tests whether the settings have been modified and need saving.
     */
    get isDirty() {
        var _a, _b;
        return ((_b = this._user.editor.model.sharedModel.getSource() !== ((_a = this._settings) === null || _a === void 0 ? void 0 : _a.raw)) !== null && _b !== void 0 ? _b : '');
    }
    /**
     * The plugin settings being edited.
     */
    get settings() {
        return this._settings;
    }
    set settings(settings) {
        if (!settings && !this._settings) {
            return;
        }
        const samePlugin = settings && this._settings && settings.plugin === this._settings.plugin;
        if (samePlugin) {
            return;
        }
        const defaults = this._defaults;
        const user = this._user;
        // Disconnect old settings change handler.
        if (this._settings) {
            this._settings.changed.disconnect(this._onSettingsChanged, this);
        }
        if (settings) {
            this._settings = settings;
            this._settings.changed.connect(this._onSettingsChanged, this);
            this._onSettingsChanged();
        }
        else {
            this._settings = null;
            defaults.editor.model.sharedModel.setSource('');
            user.editor.model.sharedModel.setSource('');
        }
        this.update();
    }
    /**
     * Get the relative sizes of the two editor panels.
     */
    get sizes() {
        return this.relativeSizes();
    }
    set sizes(sizes) {
        this.setRelativeSizes(sizes);
    }
    /**
     * The inspectable source editor for user input.
     */
    get source() {
        return this._user.editor;
    }
    /**
     * Dispose of the resources held by the raw editor.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._defaults.model.dispose();
        this._defaults.dispose();
        this._user.model.dispose();
        this._user.dispose();
        super.dispose();
    }
    /**
     * Revert the editor back to original settings.
     */
    revert() {
        var _a, _b;
        this._user.editor.model.sharedModel.setSource((_b = (_a = this.settings) === null || _a === void 0 ? void 0 : _a.raw) !== null && _b !== void 0 ? _b : '');
        this._updateToolbar(false, false);
    }
    /**
     * Save the contents of the raw editor.
     */
    save() {
        if (!this.isDirty || !this._settings) {
            return Promise.resolve(undefined);
        }
        const settings = this._settings;
        const source = this._user.editor.model.sharedModel.getSource();
        return settings
            .save(source)
            .then(() => {
            this._updateToolbar(false, false);
        })
            .catch(reason => {
            this._updateToolbar(true, false);
            this._onSaveError(reason, this.translator);
        });
    }
    /**
     * Handle `after-attach` messages.
     */
    onAfterAttach(msg) {
        Private.populateToolbar(this._commands, this._toolbar);
        this.update();
    }
    /**
     * Handle text changes in the underlying editor.
     */
    _onTextChanged() {
        const raw = this._user.editor.model.sharedModel.getSource();
        const settings = this._settings;
        this.removeClass(ERROR_CLASS);
        // If there are no settings loaded or there are no changes, bail.
        if (!settings || settings.raw === raw) {
            this._updateToolbar(false, false);
            return;
        }
        const errors = settings.validate(raw);
        if (errors) {
            this.addClass(ERROR_CLASS);
            this._updateToolbar(true, false);
            return;
        }
        this._updateToolbar(true, true);
    }
    /**
     * Handle updates to the settings.
     */
    _onSettingsChanged() {
        var _a, _b;
        const settings = this._settings;
        const defaults = this._defaults;
        const user = this._user;
        defaults.editor.model.sharedModel.setSource((_a = settings === null || settings === void 0 ? void 0 : settings.annotatedDefaults()) !== null && _a !== void 0 ? _a : '');
        user.editor.model.sharedModel.setSource((_b = settings === null || settings === void 0 ? void 0 : settings.raw) !== null && _b !== void 0 ? _b : '');
    }
    _updateToolbar(revert = this._canRevert, save = this._canSave) {
        const commands = this._commands;
        this._canRevert = revert;
        this._canSave = save;
        this._commandsChanged.emit([commands.revert, commands.save]);
    }
}
/**
 * A namespace for private module data.
 */
var Private;
(function (Private) {
    /**
     * Returns the wrapped setting defaults editor.
     */
    function defaultsEditor(editor, translator) {
        translator = translator || lib_index_js_.nullTranslator;
        const trans = translator.load('jupyterlab');
        const widget = new dist_index_es6_js_.Widget();
        const layout = (widget.layout = new dist_index_es6_js_.BoxLayout({ spacing: 0 }));
        const banner = new dist_index_es6_js_.Widget();
        const bar = new ui_components_lib_index_js_.Toolbar();
        const defaultTitle = trans.__('System Defaults');
        banner.node.innerText = defaultTitle;
        bar.insertItem(0, 'banner', banner);
        layout.addWidget(bar);
        layout.addWidget(editor);
        return widget;
    }
    Private.defaultsEditor = defaultsEditor;
    /**
     * Populate the raw editor toolbar.
     */
    function populateToolbar(commands, toolbar) {
        const { registry, revert, save } = commands;
        toolbar.addItem('spacer', ui_components_lib_index_js_.Toolbar.createSpacerItem());
        // Note the button order. The rationale here is that no matter what state
        // the toolbar is in, the relative location of the revert button in the
        // toolbar remains the same.
        [revert, save].forEach(name => {
            const item = new ui_components_lib_index_js_.CommandToolbarButton({ commands: registry, id: name });
            toolbar.addItem(name, item);
        });
    }
    Private.populateToolbar = populateToolbar;
    /**
     * Returns the wrapped user overrides editor.
     */
    function userEditor(editor, toolbar, inspector, translator) {
        translator = translator || lib_index_js_.nullTranslator;
        const trans = translator.load('jupyterlab');
        const userTitle = trans.__('User Preferences');
        const widget = new dist_index_es6_js_.Widget();
        const layout = (widget.layout = new dist_index_es6_js_.BoxLayout({ spacing: 0 }));
        const banner = new dist_index_es6_js_.Widget();
        banner.node.innerText = userTitle;
        toolbar.insertItem(0, 'banner', banner);
        layout.addWidget(toolbar);
        layout.addWidget(editor);
        layout.addWidget(inspector);
        return widget;
    }
    Private.userEditor = userEditor;
})(Private || (Private = {}));

;// CONCATENATED MODULE: ../packages/settingeditor/lib/plugineditor.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/






/**
 * The class name added to all plugin editors.
 */
const PLUGIN_EDITOR_CLASS = 'jp-PluginEditor';
/**
 * An individual plugin settings editor.
 */
class PluginEditor extends dist_index_es6_js_.Widget {
    /**
     * Create a new plugin editor.
     *
     * @param options - The plugin editor instantiation options.
     */
    constructor(options) {
        super();
        this._settings = null;
        this._stateChanged = new index_es6_js_.Signal(this);
        this.addClass(PLUGIN_EDITOR_CLASS);
        const { commands, editorFactory, registry, rendermime, translator } = options;
        this.translator = translator || lib_index_js_.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        // TODO: Remove this layout. We were using this before when we
        // when we had a way to switch between the raw and table editor
        // Now, the raw editor is the only child and probably could merged into
        // this class directly in the future.
        const layout = (this.layout = new dist_index_es6_js_.StackedLayout());
        const { onSaveError } = plugineditor_Private;
        this.raw = this._rawEditor = new RawEditor({
            commands,
            editorFactory,
            onSaveError,
            registry,
            rendermime,
            translator
        });
        this._rawEditor.handleMoved.connect(this._onStateChanged, this);
        layout.addWidget(this._rawEditor);
    }
    /**
     * Tests whether the settings have been modified and need saving.
     */
    get isDirty() {
        return this._rawEditor.isDirty;
    }
    /**
     * The plugin settings being edited.
     */
    get settings() {
        return this._settings;
    }
    set settings(settings) {
        if (this._settings === settings) {
            return;
        }
        const raw = this._rawEditor;
        this._settings = raw.settings = settings;
        this.update();
    }
    /**
     * The plugin editor layout state.
     */
    get state() {
        const plugin = this._settings ? this._settings.id : '';
        const { sizes } = this._rawEditor;
        return { plugin, sizes };
    }
    set state(state) {
        if (dist_index_js_.JSONExt.deepEqual(this.state, state)) {
            return;
        }
        this._rawEditor.sizes = state.sizes;
        this.update();
    }
    /**
     * A signal that emits when editor layout state changes and needs to be saved.
     */
    get stateChanged() {
        return this._stateChanged;
    }
    /**
     * If the editor is in a dirty state, confirm that the user wants to leave.
     */
    confirm() {
        if (this.isHidden || !this.isAttached || !this.isDirty) {
            return Promise.resolve(undefined);
        }
        return (0,index_js_.showDialog)({
            title: this._trans.__('You have unsaved changes.'),
            body: this._trans.__('Do you want to leave without saving?'),
            buttons: [
                index_js_.Dialog.cancelButton({ label: this._trans.__('Cancel') }),
                index_js_.Dialog.okButton({ label: this._trans.__('Ok') })
            ]
        }).then(result => {
            if (!result.button.accept) {
                throw new Error('User canceled.');
            }
        });
    }
    /**
     * Dispose of the resources held by the plugin editor.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        super.dispose();
        this._rawEditor.dispose();
    }
    /**
     * Handle `after-attach` messages.
     */
    onAfterAttach(msg) {
        this.update();
    }
    /**
     * Handle `'update-request'` messages.
     */
    onUpdateRequest(msg) {
        const raw = this._rawEditor;
        const settings = this._settings;
        if (!settings) {
            this.hide();
            return;
        }
        this.show();
        raw.show();
    }
    /**
     * Handle layout state changes that need to be saved.
     */
    _onStateChanged() {
        this.stateChanged.emit(undefined);
    }
}
/**
 * A namespace for private module data.
 */
var plugineditor_Private;
(function (Private) {
    /**
     * Handle save errors.
     */
    function onSaveError(reason, translator) {
        translator = translator || lib_index_js_.nullTranslator;
        const trans = translator.load('jupyterlab');
        console.error(`Saving setting editor value failed: ${reason.message}`);
        void (0,index_js_.showErrorMessage)(trans.__('Your changes were not saved.'), reason);
    }
    Private.onSaveError = onSaveError;
})(plugineditor_Private || (plugineditor_Private = {}));

;// CONCATENATED MODULE: ../packages/settingeditor/lib/jsonsettingeditor.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/








/**
 * The ratio panes in the setting editor.
 */
const DEFAULT_LAYOUT = {
    sizes: [1, 3],
    container: {
        editor: 'raw',
        plugin: '',
        sizes: [1, 1]
    }
};
/**
 * An interface for modifying and saving application settings.
 */
class JsonSettingEditor extends dist_index_es6_js_.SplitPanel {
    /**
     * Create a new setting editor.
     */
    constructor(options) {
        super({
            orientation: 'horizontal',
            renderer: dist_index_es6_js_.SplitPanel.defaultRenderer,
            spacing: 1
        });
        this._fetching = null;
        this._saving = false;
        this._state = dist_index_js_.JSONExt.deepCopy(DEFAULT_LAYOUT);
        this.translator = options.translator || lib_index_js_.nullTranslator;
        this.addClass('jp-SettingEditor');
        this.key = options.key;
        this.state = options.state;
        const { commands, editorFactory, rendermime } = options;
        const registry = (this.registry = options.registry);
        const instructions = (this._instructions = ui_components_lib_index_js_.ReactWidget.create(react_index_js_.createElement(SettingsEditorPlaceholder, { translator: this.translator })));
        instructions.addClass('jp-SettingEditorInstructions');
        const editor = (this._editor = new PluginEditor({
            commands,
            editorFactory,
            registry,
            rendermime,
            translator: this.translator
        }));
        const confirm = () => editor.confirm();
        const list = (this._list = new PluginList({
            confirm,
            registry,
            translator: this.translator
        }));
        const when = options.when;
        if (when) {
            this._when = Array.isArray(when) ? Promise.all(when) : when;
        }
        this.addWidget(list);
        this.addWidget(instructions);
        dist_index_es6_js_.SplitPanel.setStretch(list, 0);
        dist_index_es6_js_.SplitPanel.setStretch(instructions, 1);
        dist_index_es6_js_.SplitPanel.setStretch(editor, 1);
        editor.stateChanged.connect(this._onStateChanged, this);
        list.changed.connect(this._onStateChanged, this);
        this.handleMoved.connect(this._onStateChanged, this);
    }
    /**
     * Whether the raw editor revert functionality is enabled.
     */
    get canRevertRaw() {
        return this._editor.raw.canRevert;
    }
    /**
     * Whether the raw editor save functionality is enabled.
     */
    get canSaveRaw() {
        return this._editor.raw.canSave;
    }
    /**
     * Emits when the commands passed in at instantiation change.
     */
    get commandsChanged() {
        return this._editor.raw.commandsChanged;
    }
    /**
     * The currently loaded settings.
     */
    get settings() {
        return this._editor.settings;
    }
    /**
     * The inspectable raw user editor source for the currently loaded settings.
     */
    get source() {
        return this._editor.raw.source;
    }
    /**
     * Dispose of the resources held by the setting editor.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        super.dispose();
        this._editor.dispose();
        this._instructions.dispose();
        this._list.dispose();
    }
    /**
     * Revert raw editor back to original settings.
     */
    revert() {
        this._editor.raw.revert();
    }
    /**
     * Save the contents of the raw editor.
     */
    save() {
        return this._editor.raw.save();
    }
    /**
     * Handle `'after-attach'` messages.
     */
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        this.hide();
        this._fetchState()
            .then(() => {
            this.show();
            this._setState();
        })
            .catch(reason => {
            console.error('Fetching setting editor state failed', reason);
            this.show();
            this._setState();
        });
    }
    /**
     * Handle `'close-request'` messages.
     */
    onCloseRequest(msg) {
        this._editor
            .confirm()
            .then(() => {
            super.onCloseRequest(msg);
            this.dispose();
        })
            .catch(() => {
            /* no op */
        });
    }
    /**
     * Get the state of the panel.
     */
    _fetchState() {
        if (this._fetching) {
            return this._fetching;
        }
        const { key, state } = this;
        const promises = [state.fetch(key), this._when];
        return (this._fetching = Promise.all(promises).then(([value]) => {
            this._fetching = null;
            if (this._saving) {
                return;
            }
            this._state = jsonsettingeditor_Private.normalizeState(value, this._state);
        }));
    }
    /**
     * Handle root level layout state changes.
     */
    async _onStateChanged() {
        this._state.sizes = this.relativeSizes();
        this._state.container = this._editor.state;
        this._state.container.plugin = this._list.selection;
        try {
            await this._saveState();
        }
        catch (error) {
            console.error('Saving setting editor state failed', error);
        }
        this._setState();
    }
    /**
     * Set the state of the setting editor.
     */
    async _saveState() {
        const { key, state } = this;
        const value = this._state;
        this._saving = true;
        try {
            await state.save(key, value);
            this._saving = false;
        }
        catch (error) {
            this._saving = false;
            throw error;
        }
    }
    /**
     * Set the layout sizes.
     */
    _setLayout() {
        const editor = this._editor;
        const state = this._state;
        editor.state = state.container;
        // Allow the message queue (which includes fit requests that might disrupt
        // setting relative sizes) to clear before setting sizes.
        requestAnimationFrame(() => {
            this.setRelativeSizes(state.sizes);
        });
    }
    /**
     * Set the presets of the setting editor.
     */
    _setState() {
        const editor = this._editor;
        const list = this._list;
        const { container } = this._state;
        if (!container.plugin) {
            editor.settings = null;
            list.selection = '';
            this._setLayout();
            return;
        }
        if (editor.settings && editor.settings.id === container.plugin) {
            this._setLayout();
            return;
        }
        const instructions = this._instructions;
        this.registry
            .load(container.plugin)
            .then(settings => {
            if (instructions.isAttached) {
                instructions.parent = null;
            }
            if (!editor.isAttached) {
                this.addWidget(editor);
            }
            editor.settings = settings;
            list.selection = container.plugin;
            this._setLayout();
        })
            .catch(reason => {
            console.error(`Loading ${container.plugin} settings failed.`, reason);
            list.selection = this._state.container.plugin = '';
            editor.settings = null;
            this._setLayout();
        });
    }
}
/**
 * A namespace for private module data.
 */
var jsonsettingeditor_Private;
(function (Private) {
    /**
     * Return a normalized restored layout state that defaults to the presets.
     */
    function normalizeState(saved, current) {
        if (!saved) {
            return dist_index_js_.JSONExt.deepCopy(DEFAULT_LAYOUT);
        }
        if (!('sizes' in saved) || !numberArray(saved.sizes)) {
            saved.sizes = dist_index_js_.JSONExt.deepCopy(DEFAULT_LAYOUT.sizes);
        }
        if (!('container' in saved)) {
            saved.container = dist_index_js_.JSONExt.deepCopy(DEFAULT_LAYOUT.container);
            return saved;
        }
        const container = 'container' in saved &&
            saved.container &&
            typeof saved.container === 'object'
            ? saved.container
            : {};
        saved.container = {
            plugin: typeof container.plugin === 'string'
                ? container.plugin
                : DEFAULT_LAYOUT.container.plugin,
            sizes: numberArray(container.sizes)
                ? container.sizes
                : dist_index_js_.JSONExt.deepCopy(DEFAULT_LAYOUT.container.sizes)
        };
        return saved;
    }
    Private.normalizeState = normalizeState;
    /**
     * Tests whether an array consists exclusively of numbers.
     */
    function numberArray(value) {
        return Array.isArray(value) && value.every(x => typeof x === 'number');
    }
})(jsonsettingeditor_Private || (jsonsettingeditor_Private = {}));

// EXTERNAL MODULE: ../packages/settingeditor/lib/tokens.js
var tokens = __webpack_require__(45104);
;// CONCATENATED MODULE: ../packages/settingeditor/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module settingeditor
 */





/***/ })

}]);
//# sourceMappingURL=6417.3bf4469b6ed45ea6f15c.js.map?v=3bf4469b6ed45ea6f15c