"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[362],{

/***/ 20362:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "RunningLanguageServer": () => (/* binding */ RunningLanguageServer),
  "default": () => (/* binding */ lib)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/lsp@~4.1.0-alpha.2 (singleton) (fallback: ../packages/lsp/lib/index.js)
var index_js_ = __webpack_require__(84144);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/running@~4.1.0-alpha.2 (strict) (fallback: ../packages/running/lib/index.js)
var lib_index_js_ = __webpack_require__(42319);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/settingregistry@~4.1.0-alpha.2 (singleton) (fallback: ../packages/settingregistry/lib/index.js)
var settingregistry_lib_index_js_ = __webpack_require__(89397);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(30205);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @lumino/polling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/polling/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(81967);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
var react_index_js_default = /*#__PURE__*/__webpack_require__.n(react_index_js_);
;// CONCATENATED MODULE: ../packages/lsp-extension/lib/renderer.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




const SETTING_NAME = 'languageServers';
const SERVER_SETTINGS = 'configuration';
/**
 * The React component of the setting field
 */
function BuildSettingForm(props) {
    const { [SERVER_SETTINGS]: serverSettingsSchema, ...otherSettingsSchema } = props.schema;
    const { [SERVER_SETTINGS]: serverSettings, serverName, ...otherSettings } = props.settings;
    const [currentServerName, setCurrentServerName] = (0,react_index_js_.useState)(serverName);
    /**
     * Callback on server name field change event
     */
    const onServerNameChange = (e) => {
        props.updateSetting
            .invoke(props.serverHash, {
            serverName: e.target.value
        })
            .catch(console.error);
        setCurrentServerName(e.target.value);
    };
    const serverSettingWithType = {};
    Object.entries(serverSettings).forEach(([key, value]) => {
        const newProps = {
            property: key,
            type: typeof value,
            value
        };
        serverSettingWithType[dist_index_js_.UUID.uuid4()] = newProps;
    });
    const [propertyMap, setPropertyMap] = (0,react_index_js_.useState)(serverSettingWithType);
    const defaultOtherSettings = {};
    Object.entries(otherSettingsSchema).forEach(([key, value]) => {
        if (key in otherSettings) {
            defaultOtherSettings[key] = otherSettings[key];
        }
        else {
            defaultOtherSettings[key] = value['default'];
        }
    });
    const [otherSettingsComposite, setOtherSettingsComposite] = (0,react_index_js_.useState)(defaultOtherSettings);
    /**
     * Callback on additional setting field change event
     */
    const onOtherSettingsChange = (property, value, type) => {
        let settingValue = value;
        if (type === 'number') {
            settingValue = parseFloat(value);
        }
        const newProps = {
            ...otherSettingsComposite,
            [property]: settingValue
        };
        props.updateSetting.invoke(props.serverHash, newProps).catch(console.error);
        setOtherSettingsComposite(newProps);
    };
    /**
     * Callback on `Add property` button click event.
     */
    const addProperty = () => {
        const hash = dist_index_js_.UUID.uuid4();
        const newMap = {
            ...propertyMap,
            [hash]: { property: '', type: 'string', value: '' }
        };
        const payload = {};
        Object.values(newMap).forEach(value => {
            payload[value.property] = value.value;
        });
        props.updateSetting
            .invoke(props.serverHash, {
            [SERVER_SETTINGS]: payload
        })
            .catch(console.error);
        setPropertyMap(newMap);
    };
    /**
     * Callback on `Remove property` button click event.
     */
    const removeProperty = (entryHash) => {
        const newMap = {};
        Object.entries(propertyMap).forEach(([hash, value]) => {
            if (hash !== entryHash) {
                newMap[hash] = value;
            }
            const payload = {};
            Object.values(newMap).forEach(value => {
                payload[value.property] = value.value;
            });
            props.updateSetting
                .invoke(props.serverHash, {
                [SERVER_SETTINGS]: payload
            })
                .catch(console.error);
            setPropertyMap(newMap);
        });
    };
    /**
     * Save setting to the setting registry on field change event.
     */
    const setProperty = (hash, property) => {
        if (hash in propertyMap) {
            const newMap = { ...propertyMap, [hash]: property };
            const payload = {};
            Object.values(newMap).forEach(value => {
                payload[value.property] = value.value;
            });
            setPropertyMap(newMap);
            props.updateSetting
                .invoke(props.serverHash, {
                [SERVER_SETTINGS]: payload
            })
                .catch(console.error);
        }
    };
    const debouncedSetProperty = new dist_index_es6_js_.Debouncer(setProperty);
    return (react_index_js_default().createElement("div", { className: "array-item" },
        react_index_js_default().createElement("div", { className: "form-group " },
            react_index_js_default().createElement("div", { className: "jp-FormGroup-content" },
                react_index_js_default().createElement("div", { className: "jp-objectFieldWrapper" },
                    react_index_js_default().createElement("fieldset", null,
                        react_index_js_default().createElement("div", { className: "form-group small-field" },
                            react_index_js_default().createElement("div", { className: "jp-modifiedIndicator jp-errorIndicator" }),
                            react_index_js_default().createElement("div", { className: "jp-FormGroup-content" },
                                react_index_js_default().createElement("h3", { className: "jp-FormGroup-fieldLabel jp-FormGroup-contentItem" }, props.trans.__('Server name:')),
                                react_index_js_default().createElement("div", { className: "jp-inputFieldWrapper jp-FormGroup-contentItem" },
                                    react_index_js_default().createElement("input", { className: "form-control", type: "text", required: true, value: currentServerName, onChange: e => {
                                            onServerNameChange(e);
                                        } })),
                                react_index_js_default().createElement("div", { className: "validationErrors" },
                                    react_index_js_default().createElement("div", null,
                                        react_index_js_default().createElement("ul", { className: "error-detail bs-callout bs-callout-info" },
                                            react_index_js_default().createElement("li", { className: "text-danger" }, props.trans.__('is a required property'))))))),
                        Object.entries(otherSettingsSchema).map(([property, value], idx) => {
                            return (react_index_js_default().createElement("div", { key: `${idx}-${property}`, className: "form-group small-field" },
                                react_index_js_default().createElement("div", { className: "jp-FormGroup-content" },
                                    react_index_js_default().createElement("h3", { className: "jp-FormGroup-fieldLabel jp-FormGroup-contentItem" }, value.title),
                                    react_index_js_default().createElement("div", { className: "jp-inputFieldWrapper jp-FormGroup-contentItem" },
                                        react_index_js_default().createElement("input", { className: "form-control", placeholder: "", type: value.type, value: otherSettingsComposite[property], onChange: e => onOtherSettingsChange(property, e.target.value, value.type) })),
                                    react_index_js_default().createElement("div", { className: "jp-FormGroup-description" }, value.description),
                                    react_index_js_default().createElement("div", { className: "validationErrors" }))));
                        }),
                        react_index_js_default().createElement("fieldset", null,
                            react_index_js_default().createElement("legend", null, serverSettingsSchema['title']),
                            Object.entries(propertyMap).map(([hash, property]) => {
                                return (react_index_js_default().createElement(PropertyFrom, { key: hash, hash: hash, property: property, removeProperty: removeProperty, setProperty: debouncedSetProperty }));
                            }),
                            react_index_js_default().createElement("span", null, serverSettingsSchema['description'])))))),
        react_index_js_default().createElement("div", { className: "jp-ArrayOperations" },
            react_index_js_default().createElement("button", { className: "jp-mod-styled jp-mod-reject", onClick: addProperty }, props.trans.__('Add property')),
            react_index_js_default().createElement("button", { className: "jp-mod-styled jp-mod-warn jp-FormGroup-removeButton", onClick: () => props.removeSetting(props.serverHash) }, props.trans.__('Remove server')))));
}
function PropertyFrom(props) {
    const [state, setState] = (0,react_index_js_.useState)({ ...props.property });
    const TYPE_MAP = { string: 'text', number: 'number', boolean: 'checkbox' };
    const removeItem = () => {
        props.removeProperty(props.hash);
    };
    const changeName = (newName) => {
        const newState = { ...state, property: newName };
        props.setProperty.invoke(props.hash, newState).catch(console.error);
        setState(newState);
    };
    const changeValue = (newValue, type) => {
        let value = newValue;
        if (type === 'number') {
            value = parseFloat(newValue);
        }
        const newState = { ...state, value };
        props.setProperty.invoke(props.hash, newState).catch(console.error);
        setState(newState);
    };
    const changeType = (newType) => {
        let value;
        if (newType === 'boolean') {
            value = false;
        }
        else if (newType === 'number') {
            value = 0;
        }
        else {
            value = '';
        }
        const newState = { ...state, type: newType, value };
        setState(newState);
        props.setProperty.invoke(props.hash, newState).catch(console.error);
    };
    return (react_index_js_default().createElement("div", { key: props.hash, className: "form-group small-field" },
        react_index_js_default().createElement("div", { className: "jp-FormGroup-content jp-LSPExtension-FormGroup-content" },
            react_index_js_default().createElement("input", { className: "form-control", type: "text", required: true, placeholder: 'Property name', value: state.property, onChange: e => {
                    changeName(e.target.value);
                } }),
            react_index_js_default().createElement("select", { className: "form-control", value: state.type, onChange: e => changeType(e.target.value) },
                react_index_js_default().createElement("option", { value: "string" }, "String"),
                react_index_js_default().createElement("option", { value: "number" }, "Number"),
                react_index_js_default().createElement("option", { value: "boolean" }, "Boolean")),
            react_index_js_default().createElement("input", { className: "form-control", type: TYPE_MAP[state.type], required: false, placeholder: 'Property value', value: state.type !== 'boolean' ? state.value : undefined, checked: state.type === 'boolean' ? state.value : undefined, onChange: state.type !== 'boolean'
                    ? e => changeValue(e.target.value, state.type)
                    : e => changeValue(e.target.checked, state.type) }),
            react_index_js_default().createElement("button", { className: "jp-mod-minimal jp-Button", onClick: removeItem },
                react_index_js_default().createElement(ui_components_lib_index_js_.closeIcon.react, null)))));
}
/**
 * React setting component
 */
