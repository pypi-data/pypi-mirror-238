"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[6841,9867],{

/***/ 9867:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "FormWidget": () => (/* reexport */ FormWidget),
  "IMetadataFormProvider": () => (/* reexport */ IMetadataFormProvider),
  "MetadataFormProvider": () => (/* reexport */ MetadataFormProvider),
  "MetadataFormWidget": () => (/* reexport */ MetadataFormWidget)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @rjsf/validator-ajv8@^5.1.0 (strict) (fallback: ../node_modules/@rjsf/validator-ajv8/dist/validator-ajv8.esm.js)
var validator_ajv8_esm_js_ = __webpack_require__(89319);
var validator_ajv8_esm_js_default = /*#__PURE__*/__webpack_require__.n(validator_ajv8_esm_js_);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
var react_index_js_default = /*#__PURE__*/__webpack_require__.n(react_index_js_);
;// CONCATENATED MODULE: ../packages/metadataform/lib/form.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module metadataform
 */




/**
 * A ReactWidget with the form itself.
 */
class FormWidget extends index_js_.ReactWidget {
    /**
     * Constructs a new FormWidget.
     */
    constructor(props) {
        super();
        this.addClass('jp-FormWidget');
        this._props = props;
    }
    /**
     * Render the form.
     * @returns - The rendered form
     */
    render() {
        const formContext = {
            defaultFormData: this._props.settings.default(),
            updateMetadata: this._props.metadataFormWidget.updateMetadata
        };
        return (react_index_js_default().createElement(lib_index_js_.FormComponent, { validator: (validator_ajv8_esm_js_default()), schema: this._props.properties, formData: this._props.formData, formContext: formContext, uiSchema: this._props.uiSchema, liveValidate: true, idPrefix: `jp-MetadataForm-${this._props.pluginId}`, onChange: (e) => {
                this._props.metadataFormWidget.updateMetadata(e.formData || {});
            }, compact: true, showModifiedFromDefault: this._props.showModified, translator: this._props.translator }));
    }
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/notebook@~4.1.0-alpha.2 (singleton) (fallback: ../packages/notebook/lib/index.js)
var notebook_lib_index_js_ = __webpack_require__(56916);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/settingregistry@~4.1.0-alpha.2 (singleton) (fallback: ../packages/settingregistry/lib/index.js)
var settingregistry_lib_index_js_ = __webpack_require__(89397);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/metadataform/lib/metadataform.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module metadataform
 */






/**
 * A class that create a metadata form widget
 */
class MetadataFormWidget extends notebook_lib_index_js_.NotebookTools.Tool {
    /**
     * Construct an empty widget.
     */
    constructor(options) {
        super();
        /**
         * Update the metadata of the current cell or notebook.
         *
         * @param formData - the cell metadata set in the form.
         * @param reload - whether to update the form after updating the metadata.
         *
         * ## Notes
         * Metadata are updated from root only. If some metadata is nested,
         * the whole root object must be updated.
         * This function build an object with all the root object to update
         * in metadata before performing update.
         * It uses an arrow function to allow using 'this' properly when called from a custom field.
         */
        this.updateMetadata = (formData, reload) => {
            var _a, _b, _c, _d, _e, _f, _g, _h;
            if (this.notebookTools == undefined)
                return;
            const notebook = this.notebookTools.activeNotebookPanel;
            const cell = this.notebookTools.activeCell;
            if (cell == null)
                return;
            this._updatingMetadata = true;
            // An object representing the cell metadata to modify.
            const cellMetadataObject = {};
            // An object representing the notebook metadata to modify.
            const notebookMetadataObject = {};
            for (let [metadataKey, value] of Object.entries(formData)) {
                // Continue if the metadataKey does not exist in schema.
                if (!this.metadataKeys.includes(metadataKey))
                    continue;
                // Continue if the metadataKey is a notebook level one and there is no NotebookModel.
                if (((_a = this._metaInformation[metadataKey]) === null || _a === void 0 ? void 0 : _a.level) === 'notebook' &&
                    this._notebookModelNull)
                    continue;
                // Continue if the metadataKey is not applicable to the cell type.
                if (((_b = this._metaInformation[metadataKey]) === null || _b === void 0 ? void 0 : _b.cellTypes) &&
                    !((_d = (_c = this._metaInformation[metadataKey]) === null || _c === void 0 ? void 0 : _c.cellTypes) === null || _d === void 0 ? void 0 : _d.includes(cell.model.type))) {
                    continue;
                }
                let currentMetadata;
                let metadataObject;
                // Linking the working variable to the corresponding metadata and representation.
                if (((_e = this._metaInformation[metadataKey]) === null || _e === void 0 ? void 0 : _e.level) === 'notebook') {
                    // Working on notebook metadata.
                    currentMetadata = notebook.model.metadata;
                    metadataObject = notebookMetadataObject;
                }
                else {
                    // Working on cell metadata.
                    currentMetadata = cell.model.metadata;
                    metadataObject = cellMetadataObject;
                }
                // Remove first and last '/' if necessary and split the path.
                let nestedKey = metadataKey
                    .replace(/^\/+/, '')
                    .replace(/\/+$/, '')
                    .split('/');
                let baseMetadataKey = nestedKey[0];
                if (baseMetadataKey == undefined)
                    continue;
                let writeFinalData = value !== undefined &&
                    (((_g = (_f = this._metaInformation[metadataKey]) === null || _f === void 0 ? void 0 : _f.writeDefault) !== null && _g !== void 0 ? _g : true) ||
                        value !== ((_h = this._metaInformation[metadataKey]) === null || _h === void 0 ? void 0 : _h.default));
                // If metadata key is at root of metadata no need to go further.
                if (nestedKey.length == 1) {
                    if (writeFinalData)
                        metadataObject[baseMetadataKey] = value;
                    else
                        metadataObject[baseMetadataKey] = undefined;
                    continue;
                }
                let intermediateMetadataKeys = nestedKey.slice(1, -1);
                let finalMetadataKey = nestedKey[nestedKey.length - 1];
                // Deep copy of the metadata if not already done.
                if (!(baseMetadataKey in metadataObject)) {
                    metadataObject[baseMetadataKey] = currentMetadata[baseMetadataKey];
                }
                if (metadataObject[baseMetadataKey] === undefined)
                    metadataObject[baseMetadataKey] = {};
                // Let's have an object which points to the nested key.
                let workingObject = metadataObject[baseMetadataKey];
                let finalObjectReached = true;
                for (let nested of intermediateMetadataKeys) {
                    // If one of the nested object does not exist, this object is created
                    // only if there is a final data to write.
                    if (!(nested in workingObject)) {
                        if (!writeFinalData) {
                            finalObjectReached = false;
                            break;
                        }
                        else
                            workingObject[nested] = {};
                    }
                    workingObject = workingObject[nested];
                }
                // Write the value to the nested key or remove all empty object before the nested key,
                // only if the final object has been reached.
                if (finalObjectReached) {
                    if (!writeFinalData)
                        delete workingObject[finalMetadataKey];
                    else
                        workingObject[finalMetadataKey] = value;
                }
                // If the final nested data has been deleted, let see if there is not remaining
                // empty objects to remove.
                if (!writeFinalData) {
                    metadataObject[baseMetadataKey] = Private.deleteEmptyNested(metadataObject[baseMetadataKey], nestedKey.slice(1));
                    if (!Object.keys(metadataObject[baseMetadataKey])
                        .length)
                        metadataObject[baseMetadataKey] = undefined;
                }
            }
            // Set the cell metadata or delete it if value is undefined or empty object.
            for (let [key, value] of Object.entries(cellMetadataObject)) {
                if (value === undefined)
                    cell.model.deleteMetadata(key);
                else
                    cell.model.setMetadata(key, value);
            }
            // Set the notebook metadata or delete it if value is undefined or empty object.
            if (!this._notebookModelNull) {
                for (let [key, value] of Object.entries(notebookMetadataObject)) {
                    if (value === undefined)
                        notebook.model.deleteMetadata(key);
                    else
                        notebook.model.setMetadata(key, value);
                }
            }
            this._updatingMetadata = false;
            if (reload) {
                this._update();
            }
        };
        this._notebookModelNull = false;
        this._metadataSchema = options.metadataSchema;
        this._metaInformation = options.metaInformation;
        this._uiSchema = options.uiSchema || {};
        this._pluginId = options.pluginId;
        this._showModified = options.showModified || false;
        this.translator = options.translator || translation_lib_index_js_.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this._updatingMetadata = false;
        const layout = (this.layout = new index_es6_js_.SingletonLayout());
        const node = document.createElement('div');
        const content = document.createElement('div');
        content.textContent = this._trans.__('No metadata.');
        content.className = 'jp-MetadataForm-placeholderContent';
        node.appendChild(content);
        this._placeholder = new index_es6_js_.Widget({ node });
        this._placeholder.addClass('jp-MetadataForm-placeholder');
        layout.widget = this._placeholder;
    }
    /**
     * Get the form object itself.
     */
    get form() {
        return this._form;
    }
    /**
     * Get the list of existing metadataKey (array of string).
     *
     * ## NOTE:
     * The list contains also the conditional fields, which are not necessary
     * displayed and filled.
     */
    get metadataKeys() {
        var _a;
        const metadataKeys = [];
        // MetadataKey from schema.
        for (let metadataKey of Object.keys(this._metadataSchema.properties)) {
            metadataKeys.push(metadataKey);
        }
        // Possible additional metadataKeys from conditional schema.
        (_a = this._metadataSchema.allOf) === null || _a === void 0 ? void 0 : _a.forEach(conditional => {
            if (conditional.then !== undefined) {
                if (conditional.then.properties !== undefined) {
                    let properties = conditional.then
                        .properties;
                    for (let metadataKey of Object.keys(properties)) {
                        if (!metadataKeys.includes(metadataKey))
                            metadataKeys.push(metadataKey);
                    }
                }
            }
            if (conditional.else !== undefined) {
                if (conditional.else.properties !== undefined) {
                    let properties = conditional.else
                        .properties;
                    for (let metadataKey of Object.keys(properties)) {
                        if (!metadataKeys.includes(metadataKey))
                            metadataKeys.push(metadataKey);
                    }
                }
            }
        });
        return metadataKeys;
    }
    /**
     * Get the properties of a MetadataKey.
     *
     * @param metadataKey - metadataKey (string).
     */
    getProperties(metadataKey) {
        return (dist_index_js_.JSONExt.deepCopy(this._metadataSchema.properties[metadataKey]) || null);
    }
    /**
     * Set properties to a metadataKey.
     *
     * @param metadataKey - metadataKey (string).
     * @param properties - the properties to add or modify.
     */
    setProperties(metadataKey, properties) {
        Object.entries(properties).forEach(([key, value]) => {
            this._metadataSchema.properties[metadataKey][key] = value;
        });
    }
    /**
     * Set the content of the widget.
     */
    setContent(content) {
        const layout = this.layout;
        if (layout.widget) {
            layout.widget.removeClass('jp-MetadataForm-content');
            layout.removeWidget(layout.widget);
        }
        if (!content) {
            content = this._placeholder;
        }
        content.addClass('jp-MetadataForm-content');
        layout.widget = content;
    }
    /**
     * Build widget.
     */
    buildWidget(props) {
        this._form = new FormWidget(props);
        this._form.addClass('jp-MetadataForm');
        this.setContent(this._form);
    }
    /**
     * Update the form when the widget is displayed.
     */
    onAfterShow(msg) {
        this._update();
    }
    /**
     * Handle a change to the active cell.
     */
    onActiveCellChanged(msg) {
        if (this.isVisible)
            this._update();
    }
    /**
     * Handle a change to the active cell metadata.
     */
    onActiveCellMetadataChanged(_) {
        if (!this._updatingMetadata && this.isVisible)
            this._update();
    }
    /**
     * Handle when the active notebook panel changes.
     */
    onActiveNotebookPanelChanged(_) {
        const notebook = this.notebookTools.activeNotebookPanel;
        this._notebookModelNull = notebook === null || notebook.model === null;
        if (!this._updatingMetadata && this.isVisible)
            this._update();
    }
    /**
     * Handle a change to the active notebook metadata.
     */
    onActiveNotebookPanelMetadataChanged(msg) {
        if (!this._updatingMetadata && this.isVisible)
            this._update();
    }
    /**
     * Update the form with current cell metadata, and remove inconsistent fields.
     */
    _update() {
        var _a, _b, _c, _d, _e;
        const notebook = this.notebookTools.activeNotebookPanel;
        const cell = this.notebookTools.activeCell;
        if (cell == undefined)
            return;
        const formProperties = dist_index_js_.JSONExt.deepCopy(this._metadataSchema);
        const formData = {};
        for (let metadataKey of Object.keys(this._metadataSchema.properties || dist_index_js_.JSONExt.emptyObject)) {
            // Do not display the field if it's Notebook metadata and the notebook model is null.
            if (((_a = this._metaInformation[metadataKey]) === null || _a === void 0 ? void 0 : _a.level) === 'notebook' &&
                this._notebookModelNull) {
                delete formProperties.properties[metadataKey];
                continue;
            }
            // Do not display the field if the active cell's type is not involved.
            if (((_b = this._metaInformation[metadataKey]) === null || _b === void 0 ? void 0 : _b.cellTypes) &&
                !((_d = (_c = this._metaInformation[metadataKey]) === null || _c === void 0 ? void 0 : _c.cellTypes) === null || _d === void 0 ? void 0 : _d.includes(cell.model.type))) {
                delete formProperties.properties[metadataKey];
                continue;
            }
            let workingObject;
            // Remove the first and last '/' if exist, nad split the path.
            let nestedKeys = metadataKey
                .replace(/^\/+/, '')
                .replace(/\/+$/, '')
                .split('/');
            // Associates the correct metadata object to the working object.
            if (((_e = this._metaInformation[metadataKey]) === null || _e === void 0 ? void 0 : _e.level) === 'notebook') {
                workingObject = notebook.model.metadata;
            }
            else {
                workingObject = cell.model.metadata;
            }
            let hasValue = true;
            // Navigate to the value.
            for (let nested of nestedKeys) {
                if (nested in workingObject)
                    workingObject = workingObject[nested];
                else {
                    hasValue = false;
                    break;
                }
            }
            // Fill the formData with the current metadata value.
            if (hasValue)
                formData[metadataKey] = workingObject;
        }
        this.buildWidget({
            properties: formProperties,
            settings: new settingregistry_lib_index_js_.BaseSettings({
                schema: this._metadataSchema
            }),
            uiSchema: this._uiSchema,
            translator: this.translator || null,
            formData: formData,
            metadataFormWidget: this,
            showModified: this._showModified,
            pluginId: this._pluginId
        });
    }
}
var Private;
(function (Private) {
    /**
     * Recursive function to clean the empty nested metadata before updating real metadata.
     * this function is called when a nested metadata is undefined (or default), so maybe some
     * object are now empty.
     * @param metadataObject: PartialJSONObject representing the metadata to update.
     * @param metadataKeysList: Array<string> of the undefined nested metadata.
     * @returns PartialJSONObject without empty object.
     */
    function deleteEmptyNested(metadataObject, metadataKeysList) {
        let metadataKey = metadataKeysList.shift();
        if (metadataKey !== undefined && metadataKey in metadataObject) {
            if (Object.keys(metadataObject[metadataKey]).length)
                metadataObject[metadataKey] = deleteEmptyNested(metadataObject[metadataKey], metadataKeysList);
            if (!Object.keys(metadataObject[metadataKey]).length)
                delete metadataObject[metadataKey];
        }
        return metadataObject;
    }
    Private.deleteEmptyNested = deleteEmptyNested;
})(Private || (Private = {}));

;// CONCATENATED MODULE: ../packages/metadataform/lib/metadataformProvider.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */
class MetadataFormProvider {
    constructor() {
        this._items = {};
    }
    add(id, widget) {
        if (!this._items[id]) {
            this._items[id] = widget;
        }
        else {
            console.warn(`A MetadataformWidget is already registered with id ${id}`);
        }
    }
    get(id) {
        if (this._items[id]) {
            return this._items[id];
        }
        else {
            console.warn(`There is no MetadataformWidget registered with id ${id}`);
        }
    }
}

;// CONCATENATED MODULE: ../packages/metadataform/lib/token.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module metadataform
 */

/**
 * The metadata form provider token.
 */
const IMetadataFormProvider = new dist_index_js_.Token('@jupyterlab/metadataform:IMetadataFormProvider', `A service to register new metadata editor widgets.`);

;// CONCATENATED MODULE: ../packages/metadataform/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module metadataform
 */






/***/ })

}]);
//# sourceMappingURL=6841.064a36e50928297737d3.js.map?v=064a36e50928297737d3