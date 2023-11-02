"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[129,9035],{

/***/ 59035:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "default": () => (/* binding */ lib),
  "lineColItem": () => (/* binding */ lineColItem)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/application@~4.1.0-alpha.2 (singleton) (fallback: ../packages/application/lib/index.js)
var index_js_ = __webpack_require__(65681);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/codeeditor@~4.1.0-alpha.2 (singleton) (fallback: ../packages/codeeditor/lib/index.js)
var lib_index_js_ = __webpack_require__(40200);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/statusbar@~4.1.0-alpha.2 (singleton) (fallback: ../packages/statusbar/lib/index.js)
var statusbar_lib_index_js_ = __webpack_require__(34853);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @codemirror/language@^6.0.0 (singleton) (fallback: ../node_modules/@codemirror/language/dist/index.js)
var dist_index_js_ = __webpack_require__(25025);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/codemirror@~4.1.0-alpha.2 (singleton) (fallback: ../packages/codemirror/lib/index.js)
var codemirror_lib_index_js_ = __webpack_require__(29239);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/settingregistry@~4.1.0-alpha.2 (singleton) (fallback: ../packages/settingregistry/lib/index.js)
var settingregistry_lib_index_js_ = __webpack_require__(89397);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var coreutils_dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @rjsf/validator-ajv8@^5.1.0 (strict) (fallback: ../node_modules/@rjsf/validator-ajv8/dist/validator-ajv8.esm.js)
var validator_ajv8_esm_js_ = __webpack_require__(89319);
var validator_ajv8_esm_js_default = /*#__PURE__*/__webpack_require__.n(validator_ajv8_esm_js_);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
var react_index_js_default = /*#__PURE__*/__webpack_require__.n(react_index_js_);
;// CONCATENATED MODULE: ../packages/codemirror-extension/lib/services.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */









/**
 * CodeMirror settings plugin ID
 */
const SETTINGS_ID = '@jupyterlab/codemirror-extension:plugin';
/**
 * CodeMirror language registry provider.
 */
const languagePlugin = {
    id: '@jupyterlab/codemirror-extension:languages',
    description: 'Provides the CodeMirror languages registry.',
    provides: codemirror_lib_index_js_.IEditorLanguageRegistry,
    optional: [translation_lib_index_js_.ITranslator],
    activate: (app, translator) => {
        const languages = new codemirror_lib_index_js_.EditorLanguageRegistry();
        // Register default languages
        for (const language of codemirror_lib_index_js_.EditorLanguageRegistry.getDefaultLanguages(translator)) {
            languages.addLanguage(language);
        }
        // Add Jupyter Markdown flavor here to support
        // code block highlighting.
        languages.addLanguage({
            name: 'ipythongfm',
            mime: 'text/x-ipythongfm',
            load: async () => {
                const [m, tex] = await Promise.all([
                    __webpack_require__.e(/* import() */ 252).then(__webpack_require__.t.bind(__webpack_require__, 252, 23)),
                    __webpack_require__.e(/* import() */ 311).then(__webpack_require__.bind(__webpack_require__, 60311))
                ]);
                return m.markdown({
                    base: m.markdownLanguage,
                    codeLanguages: (info) => languages.findBest(info),
                    extensions: [
                        (0,codemirror_lib_index_js_.parseMathIPython)(dist_index_js_.StreamLanguage.define(tex.stexMath).parser)
                    ]
                });
            }
        });
        return languages;
    }
};
/**
 * CodeMirror theme registry provider.
 */
const themePlugin = {
    id: '@jupyterlab/codemirror-extension:themes',
    description: 'Provides the CodeMirror theme registry',
    provides: codemirror_lib_index_js_.IEditorThemeRegistry,
    optional: [translation_lib_index_js_.ITranslator],
    activate: (app, translator) => {
        const themes = new codemirror_lib_index_js_.EditorThemeRegistry();
        // Register default themes
        for (const theme of codemirror_lib_index_js_.EditorThemeRegistry.getDefaultThemes(translator)) {
            themes.addTheme(theme);
        }
        return themes;
    }
};
/**
 * CodeMirror editor extensions registry provider.
 */