class SettingRenderer extends (react_index_js_default()).Component {
    constructor(props) {
        super(props);
        /**
         * Remove a setting item by its hash
         *
         * @param hash - hash of the item to be removed.
         */
        this.removeSetting = (hash) => {
            if (hash in this.state.items) {
                const items = {};
                for (const key in this.state.items) {
                    if (key !== hash) {
                        items[key] = this.state.items[key];
                    }
                }
                this.setState(old => {
                    return { ...old, items };
                }, () => {
                    this.saveServerSetting();
                });
            }
        };
        /**
         * Update a setting item by its hash
         *
         * @param hash - hash of the item to be updated.
         * @param newSetting - new setting value.
         */
        this.updateSetting = (hash, newSetting) => {
            if (hash in this.state.items) {
                const items = {};
                for (const key in this.state.items) {
                    if (key === hash) {
                        items[key] = { ...this.state.items[key], ...newSetting };
                    }
                    else {
                        items[key] = this.state.items[key];
                    }
                }
                this.setState(old => {
                    return { ...old, items };
                }, () => {
                    this.saveServerSetting();
                });
            }
        };
        /**
         * Add setting item to the setting component.
         */
        this.addServerSetting = () => {
            let index = 0;
            let key = 'newKey';
            while (Object.values(this.state.items)
                .map(val => val.serverName)
                .includes(key)) {
                index += 1;
                key = `newKey-${index}`;
            }
            this.setState(old => ({
                ...old,
                items: {
                    ...old.items,
                    [dist_index_js_.UUID.uuid4()]: { ...this._defaultSetting, serverName: key }
                }
            }), () => {
                this.saveServerSetting();
            });
        };
        /**
         * Save the value of setting items to the setting registry.
         */
        this.saveServerSetting = () => {
            const settings = {};
            Object.values(this.state.items).forEach(item => {
                const { serverName, ...setting } = item;
                settings[serverName] = setting;
            });
            this._setting.set(SETTING_NAME, settings).catch(console.error);
        };
        this._setting = props.formContext.settings;
        this._trans = props.translator.load('jupyterlab');
        const schema = this._setting.schema['definitions'];
        this._defaultSetting = schema['languageServer']['default'];
        this._schema = schema['languageServer']['properties'];
        const title = props.schema.title;
        const desc = props.schema.description;
        const settings = props.formContext.settings;
        const compositeData = settings.get(SETTING_NAME).composite;
        let items = {};
        if (compositeData) {
            Object.entries(compositeData).forEach(([key, value]) => {
                if (value) {
                    const hash = dist_index_js_.UUID.uuid4();
                    items[hash] = { serverName: key, ...value };
                }
            });
        }
        this.state = { title, desc, items };
        this._debouncedUpdateSetting = new dist_index_es6_js_.Debouncer(this.updateSetting.bind(this));
    }
    render() {
        return (react_index_js_default().createElement("div", null,
            react_index_js_default().createElement("fieldset", null,
                react_index_js_default().createElement("legend", null, this.state.title),
                react_index_js_default().createElement("p", { className: "field-description" }, this.state.desc),
                react_index_js_default().createElement("div", { className: "field field-array field-array-of-object" }, Object.entries(this.state.items).map(([hash, value], idx) => {
                    return (react_index_js_default().createElement(BuildSettingForm, { key: `${idx}-${hash}`, trans: this._trans, removeSetting: this.removeSetting, updateSetting: this._debouncedUpdateSetting, serverHash: hash, settings: value, schema: this._schema }));
                })),
                react_index_js_default().createElement("div", null,
                    react_index_js_default().createElement("button", { style: { margin: 2 }, className: "jp-mod-styled jp-mod-reject", onClick: this.addServerSetting }, this._trans.__('Add server'))))));
    }
}
/**
 * Custom setting renderer for language server extension.
 */
