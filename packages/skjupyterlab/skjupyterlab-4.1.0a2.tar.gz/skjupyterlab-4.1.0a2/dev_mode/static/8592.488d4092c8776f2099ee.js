"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[8592],{

/***/ 98592:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "default": () => (/* binding */ lib)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/notebook@~4.1.0-alpha.2 (singleton) (fallback: ../packages/notebook/lib/index.js)
var index_js_ = __webpack_require__(56916);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
var react_index_js_default = /*#__PURE__*/__webpack_require__.n(react_index_js_);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(16415);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
;// CONCATENATED MODULE: ../packages/celltags-extension/lib/celltag.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */




/**
 * The class name added to the cell-tags field.
 */
const CELL_TAGS_WIDGET_CLASS = 'jp-CellTags';
/**
 * The class name added to each tag element.
 */
const CELL_TAGS_ELEMENT_CLASS = 'jp-CellTags-Tag';
/**
 * The class name added to each applied tag element.
 */
const CELL_TAGS_ELEMENT_APPLIED_CLASS = 'jp-CellTags-Applied';
/**
 * The class name added to each unapplied tag element.
 */
const CELL_TAGS_ELEMENT_UNAPPLIED_CLASS = 'jp-CellTags-Unapplied';
/**
 * The class name added to the tag holder.
 */
const CELL_TAGS_HOLDER_CLASS = 'jp-CellTags-Holder';
/**
 * The class name added to the add-tag input.
 */
const CELL_TAGS_ADD_CLASS = 'jp-CellTags-Add';
/**
 * The class name added to an empty input.
 */
