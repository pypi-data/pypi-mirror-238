"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[6765],{

/***/ 66765:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "default": () => (/* binding */ lib)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/completer@~4.1.0-alpha.2 (singleton) (fallback: ../packages/completer/lib/index.js)
var index_js_ = __webpack_require__(4532);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/settingregistry@~4.1.0-alpha.2 (singleton) (fallback: ../packages/settingregistry/lib/index.js)
var lib_index_js_ = __webpack_require__(89397);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
var react_index_js_default = /*#__PURE__*/__webpack_require__.n(react_index_js_);
;// CONCATENATED MODULE: ../packages/completer-extension/lib/renderer.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

const AVAILABLE_PROVIDERS = 'availableProviders';
/**
 * Custom setting renderer for provider rank.
 */
function renderAvailableProviders(props) {
    const { schema } = props;
    const title = schema.title;
    const desc = schema.description;
    const settings = props.formContext.settings;
    const userData = settings.get(AVAILABLE_PROVIDERS).user;
    const items = {
        ...schema.default
    };
    if (userData) {
        for (const key of Object.keys(items)) {
            if (key in userData) {
                items[key] = userData[key];
            }
            else {
                items[key] = -1;
            }
        }
    }
    const [settingValue, setValue] = (0,react_index_js_.useState)(items);
    const onSettingChange = (key, e) => {
        const newValue = {
            ...settingValue,
            [key]: parseInt(e.target.value)
        };
        settings.set(AVAILABLE_PROVIDERS, newValue).catch(console.error);
        setValue(newValue);
    };
    return (
    //TODO Remove hard coded class names
    react_index_js_default().createElement("div", null,
        react_index_js_default().createElement("fieldset", null,
            react_index_js_default().createElement("legend", null, title),
            react_index_js_default().createElement("p", { className: "field-description" }, desc),
            Object.keys(items).map(key => {
                return (react_index_js_default().createElement("div", { key: key, className: "form-group small-field" },
                    react_index_js_default().createElement("div", null,
                        react_index_js_default().createElement("h3", null,
                            " ",
                            key),
                        react_index_js_default().createElement("div", { className: "inputFieldWrapper" },
                            react_index_js_default().createElement("input", { className: "form-control", type: "number", value: settingValue[key], onChange: e => {
                                    onSettingChange(key, e);
                                } })))));
            }))));
}

;// CONCATENATED MODULE: ../packages/completer-extension/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module completer-extension
 */




const COMPLETION_MANAGER_PLUGIN = '@jupyterlab/completer-extension:manager';
const defaultProvider = {
    id: '@jupyterlab/completer-extension:base-service',
    description: 'Adds context and kernel completion providers.',
    requires: [index_js_.ICompletionProviderManager],
    autoStart: true,
    activate: (app, completionManager) => {
        completionManager.registerProvider(new index_js_.ContextCompleterProvider());
        completionManager.registerProvider(new index_js_.KernelCompleterProvider());
    }
};
const manager = {
    id: COMPLETION_MANAGER_PLUGIN,
    description: 'Provides the completion provider manager.',
    requires: [lib_index_js_.ISettingRegistry],
    optional: [ui_components_lib_index_js_.IFormRendererRegistry],
    provides: index_js_.ICompletionProviderManager,
    autoStart: true,
    activate: (app, settings, editorRegistry) => {
        const AVAILABLE_PROVIDERS = 'availableProviders';
        const PROVIDER_TIMEOUT = 'providerTimeout';
        const SHOW_DOCUMENT_PANEL = 'showDocumentationPanel';
        const CONTINUOUS_HINTING = 'autoCompletion';
        const manager = new index_js_.CompletionProviderManager();
        const updateSetting = (settingValues, availableProviders) => {
            var _a;
            const providersData = settingValues.get(AVAILABLE_PROVIDERS);
            const timeout = settingValues.get(PROVIDER_TIMEOUT);
            const showDoc = settingValues.get(SHOW_DOCUMENT_PANEL);
            const continuousHinting = settingValues.get(CONTINUOUS_HINTING);
            manager.setTimeout(timeout.composite);
            manager.setShowDocumentationPanel(showDoc.composite);
            manager.setContinuousHinting(continuousHinting.composite);
            const selectedProviders = (_a = providersData.user) !== null && _a !== void 0 ? _a : providersData.composite;
            const sortedProviders = Object.entries(selectedProviders !== null && selectedProviders !== void 0 ? selectedProviders : {})
                .filter(val => val[1] >= 0 && availableProviders.includes(val[0]))
                .sort(([, rank1], [, rank2]) => rank2 - rank1)
                .map(item => item[0]);
            manager.activateProvider(sortedProviders);
        };
        app.restored
            .then(() => {
            const availableProviders = [...manager.getProviders().entries()];
            const availableProviderIDs = availableProviders.map(([key, value]) => key);
            settings.transform(COMPLETION_MANAGER_PLUGIN, {
                fetch: plugin => {
                    const schema = plugin.schema.properties;
                    const defaultValue = {};
                    availableProviders.forEach(([key, value], index) => {
                        var _a;
                        defaultValue[key] = (_a = value.rank) !== null && _a !== void 0 ? _a : (index + 1) * 10;
                    });
                    schema[AVAILABLE_PROVIDERS]['default'] = defaultValue;
                    return plugin;
                }
            });
            const settingsPromise = settings.load(COMPLETION_MANAGER_PLUGIN);
            settingsPromise
                .then(settingValues => {
                updateSetting(settingValues, availableProviderIDs);
                settingValues.changed.connect(newSettings => {
                    updateSetting(newSettings, availableProviderIDs);
                });
            })
                .catch(console.error);
        })
            .catch(console.error);
        if (editorRegistry) {
            const renderer = {
                fieldRenderer: (props) => {
                    return renderAvailableProviders(props);
                }
            };
            editorRegistry.addRenderer(`${COMPLETION_MANAGER_PLUGIN}.availableProviders`, renderer);
        }
        return manager;
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [manager, defaultProvider];
/* harmony default export */ const lib = (plugins);


/***/ })

}]);
//# sourceMappingURL=6765.2fb32188db6cc420bd2a.js.map?v=2fb32188db6cc420bd2a