function renderServerSetting(props, translator) {
    return react_index_js_default().createElement(SettingRenderer, { ...props, translator: translator });
}

;// CONCATENATED MODULE: ../packages/lsp-extension/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module lsp-extension
 */







const lib_plugin = {
    activate,
    id: '@jupyterlab/lsp-extension:plugin',
    description: 'Provides the language server connection manager.',
    requires: [translation_lib_index_js_.ITranslator, index_js_.IWidgetLSPAdapterTracker],
    optional: [lib_index_js_.IRunningSessionManagers],
    provides: index_js_.ILSPDocumentConnectionManager,
    autoStart: true
};
const featurePlugin = {
    id: '@jupyterlab/lsp-extension:feature',
    description: 'Provides the language server feature manager.',
    activate: () => new index_js_.FeatureManager(),
    provides: index_js_.ILSPFeatureManager,
    autoStart: true
};
const settingsPlugin = {
    activate: activateSettings,
    id: '@jupyterlab/lsp-extension:settings',
    description: 'Provides the language server settings.',
    requires: [index_js_.ILSPDocumentConnectionManager, settingregistry_lib_index_js_.ISettingRegistry, translation_lib_index_js_.ITranslator],
    optional: [ui_components_lib_index_js_.IFormRendererRegistry],
    autoStart: true
};
const codeExtractorManagerPlugin = {
    id: index_js_.ILSPCodeExtractorsManager.name,
    description: 'Provides the code extractor manager.',
    activate: app => {
        const extractorManager = new index_js_.CodeExtractorsManager();
        const markdownCellExtractor = new index_js_.TextForeignCodeExtractor({
            language: 'markdown',
            isStandalone: false,
            file_extension: 'md',
            cellType: ['markdown']
        });
        extractorManager.register(markdownCellExtractor, null);
        const rawCellExtractor = new index_js_.TextForeignCodeExtractor({
            language: 'text',
            isStandalone: false,
            file_extension: 'txt',
            cellType: ['raw']
        });
        extractorManager.register(rawCellExtractor, null);
        return extractorManager;
    },
    provides: index_js_.ILSPCodeExtractorsManager,
    autoStart: true
};
/**
 * Activate the lsp plugin.
 */