const extensionPlugin = {
    id: '@jupyterlab/codemirror-extension:extensions',
    description: 'Provides the CodeMirror extension factory registry.',
    provides: codemirror_lib_index_js_.IEditorExtensionRegistry,
    requires: [codemirror_lib_index_js_.IEditorThemeRegistry],
    optional: [translation_lib_index_js_.ITranslator, settingregistry_lib_index_js_.ISettingRegistry, ui_components_lib_index_js_.IFormRendererRegistry],
    activate: (app, themes, translator, settingRegistry, formRegistry) => {
        const registry = new codemirror_lib_index_js_.EditorExtensionRegistry();
        // Register default extensions
        for (const extensionFactory of codemirror_lib_index_js_.EditorExtensionRegistry.getDefaultExtensions({
            themes,
            translator
        })) {
            registry.addExtension(extensionFactory);
        }
        if (settingRegistry) {
            const updateSettings = (settings) => {
                var _a;
                registry.baseConfiguration =
                    (_a = settings.get('defaultConfig').composite) !== null && _a !== void 0 ? _a : {};
            };
            void Promise.all([
                settingRegistry.load(SETTINGS_ID),
                app.restored
            ]).then(([settings]) => {
                updateSettings(settings);
                settings.changed.connect(updateSettings);
            });
            formRegistry === null || formRegistry === void 0 ? void 0 : formRegistry.addRenderer(`${SETTINGS_ID}.defaultConfig`, {
                fieldRenderer: (props) => {
                    const properties = react_index_js_default().useMemo(() => registry.settingsSchema, []);
                    const defaultFormData = {};
                    // Only provide customizable options
                    for (const [key, value] of Object.entries(registry.defaultConfiguration)) {
                        if (typeof properties[key] !== 'undefined') {
                            defaultFormData[key] = value;
                        }
                    }
                    return (react_index_js_default().createElement("div", { className: "jp-FormGroup-contentNormal" },
                        react_index_js_default().createElement("h3", { className: "jp-FormGroup-fieldLabel jp-FormGroup-contentItem" }, props.schema.title),
                        props.schema.description && (react_index_js_default().createElement("div", { className: "jp-FormGroup-description" }, props.schema.description)),
                        react_index_js_default().createElement(ui_components_lib_index_js_.FormComponent, { schema: {
                                title: props.schema.title,
                                description: props.schema.description,
                                type: 'object',
                                properties,
                                additionalProperties: false
                            }, validator: (validator_ajv8_esm_js_default()), formData: { ...defaultFormData, ...props.formData }, formContext: { defaultFormData }, liveValidate: true, onChange: e => {
                                var _a;
                                // Only save non-default values
                                const nonDefault = {};
                                for (const [property, value] of Object.entries((_a = e.formData) !== null && _a !== void 0 ? _a : {})) {
                                    const default_ = defaultFormData[property];
                                    if (default_ === undefined ||
                                        !coreutils_dist_index_js_.JSONExt.deepEqual(value, default_)) {
                                        nonDefault[property] = value;
                                    }
                                }
                                props.onChange(nonDefault);
                            }, tagName: "div", translator: translator !== null && translator !== void 0 ? translator : translation_lib_index_js_.nullTranslator })));
                }
            });
        }
        return registry;
    }
};
/**
 * CodeMirror shared model binding provider.
 */
const bindingPlugin = {
    id: '@jupyterlab/codemirror-extension:binding',
    description: 'Register the CodeMirror extension factory binding the editor and the shared model.',
    autoStart: true,
    requires: [codemirror_lib_index_js_.IEditorExtensionRegistry],
    activate: (app, extensions) => {
        extensions.addExtension({
            name: 'shared-model-binding',
            factory: options => {
                var _a;
                const sharedModel = options.model.sharedModel;
                return codemirror_lib_index_js_.EditorExtensionRegistry.createImmutableExtension((0,codemirror_lib_index_js_.ybinding)({
                    ytext: sharedModel.ysource,
                    undoManager: (_a = sharedModel.undoManager) !== null && _a !== void 0 ? _a : undefined
                }));
            }
        });
    }
};
/**
 * The editor services.
 */
const servicesPlugin = {
    id: '@jupyterlab/codemirror-extension:services',
    description: 'Provides the service to instantiate CodeMirror editors.',
    provides: lib_index_js_.IEditorServices,
    requires: [
        codemirror_lib_index_js_.IEditorLanguageRegistry,
        codemirror_lib_index_js_.IEditorExtensionRegistry,
        codemirror_lib_index_js_.IEditorThemeRegistry
    ],
    optional: [translation_lib_index_js_.ITranslator],
    activate: (app, languages, extensions, translator) => {
        const factory = new codemirror_lib_index_js_.CodeMirrorEditorFactory({
            extensions,
            languages,
            translator: translator !== null && translator !== void 0 ? translator : translation_lib_index_js_.nullTranslator
        });
        return {
            factoryService: factory,
            mimeTypeService: new codemirror_lib_index_js_.CodeMirrorMimeTypeService(languages)
        };
    }
};

;// CONCATENATED MODULE: ../packages/codemirror-extension/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module codemirror-extension
 */





/**
 * A plugin providing a line/column status item to the application.
 */
const lineColItem = {
    id: '@jupyterlab/codemirror-extension:line-col-status',
    description: 'Provides the code editor cursor position model.',
    autoStart: true,
    requires: [translation_lib_index_js_.ITranslator],
    optional: [index_js_.ILabShell, statusbar_lib_index_js_.IStatusBar],
    provides: lib_index_js_.IPositionModel,
    activate: (app, translator, labShell, statusBar) => {
        const item = new lib_index_js_.LineCol(translator);
        const providers = new Set();
        if (statusBar) {
            // Add the status item to the status bar.
            statusBar.registerStatusItem(lineColItem.id, {
                item,
                align: 'right',
                rank: 2,
                isActive: () => !!item.model.editor
            });
        }
        const addEditorProvider = (provider) => {
            providers.add(provider);
            if (app.shell.currentWidget) {
                updateEditor(app.shell, {
                    newValue: app.shell.currentWidget,
                    oldValue: null
                });
            }
        };
        const update = () => {
            updateEditor(app.shell, {
                oldValue: app.shell.currentWidget,
                newValue: app.shell.currentWidget
            });
        };
        function updateEditor(shell, changes) {
            Promise.all([...providers].map(provider => provider(changes.newValue)))
                .then(editors => {
                var _a;
                item.model.editor =
                    (_a = editors.filter(editor => editor !== null)[0]) !== null && _a !== void 0 ? _a : null;
            })
                .catch(reason => {
                console.error('Get editors', reason);
            });
        }
        if (labShell) {
            labShell.currentChanged.connect(updateEditor);
        }
        return { addEditorProvider, update };
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [
    languagePlugin,
    themePlugin,
    bindingPlugin,
    extensionPlugin,
    servicesPlugin,
    lineColItem
];
/* harmony default export */ const lib = (plugins);


/***/ })

}]);
//# sourceMappingURL=129.63a9d7782543d6216af5.js.map?v=63a9d7782543d6216af5