const CELL_TAGS_EMPTY_CLASS = 'jp-CellTags-Empty';
class CellTagField {
    constructor(tracker, translator) {
        this._tracker = tracker;
        this._translator = translator || translation_lib_index_js_.nullTranslator;
        this._trans = this._translator.load('jupyterlab');
        this._editing = false;
    }
    addTag(props, tag) {
        const data = props.formData;
        if (tag && !data.includes(tag)) {
            data.push(tag);
            props.formContext.updateMetadata({ [props.name]: data }, true);
        }
    }
    /**
     * Pull from cell metadata all the tags used in the notebook and update the
     * stored tag list.
     */
    pullTags() {
        var _a, _b;
        const notebook = (_a = this._tracker) === null || _a === void 0 ? void 0 : _a.currentWidget;
        const cells = (_b = notebook === null || notebook === void 0 ? void 0 : notebook.model) === null || _b === void 0 ? void 0 : _b.cells;
        if (cells === undefined) {
            return [];
        }
        const allTags = (0,index_es6_js_.reduce)(cells, (allTags, cell) => {
            var _a;
            const tags = (_a = cell.getMetadata('tags')) !== null && _a !== void 0 ? _a : [];
            return [...allTags, ...tags];
        }, []);
        return [...new Set(allTags)].filter(tag => tag !== '');
    }
    _emptyAddTag(target) {
        target.value = '';
        target.style.width = '';
        target.classList.add(CELL_TAGS_EMPTY_CLASS);
    }
    _onAddTagKeyDown(props, event) {
        const input = event.target;
        if (event.ctrlKey)
            return;
        if (event.key === 'Enter') {
            this.addTag(props, input.value);
        }
        else if (event.key === 'Escape') {
            this._emptyAddTag(input);
        }
    }
    _onAddTagFocus(event) {
        if (!this._editing) {
            event.target.blur();
        }
    }
    _onAddTagBlur(input) {
        if (this._editing) {
            this._editing = false;
            this._emptyAddTag(input);
        }
    }
    _onChange(event) {
        if (!event.target.value) {
            this._emptyAddTag(event.target);
        }
        else {
            event.target.classList.remove(CELL_TAGS_EMPTY_CLASS);
            const tmp = document.createElement('span');
            tmp.className = CELL_TAGS_ADD_CLASS;
            tmp.textContent = event.target.value;
            // set width to the pixel length of the text
            document.body.appendChild(tmp);
            event.target.style.setProperty('width', `calc(${tmp.getBoundingClientRect().width}px + var(--jp-add-tag-extra-width))`);
            document.body.removeChild(tmp);
        }
    }
    _onAddTagClick(props, event) {
        const elem = event.target.closest('div');
        const input = elem === null || elem === void 0 ? void 0 : elem.childNodes[0];
        if (!this._editing) {
            this._editing = true;
            input.value = '';
            input.focus();
        }
        else if (event.target !== input) {
            this.addTag(props, input.value);
        }
        event.preventDefault();
    }
    _onTagClick(props, tag) {
        const data = props.formData;
        if (data.includes(tag)) {
            data.splice(data.indexOf(tag), 1);
        }
        else {
            data.push(tag);
        }
        props.formContext.updateMetadata({ [props.name]: data }, true);
    }
    render(props) {
        const allTags = this.pullTags();
        return (react_index_js_default().createElement("div", { className: CELL_TAGS_WIDGET_CLASS },
            react_index_js_default().createElement("div", { className: "jp-FormGroup-fieldLabel jp-FormGroup-contentItem" }, "Cell Tags"),
            allTags &&
                allTags.map((tag, i) => (react_index_js_default().createElement("div", { key: i, className: `${CELL_TAGS_ELEMENT_CLASS} ${props.formData.includes(tag)
                        ? CELL_TAGS_ELEMENT_APPLIED_CLASS
                        : CELL_TAGS_ELEMENT_UNAPPLIED_CLASS}`, onClick: () => this._onTagClick(props, tag) },
                    react_index_js_default().createElement("div", { className: CELL_TAGS_HOLDER_CLASS },
                        react_index_js_default().createElement("span", null, tag),
                        props.formData.includes(tag) && (react_index_js_default().createElement(lib_index_js_.LabIcon.resolveReact, { icon: lib_index_js_.checkIcon, tag: "span", elementPosition: "center", height: "18px", width: "18px", marginLeft: "5px", marginRight: "-3px" })))))),
            react_index_js_default().createElement("div", { className: `${CELL_TAGS_ELEMENT_CLASS} ${CELL_TAGS_ELEMENT_UNAPPLIED_CLASS}` },
                react_index_js_default().createElement("div", { className: CELL_TAGS_HOLDER_CLASS, onMouseDown: (e) => this._onAddTagClick(props, e) },
                    react_index_js_default().createElement("input", { className: `${CELL_TAGS_ADD_CLASS} ${CELL_TAGS_EMPTY_CLASS}`, type: "text", placeholder: this._trans.__('Add Tag'), onKeyDown: (e) => this._onAddTagKeyDown(props, e), onFocus: (e) => this._onAddTagFocus(e), onBlur: (e) => this._onAddTagBlur(e.target), onChange: (e) => {
                            this._onChange(e);
                        } }),
                    react_index_js_default().createElement(lib_index_js_.LabIcon.resolveReact, { icon: lib_index_js_.addIcon, tag: "span", height: "18px", width: "18px", marginLeft: "5px", marginRight: "-3px" })))));
    }
}

;// CONCATENATED MODULE: ../packages/celltags-extension/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module celltags-extension
 */



/**
 * Registering cell tag field.
 */
const customCellTag = {
    id: '@jupyterlab/celltags-extension:plugin',
    description: 'Adds the cell tags editor.',
    autoStart: true,
    requires: [index_js_.INotebookTracker],
    optional: [lib_index_js_.IFormRendererRegistry],
    activate: (app, tracker, formRegistry) => {
        // Register the custom field
        if (formRegistry) {
            const component = {
                fieldRenderer: (props) => {
                    return new CellTagField(tracker).render(props);
                }
            };
            formRegistry.addRenderer('@jupyterlab/celltags-extension:plugin.renderer', component);
        }
    }
};
/* harmony default export */ const lib = ([customCellTag]);


/***/ })

}]);
//# sourceMappingURL=8592.488d4092c8776f2099ee.js.map?v=488d4092c8776f2099ee