function activate(app, translator, tracker, runningSessionManagers) {
    const languageServerManager = new index_js_.LanguageServerManager({
        settings: app.serviceManager.serverSettings
    });
    const connectionManager = new index_js_.DocumentConnectionManager({
        languageServerManager,
        adapterTracker: tracker
    });
    // Add a sessions manager if the running extension is available
    if (runningSessionManagers) {
        addRunningSessionManager(runningSessionManagers, connectionManager, translator);
    }
    return connectionManager;
}
/**
 * Activate the lsp settings plugin.
 */
function activateSettings(app, connectionManager, settingRegistry, translator, settingRendererRegistry) {
    const LANGUAGE_SERVERS = 'languageServers';
    const languageServerManager = connectionManager.languageServerManager;
    const updateOptions = (settings) => {
        const options = settings.composite;
        const languageServerSettings = (options.languageServers ||
            {});
        if (options.activate === 'on' && !languageServerManager.isEnabled) {
            languageServerManager.enable().catch(console.error);
        }
        else if (options.activate === 'off' && languageServerManager.isEnabled) {
            languageServerManager.disable();
            return;
        }
        connectionManager.initialConfigurations = languageServerSettings;
        // TODO: if priorities changed reset connections
        connectionManager.updateConfiguration(languageServerSettings);
        connectionManager.updateServerConfigurations(languageServerSettings);
        connectionManager.updateLogging(options.logAllCommunication, options.setTrace);
    };
    settingRegistry.transform(lib_plugin.id, {
        fetch: plugin => {
            const schema = plugin.schema.properties;
            const defaultValue = {};
            languageServerManager.sessions.forEach((_, key) => {
                defaultValue[key] = { rank: 50, configuration: {} };
            });
            schema[LANGUAGE_SERVERS]['default'] = defaultValue;
            return plugin;
        },
        compose: plugin => {
            const properties = plugin.schema.properties;
            const user = plugin.data.user;
            const serverDefaultSettings = properties[LANGUAGE_SERVERS]['default'];
            const serverUserSettings = user[LANGUAGE_SERVERS];
            let serverComposite = { ...serverDefaultSettings };
            if (serverUserSettings) {
                serverComposite = { ...serverComposite, ...serverUserSettings };
            }
            const composite = {
                [LANGUAGE_SERVERS]: serverComposite
            };
            Object.entries(properties).forEach(([key, value]) => {
                if (key !== LANGUAGE_SERVERS) {
                    if (key in user) {
                        composite[key] = user[key];
                    }
                    else {
                        composite[key] = value.default;
                    }
                }
            });
            plugin.data.composite = composite;
            return plugin;
        }
    });
    languageServerManager.sessionsChanged.connect(async () => {
        await settingRegistry.load(lib_plugin.id, true);
    });
    settingRegistry
        .load(lib_plugin.id)
        .then(settings => {
        updateOptions(settings);
        settings.changed.connect(() => {
            updateOptions(settings);
        });
        languageServerManager.disable();
    })
        .catch((reason) => {
        console.error(reason.message);
    });
    if (settingRendererRegistry) {
        const renderer = {
            fieldRenderer: (props) => {
                return renderServerSetting(props, translator);
            }
        };
        settingRendererRegistry.addRenderer(`${lib_plugin.id}.${LANGUAGE_SERVERS}`, renderer);
    }
}
class RunningLanguageServer {
    constructor(connection, manager) {
        this._connection = new WeakSet([connection]);
        this._manager = manager;
        this._serverIdentifier = connection.serverIdentifier;
        this._serverLanguage = connection.serverLanguage;
    }
    /**
     * This is no-op because we do not do anything on server click event
     */
    open() {
        /** no-op */
    }
    icon() {
        return ui_components_lib_index_js_.pythonIcon;
    }
    label() {
        var _a, _b;
        return `${(_a = this._serverIdentifier) !== null && _a !== void 0 ? _a : ''} (${(_b = this._serverLanguage) !== null && _b !== void 0 ? _b : ''})`;
    }
    shutdown() {
        for (const [key, value] of this._manager.connections.entries()) {
            if (this._connection.has(value)) {
                const { uri } = this._manager.documents.get(key);
                this._manager.unregisterDocument(uri);
            }
        }
        this._manager.disconnect(this._serverIdentifier);
    }
}
/**
 * Add the running terminal manager to the running panel.
 */
