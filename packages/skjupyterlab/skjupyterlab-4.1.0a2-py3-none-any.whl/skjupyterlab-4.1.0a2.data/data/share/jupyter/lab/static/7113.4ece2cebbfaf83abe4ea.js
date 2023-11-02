"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[7113],{

/***/ 57113:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(56916);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(89397);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(76351);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(22100);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_metadataform__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(20321);
/* harmony import */ var _jupyterlab_metadataform__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_metadataform__WEBPACK_IMPORTED_MODULE_5__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module metadataform-extension
 */






const PLUGIN_ID = '@jupyterlab/metadataform-extension:metadataforms';
var Private;
(function (Private) {
    async function loadSettingsMetadataForm(app, registry, notebookTools, translator, formComponentRegistry) {
        var _a;
        let canonical;
        let loaded = {};
        /**
         * Populate the plugin's schema defaults.
         */
        function populate(schema) {
            loaded = {};
            schema.properties.metadataforms.default = Object.keys(registry.plugins)
                .map(plugin => {
                var _a;
                const metadataForms = (_a = registry.plugins[plugin].schema['jupyter.lab.metadataforms']) !== null && _a !== void 0 ? _a : [];
                metadataForms.forEach(metadataForm => {
                    metadataForm._origin = plugin;
                });
                loaded[plugin] = metadataForms;
                return metadataForms;
            })
                .concat([schema['jupyter.lab.metadataforms']])
                .reduce((acc, val) => {
                // If a MetadataForm with the same ID already exists,
                // the metadataKeys will be concatenated to this MetadataForm's metadataKeys .
                // Otherwise, the whole MetadataForm will be pushed as a new form.
                val.forEach(value => {
                    const metadataForm = acc.find(addedValue => {
                        return addedValue.id === value.id;
                    });
                    if (metadataForm) {
                        // TODO do insertion of metadataSchema properties in a generic way.
                        // Currently this only support 'properties', 'allOf' and 'required'.
                        //  - add or replace entries if it is an object.
                        //  - concat if it is an array.
                        //  - replace if it is a primitive ?
                        // Includes new metadataKey in the existing metadataSchema.
                        // Overwrites if the metadataKey already exists.
                        for (let [metadataKey, properties] of Object.entries(value.metadataSchema.properties)) {
                            metadataForm.metadataSchema.properties[metadataKey] =
                                properties;
                        }
                        // Includes required fields.
                        if (value.metadataSchema.required) {
                            if (!metadataForm.metadataSchema.required) {
                                metadataForm.metadataSchema.required =
                                    value.metadataSchema.required;
                            }
                            else {
                                metadataForm.metadataSchema.required.concat(value.metadataSchema.required);
                            }
                        }
                        // Includes allOf array in the existing metadataSchema.
                        if (value.metadataSchema.allOf) {
                            if (!metadataForm.metadataSchema.allOf) {
                                metadataForm.metadataSchema.allOf =
                                    value.metadataSchema.allOf;
                            }
                            else {
                                metadataForm.metadataSchema.allOf.concat(value.metadataSchema.allOf);
                            }
                        }
                        // Includes uiSchema in the existing uiSchema.
                        // Overwrites if the uiSchema already exists for that metadataKey.
                        if (value.uiSchema) {
                            if (!metadataForm.uiSchema)
                                metadataForm.uiSchema = {};
                            for (let [metadataKey, ui] of Object.entries(value.uiSchema)) {
                                metadataForm.uiSchema[metadataKey] = ui;
                            }
                        }
                        // Includes metadataOptions in the existing uiSchema.
                        // Overwrites if options already exists for that metadataKey.
                        if (value.metadataOptions) {
                            if (!metadataForm.metadataOptions)
                                metadataForm.metadataOptions = {};
                            for (let [metadataKey, options] of Object.entries(value.metadataOptions)) {
                                metadataForm.metadataOptions[metadataKey] = options;
                            }
                        }
                    }
                    else {
                        acc.push(value);
                    }
                });
                return acc;
            }, []); // flatten one level;
        }
        // Transform the plugin object to return different schema than the default.
        registry.transform(PLUGIN_ID, {
            compose: plugin => {
                var _a, _b, _c, _d;
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.JSONExt.deepCopy(plugin.schema);
                    populate(canonical);
                }
                const defaults = (_c = (_b = (_a = canonical.properties) === null || _a === void 0 ? void 0 : _a.metadataforms) === null || _b === void 0 ? void 0 : _b.default) !== null && _c !== void 0 ? _c : [];
                const user = {
                    metadataforms: (_d = plugin.data.user.metadataforms) !== null && _d !== void 0 ? _d : []
                };
                const composite = {
                    metadataforms: defaults.concat(user.metadataforms)
                };
                plugin.data = { composite, user };
                return plugin;
            },
            fetch: plugin => {
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.JSONExt.deepCopy(plugin.schema);
                    populate(canonical);
                }
                return {
                    data: plugin.data,
                    id: plugin.id,
                    raw: plugin.raw,
                    schema: canonical,
                    version: plugin.version
                };
            }
        });
        // Repopulate the canonical variable after the setting registry has
        // preloaded all initial plugins.
        canonical = null;
        const settings = await registry.load(PLUGIN_ID);
        const metadataForms = new _jupyterlab_metadataform__WEBPACK_IMPORTED_MODULE_5__.MetadataFormProvider();
        // Creates all the forms from extensions settings.
        for (let schema of settings.composite
            .metadataforms) {
            let metaInformation = {};
            let metadataSchema = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.JSONExt.deepCopy(schema.metadataSchema);
            let uiSchema = {};
            if (schema.uiSchema) {
                uiSchema = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.JSONExt.deepCopy(schema.uiSchema);
            }
            for (let [metadataKey, properties] of Object.entries(metadataSchema.properties)) {
                if (properties.default) {
                    if (!metaInformation[metadataKey])
                        metaInformation[metadataKey] = {};
                    metaInformation[metadataKey].default = properties.default;
                }
            }
            if (schema.metadataOptions) {
                for (let [metadataKey, options] of Object.entries(schema.metadataOptions)) {
                    // Optionally links key to cell type.
                    if (options.cellTypes) {
                        if (!metaInformation[metadataKey])
                            metaInformation[metadataKey] = {};
                        metaInformation[metadataKey].cellTypes = options.cellTypes;
                    }
                    // Optionally links key to metadata level.
                    if (options.metadataLevel) {
                        if (!metaInformation[metadataKey])
                            metaInformation[metadataKey] = {};
                        metaInformation[metadataKey].level = options.metadataLevel;
                    }
                    // Optionally set the writeDefault flag.
                    if (options.writeDefault !== undefined) {
                        if (!metaInformation[metadataKey])
                            metaInformation[metadataKey] = {};
                        metaInformation[metadataKey].writeDefault = options.writeDefault;
                    }
                    // Optionally links key to a custom widget.
                    if (options.customRenderer) {
                        const component = formComponentRegistry.getRenderer(options.customRenderer);
                        // If renderer is defined (custom widget has been registered), set it as used widget.
                        if (component !== undefined) {
                            if (!uiSchema[metadataKey])
                                uiSchema[metadataKey] = {};
                            if (component.fieldRenderer) {
                                uiSchema[metadataKey]['ui:field'] = component.fieldRenderer;
                            }
                            else {
                                uiSchema[metadataKey]['ui:widget'] = component.widgetRenderer;
                            }
                        }
                    }
                }
            }
            // Adds a section to notebookTools.
            notebookTools.addSection({
                sectionName: schema.id,
                rank: schema.rank,
                label: (_a = schema.label) !== null && _a !== void 0 ? _a : schema.id
            });
            // Creates the tool.
            const tool = new _jupyterlab_metadataform__WEBPACK_IMPORTED_MODULE_5__.MetadataFormWidget({
                metadataSchema: metadataSchema,
                metaInformation: metaInformation,
                uiSchema: uiSchema,
                pluginId: schema._origin,
                translator: translator,
                showModified: schema.showModified
            });
            // Adds the form to the section.
            notebookTools.addItem({ section: schema.id, tool: tool });
            metadataForms.add(schema.id, tool);
        }
        return metadataForms;
    }
    Private.loadSettingsMetadataForm = loadSettingsMetadataForm;
})(Private || (Private = {}));
/**
 * The metadata form plugin.
 */
const metadataForm = {
    id: PLUGIN_ID,
    description: 'Provides the metadata form registry.',
    autoStart: true,
    requires: [
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTools,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.ITranslator,
        _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.IFormRendererRegistry,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry
    ],
    provides: _jupyterlab_metadataform__WEBPACK_IMPORTED_MODULE_5__.IMetadataFormProvider,
    activate: async (app, notebookTools, translator, componentsRegistry, settings) => {
        return await Private.loadSettingsMetadataForm(app, settings, notebookTools, translator, componentsRegistry);
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (metadataForm);


/***/ })

}]);
//# sourceMappingURL=7113.4ece2cebbfaf83abe4ea.js.map?v=4ece2cebbfaf83abe4ea