function addRunningSessionManager(managers, lsManager, translator) {
    const trans = translator.load('jupyterlab');
    const signal = new index_es6_js_.Signal(lsManager);
    lsManager.connected.connect(() => signal.emit(lsManager));
    lsManager.disconnected.connect(() => signal.emit(lsManager));
    lsManager.closed.connect(() => signal.emit(lsManager));
    lsManager.documentsChanged.connect(() => signal.emit(lsManager));
    let currentRunning = [];
    managers.add({
        name: trans.__('Language servers'),
        running: () => {
            const connections = new Set([...lsManager.connections.values()]);
            currentRunning = [...connections].map(conn => new RunningLanguageServer(conn, lsManager));
            return currentRunning;
        },
        shutdownAll: () => {
            currentRunning.forEach(item => {
                item.shutdown();
            });
        },
        refreshRunning: () => {
            return void 0;
        },
        runningChanged: signal,
        shutdownLabel: trans.__('Shut Down'),
        shutdownAllLabel: trans.__('Shut Down All'),
        shutdownAllConfirmationText: trans.__('Are you sure you want to permanently shut down all running language servers?')
    });
}
const adapterTrackerPlugin = {
    id: '@jupyterlab/lsp-extension:tracker',
    description: 'Provides the tracker of `WidgetLSPAdapter`.',
    autoStart: true,
    provides: index_js_.IWidgetLSPAdapterTracker,
    activate: (app) => {
        return new index_js_.WidgetLSPAdapterTracker({ shell: app.shell });
    }
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const lib = ([
    lib_plugin,
    featurePlugin,
    settingsPlugin,
    codeExtractorManagerPlugin,
    adapterTrackerPlugin
]);


/***/ })

}]);
//# sourceMappingURL=362.3ddaab83e2e5baea5907.js.map?v=3ddaab83e2e5baea5907